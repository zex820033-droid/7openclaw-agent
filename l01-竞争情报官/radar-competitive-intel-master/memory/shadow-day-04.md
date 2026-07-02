# 🦞 Shadow Day 04 — Radar T1 轻量采集

> 时间: 2026-06-23 17:01 CST | 模式: T1 Shadow采集
> 任务: web_fetch 3家(Exa/Tavily/LangChain) → 各一句话+URL

---

## 采集结果

### 1. Exa — Web Search API & AI Search Engine
**一句话**: Exa 定位为"为AI构建的最快最准确的网页搜索API"，主打AI Agent搜索上下文。
**URL**: https://exa.ai
**状态**: ✅ 可达（新鲜请求，内容与全天采集一致）

### 2. Tavily — AI Agent Web Search API
**一句话**: Tavily 通过单一API提供实时搜索+提取+爬取，核心卖点"连接AI Agent到网络"。
**URL**: https://tavily.com
**状态**: ✅ 可达（新鲜请求，内容与全天采集一致）

### 3. LangChain — Agent Development Lifecycle Platform
**一句话**: LangChain 聚焦 LangSmith，强调Agent开发生命周期（构建→测试→部署→监控）。
**URL**: https://langchain.com
**状态**: ✅ 可达（新鲜请求，内容与全天采集一致）

---

## 信号分级
| 项目 | 信号 | 备注 |
|:----|:----:|------|
| Exa | N 噪音 | 距首次~55min，零变化 |
| Tavily | N 噪音 | 距首次~55min，零变化 |
| LangChain | N 噪音 | 距首次~55min，零变化 |

## 复盘
单日T1共采集4轮(16:07/16:13/16:21/17:01)，Exa/Tavily/LangChain三家首页在约1h窗口内均零变化。建议：
- 此类成熟产品首页更新频率通常以天/周为单位，T1每日1-2轮即可
- 高频轮询(≤10min间隔)不产生增量信息，徒增工具调用

---

## 🦞 T5 轻量日报 [SHADOW-T5]

> 时间: 2026-06-23 17:01 CST | 基于T1数据

Exa 和 Tavily 今日已历经4轮采集，首页内容在约1小时窗口内持续稳定，无产品定位或功能更新。LangChain 同样维持LangSmith平台的原有品牌叙事。三家成熟产品的首页更新并不高频，单日多轮轮询未产生增量情报。
