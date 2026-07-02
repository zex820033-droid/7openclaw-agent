---
name: news-aggregator-skill
description: "国内一线大厂新闻聚合器：从 13 个国民级热榜（百度/知乎/微博/B站/抖音/头条/虎嗅/36氪/IT之家/掘金/澎湃/少数派/CSDN）和 8 个头部信源（美团技术 RSS + 量子位 RSS + 机器之心 RSS + 4 个科技社区热榜）实时抓取，输出中文深度分析报告。统一走 uapis.cn 公共 API + 串行调用，零配置、防限流。触发词：'国内早报'、'大厂动态'、'科技日报'、'AI 国内动态'、'情报虾'。"
---

# 国内一线大厂新闻聚合器（v3.1）

> **核心策略**：用 `uapis.cn` 这个**公共热榜聚合 API**（无需 API Key、免费、稳定）抓所有信源 + 3 个大厂官方 RSS。
> - 第一层·13 个国民级热榜（uapis.cn 统一接口，串行 1.5 秒间隔）
> - 第二层·8 个科技/技术信源（3 个官方 RSS + 5 个 uapis.cn 上的科技社区）
> - 共 **21 个信源**，覆盖**国内一线大厂 + 主流程序员社区 + 财经科技媒体**

---

## 🔄 Universal Workflow（3 步）

### Step 1: 抓取数据
```bash
# 单个信源
python3 scripts/fetch_news.py --source weibo --no-save
python3 scripts/fetch_news.py --source meituan --no-save    # 美团技术 RSS

# 多个信源（逗号分隔）
python3 scripts/fetch_news.py --source weibo,zhihu_hot,baidu_hot --no-save

# 整层聚合
python3 scripts/fetch_news.py --source hot_rank --limit 10 --no-save    # 13 个热榜
python3 scripts/fetch_news.py --source tech_blogs --limit 5 --no-save   # 8 个科技信源

# 全量（broad scan）
python3 scripts/fetch_news.py --source all --limit 10 --deep --no-save

# 关键词过滤（自动展开："AI" → "AI,大模型,Qwen,通义,文心,豆包,混元,DeepSeek,Kimi,智谱"）
python3 scripts/fetch_news.py --source hot_rank --keyword "AI,大模型" --deep --no-save
```

### Step 2: 生成报告
读取 JSON，按统一模板渲染，**全部翻译为简体中文**。

### Step 3: 保存 & 呈现
报告保存到 `reports/YYYY-MM-DD/<source>_report.md`，并把完整内容展示给用户。

---

## 📰 统一早报模板

```markdown
# 🇨🇳 国内大厂早报 | YYYY-MM-DD

> **5 秒速览**：<一句话总结今日核心动态>

---

## 🔥 热搜速览（Top 15）

#### 1. [标题](url)
- **平台**: 微博热搜 | **热度**: 🔥 1234万 | **时间**: 实时
- **摘要**: 一句话中文摘要。
- **解读**: 💡 为什么上热搜？跟我们有什么关系？

---

## 🏢 大厂 / 科技动态（10+ 篇）

按信源分组：阿里 / 腾讯云 / 字节 / 华为 / 美团 / 京东 / 拼多多 / 网易 / 小米 等

每篇格式：
#### N. [标题](url)
- **来源**: CSDN / 量子位 | **时间**: 1h ago
- **摘要**: 一句话技术摘要。
- **深度**: 💡 技术价值、对国内技术生态的影响。

---

## 🧠 深度解读（5 分钟精读）

把今日所有信息"穿起来"，得出 2-3 条核心洞察。
```

---

## 🛠️ 工具

### fetch_news.py

| 参数 | 说明 | 默认 |
|---|---|---|
| `--source` | 信源 key（逗号分隔） | `all` |
| `--limit` | 每信源最多条数 | `10` |
| `--keyword` | 关键词过滤 | 无 |
| `--deep` | 抓详情页正文 | 关 |
| `--save` | 强制保存 | 自动 |
| `--no-save` | 不保存 | — |
| `--outdir` | 自定义输出目录 | `reports/YYYY-MM-DD/` |
| `--list-sources` | 列出所有信源 | — |
| `--no-cache` | 不用磁盘缓存 | 默认 10 分钟缓存 |

### 可用信源（21 个）

#### 🥇 第一层：国民级热榜（13 个，uapis.cn 公共 API）

| Key | 信源 | 备注 |
|---|---|---|
| `weibo` | 微博热搜 | 100+ 实时热搜 |
| `zhihu_hot` | 知乎热榜 | 含热度值 + 简介 |
| `bilibili_hot` | B站热门 | 视频播放量 |
| `baidu_hot` | 百度热搜 | 搜索指数 |
| `douyin_hot` | 抖音热点 | 视频热点 |
| `toutiao_hot` | 头条热榜 | 字节系新闻 |
| `huxiu` | 虎嗅 24h | 商业科技 |
| `36kr` | 36 氪快讯 | 创投资讯 |
| `ithome` | IT之家 | 数码科技 |
| `juejin` | 掘金热榜 | 程序员社区 |
| `thepaper` | 澎湃新闻 | 时政深度 |
| `sspai` | 少数派 | 数字生活方式 |
| `csdn` | CSDN 热文 | 程序员技术博客 |
| `hot_rank` | 🔀 13 个热榜聚合 | 全部并发 |

#### 🥈 第二层：科技 / 大厂动态（8 个）

| Key | 信源 | 类型 |
|---|---|---|
| `meituan` | 美团技术 | 官方 RSS |
| `qbitai` | 量子位 | 官方 RSS（AI 媒体） |
| `jiqizhixin` | 机器之心 | 官方 RSS（AI 媒体） |
| `csdn` | CSDN 热文 | 程序员社区 |
| `juejin` | 掘金热榜 | 程序员社区 |
| `sspai` | 少数派 | 数字生活 |
| `ithome` | IT之家 | 科技数码 |
| `36kr` | 36 氪 | 商业科技 |
| `thepaper` | 澎湃新闻 | 时政财经 |
| `tech_blogs` | 🔀 8 个科技信源聚合 | 全部并发 |

### daily_briefing.py（场景化早报）

```bash
python3 scripts/daily_briefing.py --profile <profile>
```

| Profile | 信源 | 指令文件 |
|---|---|---|
| `general` | 13 个热榜 + 8 个科技信源 | `instructions/briefing_general.md` |
| `tech` | 科技/大厂信源为主 | `instructions/briefing_tech.md` |
| `social` | 微博/知乎/B站/抖音/头条 | `instructions/briefing_social.md` |
| `ai_focus` | 量子位 + 机器之心 + 程序员社区 + 热搜 AI 关键词 | `instructions/briefing_ai_focus.md` |
| `business` | 36 氪 + 虎嗅 + 澎湃 + IT之家 | `instructions/briefing_business.md` |
| `morning` | 8 点早报（精简版） | `instructions/briefing_morning.md` |

**工作流**：执行脚本 → 读取对应指令文件 → 按指令 + 统一模板生成报告。

---

## ⚠️ 严格规则

1. **语言**：所有输出**简体中文**。英文专有名词保留（DeepSeek、Qwen 等）。
2. **时间**：必填字段。缺失时填 "未知时间"。
3. **反幻觉**：只用 JSON 里的数据。绝不编造。用 SVO 简单句。
4. **智能关键词展开**：
   - "AI" → "AI,大模型,LLM,通义千问,Qwen,文心一言,豆包,混元,盘古,DeepSeek,Kimi,智谱,GPT"
   - "云" → "云,阿里云,腾讯云,华为云,百度云,火山引擎"
   - "电商" → "电商,淘宝,天猫,京东,拼多多,抖音电商,小红书"
5. **智能补全**：结果 < 5 条时，扩展时间窗口补全，标记 ⚠️。
6. **保存**：始终保存到 `reports/YYYY-MM-DD/` 后再展示。

---

## 📋 交互菜单

当用户说"情报虾"或"打开菜单"：

1. 读取 `templates.md`
2. 展示菜单
3. 用 Universal Workflow 执行用户选择

---

## 🆘 不会用？看这里（AI 小白模式）

直接用自然语言说就行，比如：

- **"给我看一下今天的热搜"** → Agent 自动跑 `hot_rank`
- **"大厂今天有什么新动态"** → Agent 自动跑 `tech_blogs`
- **"AI 行业今天有什么新动态"** → Agent 自动跑 `ai_focus` 早报
- **"给我一份完整的早报"** → Agent 自动跑 `general` 早报
- **"查一下 DeepSeek 相关的新闻"** → Agent 自动用关键词过滤
- **"把今天的报告存下来"** → Agent 自动加 `--save`
- **"只要微博的内容"** → `--source weibo`
- **"微博 + 知乎"** → `--source weibo,zhihu_hot`

只要像跟人说话一样说需求，Agent 会帮你跑命令 + 整理报告。

---

## Requirements

- Python 3.8+
- `pip install -r requirements.txt` （requests + beautifulsoup4）
- 不再需要 Playwright
- **无需任何 API Key** — 全部走 uapis.cn 公共 API

---

## 🔄 升级日志

### v3.1（2026-06-09）
- **架构升级**：所有热榜改走 `uapis.cn` 公共聚合 API（无需 Key、稳定）
- **去掉 Playwright**：纯 requests + bs4
- **加磁盘缓存**：避免重复抓取
- **串行 + 间隔**：避免触发 API 限流
- **21 个信源**：13 个热榜 + 8 个科技信源

### v2.0（初版国内大厂版）
- 17 个国内信源：5 个热榜 + 12 个大厂技术博客
- 用 HTML 解析抓大厂博客（部分受反爬限制）

### v1.0（原版）
- 28 个海外信源（HN/PH/Medium/Github 等）
- 需要 Playwright
