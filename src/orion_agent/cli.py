"""The `orion` command: pre-session chores."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx

from orion_agent.llm import FAST, STRONG, check_models
from orion_agent.workspace import Workspace

REPO_ROOT = Path(__file__).resolve().parents[2]


def _http_client() -> httpx.Client:
    return httpx.Client(timeout=15)


def reset(root: Path) -> Path:
    """Copy sample_project/ into workspace/, wiping anything the agent left there."""
    ws = Workspace(root / "workspace")
    ws.reset(root / "sample_project")
    return ws.root


def main(argv: list[str] | None = None, root: Path = REPO_ROOT) -> int:
    parser = argparse.ArgumentParser(prog="orion", description="Orion teaching kit commands")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("reset", help="restore workspace/ from sample_project/")
    sub.add_parser("check-models", help="verify the model IDs exist on OpenRouter")
    args = parser.parse_args(argv)

    if args.command == "reset":
        path = reset(root)
        print(f"workspace restored at {path}")
        return 0

    if args.command == "check-models":
        missing = check_models((FAST, STRONG), client=_http_client())
        if missing:
            print("Missing on OpenRouter: " + ", ".join(missing))
            return 1
        print(f"OK: {FAST}, {STRONG}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
