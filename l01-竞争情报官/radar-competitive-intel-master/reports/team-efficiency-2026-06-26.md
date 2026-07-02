# T8 团队效能分析 — 2026-06-26

> 🟢开源(GitHub API) · 🟡闭源(Changelog/RSS) · 采集 22:57 CST

## 🚨 P1

| 竞品 | 变化 | 详情 |
|:----:|------|------|
| **CrewAI** | 🆕 **v1.15.0 stable** (Jun 25 23:17 UTC) | α迭代终结→稳定版。距v1.14.7仅14d。0.7h极速PR cycle |
| **Dify** | v1.15.0 (Jun 25 13:16) | 距今33h。difyctl CLI alpha+Agent-v2内联App。37d重大版本节奏 |
| **LangChain** | langchain-fireworks 1.4.3 (Jun 26 06:52) | 14h前。core 1.4.8仍最新主版本(8d) |

## 🟢 开源竞品

| 竞品 | 最新 Release | 距今 | Median PR Cycle | Merged PRs 30d | Closed Issues 30d | 信号 |
|------|------|:--:|:--:|:--:|:--:|:--:|
| **Dify** | v1.15.0 | 33h | 2.9h | 585 | 293 | S2 |
| **LangChain** | langchain-fireworks 1.4.3 | 14h | 1.5h | 285 | 241 | S2 |
| **CrewAI** | 🆕 **v1.15.0** | 24h | **0.7h** | 143 | 28 | S2↑ |

- **Dify**: v1.15.0稳定+difyctl v0.1.0-alpha(darwin-arm64+checksums,下载27次/二进制)·37d蓄力终结·维持S2
- **LangChain**: 14h前fireworks 1.4.3(vcrpy 8.2.1+langsmith 0.8.18+mypy 2.1)·多包并行·维持S2
- **CrewAI** 🆕: v1.15.0 immutable稳定版→α3→α4→α5→stable共7d·距v1.14.7仅14d(月更→半月更)·变更含声明式flow+DMN模式+符号链接路径遍历修复+StateProxy移除+crewai run/flow kickoff合并·0.7h PR cycle行业顶配·**S2→S2(强)**

## 🟡 闭源竞品

| 竞品 | 最新更新 | 距今 | 趋势 |
|------|---------|:--:|------|
| **Cursor** | Jun 25 Customize页面 | 1d | → 平台化深化 |
| **Copilot** | 🆕 Jun 25 21:41 Code Review效率 | 1h | ↑ 三日连击 |

- **Cursor**: 无新Changelog(Customize仍为最新)·plugins/skills/MCPs/subagents/rules/commands/hooks统一管理+Marketplace排行榜+团队市场(GitLab/BitBucket/Azure DevOps导入)
- **Copilot** 🆕: code review用CLI/SDK内置文件探索工具→成本效率提升·CLI GA(Jun 23)+Auto选模(Jun 24)+Code Review效率(Jun 25)三日连击

## 🔄 vs 06-25基线

| 竞品 | 06-25基线 | 06-26今日 | 变化 | 预警 |
|:----:|:----:|:----:|:----:|:----:|
| Dify | v1.15.0 | 同上 | → 稳态 | — |
| LangChain | openrouter 0.2.4 | 🆕 fireworks 1.4.3 | ↑ 多包并行 | — |
| CrewAI | α5 (pre) | 🆕 **v1.15.0 stable** | ↑↑ pre→stable | **P1** |
| Cursor | Customize | 同上 | → 持续 | — |
| Copilot | Auto选模 | 🆕 Code Review效率 | ↑ 续行 | — |

## 预警池

| 级别 | 信号 | 状态 |
|:----:|------|:----:|
| P1 | 🆕 CrewAI v1.15.0—半月更节奏·0.7h cycle·企业特性集 | 🆕 |
| P1 | Dify v1.15.0(昨日已报) | 持续 |
| P2 | LangChain core 8d无新 | 持续 |
| P2 | Copilot三日连击(CLI+Auto+Review) | 持续 |
| P3 | Cursor Customize—持续无新 | 持续 |

---
🐦 竞争情报在此

---

## 【Skill调用报告】
- 加载文件：`skills/executive-dashboard/SKILL.md` (10.7KB)
- 实际使用的规则/模板：
  - Dashboard Design Principles (Strategic Alignment / Limited / Actionable)
  - KPI Categories (Operational: Cycle Time / Throughput)
  - Traffic Light System (🟢/🟡/🔴) — 数据质量标注
  - Alerts & Exceptions 表格模板
  - Period Comparison 表格 (vs 06-25基线)
- 不适用的规则：
  - Financial / Customer / People / Growth KPI类别 — T8 专注团队效能，其他类不适用
  - 趋势可视化 ASCII chart — ≤400字约束下，仅保留关键数字
  - KPI Definitions 大表 — T8 是动态竞品追踪，竞品即"KPI对象"
- 调用评分自检：□3=正确加载且使用 ✓
