#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
story_bank.py — 面试故事银行

存取 STAR+R 故事（Markdown，存 workspace/interviews/stories/），
并按标签匹配面试问题。

用法：
    python3 scripts/story_bank.py list                      # 列出所有故事
    python3 scripts/story_bank.py new "故事名" --tags 领导力,失败
    python3 scripts/story_bank.py show 故事名
    python3 scripts/story_bank.py match "如何说服跨部门同事"  # 按关键词匹配
"""
import argparse
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIES_DIR = os.path.join(BASE_DIR, "workspace", "interviews", "stories")
os.makedirs(STORIES_DIR, exist_ok=True)

TEMPLATE = """## {name}

- 标签：[{tags}]

### S 情境
（背景、任务目标，2 句话，含可量化背景）

### T 任务
（你具体负责什么、责任边界）

### A 行动
1. 
2. 
3. 

### R 结果
（量化结果：数字/时间/比例）

### R 反思
（学到什么、如果再遇到会怎样）

### 可回答的问题
- 
"""


def slug(name: str) -> str:
    s = re.sub(r'[\\/:*?"<>|\s]+', "_", name).strip("_")
    return s or "story"


def story_path(name: str) -> str:
    return os.path.join(STORIES_DIR, slug(name) + ".md")


def cmd_list(_):
    files = sorted(os.listdir(STORIES_DIR))
    if not files:
        print("（空）还没有故事。用 new 创建第一个。")
        return
    for f in files:
        if f.endswith(".md"):
            first = open(os.path.join(STORIES_DIR, f), encoding="utf-8").readline().strip("# \n")
            tags = ""
            for line in open(os.path.join(STORIES_DIR, f), encoding="utf-8"):
                if "- 标签：" in line:
                    tags = line.strip().replace("- 标签：", "")
                    break
            print(f"· {first}  [{tags}]")


def cmd_new(args):
    path = story_path(args.name)
    if os.path.exists(path):
        print(f"⚠️ 已存在：{path}（用 show 查看/手动编辑）")
        return
    tags = ",".join(args.tags) if args.tags else "待补充"
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(name=args.name, tags=tags))
    print(f"✅ 已创建：{path}\n请按 STAR+R 结构填写真实经历（AI 可辅助润色，勿虚构）")


def cmd_show(args):
    path = story_path(args.name)
    if not os.path.exists(path):
        print(f"❌ 不存在：{args.name}（用 list 查看）")
        sys.exit(1)
    print(open(path, encoding="utf-8").read())


def cmd_match(args):
    """按问题关键词匹配故事标签/内容。"""
    files = sorted(os.listdir(STORIES_DIR))
    q = args.question.lower()
    scored = []
    for f in files:
        if not f.endswith(".md"):
            continue
        content = open(os.path.join(STORIES_DIR, f), encoding="utf-8").read().lower()
        # 简单打分：问题词在故事里出现的次数
        words = re.findall(r"[\u4e00-\u9fa5]{2,}", args.question)
        score = sum(content.count(w) for w in words)
        scored.append((score, f))
    scored.sort(reverse=True)
    print(f"问题：{args.question}")
    if not scored:
        print("（空）先创建故事。")
        return
    for score, f in scored[:5]:
        print(f"  [{score}分] {f[:-3]}")


def main():
    parser = argparse.ArgumentParser(description="AI职业选位 故事银行")
    sub = parser.add_subparsers(dest="cmd")

    p1 = sub.add_parser("list"); p1.set_defaults(func=cmd_list)
    p2 = sub.add_parser("new")
    p2.add_argument("name")
    p2.add_argument("--tags", nargs="*", help="标签，如 领导力 失败 抗压")
    p2.set_defaults(func=cmd_new)
    p3 = sub.add_parser("show"); p3.add_argument("name"); p3.set_defaults(func=cmd_show)
    p4 = sub.add_parser("match"); p4.add_argument("question"); p4.set_defaults(func=cmd_match)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
