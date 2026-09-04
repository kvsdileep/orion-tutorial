"""The agent loop from Lesson 1: model decides, tools run, model sees the result."""

from __future__ import annotations

from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode


def build_tool_agent(
    llm: BaseChatModel,
    tools: list[BaseTool],
    system_prompt: str | None = None,
    checkpointer=None,
) -> CompiledStateGraph:
    """Compile the two-node agent loop: the model decides, the tools run, the model sees the result."""
    llm_with_tools = llm.bind_tools(tools)

    def agent(state: MessagesState) -> dict:
        messages = list(state["messages"])
        if system_prompt and not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt), *messages]
        return {"messages": [llm_with_tools.invoke(messages)]}

    def route(state: MessagesState) -> Literal["tools", "__end__"]:
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else END

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile(checkpointer=checkpointer)


def prebuilt_agent(
    llm: BaseChatModel, tools: list[BaseTool], system_prompt: str | None = None, checkpointer=None
) -> CompiledStateGraph:
    """What build_tool_agent does, as LangChain ships it."""
    from langchain.agents import create_agent

    return create_agent(llm, tools, system_prompt=system_prompt, checkpointer=checkpointer)
