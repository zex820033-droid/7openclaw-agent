# 信息源配置

## 一级信息源（每日必采）

### GitHub Trending

采集地址：`https://github.com/trending?since=daily&spoken_language_code=`（今日趋势）和 `https://github.com/trending?since=weekly`（本周趋势）

过滤关键词（项目描述或名称包含以下任意词即纳入）：
```
agent, coding, llm, ai, copilot, claude, gpt, gemini, cursor, 
code generation, code assistant, mcp, tool use, agentic,
memory, rag, context, prompt, inference, transformer
```

排除关键词（避免噪音）：
```
game, minecraft, web scraper, crypto, blockchain, nft
```

采集字段：`repo_name`, `description`, `stars_today`, `stars_week`, `language`, `url`

---

### Hacker News

API 地址：`https://hacker-news.firebaseio.com/v0/topstories.json`（获取 top 500 帖子 ID）
单帖详情：`https://hacker-news.firebaseio.com/v0/item/{id}.json`

过滤规则：
- 分数 > 100
- 标题包含 AI 相关关键词（见下方关键词表）
- 或 URL 域名属于核心信息源域名列表

AI 相关关键词：
```
AI, LLM, GPT, Claude, Gemini, Copilot, Cursor, agent, coding assistant,
code generation, Anthropic, OpenAI, Google DeepMind, HuggingFace,
MCP, tool use, agentic, RAG, context window, inference, transformer,
Llama, Mistral, Qwen, DeepSeek
```

采集字段：`id`, `title`, `url`, `score`, `descendants`（评论数）, `time`

---

### 官方博客 RSS（有 RSS Feed）

| 信息源 | RSS URL | 优先级 |
|--------|---------|--------|
| OpenAI Blog | `https://openai.com/news/rss.xml` | ⭐⭐⭐ |
| GitHub Blog | `https://github.blog/feed/` | ⭐⭐⭐ |
| Cursor Changelog | `https://cursor.com/changelog/rss.xml` | ⭐⭐⭐ |
| HuggingFace Blog | `https://huggingface.co/blog/feed.xml` | ⭐⭐ |
| The Verge | `https://www.theverge.com/rss/index.xml` | ⭐⭐ |
| LangChain Blog | `https://blog.langchain.dev/rss/` | ⭐⭐ |
| Simon Willison | `https://simonwillison.net/atom/everything/` | ⭐⭐ |
| Lilian Weng Blog | `https://lilianweng.github.io/index.xml` | ⭐⭐ |

过滤规则：只保留最近 7 天内发布的文章，且标题/摘要包含 AI Coding 相关关键词。

### 无 RSS 的重要信息源（通过 web_search 补充）

| 信息源 | 网页地址 | 优先级 | 采集方式 |
|--------|---------|--------|---------|
| Anthropic Blog | `https://www.anthropic.com/news` | ⭐⭐⭐ | `web_search site:anthropic.com/news after:{7天前}` |
| Claude Blog | `https://www.anthropic.com/claude` | ⭐⭐⭐ | `web_search site:anthropic.com/claude after:{7天前}` |
| Google DeepMind | `https://deepmind.google/discover/blog/` | ⭐⭐⭐ | `web_search site:deepmind.google after:{7天前}` |
| Mistral Blog | `https://mistral.ai/news/` | ⭐⭐ | `web_search site:mistral.ai/news after:{7天前}` |

**注意**：Cursor Changelog 和 GitHub Blog 已有 RSS，优先走 RSS 采集；若 RSS 失效则改用 web_search 补充。

---

### ArXiv 论文

API 地址：`http://export.arxiv.org/api/query`

查询参数：
```
search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.SE
sortBy=submittedDate
sortOrder=descending
max_results=50
```

过滤规则：标题或摘要包含以下关键词：
```
agent, code generation, coding assistant, tool use, agentic,
software engineering, program synthesis, LLM, large language model
```

只保留最近 3 天内提交的论文。

采集字段：`title`, `authors`, `abstract`（前 200 字）, `url`, `submitted_date`

---

## 二级信息源（补充深度，需 all-net-search-read skill）

### Twitter/X 核心账号

通过 `x_scraper.py` 采集以下账号最近 24 小时的推文：

| 账号 | 关注原因 |
|------|---------|
| @AnthropicAI | Claude/Claude Code 官方动态 |
| @OpenAI | GPT/Codex/Operator 官方动态 |
| @GithubCopilot | Copilot 产品更新 |
| @cursor_ai | Cursor 产品更新 |
| @karpathy | AI 领域最具影响力的技术声音 |
| @sama | OpenAI CEO，战略方向信号 |
| @darioamodei | Anthropic CEO |
| @ylecun | Meta AI 首席科学家，技术争论 |
| @huggingface | HuggingFace 官方 |
| @LangChainAI | LangChain 官方 |
| @swyx | AI 工程师社区意见领袖 |
| @simonw | Simon Willison，AI 工具实践 |

过滤规则：转发数 > 50 或点赞数 > 200 的推文才纳入。

### 微信公众号

通过 all-net-search-read skill 搜索以下公众号最新文章：

| 公众号 | 关注原因 |
|--------|---------|
| 机器之心 | AI 技术深度报道，中文最权威 |
| 量子位 | AI 产品动态，速度快 |
| AI科技评论 | 学术与工程结合 |
| 硅星人Pro | 硅谷 AI 公司动态 |

搜索策略：`{公众号名} AI Coding Agent {今日日期}`，取最近 24 小时内的文章。

---

## 关键词过滤总表

以下关键词用于所有信息源的统一过滤（大小写不敏感）：

```python
AI_CODING_KEYWORDS = [
    # 工具和产品
    "claude code", "copilot", "cursor", "devin", "codex", "aider",
    "codeium", "tabnine", "replit", "github copilot", "opencode",
    
    # 技术概念
    "ai coding", "code generation", "code assistant", "coding agent",
    "agentic", "agent", "multi-agent", "tool use", "function calling",
    "mcp", "model context protocol",
    
    # 模型和公司
    "anthropic", "claude", "openai", "gpt-4", "gpt-5", "gemini",
    "llama", "mistral", "deepseek", "qwen",
    
    # 工程实践
    "rag", "context window", "prompt engineering", "fine-tuning",
    "inference", "latency", "token", "embedding",
    
    # 新兴方向
    "recursive self-improvement", "self-play", "synthetic data",
    "spec-driven", "test-driven", "memory", "long-term memory"
]
```
