"""Lesson 2: generate, execute, retry on error; then add a reviewer."""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from orion_agent.sandbox import Sandbox
from orion_agent.schemas import CodeOutput, ReviewResult


class AgentState(TypedDict, total=False):
    task: str
    code: str
    explanation: str
    execution_result: str
    error: str
    attempts: int
    max_attempts: int
    status: str
    rules: str


class FullAgentState(AgentState, total=False):
    review_feedback: str
    approved: bool


def _generate_prompt(state: dict) -> str:
    prompt = f"Write Python code for: {state['task']}"
    if state.get("rules"):
        prompt = f"Follow these rules:\n{state['rules']}\n\n{prompt}"
    if state.get("error"):
        prompt += f"\n\nThe previous attempt failed with this error. Fix it:\n{state['error']}"
    if state.get("review_feedback") and not state.get("approved", True):
        prompt += f"\n\nThe reviewer rejected the previous version. Address this feedback:\n{state['review_feedback']}"
    return prompt


def _make_nodes(coder, sandbox: Sandbox, timeout: float):
    def generate(state: dict) -> dict:
        out: CodeOutput = coder.invoke(_generate_prompt(state))
        return {"code": out.code, "explanation": out.explanation, "attempts": state.get("attempts", 0) + 1}

    def execute(state: AgentState) -> dict:
        r = sandbox.run_python(state["code"], timeout=timeout)
        if r.ok:
            return {"execution_result": r.stdout, "error": "", "status": "success"}
        return {"execution_result": r.stdout, "error": r.stderr, "status": "failed"}

    def should_retry(state: AgentState) -> Literal["success", "retry", "give_up"]:
        if state["status"] == "success":
            return "success"
        if state["attempts"] < state.get("max_attempts", 3):
            return "retry"
        return "give_up"

    return generate, execute, should_retry


def build_bugbot(coder, sandbox: Sandbox, timeout: float = 10):
    generate, execute, should_retry = _make_nodes(coder, sandbox, timeout)
    graph = StateGraph(AgentState)
    graph.add_node("generate", generate)
    graph.add_node("execute", execute)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "execute")
    graph.add_conditional_edges("execute", should_retry, {"success": END, "retry": "generate", "give_up": END})
    return graph.compile()


def build_full_agent(coder, reviewer, sandbox: Sandbox, timeout: float = 10):
    generate, execute, should_retry = _make_nodes(coder, sandbox, timeout)

    def review(state: FullAgentState) -> dict:
        r: ReviewResult = reviewer.invoke(
            "Review this Python code for correctness, readability, type hints, docstrings, and PEP 8.\n"
            f"Task: {state['task']}\n\nCode:\n{state['code']}\n\nOutput when run:\n{state.get('execution_result', '')}"
        )
        return {"approved": r.approved, "review_feedback": r.feedback, "status": "approved" if r.approved else "needs_revision"}

    def after_review(state: FullAgentState) -> Literal["done", "revise", "give_up"]:
        if state["approved"]:
            return "done"
        if state["attempts"] < state.get("max_attempts", 3):
            return "revise"
        return "give_up"

    graph = StateGraph(FullAgentState)
    graph.add_node("generate", generate)
    graph.add_node("execute", execute)
    graph.add_node("review", review)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "execute")
    graph.add_conditional_edges("execute", should_retry, {"success": "review", "retry": "generate", "give_up": END})
    graph.add_conditional_edges("review", after_review, {"done": END, "revise": "generate", "give_up": END})
    return graph.compile()
