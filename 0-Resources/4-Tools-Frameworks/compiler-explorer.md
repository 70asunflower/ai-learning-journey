---
source: https://godbolt.org/
date: 2026-10-18
tags: [compiler, assembly, llvm-ir, optimization, simd, cpp, rust, cuda, interactive-tool, performance]
links:
  - https://godbolt.org/
  - https://github.com/compiler-explorer/compiler-explorer
  - https://quick-bench.com/
  - https://cppinsights.io/
---

# Compiler Explorer（Godbolt）

> 在线编译器探索工具（Matt Godbolt 创建，开源：`compiler-explorer/compiler-explorer`）。**左侧写代码，右侧实时看编译产物**——汇编、LLVM IR、AST、优化管线、控制流图，支持几十种语言与 GCC/Clang/MSVC 等主流编译器的众多版本，并可**多编译器并行对比**。性能优化与底层原理学习的日常工具。

## 核心功能

- **实时编译 + 汇编输出**：改一行代码立刻看到汇编变化；Intel / AT&T 语法一键切换，可反修饰（demangle）符号
- **多编译器并行对比**：同一段代码挂多个编译器/版本（如 gcc 16.2 vs clang）并排看输出差异
- **中间表示全覆盖**：不止汇编——AST、LLVM IR、Clang IR、Opt Pipeline（优化管线）、Opt Remarks（优化建议）、Stack Usage、Control Flow Graph、Rust MIR/HIR、GHC Core 等
- **执行模式**：可直接运行代码看结果（Execution Only 模式）
- **设备编译**：CUDA 设备代码查看（Device 视图），对 GPU 算子学习直接有用
- **Conformance View**：标准一致性测试

## 姊妹工具（同作者生态）

| 工具 | 用途 |
|------|------|
| [Quick-bench](https://quick-bench.com/) | 微基准测试：A/B 两种实现直接比耗时 |
| [CppInsights](https://cppinsights.io/) | 看编译器如何看待你的 C++（模板实例化/隐式转换展开） |
| [ABI Explorer](https://abiexplorer.org/) | ABI/结构体布局可视化 |

## 典型使用场景（AI Infra 向）

- **验证向量化**：写个简单 loop，看 `-O2/-O3` 下有没有生成 AVX/NEON 指令——没向量化就回去改写法
- **算子优化前哨**：手写 SIMD/内联汇编前，先在 Godbolt 上验证编译器自动向量化的效果
- **对比编译器代码质量**：同一 kernel 在 gcc/clang 下哪家汇编更优
- **跨架构对比**：x86-64 / ARM / RISC-V 目标的汇编差异（选型/移植时心里有数）
- **理解 C++ 底层**：虚函数调用、模板实例化、`std::vector` 边界检查的开销，全都能在汇编里看见

## 注意

- 站点带 **Claude Explain** 功能（AI 解释汇编），会把源码+编译输出发给 Anthropic——在意隐私的代码别用；仓库对含 `no-ai` 字符串的源码会自动禁用 AI 处理（这个设计值得称赞）

_Last updated: 2026-10-18_