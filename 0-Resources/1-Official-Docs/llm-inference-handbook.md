---
source: https://handbook.modular.com/
date: 2026-08-01
tags: [inference, handbook, modular, deployment, serving, gpu, optimization, reference]
---

# LLM Inference Handbook (Modular)

## 核心要点（摘要）

Modular 出品的 **LLM 推理技术手册**：把碎片化的 LLM 推理知识（散落在论文、厂商博客、GitHub issue、Discord）系统化整理成"术语表 + 指南 + 参考"三合一，覆盖从核心概念、性能指标到优化技术与生产部署的完整链路，并配套大量交互式计算器/模拟器/可视化。

## 详细内容

- **定位**：面向在自家基础设施上部署/扩缩/运维 LLM 的工程师（从微调小模型到大规模自建部署）
- **内容板块**：
  - LLM 推理基础：推理与训练差异、TTFT / TPOT / E2EL / goodput 等指标、上下文窗口
  - 推理优化：continuous batching、prefix caching、chunked prefill、PD 分离（prefill-decode disaggregation）、KV cache 卸载与量化
  - GPU 架构基础：线程 / warp / SM / 显存层级、kernel 优化
  - 部署模式：BYOC（自带云）、on-prem 私有化
- **交互工具（亮点）**：推理可视化器、生命周期可视化器、逐词元解码循环、延迟时间线、上下文窗口模拟器、延迟指标沙盒、Top-p vs Top-k 过滤、模型浏览器、GPU 对比表、GPU 显存计算器、量化显存影响可视化、批处理策略模拟器、chunked prefill 调度器、KV Cache 显存计算器、GPU 执行与显存映射
- **形式**：在线网页 + 每页可追加 `.md` 的 Markdown 版本（含 `llms.txt` 索引），持续更新
- **作者/源码**：Modular · https://github.com/modular/llm-inference-handbook

## 个人备注

推理部署层的"权威速查手册"，与仓库内 大模型推理系统入门、inferflux（交互可视化）互补：本手册偏系统化的概念/指标/优化参考，inferflux 偏单点交互演示。建议作为部署前/调优时的常备查阅源；其中的 goodput / PD 分离 / KV cache 计算器等可与 inferflux 计算器对照使用。

_Last updated: 2026-08-01_
