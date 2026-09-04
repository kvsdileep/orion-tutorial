"""Lesson 3: plan, code, test, AI review, human review, apply, verify.

Tests are the primary check. The AI reviewer sees the code and the test
output with fresh context and gives a second opinion. The human sees both
and decides. A reject carries a reason back to the coder and resets the
counters so the reviewer is consulted again.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Literal, TypedDict

from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import interrupt

from orion_agent.rules import load_rules
from orion_agent.sandbox import Sandbox
from orion_agent.schemas import CodeResult, Plan, ReviewResult
from orion_agent.search import repo_map
from orion_agent.workspace import Workspace, WorkspaceError


class OrchestratorState(TypedDict, total=False):
    """Everything the plan-code-test-review-apply run carries between nodes."""

    feature_request: str
    codebase_context: str
    plan: str
    file_tasks: list[dict]
    generated_code: list[dict]
    test_output: str
    test_attempts: int
    review_result: str
    review_attempts: int
    human_decision: str
    human_feedback: str
    status: str
    error: str


RESEARCH_PROMPT = (
    "You are researching a codebase before a change is planned. Use the tools to find every file "
    "and symbol relevant to this request, read them, and finish with a short summary of what you found.\n\n"
    "Request: {request}"
)

PLAN_PROMPT = (
    "Create an implementation plan for this feature request. List every file to create or modify.\n\n"
    "Request: {request}\n\nCodebase context:\n{context}"
)


def check_task_paths(ws: Workspace, file_tasks: list[dict]) -> list[str]:
    """Return one message per planned filepath that the workspace would refuse to write."""
    problems = []
    for task in file_tasks:
        filepath = task.get("filepath") or ""
        if not filepath:
            problems.append("a file task has no filepath")
            continue
        try:
            full = ws.resolve(filepath)
        except WorkspaceError as exc:
            problems.append(str(exc))
            continue
        if full.is_dir():
            problems.append(f"filepath is a directory: {filepath}")
    return problems


def build_code_prompt(state: dict, task: dict, rules_root: str | Path | None = None) -> str:
    """Build the coder prompt for one file task, folding in rules and the latest feedback."""
    parts = [
        "Generate the complete Python code for this file.\n\n"
        f"File: {task['filepath']}\nAction: {task['action']}\nDescription: {task['description']}"
    ]
    if rules_root:
        rules = load_rules(rules_root, task["filepath"])
        if rules:
            parts.append(f"Follow these rules:\n{rules}")
    parts.append(f"Codebase context:\n{state.get('codebase_context', '')}")
    if state.get("test_output") and state.get("status") in ("tests_failed", "human_rejected"):
        # After a human reject the tests may well have passed, so only the failure path says "fix".
        label = "Test output from the last run"
        if state["status"] == "tests_failed":
            label += " (fix these failures)"
        parts.append(f"{label}:\n{state['test_output']}")
    if state.get("status") == "needs_revision" and state.get("review_result"):
        parts.append(f"Reviewer feedback (address every point):\n{state['review_result']}")
    if state.get("human_feedback"):
        parts.append(f"Human feedback (this overrides everything else):\n{state['human_feedback']}")
    return "\n\n".join(parts)


def build_review_prompt(state: dict) -> str:
    """Build the reviewer prompt: the generated files and the test output, with no history."""
    files = "\n\n".join(f"### {g['filepath']}\n{g['code']}" for g in state.get("generated_code", []))
    return (
        "You are a code reviewer with no memory of how this code was written. Judge only what is in front of you.\n"
        f"Feature request: {state.get('feature_request', '')}\n\nFiles:\n{files}\n\n"
        f"Test output:\n{state.get('test_output', '')}\n\n"
        "Approve only if the code is correct, complete, and follows PEP 8 with type hints and docstrings."
    )


def run_tests(ws: Workspace, sandbox: Sandbox, changed: list[str]) -> tuple[str, bool]:
    """Run the workspace's pytest suite, or smoke-import the changed files, and say whether it passed."""
    test_files = sorted(set(ws.glob("**/test_*.py")) | set(ws.glob("tests/**/*.py")))
    if test_files:
        r = sandbox.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"], cwd=ws.root, timeout=120)
        return r.summary(), r.ok
    lines = []
    ok = True
    for path in changed:
        if not path.endswith(".py"):
            continue
        module = Path(path).with_suffix("").as_posix().replace("/", ".")
        r = sandbox.run_python(f"import {module}", cwd=ws.root)
        ok = ok and r.ok
        lines.append(f"Smoke import {module}: {'OK' if r.ok else 'FAILED'}" + ("" if r.ok else f"\n{r.stderr.rstrip()}"))
    return "\n".join(lines) if lines else "No Python files changed; nothing to test.", ok


def build_orchestrator(
    planner,
    coder,
    reviewer,
    ws: Workspace,
    sandbox: Sandbox,
    *,
    planner_agent=None,
    rules_root: str | Path | None = None,
    checkpointer=None,
    max_test_attempts: int = 3,
    max_review_attempts: int = 2,
) -> CompiledStateGraph:
    """Compile the full orchestrator: plan, code, test, AI review, human gate, apply, verify."""

    async def plan_node(state: OrchestratorState) -> dict:
        request = state["feature_request"]
        context = repo_map(ws)
        if planner_agent is not None:
            research = await planner_agent.ainvoke({"messages": [HumanMessage(content=RESEARCH_PROMPT.format(request=request))]})
            notes = [str(m.content) for m in research["messages"] if isinstance(m, ToolMessage)]
            summary = str(research["messages"][-1].content)
            context = "\n\n".join([context, *notes, f"Research summary:\n{summary}"])
        plan: Plan = planner.invoke(PLAN_PROMPT.format(request=request, context=context))
        file_tasks = [t.model_dump() for t in plan.file_tasks]
        problems = check_task_paths(ws, file_tasks)
        return {
            "codebase_context": context,
            "plan": plan.summary,
            "file_tasks": file_tasks,
            "status": "path_rejected" if problems else "planned",
            "error": "\n".join(problems),
            "test_attempts": 0,
            "review_attempts": 0,
            "human_feedback": "",
        }

    def route_after_plan(state: OrchestratorState) -> Literal["code", "__end__"]:
        return END if state["status"] == "path_rejected" else "code"

    def code_node(state: OrchestratorState) -> dict:
        generated = []
        for task in state["file_tasks"]:
            result: CodeResult = coder.invoke(build_code_prompt(state, task, rules_root))
            generated.append({"filepath": task["filepath"], "code": result.code, "explanation": result.explanation})
        return {"generated_code": generated, "status": "coded"}

    def test_node(state: OrchestratorState) -> dict:
        snapshot = ws.snapshot()
        try:
            scratch = Workspace(snapshot)
            for item in state["generated_code"]:
                scratch.write(item["filepath"], item["code"])
            output, ok = run_tests(scratch, sandbox, [i["filepath"] for i in state["generated_code"]])
        except (WorkspaceError, OSError) as exc:
            return {"error": str(exc), "status": "path_rejected"}
        finally:
            shutil.rmtree(snapshot, ignore_errors=True)
        return {
            "test_output": output,
            "test_attempts": state.get("test_attempts", 0) + 1,
            "status": "tests_passed" if ok else "tests_failed",
        }

    def route_after_test(state: OrchestratorState) -> Literal["ai_review", "code", "human_review", "__end__"]:
        if state["status"] == "path_rejected":
            return END
        if state["status"] == "tests_passed":
            return "ai_review"
        if state["test_attempts"] < max_test_attempts:
            return "code"
        return "human_review"

    def ai_review_node(state: OrchestratorState) -> dict:
        attempts = state.get("review_attempts", 0) + 1
        review: ReviewResult = reviewer.invoke(build_review_prompt(state))
        if review.approved:
            return {"review_result": review.feedback, "review_attempts": attempts, "status": "approved"}
        if attempts >= max_review_attempts:
            return {
                "review_result": f"auto-approved after {max_review_attempts} rejections. Last feedback: {review.feedback}",
                "review_attempts": attempts,
                "status": "approved",
            }
        return {"review_result": review.feedback, "review_attempts": attempts, "status": "needs_revision"}

    def route_after_review(state: OrchestratorState) -> Literal["human_review", "code"]:
        return "human_review" if state["status"] == "approved" else "code"

    def human_review_node(state: OrchestratorState) -> dict:
        payload = {
            "plan": state.get("plan", ""),
            "changes": [
                {"filepath": g["filepath"], "explanation": g["explanation"], "preview": g["code"][:500]}
                for g in state.get("generated_code", [])
            ],
            "test_output": state.get("test_output", ""),
            "review_result": state.get("review_result", ""),
        }
        decision = interrupt(payload)
        if isinstance(decision, str):
            decision = {"decision": decision, "feedback": ""}
        if decision.get("decision") == "approve":
            return {"human_decision": "approve", "status": "human_approved"}
        return {
            "human_decision": "reject",
            "human_feedback": decision.get("feedback", ""),
            "review_attempts": 0,
            "test_attempts": 0,
            "status": "human_rejected",
        }

    def route_after_human(state: OrchestratorState) -> Literal["apply", "code"]:
        return "apply" if state["human_decision"] == "approve" else "code"

    def apply_node(state: OrchestratorState) -> dict:
        for item in state["generated_code"]:
            try:
                ws.write(item["filepath"], item["code"])
            except (WorkspaceError, OSError) as exc:
                return {"error": str(exc), "status": "apply_failed"}
        return {"status": "applied"}

    def verify_node(state: OrchestratorState) -> dict:
        if state["status"] == "apply_failed":
            return {}
        output, ok = run_tests(ws, sandbox, [i["filepath"] for i in state["generated_code"]])
        return {"test_output": output, "status": "done" if ok else "verify_failed"}

    graph = StateGraph(OrchestratorState)
    graph.add_node("plan", plan_node)
    graph.add_node("code", code_node)
    graph.add_node("test", test_node)
    graph.add_node("ai_review", ai_review_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("apply", apply_node)
    graph.add_node("verify", verify_node)
    graph.add_edge(START, "plan")
    graph.add_conditional_edges("plan", route_after_plan, {"code": "code", END: END})
    graph.add_edge("code", "test")
    graph.add_conditional_edges("test", route_after_test, {"ai_review": "ai_review", "code": "code", "human_review": "human_review", END: END})
    graph.add_conditional_edges("ai_review", route_after_review, {"human_review": "human_review", "code": "code"})
    graph.add_conditional_edges("human_review", route_after_human, {"apply": "apply", "code": "code"})
    graph.add_edge("apply", "verify")
    graph.add_edge("verify", END)
    return graph.compile(checkpointer=checkpointer)
