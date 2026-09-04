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
    """Run one `orion` subcommand and return its exit code."""
    parser = argparse.ArgumentParser(prog="orion", description="Orion teaching kit commands")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("reset", help="restore workspace/ from sample_project/")
    sub.add_parser("check-models", help="verify the model IDs exist on OpenRouter")
    sub.add_parser("sync-web", help="copy web-tagged lesson cells into the site's chapter files")
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

    if args.command == "sync-web":
        import importlib.util

        spec = importlib.util.spec_from_file_location("sync_web_chapters", root / "scripts" / "sync_web_chapters.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in module.sync(root):
            print(f"synced {name}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
