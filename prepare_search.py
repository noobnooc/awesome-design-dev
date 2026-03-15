#!/usr/bin/env python3
"""
Awesome Design Dev - 自动化更新任务
由 cron 定时触发
"""

import os
import re
import subprocess
import json
from datetime import datetime
from pathlib import Path

REPO_DIR = "/root/.nanobot/workspace/awesome-design-dev"

# 分类和搜索关键词
CATEGORIES = {
    "UI Libraries": [
        "new React UI library 2025 open source",
        "Tailwind CSS component library 2025",
        "shadcn alternative new"
    ],
    "Icons": [
        "new open source icons 2025",
        "free SVG icons library React 2025"
    ],
    "Illustrations": [
        "free illustration website 2025",
        "open source illustrations AI generated"
    ],
    "Templates": [
        "free React template 2025 open source",
        "Next.js landing page template 2025"
    ],
    "Tools": [
        "design tool open source 2025",
        "Figma alternative 2025 free"
    ],
    "Photography": [
        "free stock photos 2025 high quality"
    ],
    "Colors": [
        "color palette generator 2025"
    ]
}


def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, 
                           capture_output=True, text=True, timeout=120)
    return result.returncode == 0, result.stdout, result.stderr


def main():
    print(f"🔄 自动更新任务开始 - {datetime.now()}")
    
    # 切换到仓库目录
    os.chdir(REPO_DIR)
    
    # 确保 main 分支是最新的
    run_cmd("git fetch origin")
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    
    # 读取现有 README 获取已收录的链接
    existing_links = set()
    readme_files = ["README.md", "README.zh.md"]
    
    for fname in readme_files:
        fpath = os.path.join(REPO_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
                urls = re.findall(r'\[.*?\]\((https?://[^\)]+)\)', content)
                existing_links.update(urls)
    
    print(f"📋 已收录 {len(existing_links)} 个项目")
    
    # 搜索新资源（这里生成搜索任务描述）
    search_tasks = []
    for category, queries in CATEGORIES.items():
        for query in queries:
            search_tasks.append(f"{category}: {query}")
    
    # 输出搜索任务列表供下一步使用
    print("\n🔍 待搜索关键词:")
    for task in search_tasks[:10]:
        print(f"  - {task}")
    
    # 保存搜索任务到文件
    with open("/root/.nanobot/workspace/awesome-design-dev/search_tasks.json", "w") as f:
        json.dump({
            "tasks": search_tasks,
            "existing_links": list(existing_links),
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print("\n✅ 搜索任务已准备，请运行搜索后更新")


if __name__ == "__main__":
    main()
