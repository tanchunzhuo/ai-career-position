#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inbox_server.py — 本地 Inbox 服务
接收 Bookmarklet（scripts/bookmarklet.js）POST 的 JD JSON，存入 workspace/inbox/。

用法：
    python3 scripts/inbox_server.py            # 默认 127.0.0.1:8787
    python3 scripts/inbox_server.py --port 9000

安全硬约束：
    - 只绑定 127.0.0.1，不对外暴露
    - 不存 cookie/密码、不自动登录、不批量爬取——只接收用户主动点击书签抓到的当前页
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# 工作目录：仓库根（本文件在 scripts/ 下）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(BASE_DIR, "workspace", "inbox")
PROCESSED_DIR = os.path.join(INBOX_DIR, "processed")
os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def safe_name(text: str, fallback: str, max_len: int = 60) -> str:
    """把公司/岗位名转成安全的文件名片段。"""
    text = re.sub(r'[\\/:*?"<>|\s]+', "_", text or "").strip("_")
    return text[:max_len] or fallback


def save_jd(data: dict) -> str:
    """保存 JD 到 inbox/，返回文件名。"""
    company = safe_name(data.get("company", ""), "unknown_company")
    title = safe_name(data.get("title", ""), "unknown_title")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{company}_{title}.json"
    path = os.path.join(INBOX_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename


class InboxHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send(self, status: int, body: str, content_type: str = "text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self._cors()
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_OPTIONS(self):
        self._send(204, "")

    def do_POST(self):
        if self.path.rstrip("/") != "/inbox":
            self._send(404, "not found")
            return
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            # 兼容 form 编码
            try:
                from urllib.parse import parse_qs
                data = {k: v[0] for k, v in parse_qs(raw.decode("utf-8")).items()}
            except Exception:
                self._send(400, "bad request: not json")
                return
        required = ["title", "content"]
        missing = [k for k in required if not data.get(k)]
        if missing:
            self._send(400, f"missing fields: {missing}")
            return
        fname = save_jd(data)
        html = f"""<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8">
<title>已收入 Inbox</title>
<body style="font-family:sans-serif;text-align:center;padding-top:60px">
<h2>✅ JD 已存到本地 Inbox</h2>
<p>文件：{fname}</p>
<p>现在回到你的 AI 助手，输入：<code>/ai-career-position inbox</code> 开始评估</p>
</body></html>"""
        self._send(200, html)

    def do_GET(self):
        if self.path.rstrip("/") in ("/", "/inbox"):
            files = sorted(os.listdir(INBOX_DIR))
            items = "".join(f"<li>{f}</li>" for f in files if f.endswith(".json"))
            html = f"""<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8">
<title>AI职业选位 · 本地 Inbox</title>
<body style="font-family:sans-serif;padding:24px">
<h2>AI职业选位 · 本地 Inbox</h2>
<p>服务运行中（仅本机 127.0.0.1）。当前收件箱：</p>
<ul>{items or '<li>（空）</li>'}</ul>
</body></html>"""
            self._send(200, html)
        else:
            self._send(404, "not found")

    def log_message(self, fmt, *args):  # 简化日志
        sys.stderr.write("[inbox] %s\n" % (fmt % args))


def main():
    parser = argparse.ArgumentParser(description="AI职业选位 本地 Inbox 服务")
    parser.add_argument("--host", default="127.0.0.1", help="仅允许 127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    if args.host not in ("127.0.0.1", "localhost"):
        print("❌ 出于隐私安全，inbox 只允许绑定 127.0.0.1")
        sys.exit(1)
    server = HTTPServer((args.host, args.port), InboxHandler)
    print(f"✅ Inbox 服务已启动：http://{args.host}:{args.port}/inbox")
    print(f"   收件目录：{INBOX_DIR}")
    print("   提示：先运行 scripts/bookmarklet.js 的安装步骤（把代码存为书签）")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")


if __name__ == "__main__":
    main()
