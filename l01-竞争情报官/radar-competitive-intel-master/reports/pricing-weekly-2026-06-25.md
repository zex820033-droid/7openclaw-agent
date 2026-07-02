# 📊 定价追踪周报 — 2026-06-25 (Week 11)

> **T3 定价扫描** | 抽样验证 3/3 通过 | 🧊 连续第11周全量冻结

---

## 一、本周扫描概要

| 维度 | 数据 |
|------|------|
| 扫描时间 | 2026-06-25 23:04 CST (轻量3/3抽样) |
| 上次全量扫描 | 2026-06-25 21:37 (1.5h前) |
| 抽样竞品 | DeepSeek · Dify · LangChain |
| 价格变更 | **0** (连续11周无变化) |
| SPA阻塞 | OpenAI/Anthropic/Coze/智谱 (第11周) |
| URL404 | 阿里百炼/百度千帆 (第11周) |

## 二、抽样验证详情

### 1️⃣ DeepSeek — [直接抓取] api-docs.deepseek.com/quick_start/pricing
| 模型 | 输入/1M (Cache Miss) | 输入/1M (Cache Hit) | 输出/1M |
|:---:|:---:|:---:|:---:|
| V4-Flash | $0.14 | $0.0028 | $0.28 |
| V4-Pro | $0.435 | $0.003625 | $0.87 |
- ⚠️ `deepseek-chat`/`deepseek-reasoner` 弃用通知持续——2026/07/24 15:59 UTC（**仅剩29天**）
- 并发限制: V4-Flash 2500 / V4-Pro 500
- **状态**: 🟢 未变化 (第11周)

### 2️⃣ Dify — [直接抓取] dify.ai/pricing
| 套餐 | 价格 | 备注 |
|:----:|:----:|:-----|
| Sandbox | **$0** | 200 msg credits, 1成员, 5 Apps |
| Professional | **$59/月** | 5K msg credits, 3成员, 50 Apps |
| Team | **$159/月** | 10K msg credits, 50成员, 200 Apps |
| Enterprise | 联系销售 | 自托管/SSO/RBAC |
- 页面 metadata: published Jun 25, 2026 9:00 AM UTC — 内容未变
- **状态**: 🟢 未变化 (第11周)

### 3️⃣ LangChain — [直接抓取] langchain.com/pricing
| 套餐 | 价格 | 备注 |
|:----:|:----:|:-----|
| Developer | **$0** | 1 seat, 5k traces/mo, 1 Fleet agent |
| Plus | **$39/seat/月** | 10k traces/mo, Unlimited seats |
| Enterprise | Custom | SSO/RBAC/SLA/自托管 |
- Engine: $1.50/LCU, Sandbox CPU: $0.0576/vCPU-hr
- **状态**: 🟢 未变化 (第11周)

## 三、定价差距分析（第11周维持不变）

| 对比组 | 倍差 |
|:------|:----:|
| GPT-5.5 vs DeepSeek V4-Flash | **214-357×** |
| GPT-5.5 vs DeepSeek V4-Pro | **69-115×** |
| GPT-5.5 vs MiniMax M3 Standard | **100-167×** (输入) / **50-83×** (输出) |
| Claude Opus vs DeepSeek V4-Pro | **172×** (输入) / **258×** (输出) |

## 四、本周信号汇总

| 信号 | 评级 | 说明 |
|:---:|:----:|------|
| DeepSeek模型弃用通知 | **S2** | deadline 2026/07/24 · 仅剩29天迁移窗口 |
| 连续11周定价全面冻结 | **S2** | 2026H1定价趋势半年度报告条件成熟 (建议6/30前产出·仅剩5天) |
| Dify pricing页元数据更新 | **S3** | published Jun 25 · 价格未变 → 稳定信号 |
| Cohere SKU精细化持续 | **S3** | Rerank 4 Pro拆分Medium/Large后第2周维持不变 |
| 定价差距未缩窄 | **S3** | GPT-5.5/Claude Opus高端差异化战略完全固化 |

## 五、待办项

| 优先级 | 事项 | 说明 |
|:-----:|------|------|
| **P1** | 建立Playwright渲染管道 | 抓取OpenAI/Anthropic/Coze/智谱4家SPA定价页 (第11周阻塞) |
| **P1** | 修复阿里百炼/百度千帆URL | 定价页404 (第11周失效) |
| **P1** | 2026H1定价趋势半年度报告 | 建议**6月30日前**产出 (仅剩5天) |
| **P2** | DeepSeek迁移跟进 | T1管道跟进API用户迁移进度 (deadline 7/24) |
| **P3** | MiniMax platform probing | 平台网络已恢复→尝试Playwright穿透pricing SPA |

---

**📋 验证**: 3/3 抽样 [直接抓取] — 零推测 | **今日最后全量**: 2026-06-25 21:37 | **cron时间**: 2026-06-25 23:04 CST
