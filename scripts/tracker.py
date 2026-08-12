#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tracker.py — 投递追踪（TSV + 状态机 + 健康检查 + 提醒）

数据文件：workspace/data/applications.tsv（UTF-8，可用 Excel 打开）
表头（与 SKILL.md §11 一致）：
    公司 | 岗位 | 招聘类型 | 职级对标 | 薪资范围(广告) | 估算总包 | 匹配度% | 综合评分 | 红线 | 状态 | 投递日期 | 下一步 | 下一步截止 | 渠道 | 备注

用法：
    python3 scripts/tracker.py list                 # 列表
    python3 scripts/tracker.py add 公司 岗位 ...     # 添加
    python3 scripts/tracker.py status 行号 新状态    # 状态流转
    python3 scripts/tracker.py next 行号 下一步 [截止日期]  # 更新下一步
    python3 scripts/tracker.py health               # 健康检查（跟进提醒）
    python3 scripts/tracker.py stats                # 渠道通过率统计
"""
import argparse
import os
import sys
from datetime import date, datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "workspace", "data")
TSV_PATH = os.path.join(DATA_DIR, "applications.tsv")

HEADER = ["公司", "岗位", "招聘类型", "职级对标", "薪资范围(广告)", "估算总包",
          "匹配度%", "综合评分", "红线", "状态", "投递日期", "下一步", "下一步截止", "渠道", "备注"]

# 状态机（顺序）
STATES = ["已评估", "已投递", "简历筛选中", "笔试中", "面试中", "Offer中", "已接受", "已拒绝", "已默拒"]

# 跟进节奏（天），与 data/followup_cadence.yml 对齐
CADENCE = {
    "已投递": 5,
    "简历筛选中": 7,
    "笔试中": 5,
    "面试中": 3,
    "Offer中": 7,
}


def ensure_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TSV_PATH):
        with open(TSV_PATH, "w", encoding="utf-8") as f:
            f.write("\t".join(HEADER) + "\n")
        print(f"✅ 已创建 {TSV_PATH}")


def read_rows():
    ensure_file()
    rows = []
    with open(TSV_PATH, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    if not lines:
        return rows
    header = lines[0].split("\t")
    for i, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        rows.append({"row": i, "cells": cells, "line": line})
    return rows


def write_rows(rows):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TSV_PATH, "w", encoding="utf-8") as f:
        f.write("\t".join(HEADER) + "\n")
        for r in rows:
            f.write("\t".join(r["cells"]) + "\n")


def parse_date(s):
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def cmd_list(args):
    rows = read_rows()
    if not rows:
        print("（空）还没有投递记录。用 add 添加，或让 AI 评估后写入。")
        return
    print(f"{'行':<4}{'公司':<18}{'岗位':<24}{'状态':<10}{'评分':<5}{'投递日期':<12}")
    print("-" * 80)
    for r in rows:
        c = r["cells"]
        print(f"{r['row']:<6}{c[0][:16]:<20}{c[1][:22]:<26}{(c[9] if len(c)>9 else ''):<12}{(c[7] if len(c)>7 else ''):<6}{(c[10] if len(c)>10 else '')}")


def cmd_add(args):
    rows = read_rows()
    cells = [args.company, args.job, args.job_type or "", "", "", "",
             args.match or "", args.score or "", "", "已评估",
             date.today().isoformat(), "", "", args.channel or "", args.note or ""]
    rows.append({"row": len(rows) + 2, "cells": cells, "line": ""})
    write_rows(rows)
    print(f"✅ 已添加：{args.company} / {args.job}（状态：已评估）")


def cmd_status(args):
    rows = read_rows()
    target = None
    for r in rows:
        if r["row"] == args.row:
            target = r
            break
    if not target:
        print(f"❌ 行 {args.row} 不存在"); sys.exit(1)
    if args.new_state not in STATES:
        print(f"❌ 非法状态：{args.new_state}，可选：{' / '.join(STATES)}"); sys.exit(1)
    target["cells"][9] = args.new_state
    if args.new_state == "已投递":
        target["cells"][10] = target["cells"][10] or date.today().isoformat()
    write_rows(rows)
    print(f"✅ 行 {args.row} 状态 → {args.new_state}")


def cmd_next(args):
    rows = read_rows()
    target = None
    for r in rows:
        if r["row"] == args.row:
            target = r
            break
    if not target:
        print(f"❌ 行 {args.row} 不存在"); sys.exit(1)
    target["cells"][11] = args.action
    target["cells"][12] = args.due or ""
    write_rows(rows)
    print(f"✅ 行 {args.row} 下一步已更新：{args.action}（截止 {args.due or '未设'}）")


def cmd_health(args):
    """健康检查：按跟进节奏找出过期/该跟进/该默拒的记录。"""
    rows = read_rows()
    today = date.today()
    due = []
    for r in rows:
        c = r["cells"]
        state = c[9] if len(c) > 9 else ""
        if state not in CADENCE:
            continue
        apply_date = parse_date(c[10] if len(c) > 10 else "")
        if not apply_date:
            continue
        days = (today - apply_date).days
        limit = CADENCE[state]
        if days > limit:
            due.append((r["row"], c[0], c[1], state, days))
    if not due:
        print("✅ 健康：没有过期的跟进项")
        return
    print(f"⚠️ {len(due)} 项需要跟进（截止日参考 data/followup_cadence.yml）：")
    for row, company, job, state, days in due:
        msg = {
            "已投递": "超5天无跟进 → 礼貌询问筛选进度",
            "简历筛选中": "超7天 → 可询问进度",
            "笔试中": "超5天 → 询问结果",
            "面试中": "超3天 → 跟进/准备默拒",
            "Offer中": "超7天 → 紧急决策",
        }[state]
        print(f"  行{row} {company}/{job} [{state}] 已过{days}天：{msg}")


def cmd_stats(args):
    """渠道通过率统计（借鉴原版 pattern analysis）。"""
    rows = read_rows()
    from collections import defaultdict
    total = defaultdict(int)
    advanced = defaultdict(int)  # 进入面试的
    offer = defaultdict(int)
    for r in rows:
        c = r["cells"]
        ch = c[13] if len(c) > 13 else "未知"
        state = c[9] if len(c) > 9 else ""
        total[ch] += 1
        if state in ("面试中", "Offer中", "已接受", "已拒绝"):
            advanced[ch] += 1
        if state in ("已接受",):
            offer[ch] += 1
    if not total:
        print("（空）无数据"); return
    print(f"{'渠道':<10}{'投递数':<8}{'进入面试':<10}{'offer':<8}{'面试转化率'}")
    print("-" * 50)
    for ch in total:
        t = total[ch]
        a = advanced[ch]
        o = offer[ch]
        rate = f"{a / t * 100:.0f}%" if t else "-"
        print(f"{ch:<12}{t:<10}{a:<12}{o:<10}{rate}")


def main():
    parser = argparse.ArgumentParser(description="AI职业选位 投递追踪")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="列出所有记录")
    p_list.set_defaults(func=cmd_list)

    p_add = sub.add_parser("add", help="添加记录")
    p_add.add_argument("company")
    p_add.add_argument("job")
    p_add.add_argument("--job_type", help="招聘类型")
    p_add.add_argument("--match", help="匹配度%")
    p_add.add_argument("--score", help="综合评分")
    p_add.add_argument("--channel", help="渠道(内推/猎头/官网/BOSS)")
    p_add.add_argument("--note", help="备注")
    p_add.set_defaults(func=cmd_add)

    p_st = sub.add_parser("status", help="状态流转")
    p_st.add_argument("row", type=int)
    p_st.add_argument("new_state", choices=STATES)
    p_st.set_defaults(func=cmd_status)

    p_nx = sub.add_parser("next", help="更新下一步")
    p_nx.add_argument("row", type=int)
    p_nx.add_argument("action")
    p_nx.add_argument("--due", help="截止日期 YYYY-MM-DD")
    p_nx.set_defaults(func=cmd_next)

    p_hl = sub.add_parser("health", help="健康检查/跟进提醒")
    p_hl.set_defaults(func=cmd_health)

    p_stt = sub.add_parser("stats", help="渠道通过率统计")
    p_stt.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
