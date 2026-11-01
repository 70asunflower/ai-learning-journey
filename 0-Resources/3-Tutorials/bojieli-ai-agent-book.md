---
title: 深入理解 AI Agent
summary: 李博杰开源书 45k+★：Agent = LLM + 上下文 + 工具，Harness 工程才是竞争力
source: https://bojieli.github.io/ai-agent-book/
date: 2026-09-14
tags: [ai-agent, llm, mcp, fine-tuning, reinforcement-learning, coding-agent, evaluation, book, chinese, open-source]
links: 
- https: //github.com/bojieli/ai-agent-book
---
# 深入理解 AI Agent：设计原理与工程实践

> 李博杰（bojieli）开源技术书（**45k+ Stars**，Apache 2.0，持续更新，GitHub Actions 自动重建站点）。核心公式：**Agent = LLM + 上下文 + 工具**；核心论断：**"Harness 工程才是竞争力"**——设计原则比模型迭代更长寿。中文原版 + 14 种社区翻译，每章附配套实验。

## 章节速览（2026-09 更新）

| 章 | 标题 | 核心内容 |
|----|------|----------|
| 1 | Agent 基础知识 | Agent = LLM + 上下文 + 工具；Harness 工程定位 |
| 2 | 上下文工程 | KV Cache、提示工程、Agent Skills、上下文压缩 |
| 3 | 用户记忆和知识库 | 用户记忆、RAG、结构化索引、知识图谱 |
| 4 | 工具 | MCP 协议、感知/执行/协作三类工具、异步 Agent |
| 5 | Coding Agent 与代码生成 | 代码是"能创造新工具的工具"，生产级 Coding Agent 全景 |
| 6 | Agent 的评估 | 评估环境、指标、统计显著性 |
| 7 | 模型后训练 | SFT、RL——把 Harness 反馈信号写入模型参数 |
| 8 | Agent 的持续进化 | 从可靠学习信号到知识、指令、程序与参数更新 |
| 9 | 多模态与实时交互 | 语音 Agent、Computer Use、机器人操作 |
| 10 | 多 Agent 协作 | 协作架构、失败模式、Agent 社会 |

## 六条主题线

1. **Harness 工程**——Agent 竞争力关键
2. **上下文工程**——上下文决定能力上限（KV Cache 视角很工程化）
3. **记忆与知识增强**——RAG、知识图谱
4. **工具体系**——MCP 协议与异步 Agent
5. **评估与后训练**——从评估信号到参数更新
6. **多模态交互与多 Agent 协作**

## 交付形态

- 在线阅读（默认）；中文 [PDF](https://github.com/bojieli/ai-agent-book/releases/download/latest/AI-Agents-in-Depth-zh-CN.pdf) / [EPUB](https://github.com/bojieli/ai-agent-book/releases/download/latest/AI-Agents-in-Depth-zh-CN.epub)
- 每章配套实验；附录思考题参考答案
- ⚠️ 侧边导航与"章节速览"偶有目录调整不同步，以速览（更新至 2026-09-03）为准

## 与既有资源的关系

- 与 Agent-Learning-Hub（Datawhale，路线图+项目清单）互补：那本管"学什么"，这本管"为什么这样设计"
- 第 2 章上下文工程 / 第 7 章后训练直接衔接 RLHF/推理系统知识；第 5 章 Coding Agent 解释了你正在用的这层工具链

_Last updated: 2026-09-14_