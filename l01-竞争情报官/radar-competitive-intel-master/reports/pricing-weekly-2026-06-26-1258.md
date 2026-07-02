# 🧊 T3 定价追踪 — 2026-06-26 12:58 CST（周五·降频扫描·零增量）

> **类型**: 非周一降频扫描（距上次扫描 38 分钟）
> **状态**: 🧊 连续第 12 周定价全面冻结
> **扫描**: 6/6 可达页均 [直接抓取] 验证 · **价格变化 0/6**
> **决策**: 跳过周报正文（与 12:20 / 09:50 三次扫描结果完全一致）·仅记录扫描事件

---

## 本轮扫描事件记录

| 时间 | 竞品 | 抓取 | 价格点核对 | 结果 |
|:----:|:----:|:----:|:---------|:----:|
| 12:58 | DeepSeek | api-docs.deepseek.com/quick_start/pricing | V4-Flash $0.14/$0.28 (cache $0.0028) + V4-Pro $0.435/$0.87 (cache $0.003625) + 并发 2500/500 | ✅ 无变化 |
| 12:58 | Dify | dify.ai/pricing | Sandbox Free / Pro $59 / Team $159 (published Jun 25 09:00 UTC) | ✅ 无变化 |
| 12:58 | LangSmith | langchain.com/pricing | Developer $0 / Plus $39/seat / Enterprise Custom + Eng $1.50/LCU + Sandbox $0.0576/vCPU-hr | ✅ 无变化 |
| 12:58 | Cohere | cohere.com/pricing | Embed 4 Small $4 / Medium $5 + Rerank 3.5 $5 + Rerank 4 Fast $5 + Rerank 4 Pro Medium $5 + Large $10 | ✅ 无变化 |
| 12:58 | Runway | runwayml.com/pricing | Free $0(125credits) / Standard $12 / Pro $28 / Max $76（年付）/ Enterprise Custom | ✅ 无变化 |
| 12:58 | CrewAI | crewai.com/pricing | Basic Free(50 wf/mo) + Enterprise Custom | ✅ 无变化 |

## 三次扫描一致性核对

| 维度 | 09:50 | 12:20 | 12:58 | 结论 |
|:-----|:-----:|:-----:|:-----:|:----:|
| 价格变化数 | 0/6 | 0/6 | 0/6 | 完全冻结 |
| 新增信号 | 0 | 0 | 0 | 无信号 |
| DeepSeek deprecated | ✓ | ✓ | ✓ | S2 持续 |
| 定价差距 | 214-357x | 214-357x | 214-357x | 未缩窄 |

## 决策说明

**不生成新周报正文**——理由：
1. 距上次扫描仅 38 分钟（cron 2h/次频率外的额外触发）
2. 6/6 价格数据点与历史完全一致，零增量
3. 周五非 T3 周报生成日（周一全量 + 周内降频）
4. 避免污染 `reports/` 目录（今日已有 09:50 + 12:20 两份等价报告）

**本次产出仅为**：
- `data/pricing-tracker.json` 更新（last_checked 时间戳 + scan_summary.notes）
- 本事件记录文档（审计追踪）

## 持续关注信号（沿用 12:20 报告，无新增）

| 信号 | 等级 | 说明 | 倒计时 |
|:----:|:----:|------|:------:|
| DeepSeek 模型弃用 | ⚠️ S2 | deepseek-chat+reasoner → 2026/07/24 15:59 UTC 弃用 | **28 天** |
| 定价差距固化 | S3 | GPT-5.5 vs DeepSeek = 214-357x 倍差 | 12 周未缩窄 |
| MiniMax 平台可访问 | 🟡 | platform.minimax.io 已恢复（pricing SPA 404 仍未穿透） | — |

## 下次扫描

**next_scan**: 2026-06-29 08:00 CST（周一全量扫描）
**本次触发原因**: cron 频率从 30min → 2h 调整后的额外触发（可能为冷启动/重连）

---

🦞 **本次扫描未发现任何战略级信号。定价市场进入深度冻结期。**
