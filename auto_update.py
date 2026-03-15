#!/usr/bin/env python3
"""
Awesome Design Dev - 自动更新脚本
每天搜索未收录的设计资源并提交 PR

排序规则 (Sorting Rules):
=========================
1. 按知名度和通用度综合排序，越知名越通用越靠前
2. 内容偏向英语/国际社区，避免收录只有中文社区使用的项目
3. 新项目默认添加到分类末尾，由维护者手动调整位置
4. 排除标准:
   - 仅在中国流行的项目（如 IconPark 字节跳动图标库）
   - GitHub star 数低于 1k 的项目（除非有特殊亮点）
   - 已停止维护的项目
"""

import os
import re
import subprocess
import json
from datetime import datetime
from pathlib import Path

# 配置
REPO_DIR = "/root/.nanobot/workspace/awesome-design-dev"
REPO_OWNER = "noobnooc"
REPO_NAME = "awesome-design-dev"
LANGUAGES = ["en", "zh", "es", "fr", "de", "ja"]
README_FILES = {
    "en": "README.md",
    "zh": "README.zh.md",
    "es": "README.es.md",
    "fr": "README.fr.md",
    "de": "README.de.md",
    "ja": "README.ja.md"
}

# 搜索关键词模板
SEARCH_QUERIES = {
    "UI Libraries": [
        "React UI library 2024 2025",
        "Tailwind CSS component library",
        "open source UI components 2025"
    ],
    "Icons": [
        "open source icons library 2025",
        "free SVG icons React 2024"
    ],
    "Illustrations": [
        "free illustration SVG 2025",
        "open source illustrations website"
    ],
    "Templates": [
        "free landing page template React 2025",
        "open source dashboard template"
    ],
    "Tools": [
        "design tool open source 2025",
        "Figma alternative open source"
    ]
}


def run_cmd(cmd, cwd=None, capture=True):
    """执行命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=capture,
            text=True, timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_git_status():
    """获取 git 状态"""
    success, stdout, _ = run_cmd("git status", cwd=REPO_DIR)
    return stdout if success else ""


def ensure_clean():
    """确保工作区干净"""
    status = get_git_status()
    if "nothing to commit" not in status and "clean" not in status:
        print("⚠️  工作区有未提交的更改，正在撤销...")
        run_cmd("git checkout .", cwd=REPO_DIR)
        run_cmd("git clean -fd", cwd=REPO_DIR)


def sync_with_remote():
    """同步远程最新状态"""
    print("🔄 同步远程最新状态...")
    run_cmd("git fetch origin", cwd=REPO_DIR)
    
    # 检查本地 main 是否落后
    success, local_hash, _ = run_cmd("git rev-parse HEAD", cwd=REPO_DIR)
    success, remote_hash, _ = run_cmd("git rev-parse origin/main", cwd=REPO_DIR)
    
    if local_hash.strip() != remote_hash.strip():
        print("📥 拉取远程最新代码...")
        run_cmd("git checkout main", cwd=REPO_DIR)
        run_cmd("git pull origin main", cwd=REPO_DIR)
    else:
        print("✅ 已同步")


def parse_readme_links(readme_content, category):
    """解析 README 中某个分类的链接"""
    links = set()
    
    # 找到分类部分
    pattern = f"## {category}(.*?)(?=##|$)"
    match = re.search(pattern, readme_content, re.DOTALL)
    if not match:
        return links
    
    section = match.group(1)
    # 提取所有链接
    url_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    for match in re.finditer(url_pattern, section):
        links.add(match.group(2))
    
    return links


def get_all_existing_links():
    """获取所有已收录的链接"""
    print("📋 获取已收录的项目...")
    links = set()
    
    for lang, filename in README_FILES.items():
        filepath = os.path.join(REPO_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for category in SEARCH_QUERIES.keys():
                category_links = parse_readme_links(content, category)
                links.update(category_links)
    
    print(f"   已收录: {len(links)} 个项目")
    return links


def search_new_resources(existing_links):
    """搜索新的设计资源"""
    print("🔍 搜索新的设计资源...")
    new_resources = []
    
    # 这里使用 web_search 搜索（需要外部工具）
    # 实际执行时会通过外部调用
    for category, queries in SEARCH_QUERIES.items():
        for query in queries:
            # 模拟搜索结果（实际需要调用 web_search）
            pass
    
    return new_resources


def update_readme_files(new_items):
    """更新所有语言版本的 README"""
    if not new_items:
        print("✅ 没有新项目需要添加")
        return False
    
    print(f"📝 更新 {len(new_items)} 个新项目到所有语言版本...")
    
    for lang, filename in README_FILES.items():
        filepath = os.path.join(REPO_DIR, filename)
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        for item in new_items:
            # 找到对应分类位置
            category = item['category']
            pattern = rf"(## {category}\n)"
            
            if re.search(pattern, content):
                # 添加新项目（格式：[名称](URL) - 描述）
                entry = f"- [{item['name']}]({item['url']}) - {item['description']}\n"
                content = re.sub(pattern, rf"\1{entry}", content, count=1)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ 已更新 {filename}")
    
    return True


def create_branch_and_commit(new_items):
    """创建分支并提交"""
    branch_name = f"update-{datetime.now().strftime('%Y%m%d')}"
    print(f"🌿 创建分支: {branch_name}")
    
    # 创建新分支
    run_cmd(f"git checkout -b {branch_name}", cwd=REPO_DIR)
    
    # 添加更改
    run_cmd("git add -A", cwd=REPO_DIR)
    
    # 检查是否有更改
    success, stdout, _ = run_cmd("git status", cwd=REPO_DIR)
    if "nothing to commit" in stdout:
        print("✅ 没有新的更改需要提交")
        run_cmd("git checkout main", cwd=REPO_DIR)
        run_cmd(f"git branch -D {branch_name}", cwd=REPO_DIR)
        return None
    
    # 提交
    item_names = ", ".join([item['name'][:20] for item in new_items[:3]])
    commit_msg = f"Add new design resources: {item_names}"
    if len(new_items) > 3:
        commit_msg += f" and {len(new_items)-3} more"
    
    run_cmd(f'git commit -m "{commit_msg}"', cwd=REPO_DIR)
    print(f"✅ 已提交: {commit_msg}")
    
    # 推送
    print("📤 推送到远程...")
    run_cmd(f"git push -u origin {branch_name}", cwd=REPO_DIR)
    
    return branch_name


def create_pull_request(branch_name, new_items):
    """创建 Pull Request"""
    if not branch_name:
        return None
    
    print("📄 创建 Pull Request...")
    
    # 使用 gh cli 创建 PR
    title = f"Add new design resources ({datetime.now().strftime('%Y-%m-%d')})"
    body = f"""## Summary
This PR adds {len(new_items)} new design resources to the list.

### New Resources
"""
    for item in new_items:
        body += f"- **{item['name']}** ({item['category']}): {item['description']}\n"
    
    body += f"""
### Changes
- Updated all language versions (en, zh, es, fr, de, ja)
- Added new entries to appropriate categories

---
*Automated update on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    cmd = f'gh pr create --title "{title}" --body "{body}" --base main'
    success, stdout, stderr = run_cmd(cmd, cwd=REPO_DIR)
    
    if success:
        pr_url = stdout.strip()
        print(f"✅ PR 创建成功: {pr_url}")
        return pr_url
    else:
        print(f"❌ PR 创建失败: {stderr}")
        return None


def switch_to_main():
    """切换回 main 分支"""
    run_cmd("git checkout main", cwd=REPO_DIR)


def main():
    print("=" * 50)
    print("🚀 Awesome Design Dev 自动更新脚本")
    print("=" * 50)
    
    # 1. 确保工作区干净
    ensure_clean()
    
    # 2. 同步远程最新状态
    sync_with_remote()
    
    # 3. 获取已收录的链接
    existing_links = get_all_existing_links()
    
    # 4. 搜索新的资源（需要外部搜索）
    # 这里返回空列表，实际使用时需要通过外部工具获取
    new_items = []
    
    if not new_items:
        print("🤷 没有发现新资源")
        switch_to_main()
        return
    
    # 5. 更新 README 文件
    if not update_readme_files(new_items):
        switch_to_main()
        return
    
    # 6. 创建分支并提交
    branch_name = create_branch_and_commit(new_items)
    
    if not branch_name:
        switch_to_main()
        return
    
    # 7. 创建 Pull Request
    pr_url = create_pull_request(branch_name, new_items)
    
    # 8. 切换回 main
    switch_to_main()
    
    print("\n" + "=" * 50)
    if pr_url:
        print(f"🎉 完成！PR: {pr_url}")
    else:
        print("❌ 流程完成但 PR 创建失败")
    print("=" * 50)


if __name__ == "__main__":
    main()
