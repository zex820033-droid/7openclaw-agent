# 模拟数据生成规范

## 使用边界

模拟数据只用于训练、演示、流程验证和模板压测。任何模拟数据输出都必须标注：

```text
数据性质：模拟数据，不代表真实业务事实。
```

## 必备数据表

### market_assumptions.csv

| 字段 | 类型 | 用途 | 真实来源 |
| --- | --- | --- | --- |
| industry | text | 行业边界 | 上岗问诊 |
| region | text | 地区边界 | 上岗问诊 |
| target_accounts | number | SAM/SOM | CRM / 工商数据库 |
| arpa | number | 收入空间 | 合同 / 财务 |
| reachable_rate | ratio | 可触达市场 | CRM / 销售触达 |
| conversion_rate | ratio | SOM | CRM 漏斗 |

### users.csv

| 字段 | 类型 | 用途 | 真实来源 |
| --- | --- | --- | --- |
| user_id | text | 用户唯一 ID | CRM / 产品 |
| last_active_days | number | RFM/R 活跃 | 产品埋点 |
| frequency | number | RFM/F 频次 | 产品/订单 |
| monetary | number | RFM/M 金额 | 订单 |
| gross_margin | ratio | 真实价值 | 财务 |
| service_cost | number | 服务成本 | 客服/交付 |
| channel | text | 渠道来源 | CRM/营销 |

### channels.csv

| 字段 | 类型 | 用途 | 真实来源 |
| --- | --- | --- | --- |
| channel | text | 渠道 | CRM |
| leads | number | 线索规模 | 营销 |
| revenue | number | 收入贡献 | 财务 |
| gross_margin | ratio | 毛利 | 财务 |
| cac | number | 获客成本 | 营销/销售 |
| discount_rate | ratio | 折扣 | 合同 |
| payback_days | number | 回款 | 财务 |
| service_hours | number | 服务成本 | 交付 |

### metrics_timeseries.csv

| 字段 | 类型 | 用途 | 真实来源 |
| --- | --- | --- | --- |
| date | date | 时间序列 | BI |
| metric | text | 指标 | BI |
| value | number | 指标值 | BI |
| segment | text | 分组 | BI |
| event_note | text | 事件 | 运营/销售/产品 |

## 生成规则

- 每个数值字段必须有合理区间。
- 至少包含 1 个异常场景。
- 至少包含 1 个收入高但利润差的渠道。
- 至少包含 1 个金额高但留存差的用户层。
- 至少包含 1 个外部资料只能做方向校准的例子。

