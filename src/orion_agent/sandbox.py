"""Run generated code with the common accidents prevented.

LocalSandbox is a jail, not a sandbox: it runs code in a temporary directory,
with a scrubbed environment, in isolated mode, with a timeout that returns
instead of raising. It does not block network access or limit CPU or memory.
Shipped coding agents use Seatbelt (macOS), bubblewrap (Linux), Docker, or a
microVM. Swap in DockerSandbox when you need that.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

_SAFE_ENV_KEYS = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "SYSTEMROOT")


@dataclass(frozen=True)
class ExecResult:
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    def summary(self) -> str:
        parts = [f"Exit code: {self.returncode}"]
        if self.timed_out:
            parts[0] += " (timed out)"
        if self.stdout:
            parts.append(f"STDOUT:\n{self.stdout.rstrip()}")
        if self.stderr:
            parts.append(f"STDERR:\n{self.stderr.rstrip()}")
        if len(parts) == 1:
            parts.append("(no output)")
        return "\n".join(parts)


class Sandbox(Protocol):
    def run_python(self, code: str, *, timeout: float = 10, cwd: Path | None = None) -> ExecResult: ...

    def run(self, argv: list[str], *, cwd: Path | None = None, timeout: float = 30) -> ExecResult: ...


class LocalSandbox:
    def __init__(self, python: str | None = None) -> None:
        self.python = python or sys.executable

    @staticmethod
    def _env() -> dict[str, str]:
        return {k: os.environ[k] for k in _SAFE_ENV_KEYS if k in os.environ}

    def run(self, argv: list[str], *, cwd: Path | None = None, timeout: float = 30) -> ExecResult:
        workdir = Path(cwd) if cwd is not None else Path(tempfile.mkdtemp(prefix="orion-sbx-"))
        try:
            proc = subprocess.run(
                list(argv),
                cwd=workdir,
                env=self._env(),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            return ExecResult(stdout=stdout, stderr=f"Timed out after {timeout}s", returncode=-1, timed_out=True)
        except FileNotFoundError as exc:
            return ExecResult(stdout="", stderr=str(exc), returncode=127)
        return ExecResult(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)

    def run_python(self, code: str, *, timeout: float = 10, cwd: Path | None = None) -> ExecResult:
        if cwd is not None:
            code = f"import sys; sys.path.insert(0, {str(Path(cwd).resolve())!r})\n" + code
        return self.run([self.python, "-I", "-c", code], cwd=cwd, timeout=timeout)


class DockerSandbox:
    """Placeholder for a real sandbox. Not implemented in this course.

    A working version runs `docker run --rm --network none -v <tmp>:/work python:3.13-slim`
    per call. Hosted options: E2B, Modal Sandboxes, Daytona.
    """

    def __init__(self, image: str = "python:3.13-slim") -> None:
        raise NotImplementedError("DockerSandbox is a stub. Use LocalSandbox, or implement this class.")
