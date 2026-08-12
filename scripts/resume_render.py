#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resume_render.py — 简历 HTML → A4 PDF（Playwright）

用法：
    python3 scripts/resume_render.py templates/resume_general_zh.html -o workspace/output/resume.pdf
    python3 scripts/resume_render.py 简历.html            # 默认输出同名 .pdf

依赖（可选层）：
    pip install playwright && playwright install chromium
没有 Playwright 时：直接浏览器打开 HTML → Ctrl+P → 打印为 PDF（同样可行）。

隐私：渲染全程在本机完成，不上传任何内容。
"""
import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def render(html_path: str, out_path: str) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("❌ 未安装 Playwright。\n"
                 "   安装：pip install playwright && playwright install chromium\n"
                 "   或直接用浏览器打开 HTML → 打印为 PDF。")

    html_path = os.path.abspath(html_path)
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    file_url = "file://" + html_path
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        page.pdf(
            path=out_path,
            format="A4",
            margin={"top": "14mm", "bottom": "14mm", "left": "16mm", "right": "16mm"},
            print_background=True,
        )
        browser.close()
    print(f"✅ PDF 已生成：{out_path}")


def main():
    parser = argparse.ArgumentParser(description="简历 HTML → A4 PDF")
    parser.add_argument("html", help="简历 HTML 文件路径")
    parser.add_argument("-o", "--output", help="输出 PDF 路径")
    args = parser.parse_args()

    out = args.output or os.path.splitext(args.html)[0] + ".pdf"
    render(args.html, out)


if __name__ == "__main__":
    main()
