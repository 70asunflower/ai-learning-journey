#!/usr/bin/env python3
"""Generate a single-file tree-shaped learning index (index.html).

Data source: build.py SKILLTREE + each resource's frontmatter and Markdown body.
The page embeds marked.js and all resource bodies, so it works fully offline.
Templates below are derived from the reviewed single-file preview.
"""
import ast
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "70asunflower/ai-learning-journey"
REPO_URL = "https://github.com/" + REPO
PAGES_URL = "https://70asunflower.github.io/ai-learning-journey/"
SIBLINGS = [
    {"name": "AI Learning Journey", "url": "https://70asunflower.github.io/ai-learning-journey/"},
]
TITLE = "AI Learning Journey"
SUBTITLE = "学习路径索引"
MAX_CONTENT = 6000
GH = "https://github.com/" + REPO + "/blob/master/"


def load_skilltree():
    """Parse SKILLTREE out of build.py without importing it (no circular import)."""
    src = (ROOT / "scripts" / "build.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "SKILLTREE" for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError("SKILLTREE not found in scripts/build.py")


def frontmatter_and_body(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    fm["tags"] = [t.strip().strip("[] ") for t in fm.get("tags", "").split(",") if t.strip()]
    body = text[m.end():]
    body = re.sub(r"^#\s+.*\n", "", body, count=1)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
    body = re.sub(r"\]\((0-Resources/[^)]+)\)", lambda mm: "](" + GH + mm.group(1) + ")", body)
    body = re.sub(r"</script", "&lt;/script", body, flags=re.I)
    if len(body) > MAX_CONTENT:
        body = body[:MAX_CONTENT] + "\n\n> 正文已截断，完整内容请点击下方「在 GitHub 中查看原文」。"
    fm["content"] = body
    return fm, ""


def build_tree(skilltree):
    def node(rel):
        fm, _ = frontmatter_and_body(rel)
        return {"title": fm.get("title", ""), "short": fm.get("short", fm.get("title", "")),
                "desc": fm.get("summary", ""), "date": fm.get("date", ""),
                "tags": fm.get("tags", []), "content": fm.get("content", ""), "path": rel}
    def group(g):
        return {"name": g["name"], "skills": [
            {"name": s["name"], "items": [node(p) for p in s["items"]]} for s in g["skills"]]}
    return {"root": skilltree["root"], "foundation": group(skilltree["foundation"]),
            "branches": [group(b) for b in skilltree["branches"]]}


def build(skilltree=None):
    """Return the complete index.html text (deterministic, no today())."""
    from generate_index import marked_js
    tree = build_tree(skilltree if skilltree is not None else load_skilltree())
    return (HTML
            .replace("__TREE__", json.dumps(tree, ensure_ascii=False, separators=(",", ":")))
            .replace("__MARKED__", marked_js.replace("</script>", "<\\/script>"))
            .replace("__TITLE__", TITLE)
            .replace("__SUBTITLE__", SUBTITLE)
            .replace("__REPO_URL__", REPO_URL))


def main():
    out = ROOT / "index.html"
    html = build()
    out.write_text(html, encoding="utf-8", newline="\n")
    tree = build_tree(load_skilltree())
    groups = [tree["foundation"], *tree["branches"]]
    n = sum(len(s["items"]) for g in groups for s in g["skills"])
    print(f"Wrote {out} — {len(groups)} trunks, {n} resources, {len(html.encode('utf-8'))} bytes")
    return html


HTML = r'''<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · 学习路径</title>
<style>
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-hover: #f1f5f9;
  --ink: #0f172a;
  --muted: #475569;
  --faint: #94a3b8;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --accent: #2563eb;
  --shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

html[data-theme="dark"] {
  --bg: #0f1115;
  --surface: #181b20;
  --surface-hover: #22262e;
  --ink: #f1f5f9;
  --muted: #94a3b8;
  --faint: #64748b;
  --border: #2a2f3a;
  --border-strong: #3f4756;
  --accent: #3b82f6;
  --shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 14px;
  line-height: 1.5;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  transition: background-color 0.2s, color 0.2s;
}
a { color: inherit; text-decoration: none; }
button, input { font-family: inherit; }

/* 顶部导航 */
.topbar {
  position: sticky;
  top: 0;
  z-index: 60;
  background: color-mix(in srgb, var(--surface) 88%, transparent);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.topin {
  max-width: 1400px;
  margin: 0 auto;
  padding: 12px 28px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.2px;
  white-space: nowrap;
}
.brand span {
  color: var(--faint);
  font-size: 13px;
  font-weight: 400;
  margin-left: 8px;
}
.spacer { flex: 1; }
.tbtn {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.tbtn:hover {
  color: var(--ink);
  border-color: var(--border-strong);
  background: var(--surface-hover);
}

/* 图标按钮 */
.ibtn{width:34px;height:34px;flex-shrink:0;display:inline-grid;place-items:center;padding:0;
  border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:7px;
  cursor:pointer;transition:all .15s}
.ibtn:hover{color:var(--ink);border-color:var(--border-strong);background:var(--surface-hover)}
.ibtn svg{width:16px;height:16px;grid-area:1/1}
.ibtn{position:relative}
.ibtn::after{content:attr(data-tip);position:absolute;top:calc(100% + 9px);left:50%;
  transform:translateX(-50%) translateY(-4px);background:var(--ink);color:var(--surface);
  font-size:11px;line-height:1.4;white-space:nowrap;padding:5px 9px;border-radius:6px;
  box-shadow:var(--shadow);opacity:0;pointer-events:none;transition:opacity .16s,transform .16s;z-index:100}
.ibtn:hover::after{opacity:1;transform:translateX(-50%) translateY(0)}
html[data-theme="light"] .i-moon{display:none}
html[data-theme="dark"] .i-sun{display:none}

/* 头部说明 */
.intro {
  max-width: 1400px;
  margin: 0 auto;
  padding: 36px 28px 18px;
}
.intro h1 {
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 700;
  line-height: 1.25;
  margin: 0;
  letter-spacing: -0.5px;
}
.intro p {
  color: var(--muted);
  max-width: 720px;
  margin: 8px 0 0;
  font-size: 13.5px;
}
.intro .meta {
  font-size: 12px;
  color: var(--faint);
  margin-top: 10px;
}
.intro .meta b {
  color: var(--ink);
  font-weight: 600;
}

/* 搜索与筛选栏 */
.controls {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 28px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.search {
  max-width: 460px;
  position: relative;
}
.search input {
  width: 100%;
  padding: 8px 12px 8px 34px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  color: var(--ink);
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.search input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 14%, transparent);
}
.search svg {
  position: absolute;
  left: 11px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--faint);
}

.legend {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.lg {
  border: 1px solid var(--border);
  background: var(--surface);
  border-radius: 6px;
  padding: 5px 11px;
  font-size: 12px;
  color: var(--muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s;
}
.lg i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--c);
}
.lg:hover {
  color: var(--ink);
  border-color: var(--border-strong);
}
.lg.on {
  background: var(--ink);
  color: var(--surface);
  border-color: var(--ink);
}

/* 树状图画布 */
.stage {
  max-width: 1400px;
  margin: 0 auto;
  padding: 8px 28px 80px;
  overflow-x: auto;
}
.tree {
  position: relative;
  min-width: 1220px;
  margin: 0 auto;
}
.wires {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}
.wires path {
  transition: opacity 0.2s, stroke-width 0.2s;
}
.divider-line {
  position: absolute;
  left: 200px;
  right: 20px;
  border-top: 1px dashed var(--border-strong);
  pointer-events: none;
}
.divider-label {
  position: absolute;
  right: 24px;
  transform: translateY(-50%);
  background: var(--bg);
  padding: 0 8px;
  font-size: 11px;
  color: var(--faint);
}

.node {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  transition: opacity 0.2s, transform 0.15s, border-color 0.15s, background-color 0.15s;
}
.node.dim { opacity: 0.14; }

/* 根节点 */
.n-root {
  left: 8px;
  width: 152px;
  padding: 12px 14px;
  border-radius: 8px;
  background: var(--ink);
  color: var(--surface);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  box-shadow: var(--shadow);
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}
.n-root small {
  font-size: 11px;
  font-weight: 400;
  opacity: 0.65;
}

/* 主干节点 */
.n-trunk {
  left: 210px;
  width: 184px;
  padding: 7px 11px;
  border-radius: 7px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3.5px solid var(--c);
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}
.n-trunk:hover, .n-trunk.active-path {
  border-color: var(--c);
  box-shadow: var(--shadow);
}
.n-trunk .badge-base {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--surface-hover);
  color: var(--muted);
}
.n-trunk .cnt {
  margin-left: auto;
  color: var(--faint);
  font-size: 11px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-weight: 400;
}
.n-trunk .fold {
  font-size: 11px;
  color: var(--faint);
  font-weight: 400;
  width: 12px;
  text-align: center;
}

/* 技能节点 */
.n-skill {
  left: 440px;
  width: 184px;
  padding: 6px 10px;
  border-radius: 6px;
  background: var(--surface);
  border: 1px solid var(--border);
  font-size: 12px;
  color: var(--muted);
  cursor: pointer;
}
.n-skill:hover, .n-skill.active-path {
  color: var(--ink);
  border-color: var(--c);
  background: var(--surface-hover);
}
.n-skill .fold {
  margin-left: auto;
  font-size: 11px;
  color: var(--faint);
}
.n-skill.empty {
  cursor: default;
  opacity: 0.45;
  border-style: dashed;
  background: transparent;
}
.n-skill.empty:hover {
  color: var(--muted);
  border-color: var(--border);
  background: transparent;
}

/* 资源叶子节点 */
.n-leaf {
  left: 672px;
  width: 520px;
  padding: 3px 8px 3px 4px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12.5px;
}
.n-leaf:hover {
  background: var(--surface);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.n-leaf .pip {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  border-radius: 50%;
  border: 1.5px solid var(--c);
  display: grid;
  place-items: center;
  font-size: 9px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  color: var(--c);
  background: var(--surface);
  transition: all 0.15s;
}
.n-leaf .txt {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--ink);
}
.n-leaf .kind {
  margin-left: auto;
  flex-shrink: 0;
  font-size: 10.5px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--surface-hover);
  color: var(--muted);
  border: 1px solid var(--border);
}
.n-leaf:hover .pip, .n-leaf.selected .pip {
  background: var(--c);
  color: #ffffff;
}
.n-leaf:hover .txt, .n-leaf.selected .txt {
  color: var(--c);
  font-weight: 600;
}
.n-leaf.hit .pip {
  background: var(--c);
  color: #ffffff;
  box-shadow: 0 0 0 2px var(--surface), 0 0 0 4px var(--c);
}
.n-leaf.faded { opacity: 0.18; }

/* 侧边详情抽屉 */
.drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 80;
  background: rgba(15, 23, 42, 0.25);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}
.drawer-mask.open {
  opacity: 1;
  pointer-events: auto;
}
.drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 90;
  width: min(480px, 94vw);
  background: var(--surface);
  border-left: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transform: translateX(100%);
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}
.drawer.open { transform: translateX(0); }
.drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.breadcrumb {
  font-size: 12px;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 6px;
}
.breadcrumb i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.close-btn {
  border: 1px solid var(--border);
  background: transparent;
  color: var(--muted);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  display: grid;
  place-items: center;
  font-size: 16px;
}
.close-btn:hover {
  color: var(--ink);
  background: var(--surface-hover);
}
.drawer h2 {
  margin: 0;
  font-size: 18px;
  line-height: 1.4;
  font-weight: 700;
}
.drawer-desc {
  margin: 0;
  color: var(--muted);
  font-size: 13.5px;
  line-height: 1.65;
  padding: 12px 14px;
  background: var(--bg);
  border-radius: 8px;
  border: 1px solid var(--border);
}
.drawer-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.drawer-tags span {
  font-size: 11.5px;
  padding: 3px 8px;
  border-radius: 5px;
  background: var(--surface-hover);
  color: var(--muted);
  border: 1px solid var(--border);
}
.drawer-meta {
  font-size: 12px;
  color: var(--faint);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
/* 抽屉正文：直接渲染资源 Markdown */
.drawer-body{flex:1;min-height:0;overflow-y:auto;border:1px solid var(--border);border-radius:8px;
  padding:14px 16px;background:var(--bg);font-size:13px;line-height:1.75}
.drawer-body h1,.drawer-body h2,.drawer-body h3{line-height:1.35;margin:1.2em 0 .5em;font-weight:650}
.drawer-body h1{font-size:19px;border-bottom:1px solid var(--border);padding-bottom:.3em}
.drawer-body h2{font-size:16px} .drawer-body h3{font-size:14px}
.drawer-body p{margin:.6em 0}
.drawer-body a{color:var(--accent);text-decoration:underline;text-underline-offset:2px}
.drawer-body code{background:var(--surface-hover);padding:1px 5px;border-radius:4px;font-size:.9em;font-family:ui-monospace,Consolas,monospace}
.drawer-body pre{background:var(--surface-hover);padding:11px 13px;border-radius:7px;overflow-x:auto;line-height:1.5}
.drawer-body pre code{background:transparent;padding:0}
.drawer-body blockquote{margin:.7em 0;padding:.3em .9em;border-left:3px solid var(--border-strong);color:var(--muted)}
.drawer-body table{border-collapse:collapse;width:100%;margin:.8em 0;font-size:12px}
.drawer-body th,.drawer-body td{border:1px solid var(--border);padding:5px 7px;text-align:left}
.drawer-body ul,.drawer-body ol{padding-left:1.4em;margin:.5em 0}
.drawer-body hr{border:0;border-top:1px solid var(--border);margin:1em 0}
.drawer-actions {
  padding-top: 4px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 10px;
}
.primary-btn {
  flex: 1;
  text-align: center;
  background: var(--ink);
  color: var(--surface);
  padding: 10px 16px;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 500;
  transition: opacity 0.15s;
}
.primary-btn:hover { opacity: 0.88; }

footer {
  border-top: 1px solid var(--border);
  text-align: center;
  color: var(--faint);
  font-size: 12px;
  padding: 20px;
}

@media (max-width: 760px) {
  .intro, .controls, .stage, .topin { padding-left: 16px; padding-right: 16px; }
}
</style>
</head>
<body>

<header class="topbar">
  <div class="topin">
    <a class="brand" href="#">__TITLE__ <span>__SUBTITLE__</span></a>
    <span class="spacer"></span>
    <button class="ibtn" id="expand" type="button" data-tip="展开全部" aria-label="展开全部"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg></button>
    <button class="ibtn" id="collapse" type="button" data-tip="收起全部" aria-label="收起全部"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v6H3"/><path d="M15 21v-6h6"/><path d="M3 3l6 6"/><path d="M21 21l-6-6"/></svg></button>
    <a class="ibtn" href="__REPO_URL__" target="_blank" rel="noopener" data-tip="在 GitHub 打开仓库" aria-label="GitHub 仓库"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A7.995 7.995 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg></a>
    <button class="ibtn" id="theme" type="button" data-tip="切换到夜间模式" aria-label="切换昼夜"><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg><svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>
  </div>
</header>

<section class="intro">
  <h1>AI 技术栈与学习路径</h1>
  <p>从左侧根节点向右依次展开为<b>学习方向</b>、<b>具体技能</b>与<b>学习资源</b>。悬停资源可高亮所属完整路径，点击资源可查看详情与仓库原文链接。</p>
  <div class="meta">
    包含 <b id="nTrunk">1 个基础层 + 7 个技术方向</b> · <b id="nSkill">24</b> 个技能模块 · <b id="nLeaf">41</b> 份精选资源
  </div>
</section>

<div class="controls">
  <label class="search">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
    <input id="q" type="search" placeholder="搜索标题、关键词或标签，自动展开匹配路径…" autocomplete="off">
  </label>
  <div class="legend" id="legend"></div>
</div>

<div class="stage">
  <div class="tree" id="tree">
    <svg class="wires" id="wires" xmlns="http://www.w3.org/2000/svg"></svg>
    <div id="nodes"></div>
  </div>
</div>

<!-- 右侧详情抽屉 -->
<div class="drawer-mask" id="drawerMask"></div>
<aside class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-head">
    <div class="breadcrumb" id="dPath"></div>
    <button class="close-btn" id="dClose" type="button" aria-label="关闭">×</button>
  </div>
  <h2 id="dTitle"></h2>
  <p class="drawer-desc" id="dDesc"></p>
  <div class="drawer-tags" id="dTags"></div>
  <div class="drawer-meta" id="dMeta"></div>
  <div class="drawer-body" id="dBody"></div>
  <div class="drawer-actions">
    <a class="primary-btn" id="dLink" href="#" target="_blank" rel="noopener">在 GitHub 中查看原文 ↗</a>
  </div>
</aside>

<footer>数据同步自仓库 build.py · 点击任意资源节点查看简介与路径归属</footer>

<script>__MARKED__</script>
<script>
const TREE = __TREE__;

// 现代简约低饱和度色板
const COLORS = ["#64748b", "#2563eb", "#059669", "#d97706", "#7c3aed", "#db2777", "#0891b2", "#4f46e5"];
const REPO = "https://github.com/70asunflower/ai-learning-journey/blob/master/";
const el = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const short = (s, n = 36) => s.length > n ? s.slice(0, n) + "…" : s;

// 根据标签提取资源类型，帮助判断学习方式
function getResourceKind(tags) {
  if (tags.includes("from-scratch")) return "手搓实战";
  if (tags.includes("book")) return "书籍";
  if (tags.includes("course")) return "系统课程";
  if (tags.includes("docs")) return "官方文档";
  if (tags.includes("framework")) return "框架源码";
  if (tags.includes("visualization")) return "交互可视化";
  if (tags.includes("roadmap")) return "学习路线";
  if (tags.includes("blog")) return "博客专栏";
  if (tags.includes("video")) return "视频";
  if (tags.includes("tool") || tags.includes("benchmarking")) return "工具";
  return "教程";
}

const folded = new Set();
let focusTrunk = -1;
let query = "";
let selectedPath = "";

const trunks = [
  { ...TREE.foundation, isBase: true },
  ...TREE.branches.map(b => ({ ...b, isBase: false }))
].map((t, i) => ({ name: t.name, skills: t.skills, isBase: t.isBase, i }));

el("nTrunk").textContent = `1 个基础层 + ${TREE.branches.length} 个技术方向`;
el("nSkill").textContent = trunks.reduce((a, t) => a + t.skills.length, 0);
el("nLeaf").textContent = trunks.reduce((a, t) => a + t.skills.reduce((b, s) => b + s.items.length, 0), 0);

// 渲染顶部筛选按钮
el("legend").innerHTML = `<button class="lg on" data-i="-1" type="button"><i style="background:var(--ink)"></i>全部路径</button>` +
  trunks.map(t => `<button class="lg" data-i="${t.i}" type="button" style="--c:${COLORS[t.i]}"><i></i>${esc(t.name)}</button>`).join("");

function setFocusTrunk(idx, updateHash = true) {
  focusTrunk = idx;
  el("legend").querySelectorAll("button").forEach(b => {
    b.classList.toggle("on", +b.dataset.i === idx);
  });
  if (updateHash) {
    if (idx === -1) {
      history.replaceState(null, "", location.pathname + location.search);
    } else {
      location.hash = "path=" + encodeURIComponent(trunks[idx].name);
    }
  }
  render();
}

el("legend").querySelectorAll("button").forEach(b => {
  b.onclick = () => setFocusTrunk(+b.dataset.i);
});

function curve(x1, y1, x2, y2) {
  const dx = Math.max(36, (x2 - x1) * 0.5);
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
}

function render() {
  const ROW = 36, PAD = 24;
  const nodes = [], wires = [];
  let row = 0;
  const yOfLeaf = () => (row++ * ROW + ROW / 2 + PAD);
  const trunkYs = [];
  let dividerY = null;

  trunks.forEach((t, idx) => {
    const c = COLORS[t.i], tk = "t" + t.i, tFold = folded.has(tk);
    const skillYs = [];

    t.skills.forEach((s, si) => {
      const sk = tk + "s" + si, sFold = folded.has(sk) || tFold;
      const leafYs = [];
      if (!sFold) s.items.forEach(() => leafYs.push(yOfLeaf()));
      const sy = leafYs.length ? leafYs.reduce((a, b) => a + b, 0) / leafYs.length : yOfLeaf();
      skillYs.push(sy);

      nodes.push(`
        <div class="node n-skill ${s.items.length ? '' : 'empty'}" id="node-${sk}" data-t="${t.i}" data-s="${sk}" style="top:${sy - 14}px;--c:${c}" data-key="${sk}" title="${s.items.length ? '点击展开或收起资源' : '暂无资源'}">
          <span>${esc(s.name)}</span>
          <span class="fold">${s.items.length ? (sFold ? '+' : '−') : '0'}</span>
        </div>
      `);

      if (!sFold) {
        s.items.forEach((it, li) => {
          const y = leafYs[li];
          const text = (it.title + " " + it.desc + " " + it.tags.join(" ")).toLowerCase();
          const hit = query && text.includes(query);
          const faded = query && !hit;
          const kind = getResourceKind(it.tags);
          const isSelected = selectedPath === it.path;

          nodes.push(`
            <div class="node n-leaf ${hit ? 'hit' : ''} ${faded ? 'faded' : ''} ${isSelected ? 'selected' : ''}"
              data-t="${t.i}" data-s="${sk}" data-path="${esc(it.path)}"
              style="top:${y - 13}px;--c:${c}">
              <span class="pip">${String(li + 1).padStart(2, '0')}</span>
              <span class="txt">${esc(short(it.short || it.title))}</span>
              <span class="kind">${esc(kind)}</span>
            </div>
          `);
          wires.push(`<path d="${curve(624, sy, 672, y)}" stroke="${c}" stroke-width="1.2" stroke-opacity="0.35" fill="none" data-t="${t.i}" data-s="${sk}" data-leaf="${esc(it.path)}"/>`);
        });
      }
    });

    const ty = skillYs.reduce((a, b) => a + b, 0) / skillYs.length;
    trunkYs.push(ty);

    nodes.push(`
      <div class="node n-trunk" id="node-${tk}" data-t="${t.i}" style="top:${ty - 17}px;--c:${c}" data-key="${tk}" title="点击展开或收起该方向">
        <span>${esc(t.name)}</span>
        ${t.isBase ? '<span class="badge-base">前置</span>' : ''}
        <span class="cnt">${t.skills.reduce((a, s) => a + s.items.length, 0)}</span>
        <span class="fold">${tFold ? '+' : '−'}</span>
      </div>
    `);

    skillYs.forEach((sy, si) => {
      const sk = tk + "s" + si;
      wires.push(`<path d="${curve(394, ty, 440, sy)}" stroke="${c}" stroke-width="1.5" stroke-opacity="0.55" fill="none" data-t="${t.i}" data-s="${sk}"/>`);
    });

    // 在基础层之后记录分隔线位置
    if (idx === 0) {
      row += 0.4;
      dividerY = row * ROW + PAD - ROW * 0.2;
    }
  });

  const ry = trunkYs.reduce((a, b) => a + b, 0) / trunkYs.length;
  nodes.push(`
    <div class="node n-root" style="top:${ry - 26}px">
      <span>AI 技术栈</span>
      <small>7 大进阶方向</small>
    </div>
  `);
  trunkYs.forEach((ty, i) => {
    wires.push(`<path d="${curve(160, ry, 210, ty)}" stroke="${COLORS[i]}" stroke-width="2" stroke-opacity="0.7" fill="none" data-t="${i}"/>`);
  });

  const tree = el("tree"), H = row * ROW + PAD * 2, W = 1220;
  tree.style.height = H + "px";
  tree.style.width = W + "px";

  const svg = el("wires");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W);
  svg.setAttribute("height", H);
  svg.innerHTML = wires.join("");

  let dividerHTML = "";
  if (dividerY !== null) {
    dividerHTML = `<div class="divider-line" style="top:${dividerY}px"></div><div class="divider-label" style="top:${dividerY}px">进阶技术方向</div>`;
  }
  el("nodes").innerHTML = dividerHTML + nodes.join("");

  // 折叠事件
  el("nodes").querySelectorAll("[data-key]").forEach(n => {
    n.onclick = () => {
      const k = n.dataset.key;
      folded.has(k) ? folded.delete(k) : folded.add(k);
      render();
    };
  });

  // 应用主干聚焦过滤
  applyFocusState();
  bindLeafEvents();
}

function applyFocusState() {
  el("nodes").querySelectorAll(".node").forEach(n => {
    if (n.classList.contains("n-root")) return;
    n.classList.toggle("dim", focusTrunk !== -1 && +n.dataset.t !== focusTrunk);
  });
  el("wires").querySelectorAll("path").forEach(p => {
    const match = focusTrunk === -1 || +p.dataset.t === focusTrunk;
    p.style.opacity = match ? "1" : "0.08";
  });
}

// 悬停高亮完整路径 + 点击打开右侧详情抽屉
function bindLeafEvents() {
  el("nodes").querySelectorAll(".n-leaf").forEach(leaf => {
    const tIdx = leaf.dataset.t;
    const sKey = leaf.dataset.s;
    const path = leaf.dataset.path;

    leaf.addEventListener("mouseenter", () => {
      el("node-t" + tIdx)?.classList.add("active-path");
      el("node-" + sKey)?.classList.add("active-path");
      el("wires").querySelectorAll("path").forEach(p => {
        const isBranchRootWire = p.dataset.t === tIdx && !p.dataset.s;
        const isSkillWire = p.dataset.s === sKey && !p.dataset.leaf;
        const isLeafWire = p.dataset.leaf === path;
        if (isBranchRootWire || isSkillWire || isLeafWire) {
          p.style.opacity = "1";
          p.setAttribute("stroke-width", "2.4");
        } else {
          p.style.opacity = "0.12";
        }
      });
    });

    leaf.addEventListener("mouseleave", () => {
      el("node-t" + tIdx)?.classList.remove("active-path");
      el("node-" + sKey)?.classList.remove("active-path");
      el("wires").querySelectorAll("path").forEach(p => {
        const isRootWire = !p.dataset.s;
        const isSkillWire = p.dataset.s && !p.dataset.leaf;
        p.setAttribute("stroke-width", isRootWire ? "2" : (isSkillWire ? "1.5" : "1.2"));
      });
      applyFocusState();
    });

    leaf.addEventListener("click", () => openDrawer(path));
  });
}

// 详情抽屉控制
function openDrawer(path) {
  let found = null;
  trunks.forEach(t => {
    t.skills.forEach(s => {
      s.items.forEach(it => {
        if (it.path === path) found = { item: it, trunk: t, skill: s };
      });
    });
  });
  if (!found) return;

  selectedPath = path;
  el("nodes").querySelectorAll(".n-leaf").forEach(n => {
    n.classList.toggle("selected", n.dataset.path === path);
  });

  const c = COLORS[found.trunk.i];
  el("dPath").innerHTML = `<i style="background:${c}"></i> ${esc(found.trunk.name)} / ${esc(found.skill.name)}`;
  el("dTitle").textContent = found.item.title;
  el("dDesc").textContent = found.item.desc;
  el("dTags").innerHTML = found.item.tags.map(tag => `<span>#${esc(tag)}</span>`).join("");
  el("dMeta").textContent = `收录日期: ${found.item.date} · 路径: ${found.item.path}`;
  el("dLink").href = REPO + found.item.path;
  el("dBody").innerHTML = (window.marked && found.item.content)
    ? marked.parse(found.item.content)
    : '<p style="color:var(--muted)">正文暂不可用，请点击下方链接查看原文。</p>';
  el("dBody").scrollTop = 0;

  el("drawerMask").classList.add("open");
  el("drawer").classList.add("open");
  el("drawer").setAttribute("aria-hidden", "false");
}

function closeDrawer() {
  selectedPath = "";
  el("nodes").querySelectorAll(".n-leaf.selected").forEach(n => n.classList.remove("selected"));
  el("drawerMask").classList.remove("open");
  el("drawer").classList.remove("open");
  el("drawer").setAttribute("aria-hidden", "true");
}

el("dClose").onclick = closeDrawer;
el("drawerMask").onclick = closeDrawer;
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeDrawer();
});

// 展开/收起按钮
el("expand").onclick = () => { folded.clear(); render(); };
el("collapse").onclick = () => {
  folded.clear();
  trunks.forEach((t, i) => {
    folded.add("t" + i);
    t.skills.forEach((_, j) => folded.add("t" + i + "s" + j));
  });
  render();
};

// 搜索联动
el("q").addEventListener("input", e => {
  query = e.target.value.trim().toLowerCase();
  if (query) {
    folded.clear();
    trunks.forEach((t, ti) => t.skills.forEach((s, si) => {
      const has = s.items.some(it => (it.title + " " + it.desc + " " + it.tags.join(" ")).toLowerCase().includes(query));
      if (has) folded.delete("t" + ti + "s" + si);
      else folded.add("t" + ti + "s" + si);
    }));
  }
  render();
});

// 日间/夜间模式切换
el("theme").onclick = () => {
  const d = document.documentElement;
  const isDark = d.getAttribute("data-theme") !== "dark";
  d.setAttribute("data-theme", isDark ? "dark" : "light");
  el("theme").dataset.tip = isDark ? "切换到日间模式" : "切换到夜间模式";
};

// 初始化解析 URL Hash（支持 #path=推理与部署）
function initFromHash() {
  const hash = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (hash.startsWith("path=")) {
    const targetName = hash.slice(5);
    const matched = trunks.find(t => t.name === targetName);
    if (matched) {
      setFocusTrunk(matched.i, false);
      return;
    }
  }
  render();
}

initFromHash();
</script>
</body>
</html>'''


if __name__ == "__main__":
    main()
