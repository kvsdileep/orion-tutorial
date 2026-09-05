# Lessons

Three lessons, eighteen files, run live from Cursor. Each file is a sequence of `# %%` cells. Put the cursor in a cell and press Shift+Enter to run it in the interactive window; the output appears next to the code. A file also runs top to bottom with `uv run python lessons/<lesson>/<file>.py`.

| Lesson | Files | What it gives the agent |
|---|---|---|
| 1 Hands | ch01 to ch07 | Tools, the agent loop, rules, streaming, memory |
| 2 Self-awareness | ch08 to ch12 | Structured output, sandboxed execution, retries, a reviewer, rules and skills, inline edits |
| 3 Brain | ch13 to ch18 | Codebase search, MCP tools, a planner, a human gate, parallel coders, time travel |

## Setup on the teaching machine

```bash
uv sync
cp .env.example .env        # add OPENROUTER_API_KEY; PARALLEL_API_KEY is optional
uv run orion check-models   # both model IDs must resolve on OpenRouter
uv run orion reset          # copies sample_project/ into workspace/
```

Open the repository folder in Cursor (not a subfolder). The workspace interpreter is `.venv` (Python 3.13). If Shift+Enter fails with `No module named ipykernel_launcher`, the kernel is Homebrew 3.14 — pick **Orion (Python 3.13)** from the kernel picker, or Command Palette → “Python: Select Interpreter” → `.venv/bin/python`.

## Cell tags

`# %% C3` is the third cell of the original lesson; `# %% N1` is a cell added later. The instructor script refers to these tags. A trailing `web` on a tag marks a cell whose code appears on the curriculum site.

## Before the session

1. `uv run orion reset`. The workspace must contain only `app.py`, `chat.py`, `config.py`, and `test_app.py`.
2. Run Lesson 1 and Lesson 2 files end to end once so the outputs are cached in your head and the models are warm.
3. Run ch16 once. It pauses; approve it. Then run ch18. Note how long each takes.
4. `uv run orion reset` again.
5. `uv run pytest` must be green.

## During the session

- ch07's last cell resets the workspace. Do not run it live.
- ch16, ch17, and ch18 share one agent when they run in the same interactive window. If you restart the kernel between them, ch18 replays the first feature on its own (cell N0).
- ch14 and ch16's research step call the Parallel Search MCP server. It works without a key; if the network is down, ch14 N1 is the only cell that fails.
