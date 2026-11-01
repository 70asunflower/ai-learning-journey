#!/usr/bin/env python3
"""Normalize resource tags against the alias registry in scripts/tags.json.

Tags live in exactly one place now — the `tags:` line of each resource's
frontmatter. 0-Index.md is generated from it by build.py, so rewriting tags
here is enough to fix every view (index, subfolder tables, README nav, site).

Usage:
    python scripts/normalize_tags.py            # rewrite in place
    python scripts/normalize_tags.py --check    # report only, exit 1 if dirty
    python scripts/normalize_tags.py --report   # tag frequency / singleton stats
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "0-Resources"
REGISTRY = ROOT / "scripts" / "tags.json"


def load_aliases() -> dict[str, str]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["aliases"]


def canonical(tags: list[str], aliases: dict[str, str]) -> list[str]:
    """Map aliases to canonical tags, drop duplicates, keep first-seen order."""
    out: list[str] = []
    for t in tags:
        t = aliases.get(t, t)
        if t not in out:
            out.append(t)
    return out


def parse_tag_list(raw: str) -> list[str]:
    """Parse a frontmatter tag list: `[a, b]` or bare `a b`."""
    s = raw.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [p.strip().strip("`").lstrip("#").strip() for p in s.split(",") if p.strip()]


# ---- 1. resource frontmatter ----
def rewrite_frontmatter(text: str, aliases: dict[str, str]) -> str:
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", text, re.DOTALL)
    if not m:
        return text
    head, body, tail = m.groups()
    out_lines = []
    for line in body.splitlines():
        if re.match(r"^tags:\s*", line):
            tags = parse_tag_list(line.split(":", 1)[1])
            if tags:
                line = "tags: [" + ", ".join(canonical(tags, aliases)) + "]"
        out_lines.append(line)
    return head + "\n".join(out_lines) + tail + text[m.end():]


# ---- 2. tag statistics (frontmatter is the only place tags live) ----
def resource_files() -> list[pathlib.Path]:
    return [
        p for p in sorted(RES.rglob("*.md"))
        if p.name not in ("README.md", "0-Index.md")
    ]


def frontmatter_tags(p: pathlib.Path) -> list[str]:
    text = p.read_text(encoding="utf-8")
    m = re.search(r"^tags:\s*(.*)$", text, re.M)
    return parse_tag_list(m.group(1)) if m else []


def collect_tags(aliases: dict[str, str]) -> dict[str, int]:
    """Canonical tag -> number of resources using it."""
    counts: dict[str, int] = {}
    for p in resource_files():
        for t in canonical(frontmatter_tags(p), aliases):
            counts[t] = counts.get(t, 0) + 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, do not write")
    ap.add_argument("--report", action="store_true", help="print tag statistics and exit")
    args = ap.parse_args()

    aliases = load_aliases()

    if args.report:
        counts = collect_tags(aliases)
        singles = sorted(t for t, c in counts.items() if c == 1)
        print(f"unique tags : {len(counts)}")
        print(f"assignments : {sum(counts.values())}")
        print(f"singletons  : {len(singles)}")
        print(f"used >= 3   : {sum(1 for c in counts.values() if c >= 3)}")
        print("\ntop 20:", ", ".join(f"{t}({c})" for t, c in
                                    sorted(counts.items(), key=lambda kv: -kv[1])[:20]))
        print("\nsingletons:", " ".join(singles) or "(none)")
        return 0

    changed: list[str] = []
    for p in resource_files():
        text = p.read_text(encoding="utf-8")
        new = rewrite_frontmatter(text, aliases)
        if new != text:
            changed.append(str(p.relative_to(ROOT)).replace("\\", "/"))
            if not args.check:
                p.write_text(new, encoding="utf-8", newline="\n")

    if not changed:
        print("Tags already canonical.")
        return 0

    verb = "Would rewrite" if args.check else "Rewrote"
    print(f"{verb} {len(changed)} file(s):")
    for c in changed:
        print("  " + c)
    return 1 if args.check else 0


if __name__ == "__main__":
    sys.exit(main())
