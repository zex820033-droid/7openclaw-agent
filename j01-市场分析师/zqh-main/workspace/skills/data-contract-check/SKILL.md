---
name: data-contract-check
description: 用于检查市场分析所需数据表字段、口径、时间窗口和缺口。
domain: [data, governance, analytics]
author: m01 市场分析师
version: 1.0.0
license: internal
trigger: 当任务输入包含用户、订单、行为、渠道或市场规模数据时调用。
---

# Data Contract Check

## 触发条件

- 开始分析前需要确认字段是否齐全。
- 数据来自多个系统。
- 口径可能不一致。

## 检查对象

- `market_size`
- `users`
- `orders`
- `events`
- `channels`
- `business_events`

## 必查项

- 日期字段。
- 币种字段。
- 地区、渠道、产品线、客户类型枚举。
- 收入、成本、毛利、订单、用户等指标口径。
- 外部数据来源、发布日期、采集日期。

## 输出

- 字段完整性检查表。
- 口径风险。
- 缺数清单。
- 最低可用估算方案。

