---
source: https://infra.seminars.lcpu.dev/
date: 2026-08-03
tags: [ai-infra, gpu, cuda, kernel, ml-compiler, tensor-core, distributed-training, llm-inference, rl-systems, course]
---

# Infra Seminars 2026 — AI 基础设施 Seminar 系列

> 由 LCPU 社团骨干与超算队设计的 AI 基础设施系列课程，覆盖「大模型如何训更快、跑更好、推更省」。
> 官网: https://infra.seminars.lcpu.dev/ ｜ 课程日历: https://infra.seminars.lcpu.dev/schedule

## Overview

Infra Seminars 是一套面向工业界大规模模型训练与推理前沿的公开课，从 Kernel 到编译器、从分布式系统到集合通信、从模型推理到强化学习系统，力求揭示真实 AI Infra 的最底层逻辑。课程采取「主题分享 → 现场讨论 → Guest Lecture → 代码实践 → 资料开源」的闭环，讲义与作业统一开源、持续更新。

## 四个 Topic（课程体系）

### Topic 1 — Kernel & ML Compiler
从 GPU 体系结构与 CUDA 出发，沿 Layout、数据复用与流水线一路抵达高性能 GEMM、Attention 与 MoE Kernel，并理解 DSL / ML Compiler 如何简化开发与自动优化。
- 关键词：CUDA · Triton · TileLang · Tensor Core · Warp Specialization · Pipeline Ordering · ML Compiler

### Topic 2 — Interconnect & Communication
从互联网络与集合通信的视角理解大规模系统的真实效率瓶颈。
- 关键词：RDMA · NCCL · Scale-Up · Scale-Out · Network Fabric · Memory-Storage Co-design

### Topic 3 — LLM Serving & Inference
围绕 KV Cache、调度与并行策略，理解推理优化的目标，并实践真实推理在系统层面的优化。
- 关键词：KV Cache Centric Systems · Batching · PD 分离 · Spec Decode · vLLM

### Topic 4 — Distributed Reinforcement Learning Systems
当训练、推理、奖励与环境同时出现，如何系统性解决长尾、资源调度、权重同步、容错与训推一致性等问题。
- 关键词：PPO · veRL · Rollout · Agentic RL · 训推一致性 · 分布式 RL 系统

## 已公开的 Session 与资料（Topic 1）

| 日期 | Session | 内容 | 回放 / 资料 |
|------|---------|------|-------------|
| 2026-07-26 | Session 1.0/1.1/1.2 | 从 HPC 到 AI Infra（并行计算与并行编程）· CUDA 编程模型 · Triton/TileLang Tile Level 编程 | [1.0 回放](https://www.bilibili.com/video/BV1u83w6DEfG) · [1.1 回放](https://www.bilibili.com/video/BV1g83w6DETm) · [1.2 回放](https://www.bilibili.com/video/BV1Sb3w6nE8v) · [Topic 1 讲义](https://infra.seminars.lcpu.dev/wiki/VWJPwVFTHifeadkE4phc45hOntg) · [A01 作业](https://infra.seminars.lcpu.dev/assignments#assignment-A01) |
| 2026-07-30 | Session 2：Memory Abstraction & Hierarchy | CUDA Core FP32 GEMM 主线，data reuse 与 memory hierarchy，Roofline Model，SM/warp/coalescing/latency hiding/shared memory bank conflict/padding/swizzle/per-thread microtile，Nsight Compute 调优 | [2.1 回放](https://www.bilibili.com/video/BV1gqGA6ZEfg) · [2.2 回放](https://www.bilibili.com/video/BV1L8GA6YEAH) |
| 2026-08-01 | Workshop 1：Parallel Programming with TileLang | TileLang 语法、用 TileLang 写 Kernel、CTA→Thread 映射与 Layout Inference、Latency Hiding、DSL JIT 编译与 Host 侧、算子优化与工具 | [腾讯会议](https://meeting.tencent.com/dm/MWmIhQau1Yb0) · [B站直播](https://live.bilibili.com/22591408) · [LCPU Live](https://live.lcpu.dev/) |
| 2026-08-02 | Session 3：Tensor Core | mma.sync（Ampere）/ wgmma（Hopper）/ tcgen05（Blackwell）三代指令演进，fragment 布局，layout 与 swizzle 解决 bank conflict，FP8 fine-grained scaling | [腾讯会议](https://meeting.tencent.com/l/r9vIJMyflfD6) · [B站直播](https://live.bilibili.com/22591408) · [LCPU Live](https://live.lcpu.dev/) |

> 后续 Topic 2/3/4 的 Session 按官方日历陆续放出，资料开源更新中。

## 资源链接

- 官网首页: https://infra.seminars.lcpu.dev/
- 课程日历（全部安排 / 回放 / 作业）: https://infra.seminars.lcpu.dev/schedule
- 讲义 Wiki（Topic 1）: https://infra.seminars.lcpu.dev/wiki/VWJPwVFTHifeadkE4phc45hOntg
- 作业与评测: https://infra.seminars.lcpu.dev/assignments

## My Notes

- **定位**: 比单篇博客更系统、比整本书更贴近工业界一线，是补齐「AI Infra 工程直觉」的优质系列。
- **学习顺序**: 建议先吃透 Topic 1（Kernel & Compiler）——它是 Topic 2/3/4 的算力底座；再按 Topic 3（推理）→ Topic 2（通信）→ Topic 4（分布式 RL）的顺序推进。
- **与本站其他资源的衔接**: 可与 `Modern GPU Programming For MLSys`、`CS336`、`大模型推理系统入门`、`AI Infra 其实没有多少新东西` 对照阅读。

---

_Last updated: 2026-08-03_
