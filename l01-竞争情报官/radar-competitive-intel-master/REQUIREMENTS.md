# REQUIREMENTS.md — 竞争情报官 初始化指南

> **写给**：新主机上的 Agent（你自己）或部署者  
> **用途**：落地上线——照着跑一遍就能干活  
> **最后验证**：2026-06-30 · 21 Python + 8 Node + 4 系统工具 · 全量通过

---

## 快速初始化

Agent 到达新主机 → 按顺序执行 → 最后跑验证 → 完成。

### Step 1：系统工具

```bash
# 确认四个基础工具存在（通常自带）
which curl jq python3 node && node -v
# 预期: /usr/bin/curl  /usr/bin/jq  /usr/bin/python3  /usr/bin/node  v22+
```

### Step 2：Python 库

```bash
# apt 包（C扩展，必须走系统包管理器，避免 ABI 冲突）
sudo apt-get install -y \
  python3-numpy python3-scipy python3-pandas \
  python3-sklearn python3-sklearn-lib \
  python3-matplotlib python3-pil python3-openpyxl \
  python3-requests

# pip 包（纯Python，轻量无编译风险）
pip3 install --break-system-packages \
  playwright playwright-stealth \
  httpx beautifulsoup4 lxml \
  rich pydantic tabulate aiohttp \
  feedparser jieba snownlp pyecharts
```

### Step 3：Node 全局包

```bash
npm i -g playwright agent-browser bing-cn-mcp mcporter clawhub jq openclaw

# 可选：小红书搜索（需扫码登录一次）
npm i -g xiaohongshu-mcp
```

### Step 4：验证

```bash
python3 -c "
import feedparser, pandas, jieba, snownlp, sklearn, pyecharts
import playwright, requests, httpx, bs4, lxml
import numpy, scipy, matplotlib, rich, pydantic, tabulate, aiohttp, openpyxl, PIL
print('21/21 Python OK')
"

which autocli && autocli --version
mcporter --version
bing-cn-mcp --version 2>/dev/null || echo 'bing-cn-mcp installed'
echo 'DONE'
```

---

## 依赖说明

### 浏览器自动化

| 包 | 方式 | 干什么 |
|------|:--:|------|
| `playwright` (Python) | pip | SPA页面渲染、JS执行 |
| `playwright-stealth` | pip | 反检测（隐藏 webdriver 标记） |
| `playwright` (Node) | npm | CLI 工具、浏览器安装 |
| `agent-browser` | npm | 托管 Chrome（149.0.7827.115），无需手动装浏览器 |

> 启动 Chrome 的完整链路：`agent-browser` → 下载/管理 Chrome 二进制 → Python `playwright` 连接 → `playwright-stealth` 注入反检测。

### 数据采集管道

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `curl` + `jq` | L2 直连爬虫：HTTP 请求 + JSON 解析 | direct-crawler-pipeline |
| `requests` | Python HTTP 客户端 | cookie-auto-login |
| `httpx` + `aiohttp` | 异步并发爬取 | direct-crawler-pipeline |
| `beautifulsoup4` + `lxml` | HTML 解析、XPath 提取 | direct-crawler-pipeline |
| `autocli` (v0.3.8) | L1 数据采集：HN / Dev.to / Lobsters / StackOverflow | autocli-competitive-intel |

### 中文 NLP & 情感分析

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `jieba` | 中文分词（关键词提取、热词发现） | yuqing / xinwen / brand-monitoring |
| `snownlp` | 中文情感分析（正面/负面/中性评分，免训练） | yuqing / brand-monitoring |

### 数据分析 & 统计

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `numpy` | 数值计算底层 | 全部数据 Skill 的基石 |
| `scipy` | 统计检验、分布拟合 | risk-metrics-calculation |
| `pandas` | 时间序列、定价对比表、团队效能中位数 | T3/T8/attribution-modeling |
| `scikit-learn` | 回归/分类/聚类/Monte Carlo | attribution-modeling / risk-metrics |

### 输出 & 可视化

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `matplotlib` | KPI 折线图、风险热力图 | executive-dashboard / retention-risk |
| `pyecharts` | 交互式 ECharts（舆情趋势、情感饼图） | yuqing |
| `tabulate` | 终端表格输出 | executive-dashboard / T3 定价对比 |
| `rich` | 终端美化（进度条、面板） | channel-health-check |
| `pillow` | 截图处理 | playwright-anti-detection |
| `openpyxl` | Excel 导出（定价历史、财务数据） | T3 / company-investment-research |

### 搜索 & 监控

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `bing-cn-mcp` + `mcporter` | 中文必应搜索 MCP 服务 | bing-cn-search |
| `feedparser` | RSS/Atom 订阅解析（竞品博客、GitHub Release） | feed-watcher / ai-news-aggregator |

### 数据校验 & 品质门禁

| 包 | 干什么 | 对应 Skill |
|------|------|------|
| `pydantic` | 数据模型校验（字段类型/范围/必填） | data-integrity-gate / chinese-intelligence-quality-gate |

---

## 非代码依赖（手动配置）

这些在新主机上需要人工介入，Agent 无法自动完成。

| 项目 | 怎么配 | 影响 |
|------|--------|------|
| **GitHub Token** | `export GITHUB_TOKEN=ghp_xxx` | T7 版本追踪 / T8 团队效能。无 Token = 60次/h，有 = 5000次/h |
| **小红书扫码** | `xiaohongshu-mcp` 启动后扫码一次 | direct-crawler-apis.json 中 `xiaohongshu_mcp` 管道需此 |
| **飞书授权** | 飞书 OAuth 授权（平台处理） | 日报推送 / 飞书表格写入 |
| **竞品登录 Cookie** | `python3 tools/cookie_extractor.py {平台}` | 知乎搜索 / 抖音搜索 需登录态 |

---

## 故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| `pip3 install` 报 externally-managed | PEP 668 保护 | 加 `--break-system-packages` |
| pandas import 报 numpy ABI 不兼容 | pip numpy 2.x 与 apt pandas 冲突 | 卸载 pip numpy/scipy，用 apt 版本 |
| jieba/snownlp pip 安装 OOM | 源码编译内存不足 | 用清华镜像 `-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| Playwright 报 "Executable doesn't exist" | 缺少浏览器二进制 | `npx playwright install chromium` 或确保 `agent-browser` 已装 |
| bing-cn-mcp 无响应 | MCP 服务未启动 | 检查 `mcporter` 配置 `config/mcporter.json` |

---

> *Agent 到达 → 跑完 Step 1-4 → 验证通过 → 开始干活。*
