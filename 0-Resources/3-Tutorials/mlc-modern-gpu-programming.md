---
source: https://mlc.ai/modern-gpu-programming-for-mlsys/
date: 2026-06-25
tags: [gpu, cuda, blackwell, gemm, flash-attention, tirx, kernel-optimization, ml-systems, tma, warp-specialization]
---

# Modern GPU Programming For MLSys

> MLC.ai 出品，基于 Blackwell 架构的现代 GPU Kernel 编程实战教材，源自 CMU MLSys 课程。

## 基本信息

| 项目 | 详情 |
|------|------|
| **作者** | MLC.ai (Tianqi Chen 团队) |
| **来源** | CMU Machine Learning Systems 课程系列 |
| **编程模型** | TIRx Python DSL（贴近硬件的底层编程接口） |
| **目标架构** | NVIDIA Blackwell (B200/B100) |
| **核心案例** | GEMM 优化 + FlashAttention 4 |

## 核心要点（摘要）

本书的核心命题：现代 GPU 不再是简单设计的变体——Blackwell 引入更丰富的内存空间、新的访存模式和更专用的执行单元。要写出高性能 Kernel，需要「硬件心智模型」+「实战构建能力」二者兼备。

全书按 **硬件理解 → 编程模型 → State-of-the-Art Kernel 构建** 的递进路径展开，覆盖 TMA 流水线、Persistent Scheduling、Warp Specialization、2-CTA Cluster 等前沿技术。

## 目录结构

### Part I: Understanding the GPU
GPU 整体组织、编写快速 Kernel 的通用方法、数据布局、异步内存操作与协调机制。

### Part II: TIRx Overview
TIRx 语言关键元素，后续所有代码示例的基础。

### Part III: GEMM — Tiled to SOTA
从分块 GEMM 出发，逐步引入 TMA Pipelining → Persistent Scheduling → Warp Specialization → 2-CTA Clusters，完整构建 SOTA 矩阵乘法 Kernel。

### Part IV: Flash Attention 4
基于 Part III 技术栈构建完整 Attention Kernel：双 MMA + Softmax、Online-Softmax Rescaling、Causal Masking、GQA 支持。

### Reference
TIRx 语言参考与编译器内部实现。

## 关键技术点

| 技术 | 说明 | 阶段 |
|------|------|------|
| **TMA (Tensor Memory Accelerator)** | Blackwell 硬件异步数据搬运单元 | GEMM Part III |
| **Persistent Scheduling** | 避免 Kernel 重启动开销的持久化线程调度 | GEMM Part III |
| **Warp Specialization** | 生产者-消费者分离的 Warp 角色分工 | GEMM Part III |
| **2-CTA Clusters** | 两个 CTA 协作共享 SMEM | GEMM Part III |
| **Online-Softmax Rescaling** | 流式 softmax 避免全局归约 | Flash Attention IV |
| **Causal Masking + GQA** | 生产级 Attention 必备特性 | Flash Attention IV |

## 与现有资源关联

- [CUDA Programming Guide](../1-Official-Docs/cuda-programming-guide.md) — GPU 编程基础，本课程的前置知识
- [AI Infra 其实没有多少新东西](ai-infra-nothing-new.md) — AI Infra 全局视角，GPU 算子是其中关键一环
- [大模型推理系统入门](llm-inference-system-intro.md) — 推理系统宏观视角，与本书的 Kernel 级优化互补
- [Infinitensor 夏立营 2025](infinitensor-winter-camp-2025.md) — 覆盖推理 Infra 的算子层实战

## 个人备注

与现有 GPU 学习资源（CUDA Programming Guide、Infinitensor 训练营）的互补关系：CUDA Guide 是通用编程基础，本书聚焦 Blackwell 特定架构特性和 Kernel 级极致优化，且使用 TIRx DSL 提供可运行的渐进式代码。对毕设 GEMM/Attention Kernel 优化方向直接相关，计划系统学习。

_Last updated: 2026-06-25_
