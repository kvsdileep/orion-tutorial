# Orion IDE

A small Cursor-like IDE that runs the same agent the lessons build: chat with tools, an agent mode with a plan, tests, an AI review, and a human gate, plus panels for the repo's rules and skills.

## Run

Backend, from the repo root:

```bash
uv sync --group ide
uv run orion reset
uv run --group ide --directory orion-ide/backend uvicorn main:app --port 8000 --reload
```

Frontend, in a second terminal:

```bash
cd orion-ide/frontend
npm install
npm run dev
```

Open http://localhost:5173. Enter an OpenRouter key in the chat panel, or put it in the repo's `.env`.

## What is where

| Panel | Backed by |
|---|---|
| Explorer | `workspace/`, the copy of `sample_project/` that `orion reset` makes |
| Agent | `orion_agent.graphs.orchestrator` through `backend/agent/graph.py` |
| Rules | `AGENTS.md` and `.cursor/rules/*.mdc`, through `/api/rules` |
| Skills | `.cursor/skills/*/SKILL.md`, through `/api/skills` |
| Time travel | the graph's checkpoint history, through `/api/agent/history` |
| Chat | `orion_agent.graphs.tool_agent` with every tool, the rules, and the skills catalog |
| Terminal | `orion_agent.sandbox.LocalSandbox` (argv only, no shell) |

The backend has no agent logic of its own. Change the package and the IDE changes with it.

## Tests

```bash
uv run --group ide --directory orion-ide/backend pytest tests
```
