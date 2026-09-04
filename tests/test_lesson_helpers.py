import asyncio
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from orion_agent import lesson


def test_repo_root_walks_up_to_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    (tmp_path / "src" / "orion_agent").mkdir(parents=True)
    deep = tmp_path / "lessons" / "01_hands"
    deep.mkdir(parents=True)
    assert lesson.repo_root(deep) == tmp_path.resolve()


def test_repo_root_raises_outside_repo(tmp_path):
    try:
        lesson.repo_root(tmp_path)
    except RuntimeError as exc:
        assert "orion-tutorial" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")


async def _double(x):
    return x * 2


def test_run_without_a_loop():
    assert lesson.run(_double(2)) == 4


def test_run_inside_a_running_loop():
    async def outer():
        return lesson.run(_double(3))

    assert asyncio.run(outer()) == 6


def test_print_messages_formats_each_kind(capsys):
    lesson.print_messages([
        HumanMessage(content="hi"),
        AIMessage(content="", tool_calls=[{"name": "read_file", "args": {"filepath": "a.py"}, "id": "1", "type": "tool_call"}]),
        ToolMessage(content="x = 1", tool_call_id="1", name="read_file"),
        AIMessage(content="done"),
    ])
    out = capsys.readouterr().out
    assert "[human] hi" in out
    assert "[agent] calls read_file({'filepath': 'a.py'})" in out
    assert "[tool:read_file] x = 1" in out
    assert "[agent] done" in out


def test_demo_orchestrator_is_cached(ws_dir, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    root = ws_dir.parent
    a = lesson.demo_orchestrator(root, lesson.Workspace(ws_dir))
    b = lesson.demo_orchestrator(root, lesson.Workspace(ws_dir))
    assert a is b
    names = set(a.get_graph().nodes) - {"__start__", "__end__"}
    assert names == {"plan", "code", "test", "ai_review", "human_review", "apply", "verify"}
