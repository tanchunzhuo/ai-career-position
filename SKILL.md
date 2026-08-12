# SKILL.md —《AI职业选位》主调度

> 名称：AI职业选位 / ai-career-position
> 版本：v1.0 · 2026-08
> 作者：tanchunzhuo
> 简介：找到你在 AI 时代最值得站的位置。粘贴一个 JD（文本/URL/截图），本地评估匹配度、识破外包与骗局、对标职级与总包、生成过国内 ATS 的中文简历、准备面试、追踪投递、比较 offer——投递永远由用户自己完成。

---

## 0. 三条铁律（任何模块都不得违反）

1. **人机协同，不是自动求职机**：所有投递、发送、点击、提交动作必须由用户手动完成。绝不登录招聘平台、绝不自动投递、绝不存储账号密码。
2. **隐私优先，100% 数据本地**：简历、JD、追踪记录全部以纯文本（Markdown/TSV/JSON/YAML）存于用户授权的本地工作目录 `workspace/`。不上传、不外发、不内置遥测。
3. **不造假、不替用户做决定**：简历优化只做"真实经历的准确呈现"，红线检测只做"提示去核验"，薪资数据标注来源与时点，不承诺结果。

---

## 1. 触发词

- `评估这个 JD` / `分析这个职位` / `这个岗位怎么样`
- `/ai-career-position`（后接参数：`inbox` / `tracker` / `radar` / `resume` / `story` / `offer`）
- `比较 offer` / `准备面试` / `帮我找方向` / `我适合什么` / `看看这个简历`

## 2. 输入处理

**输入类型**（按优先级）：
1. 粘贴的 JD 文本；
2. JD URL（提示用户手动打开并复制正文，或用 Bookmarklet 存入 inbox；**绝不自动抓取批量页面**）；
3. 截图（走宿主 OCR）；
4. `workspace/inbox/*.json`（Bookmarklet 抓取，`/ai-career-position inbox` 扫描）；
5. 对话补全（用户直接描述岗位）。

**识别字段**：
- 来源平台：BOSS直聘 / 猎聘 / 拉勾 / 智联招聘 / 牛客 / 应届生求职网 / 公司官网 / 外企官网 / 其他；
- 招聘类型：**社招 / 校招 / 实习 / 管培生 / 外包**；
- 行业、城市、岗位方向。

**必读文件**：
- `workspace/cv.md`（用户主简历）
- `workspace/profile.yml`（用户画像：期望薪资、城市、红线、校招/社招、雷达锁定的方向）
- 若已跑过侧翼雷达，读取其锁定的"交集坐标"，用于加权匹配。

## 3. 编排流程

```
0. 首次使用，或用户说"找方向/我适合什么/不知道投什么"时
   → 先跑 prompts/radar.md（侧翼雷达），产出候选交集坐标 + 目标岗位清单
   → 写入 workspace/profile.yml 的 radar_locked 字段

1. 当用户给出具体 JD：
   → 解析清洗（§4 规范：来源、类型、行业、城市；中式薪资格式解析；福利制度；合同主体与外包识别）
2. 读取 workspace/cv.md 与 workspace/profile.yml
3. 若识别为 校招/实习/管培生 → 追加 prompts/school_recruit.md
4. 并行/顺序执行 A–G 七模块（prompts/A~G_*.md），每模块输出结构化结果
5. 按权重聚合综合评分（默认权重见下），给出 投/不投 建议 + 行动清单
6. 用户确认后，将记录写入 workspace/data/applications.tsv，状态"已评估"
7. 按需触发：简历生成（templates/ + scripts/resume_render.py）、面试准备（F + story_bank）、offer 比较（offer_compare.md）
```

**评分权重（默认，可被用户 profile.yml 覆盖）**：
| 模块 | 权重 | 说明 |
|---|---|---|
| B 匹配度 | 25% | CV vs JD |
| D 薪酬 | 20% | 市场对标 + 总包拆解 |
| G 红线 | 25% | **可一票否决**：命中"诈骗/严重违法"类红旗 → 综合评分直接 ≤2.0 并置顶警告 |
| C 职级 | 10% | 职级对标与年限预期 |
| A 角色 | 10% | 岗位本质 |
| E 个性化 | 10% | 投递策略 |
| F 面试 | — | 不参与评分，提供准备材料 |

**评分建议**：综合 ≥4.0 → 建议投；3.0–4.0 → 有保留地投（列明条件）；<3.0 → 不建议投。
**拒绝海投**：宁可少投，用 A–G 筛出值得投的岗位。

## 4. 输出纪律

- 所有事实性结论**必须可追溯**：引用 JD 原文（带原文摘录）或 `data/*.yml` 文件；
- 无法确定的信息标注 **"待核验"**，绝不编造；
- 薪资/职级类结论必须带**来源与数据时点**；
- 给用户的行动建议要具体到"下一步做什么、找谁、问什么"，而不是空泛建议。

## 5. 模块与文件映射

| 模块 | 提示词 | 数据 | 脚本 |
|---|---|---|---|
| 侧翼雷达（入口） | `prompts/radar.md` | `data/adjacent_roles.yml` | — |
| A 角色总结 | `prompts/A_role_summary.md` | — | — |
| B CV 匹配 | `prompts/B_cv_match.md` | — | — |
| C 职级对标 | `prompts/C_level_benchmark.md` | `data/levels.yml` | — |
| D 薪酬调研 | `prompts/D_compensation.md` | `data/salary.yml` | — |
| E 个性化建议 | `prompts/E_personalization.md` | `workspace/profile.yml` | — |
| F 面试准备 | `prompts/F_interview_prep.md` | `data/interview_formats.yml` | `scripts/story_bank.py` |
| G 红线尽调 | `prompts/G_redflag_due_diligence.md` | `data/redflags.yml` `data/companies.yml` | — |
| 校招专属 | `prompts/school_recruit.md` | — | — |
| 故事银行 | `prompts/story_bank.md` | — | `scripts/story_bank.py` |
| 谈薪话术 | `prompts/negotiation.md` | `data/followup_cadence.yml` | — |
| Offer 比较 | `prompts/offer_compare.md` | — | — |
| 简历 | §7 | `templates/*.html` | `scripts/resume_render.py` `scripts/ats_parser.py` |
| 追踪 | §11 | `workspace/data/applications.tsv` | `scripts/tracker.py` |
| Inbox | §12 | `workspace/inbox/` | `scripts/inbox_server.py` `scripts/bookmarklet.js` |

## 6. 无脚本使用指南（平台无关核心）

如果宿主没有脚本能力（纯聊天 AI），按此流程同样可用：
1. 把本文件 + `prompts/00_syspersona.md` 的内容贴给任意 AI；
2. 按需贴入对应模块提示词（A–G、radar 等）；
3. 粘贴 JD 文本（或让用户手动上传截图/文件）；
4. 让 AI 按模块逐项输出，最后聚合评分；
5. 用户手动执行所有投递动作。

差异仅在于：无自动 PDF 渲染、无本地 inbox 服务、无 TSV 自动读写（用户手动维护表格或让 AI 输出表格文本）。
