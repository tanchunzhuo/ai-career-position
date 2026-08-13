# AI职业选位 · ai-career-position

> **找到你在 AI 时代最值得站的位置。**
> 一个本地运行、平台无关、人机协同的中国求职 AI 助手。
> by **tanchunzhuo** ｜ v1.0（2026-08）｜ MIT 协议 ｜ 免费开源

---

## 它解决什么问题

市面上的求职工具都在教你「**怎么投简历**」。这个工具在教你「**该投哪个方向**」。

大多数人的焦虑不是「我不会用 AI」，而是「我该往哪走、这个岗位值不值得去、我会不会被 AI 替代」。**AI职业选位**用一套可落地的判断标准，帮你把模糊的焦虑变成具体的决策：

- 🧭 **侧翼雷达（核心差异化）**：先回答最痛的问题——「我该找什么方向」。输入你的背景和约束，产出 3–5 个「领域 × AI」交集坐标 + 90 天验证计划。它不做算命，只给「值得验证的假设」。
- ⚖️ **A–G 七模块评估**：粘贴一个 JD，拆解成 角色 / 匹配度 / 职级 / 薪酬 / 个性化 / 面试 / 红线尽调 七个维度，加权出 1–5 分 + 投/不投建议，拒绝海投。
- 🛡️ **红线尽调**：反诈（培训贷/电诈园区）、劳动合规（试用期/竞业/五险一金基数）、外包识别、雇主尽调清单。命中诈骗类红旗直接一票否决。
- 📄 **ATS 中文简历**：北森/大易/Moka 友好的单栏 HTML + Playwright 出 PDF，通用/创意/国企多版 + ATS 诊断，简历能真正被机器读到。
- 🗂️ **本地追踪**：`applications.tsv` 状态机 + 跟进提醒 + 渠道通过率分析。
- 💬 **面试与谈薪**：STAR+R 故事银行、10 个高信息反问、HR 压价话术、offer 多维比较与合同审阅清单。

## 为什么值得相信它

1. **100% 本地运行，数据不上传**。简历、薪资、投递记录只存你电脑的 `workspace/`，`.gitignore` 已忽略，永不提交任何服务器。2026 年最该被问的问题，这里已经替你守住了。
2. **人机协同，不是自动投递机器**。所有投递、发送、点击由你手动完成，绝不登录招聘平台、绝不存账号密码。它帮你把「该投哪些、怎么避坑」想清楚，把决策权留给你。
3. **不造假、不承诺**。简历优化是「让真实经历被准确解析」，不是伪造；红线检测是「提示去核验」，不是定罪；薪资标注来源与时点，给不出就标「待核验」，绝不编一个漂亮数字。
4. **站在巨人的肩膀上**。理念致敬 **santifer/career-ops**（约 62K★ 的开源求职系统，MIT）：薪资对标、投递模式分析、面试复盘的设计思路源自它，代码为**中国市场完全重写**——中式薪资格式解析（"25-40K×15薪"）、大厂职级对标（阿里 P6/字节 2-2/腾讯 T3）、外包/派遣/培训贷识别，都是原版没有、只为中国求职者做的。

## 安装

### 方式一：一键安装（推荐，一句话）

不用先下载，打开终端贴这一句回车：

```bash
curl -fsSL https://raw.githubusercontent.com/tanchunzhuo/ai-career-position/main/install.sh | bash
```

脚本自动装到 WorkBuddy / Claude Code / Codex / Cursor 的 skills 目录。重启后直接说「帮我找方向」或「评估这个 JD」就会触发，不用记任何命令。

只装某一个平台（例如 WorkBuddy）：

```bash
curl -fsSL https://raw.githubusercontent.com/tanchunzhuo/ai-career-position/main/install.sh | bash -s -- workbuddy
```

### 方式二：clone 后本地安装

```bash
git clone https://github.com/tanchunzhuo/ai-career-position.git
cd ai-career-position && ./install.sh
```

### 方式三：手动复制

把整个 `ai-career-position` 文件夹放进平台的 skills 目录，重启即可：

| 平台 | 目录 |
| :--- | :--- |
| WorkBuddy | `~/.workbuddy/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.agents/skills/` |
| Cursor | `~/.cursor/skills/` |

### 方式四：无脚本使用（任何 AI 都能用，零安装）

1. 复制 `SKILL.md` 与 `prompts/00_syspersona.md` 全文，粘贴给任意 AI（Claude / ChatGPT / Kimi / 豆包 / DeepSeek）；
2. 按需粘贴对应模块提示词，再粘贴 JD 文本；
3. AI 输出完整 A–G 报告 + 评分 + 建议；投递由你自己完成。

### 首次使用流程

1. 创建 `workspace/` 目录（如不存在），写入 `cv.md`（你的真实经历，Markdown）与 `profile.yml`（期望薪资、城市、红线、社招/校招）；
2. 对 AI 说「帮我找方向」→ 跑**侧翼雷达**，锁定 3–5 个目标方向；
3. 看到感兴趣的 JD，说「评估这个 JD」+ 粘贴内容；
4. 用 Bookmarklet（`scripts/bookmarklet.js`）或手动粘贴收集 JD 到本地 inbox；
5. 确认投递后，用 `scripts/tracker.py` 记录并跟进。

## 目录结构

```
ai-career-position/
├── SKILL.md                  # 主调度：解析输入、路由、编排 A–G、聚合输出
├── prompts/                  # 各模块提示词（平台无关核心）
│   ├── 00_syspersona.md      # 统一角色与红线
│   ├── radar.md              # 侧翼雷达（入口模块，差异化核心）
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
├── templates/                # 简历 HTML 模板（模板矩阵见 RESUME_DESIGN_SYSTEM.md）
├── scripts/                  # 本地脚本（可选增强层）
├── workspace/                # 用户数据（gitignore，绝不提交）
└── docs/
    ├── PLATFORM_ADAPTERS.md  # 各宿主适配说明
    ├── DATA_UPDATES.md       # 如何更新 data/*.yml
    ├── PRIVACY.md            # 隐私与合规说明
    ├── VALUE_AND_BOUNDARIES.md # 适用人群、质量与可靠性边界
    └── PUBLISH_TO_GITHUB.md  # SSH 方式发布到 GitHub
```

## 数据与免责声明

- `data/*.yml` 全部带 `meta` 块（版本、更新时点、来源、免责声明）；薪资/职级为 B/C 级社区数据（猎聘/脉脉/看准/OfferShow 等），**仅供谈判锚点参考，决策前请自行核实**；
- 本工具不构成法律意见、求职中介意见，不承诺录用/涨薪结果；
- 数据更新方式见 `docs/DATA_UPDATES.md`，欢迎 PR 一起维护——这类数据变化快，靠社区比靠一个人靠谱。


---

© 2026 tanchunzhuo · 本地运行 · 数据不上传 · 投递的手永远是你自己的
