---
source: https://Abatom.github.io/inferflux/
date: 2026-08-01
tags: [inference, visualization, llm, interactive, simulation, sglang, vllm, threejs]
---

# InferFlux — 推理系统可视化

## 核心要点（摘要）

一套面向 **LLM 推理系统** 的交互式、单文件 Web 动画合集（作者 Abatom，CC BY-NC 4.0）。每个页面零依赖、自包含，拖动参数即可实时观察系统行为。对理解 PD 分离、吞吐/KV 容量可行性、Transformer 推理执行序、GPU 集合通信极有帮助。

## 详细内容

- **定位**：把抽象的 LLM 推理系统（调度、并行、带宽墙）变成可拖拽、可旋转的可视化交互
- **技术栈**：原生 HTML/CSS/JS（零框架）；3D 部分用 Three.js；仓库附带一个 Python HTTPS server 供本地安全上下文访问
- **许可**：CC BY-NC 4.0（署名-非商业，商业用途需作者授权）
- **在线访问**：https://Abatom.github.io/inferflux/ ；源码：https://github.com/Abatom/inferflux

### 页面清单

- `index.html` — 首页，各页入口
- `pd-disagg.html` — **PD 分离模拟器**：忠实还原 SGLang 的 PD 分离请求生命周期，实时联动 TTFT / TPOT / 吞吐 / 排队 / KV 利用率（含 chunked prefill、KV transfer、handshake gating）
- `calc-input.html` — **输入吞吐计算器**：由模型/GPU/TP/DP/EP/输入长度/缓存命中率推算 prefill 吞吐与 KV 内存可行性，按实测数据反解 MFU（Roofline 视角）
- `calc-output.html` — **输出吞吐计算器**：推算 decode 输出吞吐与 TPOT，展示 weight/KV 带宽 roofline 拐点，反解 MBU
- `transformer-3d.html` — **请求生命周期 3D**：依真实执行顺序复现 SGLang `eagle_worker` 全流程（Prefill 全前向→首 token→draft 预热；Decode 草稿提议→目标层并行校验→accept+bonus），展开 attention(MHA/GQA/MQA)+MLP/MoE(top-k+shared expert)+TP/EP/DP 并行；投机为 DFLASH 或 MTP
- `collective-3d.html` — **GPU 集合通信 3D**：逐帧走查 AllReduce(Ring=ReduceScatter+AllGather)/AllGather/ReduceScatter/Broadcast/All-to-All，按源 GPU 着色，可切换 2/4/8 卡
- `attention-3d.html` — Attention 机制 3D 可视化

## 个人备注

推理系统层的"直觉建立器"：比读文字更快建立对 PD 分离、带宽墙、并行维度的体感。建议路线——先 `calc-input/output` 建立吞吐/KV 容量直觉 → `pd-disagg` 看调度联动 → `transformer-3d` / `collective-3d` 把执行序与通信拓扑钉进脑图。与仓库内 nano-vllm / mini-sglang（推理框架层源码）互补：一个看"为什么这么设计"，一个看"系统跑起来长什么样"。

_Last updated: 2026-08-01_
