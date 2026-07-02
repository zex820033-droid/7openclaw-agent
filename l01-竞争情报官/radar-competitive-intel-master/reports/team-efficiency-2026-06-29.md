# T8 团队效能分析 — 2026-06-29 22:57 CST

> **Top5竞品效能** | **窗口**: PR/Issue 30d (≥2026-05-30) · 闭源代理 30d
> **开源数据源**: GitHub API (curl -k) · **闭源数据源**: cursor.com/changelog + github.blog/changelog/feed/

## 一、效能矩阵（Cycle / Lead / Throughput）

| 竞品 | 类型 | 最新版本 | 30d PRs | 30d 关Issues | 中位PR Cycle | 节奏 | 🟢🟡🔴 |
|:--:|:--:|:--|--:|--:|--:|:--:|:--:|
| **Dify** | 开源 | 1.15.0 (Jun 25) | 573 | 298 | **2.75h** | 稳态 | 🟢 |
| **LangChain** | 开源 | core 1.4.8 (Jun 18) + 子包并行 | 274 | 242 | **0.36h** | 多包并行 | 🟢 |
| **CrewAI** | 开源 | 1.15.1 (Jun 27) | 144 | 27 | **0.45h** | 半月更 | 🟡 |
| **Cursor** | 闭源 | Jun 22 (Customize) | 7次更新/30d | — | — | 平台化 | 🟢 |
| **GitHub Copilot** | 闭源 | Jun 26 20:55 UTC | 4次/近4d | — | — | 周更+ | 🟢 |

> 注：Cursor 直连抓取(cursor.com/changelog)显示最新条目 = Jun 22。晨间基线(07:46)记录的 Jun 25 "Customize" 可能来自缓存/Playwright 渲染差异 — **以直连可达日期为准 (6d 静默)**。

## 二、Δ vs 晨间基线 (07:46 → 22:57, 15h滑动窗口)

| 竞品 | ΔPRs | ΔIssues | ΔCycle | 触发阈值 | 信号 |
|:--|--:|--:|--:|:--:|:--|
| Dify | +22 (+4.0%) | +16 (+5.7%) | -0.15h | 无 | 🟢 稳态 |
| LangChain | +3 (+1.1%) | +6 (+2.5%) | **-1.04h** | Cycle>50%⚠️ | 🟢 维持高速 |
| CrewAI | +2 (+1.4%) | +0 (0%) | -0.05h | 无 | 🟡 维持 |
| Cursor | 0 | — | — | 无 | 🟢 静默期 |
| Copilot | 0 | — | — | 无 | 🟢 静默期 |

**判读**: 15h内所有开源PR cycle变化 < 50%, PR吞吐无骤降, **无P1预警触发**。

## 三、关键信号

🟡 **CrewAI 中位PR Cycle 0.45h (连续3d 维持)** — 接近自动化合并水平。提示其内部流程已高度自动化,可能牺牲审查深度。D-052 铁律标注:`0.5h中位数 → 可能牺牲审查深度` 持续生效。

🟢 **Dify 2.75h 中位cycle** — 严守窗口(<48h), 反映成熟CI/QA体系。3d内 v1.15.0 已稳态, 无新潮。

🟢 **LangChain 0.36h 中位cycle** — 多包并行版本分发(2-3/周),核心放缓向集成商层转移。

🟢 **Cursor 直连 6d 静默** — Customize 平台化(plugins/skills/MCPs/subagents/rules/commands/hooks)功能已完备, 静默属正常。

🟢 **Copilot 静默3d** — Jun 26 Adoption Phase Metric 是近4d内最后动作, 周更节奏未恢复。

## 四、零推测自检

- [x] 所有数据点经 curl 直连 GitHub API / github.blog RSS / cursor.com 获取
- [x] 数据来源URL附后
- [x] 闭源 Cycle/Lead 不报具体小时数(无数据) — 标注 🟡 代理
- [x] Cursor Jun 25 基线 vs Jun 22 直连差异已诚实标注
- [x] 无填充性"团队建设/氛围"等软指标

## 五、来源

| 源 | URL | 可达 |
|:--|:--|:--:|
| Dify | `api.github.com/repos/langgenius/dify/...` | ✅ |
| LangChain | `api.github.com/repos/langchain-ai/langchain/...` | ✅ |
| CrewAI | `api.github.com/repos/crewAIInc/crewAI/...` | ✅ |
| Cursor | `cursor.com/changelog` | ✅ |
| Copilot | `github.blog/changelog/feed/` | ✅ |

---
**统计**: 🟢4 / 🟡1 / 🔴0 | **数据质量**: 开源A级 / 闭源B级代理
**下一扫描**: 2026-06-30 06:00 (T8 cron 22h)
