# 数据字典 v1.1

## 一、通用口径

| 字段 | 类型 | 说明 |
|---|---|---|
| period | string | 会计期间，YYYY-MM |
| currency | string | 币种，本包为 CNY |
| source | string | 数据来源，本包为 synthetic_training_seed_v1 |

## 二、利润表字段

| 字段 | 口径 | 单位 |
|---|---|---|
| revenue | 主营业务收入，本月发生额 | 元 |
| cogs | 主营业务成本，本月发生额 | 元 |
| gross_profit | revenue - cogs | 元 |
| gross_margin_pct | gross_profit / revenue | % |
| opex | 销售、管理、研发等期间费用合计 | 元 |
| depreciation_amortization | 折旧摊销，本月发生额 | 元 |
| operating_profit | gross_profit - opex - depreciation_amortization | 元 |
| interest_expense | 利息支出 | 元 |
| profit_before_tax | operating_profit - interest_expense | 元 |
| income_tax | 企业所得税训练口径测算 | 元 |
| net_profit | profit_before_tax - income_tax | 元 |

## 三、资产负债表字段

| 字段 | 口径 | 单位 |
|---|---|---|
| cash | 月末货币资金 | 元 |
| accounts_receivable | 月末应收账款 | 元 |
| inventory | 月末存货/履约资源 | 元 |
| fixed_assets_net | 固定资产净额 | 元 |
| total_assets | 资产合计 | 元 |
| accounts_payable | 月末应付账款 | 元 |
| short_term_debt | 短期借款 | 元 |
| long_term_debt | 长期借款 | 元 |
| total_liabilities | 负债合计 | 元 |
| paid_in_capital | 实收资本 | 元 |
| retained_earnings | 留存收益/平衡项 | 元 |
| total_equity | 所有者权益合计 | 元 |

## 四、现金流字段

| 字段 | 口径 | 单位 |
|---|---|---|
| begin_cash | 期初现金 | 元 |
| cash_flow_from_operations | 经营活动现金流 | 元 |
| cash_flow_from_investing | 投资活动现金流 | 元 |
| cash_flow_from_financing | 筹资活动现金流 | 元 |
| net_change_in_cash | 本期现金净增加额 | 元 |
| end_cash | 期末现金 | 元 |

## 五、预算字段

| 字段 | 说明 |
|---|---|
| budget_year | 预算年度 |
| department | 责任部门 |
| budget_item | 预算项目 |
| budget_owner | 预算责任人 |
| planned_amount | 月度预算金额 |
| actual_amount | 月度执行金额 |
| variance_amount | actual_amount - planned_amount |
| variance_pct | variance_amount / planned_amount |
| variance_band | green/yellow/red，按 5%/10% 阈值判断 |
| variance_driver | 初始归因，占位后需业务证据确认 |

## 六、现金流预测字段

| 字段 | 说明 |
|---|---|
| forecast_date | 预测编制日期 |
| week_no | 未来第几周 |
| scenario | optimistic/neutral/pessimistic |
| collections | 预计回款 |
| payroll | 工资社保等刚性支出 |
| supplier_payments | 供应商付款 |
| tax_payments | 税费支出 |
| opex_payments | 日常运营付款 |
| capex_payments | 资本性支出 |
| net_cash_flow | 当周现金净流量 |
| ending_cash_projection | 单周末现金测算值 |
| key_assumption | 场景假设说明 |

## 七、注意事项

- 本包金额单位均为元。
- 利润表为期间发生额，资产负债表为月末余额。
- 预算执行只覆盖 2026-01 至 2026-05。
- 税额和留存收益为训练口径，不构成真实税务或法定报表结论。
