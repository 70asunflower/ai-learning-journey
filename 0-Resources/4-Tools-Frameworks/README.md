# Tools & Frameworks

Commonly used tools, frameworks, and libraries.

## Current Stack

<!-- BUILD:TABLE:START -->
| Resource | Description | Date |
| :--- | :--- | :--- |
| [ModelScope Notebook 免费试用](modelscope-notebook.md) | 魔搭云上开发环境，开箱即用 GPU/CPU，提供免费使用时长 | 2026-03-31 |
| [ms-swift 微调部署框架](ms-swift.md) | 魔搭社区大模型与多模态模型全链路框架，覆盖训练→推理→评测→量化→部署 | 2026-03-31 |
| [TikTokenizer 可视化交互工具](tiktokenizer.md) | 可视化学习 LLM Tokenizer 工作原理的交互工具 (GPT2/CL100K 等编码器) | 2026-04-02 |
| [LlamaFactory 微调框架](llamafactory.md) | 100+ LLM/VLM 高效微调框架，支持 LoRA/QLoRA/SFT/DPO | 2026-04-04 |
| [CanIRun.ai 硬件兼容性检测](canirun.md) | 检测本地 GPU/VRAM/RAM 能跑哪些本地大模型，支持 llama.cpp/Ollama/LM Studio 数据源 | 2026-04-09 |
| [GPT Image 2 提示词合集](gpt-image-2-prompts.md) | 725+ 精选提示词，JSON 结构化+参数化模板（产品海报/信息图/UI设计/动漫插画） | 2026-04-22 |
| [mini-sglang](mini-sglang.md) | 极简 SGLang 实现，学习推理框架另一技术路线（RadixAttention/前缀缓存） | 2026-04-25 |
| [nano-vllm](nano-vllm.md) | 极简 vLLM 实现，学习推理框架核心原理（PagedAttention/Continuous Batching） | 2026-04-25 |
| [Open Design](open-design.md) | Claude Design 开源替代，AI 驱动 artifact-first 设计工具（13 CLI/31 Skills/129 设计系统） | 2026-05-05 |
| [InferFlux 推理系统可视化](inferflux.md) | 零依赖交互式动画：PD分离模拟/吞吐计算/3D请求生命周期/GPU集合通信（Three.js） | 2026-08-01 |
| [LLM Visualization (bbycroft)](llm-viz.md) | GPT 风格 LLM 推理 3D 交互可视化，逐层看注意力/FFN/词元流动（WebGL） | 2026-08-01 |
| [Compiler Explorer (Godbolt)](compiler-explorer.md) | 在线编译器探索：实时汇编/LLVM IR/优化管线，多编译器对比，验证向量化 | 2026-10-18 |
<!-- BUILD:TABLE:END -->

---

## 其它常用工具（未收录详情页）

长期在用、但还没单独写详情页的，先记在这里：

| 工具 | 用途 | 链接 |
|------|------|------|
| vLLM | LLM 推理加速 | https://github.com/vllm-project/vllm |
| SGLang | 结构化生成 / 高吞吐推理 | https://github.com/sgl-project/sglang |
| Ollama | 本地运行大模型 | https://github.com/ollama/ollama |
| PyTorch | 深度学习框架 | https://pytorch.org |
| LangChain | LLM 应用开发 | https://github.com/langchain-ai/langchain |

_想给上面某个工具补详情页？按 `CONTRIBUTING.md` 建一个 `<name>.md`，重跑 `python scripts/build.py` 就会自动出现在上表里。_
