# AI职业选位 · ai-career-position

> **找到你在 AI 时代最值得站的位置。**
> 一个本地运行、平台无关、人机协同的中国求职 AI 助手 Skill。
> 作者：**tanchunzhuo** ｜ 版本：v1.0（2026-08）｜ 协议：MIT

---

## 它是什么

**粘贴一个 JD（文本/URL/截图），《AI职业选位》在本地帮你：**
评估匹配度 → 识破外包与骗局 → 对标职级与总包 → 生成过国内 ATS 的中文简历 → 准备面试 → 追踪投递 → 比较 offer——**但投递永远由你自己点。**

这不是一个"自动投递机器"，而是一个本地 AI 求职参谋：

- 🧭 **侧翼雷达**：先回答最痛的问题"我该找什么方向"，产出 3–5 个"领域 × AI"交集坐标 + 90 天验证计划（本书核心主张的交互版）；
- ⚖️ **A–G 七模块评估**：角色 / 匹配度 / 职级 / 薪酬 / 个性化 / 面试 / 红线尽调，加权出 1–5 分综合评分 + 投/不投建议；
- 🛡️ **红线尽调**：反诈（培训贷/电诈园区）、劳动合规（试用期/竞业/五险一金基数）、外包识别、雇主尽调清单，命中诈骗类红旗直接一票否决；
- 📄 **ATS 中文简历**：北森/大易/Moka 友好的单栏 HTML + Playwright 出 PDF，通用（4 主题）/创意/国企三版 + ATS 诊断；简历视觉基于内置设计系统（SSOT），借鉴 loki-design-system / loki-deck 的配色×版式矩阵思路，并对 ATS/打印做了深底禁用等适配；
- 🗂️ **本地追踪**：`applications.tsv` 状态机 + 跟进提醒 + 渠道通过率分析；
- 💬 **面试与谈薪**：STAR+R 故事银行、10 个高信息反问、HR 话术、offer 多维比较与合同审阅清单。

## 设计底线

1. **人机协同**：所有投递/发送/点击由用户手动完成；绝不自动登录招聘平台、绝不存账号密码。
2. **100% 数据本地**：简历、薪资、追踪记录只存 `workspace/`，`.gitignore` 已忽略，永不提交。
3. **不造假**：简历优化是"让真实经历被准确解析"，不是伪造；红线检测是"提示去核验"，不是定罪。
4. **宁缺毋假**：薪资/职级数据标注来源与时点，无法确认的标"待核验"，不编造精确数字。

## 快速开始

### 方式一：作为 Skill 导入（推荐）

把本目录作为 Skill 放入宿主（腾讯 WorkBuddy 桌面端 / Claude / 其他支持 SKILL.md 的平台）的 skills 目录。触发词见 `SKILL.md` §1。

### 方式二：无脚本使用（任何 AI 都能用）

1. 复制 `SKILL.md` 与 `prompts/00_syspersona.md` 全文，粘贴给任意 AI（Claude / ChatGPT / Kimi / 豆包 / DeepSeek）；
2. 按需粘贴对应模块提示词，再粘贴 JD 文本；
3. AI 输出完整 A–G 报告 + 评分 + 建议；你自己完成投递。

### 首次使用流程

1. 编辑 `workspace/cv.md`（你的真实经历，Markdown）与 `workspace/profile.yml`（期望薪资、城市、红线、社招/校招）；
2. 对 AI 说"帮我找方向" → 跑**侧翼雷达**，锁定 3–5 个目标方向；
3. 看到感兴趣的 JD 后说"评估这个 JD"+ 粘贴内容；
4. 用 Bookmarklet（`scripts/bookmarklet.js`）或手动粘贴收集 JD 到本地 inbox；
5. 确认投递后，用 `scripts/tracker.py` 记录并跟进。

## 目录结构

```
ai-career-position/
├── SKILL.md                  # 主调度：解析输入、路由、编排 A–G、聚合输出
├── prompts/                  # 各模块提示词（平台无关核心）
│   ├── 00_syspersona.md      # 统一角色与红线
│   ├── radar.md              # 侧翼雷达（入口模块）
│   ├── A_role_summary.md … G_redflag_due_diligence.md   # A–G 七模块
│   ├── school_recruit.md     # 校招专属
│   ├── story_bank.md         # 面试故事银行
│   ├── negotiation.md        # 谈薪话术
│   └── offer_compare.md      # offer 比较 + 合同审阅
├── data/                     # 规则与对标数据（社区可更新，均带来源与时点）
│   ├── adjacent_roles.yml    # 侧翼岗位知识库
│   ├── levels.yml            # 大厂职级对标
│   ├── salary.yml            # 分城市/行业/职级薪资
│   ├── redflags.yml          # 反诈/合规/制度/尽调规则
│   ├── companies.yml         # 尽调链接模板 + 外包/派遣名单
│   ├── interview_formats.yml # 面试形式库
│   └── followup_cadence.yml  # 跟进节奏
├── templates/                # 简历 HTML 模板（ATS 友好，设计系统见 RESUME_DESIGN_SYSTEM.md）
│   ├── RESUME_DESIGN_SYSTEM.md   # 简历设计系统 SSOT（色板/字体/版式/质量门禁）
│   ├── resume_general_zh_v3.html # ★旗舰：单栏通用版，4 套主题（navy/rock/sage/tech）CSS 变量切换
├── scripts/                  # 本地脚本（可选增强层）
├── workspace/                # 用户数据（gitignore，绝不提交）
└── docs/
    ├── PLATFORM_ADAPTERS.md  # 各宿主适配说明
    ├── DATA_UPDATES.md       # 如何更新 data/*.yml
    └── PRIVACY.md            # 隐私与合规说明
```

## 数据与免责声明

- `data/*.yml` 全部带 `meta` 块（版本、更新时点、来源、免责声明）；薪资/职级为 C 级匿名社区数据（看准/脉脉/OfferShow 等），**仅供参考，决策前请自行核实**；
- 本工具不构成法律意见、求职中介意见，不承诺录用/涨薪结果；
- 数据更新方式见 `docs/DATA_UPDATES.md`，欢迎 PR。

## 致谢与开源

- 理念致敬 **santifer/career-ops**（MIT 协议，约 63K★）：薪资对标、投递模式分析、面试复盘等设计思路源自该项目，代码全部为中国市场重写；
- 简历 ATS 诊断思路借鉴 OpenResume；简历设计系统（配色/字体/版式/质量门禁）借鉴 loki2046-mao/cola-skills 的 loki-design-system 与 loki-deck（MIT）；
- 本仓库 MIT 协议开源（见 `LICENSE`），引用第三方数据均注明出处。

## 与书的关系

本工具随《AI时代，什么工作值得做？》——站在 AI 的侧翼，找到你的职业坐标（作者 tanchunzhuo）——使用。"侧翼雷达"是书中"侧翼 / 领域 × AI 交集 / 90 天验证"心智模型的交互版：书讲为什么，工具帮你落到自己身上。

---

© 2026 tanchunzhuo · 本地运行 · 数据不上传 · 投递的手永远是你自己的
