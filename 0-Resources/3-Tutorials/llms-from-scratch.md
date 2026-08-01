---
source: https://github.com/rasbt/LLMs-from-scratch
date: 2026-05-07
tags: [llm, from-scratch, pytorch, gpt, fine-tuning, lora, textbook]
---

# Build a Large Language Model (From Scratch)

> Sebastian Raschka 著，从零构建 ChatGPT 级 LLM 的完整指南
> GitHub: https://github.com/rasbt/LLMs-from-scratch（92k+ Stars）

## Overview

Manning 2024 年出版的 *Build a Large Language Model (From Scratch)* 官方代码仓库。全书用 PyTorch 从零实现一个类 ChatGPT 的 LLM，不依赖任何外部 LLM 库，每一步都可理解、可修改、可运行。

## 内容覆盖

| 章节 | 主题 |
|------|------|
| Ch 1 | 理解大语言模型 |
| Ch 2 | 文本数据处理（tokenization / dataloader / BPE） |
| Ch 3 | 编码注意力机制（Multi-Head Attention） |
| Ch 4 | 从零实现 GPT 模型 |
| Ch 5 | 无标签数据预训练（训练循环 / 权重加载） |
| Ch 6 | 文本分类微调 |
| Ch 7 | 指令跟随微调 |
| App A | PyTorch 入门 |
| App D | 训练循环增强技巧 |
| App E | LoRA 参数高效微调 |

## 扩展内容

- **其他 LLM 架构从零实现**：Llama 3.2 / Qwen3 / Gemma 3 / Olmo 3 / Tiny Aya / Qwen3.5 / Gemma 4
- **注意力变体**：Grouped-Query Attention / Multi-Head Latent Attention / Sliding Window Attention / Gated DeltaNet
- **MoE / KV Cache / FLOPs 分析 / DPO 对齐**
- **BPE Tokenizer 从零实现**
- 配套 17 小时视频课程 + 170 页 Quiz PDF

## 适合谁

- 有 Python 基础，想从代码层面理解 LLM 内部机制
- PyTorch 经验非必需但有帮助
- CPU 即可运行大部分代码，GPU 加速更快

---

_Last updated: 2026-05-07_
