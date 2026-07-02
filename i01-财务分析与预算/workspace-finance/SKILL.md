# SKILL.md — 财务分析与预算 i01 · 技能清单

## Skill Matrix（v4.2 规范化版 · 只引不载）

> 版本：v4.2
> 更新日期：2026-06-26
> 原则：只保留财务分析、预算、现金流、合规边界直接相关 Skill。归档的通用插件类 Skill 已按养虾人要求删除。

---

## P0 核心技能（启动即用）

| 技能 | 版本 | 存放位置 | 调用场景 |
|---|---:|---|---|
| financial-statement-analysis | v1.4.0 | skills/financial-statement-analysis/ | 月度三表、R1-R7 勾稽、T+1 报表草稿 |
| budget-realtime-tracking | v1.2.0 | skills/budget-realtime-tracking/ | 预算执行、三色阈值、红色预警清单 |
| cashflow-forecast | v1.3.0 | skills/cashflow-forecast/ | 12 周现金流、乐观/中性/悲观三情景 |
| boundary-guard | v1.3.0 | skills/boundary-guard/ | 只读边界、估算拒绝、对外合规红线 |

## P1 高频专项（按需加载）

| 技能 | 版本 | 存放位置 | 调用场景 |
|---|---:|---|---|
| financial-report-writer | v1.1.0 | skills/financial-report-writer/ | 月度/季度管理报告草稿、一页式财务快照 |
| budget-draft-generator | v1.1.0 | skills/budget-draft-generator/ | 年度/季度预算草案与监控规则 |
| cost-structure-decomposition | v1.1.0 | skills/cost-structure-decomposition/ | 成本结构、费用异常、30 天成本控制动作 |
| weekly-cashflow-expansion | v1.2.0 | skills/weekly-cashflow-expansion/ | 现金流逐周展开、最低水位、字段口径验证 |
| ar-ap-cash-impact | v1.0.0 | skills/ar-ap-cash-impact/ | AR/AP/存货变化对 CFO 的方向判断 |

## P2 专项工具（低频但保留）

| 技能 | 版本 | 存放位置 | 调用场景 |
|---|---:|---|---|
| tax-inclusive-basis-conversion | v1.0.0 | skills/tax-inclusive-basis-conversion/ | 含税/不含税口径转换，PL/BS/CF 口径对齐 |
| price-volume-variance-pyramid | v1.1.0 | skills/price-volume-variance-pyramid/ | 量价分离、预算/成本偏差归因拆解 |

---

## 已删除归档 Skill

以下通用插件类 Skill 已从 `archive/skills-20260626/generic-plugin-skills/` 删除，不再保留在本 i01 工作区：

| Skill | 删除原因 |
|---|---|
| agent-browser-clawdbot | 通用浏览器自动化，非 i01 财务核心 |
| ontology | 通用知识图谱，当前财务 Eval 不需要默认加载 |
| self-improving-agent | 通用自进化 Skill，体量过大，避免默认污染 i01 |

## Skill 文件规范

每个 active Skill 应包含：

1. YAML frontmatter：`name / description / version / last_updated / priority / status / trigger`
2. `## Standard Interface`：Trigger / Inputs / Procedure / Output Format / Guardrails / Pass Criteria
3. 领域专属流程：公式、模板、异常处理、复核路径
4. Common Failures：来自 Eval 的真实失败案例
5. Change Log：重要版本变更

## 使用纪律

1. 先读本清单，再按需加载具体 Skill。
2. Skill 不等于结论；必须结合数据来源、三表勾稽、复核边界输出。
3. Eval 失败时，优先修对应 Skill 的 procedure/common_failures/pass_criteria，再重新跑 Eval。
4. 新 Skill 必须满足 2/3：重复出现、固定步骤、其他场景可复用。
5. 训练目标是会干活；Skill 是稳定流程的沉淀，不为 Skill 而 Skill。
