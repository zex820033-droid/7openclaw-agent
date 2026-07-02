---
name: ar-ap-cash-impact
description: 判断应收、应付、存货、预收预付等营运资金变化对经营现金流的方向影响。
domain: [cashflow, working-capital]
author: i01 财务分析与预算
version: 1.0.0
last_updated: 2026-06-26
priority: P1
status: active
trigger: 做间接法 CFO、现金流桥、AR/AP 变动解释时触发。
---

# AR/AP Cash Impact — 营运资金方向直觉

## Standard Interface

### Trigger
AR/AP/存货变化对 CFO 的方向判断和间接法解释。

### Inputs
- BS 两期 AR/AP/Inventory
- CF 变动字段
- net_profit
- D&A

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

## Rules

| 科目变动 | 现金影响 |
|---|---|
| 应收增加 | 现金减少 |
| 应收减少 | 现金增加 |
| 存货增加 | 现金减少 |
| 存货减少 | 现金增加 |
| 应付增加 | 现金增加 |
| 应付减少 | 现金减少 |
| 预付增加 | 现金减少 |
| 预付减少 | 现金增加 |
| 预收增加 | 现金增加 |
| 预收减少 | 现金减少 |

## CFO Formula

CFO = net_profit + depreciation_amortization - ΔAR - ΔInventory + ΔAP

## Common Failures

- 把 AR 增加误判为现金增加。
- 说 balance_sheet_monthly.csv 内有 change_in_accounts_receivable 字段；正确做法是两期 AR 相减，或读现金流表字段。
