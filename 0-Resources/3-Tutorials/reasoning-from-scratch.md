---
source: https://github.com/rasbt/reasoning-from-scratch
date: 2026-05-07
tags: [reasoning, llm, reinforcement-learning, grpo, distillation, pytorch, textbook]
---

# Build a Reasoning Model (From Scratch)

> Sebastian Raschka 著，从预训练模型出发构建推理型 LLM
> GitHub: https://github.com/rasbt/reasoning-from-scratch（4.3k+ Stars）

## Overview

Manning 2025 年出版的 *Build a Reasoning Model (From Scratch)* 官方代码仓库。从预训练基座模型（Qwen3）出发，用 PyTorch 逐步实现具备推理能力的大语言模型，涵盖推理时扩展、强化学习训练、知识蒸馏三大路线，呼应 DeepSeek R1 等推理模型的技术范式。

## 内容覆盖

| 章节 | 主题 |
|------|------|
| Ch 1 | 理解推理模型 |
| Ch 2 | 用预训练 LLM 生成文本 |
| Ch 3 | 评估推理模型 |
| Ch 4 | 推理时扩展（多数投票等） |
| Ch 5 | 推理时扩展——自我精炼 |
| Ch 6 | 强化学习训练推理模型（GRPO） |
| Ch 7 | 改进 GRPO |
| Ch 8 | 蒸馏推理模型以提高效率 |

附录：Qwen3 源码解析 / 更大 LLM / 批处理与吞吐量 / LLM 评估方法 / 构建聊天界面

## 核心路线

1. **Inference-time Scaling** — 不重新训练，在推理阶段提升推理质量（多数投票 / 自我精炼）
2. **Reinforcement Learning (GRPO)** — 用强化学习训练推理行为
3. **Knowledge Distillation** — 将推理能力压缩到更小模型

## 适合谁

- 已读过 *LLMs-from-scratch* 或对 LLM 内部机制有基本了解
- Python + PyTorch 熟练
- Ch 2-4 可在消费级 CPU/GPU 运行；Ch 5-7 建议 GPU

---

_Last updated: 2026-05-07_
