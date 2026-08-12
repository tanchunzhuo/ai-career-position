# DATA_UPDATES.md — 如何更新 data/*.yml

`data/` 下的所有 YAML 都是**社区可更新**的（对应 SKILL.md 元指令 5：所有易过时数据放 `data/*.yml`，不写死在提示词里）。职级、薪资、红线规则会变，欢迎提 PR。

## 1. 通用规范

每个 `data/*.yml` 顶部必须保留 `meta` 块：

```yaml
meta:
  version: "1.0"          # 语义化版本，改内容时递增
  last_updated: "2026-08" # 改为你的更新月份
  sources: [来源列表]      # 新增数据必须注明来源
  disclaimer: "仅供参考，薪资/职级/规则会变化，决策前请自行核实"
```

**数据准确性原则**：宁可标"数据不足/待核验"，不给精确但错误的数字。
**C 级数据**（看准/脉脉匿名）必须标注来源性质（`level: C级` + 来源 + 时点）。

## 2. 各文件更新指引

### levels.yml（职级对标）
- 新增公司：按 `companies:` 下现有结构添加序列与级别，附来源与时点；
- 公司调整职级体系时（如字节 2025 年调整），新增条目并注明，不删除旧条目做历史参考；
- 每条总包区间必须带时点，避免过时误导。

### salary.yml（薪资）
- 优先引用：B 级（招聘平台官方报告、企业官方校招薪资）、A 级（政府公布的平均工资/社保基数）；
- C 级数据（看准/脉脉/OfferShow 爆料）标注 `level: C级` + 时间；
- 分位数 P25/P50/P75 拿不到就写 `null`，**绝不编造**；
- 附数据来源链接（如有）。

### redflags.yml（红线规则）
- 法律类规则（劳动法、司法解释）变化频率低，但**司法解释（二）**等新规出台时需跟进（2025-09-01 已施行）；
- 反诈类规则（新骗局模式）需要持续补充——看到新型骗局可加规则；
- 新增规则必须写清 `severity` 与 `veto`（是否一票否决）。

### adjacent_roles.yml（侧翼岗位）
- 原则：只收录"现在已有真实招聘和付费"的岗位，预测类一律标 `高投机` 或不收；
- 每条岗位要有三原则论证与失效信号，避免沦为"热门岗位清单"。

### companies.yml（尽调入口与名单）
- 外包/派遣公司名单持续补充（公开信息）；注意标注"仅供参考"；
- 尽调链接模板若平台改版需更新 URL。

### interview_formats.yml（面试形式）
- 大厂流程每半年复核一次（校招季前后变化多）；
- 面经是 C 级数据，注明"以实际邀约为准"。

### followup_cadence.yml（跟进节奏）
- 变动少；如需调整直接改天数并在 meta 中说明。

## 3. 提交流程

1. 改 `data/*.yml`（更新 `last_updated`、必要时 `version`、`sources`）；
2. 本地验证 YAML 语法：
   ```bash
   python3 -c "import yaml,sys; [yaml.safe_load(open(f)) for f in ['data/levels.yml','data/salary.yml','data/redflags.yml','data/adjacent_roles.yml','data/companies.yml','data/interview_formats.yml','data/followup_cadence.yml']]; print('OK')"
   ```
3. 提交 PR，说明：改了什么、数据来源、时点、级别。

## 4. 常见坑

- YAML 里含中文冒号 `：` 或列表符号时注意缩进与引号；
- 金额统一用"万元/年"或标注单位，别混用；
- 别把匿名社区单条爆料当成普遍水平（注明是单点信息）。
