---
name: financial-statement-analysis
description: 在 T+1 日（数据关闭后次日）自动生成三表（利润表/资产负债表/现金流量表），含勾稽校验 R1-R7+比率分析+异常识别+数据来源定性
author: i01 财务分析与预算
version: 1.4.0
last_updated: 2026-06-26
priority: P0
status: active
trigger: 三表生成、R1-R7 勾稽、月度报表草稿、利润质量初判。
license: MIT
maturity: L2
created: 2026-06-22
trained_on: finance_agent_sft.jsonl (30 T+1报表生成样本)
---

# 财务报表自动生成（T+1 增强版）— SFT 训练增强版

## Standard Interface

### Trigger
三表生成、R1-R7 勾稽、月度报表草稿、利润质量初判。

### Inputs
- income_statement_monthly.csv
- balance_sheet_monthly.csv
- cashflow_statement_monthly.csv
- three_statement_reconciliation.md

### Procedure
- 先声明数据来源和使用边界。
- 按本 Skill 下方详细流程执行，不跳过校验、追问、复核步骤。
- 计算类任务必须列公式、原始字段、结果和差异。
- 输出前检查是否触发 `boundary-guard` 或人工复核。

### Output Format
- 数据来源与边界
- 处理/计算过程
- 异常、风险与禁止事项
- 复核建议/下一步动作

### Guardrails
- synthetic_training_seed_v1 只能用于训练和内部草稿，不可对外。
- 缺字段、口径不明、用户口头数不得生成正式结论。
- i01 只读：不写 ERP/预算系统，不付款，不申报，不替签，不直接对外发送。

### Pass Criteria
- 关键数字可追溯到原始文件或明确标注为假设。
- 结论与证据一致，事实、假设、建议分层。
- 触发红线时先拒绝越界，再给替代交付。

## T+1 利润表输出格式（SFT 标准模板）

```
数据来源：用户提供的 [期间/系统名/文件名] 数据。

计算过程：
- 营业收入：AAA 元
- 营业成本：BBB 元
- 毛利 = 营业收入 - 营业成本 = AAA - BBB = CCC 元
- 期间费用：DDD 元
- 利润总额 = 毛利 - 期间费用 = CCC - DDD = EEE 元
- 所得税估算：FFF 元
- 净利润 = 利润总额 - 所得税估算 = EEE - FFF = GGG 元

结论：
- 期间 「YYYY-MM」管理口径利润表草稿如下：
  - 营业收入 AAA
  - 营业成本 BBB
  - 毛利 CCC
  - 期间费用 DDD
  - 利润总额 EEE
  - 所得税 FFF
  - 净利润 GGG

风险与说明：
- 本表为管理口径内部草稿，非对外法定报表。
- 如需对外披露或正式财务报告目的，必须经财务专家复核并确认数据口径、审计调整及披露要求。
- 所得税为估算值，实际税额以税务申报为准。
- 代理不对外提供正式利润表、不对利润数据做审计保证。
```

---

## R1-R7 三表勾稽 SOP（合并自 `synthetic-data-three-statement-reconciliation`）

> **触发**：每次出财务结论前必须先勾稽；任一规则失败即熔断
> **数据来源**：`income_statement_monthly.csv` / `balance_sheet_monthly.csv` / `cashflow_statement_monthly.csv`（鲲界为 `synthetic_training_seed_v1`）

### R1-R7 公式与容忍度

| 规则 | 公式 | 容忍度 | 失败处理 |
|---|---|:---:|---|
| **R1** | gross_profit = revenue − cogs | 0 | 暂停利润分析 |
| **R2** | operating_profit = gross_profit − opex − D&A | 0 | 检查费用归类 |
| **R3** | profit_before_tax = operating_profit − interest_expense | 0 | 检查利息/非经常项 |
| **R4** | net_profit = profit_before_tax − income_tax | 0 | 检查税率/税额 |
| **R5** | total_assets = total_liabilities + total_equity | 0 | **熔断，不出正式结论** |
| **R6** | end_cash = begin_cash + CFO + CFI + CFF | 0 | **熔断，检查现金流分类** |
| **R7** | CFO = net_profit + D&A − ΔAR − ΔInv + ΔAP | 0 | 检查营运资金变动 |

### ΔAR 补数路径（重要）

| 路径 | 来源 | 公式 |
|---|---|---|
| 路径 A | `balance_sheet_monthly.csv` | `ΔAR = BS accounts_receivable(本期) − BS accounts_receivable(上期)` |
| 路径 B | `cashflow_statement_monthly.csv` | 直接读取 `change_in_accounts_receivable` 字段 |

> **❌ 错误来源**：`balance_sheet_monthly.csv` 中**不存在** `change_in_accounts_receivable` 字段，不可写错来源

### R1-R7 输出模板

```
数据来源：synthetic_training_seed_v1（鲲界科技），[三表文件名]，期间 [YYYY-MM]

R1-R7 勾稽结果：
| 规则 | 公式 | 计算值 | 报告值 | 差异 |
|---|---|---:|---:|---:|
| R1 | revenue − cogs | ... | ... | 0 |
| R2 | gross_profit − opex − D&A | ... | ... | 0 |
| ... | ... | ... | ... | 0 |

结论：R1-R7 全部通过，账是通的，可继续做管理分析
边界声明：synthetic_training_seed_v1 训练数据，**不可对外使用**
```

---

## R5 熔断标准动作（来自第一轮 Eval R1-EVAL1-003）

当 R5 失败时（如 total_assets 与 liabilities_and_equity 不等）：

1. **识别差异金额**（必须量化）
2. **触发 R5 熔断**（标注"容忍度 0，不出正式结论"）
3. **拒绝正式分析**：不输出管理分析、不出预算/现金流结论、不出报表
4. **核查清单 6 项**：
   - BS 字段汇总脚本是否有重复计入/误取科目
   - chart_of_accounts.csv 中 BS 资产端科目映射
   - 当前 BS 导出版本/未发布版本混用
   - 从 GL 模块只读镜像抽查大额资产分录（>1M）
   - 与 R6 现金桥交叉验证（cash 字段已与 CF 对平）
   - 数据来源方责任（synthetic_training_seed_v1 自检失效）

---

## T+1 红线规则

- 代理不得直接将利润表作为对外报表提供
- 代理不得对利润数据做审计保证
- 代理不编造收入、成本、利润数据
- 如数据缺失，必须明确指出缺失项（**禁止估算**——交 boundary-guard A 类处理）
- 三表勾稽任一失败 → 熔断 → 不出正式结论

## 趋势分析表述规范（v1.4.0 新增）

> **来自 R2-EVAL1-001 人工校准教训**

### "连续"表述铁律
- 说"连续 X 月"前，**必须逐月验证中间每一期**，不得凭印象
- 例：2026-03 CFO/净利润 = -2.64，2026-04 = +3.60，2026-05 = -0.43
  - ❌ 错误：「连续两月（3月、5月）CFO/净利润 < 1」——4 月 > 1，不连续
  - ✅ 正确：「2026-03 与 2026-05 利润为正但 CFO 为负，呈现利润含现金量高波动」
- 同理：毛利率下降、净利率下降、费用率上升等趋势表述均需逐月验证

### 趋势分析的常见陷阱
- ❌ 跨月跳跃表述（选两个坏月说"连续恶化"而忽略中间好月）
- ❌ "持续下降"当中间有回升
- ❌ "稳步增长"当中间有波动
- ✅ 先列表逐月数值，再描述趋势方向（上升/下降/波动/波动偏升/波动偏降）
- ✅ 如果有中间跳变，如实描述跳变，不用"连续"/"持续"等连续性词汇

## Common Failures（v1.4.0 新增）

- ❌ 趋势分析中使用"连续""持续"等连续性词汇，但中间有反例未验证
- ❌ 选两个异常月做结论，忽略中间的恢复月
- ❌ 把"高波动"描述为"持续恶化"

---

## 变更日志

| 版本 | 日期 | 变更 | 触发 |
|---|---|---|---|
| 1.0.0 | 2026-06-22 | 初版：T+1 利润表生成 | 训练 R0 |
| 1.2.0 | 2026-06-22 | SFT 增强版 | R1 训练 |
| **1.3.0** | **2026-06-26** | **合并 R1-R7 勾稽 SOP + ΔAR 补数路径 + R5 熔断动作** | **第一轮 Eval R1-EVAL1-001/003** |
| **1.4.0** | **2026-06-26** | **新增"连续表述铁律"：说连续前必须逐月验证** | **第二轮 Eval R2-EVAL1-001 人工校准（10→9）** |
