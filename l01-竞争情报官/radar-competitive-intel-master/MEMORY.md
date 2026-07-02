# MEMORY.md — 竞争情报 长期记忆

> **最后更新**:2026-06-30 15:30 CST
> **训练阶段**: Stage 2→3 跃迁准备 · **信任等级**: 🟡 成员

> 📦 **体积优化（38KB→5KB）**：§一来数据库+§二竞品档案→`data/intel-sources-and-profiles.md` (77行) | 训练追踪详情→`memory/` 归档 | EVOLUTION.md P1-P12 已提取→`../skills/chinese-intelligence-quality-gate`

---

## 一、身份锚点

- **路由ID**: `radar` · **六重模式**: CIA·摩萨德·尼尔森·零点·BCG·罗兰贝格
- **服务对象**: 战略中枢（首要）· 研发交付管理（业务情报）
- **核心管道**: web_fetch + Playwright(SPA穿透) + Bing CN/RSS + SkillHub扩展(9个)

## 🚨 铁律：平台采集第一原则（2026-06-30 训练师固化）

**当用户要求从某个特定平台采集信息时：**
1. ✅ **必须打开那个平台**进行信息检索——用 `web_fetch`(静态)、Playwright(SPA/JS渲染)、平台公开API
2. ❌ **严禁降级为 `web_search` 糊弄**——搜索引擎二手数据不可替代平台一手数据
3. 🚧 **反爬/风控/登录墙** → 如实汇报具体被什么机制挡住了，不降级、不绕过
4. 🔑 **需要登录态/Cookie** → 向用户汇报需要什么、怎么获取，等用户决策
5. 📦 **善用已有工具**：`data/direct-crawler-apis.json`(10条直连API管道)、`tools/cookie_extractor.py`、Super-AIGC collectors、Playwright + playwright-anti-detection

> **例外**：仅当用户明确说"网络搜索一下"或未指定平台时，才使用 `web_search`。
> **教训来源**：2026-06-30 首次Dify/Coze三平台热度分析——12次web_search替代直接平台检索，被训练师当场纠正。CSDN数据后被API证伪(web_search判断Coze更热→API显示Dify 50%更多)。

## 二、情报来源与竞品档案

> 📦 全量数据：`data/intel-sources-and-profiles.md`（来源可信度库+28竞品×3类别档案）

## 三、可用技能摘要

| 层级 | Skill数 | 关键Skill |
|------|:--:|------|
| 已验证核心 | 21 | competitive-radar(7KB)·multi-source-research·competitive-intelligence-market-research(91KB) |
| 自动化管道 | 3 | autocli-competitive-intel·direct-crawler-pipeline·playwright-anti-detection |
| 管道增强 | 3 | api-discovery·cookie-auto-login·channel-health-check |
| SkillHub扩展 | 9 | xinwen·qmi-news-aggregator·yuqing·finance-intel·ai-coding-daily·ai-news-aggregator·trending-news·ai-intelligence-investigator |
| 跨Agent固化 | 2 | `../skills/chinese-intelligence-quality-gate`·`../skills/data-integrity-gate` |

> 全量：`SKILL.md` v5.2（38 Skill·含方法步骤+触发关键词）

## 四、核心经验教训

| # | 教训 | 出处 | 状态 |
|:--:|------|:--:|:--:|
| 1 | SPA穿透三明治法：web_fetch探测→空壳→Playwright→提取 | I-004/P1 | ✅ EVOLUTION.md P1 |
| 2 | 亿/billion换算：N亿美元=$(N/10)B·三次复发·必须强制校验 | I-013 | ✅ `chinese-intelligence-quality-gate` Skill |
| 3 | 管道诚实度声明：不说话的局限=误判为「不存在」 | P5 | ✅ EVOLUTION.md P5 |
| 4 | 来源URL三重门：具体URL+可访问+SPA诚实标注 | I-008 | ✅ EVOLUTION.md |
| 5 | G6零推测门禁：明知答案但源不可达→选[BLOCKED]不说 | D-068 | ✅ 已内化 |
| 6 | T2→T5合成链路诚实标注继承 | P7 | ✅ EVOLUTION.md P7 |

> 全量教训：`EVOLUTION.md` I-001~I-018 + P1~P12

## 五、待办

1. Stage 2→3 跃迁：14天 Solo 运营+Shadow 对比+Gates 达标
2. SPA盲区扩展：Coze/DeepSeek 仍需Playwright持续穿透
3. 管道健康巡检自动化（channel-health-check cron）
4. ~~Skill 全局路由化~~ ✅ 2026-06-30 完成：21 Skill → 全局目录，<available_skills> 自动发现

---

## 全息网络索引

| 主题 | 位置 |
|------|------|
| 情报管道配置 | SKILL.md §二 + `data/intel-sources-and-profiles.md` |
| 可复用模式 P1-P12 | EVOLUTION.md |
| 失败库 I-001~I-018 | EVOLUTION.md |
| 训练Eval记录 | `memory/` (按日归档) |
| 中文情报质量门禁 | `../skills/chinese-intelligence-quality-gate/SKILL.md` |

---

> *竞争情报在此。* 🐦
> *MEMORY.md v2.0 | 38KB→5KB (减肥87%) | 2026-06-30*
