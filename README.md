# Orion

Build an AI coding agent with LangChain and LangGraph, one capability at a time: tools, a self-correcting loop, then a planner, a reviewer, a human gate, and parallel coders, all working on a small Streamlit app.

**Site:** the curriculum companion (URL in `web/README.md` once deployed).

## What is here

| Path | What |
|---|---|
| `src/orion_agent/` | The agent: workspace jail, sandbox, tools, rules, skills, MCP, search, and the LangGraph graphs |
| `lessons/` | Eighteen Python files with `# %%` cells, taught live from Cursor |
| `sample_project/` | The Streamlit chatbot the agent modifies; copied into `workspace/` by `orion reset` |
| `.cursor/rules/`, `.cursor/skills/`, `AGENTS.md`, `DESIGN.md` | The rules and skills the agent (and Cursor) read |
| `orion-ide/` | A FastAPI + React IDE that runs the same agent |
| `web/` | The Next.js curriculum site |
| `tests/` | Offline tests against a stub model |

## Setup

```bash
uv sync
cp .env.example .env   # add OPENROUTER_API_KEY
uv run orion reset
uv run pytest
```

Then open `lessons/README.md`.

## Stack

Python 3.13 with uv. langchain 1.x, langgraph 1.x, langchain-mcp-adapters, pydantic 2. OpenRouter for models. Parallel Search MCP for web research. Next.js 15 and React 19 for the site.
