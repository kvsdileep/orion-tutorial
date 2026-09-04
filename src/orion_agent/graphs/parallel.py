"""Lesson 3, part 9: fan out one coder per file with Send, merge with a reducer."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from orion_agent.graphs.orchestrator import PLAN_PROMPT, build_code_prompt
from orion_agent.schemas import CodeResult, Plan
from orion_agent.search import repo_map
from orion_agent.workspace import Workspace


def add_to_list(existing: list, new: list) -> list:
    return existing + new


class ParallelState(TypedDict, total=False):
    feature_request: str
    codebase_context: str
    plan: str
    file_tasks: list[dict]
    generated_code: Annotated[list[dict], add_to_list]
    status: str


class SingleFileState(TypedDict):
    task: dict
    codebase_context: str


def build_parallel_agent(planner, coder, ws: Workspace, *, rules_root: str | Path | None = None, checkpointer=None):
    def plan_node(state: ParallelState) -> dict:
        context = repo_map(ws)
        plan: Plan = planner.invoke(PLAN_PROMPT.format(request=state["feature_request"], context=context))
        return {
            "codebase_context": context,
            "plan": plan.summary,
            "file_tasks": [t.model_dump() for t in plan.file_tasks],
            "status": "planned",
        }

    def fan_out_to_coders(state: ParallelState) -> list[Send]:
        return [Send("code_file", {"task": t, "codebase_context": state["codebase_context"]}) for t in state["file_tasks"]]

    def code_file(state: SingleFileState) -> dict:
        prompt = build_code_prompt({"codebase_context": state["codebase_context"]}, state["task"], rules_root)
        result: CodeResult = coder.invoke(prompt)
        return {"generated_code": [{"filepath": state["task"]["filepath"], "code": result.code, "explanation": result.explanation}]}

    def collect_results(state: ParallelState) -> dict:
        return {"status": "collected"}

    graph = StateGraph(ParallelState)
    graph.add_node("plan", plan_node)
    graph.add_node("code_file", code_file)
    graph.add_node("collect", collect_results)
    graph.add_edge(START, "plan")
    graph.add_conditional_edges("plan", fan_out_to_coders, ["code_file"])
    graph.add_edge("code_file", "collect")
    graph.add_edge("collect", END)
    return graph.compile(checkpointer=checkpointer)
