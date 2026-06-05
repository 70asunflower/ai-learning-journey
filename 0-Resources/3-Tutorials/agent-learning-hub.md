---
source: https://github.com/datawhalechina/Agent-Learning-Hub
date: 2026-06-05
tags: [ai-agent, agent, tutorial, roadmap, datawhale, mcp, tool-use]
---

# Agent-Learning-Hub — AI Agent 学习路线与资料库

> Datawhale 出品，2.9k⭐，一份有观点、可执行的 AI Agent 学习路线图

## 基本信息

| 项目 | 详情 |
|------|------|
| **组织** | Datawhale China |
| **作者** | 陈思州 |
| **Star** | 2.9k |
| **Fork** | 288 |
| **许可证** | MIT |
| **在线版** | [datawhalechina.github.io/Agent-Learning-Hub/](https://datawhalechina.github.io/Agent-Learning-Hub/) |
| **定位** | 不是链接合集，而是有优先级的可执行学习清单 |

## 核心学习原则

- 先动手再深读
- 宁要一个可靠的智能体，不要十个花哨的演示
- 在加更多智能体之前先加上评估
- 把多智能体当作协调问题来对待

## 学习优先级

| 优先级 | 学什么 | 为什么 |
|--------|--------|--------|
| 1 | Claude Code / Codex 类编程智能体 | Agent 工程的最佳实践（真实代码库、shell、文件、权限） |
| 2 | Agent harness 工程 | Agent 能力大部分来自 harness |
| 3 | OpenClaw / Hermes 类个人智能体 | 长时间运行、本地优先、跨应用、记忆、技能 |
| 4 | Skills / MCP / A2A / ACP | 技能复用、工具协议、智能体通信 |
| 5 | 评估与安全 | 没有评估和追踪就只是 demo |

## 8 阶段学习清单

| 阶段 | 内容 |
|------|------|
| 0 | 理解 Agent 是什么 — 区分 chatbot/workflow/agent/multi-agent |
| 1 | 搭建最小 Agent 循环 — LLM API + JSON 输出 + 工具调用 |
| 2 | 工具使用、RAG 与记忆 — 搜索/数据库/文件/浏览器/代码执行 |
| 3 | 深入学习一个现代 Agent Harness — Claude Code / OpenClaw / LangGraph |
| 4 | 多智能体是协调问题 — planner/executor/reviewer 角色 |
| 5 | Skills 与协议 — MCP / A2A / ACP / SKILL.md |
| 6 | 浏览器和计算机使用 Agent — Playwright + 安全限制 |
| 7 | 评估与可观测性 — 测试集、追踪、安全门控 |
| 8 | 部署真正的 Agent — CLI / Web / Slack / GitHub Action |

## 项目梯子（11 个层级）

| 层级 | 项目 |
|------|------|
| 1 | Calculator Agent — 最小工具调用循环 |
| 2 | Web Research Agent — 搜索、过滤、引用、总结 |
| 3 | PDF QA Agent — RAG、分块、检索 |
| 4 | Coding Review Agent — Diff 读取、风险排序 |
| 5 | Browser Agent — 页面观察、点击、提取 |
| 6 | Claude Code 类 Nano Agent — shell、文件编辑 |
| 7 | OpenClaw 类 Gateway — 通道、路由、记忆 |
| 8 | 可复用技能包 — SKILL.md 模板 |
| 9 | 多智能体写作器 — planner/writer/reviewer |
| 10 | 个人 Agent — 记忆、技能、消息入口 |
| 11 | 生产级 Harness — 评估、追踪、CI |

_Last updated: 2026-06-05_
