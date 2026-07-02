# 三表结构与勾稽关系说明 v1.1

> 目标：训练 i01 在出任何财务结论前，先证明“账是通的”。

## 一、三表定位字段

所有月度报表以以下字段定位：

| 字段 | 说明 |
|---|---|
| period | 会计期间，格式 YYYY-MM |
| currency | 币种，本包统一为 CNY |
| source | 数据来源，本包为 synthetic_training_seed_v1 |

## 二、三表核心结构

### 利润表

反映一个期间内的经营成果。训练重点不是只看净利润，而是拆出收入、成本、毛利、费用、税费之间的变化。

关键字段：revenue、cogs、gross_profit、opex、depreciation_amortization、operating_profit、interest_expense、income_tax、net_profit。

### 资产负债表

反映月末财务状况。训练重点是资产质量、负债结构和权益平衡。

关键字段：cash、accounts_receivable、inventory、fixed_assets_net、accounts_payable、short_term_debt、long_term_debt、paid_in_capital、retained_earnings。

### 现金流量表

反映现金变动。训练重点是净利润是否转化为现金、营运资金是否吃现金、投资与融资是否带来压力。

关键字段：begin_cash、cash_flow_from_operations、cash_flow_from_investing、cash_flow_from_financing、end_cash。

## 三、核心勾稽规则

| 编号 | 规则 | 公式 | 容忍度 | 失败处理 |
|---|---|---|---|---|
| R1 | 毛利 | gross_profit = revenue - cogs | 0 | 暂停利润分析 |
| R2 | 营业利润 | operating_profit = gross_profit - opex - depreciation_amortization | 0 | 检查费用归类 |
| R3 | 税前利润 | profit_before_tax = operating_profit - interest_expense | 0 | 检查利息与非经常项 |
| R4 | 净利润 | net_profit = profit_before_tax - income_tax | 0 | 检查税率和税额 |
| R5 | 资产负债表平衡 | total_assets = total_liabilities + total_equity | 0 | 熔断，不出正式结论 |
| R6 | 现金桥 | end_cash = begin_cash + CFO + CFI + CFF | 0 | 熔断，检查现金流分类 |
| R7 | 间接法 CFO | CFO = net_profit + 折旧摊销 - 应收增加 - 存货增加 + 应付增加 | 0 | 检查营运资金变动 |

## 四、管理分析指标

| 指标 | 公式 | 解释 |
|---|---|---|
| 毛利率 | gross_profit / revenue | 产品、交付与云成本效率 |
| 净利率 | net_profit / revenue | 最终盈利质量 |
| 应收收入比 | accounts_receivable / revenue | 回款压力与收入质量 |
| 存货成本比 | inventory / cogs | 交付库存或履约资源占用 |
| 应付成本比 | accounts_payable / cogs | 供应商账期与短期资金缓冲 |
| CFO/净利润 | cash_flow_from_operations / net_profit | 利润含现金量 |

## 五、异常阈值

| 异常 | 阈值 | 处理 |
|---|---|---|
| 三表勾稽差异 | 大于 0，或超过 1% | 直接熔断，先查数据 |
| 费用科目月环比 | 超过 50% | 红色预警，需归因 |
| 毛利率下滑 | 连续三月累计下滑超过 5 个百分点 | 红色预警，需拆成本 |
| 应收账款 | 应收收入比连续上升 | 回款风险预警 |
| CFO/净利润 | 连续两月低于 0.8 | 利润质量预警 |
| 现金余额 | 低于未来 8 周刚性支出 | 现金流预警 |

## 六、i01 输出模板

1. 数据来源：文件、期间、source。
2. 校验结论：R1-R7 是否通过。
3. 关键发现：毛利、费用、应收、现金流中的异常。
4. 计算过程：列公式和输入数字。
5. 复核建议：需要财务、业务、税务或审计复核什么。
6. 边界声明：训练数据、管理报表、未经审计、不可对外。
