import pytest

from orion_agent.sandbox import DockerSandbox, ExecResult, LocalSandbox


def test_hello_world():
    r = LocalSandbox().run_python("print('hello world')")
    assert r.ok
    assert r.stdout.strip() == "hello world"
    assert r.stderr == ""


def test_error_is_reported_not_raised():
    r = LocalSandbox().run_python("print(1/0)")
    assert not r.ok
    assert r.returncode == 1
    assert "ZeroDivisionError" in r.stderr


def test_timeout_returns_failed_result():
    r = LocalSandbox().run_python("import time; time.sleep(5)", timeout=1)
    assert r.timed_out
    assert not r.ok
    assert r.returncode == -1
    assert "Timed out" in r.stderr


def test_environment_is_scrubbed(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "secret")
    r = LocalSandbox().run_python("import os; print(os.environ.get('OPENROUTER_API_KEY'))")
    assert r.stdout.strip() == "None"


def test_cwd_is_importable(tmp_path):
    (tmp_path / "config.py").write_text('PAGE_TITLE = "T"\n')
    r = LocalSandbox().run_python("import config; print(config.PAGE_TITLE)", cwd=tmp_path)
    assert r.stdout.strip() == "T"


def test_run_argv_without_shell(tmp_path):
    r = LocalSandbox().run(["echo", "a && b"], cwd=tmp_path)
    assert r.stdout.strip() == "a && b"


def test_summary_formats_output():
    r = ExecResult(stdout="out\n", stderr="err\n", returncode=2)
    s = r.summary()
    assert "Exit code: 2" in s and "STDOUT:\nout" in s and "STDERR:\nerr" in s
    assert ExecResult("", "", 0).summary() == "Exit code: 0\n(no output)"


def test_docker_sandbox_is_a_stub():
    with pytest.raises(NotImplementedError):
        DockerSandbox()
