---
source: https://vllm.hyper.ai/docs/
date: 2026-07-07
tags: [vllm, inference, serving, llm, quantization, lora, documentation, chinese]
---

# vLLM 中文文档

## 核心要点（摘要）

vLLM 是快速、易用的 LLM 推理与服务库，最初由 UC Berkeley Sky Computing Lab 开发，现为社区驱动项目。本项目页面是 **vLLM 官方文档的中文翻译版**（英文原版位于 docs.vllm.ai），覆盖从安装到源码设计的完整链路，是中文环境下学习推理/服务框架最权威的参考资料。

核心能力：PagedAttention 显存管理、连续批处理（Continuous Batching）、CUDA/HIP Graph 快速执行、多种量化（GPTQ/AWQ/INT4/INT8/FP8）、推测性解码、分块预填充、张量/流水线并行、OpenAI 兼容 API 服务器、前缀缓存、多 LoRA。

## 主要内容（按文档分区）

- **快速开始** — [安装](https://vllm.hyper.ai/docs/getting-started/installation/) · [Quickstart](https://vllm.hyper.ai/docs/getting-started/quickstart) · [示例](https://vllm.hyper.ai/docs/getting-started/examples/offline-inference/) · [FAQ](https://vllm.hyper.ai/docs/getting-started/faq) · [V1 用户指南](https://vllm.hyper.ai/docs/getting-started/v1-user-guide)
- **支持模型** — [模型列表](https://vllm.hyper.ai/docs/models/supported_models) · [生成模型](https://vllm.hyper.ai/docs/models/generative_models) · [池化模型](https://vllm.hyper.ai/docs/models/Pooling%20Models)
- **功能特性** — [量化](https://vllm.hyper.ai/docs/features/quantization/) · [LoRA](https://vllm.hyper.ai/docs/features/lora) · [工具调用](https://vllm.hyper.ai/docs/features/tool_calling) · [结构化输出](https://vllm.hyper.ai/docs/features/structured_outputs) · [自动前缀缓存](https://vllm.hyper.ai/docs/features/automatic_prefix_caching) · [分离式预填充](https://vllm.hyper.ai/docs/features/disagg_prefill) · [推测解码](https://vllm.hyper.ai/docs/features/spec_decode)
- **训练** — [TRL 强化学习](https://vllm.hyper.ai/docs/training/trl) · [RLHF](https://vllm.hyper.ai/docs/training/rlhf)
- **推理与服务** — [离线推理](https://vllm.hyper.ai/docs/inference-and-serving/offline_inference) · [OpenAI 兼容服务器](https://vllm.hyper.ai/docs/inference-and-serving/openai_compatible_server) · [多模态输入](https://vllm.hyper.ai/docs/inference-and-serving/multimodal_inputs) · [分布式推理](https://vllm.hyper.ai/docs/inference-and-serving/distributed_serving_new) · [生产指标](https://vllm.hyper.ai/docs/inference-and-serving/metrics) · [引擎参数](https://vllm.hyper.ai/docs/inference-and-serving/engine_args)
- **部署** — [Docker](https://vllm.hyper.ai/docs/deployment/docker) · [Kubernetes](https://vllm.hyper.ai/docs/deployment/k8s) · [Nginx](https://vllm.hyper.ai/docs/deployment/nginx)
- **性能** — [优化与调优](https://vllm.hyper.ai/docs/performance/optimization) · [基准测试](https://vllm.hyper.ai/docs/performance/benchmarks)
- **设计文档** — [架构概览](https://vllm.hyper.ai/docs/design/arch_overview) · [PagedAttention](https://vllm.hyper.ai/docs/design/paged_attention) · [插件系统](https://vllm.hyper.ai/docs/design/plugin_system) · [多模态处理](https://vllm.hyper.ai/docs/design/mm_processing)
- **V1 设计文档** — [torch.compile 集成](https://vllm.hyper.ai/docs/design-v1/torch_compile) · [前缀缓存](https://vllm.hyper.ai/docs/design-v1/prefix_caching)
- **开发者指南** — [贡献](https://vllm.hyper.ai/docs/contributing/overview) · [性能分析](https://vllm.hyper.ai/docs/contributing/profiling_index) · [添加新模型](https://vllm.hyper.ai/docs/contributing/model/)
- **API 参考** — [LLM 类](https://vllm.hyper.ai/docs/api/offline_interence/LLM) · [LLMEngine](https://vllm.hyper.ai/docs/api/engine/llm_engine) · [采样参数](https://vllm.hyper.ai/docs/api/inference_params)

## 个人备注

和仓库里 `nano-vllm`（极简实现，学原理）、`llm-inference-system-intro`（概念入门）形成三层递进：入门概念 → 极简代码 → **官方完整文档**（生产级参考）。实际做推理部署/调优时，以这份中文文档为准，比翻英文原版快很多。

英文原版入口：https://docs.vllm.ai/

_Last updated: 2026-07-07_
