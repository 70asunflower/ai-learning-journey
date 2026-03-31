#!/usr/bin/env python3
"""
自动生成资源索引脚本
扫描 0-Resources/ 目录，生成索引文件
"""

import os
from pathlib import Path


def scan_directory(base_path: str) -> dict:
    """扫描目录，收集所有 markdown 文件"""
    resources = {
        "1-Official-Docs": [],
        "2-Papers": [],
        "3-Tutorials": [],
        "4-Tools-Frameworks": [],
        "5-Datasets": [],
    }

    base = Path(base_path)

    for category in resources.keys():
        category_path = base / category
        if category_path.exists():
            for md_file in sorted(category_path.glob("*.md")):
                if md_file.name != "README.md":
                    resources[category].append(md_file.name)

    return resources


def generate_index(resources: dict) -> str:
    """生成索引 markdown 内容"""
    content = """# 资源索引（自动生成）\n\n"""

    category_names = {
        "1-Official-Docs": "官方文档",
        "2-Papers": "论文",
        "3-Tutorials": "教程",
        "4-Tools-Frameworks": "工具框架",
        "5-Datasets": "数据集",
    }

    for category, files in resources.items():
        content += f"## {category_names.get(category, category)}\n\n"
        if files:
            for f in files:
                name = f.replace(".md", "")
                content += f"- [{name}]({category}/{f})\n"
        else:
            content += "_暂无内容_\n"
        content += "\n"

    return content


if __name__ == "__main__":
    resources_path = "0-Resources"
    resources = scan_directory(resources_path)

    index_content = generate_index(resources)

    # 可以在这里选择更新 0-Index.md 或输出到控制台
    print(index_content)
