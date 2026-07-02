# 12 竞争情报官 SKILL.md — 技能清单 v5.3

> **版本**：v5.3（2026-06-30 全局路由架构·21 Skill 推至系统全局 `<available_skills>` 自动发现）  
> **上版**：v5.2（训练师场景深化）  
> 🏗️ **路由方式已变更**：优先通过 `<available_skills>` 系统自动匹配 → 本文件作为索引兜底

## 🌐 通用基础技能组 (Universal Base Skills)

> 编队级通用技能，所有Agent标配。优先使用以下4个技能处理网络搜索/浏览器自动化/RSS监控需求。
> **基础套装（必装）**: playwright-han + web-search-ex-skill（打穿SPA + 多引擎搜索）
> **进阶套装（选装）**: bing-cn-search + feed-watcher（中文搜索增强 + 行业动态监控）

| 技能 | 路径 | 用途 |
|------|------|------|
| `playwright-han` | `../skills/playwright-han/SKILL.md` | 🔧 浏览器自动化（Python Playwright，打穿SPA/JS渲染页面抓取） |
| `web-search-ex-skill` | `../skills/web-search-ex-skill/SKILL.md` | 🔍 通用网络搜索（百度/必应/DuckDuckGo，无需API Key） |
| `bing-cn-search` | `../skills/bing-cn-search/SKILL.md` | 🇨🇳 中文必应MCP搜索（bing-cn-mcp，更稳定的中文互联网） |
| `feed-watcher` | `../skills/feed-watcher/SKILL.md` | 📡 RSS/Atom订阅监控（博客/YouTube/GitHub/Reddit，支持Webhook） |

> **版本**：v3.1（2026-06-26 训练师修复·加关键词触发列）  
> **上版问题**：v2.x 声称32个Skill，实际仅14个存在，56%虚假率  
> **原则**：只列真实可用的 Skill，按训练看板六任务映射

---

## 一、训练看板任务×Skill映射

| 看板任务 | 权重 | 核心Skill | 辅助Skill | 典型关键词触发 |
|---------|:--:|------|------|------|
| **T1** 竞品自动监控 | 25 | `competitive-radar` | `autocli-competitive-intel`, `direct-crawler-pipeline`, `playwright-anti-detection`, `multi-source-research`, `brand-monitoring-strategies`, `playwright-han`, `bing-cn-search`, `web-search-ex-skill`, `multi-engine-websearch`, `feed-watcher`, `recent-news-article-aggregator` | "changelog" "更新" "最近有什么" "新产品" "发布" |
| **T2** 社媒/PR收集 | 20 | `multi-source-research` | `autocli-competitive-intel`, `direct-crawler-pipeline`, `playwright-anti-detection`, `brand-monitoring-strategies`, `global-talent-radar`, `playwright-han`, `bing-cn-search`, `web-search-ex-skill`, `recent-news-article-aggregator` | "新闻" "媒体" "报道" "高管" "社媒" |
| **T3** 定价策略追踪 | 20 | `competitive-intelligence-market-research` | `company-investment-research` | "定价" "价格" "多少钱" "价格变化" "订阅" |
| **T4** SWOT自动更新 | 15 | `competitive-intelligence-market-research` | `decision-advisor` | "SWOT" "优势" "劣势" "机会" "威胁" |
| **T5** 竞争事件日报 | 10 | `executive-dashboard` | `autocli-competitive-intel`, `direct-crawler-pipeline`, `decision-advisor` | "日报" "简报" "今日" "今日必看" |
| **T6** 产品拆解报告 | 10 | `competitive-intelligence-market-research` | `entity-optimizer` | "拆解" "深度分析" "详细分析" "对比" |
| **UT** 通用工具类 | — | `api-discovery` | `cookie-auto-login`, `channel-health-check` | "发现API" "找端点" "登录" "Cookie" "检查管道" "健康检查" "doctor" |

---

## 一.五、Skill 选择铁律（2026-06-30 全局路由版）

```
🏗️ 新路由流程（v5.3）：
  1. 检查 <available_skills>（系统自动注入）→ 按描述匹配任务类型 → read 匹配 Skill → 执行
  2. 如 <available_skills> 未命中 → 查下表（§一 映射表）→ read 对应 Skill → 执行
  3. 如仍不确定 → read 本文件 §二完整清单 → 匹配

⚠️ T3 定价任务即使缺少历史数据，也必须先抓当前定价页，再诚实标注"无历史基线"。
⚠️ 禁止错选 Skill（盲测反馈：T1 错选 competitive-intelligence-market-research 91KB → 应选 competitive-radar 7KB）
⚠️ 所有 21 个核心 Skill 已推送至系统全局目录，<available_skills> 可直接发现
```

---

## 二、已验证 Skill 清单（21个，100%真实可用）

### 情报采集层（11个）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `competitive-radar` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/competitive-radarSKILL.md` | 7.3KB | **竞品动态雷达扫描**：多源并行采集→信号分级（S1确凿/S2强信号/S3弱信号/N噪音）→去重→按赛道分组。T1 竞品自动监控核心 Skill。触发："changelog""更新""新产品""发布" |
| `playwright-han` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/playwright-han/SKILL.md` | 5.2KB | **SPA 穿透三明治法**：Layer1 web_fetch 探测→返回空壳（<500字）→Layer2 Playwright+Chrome 渲染（page.goto→wait_for_timeout 3000ms）→Layer3 inner_text 提取有效行。已验证：36氪(100%)/火山引擎/知乎。触发：web_fetch 返回空壳时自动 fallback |
| `bing-cn-search` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/bing-cn-search/SKILL.md` | 2.0KB | **中文必应搜索**：Bing CN MCP 引擎，更稳定的中文互联网覆盖。用于绕过 Google 沙箱封锁、覆盖百度/CSDN/36氪等中文源。T1/T2 中文竞品发现首选 |
| `web-search-ex-skill` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/web-search-ex-skill/SKILL.md` | — | **通用网络搜索**：百度+必应+DuckDuckGo 三引擎聚合，无需 API Key。T2 社媒/PR 扫描的基础管道——多引擎并行搜索弥补单引擎盲区 |
| `multi-engine-websearch` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/multi-engine-websearch/SKILL.md` | — | **6 引擎搜索**：DDG/Google/Yahoo/Startpage 等，无需 API Key。作为 Bing CN 覆盖不到的英文源补充（Ars Technica/The Verge/TechCrunch） |
| `recent-news-article-aggregator` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/recent-news-article-aggregator/SKILL.md` | — | **全球新闻聚合**：100 万+/周新闻源，支持语言/地区/分类筛选。T2 社媒扫描覆盖非中文新闻管道 |
| `feed-watcher` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/feed-watcher/SKILL.md` | — | **RSS/Atom 订阅监控**：跟踪竞品博客/GitHub Release/YouTube 频道。设置 cron 定时抓取→Webhook 推送。T1/T2 被动监控管道补丁——覆盖 web_fetch 不可达的 RSS 源 |
| `internet-search` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/internet-search/SKILL.md` | — | **搜索方法论**：分类路由（按信息类型选择搜索引擎）+查询策略（关键词组合/时间过滤/域名过滤）+多搜索技巧（site:/inurl:/intitle:）。所有搜索任务的元 Skill |
| `brand-monitoring-strategies` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/brand-monitoring-strategies/SKILL.md` | 3.6KB | **品牌舆情监控**：竞品声量趋势→情感分析→负面信号预警（产品事故/安全漏洞/用户投诉突增）。T2 社媒扫描的品牌维度增强 |
| `multi-source-research` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/multi-source-research/SKILL.md` | 3.3KB | **多源交叉验证**：Phase1 制定搜索策略→Phase2 多源并行采集→Phase3 逐条比对一致性→Phase4 可信度评级（A/B/C/D）。T2 社媒/PR 核心 Skill——所有情报必须通过交叉验证门禁（单源=暂不采用/双源一致=B+/三源一致=A-） |
| `global-talent-radar` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/global-talent-radar/SKILL.md` | 19.3KB | **竞品人才动向追踪**：核心团队变动（CTO/VP 离职/入职）→招聘趋势（JD 数量/方向变化）→组织架构调整。人才流动=战略转向的先行指标 |

### 分析加工层（5个）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `competitive-intelligence-market-research` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/competitive-intelligence-market-research/SKILL.md` | 91KB | **竞品深度拆解**：24 场景全覆盖——定价追踪·功能矩阵·融资监控·团队变动·合作伙伴·客户案例·负面信号。⚠️ T3 定价追踪+T4 SWOT 更新+T6 产品拆解报告专用。注意：T1 竞品扫描应选 competitive-radar(7KB)，非此(91KB) |
| `company-investment-research` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/company-investment-research/SKILL.md` | 19.5KB | **竞品融资/估值分析**：融资轮次/金额/估值·投资方背景·资金用途·估值变化趋势。⚠️ 含中文金融数据必须执行亿/billion 换算校验（N亿美元=$(N/10)B） |
| `attribution-modeling` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/attribution-modeling/SKILL.md` | 10.6KB | **归因分析**：信号影响力评估——哪些事件真正驱动了竞品指标变化（用户增长/收入/市场份额）vs 哪些只是噪音。T5 日报因果关系判断辅助 |
| `risk-metrics-calculation` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/risk-metrics-calculation/SKILL.md` | 19.1KB | **竞品风险评估量化**：可能性×影响矩阵→竞品威胁等级→OpenClaw 受影响概率→应对成本估算。T4 SWOT 的风险量化辅助 |
| `entity-optimizer` | `.openclaw/workspace/十二虾/l01-竞争情报官/radar-competitive-intel-master/skills/entity-optimizer/SKILL.md` | 27.8KB | **产品功能/实体对比矩阵**：竞品功能清单→差异化评分→空白机会识别。T6 产品拆解报告的功能对比维度专用 |

### 🆕 自动化采集管道层（3个·2026-06-27 重构：Skill⇄配置分离）

| Skill | 配置文件 | 场景 |
|-------|---------|------|
| `autocli-competitive-intel` | `data/autocli-commands.json` | 何时用autocli/决策树/自建适配器。55+站点命令数据在配置 |
| `direct-crawler-pipeline` | `data/direct-crawler-apis.json` | 何时选哪个爬虫/错误降级。10管道API数据在配置 |
| `playwright-anti-detection` | `data/playwright-anti-detection.json` + `.js` | 何时用Playwright/三层防御原理。Chrome args+JS脚本在配置 |

> 🏗️ **架构原则**：Skill = 怎么用/决策树 · 配置 = endpoint/headers/常量/脚本
> autocli 二进制：`~/.local/bin/autocli`（`which autocli` 确认路径）
> 源码参考：Super-AIGC/collectors/_direct_crawlers/（非运行时依赖）

### 🆕 管道增强层（3个·2026-06-29 联合审计提取）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `api-discovery` | `../skills/api-discovery/SKILL.md` | 🆕 | 新站点API端点自动发现 (6策略: Performance/Refetch/SSR/Pinia/盲探) |
| `cookie-auto-login` | `../skills/cookie-auto-login/SKILL.md` | 🆕 | 从Chrome/Edge/Firefox提取登录Cookie，突破知乎/小红书登录墙 |
| `channel-health-check` | `../skills/channel-health-check/SKILL.md` | 🆕 | 采集管道自动健康巡检，替代手动HEARTBEAT.md |

> 🛠️ 配套工具：`tools/rate_limiter.py` `tools/cookie_extractor.py` `tools/api_discoverer.py` `tools/page_adapter.py` `tools/stealth.js`

### 决策输出层（5个）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `executive-dashboard` | `../skills/executive-dashboard/SKILL.md` | 10.7KB | **高管日报自动生成**：T5竞争事件日报核心 Skill。三段漏斗过滤（原始→候选→精选）→≤500字硬约束→四板块结构（今日必看/竞品动态/预警池/情报统计）。日报不重复昨日已推P0 |
| `decision-advisor` | `../skills/decision-advisor/SKILL.md` | 3.2KB | **决策建议**：基于情报信号生成可选行动方案→评估每个方案的预期结果/风险/成本→推荐优先级。T5日报「行动建议」板块专用 |
| `boardroom-advisor` | `../skills/boardroom-advisor/SKILL.md` | 11.1KB | **战略层汇报材料**：将技术情报转化为管理层可读的战略简报（PPT/飞书文档）。季度/年度竞品总结或向战略中枢汇报时使用 |
| `retention-risk-predictor` | `../skills/retention-risk-predictor/SKILL.md` | 6.6KB | **竞品用户流失预测**：竞品用户评价/NPS趋势→流失信号→OpenClaw可抢占的机会窗口。T4 SWOT「机会」象限增强 |
| `geo-content-optimizer` | `../skills/geo-content-optimizer/SKILL.md` | 8.3KB | **区域化竞品分析**：按地理市场（中国/美国/欧洲/东南亚）分别分析竞品策略和定价差异。跨国竞品对比时使用 |

### 🆕 自动化采集管道层（3个·Skill⇄配置分离）

| Skill | 配置文件 | 场景 |
|-------|---------|------|
| `autocli-competitive-intel` | `data/autocli-commands.json` | **autocli 调度器**：55+站点命令→按站点类型选采集策略→回退降级。配置与 Skill 分离——Skill=决策树/使用说明，配置=endpoint/headers/常量 |
| `direct-crawler-pipeline` | `data/direct-crawler-apis.json` | **直接爬虫管道**：10条专属API管道→按数据源类型选择爬虫→错误降级。覆盖 GitHub/ProductHunt/HN 等有公开 API 的站点 |
| `playwright-anti-detection` | `data/playwright-anti-detection.json`+`.js` | **反检测 Playwright**：三层防御（Chrome args伪装+JS脚本注入+行为模拟）→突破 CloudFlare/反爬。中文SPA站点（36氪/知乎/Coze）的最终 fallback |

### 🆕 管道增强层（3个·2026-06-29 联合审计提取）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `api-discovery` | `../skills/api-discovery/SKILL.md` | 🆕 | **API端点发现**：6策略自动探测（Performance/Refetch/SSR/Pinia/盲探）→发现新站点的隐藏API→绕过SPA直接调用。降低对Playwright的依赖 |
| `cookie-auto-login` | `../skills/cookie-auto-login/SKILL.md` | 🆕 | **Cookie自动提取**：从Chrome/Edge/Firefox浏览器提取登录Cookie→注入Playwright→突破知乎/小红书等登录墙。扩大可覆盖的中文源范围 |
| `channel-health-check` | `../skills/channel-health-check/SKILL.md` | 🆕 | **采集管道健康巡检**：自动检测每条管道的可达性→识别SPA盲区/反爬墙/API限流→输出管道健康度报告。替代手动HEARTBEAT检查 |

> 来源：腾讯 SkillHub (skillhub.cn) · 6.1万+ AI Skills 社区
> 安装方式：`skillhub install` CLI v2026.6.12 → `workspace/skills/`

### 情报增强层（6个·核心推荐）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `xinwen` | `../skills/xinwen/SKILL.md` | 5.5KB | 🆕 新闻情报雷达：四级分级(关键/关注/一般/噪音)+语义去重+自适应排序+行动建议 |
| `qmi-news-aggregator-skill` | `../skills/qmi-news-aggregator-skill/SKILL.md` | 8.0KB | 🆕 情报虾：13国民级热榜(百度/知乎/微博/B站/抖音等)+8头部信源实时抓取 |
| `news-aggregator-skill` | `../skills/news-aggregator-skill/SKILL.md` | 5.1KB | 🆕 News Aggregator：HN/GitHub/ProductHunt/36Kr/腾讯新闻/华尔街见闻/V2EX/微博8源聚合 |
| `yuqing` | `../skills/yuqing/SKILL.md` | 10.3KB | 🆕 多平台舆情监控：腾讯新闻/微博/抖音/小红书/知乎+情感分析+ECharts交互报告 |
| `finance-intel` | `../skills/finance-intel/SKILL.md` | 4.1KB | 🆕 财经情报局：12+权威财经源+利好利空信号分析+个股/行业/大盘影响评估 |
| `ai-coding-daily` | `../skills/ai-coding-daily/SKILL.md` | 6.7KB | 🆕 AI Coding日报：GitHub/HN/Anthropic&OpenAI博客/ArXiv/公众号自动采集+带点评日报 |

### 聚合增强层（3个·可选扩展）

| Skill | 路径 | 大小 | 场景 |
|-------|------|:--:|------|
| `ai-news-aggregator` | `../skills/ai-news-aggregator/SKILL.md` | 4.0KB | 🆕 AI新闻聚合引擎：100+ RSS源并发抓取+兴趣评分+跨天去重 |
| `trending-news-aggregator` | `../skills/trending-news-aggregator/SKILL.md` | 7.5KB | 🆕 热点新闻聚合器：多平台热点自动抓取+AI趋势分析+定时推送+热度评分 |
| `ai-intelligence-investigator` | `../skills/ai-intelligence-investigator/SKILL.md` | 8.3KB | 🆕 A股情报调查员：17搜索引擎+竞品分析+舆情监测+信息交叉验证 |

> ⚠️ 使用铁律：优先用现有21个核心Skill（§二），SkillHub扩展仅在核心Skill无法覆盖时启用

## 四、已知缺口（不需要假Skill填补）

| 缺口 | 影响任务 | 替代方案 | 是否需要新Skill |
|------|:--:|------|:--:|
| web_search / web_fetch | T1/T2 | **OpenClaw 内置工具**，不需要 Skill | ❌ |
| Playwright 浏览器自动化 | T1 | `playwright-anti-detection` (🆕已补) + `playwright-han` | ✅ 已补 |
| 定时推送管道 | T5 | cron + 文件输出（架构问题，非Skill问题） | ❌ |
| SWOT 基线存储 | T4 | workspace 文件持久化（12_radar/data/swot-baseline.json） | ❌ |

> 2026-06-26 升级：Playwright 反检测缺口已通过 `playwright-anti-detection` Skill 填补。
> 工具能力归工具，Skill 归 Skill。

---

## 🆕 跨Agent模式固化技能组（2026-06-30 训练师从踩坑日志提取）

> 来源：12_radar EVOLUTION P4/P5/P6/I-008/I-013 复现模式

| Skill | 路径 | 场景 |
|-------|------|------|
| `chinese-intelligence-quality-gate` ⭐ | `../skills/chinese-intelligence-quality-gate/SKILL.md` | 🆕 中文情报质量门禁：亿/billion换算+时效三要素标注+管道诚实声明+来源URL三重门——T2/T5产出前必读 |
| `data-integrity-gate` | `../skills/data-integrity-gate/SKILL.md` | 🆕 数据诚信防护：curl参数铁律+缓存验证门禁+Σ计数偏误修复——T2/T3/T6数据统计前必读 |

---

## 五、使用规则

1. **每任务加载 ≤3 个 Skill**：T1-T6 按上表映射，不堆砌
2. **按需加载，用完释放**：不预加载全量 Skill
3. **Skill 未命中时**：先检查本清单 → 不存在则如实告知用户（不虚拟 Skill）

---

## 六、三级采集管道状态机（2026-06-27 核心运营文档）

### 6.0 设计原则（LLM 可读性优先）

```
⚠️ 以下状态机 = 每次 cron/情报请求的完整执行脚本。
   不需要先"理解"再"执行" — 直接按表走，遇错看注释。
   
   当前环境事实 (2026-06-29 升级):
     - Chrome ❌ 不可用 → autocli Browser 命令全部不可用
     - autocli Public 命令 ✅ 可用 (hackernews/devto/lobsters/stackoverflow)
     - 直连爬虫 ✅ 可用 (19端点, 来自 direct-crawler-apis.json)
     - Playwright ✅ 可用 + Stealth三层 (playwright-stealth + tools/stealth.js + WebGL欺骗)
     - Cookie提取 ✅ 可用 (tools/cookie_extractor.py → 突破登录墙)
     - API自动发现 ✅ 可用 (tools/api_discoverer.py → 新站点端点探测)
     - RateLimiter ✅ 可用 (tools/rate_limiter.py → 自适应限速)
     - curl ✅ 可用 | jq ✅ 可用 | python ✅ 可用
     
   每次 cron 触发时:
     1. 你已经读到了这个文件 ← 状态机在此
     2. 当前状态 = START
     3. 按下面 §6.1 的逐级检查表执行
     4. 不要跳过任何一级
```

### 6.1 逐级检查表 (LLM 执行脚本 — 按顺序,不跳步)

```
Step 0: 当前状态 = START
        确认情报目标: 要查哪个平台? 哪个关键词?
        ↓
Step 1: 读 data/autocli-commands.json
        查 public_verified[] 中是否有目标平台
        ├─ 找到了 → 进入 Step 2 (L1 autocli)
        ├─ 没找到但目标在 browser_required[] 中
        │   → 当前环境无Chrome → 跳过L1 → 进入 Step 3 (L2)
        └─ 完全没找到 → 进入 Step 3 (L2)
        ↓
Step 2 [L1 · autocli]:
        exec: autocli {platform} {command} {args} --format json  (timeout=20s)
        ├─ exit=0 且有数据 → DONE ✅
        │   标注: "来源: autocli {site} {command} [直接抓取·Public]"
        └─ exit≠0 或超时 或 空结果
            → ⚠️ L1降级 → 进入 Step 3
        ↓
Step 3 [L2 · 直连爬虫]:
        读 data/direct-crawler-apis.json
        查 pipelines[] 中 {id} == 目标平台
        ├─ 找到了 → 看该管道的 priority 和 auth 字段:
        │   ├─ auth="public" 且 只有简单 GET → Step 3a (curl)
        │   │   exec: curl -s "{endpoint.primary}" -H "key: value" -H ... --max-time 15
        │   │   └─ 成功(HTTP 200 + JSON解析成功) → DONE ✅
        │   │      标注: "来源: {platform} {endpoint} [直接抓取·Public HTTP]"
        │   │   └─ 失败 → 检查 endpoint.fallback:
        │   │       ├─ 有 fallback → 重试 → 成功=DONE / 失败=进入Step 4
        │   │       └─ 无 fallback → 进入 Step 4
        │   │
        │   └─ 复杂解析(bilibili WBI / kuaishou Apollo / zhihu INITIAL_STATE)
        │       → 需要 Python → 标注"[需Python管道·待执行]" → 进入 Step 4
        │       (当前 cron 环境下,复杂管道作为预备但不在 curl 中实现)
        │
        └─ 没找到 → 进入 Step 4
        ↓
Step 3.5 [L2.5 · Cookie注入]:
        当前 L2 API 返回 401/403/需要登录?
        ├─ NO → 继续 Step 4
        └─ YES → read tools/cookie_extractor.py
            exec: python3 tools/cookie_extractor.py {platform}
            ├─ Cookie提取成功 → 注入到 L2 请求头 → 重试 Step 3
            │   └─ 成功 → DONE ✅ 标注: "来源: {platform} API [Cookie注入·浏览器提取]"
            │   └─ 仍失败 → 进入 Step 4
            └─ Cookie提取失败 (浏览器未登录/rookiepy不可用)
                → 标注 "[BLOCKED·登录墙·Cookie提取失败]" → 进入 Step 4
        ↓
Step 4 [L3 · Playwright增强版]:
        目标平台有公开URL?
        ├─ YES → web_fetch({url}, extractMode=markdown, maxChars=5000)
        │   ├─ 返回内容 > 500字符 → DONE ✅ (非空壳)
        │   └─ 返回 < 500字符或空壳 → 触发SPA规则 → Step 5
        │
Step 5 [L3 · Playwright增强版 (Stealth+ApiDiscovery)]:
        ├─ 目标为新域名(无缓存)? → 先跑 ApiDiscoverer 预检
        │   exec: python3 tools/api_discoverer.py {url}
        │   └─ 发现API端点 → 写入 data/direct-crawler-apis.json → 重试 Step 3 (L2)
        │
        └─ Playwright渲染:
            exec: python3 tools/stealth_runner.py "{url}" "{keyword}"
            (自动注入: playwright-stealth + tools/stealth.js + WebGL RTX3060欺骗)
            ├─ 页面渲染成功 + 内容 > 5行 → DONE ✅
            │   标注: "来源: Playwright+Stealth({url}) [增强隐身]"
            ├─ 页面渲染成功 + 内容 ≤ 5行 → [BLOCKED·登录墙]
            │   标注: "⚠️ {平台}·反爬已穿透·登录墙·建议: cookie-auto-login"
            └─ 网络错误/timeout → BLOCKED ❌
                标注: "[BLOCKED·{平台}·{原因}·{时间}]"
        └─ NO → BLOCKED ❌
            标注: "[BLOCKED·{平台}·{原因}·{时间}]"
```

### 6.2 状态转移表 (紧凑版·查表即执行)

| # | 你现在在哪 | 条件 | 下一步 | 做什么 |
|:--:|----------|------|-------|------|
| 0 | START | 任意情报请求 | →L1CHECK | read data/autocli-commands.json |
| 1 | L1CHECK | 目标∈public_verified | →L1EXEC | exec autocli {platform} {command} {args} --format json |
| 2 | L1CHECK | 目标∈browser_required(无Chrome) | →L2CHECK | 跳过L1, read data/direct-crawler-apis.json |
| 3 | L1CHECK | 目标∉autocli-commands.json | →L2CHECK | read data/direct-crawler-apis.json |
| 4 | L1EXEC | exit=0 且有数据 | →DONE | 解析JSON,标注来源 |
| 5 | L1EXEC | exit≠0/超时/空 | →L2CHECK | echo "[L1降级] autocli失败→L2" |
| 6 | L2CHECK | 目标∈pipelines | →L2EXEC | curl -s {endpoint} -H {headers} |
| 7 | L2CHECK | 目标∉pipelines | →L3 | web_fetch |
| 8 | L2EXEC | HTTP 200 + JSON有效 | →DONE | 标注来源 |
| 9 | L2EXEC | 失败 + 有fallback | →L2RETRY | curl -s {endpoint.fallback} -H {headers} |
| 10 | L2RETRY | fallback成功 | →DONE | 标注来源 |
| 11 | L2RETRY | fallback也失败 | →L3 | web_fetch |
| 12 | L2EXEC | 失败 + 无fallback | →L3 | web_fetch |
| 13 | L3 | web_fetch有内容(>500chars) | →DONE | 标注来源 |
| 14 | L2EXEC | HTTP 401/403 | →L2.5COOKIE | 触发Cookie提取注入 |
| 15 | L2.5COOKIE | Cookie提取成功 | →L2RETRY | 注入Cookie→重试API |
| 16 | L2.5COOKIE | Cookie提取失败 | →L3 | Playwright最后一搏 |
| 17 | L3 | 新域名/无缓存 | →L3PRECHK | 运行 ApiDiscoverer |
| 18 | L3PRECHK | 发现API端点 | →L2CHECK | 写入配置→重试L2 |
| 19 | L3 | web_fetch空壳/SPA | →L3PW | Playwright+Stealth渲染 |
| 20 | L3PW | 有内容(>5行) | →DONE ✅ | 标注"Playwright+Stealth" |
| 21 | L3PW | 内容≤5行 | →BLOCKED | 标注"登录墙·建议cookie-auto-login" |
| 22 | L3 | 目标无公开URL | →BLOCKED | 标注原因+时间 |

### 6.3 批量执行模式 (cron T1/T5 每日触发)

```
当 cron 触发 T1(全28竞品扫描) 或 T5(日报)时:

  FOR EACH 竞品 IN data/competitors.json:
    FOR EACH 情报维度 (最新动态/新闻/定价):
      ① 确定目标平台 (如 "hackernews" / "weibo")
      ② 从 §6.1 Step 0 开始执行逐级检查表
      ③ 同级平台可并行 (hackernews + devto + lobsters 同时 exec)
      ④ 结果写入 memory/{date}.md
    END
  END
  
  ⚠️ 并行限制: 同时 ≤3 个 exec (避免速率限制)
  ⚠️ 每个平台间隔 ≥2秒 (RateLimiter)
```

### 6.4 Skill vs 配置文件 读写规则

```
┌─────────────┬──────────────────────┬──────────────────────────┐
│ 要做什么     │ 读哪个                │ 为什么                    │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 查autocli命令│ data/autocli-commands │ 存的是 platform+cmd+args │
│             │ .json (必读)          │ 性能高,5KB               │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 查直连API   │ data/direct-crawler-  │ 存的是 endpoint+headers  │
│             │ apis.json (必读)      │ +response_path, 8.5KB    │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 查Playwright│ data/playwright-anti- │ 存的是 chromium_args +   │
│ 配置        │ detection.json (必读) │ stealth + JS脚本路径      │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 不知道怎么  │ ../skills/autocli-     │ 存的是决策树+YAML模板    │
│ 选管道了    │ competitive-intel/SKILL.md│ (仅L2降级不清楚时 read)   │
├─────────────┼──────────────────────┼──────────────────────────┤
│ API调不动   │ ../skills/direct-crawler-│ 存的是降级策略+边界条件  │
│ 不知道怎么  │ pipeline/SKILL.md       │ (仅异常时 read)           │
│ 降级了      │                       │                          │
├─────────────┼──────────────────────┼──────────────────────────┤
│ L2返回401   │ api-discovery Skill   │ 🆕 触发Cookie提取+注入   │
│ 需要登录了   │ + cookie-auto-login   │ + 重试 (L2.5层)          │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 新站点不知道 │ api-discovery Skill   │ 🆕 6策略自动发现API端点  │
│ API在哪      │ + tools/api_discoverer │ (L3预检层)              │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 采集管道     │ channel-health-check  │ 🆕 逐管道check→分级报告   │
│ 全挂了？     │ Skill (替代HEARTBEAT) │ (T5日报前自动巡检)        │
├─────────────┼──────────────────────┼──────────────────────────┤
│ 需要浏览器  │ ../skills/playwright-  │ 存的是Playwright调用模板 │
│ 不知道怎么  │ anti-detection/SKILL.md│ (仅到L3时 read)           │
│ 启动了      │                       │                          │
└─────────────┴──────────────────────┴──────────────────────────┘

⚠️ 常规路径: 读本文件 → 读配置JSON → exec → DONE  (不碰3个Skill)
⚠️ 异常路径: 降级卡住 → 才读对应 Skill 查策略
```

---

> **v6.0 联合审计升级**：+3 Skill(api-discovery/cookie-auto-login/channel-health-check) | +9 API端点 | L2.5 Cookie层 | L3预检ApiDiscoverer | Stealth增强 | 状态机15→22状态
> **v5.1 SkillHub扩展**：新增§三.五 SkillHub扩展技能组 | 9个新Skill
> **v5.0 重构记录**：新增§六三级采集管道状态机 | Skill⇄配置分离  
> 采集管道：autocli (L1) → direct-crawler (L2) → Cookie注入 (L2.5) → Playwright+Stealth+ApiDiscovery (L3) 自动降级  
> autocli 二进制：`~/.local/bin/autocli`（`which autocli` 确认路径）  
> 配置：mcporter bing-cn MCP 已就绪 (`config/mcporter.json`)  
> *SKILL.md v5.1 | 12_radar | 2026-06-28*
