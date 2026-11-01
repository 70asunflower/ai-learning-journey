---
source: https://bojieli.github.io/ai-infra-book/index.html
date: 2026-09-14
tags: [ai-infra, gpu, hardware, inference, training, distributed-systems, networking, scheduling, quantitative-analysis, book, chinese]
links:
  - https://bojieli.github.io/ai-infra-book/index.html
  - https://github.com/bojieli/ai-infra-book
  - https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf
---

# 深入理解 AI Infra：量化分析与系统设计

> 李博杰（bojieli）开源技术书，初稿持续修订中。全书 12 章，主线只有一条：**"数据搬移塑造了 AI Infra 的架构"**——反复追问五个问题：搬什么、搬多少、搬几次、经过哪里、谁必须等它。方法论是**从约束推导设计**：对照硬件容量、带宽、算力做量化估算。

## 章节速览

| 章 | 标题 | 核心问题 |
|----|------|----------|
| 1 | 初识 AI Infra | 一次生成需要多少显存、计算和数据读写？ |
| 2 | 模型架构 | 注意力、历史状态与专家结构如何改变系统需求？ |
| 3 | 推理与训练负载 | 任务阶段、到达模式和状态寿命如何影响资源需求？ |
| 4 | 加速器架构 | 计算、存储、带宽、功耗与成本如何取舍？ |
| 5 | 算子与运行时 | 融合、复用、并发和调度如何减少执行开销？ |
| 6 | 超节点 | 多设备协作如何平衡容量、吞吐和同步代价？ |
| 7 | 数据中心网络 | 带宽、通信方式和拥塞怎样影响计算效率？ |
| 8 | 推理优化 | 批处理、KV 管理、卸载与推测解码何时有效？ |
| 9 | 分布式推理 | 如何放置计算和状态，处理扩缩容与恢复？ |
| 10 | 训练系统 | 怎样安排显存、通信和重算？ |
| 11 | 资源调度与运行环境 | 模型服务和工具环境如何共享资源？ |
| 12 | 端边云协同 | 任务放本地/边缘/云端，怎样兼顾效果、延迟和成本？ |

## 关键论断

- **"模型成了 LLM 时代的操作系统，AI Infra 成了 LLM 时代的计算机体系结构"**——类比 OS/体系结构的学习路径
- 常见估算漏项：忘算 KV 缓存、忽略卡间通信——量化分析能兜住这些
- 正文唯一维护源是仓库 `manuscripts/` 目录的 Markdown；PDF 版公式/表格排版更完整

## 配套资源

- 量化计算项目（可复算数值的计算工具与固定输入）
- 按章节组织的配套实验与运行记录
- [PDF 下载](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)

## 与既有资源的关系

- 比 Ultra-Scale Playbook（训练并行专精）覆盖面更宽：推理/网络/调度/端边云都有
- 与 JAX Scaling Book、Infra Seminars 2026 互补；第 4 章加速器架构直接衔接数字 IC 方向
- 阅读顺序建议：前言 + 第 1 章打底（建立的模型/硬件/负载设定后面反复用）

_Last updated: 2026-09-14_