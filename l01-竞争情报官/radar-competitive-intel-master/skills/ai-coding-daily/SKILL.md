---
name: ai-coding-daily
description: "AI Coding & Agent 情报日报生成器。每日自动采集 GitHub Trending、Hacker News、官方博客 RSS（Anthropic/OpenAI/Google DeepMind/GitHub/HuggingFace/Cursor）、Twitter/X 核心账号、ArXiv 最新论文、微信公众号（机器之心/量子位）等多渠道信息，过滤 AI Coding 和 Agent 相关内容，由 AI 生成带「臣按」点评的宫廷体情报日报，并发布到学城文档。当用户说「生成日报」「出今天的日报」「AI Coding 日报」「情报日报」「跑日报」时触发。也可用于手动触发单次生成或配置定时自动化任务。"
---

# AI Coding & Agent 情报日报

每日自动采集多渠道信息，生成带深度点评的 AI Coding & Agent 情报日报，发布到学城。

## 快速开始

首次使用前检查依赖：

```bash
python3 ~/.catpaw/skills/ai-coding-daily/scripts/setup.py
```

生成今日日报：

```bash
python3 ~/.catpaw/skills/ai-coding-daily/scripts/fetch_all.py
```

脚本会依次采集所有信息源，输出结构化 JSON，然后由 AI 生成日报正文并发布到学城。

---

## 完整工作流

### Step 1：并行采集所有信息源

同时运行以下三个采集脚本（可并行执行，互不依赖）：

```bash
# 采集 GitHub Trending + HN
python3 ~/.catpaw/skills/ai-coding-daily/scripts/fetch_github_trending.py > /tmp/ai-daily-github.json
python3 ~/.catpaw/skills/ai-coding-daily/scripts/fetch_hn.py > /tmp/ai-daily-hn.json

# 采集 RSS 博客 + Twitter/X + ArXiv
python3 ~/.catpaw/skills/ai-coding-daily/scripts/fetch_rss.py > /tmp/ai-daily-rss.json
```

如果某个脚本失败，跳过该信息源，继续生成日报，在日报末尾注明「本期 XX 信息源采集失败，已跳过」。

### Step 1.5：无 RSS 信息源的 web_search 补充采集

以下重要信息源没有公开 RSS，需要通过 web_search 工具补充采集最近 7 天的文章：

- **Anthropic**：搜索 `site:anthropic.com/news after:{7天前日期}`
- **Claude Blog**：搜索 `site:anthropic.com/claude after:{7天前日期}`（Claude 产品更新单独搜索）
- **Google DeepMind**：搜索 `site:deepmind.google/discover/blog after:{7天前日期}`
- **Mistral**：搜索 `site:mistral.ai/news after:{7天前日期}`
- **Cursor**：搜索 `site:cursor.com/changelog after:{7天前日期}`
- **GitHub Blog**：搜索 `site:github.blog "copilot" OR "agent" after:{7天前日期}`
- **OpenAI**：搜索 `site:openai.com/blog after:{7天前日期}`（RSS 可能不稳定时补充）

对每个搜索结果，用 web_fetch 或 defuddle skill 获取文章标题和摘要（前 300 字即可）。

**补充采集优先级**：Anthropic/Claude Blog > GitHub Blog > OpenAI > Cursor > DeepMind > Mistral。如果时间有限，至少完成前三个。

### Step 2：微信公众号补充采集（可选，需 all-net-search-read skill）

如果 all-net-search-read skill 可用，额外搜索以下公众号最新文章（最近 24 小时内）：

- 机器之心（jiqizhixin）
- 量子位（QbitAI）
- AI科技评论

搜索关键词：`AI Coding Agent 大模型` + 今日日期

### Step 3：AI 生成日报正文

读取 `references/template.md` 中的日报模板，结合采集到的数据，按以下规则生成正文：

**内容筛选原则**
- 只保留与 AI Coding、Agent、LLM 工具链、代码生成、AI 辅助开发相关的内容
- GitHub 项目：今日 Star 增量 > 200 或本周 > 1000 才纳入
- HN 帖子：分数 > 100 才纳入
- RSS/web_search 文章：来自核心信息源（见 `references/sources.md`）的所有文章都纳入
- ArXiv 论文：只纳入与 Agent/Coding/Tool Use 直接相关的论文

**行业动态合并规则**
同一公司/产品在同一时期的多条动态，合并为一条行业动态，避免碎片化。例如：
- Claude Blog 同期发布多篇更新 → 合并为「Claude Managed Agents 全面升级」一条，正文中列出各篇文章链接
- Cursor 同期发布多个 Changelog → 合并为「Cursor 近期更新」一条

**链接质量要求**
- 所有 GitHub 项目链接必须是真实存在的 `https://github.com/{owner}/{repo}` 格式
- 文章链接从 RSS 或 web_search 结果中获取原始 URL，不得编造
- 如果无法获取真实链接，宁可不加链接，也不要写假链接

**「臣按」点评规则**
每条信息必须附一段「臣按」，要求：
- 不超过 80 字
- 给出明确判断，不说废话（禁止「值得关注」「有一定价值」等模糊表述）
- 指出该信息对 AI Coding 产品/工程实践的具体影响
- 风格：宫廷奏折体，但观点要犀利

**头条选择**
从所有信息中选出 1-2 条最重要的作为「本期头条」，判断标准：
- 来自 Anthropic/OpenAI/Google 的重大产品发布
- HN 分数 > 300 的讨论
- GitHub 今日 Star > 2000 的新项目

### Step 4：输出日报正文

直接将生成的日报正文完整输出到对话中，不做任何自动发布操作。


**如果用户希望发布到其他地方**（如飞书、Notion、本地文件等），按用户指定方式处理。

---

## 信息源体系

详见 `references/sources.md`，包含所有信息源的 URL、采集频率、过滤关键词配置。

## 日报模板

详见 `references/template.md`，包含完整的日报结构和各板块的生成规则。

## 脚本说明

| 脚本 | 功能 | 输出 |
|------|------|------|
| `scripts/setup.py` | 检查并安装依赖 | 控制台输出 |
| `scripts/fetch_github_trending.py` | 采集 GitHub Trending | JSON |
| `scripts/fetch_hn.py` | 采集 Hacker News | JSON |
| `scripts/fetch_rss.py` | 采集 RSS + ArXiv | JSON |
| `scripts/fetch_all.py` | 一键采集所有信息源 | JSON |

---

## 定时自动化

如需每日自动生成，使用 CatDesk 自动化功能：

```
catdesk automation create \
  --name "AI Coding 日报" \
  --prompt "运行 ai-coding-daily skill，生成今日 AI Coding & Agent 情报日报并发布到学城" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=9;BYMINUTE=0"
```

工作日早 9 点自动触发，生成并发布日报。

---

## 故障排查

**GitHub Trending 采集失败**：GitHub 无官方 API，通过解析 HTML 页面获取。如遇反爬，等待 10 分钟后重试，或手动访问 `https://github.com/trending` 复制内容。

**RSS 采集超时**：部分境外 RSS 源（如 Anthropic Blog）可能需要代理。设置 `HTTP_PROXY` 环境变量后重试。

**citadel 认证失败**：运行 `oa-skills citadel --clear-cache` 后重试。

**all-net-search-read 不可用**：微信公众号板块跳过，其他板块不受影响。
