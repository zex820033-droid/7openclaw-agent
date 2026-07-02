# 市场分析师专家虾工作区

本工作区用于训练、维护和复制 `m01 市场分析师` 专家虾。项目结构已按《蓝血军团-最佳实践手册》和《硅基生命训练学》整理。

## 核心职责

- TAM/SAM/SOM 测算：基于行业报告、财报、公司经营数据估算市场空间，并按季度刷新。
- 用户分层分析：基于 RFM、行为、交易和生命周期数据输出高价值用户画像。
- 细分赛道机会评估：按规模、增速、利润空间、竞争密度和能力匹配评分排序。
- 渠道结构分析：比较各销售渠道的容量、价格带、利润空间和转化效率。
- 月度市场简报：汇总市场变化、用户行为变化、渠道变化、竞品动态、机会和风险。
- 异常检测：市场份额、客单价、转化率、毛利率、渠道 ROI 等指标突变时告警。

## 标准结构

| 路径 | 作用 |
| --- | --- |
| `agents/m01/` | 市场分析师专家虾标准 7 件套 |
| `SHARED/` | 全局共享 USER、TOOLS、组织级知识入口 |
| `workspace/skills/` | 共享 Skill 库，所有技能集中存放 |
| `workspace/training/` | 可复用训练场、案例库、评分表和结业考核 |
| `references/` | 两本手册和训练体系参考资料 |
| `governance/` | 任务卡、三证验真、整改单、军功簿、周检、回归测试 |
| `project1/` | m01 训练手册和复制上岗说明 |
| `knowledge/` | 市场分析师长期业务知识 |
| `memory/` | 项目级长期记忆 |
| `templates/` | 角色和 Skill 模板 |
| `archive/v0-draft/` | 第一版草稿归档 |

## 专家虾 7 件套

`agents/m01/` 必须且只能包含：

- `README.md`
- `SOUL.md`
- `AGENTS.md`
- `SKILL.md`
- `HEARTBEAT.md`
- `MEMORY.md`
- `EVOLUTION.md`

## 关键入口

- 角色总览：[agents/m01/README.md](agents/m01/README.md)
- 技能索引：[workspace/skills/skills-index.md](workspace/skills/skills-index.md)
- 1 天速成训练场：[workspace/training/one-day-bootcamp/README.md](workspace/training/one-day-bootcamp/README.md)
- Day 2 口径校准训练：[workspace/training/day-02-calibration/README.md](workspace/training/day-02-calibration/README.md)
- Day 3 外部研究训练：[workspace/training/day-03-external-research/README.md](workspace/training/day-03-external-research/README.md)
- Day 4 人格铸造训练：[workspace/training/day-04-persona-forging/README.md](workspace/training/day-04-persona-forging/README.md)
- Day 5 复制上岗训练：[workspace/training/day-05-replication-onboarding/README.md](workspace/training/day-05-replication-onboarding/README.md)
- 训练手册：[project1/m01-市场分析师-训练手册.md](project1/m01-市场分析师-训练手册.md)
- 复制上岗：[project1/m01-复制上岗说明.md](project1/m01-复制上岗说明.md)
- 任务卡：[governance/task-card.md](governance/task-card.md)
- 回归测试：[governance/regression-tests.md](governance/regression-tests.md)

## 参考资料

- [references/蓝血军团-最佳实践手册.md](references/蓝血军团-最佳实践手册.md)
- [references/silicon-life-handbook/](references/silicon-life-handbook/)

## 复制方式

复制本工作区后，至少替换：

1. `agents/m01/` 中的角色定位、行业边界、指标口径和心跳阈值。
2. `workspace/skills/` 中的行业专属技能。
3. `knowledge/` 中的公司、产品、客户、渠道和竞品知识。
4. `memory/MEMORY.md` 中的目标行业、地区、币种和数据源。
5. `governance/` 中的验收人、任务卡字段和军功簿规则。

## 快速训练

需要把一只新复制的市场分析师快速压测到可上岗雏形时，执行：

1. 读取 `workspace/training/one-day-bootcamp/day-schedule.md`。
2. 使用 `workspace/training/one-day-bootcamp/datasets/bootcamp-market-data.csv` 完成六大任务。
3. 完成 `workspace/training/one-day-bootcamp/cases/adversarial-cases.md` 的 8 个对抗案例。
4. 完成 `workspace/training/one-day-bootcamp/final-exam.md`。
5. 使用 `workspace/training/one-day-bootcamp/scorecard.md` 评分，低于 80 分必须返工。

第一天通过后，执行 `workspace/training/day-02-calibration/`，把训练重点从“完整交付”推进到“真实口径校准、预测复盘和渠道利润审计”。

第二天通过后，执行 `workspace/training/day-03-external-research/`，把训练重点推进到“外部资料分级、竞品压测、证据冲突处理和机会评分修正”。

第三天通过后，执行 `workspace/training/day-04-persona-forging/`，把训练重点推进到“命名、人格锚点、战场记忆、标准表达和高压对话稳定性”。

第四天通过后，执行 `workspace/training/day-05-replication-onboarding/`，把训练重点推进到“复制上岗、行业适配、模拟数据边界、首周任务和认证标准”。
