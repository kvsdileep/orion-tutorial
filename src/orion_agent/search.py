"""Agentic codebase search: grep, rank, read. No index, no embeddings."""

from __future__ import annotations

import ast
import re

from orion_agent.workspace import Match, Workspace


def search_codebase(ws: Workspace, query: str, max_files: int = 5, max_lines: int = 12) -> str:
    words = [w for w in re.findall(r"\w+", query) if len(w) > 2]
    hits: dict[str, list[Match]] = {}
    for word in words:
        for m in ws.grep(re.escape(word)):
            hits.setdefault(m.path, []).append(m)
    if not hits:
        return "No matches."
    ranked = sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:max_files]
    blocks = []
    for path, matches in ranked:
        seen: set[int] = set()
        lines = []
        for m in sorted(matches, key=lambda m: m.line):
            if m.line in seen:
                continue
            seen.add(m.line)
            lines.append(f"{m.line}: {m.text}")
        blocks.append(f"--- {path} ({len(matches)} hits) ---\n" + "\n".join(lines[:max_lines]))
    return "\n\n".join(blocks)


def repo_map(ws: Workspace) -> str:
    """One line per file with its top-level functions, classes, and constants."""
    lines = []
    for path in ws.glob("**/*.py"):
        try:
            tree = ast.parse(ws.read(path))
        except SyntaxError:
            lines.append(f"{path}: (syntax error)")
            continue
        names = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.append(f"def {node.name}")
            elif isinstance(node, ast.ClassDef):
                names.append(f"class {node.name}")
            elif isinstance(node, ast.Assign):
                names += [t.id for t in node.targets if isinstance(t, ast.Name)]
        lines.append(f"{path}: {', '.join(names) if names else '(no top-level definitions)'}")
    return "\n".join(lines)
