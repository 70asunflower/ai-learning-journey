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
MAP_START, MAP_END = "<!-- BUILD:MAP:START -->", "<!-- BUILD:MAP:END -->"
TREE_START, TREE_END = "<!-- BUILD:TREE:START -->", "<!-- BUILD:TREE:END -->"

# The learning map. Every resource must appear exactly once — the build fails
# otherwise, so the diagram can never silently drop an entry again.
# Order inside a track is the suggested reading order.
ROADMAP = [
    {"track": "建立全局观", "items": [
        "0-Resources/3-Tutorials/ai-infra-nothing-new.md",
        "0-Resources/3-Tutorials/llm-algorithm-engineering-roadmap.md",
        "0-Resources/3-Tutorials/top-10-hell-level-cs-courses.md",
        "0-Resources/3-Tutorials/bojieli-ai-infra-book.md",
        "0-Resources/3-Tutorials/mengyuan-llm-articles-index.md",
        "0-Resources/3-Tutorials/sebastian-raschka-blog.md",
    ]},
    {"track": "LLM 原理与从零实现", "items": [
        "0-Resources/3-Tutorials/dive-into-deep-learning.md",
        "0-Resources/3-Tutorials/cs336-language-modeling-from-scratch.md",
        "0-Resources/3-Tutorials/llms-from-scratch.md",
        "0-Resources/3-Tutorials/datawhale-diy-llm.md",
        "0-Resources/3-Tutorials/reasoning-from-scratch.md",
        "0-Resources/3-Tutorials/rl-intuitive-explanation-vzstudio.md",
    ]},
    {"track": "训练与分布式", "items": [
        "0-Resources/3-Tutorials/jax-scaling-book.md",
        "0-Resources/3-Tutorials/ultrascale-playbook.md",
        "0-Resources/3-Tutorials/machine-learning-systems-book.md",
        "0-Resources/3-Tutorials/mit-65840-distributed-systems.md",
    ]},
    {"track": "推理系统与部署", "items": [
        "0-Resources/3-Tutorials/llm-inference-system-intro.md",
        "0-Resources/1-Official-Docs/llm-inference-handbook.md",
        "0-Resources/1-Official-Docs/vllm-docs-zh.md",
        "0-Resources/4-Tools-Frameworks/nano-vllm.md",
        "0-Resources/4-Tools-Frameworks/mini-sglang.md",
        "0-Resources/3-Tutorials/infinitensor-winter-camp-2025.md",
        "0-Resources/3-Tutorials/infra-seminars-2026.md",
    ]},
    {"track": "GPU Kernel 与性能", "items": [
        "0-Resources/1-Official-Docs/cuda-programming-guide.md",
        "0-Resources/3-Tutorials/mlc-modern-gpu-programming.md",
        "0-Resources/4-Tools-Frameworks/compiler-explorer.md",
    ]},
    {"track": "微调与工程实践", "items": [
        "0-Resources/3-Tutorials/self-llm.md",
        "0-Resources/3-Tutorials/unsloth-fine-tuning-guide.md",
        "0-Resources/4-Tools-Frameworks/llamafactory.md",
        "0-Resources/4-Tools-Frameworks/ms-swift.md",
        "0-Resources/4-Tools-Frameworks/modelscope-notebook.md",
        "0-Resources/4-Tools-Frameworks/canirun.md",
    ]},
    {"track": "Agent", "items": [
        "0-Resources/3-Tutorials/bojieli-ai-agent-book.md",
        "0-Resources/3-Tutorials/agent-learning-hub.md",
    ]},
    {"track": "工具与可视化", "items": [
        "0-Resources/4-Tools-Frameworks/tiktokenizer.md",
        "0-Resources/4-Tools-Frameworks/llm-viz.md",
        "0-Resources/4-Tools-Frameworks/inferflux.md",
        "0-Resources/4-Tools-Frameworks/open-design.md",
        "0-Resources/4-Tools-Frameworks/gpt-image-2-prompts.md",
    ]},
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
                "short": fm.get("short") or fm.get("title") or p.stem,
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


# ---------------------------------------------------------------- roadmap
def check_roadmap(by_rel: dict[str, dict]) -> None:
    """Every resource must be listed exactly once, and nothing else may be."""
    listed = [rel for t in ROADMAP for rel in t["items"]]
    dupes = sorted({r for r in listed if listed.count(r) > 1})
    missing = sorted(set(by_rel) - set(listed))
    unknown = sorted(set(listed) - set(by_rel))
    problems = []
    if missing:
        problems.append(f"not in ROADMAP: {missing}")
    if unknown:
        problems.append(f"ROADMAP points at missing files: {unknown}")
    if dupes:
        problems.append(f"listed twice: {dupes}")
    if problems:
        raise SystemExit("roadmap is out of sync with 0-Resources/\n  "
                         + "\n  ".join(problems))


THEMES = {
    "light": dict(
        bg="#fcfcfb", card="#ffffff", border="#e6e6e4", text="#1c1c1c",
        muted="#8f8f8f", sub="#6b6b6b", rule="#efefec", pill="#ffffff", tree="#d3d3ce",
        track=["#2f6df6", "#0a7d3b", "#8250df", "#d9730d", "#cf222e",
               "#1a7f64", "#bf3989", "#8b5cf6"],
    ),
    "dark": dict(
        bg="#101011", card="#1b1b1d", border="#2c2c30", text="#e9e9e7",
        muted="#8c8c8c", sub="#a6a6a6", rule="#232327", pill="#1b1b1d", tree="#3c3c43",
        track=["#6f9bf2", "#3fb950", "#b18aff", "#e8913a", "#ff7b72",
               "#4ec9a0", "#f778ba", "#a78bfa"],
    ),
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', sans-serif")

W, PAD = 900, 26
LABEL_W = 148                 # left column holding the track name
X_FLOW = PAD + LABEL_W + 14   # pills start here
FLOW_W = W - PAD - X_FLOW
PILL_H, PILL_GAP, LINE_GAP = 28, 8, 10
BAND_PAD_TOP, BAND_PAD_BOT = 12, 14
SIZE = 11.5


def _tw(s: str, size: float) -> float:
    """Rough text width: CJK ~1em, latin ~0.55em."""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)


def _fit(s: str, size: float, maxw: float) -> tuple[str, bool]:
    if _tw(s, size) <= maxw:
        return s, False
    while s and _tw(s + "…", size) > maxw:
        s = s[:-1]
    return s + "…", True


def _layout_band(titles: list[str]) -> list[list[tuple[str, float, bool]]]:
    """Flow pills left→right, wrapping. Returns lines of (text, width, truncated)."""
    lines: list[list[tuple[str, float, bool]]] = [[]]
    used = 0.0
    for t in titles:
        text, cut = _fit(t, SIZE, 168)
        w = _tw(text, SIZE) + 40          # 8 pad + 16 badge + 6 + 10 pad
        if lines[-1] and used + PILL_GAP + w > FLOW_W:
            lines.append([])
            used = 0.0
        if lines[-1]:
            used += PILL_GAP
        lines[-1].append((text, w, cut))
        used += w
    return lines


def render_roadmap(by_rel: dict[str, dict], theme: str) -> str:
    t = THEMES[theme]
    e = escape
    bands = [(track, _layout_band([by_rel[rel]["short"] for rel in track["items"]]))
             for track in ROADMAP]

    heights = [BAND_PAD_TOP + len(ls) * PILL_H + (len(ls) - 1) * LINE_GAP + BAND_PAD_BOT
               for _, ls in bands]
    H = 96 + sum(heights) + 46

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="学习地图：按学习顺序分轨列出全部资源" font-family="{FONT}">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<text x="{PAD}" y="42" font-size="17" font-weight="650" fill="{t["text"]}">'
        f'学习地图</text>',
        f'<text x="{PAD}" y="64" font-size="12.5" fill="{t["sub"]}">'
        f'按轨道分组，组内从左到右是建议阅读顺序 · 全部 {len(by_rel)} 份资源</text>',
        f'<line x1="{PAD}" y1="80" x2="{W - PAD}" y2="80" stroke="{t["rule"]}"/>',
    ]

    y = 96
    for i, ((track, lines), h) in enumerate(zip(bands, heights)):
        color = t["track"][i % len(t["track"])]
        cy = y + BAND_PAD_TOP + PILL_H / 2
        o.append(f'<circle cx="{PAD + 5}" cy="{cy}" r="3.5" fill="{color}"/>')
        o.append(f'<text x="{PAD + 16}" y="{cy + 4.5}" font-size="12.5" font-weight="600" '
                 f'fill="{t["text"]}">{e(track["track"])}</text>')

        n = 0
        for li, line in enumerate(lines):
            ly = y + BAND_PAD_TOP + li * (PILL_H + LINE_GAP)
            x = X_FLOW
            for text, w, cut in line:
                n += 1
                o.append(f'<rect x="{x:.1f}" y="{ly}" width="{w:.1f}" height="{PILL_H}" '
                         f'rx="14" fill="{t["pill"]}" stroke="{color}" stroke-opacity="0.45"/>')
                o.append(f'<circle cx="{x + 15:.1f}" cy="{ly + PILL_H / 2}" r="7.5" '
                         f'fill="{color}" fill-opacity="0.16"/>')
                o.append(f'<text x="{x + 15:.1f}" y="{ly + PILL_H / 2 + 3.6}" '
                         f'text-anchor="middle" font-size="9.5" font-weight="700" '
                         f'fill="{color}">{n}</text>')
                o.append(f'<text x="{x + 28:.1f}" y="{ly + PILL_H / 2 + 4.2}" '
                         f'font-size="{SIZE}" fill="{t["text"]}">{e(text)}</text>')
                x += w + PILL_GAP
        y += h

    o.append(f'<text x="{PAD}" y="{H - 22}" font-size="11.5" fill="{t["muted"]}">'
             f'完整索引：0-Resources/0-Index.md　·　在线版：'
             f'{generate_index.PAGES_URL.replace("https://", "").rstrip("/")}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def render_roadmap_md(by_rel: dict[str, dict]) -> str:
    """Clickable text version of the map (an <img> cannot carry links)."""
    out = []
    for i, track in enumerate(ROADMAP, 1):
        out.append(f"**{i}. {track['track']}**")
        out.append("")
        for rel in track["items"]:
            r = by_rel[rel]
            out.append(f"- [{r['title']}]({rel}) — {r['summary']}")
        out.append("")
    return "\n".join(out).rstrip()


def splice(text: str, start: str, end: str, body: str, path: str) -> str:
    """Replace whatever sits between the two markers with `body`."""
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"{path}: missing markers {start!r} / {end!r}")
    return text[:i + len(start)] + "\n" + body + "\n" + text[j:]


# ---------------------------------------------------------------- skill tree
# A real tree, drawn bottom-up: root -> foundation slab -> specialisation
# branches. Foundational skills sit at the root, specialisations fan upward.
# Every resource must appear exactly once; an empty skill renders as a gap.
SKILLTREE = {
    "root": "AI 技术栈",
    "foundation": {"name": "基础层", "skills": [
        {"name": "深度学习", "items": [
            "0-Resources/3-Tutorials/dive-into-deep-learning.md",
            "0-Resources/3-Tutorials/rl-intuitive-explanation-vzstudio.md"]},
        {"name": "系统与体系结构", "items": [
            "0-Resources/3-Tutorials/top-10-hell-level-cs-courses.md",
            "0-Resources/3-Tutorials/mit-65840-distributed-systems.md"]},
        {"name": "AI Infra 全景", "items": [
            "0-Resources/3-Tutorials/ai-infra-nothing-new.md",
            "0-Resources/3-Tutorials/bojieli-ai-infra-book.md"]},
        {"name": "路线与索引", "items": [
            "0-Resources/3-Tutorials/llm-algorithm-engineering-roadmap.md",
            "0-Resources/3-Tutorials/mengyuan-llm-articles-index.md",
            "0-Resources/3-Tutorials/sebastian-raschka-blog.md"]},
    ]},
    "branches": [
        {"name": "LLM 原理", "skills": [
            {"name": "从零构建 LLM", "items": [
                "0-Resources/3-Tutorials/llms-from-scratch.md",
                "0-Resources/3-Tutorials/datawhale-diy-llm.md"]},
            {"name": "中文通识", "items": [
                "0-Resources/3-Tutorials/cs336-language-modeling-from-scratch.md"]},
            {"name": "推理模型", "items": [
                "0-Resources/3-Tutorials/reasoning-from-scratch.md"]},
        ]},
        {"name": "训练与分布式", "skills": [
            {"name": "扩展与并行", "items": [
                "0-Resources/3-Tutorials/ultrascale-playbook.md",
                "0-Resources/3-Tutorials/jax-scaling-book.md"]},
            {"name": "ML 系统", "items": [
                "0-Resources/3-Tutorials/machine-learning-systems-book.md"]},
            {"name": "数据工程", "items": []},
        ]},
        {"name": "推理与部署", "skills": [
            {"name": "推理系统原理", "items": [
                "0-Resources/3-Tutorials/llm-inference-system-intro.md",
                "0-Resources/1-Official-Docs/llm-inference-handbook.md"]},
            {"name": "推理引擎", "items": [
                "0-Resources/1-Official-Docs/vllm-docs-zh.md"]},
            {"name": "框架源码", "items": [
                "0-Resources/4-Tools-Frameworks/nano-vllm.md",
                "0-Resources/4-Tools-Frameworks/mini-sglang.md"]},
            {"name": "系统课程", "items": [
                "0-Resources/3-Tutorials/infinitensor-winter-camp-2025.md",
                "0-Resources/3-Tutorials/infra-seminars-2026.md"]},
        ]},
        {"name": "GPU 与 Kernel", "skills": [
            {"name": "CUDA 编程", "items": [
                "0-Resources/1-Official-Docs/cuda-programming-guide.md"]},
            {"name": "Kernel 优化", "items": [
                "0-Resources/3-Tutorials/mlc-modern-gpu-programming.md"]},
            {"name": "编译与汇编", "items": [
                "0-Resources/4-Tools-Frameworks/compiler-explorer.md"]},
        ]},
        {"name": "微调与工程", "skills": [
            {"name": "微调方法", "items": [
                "0-Resources/3-Tutorials/unsloth-fine-tuning-guide.md",
                "0-Resources/3-Tutorials/self-llm.md"]},
            {"name": "微调框架", "items": [
                "0-Resources/4-Tools-Frameworks/llamafactory.md",
                "0-Resources/4-Tools-Frameworks/ms-swift.md"]},
            {"name": "环境与选型", "items": [
                "0-Resources/4-Tools-Frameworks/modelscope-notebook.md",
                "0-Resources/4-Tools-Frameworks/canirun.md"]},
        ]},
        {"name": "Agent", "skills": [
            {"name": "Agent 原理", "items": [
                "0-Resources/3-Tutorials/bojieli-ai-agent-book.md"]},
            {"name": "学习路线", "items": [
                "0-Resources/3-Tutorials/agent-learning-hub.md"]},
        ]},
        {"name": "工具与可视化", "skills": [
            {"name": "模型可视化", "items": [
                "0-Resources/4-Tools-Frameworks/llm-viz.md",
                "0-Resources/4-Tools-Frameworks/inferflux.md"]},
            {"name": "Tokenizer", "items": [
                "0-Resources/4-Tools-Frameworks/tiktokenizer.md"]},
            {"name": "设计与提示词", "items": [
                "0-Resources/4-Tools-Frameworks/open-design.md",
                "0-Resources/4-Tools-Frameworks/gpt-image-2-prompts.md"]},
        ]},
    ],
}

TREE_TOP = 24
BRANCH_GAP = 8
FAN_H = 64
SLAB_GAP = 30
ROOT_H = 34
NAME_SIZE, SKILL_SIZE, RES_SIZE = 10.8, 9.4, 8.6
LH_NAME, LH_SKILL, LH_RES = 15, 12, 10.5


def _skills_of(node: dict) -> list[dict]:
    return node["skills"]


def all_tree_skills() -> list[dict]:
    out = list(SKILLTREE["foundation"]["skills"])
    for b in SKILLTREE["branches"]:
        out.extend(b["skills"])
    return out


def check_skilltree(by_rel: dict[str, dict]) -> None:
    listed = [rel for s in all_tree_skills() for rel in s["items"]]
    dupes = sorted({r for r in listed if listed.count(r) > 1})
    missing = sorted(set(by_rel) - set(listed))
    unknown = sorted(set(listed) - set(by_rel))
    problems = []
    if missing:
        problems.append(f"not in SKILLTREE: {missing}")
    if unknown:
        problems.append(f"SKILLTREE points at missing files: {unknown}")
    if dupes:
        problems.append(f"listed twice: {dupes}")
    if problems:
        raise SystemExit("skill tree is out of sync with 0-Resources/\n  "
                         + "\n  ".join(problems))


def _wrap(s: str, size: float, maxw: float, max_lines: int) -> list[str]:
    if _tw(s, size) <= maxw:
        return [s]
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if _tw(cand, size) <= maxw:
            cur = cand
            continue
        if cur:
            lines.append(cur)
        cur = w
        if len(lines) == max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    lines = lines[:max_lines]
    lines[-1] = _fit(lines[-1], size, maxw)[0]
    return lines


def _skill_lines(skill: dict, by_rel: dict, width: float) -> tuple[list[str], list[str]]:
    """Return (skill name line, resource lines) for a column of the given width."""
    res = []
    if skill["items"]:
        for rel in skill["items"]:
            res.extend(_wrap(by_rel[rel]["short"], RES_SIZE, width, 2))
    return [skill["name"]], res


def render_skilltree(by_rel: dict[str, dict], theme: str) -> str:
    t = THEMES[theme]
    e = escape
    branches = SKILLTREE["branches"]
    n = len(branches)
    bw = (W - 2 * PAD - (n - 1) * BRANCH_GAP) / n

    # --- measure branch columns ---
    cols = []
    for b in branches:
        blocks = []
        for s in b["skills"]:
            name, res = _skill_lines(s, by_rel, bw - 16)
            blocks.append((name, res))
        h = 8 + LH_NAME + sum(LH_SKILL + len(r) * LH_RES + 4 for _, r in blocks) + 12
        cols.append((b, blocks, h))
    box_h = round(max(h for _, _, h in cols))

    # --- foundation slab: skills laid out as columns ---
    fskills = SKILLTREE["foundation"]["skills"]
    fw = (W - 2 * PAD - (len(fskills) - 1) * BRANCH_GAP) / len(fskills)
    fblocks = []
    for s in fskills:
        name, res = _skill_lines(s, by_rel, fw - 16)
        fblocks.append((name, res))
    SLAB_LABEL_H = 24
    slab_h = SLAB_LABEL_H + max(LH_SKILL + len(r) * LH_RES + 4 for _, r in fblocks) + 12

    slab_top = TREE_TOP + box_h + FAN_H
    root_top = slab_top + slab_h + SLAB_GAP
    H = round(root_top + ROOT_H + 46)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="技术栈树：基础技能在根部，向上分叉到各专业方向" font-family="{FONT}">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<text x="{PAD}" y="0" font-size="0" fill="none">.</text>',
    ]

    # --- branch boxes (top) ---
    for i, (b, blocks, _h) in enumerate(cols):
        x = PAD + i * (bw + BRANCH_GAP)
        color = t["track"][i % len(t["track"])]
        o.append(f'<rect x="{x:.1f}" y="{TREE_TOP}" width="{bw:.1f}" height="{box_h}" '
                 f'rx="9" fill="{t["pill"]}" stroke="{color}" stroke-opacity="0.40"/>')
        o.append(f'<rect x="{x:.1f}" y="{TREE_TOP}" width="{bw:.1f}" height="3.5" '
                 f'rx="1.8" fill="{color}" fill-opacity="0.85"/>')
        cy = TREE_TOP + 8 + LH_NAME - 4
        o.append(f'<text x="{x + bw / 2:.1f}" y="{cy}" text-anchor="middle" '
                 f'font-size="{NAME_SIZE}" font-weight="650" fill="{t["text"]}">'
                 f'{e(b["name"])}</text>')
        cy += 4
        for name, res in blocks:
            cy += LH_SKILL
            o.append(f'<text x="{x + 8:.1f}" y="{cy}" font-size="{SKILL_SIZE}" '
                     f'fill="{t["text"]}">{e(_fit(name[0], SKILL_SIZE, bw - 16)[0])}</text>')
            if res:
                for line in res:
                    cy += LH_RES
                    o.append(f'<text x="{x + 8:.1f}" y="{cy}" font-size="{RES_SIZE}" '
                             f'fill="{t["sub"]}">{e(line)}</text>')
            else:
                cy += LH_RES
                o.append(f'<text x="{x + 8:.1f}" y="{cy}" font-size="{RES_SIZE}" '
                         f'fill="{t["muted"]}" fill-opacity="0.8">待补充</text>')
            cy += 4

    # --- fan: slab top centre -> each branch box bottom centre ---
    cx0, cy0 = W / 2, slab_top
    for i in range(n):
        bx = PAD + i * (bw + BRANCH_GAP) + bw / 2
        by = TREE_TOP + box_h
        color = t["track"][i % len(t["track"])]
        o.append(f'<path d="M{cx0:.1f} {cy0} C{cx0:.1f} {cy0 - FAN_H * 0.55:.1f} '
                 f'{bx:.1f} {by + FAN_H * 0.45:.1f} {bx:.1f} {by}" '
                 f'fill="none" stroke="{color}" stroke-opacity="0.45" stroke-width="1.5"/>')

    # --- foundation slab ---
    o.append(f'<rect x="{PAD}" y="{slab_top}" width="{W - 2 * PAD}" height="{slab_h}" '
             f'rx="10" fill="{t["pill"]}" stroke="{t["tree"]}"/>')
    o.append(f'<text x="{PAD + 12}" y="{slab_top + 16}" font-size="{NAME_SIZE}" '
             f'font-weight="650" fill="{t["text"]}">{e(SKILLTREE["foundation"]["name"])}</text>')
    o.append(f'<text x="{W - PAD - 12}" y="{slab_top + 16}" text-anchor="end" '
             f'font-size="9" fill="{t["muted"]}">所有方向的共同基础</text>')
    for j, (name, res) in enumerate(fblocks):
        fx = PAD + 12 + j * fw
        fy = slab_top + SLAB_LABEL_H + 10
        o.append(f'<text x="{fx:.1f}" y="{fy}" font-size="{SKILL_SIZE}" '
                 f'fill="{t["text"]}">{e(_fit(name[0], SKILL_SIZE, fw - 16)[0])}</text>')
        for line in (res or ["待补充"]):
            fy += LH_RES
            muted = not res
            o.append(f'<text x="{fx:.1f}" y="{fy}" font-size="{RES_SIZE}" '
                     f'fill="{t["muted"] if muted else t["sub"]}"'
                     f'{" fill-opacity=\"0.8\"" if muted else ""}>{e(line)}</text>')

    # --- root ---
    rw = _tw(SKILLTREE["root"], 12.5) + 44
    rx = (W - rw) / 2
    o.append(f'<line x1="{W / 2}" y1="{root_top}" x2="{W / 2}" y2="{slab_top + slab_h}" '
             f'stroke="{t["tree"]}" stroke-width="1.3"/>')
    o.append(f'<rect x="{rx:.1f}" y="{root_top}" width="{rw:.1f}" height="{ROOT_H}" '
             f'rx="{ROOT_H / 2}" fill="{t["text"]}"/>')
    o.append(f'<text x="{W / 2}" y="{root_top + ROOT_H / 2 + 4.4}" text-anchor="middle" '
             f'font-size="13" font-weight="700" fill="{t["bg"]}">'
             f'{e(SKILLTREE["root"])}</text>')

    o.append(f'<text x="{PAD}" y="{H - 20}" font-size="10.5" fill="{t["muted"]}">'
             f'共 {len(by_rel)} 份资源 · 灰色「待补充」= 该技能还没有收录资源　·　'
             f'{generate_index.PAGES_URL.replace("https://", "").rstrip("/")}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def render_skilltree_md(by_rel: dict[str, dict]) -> str:
    def skill_md(s: dict) -> str:
        if not s["items"]:
            return f"- {s['name']} — _待补充_"
        names = " · ".join(f"[{by_rel[r]['title']}]({r})" for r in s["items"])
        return f"- {s['name']} — {names}"

    out = ["**基础层**（所有方向的共同基础）", ""]
    out += [skill_md(s) for s in SKILLTREE["foundation"]["skills"]]
    out.append("")
    for b in SKILLTREE["branches"]:
        out.append(f"**{b['name']}**")
        out.append("")
        out += [skill_md(s) for s in b["skills"]]
        out.append("")
    return "\n".join(out).rstrip()


# ---------------------------------------------------------------- driver
def build(check: bool = False) -> int:
    groups = load_resources()
    index_md = render_index_md(groups)
    by_rel = {r["rel"]: r for items in groups.values() for r in items}
    check_roadmap(by_rel)
    check_skilltree(by_rel)

    targets: list[tuple[pathlib.Path, str]] = [(RES / "0-Index.md", index_md)]

    for sub in SUBDIRS:
        p = RES / sub / "README.md"
        if not p.is_file():
            continue
        targets.append((p, splice(p.read_text(encoding="utf-8"), TAB_START, TAB_END,
                                  render_table(groups[sub], sub), str(p))))

    readme_p = ROOT / "README.md"
    readme = readme_p.read_text(encoding="utf-8")
    readme = splice(readme, MAP_START, MAP_END, render_roadmap_md(by_rel), "README.md")
    readme = splice(readme, TREE_START, TREE_END, render_skilltree_md(by_rel), "README.md")
    targets.append((readme_p, splice(readme, NAV_START, NAV_END,
                                     render_nav(groups), "README.md")))

    # index.html consumes the freshly rendered README nav + 0-Index
    targets.append((ROOT / "index.html",
                    generate_index.build(targets[-1][1], index_md)))

    for theme in ("light", "dark"):
        targets.append((ROOT / "assets" / f"roadmap-{theme}.svg",
                        render_roadmap(by_rel, theme)))
        targets.append((ROOT / "assets" / f"skilltree-{theme}.svg",
                        render_skilltree(by_rel, theme)))

    stale = []
    for p, new in targets:
        old = p.read_text(encoding="utf-8") if p.is_file() else ""
        if old == new:
            continue
        stale.append(p)
        if not check:
            p.parent.mkdir(parents=True, exist_ok=True)
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
    n_gap = sum(1 for s in all_tree_skills() if not s["items"])
    print(f"{n_items} resources, {n_tags} tags, {len(SUBDIRS)} categories, "
          f"{len(ROADMAP)} roadmap tracks, {len(SKILLTREE['branches'])} branches / {n_gap} gaps")

    # A pill that had to be cut needs a `short:` frontmatter field to read well.
    for track in ROADMAP:
        for rel in track["items"]:
            _text, cut = _fit(by_rel[rel]["short"], SIZE, 168)
            if cut:
                print(f"  note: roadmap label truncated — add `short:` to {rel}")
    return 1 if (check and stale) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, exit 1 if stale")
    sys.exit(build(ap.parse_args().check))
