# 🗞️ 情报虾 · 国内大厂新闻聚合器

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Sources](https://img.shields.io/badge/sources-21%2B-brightgreen.svg)]()
[![Zero Config](https://img.shields.io/badge/config-zero-blueviolet.svg)]()

> **国内一线大厂新闻聚合，专为 AI Agent 打造的高效信息引擎。**
> v3.1 · 21 个信源 · 零配置 · 全程防限流

---

## ✨ 核心特性

- **🌍 国内全源覆盖**：一站式覆盖 13 个国民级热榜 + 8 个科技/大厂信源
- **🚀 零配置即用**：**无需任何 API Key** — 全部走 `uapis.cn` 公共热榜聚合 API + 3 个官方 RSS
- **🛡️ 防限流设计**：串行调用 + 1.5 秒间隔 + 磁盘缓存（10 分钟 TTL）
- **🧠 AI 智能阅读**：智能抓取详情页正文（Deep 模式），交给大模型过滤、提炼、总结
- **📰 场景化早报**：6 套早报 Profile（综合/科技/吃瓜/AI/商业/精简），一键生成杂志级 Markdown 报告
- **🪄 自然语言交互**：支持"情报虾"口令唤醒菜单，用人话即可触发

---

## 📚 信源图谱（21 个）

### 🥇 第一层：国民级热榜（13 个，走 uapis.cn 公共 API）

- **社交/讨论**：🔴 微博热搜 / 💭 知乎热榜 / 📺 B站热门 / 🎵 抖音热点 / 📰 头条热榜
- **资讯/商业**：🦊 虎嗅 24h / ⚡ 36 氪快讯 / 📜 澎湃新闻 / 💻 IT 之家
- **技术/社区**：⚛️ 掘金热榜 / 🎯 少数派 / 📚 CSDN 热文 / 🔍 百度热搜

### 🥈 第二层：科技/大厂动态（8 个）

- **官方 RSS（2026 年实测可用）**：🍱 美团技术 / 🤖 量子位 / 🧠 机器之心
- **科技媒体**：💻 CSDN / ⚛️ 掘金 / 🎯 少数派 / 💻 IT 之家 / ⚡ 36 氪 / 📜 澎湃新闻

> **为什么"大厂技术博客"层改用科技媒体？**
> 2026 年国内大厂官方技术博客（阿里云/腾讯云/字节/华为/百度AI/小米/360 等）100% 加了反爬验证（Cloudflare 验证或 403 Forbidden）。**对国内大厂的深度报道，80% 来自 CSDN 程序员社区和 IT 之家、IT 桔子、36 氪等科技媒体**。所以 v3.1 用科技媒体覆盖"大厂视角"，更稳定、内容更丰富。

---

## 📥 安装

### 1. 复制到项目
```bash
cp -r news-aggregator-skill YourProject/.claude/skills/
```

### 2. 安装依赖
```bash
cd news-aggregator-skill
pip install -r requirements.txt   # 只有 requests + beautifulsoup4
```

> **不需要 Playwright，不需要任何 API Key！**

---

## 🚀 使用方法

### 1. 命令行（直接调用）

```bash
# 列出所有信源
python3 scripts/fetch_news.py --list-sources

# 单个信源
python3 scripts/fetch_news.py --source weibo --no-save
python3 scripts/fetch_news.py --source meituan --no-save    # 美团官方 RSS

# 多个信源（逗号分隔）
python3 scripts/fetch_news.py --source weibo,zhihu_hot,baidu_hot --no-save

# 整层聚合
python3 scripts/fetch_news.py --source hot_rank --limit 10 --no-save    # 13 个热榜
python3 scripts/fetch_news.py --source tech_blogs --limit 5 --no-save   # 8 个科技信源

# 关键词过滤（自动展开："AI" → "AI,大模型,Qwen,通义,文心,豆包,混元,DeepSeek"）
python3 scripts/fetch_news.py --source hot_rank --keyword "AI,大模型" --deep --no-save

# 完整报告（带 Deep 详情）
python3 scripts/fetch_news.py --source all --limit 10 --deep --no-save
```

### 2. 场景化早报

```bash
python3 scripts/daily_briefing.py --profile general --no-save    # 综合早报
python3 scripts/daily_briefing.py --profile tech --no-save       # 科技大厂早报
python3 scripts/daily_briefing.py --profile social --no-save     # 吃瓜早报
python3 scripts/daily_briefing.py --profile ai_focus --no-save   # AI 行业早报
python3 scripts/daily_briefing.py --profile business --no-save   # 商业资讯早报
python3 scripts/daily_briefing.py --profile morning --no-save    # 8 点精简早报
```

### 3. 交互菜单

> **"情报虾"** 或 **"打开菜单"** → Agent 弹出 30 个选项的菜单

### 4. 自然语言（推荐）

直接用中文跟 Agent 说：
- *"给我看一下今天的热搜"* → Agent 自动跑 `hot_rank`
- *"大厂今天有什么新闻"* → Agent 自动跑 `tech_blogs`
- *"AI 行业今天发生了什么"* → Agent 自动跑 `ai_focus` 早报
- *"查一下 DeepSeek 相关的"* → Agent 自动用关键词过滤
- *"把今天的报告存下来"* → Agent 自动加 `--save`

---

## 📊 性能指标

| 指标 | 数值 |
|---|---|
| 信源数 | 21 |
| 零配置 | ✅ 无需任何 API Key |
| 抓取时间（hot_rank 13 个信源） | ~25 秒（含 1.5 秒礼貌间隔） |
| 抓取时间（tech_blogs 8 个信源） | ~15 秒 |
| 抓取时间（general 早报全套） | ~50 秒 |
| 缓存 TTL | 10 分钟（磁盘） |
| 限流风险 | 0（串行 + 间隔） |
| 数据总量（一次 general 早报） | 300+ 条 |

---

## 🔧 进阶

### 自定义输出目录
```bash
python3 scripts/fetch_news.py --source hot_rank --outdir /path/to/output
```

### 不使用缓存
```bash
python3 scripts/fetch_news.py --source hot_rank --no-cache --no-save
```

### Deep 模式（抓详情页正文）
```bash
python3 scripts/fetch_news.py --source hot_rank --deep --no-save
```

---

## 📜 License

MIT License

---

## 🔄 版本

- **v3.1** (2026-06-09) — 全部走 uapis.cn 公共 API，零配置、零限流
- **v2.0** (2026-06-09) — 国内大厂版（HTML 抓大厂博客，受反爬影响）
- **v1.0** — 原版海外 28 信源（HN/PH/Newsletters/Podcasts/Essays）
