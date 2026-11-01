---
source: https://github.com/datawhalechina/diy-llm
date: 2026-10-30
tags: [cs336, llm, from-scratch, datawhale, chinese, tokenizer, moe, cuda, kernel, distributed-training, inference, alignment, grpo, course]
links:
  - https://github.com/datawhalechina/diy-llm
  - https://datawhalechina.github.io/diy-llm/
  - https://github.com/datawhalechina/diy-llm/releases/latest
---

# Diy-LLM（Datawhale）

> 斯坦福 **CS336 (Spring 2026)** 的中文本土化实现课程，2302★。自我定位不是"汉化版"，而是"**LLM 炼丹工坊**"——16 章硬核理论 + **6 个渐进代码作业**，代码驱动、每行实现都讲思考过程；额外做了国内环境适配（Qwen/DeepSeek 案例、算力现实）。中文文档为默认，另有 `docs/en/` 英文版与 PDF 讲义。

## 16 章结构

| 章 | 关键内容 | 配套作业 |
|----|----------|----------|
| 1 | 工具使用：W&B 实验追踪、超参搜索、可视化面板 | — |
| 2 | 分词器：BPE 原理、Unicode 规范化、**手写 tokenizer 训练代码** | 作业 1 |
| 3 | PyTorch 与资源核算：混合精度、梯度累积、FLOPs/显存估算 | — |
| 4 | LM 架构与训练细节：RoPE、RMSNorm、SwiGLU、AdamW、Pre/Post-Norm、学习率调度 | 作业 1 |
| 5 | 混合专家模型：Top-K 路由、负载均衡、辅助损失、Expert Parallelism、DeepSeekMoE | — |
| 6 | GPU 与优化：显存带宽/计算强度、Flash Attention、Kernel Fusion、BF16/TF32 | 作业 2 |
| 7 | GPU 高性能编程：CUDA 编程模型、Tensor Cores、Shared Memory、**Triton 入门** | 作业 2 |
| 8 | 分布式训练：DP/MP/PP、ZeRO-1/2/3、FSDP、All-Reduce | 作业 2 |
| 9 | Scaling Laws：Chinchilla 定律、计算最优配置、外推 | 作业 3 |
| 10 | 推理：KV Cache、投机解码、量化（GPTQ/AWQ）、PagedAttention、Continuous Batching | 作业 6 |
| 11 | 数据工程：质量过滤、MinHash 去重、PII 脱敏、数据配比、Data Curriculum | 作业 4 |
| 12 | 评估与基准：MMLU、HumanEval、HELM、CEval、AlpacaEval、Arena 排名 | 作业 6 |
| 13 | 训练流程：Pre-training、SFT、DPO、RLHF PPO、Alignment Tax | 作业 5 |
| 14 | 可验证奖励的 RL：GRPO、Rule-based Verifier、Outcome/Process Reward、RLVR 与 R1 方案 | 作业 5 |
| 15 | 多模态：CLIP/SigLIP → LLaVA → Qwen-VL → Chameleon 到 Omni Model | — |
| 16 | 扩展内容：LLM 推理与未来（更新中） | — |

## 6 个渐进作业

| 作业 | 主题 |
|------|------|
| assignment1-basics | 手搓大模型（tokenizer + 架构 + 训练） |
| assignment2-systems | 系统优化（GPU 优化 + 分布式训练） |
| assignment3-scaling | 扩展定律实验 |
| assignment4-data | 预训练数据处理 |
| assignment5-alignment | 对齐（SFT/DPO/RLHF/GRPO） |
| assignment6-evaluation | 评估与推理优化 |

## 与库内「CS336 中文读本」的分工

库里已有 `cs336-language-modeling-from-scratch.md`（高飞的电子替身改编），两者是**同一门课的两条路线**：

| 维度 | 已有：CS336 中文读本 | 本条目：Diy-LLM |
|------|---------------------|-----------------|
| 出品 | 个人改编 | **Datawhale 团队**（徐虎/李盛康/黎又榛等，含审核流程） |
| 定位 | 面向高中生的**通识读本**（降门槛、阅读向） | 面向能写 PyTorch 者的**工程实现课**（代码驱动） |
| 作业 | 无 | **6 个渐进作业**（含手写 tokenizer、CUDA/Triton、ZeRO/FSDP） |
| 章节 | 17 讲通识化改写 | 16 章 + 作业，覆盖更细（MoE/分布式/数据工程/RLVR） |
| 适合场景 | 先建立全景认知 | 之后动手真做一遍 |

**建议路径**：先读读本建立地图 → 再用 Diy-LLM 动手（尤其作业 1/2，直接对应 CUDA + 分布式训练主线）。

## 前置要求与注意

- 前置：熟练 Python、PyTorch、线代/概率/微积分（CUDA 基础可选，课内有入门）
- 无 GPU 也能学理论，完整训练需 GPU（建议云平台）
- ⚠️ 仓库体积约 **200MB**（含 PDF/图片），`git clone` 慢；只要文档可加 `--depth 1`
- License：README 声明 **CC BY-NC-SA 4.0**（GitHub SPDX 未自动识别，引用前以 README/LICENSE 原文为准）
- 在线阅读：https://datawhalechina.github.io/diy-llm/ ；PDF 讲义在 Releases

_Last updated: 2026-10-30_