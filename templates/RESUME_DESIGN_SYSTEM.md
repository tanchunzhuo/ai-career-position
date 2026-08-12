# RESUME_DESIGN_SYSTEM.md — 简历设计系统（单一事实源 SSOT）

> 定位：本仓库所有简历模板（`templates/*.html`）的**共享基础层**。
> 生成/修改简历模板时，必须先读本文件，再改模板；不允许"凭记忆直接写"。
> 架构借鉴：loki2046-mao/cola-skills 的 loki-design-system（SSOT）与 loki-deck（12配色×12版式矩阵），MIT 协议，致谢。

---

## 0. 三条铁律（ATS/打印语境下的硬约束）

1. **关键信息必须在文本流中**：姓名/电话/邮箱/日期/公司/岗位不得放在图片、文本框、页眉页脚、SVG 里——国内 ATS（北森/大易/Moka/e成）读不到。
2. **底色保持纯白或近白**：深色主题在 PPT 上好看，但简历要进 ATS 和打印机，**深底一律禁用**；"对比"由色条/细线/字重/留白实现，不由背景实现。
3. **装饰克制，信息密度优先**：单栏优先（创意版可双栏但必须标注"仅设计岗"）；禁止 emoji、蓝紫渐变、玻璃拟态、霓虹（借鉴 loki 禁用清单）。

## 1. 色彩系统（全部走 CSS 变量）

**主色板（4 套主题，模板通过 `<body class="theme-xxx">` 切换，只允许选预设，不接受裸 hex）**：

| 主题 | 场景 | 主色 | 强调色 | 正文 | 辅助 | 适用 |
|---|---|---|---|---|---|---|
| `theme-navy` 商务藏青 | 默认/互联网/外企 | `#1f3864` | `#c0a062`(金) | `#2b2f36` | `#718096` | 通用社招 |
| `theme-rock` 极简墨黑 | 设计/极简/知识 | `#111111` | `#e5e5e5` | `#1a1a1a` | `#6b6b6b` | 创意/极简表达 |
| `theme-sage` 鼠尾草知识分子 | 生活/教育/慢节奏 | `#4a6741` | `#9caf88` | `#2f3a2c` | `#7a8a6f` | 教育/心理/非科技 |
| `theme-tech` 科技灰蓝 | 技术/AI/数据 | `#0f4c5c` | `#5fe3d0` | `#1c2733` | `#5a7a85` | 算法/研发/AI岗 |

**用法示例**：
```css
:root { --paper:#fff; --ink:#2b2f36; --muted:#718096; --line:#e4e8ef;
        --brand:#1f3864; --accent:#c0a062; }
body.theme-rock { --brand:#111; --accent:#e5e5e5; --ink:#1a1a1a; --muted:#6b6b6b; --line:#eaeaea; }
```
所有颜色必须 `var(--xxx)` 引用；直接写 hex 视为违规（自检命令见 §6）。

## 2. 字体系统

```css
--font-body: "PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;   /* 正文 */
--font-display: "PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif; /* 标题（用 700-900 字重） */
--font-mono: "SF Mono","JetBrains Mono",Consolas,monospace;               /* 日期/序号/数字 */
```
- **极端反差**（借鉴 loki）：姓名 20–24pt/700–900，正文 10pt，日期 8.5–9pt 用 mono——三者差距拉开；
- 标题用 700–900（中文黑体没有 200 细体，反差靠"标题粗×正文常规×日期细 mono"实现）；
- 本地 PDF 渲染（Playwright）依赖系统字体，勿引入需联网的 web font（预览沙箱无网络）。

## 3. 版式系统（组件矩阵，按场景组合）

| 组件 | 样式 | 说明 |
|---|---|---|
| H1 头部 | 左：姓名+求职意向 ｜ 右：联系方式列（右对齐，图标用内联 SVG，仅装饰、关键文本仍在文本流） | 非对称布局（借鉴 loki 原则④） |
| 节标题 | 色条（4px）+ 标题 + 细线延展（`::after` 占满剩余） | 模仿 loki eyebrow：色条即"眉头标签" |
| 条目头 | 公司（粗）· 岗位（主题色）· 日期（右对齐 mono） | 信息三要素分离 |
| 要点 | 自定义小圆点（`li::before`，用强调色 5px 圆点） | 替代浏览器默认实心点，细节感 |
| 技能区 | 分隔符 `｜` 横排 | 一屏可读，不打散 |
| 自我评价 | 3 行，标签词加粗+主题色 | 克制 |

## 4. 场景映射（scene-mapping，借鉴 loki）

| 用户场景 | 模板 | 主题 |
|---|---|---|
| 通用社招（互联网/外企/软件） | `resume_general_zh_v3.html` | navy（默认） |
| 技术/AI/算法岗 | `resume_general_zh_v3.html` | tech |
| 设计/创意岗 | `resume_creative_zh.html` | rock（双栏） |
| 国企/事业单位/选调 | `resume_state_owned.html` | navy（可加红金辅助，但保持克制） |
| 教育/心理/人文类 | `resume_general_zh_v3.html` | sage |

## 5. 质量清单（P0/P1/P2，交付前必须过 P0）

**P0（不过不出门）**
- [ ] 关键信息（姓名/电话/邮箱/日期/公司/岗位）在文本流中，不在图片/SVG/页眉页脚
- [ ] 单栏（创意版除外且已标注）
- [ ] 所有颜色走 `var()`，无裸 hex
- [ ] 无 emoji、无蓝紫渐变、无玻璃拟态、无霓虹
- [ ] 字体回退链完整（PingFang → YaHei → Noto Sans SC → sans-serif）
- [ ] A4 打印页边距与分页正常（Playwright 渲染实测）
- [ ] 日期格式统一 YYYY.MM

**P1（推荐）**
- [ ] 每条经历至少 1 个可核验数字（真实）
- [ ] 字号三级反差（标题/正文/日期 mono）
- [ ] 深浅/粗细节奏：连续条目无视觉疲劳
- [ ] 技能表述与目标 JD 关键词对齐（真实能力范围内）

**P2（可选）**
- [ ] 内联 SVG 图标点缀（电话/邮箱/位置，保持单色=主题色）
- [ ] 一页纸（应届/3年内）或两页内（资深）

## 6. 自检命令

```bash
# 检查裸 hex（应无输出或仅出现在 :root/主题块定义处）
grep -nE "color:\s*#[0-9A-Fa-f]{3,6}" templates/*.html | grep -v "var(" | grep -v "^\s*#" | head
# 检查字体回退
grep -c "PingFang SC" templates/*.html   # 每个文件应 ≥1
# 检查 emoji（应无输出）
grep -nP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" templates/*.html
```

## 7. 模板清单与状态

| 文件 | 状态 | 主题支持 |
|---|---|---|
| `resume_general_zh.html` | v1 基础版（保留兼容） | 单一 |
| `resume_general_zh_v2.html` | v2（旧现代风，可弃用） | 单一 |
| `resume_general_zh_v3.html` | ★旗舰（本设计系统首落） | navy/rock/sage/tech 四套 |
| `resume_creative_zh.html` | 双栏创意版 | rock |
| `resume_state_owned.html` | 国企版 | navy |

## 8. 致谢

设计系统架构与设计原则借鉴 loki2046-mao/cola-skills 的 loki-design-system / loki-deck（MIT），已做简历场景适配（深底→纯白、emoji→禁用、对称网格→非对称信息布局）。
