# Teaching drawings

The six drawings the instructor script makes live, one file per beat. Each exists twice: a `.excalidraw` file to open at [excalidraw.com](https://excalidraw.com) (drag it onto the canvas, or use Open from the menu) and an `.svg` for a quick look. Regenerate them with:

```bash
uv run python scripts/build_graphs.py
```

| Beat | File | What it is |
|---|---|---|
| 14 | `beat14_agent_loop` | The first graph: agent, tools, one conditional edge (ch03 C6) |
| 27 | `beat27_self_correcting` | generate, execute, retry, give up, plus the state table to fill row by row (ch09 C13) |
| 30 | `beat30_generate_execute_review` | The reviewer added, plus the second state table (ch10 C19) |
| 44 | `beat44_orchestrator` | plan, code, test, AI review, human review, apply, verify; 7 nodes, 4 routes (ch16 C13) |
| 47 | `beat47_state_table` | The state through one full run of demo-1 |
| 48 | `beat48_parallel` | One coder per file with Send and the reducer (ch17 C20) |

## Two ways to use them live

**Trace.** Open the `.excalidraw` file, set every element's opacity to 20 percent (select all, then the opacity slider), and draw over it in front of the room. The layout is already solved, so you draw at speaking pace.

**Reveal.** Open the file, select all, delete, and redraw freehand while talking; then Undo (Cmd+Z) once to bring the finished drawing back for the trace and the state table. Or keep the finished file in a second tab and switch to it after drawing.

The state tables in beats 27, 30, and 47 are filled in. To fill them live, open the file and delete the cell text before the session; the grid stays.

## Mermaid, for slides or the site

```mermaid
flowchart TB
    START --> agent
    agent -- "tool_calls non-empty" --> tools
    tools -- "tool result" --> agent
    agent -- "tool_calls empty" --> END
```

```mermaid
flowchart TB
    START --> generate --> execute
    execute -- success --> END
    execute -- "failed, attempts < max" --> generate
    execute -- "failed at max" --> giveup[give up] --> END
```

```mermaid
flowchart TB
    START --> generate --> execute
    execute -- passed --> review
    execute -- "failed, retry" --> generate
    execute -- "failed at max" --> END
    review -- approved --> END
    review -- "rejected: feedback" --> generate
```

```mermaid
flowchart LR
    START --> plan --> code --> test
    test -- "tests pass" --> ai_review
    test -- "fail, attempts left" --> code
    test -- "fail at cap" --> human_review
    ai_review -- approved --> human_review
    ai_review -- revise --> code
    human_review -- approve --> apply --> verify --> END
    human_review -- "reject + reason" --> code
    plan -- "path escapes workspace" --> END
```

```mermaid
flowchart LR
    START --> plan
    plan -- Send --> c1["code_file config.py"]
    plan -- Send --> c2["code_file chat.py"]
    plan -- Send --> c3["code_file app.py"]
    c1 --> collect
    c2 -- "reducer: add_to_list" --> collect
    c3 --> collect
    collect --> END
```
