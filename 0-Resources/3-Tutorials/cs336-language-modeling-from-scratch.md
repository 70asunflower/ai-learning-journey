---
source: https://feigaobox10.github.io/llm-from-scratch-reader/
date: 2026-06-28
tags: [cs336, llm, from-scratch, tokenization, pretraining, alignment, chinese-book, free-book, stanford-course]
links:
  - https://cs336.stanford.edu/
  - https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV
---

# CS336 Language Modeling from Scratch — 从零构建语言模型

> 斯坦福 CS336 (Spring 2026, Percy Liang/Tatsunori Hashimoto) 全17讲改写为面向高中生的通识中文读本，完整、准确、保留全部专业术语。

## 基本信息

| 项目 | 详情 |
|------|------|
| **原著** | Stanford CS336 Language Modeling from Scratch (Spring 2026) |
| **讲师** | Percy Liang · Tatsunori Hashimoto |
| **改编** | 高飞的电子替身（微信 rohanjojo） |
| **许可** | CC BY-NC-SA 4.0 |
| **阅读方式** | HTML 在线 / PDF 下载 |
| **字数** | 约 8 万字 |
| **插图** | 20+ 原创示意图 |
| **GitHub** | [feigaobox10/llm-from-scratch-reader](https://github.com/feigaobox10/llm-from-scratch-reader) |
| **课程官网** | [cs336.stanford.edu](https://cs336.stanford.edu/) |
| **YouTube 课程视频** | [完整播放列表](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV) |

## 内容覆盖

| 模块 | 章节 |
|------|------|
| **分词 (Tokenizer)** | Byte-Pair Encoding、SentencePiece、Unigram 等分词算法原理与实现 |
| **架构** | Transformer、Attention Mechanism、Positional Encoding |
| **预训练** | 数据准备、训练目标、训练策略、损失函数 |
| **对齐** | RLHF、DPO、Instruction Tuning、RLVR 等对齐方法 |
| **评估** | 语言模型评估方法论、Benchmark |
| **系统优化** | GPU/TPU 编程、Triton Kernel、并行策略（TP/PP/DP） |
| **数据工程** | Common Crawl 处理、过滤、去重、数据混合 |

## 原版课程大纲 (Spring 2026)

| 讲次 | 主题 | 讲师 |
|------|------|------|
| 1 | 概览 & Tokenization | Percy |
| 2 | PyTorch (einops), 资源核算 (FLOPs/内存/算术强度) | Percy |
| 3 | 架构 & 超参数 | Tatsu |
| 4 | Attention 替代方案 & Mixture of Experts | Tatsu |
| 5 | GPU, TPU | Tatsu |
| 6 | Kernel, Triton | Percy |
| 7-8 | 并行策略 (TP/PP/DP/EP) | Percy + Tatsu |
| 9, 11 | Scaling Laws | Tatsu |
| 10 | 推理 | Percy |
| 12 | 评估 | Percy |
| 13-14 | 数据 (来源/过滤/去重/混合/合成数据) | Percy |
| 15-16 | 训练后对齐 (SFT/RLHF/RLVR) | Tatsu |
| 17 | 对齐 - 多模态 | Percy |
| 18-19 | 客座讲座 | Daniel Selsam, Dan Fu |

## 课程作业

| Assignment | 内容 | 技能点 |
|------------|------|--------|
| **A1: Basics** | 实现 Tokenizer / 模型架构 / 优化器，训练最小语言模型 | Transformer 全栈实现 |
| **A2: Systems** | Profile 模型 → Triton 实现 FlashAttention2 → 分布式训练 | 性能分析 + CUDA/Triton 内核 |
| **A3: Scaling** | 拟合 Scaling Law，预测最优模型规模 | 实验设计 + 数学建模 |
| **A4: Data** | 处理 Common Crawl → 过滤/去重 → 提升模型质量 | 数据工程全链路 |
| **A5: Alignment** | SFT + RL (RLVR) 训练数学推理，可选 DPO 安全对齐 | 对齐技术实战 |

## 中文通识读本特色

- 面向高中生也能读懂，但**不删减专业术语**
- 每章配有原创示意图辅助理解
- 中文本地化阅读体验，降低 CS336 原版门槛
- HTML 和 PDF 双格式，免费开源

## 学习建议

搭配使用：**中文读本通览概念 → 原版课程视频深入理解 → Assignment 动手实现**。

| 资源 | 用途 | 难度 |
|------|------|------|
| 中文通识读本（feigaobox10） | 通览全局，建立概念框架 | 高中水平 |
| YouTube 课程视频 | 深入原理解析 | 本科生/研究生 |
| Stanford 课程作业 (GitHub) | 动手实现从 Tokenizer 到 Alignment 全流程 | 高阶（PyTorch/Triton） |

## 与现有资源关联

- [Build a LLM (From Scratch)](llms-from-scratch.md) — Sebastian Raschka 英文版从零构建 LLM，互补学习
- [LLM 算法与工程学习路线](llm-algorithm-engineering-roadmap.md) — 更工程化/实战导向的路线图

_Last updated: 2026-06-28_

