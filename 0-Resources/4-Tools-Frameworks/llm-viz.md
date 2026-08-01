---
source: https://bbycroft.net/llm
date: 2026-08-01
tags: [llm, transformer, visualization, attention, gpt2, interactive, threejs, interpretability]
---

# LLM Visualization (bbycroft)

## 核心要点（摘要）

Brendan Bycroft 制作的 **GPT 风格 LLM 推理 3D 交互可视化**：把网络前向传播的每一步（词元化、词嵌入、位置编码、单层注意力、前馈、残差/归一化、逐词元自回归解码）渲染成可旋转、可缩放、可逐步推进的 3D 模型，是理解 Transformer 内部机制最直观的方式之一。

## 详细内容

- **演示模型**：基于 Andrej Karpathy `minGPT` 的示例权重（一个对 A/B/C 三字排序的极小 GPT 网络）；渲染器也支持任意规模（含 gpt2 尺寸），但大模型权重需自行下载（数百 MB）
- **技术栈**：WebGL/Three.js 渲染 + TypeScript + Next.js/React（仓库 `bbycroft/llm-viz`）；纯前端，浏览器直接跑
- **覆盖流程**：Tokenization → Embedding → 位置编码 → 多头注意力（Q/K/V、softmax、加权求和）→ FFN → LayerNorm/残差 → 输出 logits → 自回归生成
- **价值**：把抽象的矩阵运算变成"看得见"的数据流，配合 Karpathy minGPT / nanoGPT 源码食用效果最佳
- **作者/源码**：Brendan Bycroft · https://github.com/bbycroft/llm-viz

## 个人备注

Transformer 内部结构"体感"建立器，与仓库内 nano-vllm / mini-sglang（推理框架层源码）互补：一个看"网络内部在算什么"，一个看"工业级推理怎么调度"。建议路线——先看本可视化建立注意力/FFN 直觉 → 再读 nanoGPT 源码 → 最后看 inferflux 把推理系统放大到 PD 分离/吞吐维度。

_Last updated: 2026-08-01_
