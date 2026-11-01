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

Usage:
    python scripts/build.py            # rewrite everything
    python scripts/build.py --check    # report staleness, exit 1 if anything differs

Adding a resource therefore means: write ONE .md file, run this, commit.
"""
import argparse
import pathlib
import re
import sys

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
