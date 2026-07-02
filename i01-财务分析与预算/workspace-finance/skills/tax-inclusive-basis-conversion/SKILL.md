---
name: tax-inclusive-basis-conversion
description: 处理含税/不含税口径转换，避免利润表、资产负债表、现金流量表跨口径混用。
domain: [tax, basis-conversion, reconciliation]
author: i01 财务分析与预算
version: 1.0.0
last_updated: 2026-06-26
priority: P2
status: active
trigger: 涉及增值税、含税收入、应收应付、回款付款、PL/BS/CF 口径对齐时触发。
---

# Tax Inclusive Basis Conversion — 含税口径转换

## Standard Interface

### Trigger
含税/不含税口径转换，PL/BS/CF 口径对齐。

### Inputs
- PL 不含税金额
- BS/CF 含税金额
- 税率
- 发票/回款口径

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

## Core Principle

- 利润表收入/成本通常是不含税口径。
- 资产负债表应收/应付通常是含税发票价。
- 现金流收/付款是含税实收实付。

## Procedure

1. 先标注每个字段是否含税。
2. 用税率将 PL 口径转为 BS/CF 可比口径。
3. 再做 AR/AP、回款/付款推导。
4. 输出时声明税率和口径。

## Common Failures

- 用不含税收入直接和含税应收比较。
- 未说明税率。
- 把税务测算当正式申报。
