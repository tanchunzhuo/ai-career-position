# PLATFORM_ADAPTERS.md — 多端适配说明

《AI职业选位》设计为**平台无关核心 + 多端适配层**：
- 核心层（`prompts/` + `data/` + `templates/`）是纯文本，任何 AI 复制即可用；
- 适配层（脚本、本地服务、浏览器自动化）按宿主能力可选启用。

## 一、核心层（所有平台通用）

**无脚本使用方式**（任何 AI 都能用）：
1. 复制 `SKILL.md` + `prompts/00_syspersona.md` 全文；
2. 首次使用：粘贴 `prompts/radar.md`（找方向）或直接粘贴 JD 开始评估；
3. 需要哪个模块就粘贴对应 `prompts/*.md`；
4. 数据文件（`data/*.yml`）按需贴给 AI（或让 AI 依葫芦画瓢）；
5. 所有投递动作用户手动完成。

## 二、腾讯 WorkBuddy（首选完整形态）

- **Skill 形态**：整个仓库作为 Skill 目录，`SKILL.md` 即主提示词/调度逻辑；
- 能力映射：
  - 本地文件读写 → `workspace/` 与 `data/`（用户授权目录）
  - 本地服务 → `scripts/inbox_server.py`（可选）
  - 浏览器 → 引导用户手动打开页面 + Bookmarklet（`scripts/bookmarklet.js`）
  - 渲染 → `scripts/resume_render.py`（可选，有 Playwright 时）
- 触发词见 `SKILL.md` §1；`/ai-career-position inbox` 扫描 inbox。

## 三、Claude（Custom Skills / Projects）

- 用 Project/Knowledge 挂载：`prompts/`、`data/`、`templates/`；
- `SKILL.md` 作为项目说明/系统提示；
- 文件读写依赖用户手动上传/下载（无本地文件系统时）；
- 脚本层不适用，用"无脚本使用方式"。

## 四、ChatGPT（Custom GPT / Projects）

- 把核心提示词 + 数据放进 GPT 的 Instructions / Knowledge；
- JD 由用户粘贴或上传；简历用模板 HTML + 浏览器打印为 PDF；
- 追踪表让 GPT 输出 TSV 文本，用户粘回本地。

## 五、Kimi / 豆包 / DeepSeek / 其他国产 AI

- 同样用"无脚本使用方式"：粘贴提示词 + JD 即可跑 A–G；
- 这些平台更擅长中文，输出 A–G 报告质量通常不错；
- 注意：以上平台均为联网服务——**不要粘贴含隐私信息的完整简历/薪资**，或仅粘贴脱敏后的 JD 分析请求（隐私规则见 `PRIVACY.md`）。

## 六、差异速查

| 能力 | 核心层（任何AI） | WorkBuddy | Claude/ChatGPT 等 |
|---|---|---|---|
| A–G 评估 | ✅ 粘贴即用 | ✅ | ✅ |
| 侧翼雷达 | ✅ | ✅ | ✅ |
| 本地 inbox/Bookmarklet | ❌ | ✅（脚本可选） | ❌ |
| PDF 渲染 | ❌（浏览器打印） | ✅（可选） | ❌（浏览器打印） |
| TSV 追踪 | ❌（手动表格） | ✅ tracker.py | ❌（手动） |
| 隐私 | 视平台（联网服务慎贴隐私） | ✅ 本地 | ⚠️ 慎贴隐私 |
