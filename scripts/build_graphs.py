"""Generate the teaching drawings as Excalidraw files and SVG previews.

One drawing per beat that the instructor script draws live. Run from the repo root:

    uv run python scripts/build_graphs.py

Outputs go to docs/graphs/. Open a .excalidraw file at excalidraw.com (drag it onto the
canvas) to trace it live or reveal it; the .svg is the same layout for a quick look.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "graphs"

NODE_W, NODE_H = 160, 68
PILL_W, PILL_H = 96, 40
FONT = 22
INK = "#1e1e1e"
NODE_FILL = "#e9ecef"
TERMINAL_FILL = "#d0ebff"
DECISION_FILL = "#fff3bf"
HUMAN_FILL = "#ffd8a8"
TABLE_HEAD_FILL = "#e8eef4"

_rng = random.Random(7)


def _seed() -> int:
    return _rng.randint(1, 2**31 - 1)


# ---------------------------------------------------------------- drawing model


class Node:
    def __init__(self, name: str, x: float, y: float, kind: str = "node", label: str | None = None):
        self.name, self.x, self.y, self.kind = name, x, y, kind
        self.label = label or name
        if kind == "terminal":
            self.w, self.h = PILL_W, PILL_H
        else:
            self.w, self.h = NODE_W, NODE_H

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def anchor(self, side: str) -> tuple[float, float]:
        return {
            "top": (self.cx, self.y),
            "bottom": (self.cx, self.y + self.h),
            "left": (self.x, self.cy),
            "right": (self.x + self.w, self.cy),
        }[side]

    def toward(self, px: float, py: float) -> tuple[float, float]:
        """Point on this node's boundary in the direction of (px, py)."""
        dx, dy = px - self.cx, py - self.cy
        if dx == dy == 0:
            return self.cx, self.cy
        if self.kind == "terminal":
            # rounded rectangle: clip to the box
            sx = (self.w / 2) / abs(dx) if dx else math.inf
            sy = (self.h / 2) / abs(dy) if dy else math.inf
            t = min(sx, sy)
        else:
            # ellipse
            a, b = self.w / 2, self.h / 2
            t = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2)
        return self.cx + dx * t, self.cy + dy * t


class Edge:
    def __init__(self, src: str, dst: str, label: str = "", via: list[tuple[float, float]] | None = None,
                 dashed: bool = False, src_side: str | None = None, dst_side: str | None = None,
                 label_at: tuple[float, float] | None = None, src_dx: float = 0, dst_dx: float = 0):
        self.src, self.dst, self.label, self.via = src, dst, label, via or []
        self.dashed, self.src_side, self.dst_side, self.label_at = dashed, src_side, dst_side, label_at
        self.src_dx, self.dst_dx = src_dx, dst_dx


class Table:
    def __init__(self, x: float, y: float, header: list[str], rows: list[list[str]], col_w: list[int], title: str = ""):
        self.x, self.y, self.header, self.rows, self.col_w, self.title = x, y, header, rows, col_w, title


class Drawing:
    def __init__(self, name: str, title: str, nodes: list[Node], edges: list[Edge], tables: list[Table] | None = None,
                 caption: str = ""):
        self.name, self.title, self.nodes, self.edges = name, title, nodes, edges
        self.tables, self.caption = tables or [], caption
        self.by_name = {n.name: n for n in nodes}

    @property
    def caption_y(self) -> float:
        return max([n.y + n.h for n in self.nodes] + [t.y + 34 * (len(t.rows) + 1) for t in self.tables] + [300]) + 50

    def edge_points(self, e: Edge) -> list[tuple[float, float]]:
        a, b = self.by_name[e.src], self.by_name[e.dst]

        def shifted(node: Node, side: str, dx: float) -> tuple[float, float]:
            x, y = node.anchor(side)
            return x + dx, y

        if e.via:
            start = shifted(a, e.src_side, e.src_dx) if e.src_side else a.toward(*e.via[0])
            end = shifted(b, e.dst_side, e.dst_dx) if e.dst_side else b.toward(*e.via[-1])
            return [start, *e.via, end]
        start = shifted(a, e.src_side, e.src_dx) if e.src_side else a.toward(b.cx, b.cy)
        end = shifted(b, e.dst_side, e.dst_dx) if e.dst_side else b.toward(a.cx, a.cy)
        return [start, end]


# ---------------------------------------------------------------- excalidraw


def _base(kind: str, x: float, y: float, w: float, h: float, **extra) -> dict:
    el = {
        "id": f"{kind}-{_seed():x}",
        "type": kind,
        "x": round(x, 1), "y": round(y, 1), "width": round(w, 1), "height": round(h, 1),
        "angle": 0,
        "strokeColor": INK, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": None,
        "seed": _seed(), "version": 1, "versionNonce": _seed(), "isDeleted": False,
        "boundElements": [], "updated": 1, "link": None, "locked": False,
    }
    el.update(extra)
    return el


def _text(x: float, y: float, w: float, h: float, text: str, size: int = FONT, align: str = "center",
          valign: str = "middle", color: str = INK) -> dict:
    lines = text.count("\n") + 1
    return _base(
        "text", x, y, w, h,
        strokeColor=color, text=text, originalText=text, fontSize=size, fontFamily=1,
        textAlign=align, verticalAlign=valign, lineHeight=1.25, baseline=size * lines, autoResize=True,
        containerId=None,
    )


def _node_elements(n: Node) -> list[dict]:
    if n.kind == "terminal":
        shape = _base("rectangle", n.x, n.y, n.w, n.h, backgroundColor=TERMINAL_FILL, roundness={"type": 3})
    else:
        fill = {"decision": DECISION_FILL, "human": HUMAN_FILL}.get(n.kind, NODE_FILL)
        shape = _base("ellipse", n.x, n.y, n.w, n.h, backgroundColor=fill)
    label = _text(n.x, n.y, n.w, n.h, n.label, size=FONT if n.kind != "terminal" else 16)
    return [shape, label]


def _arrow_elements(pts: list[tuple[float, float]], label: str, dashed: bool, label_at=None) -> list[dict]:
    x0, y0 = pts[0]
    rel = [[round(px - x0, 1), round(py - y0, 1)] for px, py in pts]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    arrow = _base(
        "arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys),
        points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
        startArrowhead=None, endArrowhead="arrow", elbowed=False,
        strokeStyle="dashed" if dashed else "solid",
    )
    out = [arrow]
    if label:
        if label_at is None:
            mid = len(pts) // 2
            (ax, ay), (bx, by) = pts[mid - 1], pts[mid]
            lx, ly = (ax + bx) / 2, (ay + by) / 2 - 14
        else:
            lx, ly = label_at
        w = max(60, 8.5 * max(len(s) for s in label.split("\n")))
        out.append(_text(lx - w / 2, ly - 10, w, 20 * (label.count("\n") + 1), label, size=15, color="#495057"))
    return out


def _table_elements(t: Table) -> list[dict]:
    els = []
    row_h = 34
    if t.title:
        els.append(_text(t.x, t.y - 34, sum(t.col_w), 26, t.title, size=18, align="left"))
    y = t.y
    for r, row in enumerate([t.header, *t.rows]):
        x = t.x
        for c, cell in enumerate(row):
            w = t.col_w[c]
            fill = TABLE_HEAD_FILL if r == 0 else "transparent"
            els.append(_base("rectangle", x, y, w, row_h, backgroundColor=fill, strokeWidth=1, roughness=0))
            els.append(_text(x, y, w, row_h, cell, size=14 if r else 15))
            x += w
        y += row_h
    return els


def to_excalidraw(d: Drawing) -> dict:
    els = []
    els.append(_text(40, 20, 1200, 40, d.title, size=30, align="left"))
    for n in d.nodes:
        els += _node_elements(n)
    for e in d.edges:
        els += _arrow_elements(d.edge_points(e), e.label, e.dashed, e.label_at)
    for t in d.tables:
        els += _table_elements(t)
    if d.caption:
        els.append(_text(40, d.caption_y, 1200, 26 * (d.caption.count("\n") + 1), d.caption, size=18, align="left", color="#343a40"))
    return {
        "type": "excalidraw", "version": 2, "source": "orion-tutorial/scripts/build_graphs.py",
        "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
    }


# ---------------------------------------------------------------- svg


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_svg(d: Drawing) -> str:
    parts = []
    W = max([n.x + n.w for n in d.nodes] + [t.x + sum(t.col_w) for t in d.tables] + [900]) + 60
    H = d.caption_y + 30 * (d.caption.count("\n") + 1) + 40
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Helvetica, Arial, sans-serif">')
    parts.append('<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#1e1e1e"/></marker></defs>')
    parts.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>')
    parts.append(f'<text x="40" y="50" font-size="30" font-weight="600" fill="{INK}">{_esc(d.title)}</text>')
    for e in d.edges:
        pts = d.edge_points(e)
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        dash = ' stroke-dasharray="8,6"' if e.dashed else ""
        parts.append(f'<polyline points="{path}" fill="none" stroke="{INK}" stroke-width="2" marker-end="url(#ah)"{dash}/>')
        if e.label:
            if e.label_at is None:
                mid = len(pts) // 2
                (ax, ay), (bx, by) = pts[mid - 1], pts[mid]
                lx, ly = (ax + bx) / 2, (ay + by) / 2 - 8
            else:
                lx, ly = e.label_at
            for i, line in enumerate(e.label.split("\n")):
                parts.append(f'<text x="{lx:.1f}" y="{ly + i * 19:.1f}" font-size="16" fill="#495057" text-anchor="middle" stroke="#ffffff" stroke-width="5" paint-order="stroke">{_esc(line)}</text>')
    for n in d.nodes:
        if n.kind == "terminal":
            parts.append(f'<rect x="{n.x}" y="{n.y}" width="{n.w}" height="{n.h}" rx="12" fill="{TERMINAL_FILL}" stroke="{INK}" stroke-width="2"/>')
            size = 17
        else:
            fill = {"decision": DECISION_FILL, "human": HUMAN_FILL}.get(n.kind, NODE_FILL)
            parts.append(f'<ellipse cx="{n.cx}" cy="{n.cy}" rx="{n.w / 2}" ry="{n.h / 2}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
            size = 21
        lines = n.label.split("\n")
        y0 = n.cy - (len(lines) - 1) * size * 0.6
        for i, line in enumerate(lines):
            parts.append(f'<text x="{n.cx}" y="{y0 + i * size * 1.2 + size * 0.35:.1f}" font-size="{size}" fill="{INK}" text-anchor="middle">{_esc(line)}</text>')
    for t in d.tables:
        if t.title:
            parts.append(f'<text x="{t.x}" y="{t.y - 12}" font-size="17" fill="{INK}">{_esc(t.title)}</text>')
        y = t.y
        for r, row in enumerate([t.header, *t.rows]):
            x = t.x
            for c, cell in enumerate(row):
                w = t.col_w[c]
                fill = TABLE_HEAD_FILL if r == 0 else "#ffffff"
                parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{fill}" stroke="#adb5bd" stroke-width="1"/>')
                parts.append(f'<text x="{x + w / 2}" y="{y + 22}" font-size="{14 if r else 15}" font-weight="{"bold" if r == 0 else "normal"}" fill="{INK}" text-anchor="middle">{_esc(cell)}</text>')
                x += w
            y += 34
    for i, line in enumerate(d.caption.split("\n")):
        if line:
            parts.append(f'<text x="40" y="{d.caption_y + 20 + i * 30:.0f}" font-size="19" fill="#343a40">{_esc(line)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------- the six drawings


def drawings() -> list[Drawing]:
    out = []

    # Beat 14: the first graph
    out.append(Drawing(
        "agent_loop", "The agent loop",
        nodes=[
            Node("START", 327, 80, "terminal"), Node("agent", 300, 190), Node("tools", 300, 380),
            Node("END", 600, 202, "terminal"),
        ],
        edges=[
            Edge("START", "agent"),
            Edge("agent", "tools", "tool_calls non-empty", src_side="bottom", dst_side="top", src_dx=-22, dst_dx=-22, label_at=(265, 320)),
            Edge("tools", "agent", "tool result", src_side="top", dst_side="bottom", src_dx=22, dst_dx=22, label_at=(470, 320)),
            Edge("agent", "END", "tool_calls empty", label_at=(530, 190)),
        ],
        caption="The model decides which tool to call. The tool runs. The model sees the result and decides again,\n"
                "until an answer comes back with no tool calls.",
    ))

    # Beat 27: self-correcting graph with its state table
    out.append(Drawing(
        "self_correction", "Self-correction: generate, execute, retry",
        nodes=[
            Node("START", 357, 80, "terminal"), Node("generate", 330, 190), Node("execute", 330, 370),
            Node("give up", 330, 560, "decision"), Node("END", 640, 382, "terminal"),
        ],
        edges=[
            Edge("START", "generate"),
            Edge("generate", "execute", src_side="bottom", dst_side="top"),
            Edge("execute", "END", "success", label_at=(560, 380)),
            Edge("execute", "generate", "failed, attempts < max:\nretry with the error", dashed=True,
                 src_side="left", dst_side="left", via=[(230, 402), (230, 222)], label_at=(120, 300)),
            Edge("execute", "give up", "failed at max attempts", src_side="bottom", dst_side="top", label_at=(500, 500)),
            Edge("give up", "END", src_side="right", dst_side="bottom", via=[(688, 592)]),
        ],
        tables=[Table(800, 120, ["step", "task", "code", "expl", "error", "attempt"],
                      [["START", "task", "-", "-", "-", "0"],
                       ["generate", "task", "func_v1", "yes", "-", "1"],
                       ["execute", "task", "func_v1", "yes", "traceback_v1", "1"],
                       ["generate", "task", "func_v2", "yes", "-", "2"],
                       ["execute", "task", "func_v2", "yes", "traceback_v2", "2"],
                       ["generate", "task", "func_v3", "yes", "-", "3"],
                       ["execute", "task", "func_v3", "yes", "- (success)", "3"]],
                      [90, 70, 100, 60, 130, 80], title="The state after each step")],
        caption="generate writes the code. execute runs it in the sandbox. A failure goes back to generate with the error\n"
                "in the prompt. After three failures the graph gives up and reports the last state.",
    ))

    # Beat 30: generate, execute, review with its state table
    out.append(Drawing(
        "self_correction_with_review", "Self-correction with a reviewer",
        nodes=[
            Node("START", 357, 80, "terminal"), Node("generate", 330, 190), Node("execute", 330, 370),
            Node("review", 330, 550), Node("END", 660, 562, "terminal"),
        ],
        edges=[
            Edge("START", "generate"),
            Edge("generate", "execute", src_side="bottom", dst_side="top"),
            Edge("execute", "review", "passed", src_side="bottom", dst_side="top", label_at=(450, 500)),
            Edge("execute", "generate", "failed, attempts < max:\nretry with the error", dashed=True,
                 src_side="left", dst_side="left", via=[(230, 402), (230, 222)], label_at=(120, 300)),
            Edge("execute", "END", "failed at max: give up", via=[(708, 402)], src_side="right", dst_side="top", label_at=(830, 402)),
            Edge("review", "END", "approved", label_at=(600, 615)),
            Edge("review", "generate", "rejected: the feedback\ngoes into the prompt", dashed=True,
                 src_side="right", dst_side="right", via=[(560, 582), (560, 222)], label_at=(660, 290)),
        ],
        tables=[Table(940, 120, ["step", "task", "code", "error", "review", "attempt"],
                      [["generate", "task", "v1", "-", "-", "1"],
                       ["execute", "task", "v1", "traceback_v1", "-", "1"],
                       ["generate", "task", "v2", "-", "-", "2"],
                       ["execute", "task", "v2", "- (ran)", "-", "2"],
                       ["review", "task", "v2", "-", "rejected: feedback_1", "2"],
                       ["generate", "task", "v3", "-", "-", "3"],
                       ["execute", "task", "v3", "- (ran)", "-", "3"],
                       ["review", "task", "v3", "-", "approved", "3"]],
                      [90, 70, 60, 120, 170, 80], title="The state after each step")],
        caption="Execution proves the code runs. The reviewer judges whether it is good. Either kind of feedback, an error\n"
                "or a rejection, goes back into the next prompt. Review runs only on code that already works.",
    ))

    # Beat 44: the orchestrator
    y = 300
    out.append(Drawing(
        "orchestrator", "The orchestrator: plan, code, test, review, approve, apply, verify",
        nodes=[
            Node("START", 40, y + 12, "terminal"),
            Node("plan", 180, y), Node("code", 380, y), Node("test", 580, y), Node("ai_review", 780, y, label="AI review"),
            Node("human_review", 980, y, "human", label="human review"), Node("apply", 1180, y), Node("verify", 1380, y),
            Node("END", 1580, y + 12, "terminal"),
            Node("END2", 180, 560, "terminal", label="END"),
        ],
        edges=[
            Edge("START", "plan"), Edge("plan", "code"), Edge("code", "test"),
            Edge("test", "ai_review", "tests pass", label_at=(742, 296)),
            Edge("ai_review", "human_review", "approved", label_at=(890, 296)),
            Edge("human_review", "apply", "approve", label_at=(1140, 296)),
            Edge("apply", "verify"), Edge("verify", "END"),
            Edge("test", "code", "fail, attempts left:\nback with the traceback", dashed=True,
                 src_side="bottom", dst_side="bottom", via=[(655, 440), (455, 440)], label_at=(555, 470)),
            Edge("ai_review", "code", "revise: feedback goes\ninto the coder prompt (max 2)", dashed=True,
                 src_side="bottom", dst_side="bottom", via=[(855, 520), (455, 520)], label_at=(760, 550)),
            Edge("human_review", "code", "reject + reason: counters reset", dashed=True,
                 src_side="top", dst_side="top", via=[(1055, 160), (455, 160)], label_at=(760, 140)),
            Edge("test", "human_review", "fail at the cap: the human sees it", dashed=True,
                 src_side="top", dst_side="top", via=[(655, 220), (1055, 220)], label_at=(855, 200)),
            Edge("plan", "END2", "a planned path escapes\nthe workspace", dashed=True, src_side="bottom", dst_side="top", label_at=(120, 470)),
        ],
        caption="Tests run on a copy of the workspace before anyone reviews. Only passing code reaches the AI reviewer, and only\n"
                "reviewed code reaches the human. A reject carries the human's reason back to the coder. Apply writes the real files;\n"
                "verify runs the tests once more on them.",
    ))

    # Beat 47: orchestrator state table
    out.append(Drawing(
        "orchestrator_state", "The state through one run",
        nodes=[], edges=[],
        tables=[Table(40, 100, ["step", "feature_request", "plan", "code", "test", "AI review", "human", "tests / reviews"],
                      [["START", "add a system prompt", "-", "-", "-", "-", "-", "0 / 0"],
                       ["plan", "same", "modify config, chat, app", "-", "-", "-", "-", "0 / 0"],
                       ["code", "same", "same", "v1 x3 (not on disk)", "-", "-", "-", "0 / 0"],
                       ["test", "same", "same", "v1 x3", "3 passed (on a copy)", "-", "-", "1 / 0"],
                       ["AI review", "same", "same", "v1 x3", "3 passed", "rejected: reason_1", "-", "1 / 1"],
                       ["code", "same", "same", "v2 x3 (reason_1 in the prompt)", "-", "-", "-", "1 / 1"],
                       ["test", "same", "same", "v2 x3", "3 passed", "-", "-", "2 / 1"],
                       ["AI review", "same", "same", "v2 x3", "3 passed", "approved", "-", "2 / 2"],
                       ["human review", "same", "same", "v2 x3", "3 passed", "approved", "paused, then approve", "2 / 2"],
                       ["apply", "same", "same", "v2 x3 written to disk", "-", "-", "-", "2 / 2"],
                       ["verify", "same", "same", "on disk", "3 passed (real files)", "-", "-", "2 / 2"],
                       ["END", "same", "same", "done", "done", "-", "-", "2 / 2"]],
                      [110, 150, 190, 230, 170, 150, 170, 120])],
        caption="What each field holds after each node. The second code row is the one to notice: v2 was written with the\n"
                "reviewer's reason in the prompt. A human reject would send both counters back to 0 / 0.",
    ))

    # Beat 48: parallel fan-out
    out.append(Drawing(
        "parallel_coders", "Parallel coders with Send",
        nodes=[
            Node("START", 40, 262, "terminal"), Node("plan", 180, 250),
            Node("c1", 450, 90, label="code_file\nconfig.py"), Node("c2", 450, 250, label="code_file\nchat.py"), Node("c3", 450, 410, label="code_file\napp.py"),
            Node("collect", 800, 250), Node("END", 1020, 262, "terminal"),
        ],
        edges=[
            Edge("START", "plan"),
            Edge("plan", "c1", "Send", label_at=(390, 150)), Edge("plan", "c2", "Send", label_at=(390, 268)), Edge("plan", "c3", "Send", label_at=(390, 390)),
            Edge("c1", "collect", label_at=None), Edge("c2", "collect", "reducer:\nadd_to_list", label_at=(700, 250)), Edge("c3", "collect"),
            Edge("collect", "END"),
        ],
        caption="One plan, then one copy of the coder per file, all running at once. Send creates the copies with different inputs;\n"
                "the reducer on generated_code merges their results into one list.",
    ))
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for d in drawings():
        (OUT / f"{d.name}.excalidraw").write_text(json.dumps(to_excalidraw(d), indent=1))
        (OUT / f"{d.name}.svg").write_text(to_svg(d))
        print("wrote", d.name)


if __name__ == "__main__":
    main()
