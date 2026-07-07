---
source: https://zhuanlan.zhihu.com/p/654910335
date: 2026-07-07
tags: [llm, distributed-training, inference, rlhf, diffusion, multimodal, transformer, blog-index, chinese]
---

# 猛猿大模型技术文章导航（历史文章总索引）

> 知乎答主「猛猿」的图文并茂（图解）大模型技术文章合集总目录。覆盖训练并行、微调、RLHF、推理加速、扩散模型、多模态、Transformer 系列，质量高、图示清晰，是中文社区最系统的 LLM 工程/原理学习素材之一。

## 基本信息

| 项目 | 详情 |
|------|------|
| **作者** | 猛猿（知乎专栏「前面de算法」） |
| **类型** | 技术博客文章索引（持续更新） |
| **特点** | 图解为主，原理 + 源码解读双线，适合工程向深度学习 |
| **编辑时间** | 2026-01-15（仍在更新） |
| **总入口** | https://zhuanlan.zhihu.com/p/654910335 |

## 核心要点（摘要）

这是一份**导航型索引**，本身不是单篇教程，而是把作者全部历史文章按系列归类，方便系统性地按顺序阅读。对想构建「从训练到推理」完整 LLM 知识体系的读者尤其有用——每个系列都从原理讲起，再落地到源码（Megatron / DeepSpeed / vLLM 等）。

## 系列目录

### 大模型训练系列（并行 / ZeRO / Megatron / MoE / 序列并行）

- [图解流水线并行（Pipeline Parallelism, Gpipe)](https://zhuanlan.zhihu.com/p/613196255)
- [图解数据并行上篇（DP, DDP 与 ZeRO）](https://zhuanlan.zhihu.com/p/617133971)
- [图解数据并行下篇（ZeRO，零冗余优化）](https://zhuanlan.zhihu.com/p/618865052)
- [图解张量模型并行（Megatron-LM）](https://zhuanlan.zhihu.com/p/622212228)
- [Megatron 源码解读 1：分布式环境初始化](https://zhuanlan.zhihu.com/p/629121480)
- [Megatron 源码解读 2：模型并行](https://zhuanlan.zhihu.com/p/634377071)
- [Megatron 源码解读 3：分布式混合精度训练](https://zhuanlan.zhihu.com/p/662700424)
- [DeepSpeed-Megatron MoE 并行训练（原理篇）](https://zhuanlan.zhihu.com/p/681154742)
- [DeepSpeed-Megatron MoE 并行训练（源码解读篇）](https://zhuanlan.zhihu.com/p/681692152)
- [序列并行 1：Megatron SP](https://zhuanlan.zhihu.com/p/4083427292)
- [序列并行 2：DeepSpeed Ulysses](https://zhuanlan.zhihu.com/p/4496065391)
- [序列并行 3：Ring Attention](https://zhuanlan.zhihu.com/p/4963530231)
- [序列并行 4：Megatron Context Parallel](https://zhuanlan.zhihu.com/p/5502876106)
- [图解 Megatron TP 中的计算通信 overlap](https://zhuanlan.zhihu.com/p/16594218518)
- [探索一个关于 DeepSpeed ZeRO3 的认知误区](https://zhuanlan.zhihu.com/p/20115278338)

### 大模型微调系列

- [图解 LoRA（原理篇）](https://zhuanlan.zhihu.com/p/646831196)
- [图解 LoRA（源码解读与实操篇）](https://zhuanlan.zhihu.com/p/654897296)
- [AdaLoRA：能做"财务"预算的低秩适配器](https://zhuanlan.zhihu.com/p/657130029)

### RLHF 系列

- [人人都能看懂的 PPO 原理与源码解读](https://zhuanlan.zhihu.com/p/677607581)
- [人人都能看懂的 RLHF-PPO 理论知识](https://zhuanlan.zhihu.com/p/7461863937)
- [图解 OpenRLHF 中基于 Ray 的分布式训练流程](https://zhuanlan.zhihu.com/p/12871616401)
- [人人都能看懂的 DPO 数学原理](https://zhuanlan.zhihu.com/p/721073733)
- [OpenAI o1 技术初探 1：整体框架，Test-Time Scaling Law](https://zhuanlan.zhihu.com/p/773907223)
- [OpenAI o1 技术初探 2：使用 MCTS 增强推理能力](https://zhuanlan.zhihu.com/p/864190605)
- [OpenAI o1 技术初探 3：让模型拥有自我纠错能力](https://zhuanlan.zhihu.com/p/905620136)
- [记录对 DeepSeek-R1 的一些理解](https://zhuanlan.zhihu.com/p/19843230707)
- [强化学习解析一：MDP 和有模型学习](https://zhuanlan.zhihu.com/p/607596944)

### 大模型推理 / 计算加速系列

- [FlashAttention V1：从硬件到计算逻辑](https://zhuanlan.zhihu.com/p/669926191)
- [Flash Attention V2：从原理到并行计算](https://zhuanlan.zhihu.com/p/691067658)
- [Mixtral 8×7B 推理优化原理与源码实现](https://zhuanlan.zhihu.com/p/691066049)
- [vLLM 核心技术 PagedAttention 原理](https://zhuanlan.zhihu.com/p/691038809)
- [vLLM 源码解析 1：整体架构](https://zhuanlan.zhihu.com/p/691045737)
- [vLLM 源码解析 2：调度器策略（Scheduler）](https://zhuanlan.zhihu.com/p/692540949)
- [vLLM 源码解析 3：块管理器 BlockManager（上篇）](https://zhuanlan.zhihu.com/p/700780161)
- [vLLM 源码解析 3：Prefix Caching（BlockManager 下篇）](https://zhuanlan.zhihu.com/p/707228704)
- [从啥也不会到 CUDA GEMM 优化](https://zhuanlan.zhihu.com/p/703256080)
- [分离式推理架构 1：从 DistServe 谈起](https://zhuanlan.zhihu.com/p/706761664)
- [分离式推理架构 2：chunked-prefills](https://zhuanlan.zhihu.com/p/710165390)
- [再读 MLA，还有多少细节是你不知道的](https://zhuanlan.zhihu.com/p/19585986234)
- [图解 vLLM V1 系列 1-7：整体流程 / Executor-Workers / KV Cache 初始化 / 加载权重 / 调度器 / KVCacheManager / AsyncLLM](https://zhuanlan.zhihu.com/p/1900126076279160869)

### 扩散模型系列

- [DDPM（模型架构篇）](https://zhuanlan.zhihu.com/p/637815071)
- [DDPM（数学原理篇）](https://zhuanlan.zhihu.com/p/650394311)
- [DDPM（源码解读篇）](https://zhuanlan.zhihu.com/p/655568910)

### CV 大模型与多模态系列

- [再读 ViT，还有多少细节是你不知道的](https://zhuanlan.zhihu.com/p/657666107)
- [关于 CLIP，还有哪些细节是你不知道的](https://zhuanlan.zhihu.com/p/660476765)
- [再读 GAN：博弈理论下的一个实例](https://zhuanlan.zhihu.com/p/663253709)
- [再读 Swin Transformer](https://zhuanlan.zhihu.com/p/663747861)
- [再读 Deformable DETR](https://zhuanlan.zhihu.com/p/700776674)
- [万字长文图解 Qwen2.5-VL 实现细节](https://zhuanlan.zhihu.com/p/1921289925552210138)

### ChatGPT 技术解析系列

- [训练框架 InstructGPT](https://zhuanlan.zhihu.com/p/605516116)
- [GPT1、GPT2 与 GPT3](https://zhuanlan.zhihu.com/p/609367098)
- [赋予 GPT 写代码能力的 Codex](https://zhuanlan.zhihu.com/p/611313567)

### Transformer 系列

- [Positional Encoding（位置编码）](https://zhuanlan.zhihu.com/p/454482273)
- [避开复数推导理解 RoPE](https://zhuanlan.zhihu.com/p/863378538)
- [Self-Attention（自注意力机制）](https://zhuanlan.zhihu.com/p/455399791)
- [为什么 Transformer 要用 LayerNorm](https://zhuanlan.zhihu.com/p/456863215)
- [ResNet（残差网络）](https://zhuanlan.zhihu.com/p/459065530)
- [BERT 学习笔记一：基于论文精读的模型详解](https://zhuanlan.zhihu.com/p/461267517)

### 其他（大数据 / Git）

- [Hadoop 学习笔记：图解 HDFS 文件系统](https://zhuanlan.zhihu.com/p/459921566)
- [如何理解 git 的快照](https://www.zhihu.com/question/27680108/answer/2300327037)
- [git rebase 和 merge 的具体分别](https://www.zhihu.com/question/26492099/answer/2300416608)

## 与现有资源关联

- [大模型推理系统入门](llm-inference-system-intro.md) — 宏观推理优化视角，本文索引中的 vLLM / PagedAttention / FlashAttention 系列是其原理溯源
- [AI Infra 其实没有多少新东西](ai-infra-nothing-new.md) — 训练/推理 Infra 全局视角，与本文的并行训练、分离式推理系列互补
- [Modern GPU Programming For MLSys](mlc-modern-gpu-programming.md) — 本文「CUDA GEMM 优化」「FlashAttention」系列的底层硬件延伸
- [LLM 算法与工程学习路线](llm-algorithm-engineering-roadmap.md) — 本文索引可作为该路线的「图解版配套阅读材料」

## 个人备注

猛猿的图解系列是中文社区质量 top 级的 LLM 原理/工程素材，尤其适合作为：
1. **分布式训练**系统学习的图解入口（DP/DDP/ZeRO → TP/PP → SP/MoE）；
2. **推理加速**源码级溯源（vLLM 全系列、FlashAttention、分离式架构）；
3. **RLHF/o1/DeepSeek-R1** 对齐与推理时扩展的直觉建立。

与毕设 GEMM/Attention Kernel 优化方向、以及 AI Infra 到 IC 交叉方向高度相关。计划按「训练 → 推理 → RLHF」顺序精读，作为现有英文教材（CS336、JAX Scaling Book）的中文图解补充。

_Last updated: 2026-07-07_
