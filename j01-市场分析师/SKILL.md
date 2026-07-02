# 周启衡 · 市场分析师 SKILL

## 模式说明

本文件是技能清单，不是技能正文。

- 清单：说明什么场景调用什么技能。
- 内容：实际技能在 `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/<skill-name>/SKILL.md` 中。
- 原则：只引不载，按需读取，避免把所有技能塞进角色文件。
- 身份：周启衡调用技能时，仍保持“口径、证据、边界、动作”的专家表达；人格内容不写入技能正文。

## 九技能完整清单

周启衡当前标准技能数：9 个。

| Skill | 类型 |
| --- | --- |
| market-sizing | 核心 |
| market-briefing | 核心 |
| anomaly-detection | 核心 |
| user-segmentation | 核心 |
| opportunity-scoring | 核心 |
| channel-analysis | 核心 |
| evidence-review | 支撑 |
| data-contract-check | 支撑 |
| market-research-synthesis | 支撑 |

调用纪律：核心 Skill 负责产出，支撑 Skill 负责防错。凡涉及数据字段、外部资料、关键数字、预算或战略判断，不得只调用核心 Skill，必须叠加对应支撑 Skill。

## 前置读取纪律（2026-06-30 新增）

执行任何任务前，先按 AGENTS.md 中的"Skill 文件前置读取规则"判断是否需要 `read` 对应 Skill 文件。不得仅凭记忆运行。

| 触发场景 | 必须前置 read 的 Skill |
| --- | --- |
| 外部报告/竞品/公开资料 | market-research-synthesis |
| 关键结论进入预算/战略 | evidence-review |
| 表格/字段/CRM/订单数据 | data-contract-check |
| TAM/SAM/SOM 测算 | market-sizing |
| 渠道预算/利润判断 | channel-analysis |
| 指标突变/异常告警 | anomaly-detection |
| 用户分层/画像 | user-segmentation |
| 赛道机会排序 | opportunity-scoring |
| 月度市场简报 | market-briefing |

## P0 启动即用技能

| Skill | 路径 | 调用场景 |
| --- | --- | --- |
| market-sizing | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/market-sizingSKILL.md` | TAM/SAM/SOM 测算、季度刷新 |
| market-briefing | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/market-briefing/SKILL.md` | 月度市场简报、经营会输入 |
| anomaly-detection | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/anomaly-detection/SKILL.md` | 指标突变、异常告警 |

## P1 高频技能

| Skill | 路径 | 调用场景 |
| --- | --- | --- |
| user-segmentation | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/user-segmentationSKILL.md` | RFM、行为聚类、高价值用户画像 |
| opportunity-scoring | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/opportunity-scoring/SKILL.md` | 细分赛道评分、机会排序 |
| channel-analysis | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/channel-analysis/SKILL.md` | 渠道容量、价格带、利润空间对比 |

## P2 按需技能

| Skill | 路径 | 调用场景 |
| --- | --- | --- |
| evidence-review | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/evidence-review/SKILL.md` | 检查来源、三证验真、报告可信度 |
| data-contract-check | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/data-contract-check/SKILL.md` | 检查数据字段、口径、缺口 |
| market-research-synthesis | `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/market-research-synthesis/SKILL.md` | 综合外部报告、竞品信号和访谈材料 |

## 训练蒸馏索引

即使无法读取 `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/training`，周启衡也必须记住以下已训练能力：

| 能力 | 运行时动作 |
| --- | --- |
| 六大核心任务 | 市场空间、用户分层、机会评分、渠道分析、月报、异常检测可独立闭环 |
| 真实口径校准 | 缺数据时拆字段、来源、用途、频率和缺失替代 |
| 外部研究压测 | 公开资料分级，竞品包含直接竞品、平台、系统内置、人工替代、不作为 |
| 专家人格稳定 | 用周启衡式表达保持口径、证据、边界、动作 |
| 复制上岗 | 先问诊、再适配、再使用真实/公开/半真实/模拟数据 |

## 复制上岗模板记忆

复制到新行业时至少适配：

- B2B SaaS / AI 工具：ARR、ARPA、MQL-SQL、试点转付费、NRR。
- 消费品 / 零售：GMV、毛利、复购、客单价、库存周转、退货。
- 制造业 AI：上线周期、定制占比、设备效率、良率、试点转付费。
- 本地生活：商家数、核销率、补贴 ROI、商家流失。
- 跨境电商：GMV、广告 ROI、库存周转、退款率、地区/品类机会。

## Work-to-Skill 机制

任务完成后，若满足以下任意两条，必须评估是否沉淀为 Skill：

- 同类任务预计每月至少重复 2 次。
- 已形成稳定步骤、模板或评分规则。
- 其他 Agent 也可能复用。
- 本次任务出现可复用的踩坑记录。

新增 Skill 时：

1. 在 `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/<skill-name>/SKILL.md` 创建技能正文。
2. 更新 `.openclaw/workspace/十二虾/j01-市场分析师/zqh-main/workspace/skills/skills-index.md`。
3. 在本文件添加索引。
4. 在 `EVOLUTION.md` 记录技能基因。
