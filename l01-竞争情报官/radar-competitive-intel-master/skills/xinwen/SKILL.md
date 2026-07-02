# 新闻情报雷达

> 不是告诉你发生了什么，而是帮你判断什么该看、为什么重要、下一步该怎么办。

## 简介

新闻情报雷达 —— 专为信息过载场景设计的新闻分级决策工具。自动将海量新闻分为🔴关键/🟡关注/⚪一般/🔇噪音四级，语义去重合并重复报道，根据用户画像自适应排序，输出带影响判断和行动建议的决策简报。支持话题追踪联动，零配置开箱即用。

## 核心能力

- **四级智能分级**：基于多源覆盖度、热度、画像匹配度、信源可信度四维评分，自动判定每条新闻的优先级
- **语义去重合并**：同一事件多源报道自动合并，保留不同视角，不再重复刷屏
- **决策简报**：按价值而非来源分类，每条关键情报附带影响判断和建议行动，不是"新闻列表"而是"决策备忘"
- **用户画像自适应**：读取USER.md和MEMORY.md，自动匹配关注领域，你的行业新闻优先级更高
- **话题追踪联动**：一键生成追踪命令模板，与topic_tracking技能联动，持续跟踪关键事件
- **30+信源支撑**：全球科技、开源社区、国内资讯、金融财经、AI深度五大分类，所有抓取走公开接口/RSS，零配置
- **快速扫描模式**：10秒内只看最关键的3-5条，适合碎片时间

## 触发方式

当用户说以下内容时触发：
- 新闻雷达、情报雷达
- 今日简报、有什么重要的
- 科技早报、财经早报、AI早报
- 快速看看、扫描一下

## 使用方式

### 快速扫描（只看关键和关注，5条以内）

```
python3 scripts/intelligence.py --mode quick
```

适用场景：快速了解最重要的几条情报，适合碎片时间。10-20秒完成。

### 每日情报（完整抓取+全量分析）

```
python3 scripts/intelligence.py --mode daily
```

适用场景：每天早晨的完整情报扫描，获取全面分析。

### 领域深挖（单领域详细分析）

```
python3 scripts/intelligence.py --mode topic --topic AI深度
```

支持的话题：全球科技、开源社区、国内资讯、金融财经、AI深度

### 追踪更新（按关键词追踪）

```
python3 scripts/intelligence.py --mode trace --keyword "GPT-5"
```

适用场景：追踪特定话题的最新动态。

### JSON输出（调试/程序调用）

```
python3 scripts/intelligence.py --mode quick --json
```

## 分级说明

| 等级 | 含义 | 判定规则 |
|------|------|----------|
| 🔴关键 | 必须关注 | 3+源同时报道，或综合评分≥65，或与用户核心领域高度匹配 |
| 🟡关注 | 值得留意 | 2源报道，或综合评分40-64，或与用户领域间接相关 |
| ⚪一般 | 可选浏览 | 单源报道，热度一般，评分<40 |
| 🔇噪音 | 已折叠 | 重复/广告/营销/与用户领域无关 |

## 信源一览

| 分类 | 信源 | 抓取方式 |
|------|------|----------|
| 全球科技 | Hacker News、Product Hunt、TechCrunch、The Verge、Ars Technica | API/RSS/爬虫 |
| 开源社区 | GitHub Trending、GitHub Show HN、V2EX | API/爬虫 |
| 国内资讯 | 36氪、微博热搜、IT之家、腾讯科技、知乎热榜、B站热门 | API/爬虫 |
| 金融财经 | 东方财富、雪球、华尔街见闻、财联社 | API/爬虫 |
| AI深度 | HuggingFace Papers、ArXiv AI、8个AI Newsletter RSS源 | RSS |

## 话题追踪

对任意情报说"追踪"，系统将：
1. 自动提取追踪关键词
2. 生成初始快照
3. 输出追踪命令模板

示例输出：
```
帮我追踪/关注 "GPT-5 OpenAI"
追踪关键词：GPT-5、OpenAI、大模型
初始快照：{...}
```
将命令发送给主助手即可启动话题追踪。

## 用户画像

首次使用时自动读取工作目录下的 `USER.md` 和 `MEMORY.md`，提取关注领域关键词。无画像文件时使用内置默认画像（AI/科技/金融）。

## 依赖

仅需：`requests`、`beautifulsoup4`

其余功能使用Python标准库实现（json, re, datetime, concurrent.futures, collections, math, os, sys, argparse, hashlib）。

## 文件结构

```
├── SKILL.md                    # 本文件
├── scripts/
│   ├── intelligence.py         # 主引擎
│   ├── fetch_sources.py        # 30+信源抓取
│   ├── classifier.py           # 智能分级
│   ├── deduplicator.py         # 语义去重合并
│   ├── profiler.py             # 用户画像
│   ├── tracker.py              # 话题追踪联动
│   └── briefing.py             # 简报格式化
├── instructions/
│   ├── daily_intel.md          # 每日情报指令
│   ├── quick_scan.md           # 快速扫描指令
│   └── topic_trace.md          # 话题追踪指令
├── references/
│   ├── classification_rules.md # 分级规则详解
│   ├── dedup_strategy.md       # 去重策略说明
│   └── source_config.md        # 信源配置
├── reports/                    # 简报输出目录
│   └── .gitkeep
└── requirements.txt            # 依赖声明
```

## 注意事项

- 部分信源可能因网络环境无法访问，系统会自动跳过并继续
- 抓取过程有超时和异常兜底，不会因单个信源失败而崩溃
- 微博、知乎等平台API可能不定期变更，如抓取失败请反馈
- 华尔街见闻受Cloudflare保护，可能无法抓取，系统用东方财富+雪球替代
