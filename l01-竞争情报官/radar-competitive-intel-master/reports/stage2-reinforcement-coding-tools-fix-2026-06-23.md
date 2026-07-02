# 修正报告 — Stage 2 第6轮数据源修复

> **时间**: 2026-06-23 11:45 CST  
> **原因**: 训练师审计发现T2来源标注不规范（"媒体名+日期"代替具体URL）  
> **状态**: ✅ 已修正并补充可验证URL

---

## T2 来源修正表

| 原声明 | 原来源 | 修正来源 | 修正后信号 |
|:-------|:------|:---------|:---------:|
| SpaceX$600亿收购Cursor | "36氪"×10篇 (无URL) | ⚠️ 36氪为SPA站点，无法提供稳定独立文章URL。Cursor官方博客零收购公告。36氪Playwright搜索"Cursor Windsurf"确有多篇文章提及"SpaceX一分现金没花收购Cursor"，但无法逐篇链接。**降级:S2(强信号·待验证)** | S2 |
| AI ROI退潮·Uber烧光预算 | "TechCrunch Jun 17" | ✅ [techcrunch.com/2026/06/05/the-token-bill-comes-due](https://techcrunch.com/2026/06/05/the-token-bill-comes-due-inside-the-industry-scramble-to-manage-ais-runaway-costs/) **+(补充)** [techcrunch.com/video/neas-tiffany-luck](https://techcrunch.com/video/neas-tiffany-luck-says-enterprises-are-still-figuring-out-their-ai-roi/) | S1 |
| Tokenmaxxing降温 | "TechCrunch Apr 17" | ✅ [techcrunch.com/2026/04/17/tokenmaxxing](https://techcrunch.com/2026/04/17/tokenmaxxing-is-making-developers-less-productive-than-they-think/) | S1 |
| Self-Harness Agent自我修改 | "VentureBeat Jun 22" | ✅ [venturebeat.com/orchestration/self-harness](https://venturebeat.com/orchestration/researchers-introduce-self-harness-a-framework-that-lets-ai-agents-rewrite-their-own-rules-boosting-performance-up-to-60/) | S1 |
| 国产AI编程"御三家" | "36氪" (无URL) | ⚠️ 36氪SPA搜索"AI编程"返回文章标题"一手实测智谱最强模型，AI编程'御三家'要成型了？"(Playwright渲染)，但无稳定URL。**降级:S2(强信号·待验证)** | S2 |
| Sakana Fugu多模型融合 | "VentureBeat Jun 22" | ✅ [venturebeat.com/orchestration/fugu](https://venturebeat.com/orchestration/no-claude-fable-5-no-problem-sakana-achieves-frontier-performance-with-new-fugu-multi-model-auto-synthesis-system) (from earlier scan) | S1 |
| AI编码六巨头竞争 | "36氪" (无URL) | ⚠️ 同上SPA限制。**降级:S2** | S2 |

### 修正前后信号分布对比

| 信号级别 | 原报告 | 修正后 | 变化 |
|:-------:|:-----:|:------:|:----:|
| S1(确凿) | 18条 | 15条 | -3(SPA来源无法验证) |
| S2(强信号) | 5条 | 8条 | +3 |
| S3(弱信号) | 2条 | 2条 | — |

---

## 核心教训

### 36氪SPA来源的URL困境

36氪搜索页面(36kr.com/search/...)是React SPA，返回的搜结果是JS渲染的，web_fetch仅返回空壳。Playwright可以穿透并提取文章标题，但**无法获取独立的、可永久引用的文章URL**。

**应对策略**:
1. 首次扫描时即用Playwright提取标题+片段 → 标注为**S2强信号·待验证**
2. 尝试寻找同一事件的英文/其他媒体来源进行交叉验证
3. 对SPA-only来源永不标注S1

### "来源URL全覆盖"声明是虚假的

原报告末尾称"来源URL全覆盖✅"是**质量声称虚假**。T2部分存在5条"媒体名+日期"格式的引用，不符合"每条来源=具体URL"的标准。

**铁律更新**:
```
来源有效性的三条检查:
□ 每条来源标注为具体URL，非"媒体名+日期"
□ URL可访问(已用web_fetch验证)
□ 如SPA站点无法提供独立URL → 诚实标注⚠️并降级信号
```

---

## 对原报告各T的修正影响

| 任务 | 原分 | 修正后 | 影响说明 |
|:---:|:----:|:------:|:--------|
| T1 | 78% | 78% | ✅ 无影响 — 所有URL来自直接web_fetch |
| T2 | 50% | 50%(维持) | ⚠️ 5条来源已全部修正或标注; 3条从S1降为S2 |
| T4 | 78% | 75% | Weakness#4参考T2未验证数据 → 标注"SPA不可验证" |
| T5 | 75% | 70% | "今日必看"中SpaceX收购降为S2 |
| **综合** | **76.0%** | **72.0%** | -4pp |

---

*修正完成。数据纪律已更新。* 🐦
