---
title: AIPerf (NVIDIA)
short: AIPerf
summary: GenAI-Perf 官方继任者，底层重写：多进程负载生成 + 15+ 端点 + 泊松/伽马流量 + TTFT/ITL 分位数
source: https://github.com/ai-dynamo/aiperf
date: 2026-11-14
tags: [inference, benchmarking, llm, serving, gpu, tool, vllm, sglang, telemetry, open-source]
---
# AIPerf — NVIDIA 官方 LLM 推理压测工具

> **NVIDIA 指定的 GenAI-Perf 继任者**，官方措辞是 "designated successor ... and a **ground-up rewrite**"
> （[官方技术博客](https://developer.nvidia.com/blog/benchmarking-llm-inference-at-scale-with-aiperf/)，
> 2026-09-18）。仓库 [ai-dynamo/aiperf](https://github.com/ai-dynamo/aiperf) 属 NVIDIA Dynamo 生态，
> **Apache-2.0**，Python 实现，878★ / 266 forks（2026-11-14 核验），当天仍有 push。
> 最新稳定版 **v0.13.0**（GitHub Release 2026-09-24，PyPI `aiperf` 0.13.0，文档 Latest 同为 v0.13.0）。

⚠️ 时间线要说清：仓库 2025-04 就已创建并持续迭代，**2026-09-18 是官方博客正式宣布"接班"的日子**，
不是项目首发。另外 "ground-up rewrite" 指的是**架构层重写**（不再套 Perf Analyzer、单进程改多进程），
不是换语言重写——AIPerf 仍然是 Python，只是绕开了 GIL 的单进程上限。

## 为什么必须重写：压测客户端自己先成了瓶颈

高并下发压时，单进程负载发生器（curl 循环、手写 asyncio 脚本、GenAI-Perf）会先被 Python GIL
卡住，测出来的是**客户端的上限**而不是服务端的容量。

| 维度 | GenAI-Perf（旧） | AIPerf（新） |
|------|------------------|--------------|
| 底座 | 构建在 **Perf Analyzer** 之上（旧栈的封装） | **完全脱离 Perf Analyzer**，独立实现 |
| 并发模型 | 单进程，高并发下 GIL-bound | **多进程**：worker 进程发负载，独立 record-processor 服务处理结果 |
| 组件通信 | — | **ZMQ**，README 称 10 个服务相互通信 |
| 架构分层 | — | 官方架构文档的三平面：**Control**（SystemController / Timing / Dataset / Worker Manager）、**Data**（Workers + 推理服务）、**Analytic**（Record Processors / Records / GPU Telemetry / Server Metrics） |
| 结果可靠性 | 并发升高时读数可能失真 | 客户端不再先饱和，能真正把服务端压满 |

请求生命周期：Dataset Manager 载入数据（内存映射供 worker 直读）→ Timing Manager 用 credit 机制
按选定模式排程 → 可选 warmup 预热 JIT/缓存 → Workers 发请求并采集时间戳 → Record Processor 并行算指标
→ Records Manager 汇总导出。

## 能力清单

| 类别 | 内容 |
|------|------|
| 端点 | 官方博客口径 **15+ 种**：chat、responses、NIM rankings、图像生成等；README 的 Supported APIs 另列 OpenAI chat/completions/embeddings/audio/images 与 NIM embeddings/rankings |
| 负载塑形 | **constant / Poisson / gamma** 到达模式、可调突发度、并发与请求速率渐进 ramp、可变 ISL/OSL 合成分布（含 vLLM/SGLang range-ratio） |
| 压测模式 | concurrency、request-rate、request-rate + max concurrency、**trace replay**（确定性回放生产流量） |
| 数据 | 合成数据、ShareGPT 等公开数据集；trace 格式支持 Mooncake、Baseten、WEKA (AgentX)、Bailian、BurstGPT、SageMaker Data Capture、Weka、TraceLab 等（来源：官方博客 + 仓库 tutorials 清单） |
| 核心指标 | **TTFT / ITL / Request Latency / Output Token Throughput**，均给 p25–p99 分位 + min/max/avg/std |
| 硬件遥测 | 有 DCGM exporter 或本机 pynvml 时，同次运行附带 GPU 功耗、利用率、显存占用 |
| 高级能力 | Goodput（SLA 合规率）、时间切片分析、KV Cache 效率、用户视角计时、请求取消测试、参数扫描 sweep / 自适应搜索与扩展、Pareto 曲线、Prometheus 服务端指标、Kubernetes operator/CRD |
| 输出 | 实时 TUI dashboard（另有 simple / headless 共 3 种 UI）、控制台指标表、**CSV + JSON** 全量结果、自动绘图 |
| 集成 | 可选 extras：`tdigest` / `mlflow` / `otel` / `wandb` |

## 5 分钟上手（官方博客的基线流程）

```bash
# 安装：Python >=3.11,<3.14
pip install aiperf          # 或 uv tool install aiperf

# 1) 起一个 vLLM 服务（示例模型 Qwen3-0.6B）
docker run --gpus all -p 8000:8000 vllm/vllm-openai:latest \
  --model Qwen/Qwen3-0.6B --host 0.0.0.0 --port 8000

# 2) 静态基线：把 ISL/OSL 钉死在 128/128
aiperf profile \
  --model Qwen/Qwen3-0.6B --endpoint-type chat --streaming --url localhost:8000 \
  --synthetic-input-tokens-mean 128 --synthetic-input-tokens-stddev 0 \
  --output-tokens-mean 128 --output-tokens-stddev 0 \
  --extra-inputs min_tokens:128 --extra-inputs ignore_eos:true

# 3) 换成真实感的泊松流量（平均 10 req/s，长度带方差，可复现）
aiperf profile \
  --model Qwen/Qwen3-0.6B --endpoint-type chat --streaming --url localhost:8000 \
  --request-rate 10 --arrival-pattern poisson \
  --synthetic-input-tokens-mean 512 --synthetic-input-tokens-stddev 128 \
  --output-tokens-mean 128 --output-tokens-stddev 32 \
  --random-seed 42 --request-count 200
```

三个最容易踩的坑（官方特意点名）：

1. **`--streaming` 不是可选项**——不开流式，服务端会攒完整响应再返回，根本没有 first-token / decode-token 事件，TTFT 和 ITL 无从测起。
2. **`min_tokens` + `ignore_eos` 决定结果能否复现**——否则 "128 output tokens" 只是建议值，模型自然结束时输出变短，吞吐被低估且各次运行不可比。
3. **`--random-seed` 保证泊松到达与长度抽样可复现**，改配置前后对比才有意义。

更轻的起点：README 的 Quick Start 用 Ollama + `granite4:350m` 本地服务，10 条请求即可跑通，CPU 也能出数。

## 从 GenAI-Perf 迁移

官方[迁移指南](https://docs.nvidia.com/aiperf/getting-started/migrating-from-gen-ai-perf)的定位是
"**对目前已支持的功能**做 drop-in replacement"，多数参数直接对应，但下面几处必须改：

| GenAI-Perf | AIPerf | 说明 |
|------------|--------|------|
| `--max-threads N` | `--workers-max N` | 由全局线程数改为直接控制发请求的 worker 数 |
| `-- ...`（透传） | 删掉 | 所有参数都是原生支持，不再需要 passthrough |
| `--server-metrics-url http://node:9400` | **`--gpu-telemetry`** | ⚠️ 旧参数名骗人：它指向 Triton/DCGM 遥测端口，**不是** Prometheus 推理服务指标。AIPerf 把两者拆开：`--gpu-telemetry`（DCGM exporter 或 `pynvml`）与 `--server-metrics`（模型端点 `/metrics`，默认开启） |
| `inputs.json` 的 `payload` | `payloads` | 复数；数组每项代表一轮对话，新增 `session_id` 便于请求关联 |
| `analyze` 子命令部分选项 | **尚未支持** | 官方标注 planned for future releases，迁移前先查 CLI 对比矩阵 |

**推理模型（Qwen3 / DeepSeek-R1 / gpt-oss 等）口径差异**：GenAI-Perf 忽略 `reasoning_content`，
TTFT 只算到首个非推理 token；AIPerf 把推理 token 也算进 TTFT，因此**新旧工具的数字不能直接比**。

| 想对比的量 | 用 AIPerf 的哪个指标 |
|------------|----------------------|
| GenAI-Perf TTFT | **AIPerf TTFO**（Time to First Output Token） |
| GenAI-Perf OSL | **AIPerf Output Token Count**（不含推理 token；AIPerf OSL 是含的） |

## 与库内资源的分工

| 资源 | 关系 |
|------|------|
| [zero-to-sglang](../3-Tutorials/zero-to-sglang.md) | 其 Part I 第 5 章讲 TTFT/TPOT/ITL/Goodput 与「如何设计并读懂一次 benchmark」；AIPerf 就是把这个章节落到实处的那把工具 |
| [大模型推理系统入门](../3-Tutorials/llm-inference-system-intro.md) | 概念地图（PagedAttention / Continuous Batching / 投机解码）；压测看到的现象要回到这里解释 |
| [LLM Inference Handbook](../1-Official-Docs/llm-inference-handbook.md) | 官方手册给指标定义与 GPU 架构背景 |
| [vLLM 中文文档](../1-Official-Docs/vllm-docs-zh.md) / [nano-vllm](nano-vllm.md) / [mini-sglang](mini-sglang.md) | 被压测的服务端与对照实现；改引擎配置后用同一份 AIPerf 命令做 A/B |
| [InferFlux](inferflux.md) | 同样围绕推理系统，但它是动画演示「机制长什么样」，AIPerf 是「真实跑出多少」 |

**建议顺序**：先读概念 → 用静态 ISL/OSL 基线建立可复现的测量闭环 → 换泊松/gamma 流量看 p99 尾延迟
→ 回放生产 trace → 再做配置 sweep 画 Pareto 曲线。读分位数（尤其 p99）而不是只看平均吞吐。

## 注意点

- Python **>=3.11, <3.14**；Linux aarch64 上可选依赖 `crick` 只有 sdist，需要 C 工具链（`build-essential` / `Development Tools`）；普通 `pip install aiperf` 不会拉它
- 版本迭代很快（0.7 → 0.13，2026 年内多个 release），CLI 以[当前版本文档](https://docs.nvidia.com/aiperf/latest/)为准，别照抄旧博客命令
- 它对 OpenAI 兼容端点友好；非兼容协议要看插件/端点类型支持情况
- GPU telemetry 依赖 DCGM exporter 或 pynvml；**Jetson / Thor 集成 GPU 上 DCGM 是否可用，待核实**，边缘部署需实测

## 个人备注

库里此前收的都是「推理系统的原理、实现与可视化」，一直缺一个能把服务端真正压满、并把
TTFT/ITL 分位数与 GPU 遥测落到 CSV/JSON 的测量端工具。AIPerf 补的是这条链路。后续若要对
本地或边缘侧部署做容量评估，可以直接复用上面两条命令（静态基线 + 泊松流量）；但要留意
DCGM/pynvml 在 Jetson 类设备上的可用性，别默认遥测一定能拿到——这项还没核实。

_Last updated: 2026-11-14_
