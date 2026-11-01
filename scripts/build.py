#!/usr/bin/env python3
"""Build every derived artifact from the resource files themselves.

Single source of truth = the frontmatter of each `0-Resources/<sub>/<name>.md`:

    ---
    title: 显示名称
    summary: 一句话说明（同时用于网页卡片和子目录表格）
    source: 原始链接
    date: YYYY-MM-DD
    tags: [tag1, tag2]
    ---

Generated from it:
  * 0-Resources/0-Index.md                     (whole file)
  * 0-Resources/<sub>/README.md                (table between BUILD:TABLE markers)
  * README.md                                  (nav block between BUILD:NAV markers)
  * index.html                                 (whole file)
  * assets/roadmap-light.svg / -dark.svg       (the ✨ 从这里开始 diagram)

Usage:
    python scripts/build.py            # rewrite everything
    python scripts/build.py --check    # report staleness, exit 1 if anything differs

Adding a resource therefore means: write ONE .md file, run this, commit.
"""
import argparse
import pathlib
import re
import sys
from xml.sax.saxutils import escape

import generate_index

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "0-Resources"

SUBDIRS = ["1-Official-Docs", "2-Papers", "3-Tutorials", "4-Tools-Frameworks", "5-Datasets"]
LABELS = {
    "1-Official-Docs": "Official Docs",
    "2-Papers": "Papers",
    "3-Tutorials": "Tutorials",
    "4-Tools-Frameworks": "Tools & Frameworks",
    "5-Datasets": "Datasets",
}
EMPTY_HINT = {
    "1-Official-Docs": "add your first official doc",
    "2-Papers": "add your first paper",
    "3-Tutorials": "add your first tutorial",
    "4-Tools-Frameworks": "add your first tool",
    "5-Datasets": "add your first dataset",
}

NAV_START, NAV_END = "<!-- BUILD:NAV:START -->", "<!-- BUILD:NAV:END -->"
TAB_START, TAB_END = "<!-- BUILD:TABLE:START -->", "<!-- BUILD:TABLE:END -->"

# The learning-path diagram. Only the *structure* is editorial (which goal, which
# two resources); titles come from frontmatter, so renaming a resource updates
# the diagram automatically.
ROADMAP = [
    {"goal": "系统入门 LLM",
     "first": "0-Resources/3-Tutorials/cs336-language-modeling-from-scratch.md",
     "next": "0-Resources/3-Tutorials/datawhale-diy-llm.md"},
    {"goal": "搞懂推理系统",
     "first": "0-Resources/3-Tutorials/llm-inference-system-intro.md",
     "next": "0-Resources/4-Tools-Frameworks/nano-vllm.md"},
    {"goal": "建立 AI Infra 全局观",
     "first": "0-Resources/3-Tutorials/bojieli-ai-infra-book.md",
     "next": "0-Resources/3-Tutorials/ultrascale-playbook.md"},
    {"goal": "上手 GPU Kernel",
     "first": "0-Resources/1-Official-Docs/cuda-programming-guide.md",
     "next": "0-Resources/3-Tutorials/mlc-modern-gpu-programming.md"},
    {"goal": "做 AI Agent",
     "first": "0-Resources/3-Tutorials/bojieli-ai-agent-book.md",
     "next": "0-Resources/3-Tutorials/agent-learning-hub.md"},
]


# ---------------------------------------------------------------- frontmatter
def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        fm[k.strip()] = v
    return fm


def parse_tags(raw: str) -> list[str]:
    s = raw.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [p.strip().strip("`").lstrip("#").strip() for p in s.split(",") if p.strip()]


def load_resources() -> dict[str, list[dict]]:
    """{subfolder: [resource, ...]} sorted by (date, title)."""
    groups: dict[str, list[dict]] = {}
    for sub in SUBDIRS:
        items = []
        d = RES / sub
        if not d.is_dir():
            groups[sub] = items
            continue
        for p in sorted(d.glob("*.md")):
            if p.name == "README.md":
                continue
            fm = parse_frontmatter(p.read_text(encoding="utf-8"))
            items.append({
                "file": p.name,
                "rel": f"0-Resources/{sub}/{p.name}",
                "title": fm.get("title") or p.stem,
                "summary": fm.get("summary", ""),
                "source": fm.get("source", ""),
                "date": fm.get("date", ""),
                "tags": parse_tags(fm.get("tags", "")),
            })
        items.sort(key=lambda r: (r["date"], r["title"]))
        groups[sub] = items
    return groups


# ---------------------------------------------------------------- renderers
def render_index_md(groups: dict[str, list[dict]]) -> str:
    out = [
        "# Resources Index",
        "",
        "Quick-lookup index for all collected resources.",
        "",
    ]
    for sub in SUBDIRS:
        items = groups[sub]
        out.append(f"## {LABELS[sub]}")
        out.append("")
        if not items:
            out.append(f"_Empty — {EMPTY_HINT[sub]}!_")
            out.append("")
            continue
        out.append("| Resource | Tags | Date |")
        out.append("|----------|------|------|")
        for r in items:
            tags = " ".join("#" + t for t in r["tags"])
            out.append(f"| [{r['title']}]({sub}/{r['file']}) | `{tags}` | {r['date']} |")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def render_table(items: list[dict], sub: str) -> str:
    if not items:
        return f"_Empty — {EMPTY_HINT[sub]}!_"
    out = ["| Resource | Description | Date |", "| :--- | :--- | :--- |"]
    for r in items:
        out.append(f"| [{r['title']}]({r['file']}) | {r['summary']} | {r['date']} |")
    return "\n".join(out)


def render_nav(groups: dict[str, list[dict]]) -> str:
    out = ["<details open>", "<summary><b>📚 Resources</b></summary>", ""]
    for sub in SUBDIRS:
        out.append("<details>")
        out.append(f"<summary>{sub[0]}-{LABELS[sub]}</summary>")
        out.append("")
        for r in groups[sub]:
            desc = f" — {r['summary']}" if r["summary"] else ""
            out.append(f"- [{r['title']}]({r['rel']}){desc}")
        out.append(f"- [📄 {LABELS[sub]} Index](0-Resources/{sub}/README.md)")
        out.append("")
        out.append("</details>")
        out.append("")
    out.append("- [📋 Full Resource Index](0-Resources/0-Index.md)")
    out.append("")
    out.append("</details>")
    return "\n".join(out)


# ---------------------------------------------------------------- roadmap svg
THEMES = {
    "light": dict(
        bg="#fcfcfb", card="#ffffff", border="#e6e6e4", text="#1c1c1c",
        muted="#8f8f8f", sub="#6b6b6b", arrow="#c9c9c9", rule="#efefec",
        track=["#2f6df6", "#0a7d3b", "#8250df", "#d9730d", "#cf222e"],
    ),
    "dark": dict(
        bg="#101011", card="#1b1b1d", border="#2c2c30", text="#e9e9e7",
        muted="#8c8c8c", sub="#a6a6a6", arrow="#3f3f45", rule="#232327",
        track=["#6f9bf2", "#3fb950", "#b18aff", "#e8913a", "#ff7b72"],
    ),
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', sans-serif")

W, PAD = 900, 26
X_GOAL, X1, NW1 = 26, 200, 300
X2, NW2 = 556, 318
ARROW_X1, ARROW_X2 = X1 + NW1 + 8, X2 - 8
ROW_H, Y0 = 62, 120
H = Y0 + ROW_H * len(ROADMAP) + 62


def _tw(s: str, size: float) -> float:
    """Rough text width: CJK ~1em, latin ~0.55em."""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)


def _fit(s: str, size: float, maxw: float) -> str:
    if _tw(s, size) <= maxw:
        return s
    while s and _tw(s + "…", size) > maxw:
        s = s[:-1]
    return s + "…"


def render_roadmap(by_rel: dict[str, dict], theme: str) -> str:
    t = THEMES[theme]
    e = escape
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="从这里开始：五条学习路径，每条给出先读与接着" font-family="{FONT}">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        # header
        f'<text x="{PAD}" y="44" font-size="17" font-weight="650" fill="{t["text"]}">从这里开始</text>',
        f'<text x="{PAD}" y="67" font-size="12.5" fill="{t["sub"]}">'
        f'按目标选一条路径 · 先读左边，读完接右边</text>',
        f'<line x1="{PAD}" y1="84" x2="{W - PAD}" y2="84" stroke="{t["rule"]}"/>',
        # column headers
        f'<text x="{X_GOAL}" y="106" font-size="10.5" letter-spacing="1.4" fill="{t["muted"]}">目标</text>',
        f'<text x="{X1}" y="106" font-size="10.5" letter-spacing="1.4" fill="{t["muted"]}">先读</text>',
        f'<text x="{X2}" y="106" font-size="10.5" letter-spacing="1.4" fill="{t["muted"]}">接着</text>',
    ]

    for i, row in enumerate(ROADMAP):
        y = Y0 + i * ROW_H
        cy = y + 31
        color = t["track"][i % len(t["track"])]
        first = by_rel.get(row["first"])
        nxt = by_rel.get(row["next"])
        if first is None or nxt is None:
            raise SystemExit(f"roadmap references a missing resource: "
                             f"{row['first']!r} / {row['next']!r}")

        # goal label (right aligned against the first column)
        o.append(f'<circle cx="{X1 - 22}" cy="{cy}" r="3.5" fill="{color}"/>')
        o.append(f'<text x="{X1 - 34}" y="{cy + 4.5}" text-anchor="end" font-size="13" '
                 f'font-weight="600" fill="{t["text"]}">'
                 f'{e(_fit(row["goal"], 13, X1 - 34 - X_GOAL))}</text>')

        # first node — tinted with the track colour
        o.append(f'<rect x="{X1}" y="{y + 10}" width="{NW1}" height="42" rx="9" '
                 f'fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.55"/>')
        o.append(f'<text x="{X1 + 15}" y="{cy + 4.5}" font-size="13" fill="{t["text"]}">'
                 f'{e(_fit(first["title"], 13, NW1 - 30))}</text>')

        # arrow
        o.append(f'<line x1="{ARROW_X1}" y1="{cy}" x2="{ARROW_X2 - 7}" y2="{cy}" '
                 f'stroke="{t["arrow"]}" stroke-width="1.4" stroke-linecap="round"/>')
        o.append(f'<path d="M{ARROW_X2 - 8} {cy - 4} L{ARROW_X2} {cy} L{ARROW_X2 - 8} {cy + 4}" '
                 f'fill="none" stroke="{t["arrow"]}" stroke-width="1.4" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')

        # next node — dashed, reads as "then"
        o.append(f'<rect x="{X2}" y="{y + 10}" width="{NW2}" height="42" rx="9" '
                 f'fill="{t["card"]}" stroke="{t["arrow"]}" stroke-dasharray="4 3"/>')
        o.append(f'<text x="{X2 + 15}" y="{cy + 4.5}" font-size="13" fill="{t["text"]}">'
                 f'{e(_fit(nxt["title"], 13, NW2 - 30))}</text>')

    o.append(f'<text x="{PAD}" y="{H - 24}" font-size="11.5" fill="{t["muted"]}">'
             f'完整索引：0-Resources/0-Index.md　·　在线版：'
             f'70asunflower.github.io/ai-learning-journey</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def splice(text: str, start: str, end: str, body: str, path: str) -> str:
    """Replace whatever sits between the two markers with `body`."""
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"{path}: missing markers {start!r} / {end!r}")
    return text[:i + len(start)] + "\n" + body + "\n" + text[j:]


# ---------------------------------------------------------------- driver
def build(check: bool = False) -> int:
    groups = load_resources()
    index_md = render_index_md(groups)

    targets: list[tuple[pathlib.Path, str]] = [(RES / "0-Index.md", index_md)]

    for sub in SUBDIRS:
        p = RES / sub / "README.md"
        if not p.is_file():
            continue
        targets.append((p, splice(p.read_text(encoding="utf-8"), TAB_START, TAB_END,
                                  render_table(groups[sub], sub), str(p))))

    readme_p = ROOT / "README.md"
    readme = readme_p.read_text(encoding="utf-8")
    targets.append((readme_p, splice(readme, NAV_START, NAV_END,
                                     render_nav(groups), "README.md")))

    # index.html consumes the freshly rendered README nav + 0-Index
    targets.append((ROOT / "index.html",
                    generate_index.build(targets[-1][1], index_md)))

    by_rel = {r["rel"]: r for items in groups.values() for r in items}
    for theme in ("light", "dark"):
        targets.append((ROOT / "assets" / f"roadmap-{theme}.svg",
                        render_roadmap(by_rel, theme)))

    stale = []
    for p, new in targets:
        old = p.read_text(encoding="utf-8") if p.is_file() else ""
        if old == new:
            continue
        stale.append(p)
        if not check:
            p.write_text(new, encoding="utf-8", newline="\n")

    n_items = sum(len(v) for v in groups.values())
    n_tags = len({t for v in groups.values() for r in v for t in r["tags"]})
    verb = "stale" if check else "rewrote"
    if stale:
        print(f"{verb} {len(stale)} file(s):")
        for p in stale:
            print("  " + str(p.relative_to(ROOT)).replace("\\", "/"))
    else:
        print("All artifacts up to date.")
    print(f"{n_items} resources, {n_tags} tags, {len(SUBDIRS)} categories")
    return 1 if (check and stale) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, exit 1 if stale")
    sys.exit(build(ap.parse_args().check))
