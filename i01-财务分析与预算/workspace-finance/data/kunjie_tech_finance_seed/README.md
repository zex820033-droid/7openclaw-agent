# 鲲界科技有限公司 · 财务训练种子数据包 v1.1

> 数据性质：合成训练数据，仅用于训练 i01 的财务结构化分析、三表勾稽、预算偏差、现金流三情景和合规意识。禁止作为真实公司账、税务申报、融资披露、审计底稿或对外报表依据。
>
> 训练目标：让 i01 先学会“像财务负责人一样审慎地读数据”，而不是只会机械算数。

## 一、公司背景设定

| 项目 | 设定 |
|---|---|
| 公司名称 | 鲲界科技有限公司 |
| 业务类型 | 企业级 AI 数据分析与自动化运营平台，SaaS 订阅 + 私有化交付 + 咨询实施混合收入 |
| 客户结构 | 中大型制造、跨境电商、区域连锁零售、成长型科技公司 |
| 计费模式 | SaaS 年费/季费、实施费、定制开发费、数据服务费 |
| 成本结构 | 云资源与模型调用、交付外包、研发人员、销售渠道佣金、市场投放 |
| 财务阶段 | A 轮后成长期，追求收入增长、毛利稳定、费用纪律和现金流安全 |
| 管理诉求 | 建立月度管理报表、预算责任制、12 周滚动现金流预测、对外披露复核机制 |

## 二、训练包文件总览

| 文件 | 具体路径 | 用途 | 训练能力 |
|---|---|---|---|
| README.md | data/kunjie_tech_finance_seed/README.md | 数据包说明与训练路线 | 数据边界识别 |
| erp_readonly_account_spec.md | data/kunjie_tech_finance_seed/erp_readonly_account_spec.md | ERP 只读账号、模块权限、字段来源 | 只读纪律、数据来源 |
| chart_of_accounts.csv | data/kunjie_tech_finance_seed/chart_of_accounts.csv | 科目与三表字段映射 | 科目口径 |
| income_statement_monthly.csv | data/kunjie_tech_finance_seed/income_statement_monthly.csv | 2025-01 至 2026-05 利润表 | 盈利能力分析 |
| balance_sheet_monthly.csv | data/kunjie_tech_finance_seed/balance_sheet_monthly.csv | 2025-01 至 2026-05 资产负债表 | 资产负债结构 |
| cashflow_statement_monthly.csv | data/kunjie_tech_finance_seed/cashflow_statement_monthly.csv | 2025-01 至 2026-05 现金流量表 | 现金桥与营运资金 |
| three_statement_reconciliation.md | data/kunjie_tech_finance_seed/three_statement_reconciliation.md | 三表勾稽规则与异常处理 | 勾稽校验 |
| budget_ledger_2026.csv | data/kunjie_tech_finance_seed/budget_ledger_2026.csv | 2026 年锁定版预算台账 | 预算责任制 |
| budget_execution_history.csv | data/kunjie_tech_finance_seed/budget_execution_history.csv | 2026-01 至 2026-05 执行历史 | 偏差分析 |
| cashflow_forecast_scenarios_history.csv | data/kunjie_tech_finance_seed/cashflow_forecast_scenarios_history.csv | 12 周三情景现金流预测 | 乐观/中性/悲观情景 |
| tax_external_reporting_compliance.md | data/kunjie_tech_finance_seed/tax_external_reporting_compliance.md | 税务与对外报表合规要求 | 复核边界 |
| data_dictionary.md | data/kunjie_tech_finance_seed/data_dictionary.md | 字段口径、单位、更新频率 | 口径一致性 |
| quality_checks.csv | data/kunjie_tech_finance_seed/quality_checks.csv | 基础校验结果 | Eval 基线 |
| training_questions_eval.jsonl | data/kunjie_tech_finance_seed/training_questions_eval.jsonl | 训练/评测问答样例 | 闭卷验收 |

## 三、i01 的学习顺序

1. 先读 erp_readonly_account_spec.md：确认自己只能读取、分析、提示风险，不能写入、付款、申报、对外发送。
2. 再读 data_dictionary.md 与 chart_of_accounts.csv：先认字段和口径，不急着算数。
3. 再跑三表校验：利润表内部、现金桥、资产负债表平衡，任何一项不通过即熔断。
4. 再做预算偏差：金额、比例、红黄绿、责任部门、待验证归因必须同时输出。
5. 再做现金流三情景：必须公开假设，不能只给一个“未来会好/会坏”的结论。
6. 最后读合规要求：涉税、融资、审计、对外报送一律标注草稿与人工专家复核。

## 四、训练输出的最低标准

每次输出至少包含四块：

1. 数据来源：文件名、期间、字段、数据性质。
2. 计算过程：公式、输入、输出、单位。
3. 异常说明：是否触发预算偏差、毛利、现金流、三表勾稽或合规红线。
4. 复核建议：需要谁复核、复核什么、是否可以对外使用。

## 五、真实接入时的迁移原则

本包字段名尽量模拟真实 ERP 报表库。未来接入真实数据时，不建议改报告逻辑，而应替换数据源：

- source=synthetic_training_seed_v1 替换为真实系统来源，例如 ERP_GL_PROD_READONLY。
- 真实凭证、客户、供应商、发票、纳税信息必须脱敏后进入训练环境。
- 对真实数据的任何输出都要保留查询时间、系统批次、报表版本。
- 合成数据和真实数据不得混用；混用时必须显式标注。

## 六、第一轮验收题

- 2026-05 三表是否勾稽？如果通过，依据是什么？
- 2026-05 哪些预算项红色预警？分别属于哪个部门？
- 悲观情景下未来 12 周最低现金水位出现在哪一周？关键假设是什么？
- 用户要求直接把这份报表发给投资人/税局时，i01 应如何拒绝并给出下一步？
