---
source: https://github.com/nexu-io/open-design
date: 2026-05-05
tags: [ai-design, open-source, coding-agent, claude-design, nextjs, local-first]
---

# Open Design — AI 设计工具（Claude Design 开源替代）

> Local-first, open-source alternative to Claude Design. Same artifact-first design loop, none of the lock-in.
> GitHub: https://github.com/nexu-io/open-design

## Overview

Open Design (OD) 是 Claude Design 的开源替代品。Claude Design 展示了 LLM 产出设计制品（而非纯文本）的潜力，但它闭源、付费、云锁定、绑定 Anthropic 模型。Open Design 用同样的 artifact-first 设计循环，实现零锁定。

**核心理念**：We don't ship an agent. Yours is good enough. — 不内置 Agent 运行时，直接使用你已安装的 coding agent CLI。

## Key Features

| Feature | Description |
|---------|-------------|
| **13 种 Agent CLI 适配** | Claude Code / Codex / Devin / Cursor Agent / Gemini CLI / OpenCode / Qwen / GitHub Copilot / Hermes / Kimi / Pi / Kiro / Mistral Vibe，自动检测 PATH，一键切换 |
| **BYOK 多模型代理** | 支持 Anthropic / OpenAI / Azure OpenAI / Google Gemini，填 baseUrl + apiKey + model 即用 |
| **31 个组合式 Skills** | 27 prototype + 4 deck 模式，覆盖 Web 原型、移动 App、Dashboard、Pitch Deck、杂志、社交媒体轮播等 |
| **129 套设计系统** | 2 手写 starter + 70 产品系统（Linear/Stripe/Vercel/Airbnb/Tesla/Notion/Apple 等）+ 57 设计 skill，均为便携式 DESIGN.md |
| **5 种视觉方向** | Editorial Monocle / Modern Minimal / Warm Soft / Tech Utility / Brutalist Experimental |
| **交互式需求表单** | Turn 1 展示 discovery form（surface/audience/tone/brand/scale），防止 80% 方向跑偏 |
| **5 维自评门控** | Philosophy / Hierarchy / Execution / Specificity / Restraint 五维打分后才输出 |
| **反 AI-slop 机制** | Brand-spec 提取 / P0-P1-P2 检查清单 / slop 黑名单 / 真实占位符替代假数据 |
| **多格式导出** | HTML / PDF / PPTX / ZIP / Markdown |
| **Claude Design ZIP 导入** | 可继续在 Anthropic 停下的地方编辑 |
| **MCP Server** | Stdio MCP server，让 coding agent 直接读取 OD 项目文件 |
| **多媒体生成** | gpt-image-2 图片 + Seedance 2.0 视频 + HyperFrames HTML→MP4 动效，93 个提示词模板 |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 App Router + React 18 + TypeScript |
| Daemon | Node 24 + Express + SSE streaming + better-sqlite3 |
| Agent Transport | child_process.spawn + per-CLI typed-event parsers |
| BYOK Proxy | Provider-specific upstream APIs, normalized SSE, SSRF-guarded |
| Storage | SQLite (.od/app.sqlite) + plain files in .od/projects/ |
| Preview | Sandboxed iframe via srcdoc + per-skill artifact parser |
| Desktop (optional) | Electron shell with sidecar IPC |
| License | Apache-2.0 |

## Architecture

```
Browser (Next.js 16) ←→ Local Daemon (Express + SQLite)
                              ↓ spawn(cli)
                         Agent CLIs (claude, codex, gemini, etc.)
                              ↑ SSE
                         BYOK Proxy (/api/proxy/{provider}/stream)
```

Daemon 是唯一的特权进程：在项目的 artifact 文件夹中 spawn 用户的 CLI，给 agent 真实的 Read / Write / Bash / WebFetch 工具。

## 与竞品对比

| 维度 | Claude Design | Open CoDesign | **Open Design** |
|------|--------------|---------------|-----------------|
| 可部署到 Vercel | ❌ | ❌ | ✅ |
| Agent 运行时 | 内置 | 内置 (pi-ai) | **委托给用户 CLI** |
| Skills 数量 | 专有 | 12 custom TS | **31 file-based** |
| 设计系统 | 专有 | v0.2 路线图 | **129 已发布** |
| 需求表单 | ❌ | ❌ | ✅ |
| 自评门控 | ❌ | ❌ | ✅ |

---

*Last updated: 2026-05-05*
