---
source: https://docs.nvidia.com/cuda/cuda-programming-guide/
date: 2026-04-03
tags: [cuda, nvidia, gpu, parallel-computing, hardware-acceleration]
---

# CUDA Programming Guide

## 核心要点（摘要）

NVIDIA 官方 CUDA 编程模型权威文档。AI 框架底层依赖 GPU 并行计算，理解 CUDA 编程模型有助于深入优化模型推理和训练性能。

## 主要内容

- **CUDA C++ 编程接口** — GPU kernel 编写范式
- **线程层次** — thread/block/grid 的组织结构
- **内存层次** — global/shared/local/constant/texture memory
- **执行模型** — stream、并发 kernel、同步机制
- **硬件映射** — SM、warp execution、occupancy

## 个人备注

理解 GPU 底层执行模型，对 CUDA kernel 优化、vLLM/TensorRT 推理部署调优有指导意义。

_Last updated: 2026-04-03_
