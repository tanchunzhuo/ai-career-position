#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ats_parser.py — 本地 ATS 解析诊断（借鉴 OpenResume 思路）

目的：把用户的简历（PDF/HTML/Markdown/文本）解析成"ATS 实际能读到的文本"，
并对照目标 JD 关键词做差异报告。全部在本机完成，数据不出本地。

用法：
    python3 scripts/ats_parser.py resume.pdf --jd jd.txt
    python3 scripts/ats_parser.py resume.html
    python3 scripts/ats_parser.py cv.md --jd jd.txt --out workspace/output/ats_report.html

输出：
    1. 控制台打印提取文本摘要 + 关键词命中报告
    2. --out 指定时生成 ats_diagnostic.html 报告（预览用）
"""
import argparse
import os
import re
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                return "\n".join((p.extract_text() or "") for p in pdf.pages)
        except ImportError:
            try:
                from pypdf import PdfReader
                return "\n".join((page.extract_text() or "") for page in PdfReader(path).pages)
            except ImportError:
                sys.exit("❌ 解析 PDF 需要 pdfplumber 或 pypdf：pip install pdfplumber")
    if ext in (".html", ".htm"):
        import html as htmlmod
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.parts = []
                self.skip = 0

            def handle_starttag(self, tag, attrs):
                if tag in ("script", "style"):
                    self.skip += 1

            def handle_endtag(self, tag):
                if tag in ("script", "style") and self.skip:
                    self.skip -= 1

            def handle_data(self, data):
                if not self.skip:
                    self.parts.append(data)

        p = TextExtractor()
        p.feed(open(path, encoding="utf-8", errors="ignore").read())
        text = "\n".join(x.strip() for x in p.parts if x.strip())
        return htmlmod.unescape(text)
    if ext in (".md", ".txt"):
        return open(path, encoding="utf-8", errors="ignore").read()
    sys.exit(f"❌ 不支持的文件类型：{ext}（支持 pdf/html/md/txt）")


def analyze(text: str, jd_text: str = ""):
    norm = re.sub(r"\s+", "", text)
    report = {
        "chars": len(norm),
        "has_phone": bool(re.search(r"1[3-9]\d{9}", text)),
        "has_email": bool(re.search(r"[\w.\-]+@[\w\-]+\.\w+", text)),
        "has_birth": bool(re.search(r"(19|20)\d{2}[.\-]\d{1,2}", text)) or bool(re.search(r"\d{4}年\d{1,2}月", text)),
        "has_quantified": len(re.findall(r"\d+%|\d{2,}(万|K|k)|提升|降低|节省|覆盖|规模", text)),
        "jd_hits": [],
        "jd_miss": [],
    }
    if jd_text:
        jd_words = set()
        for m in re.findall(r"[\u4e00-\u9fa5A-Za-z0-9+#.\-/]{2,}", jd_text):
            w = m.strip()
            if 2 <= len(w) <= 30 and not w.isdigit():
                jd_words.add(w.lower())
        # 关键词频次
        for w in sorted(jd_words, key=lambda x: -len(x)):
            if w.lower() in norm.lower():
                report["jd_hits"].append(w)
            elif len(w) >= 3:
                report["jd_miss"].append(w)
        # 只保留缺失中较关键的（按长度排序取前 20）
        report["jd_miss"] = report["jd_miss"][:20]
        report["jd_hits"] = report["jd_hits"][:30]
    return report


def render_html(report, filename, text):
    def badge(ok, label, cls=None):
        k = "ok" if ok else "warn"
        return f'<span class="badge {k}">{label} {"✓" if ok else "⚠"}</span>'

    hits = ", ".join(report["jd_hits"]) if report["jd_hits"] else "（无）"
    miss = ", ".join(report["jd_miss"]) if report["jd_miss"] else "（无）"
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>ATS 诊断报告</title><style>
body{{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#f4f6f8;padding:24px;color:#222}}
.card{{background:#fff;border-radius:8px;padding:20px 24px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
h1{{font-size:20px}} h2{{font-size:15px;color:#1a365d}}
pre{{background:#fafafa;border:1px solid #e2e8f0;border-radius:6px;padding:14px;white-space:pre-wrap;font-family:Consolas,monospace;font-size:12.5px}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:12px;margin:2px 4px 2px 0}}
.ok{{background:#c6f6d5;color:#22543d}} .warn{{background:#feebc8;color:#7c4a03}} .bad{{background:#fed7d7;color:#742a2a}}
table{{width:100%;border-collapse:collapse;font-size:13px}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid #e2e8f0}}
</style></head><body>
<div class="card"><h1>ATS 诊断报告</h1>
<p>文件：{os.path.basename(filename)} ｜ 解析时间：{datetime.now():%Y-%m-%d %H:%M} ｜ 全部在本机完成</p>
{badge(report['has_phone'],'电话')} {badge(report['has_email'],'邮箱')} {badge(report['has_birth'],'出生年月')} {badge(report['has_quantified']>=3,'量化数字')}
<span class="badge {'ok' if report['chars']>200 else 'bad'}">文本量 {report['chars']} 字</span></div>
<div class="card"><h2>ATS 实际提取到的文本（前 1500 字）</h2>
<pre>{text[:1500]}</pre></div>
<div class="card"><h2>JD 关键词命中</h2><table>
<tr><th>已命中</th><td>{hits}</td></tr>
<tr><th>缺失（建议在真实能力范围内对齐表述）</th><td>{miss or '—'}</td></tr></table></div>
<div class="card"><h2>修改建议</h2><ul>
<li>缺失关键词若你真实具备，把简历表述改为 JD 用词（同一技能不同说法）</li>
<li>每条经历至少 1 个可核验数字</li>
<li>日期统一 YYYY.MM；关键信息不放页眉页脚</li>
<li>导出 PDF 时嵌入中文字体，避免乱码</li></ul></div>
</body></html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="ATS 解析诊断")
    parser.add_argument("resume", help="简历文件（pdf/html/md/txt）")
    parser.add_argument("--jd", help="目标 JD 文本文件（可选）")
    parser.add_argument("--out", help="输出 HTML 报告路径（可选）")
    args = parser.parse_args()

    text = extract_text(args.resume)
    jd_text = ""
    if args.jd:
        jd_text = open(args.jd, encoding="utf-8", errors="ignore").read()

    report = analyze(text, jd_text)
    print("=" * 50)
    print("ATS 解析摘要：")
    print(f"  提取文本 {report['chars']} 字 | 电话 {'✓' if report['has_phone'] else '✗'} | 邮箱 {'✓' if report['has_email'] else '✗'} | 出生年月 {'✓' if report['has_birth'] else '✗'}")
    print(f"  量化表述出现 {report['has_quantified']} 次")
    if jd_text:
        print(f"  JD 关键词命中 {len(report['jd_hits'])} 个；缺失 {len(report['jd_miss'])} 个")
        if report["jd_miss"]:
            print("  缺失关键词：", ", ".join(report["jd_miss"]))
    print("=" * 50)
    print("提取文本预览（前 800 字）：\n")
    print(text[:800])

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(render_html(report, args.resume, text))
        print(f"\n✅ 报告已生成：{args.out}")


if __name__ == "__main__":
    main()
