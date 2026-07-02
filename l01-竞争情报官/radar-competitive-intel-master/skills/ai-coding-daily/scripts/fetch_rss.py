#!/usr/bin/env python3
"""
RSS + ArXiv 采集脚本
采集官方博客 RSS 和 ArXiv 最新论文
输出 JSON 到 stdout
"""

import json
import sys
import re
import time
import subprocess
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET

# RSS 信息源配置（已验证可访问的 URL）
RSS_SOURCES = [
    # OpenAI - 有效
    {"name": "OpenAI Blog", "url": "https://openai.com/news/rss.xml", "priority": 3},
    # GitHub Blog - 有效
    {"name": "GitHub Blog", "url": "https://github.blog/feed/", "priority": 3},
    # HuggingFace Blog - 有效
    {"name": "HuggingFace Blog", "url": "https://huggingface.co/blog/feed.xml", "priority": 2},
    # Cursor Changelog - 有效
    {"name": "Cursor Changelog", "url": "https://cursor.com/changelog/rss.xml", "priority": 3},
    # The Verge（全站 RSS，通过关键词过滤 AI 内容）
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "priority": 2},
    # LangChain Blog（RSS 有时格式不规范，容错处理）
    {"name": "LangChain Blog", "url": "https://blog.langchain.dev/rss/", "priority": 2},
    # Simon Willison's blog（AI 工具实践权威）
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "priority": 2},
    # Lilian Weng's blog（OpenAI 研究员，深度技术文章）
    {"name": "Lilian Weng Blog", "url": "https://lilianweng.github.io/index.xml", "priority": 2},
]

# 无 RSS 的重要信息源，通过 web_search 补充采集（在 SKILL.md 中说明）
# - Anthropic Blog: https://www.anthropic.com/news（无 RSS，需 web_search）
# - Google DeepMind: https://deepmind.google/discover/blog/（无 RSS，需 web_search）
# - Mistral Blog: https://mistral.ai/news/（无 RSS，需 web_search）

# ArXiv API
ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_QUERY = "cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.SE"
ARXIV_MAX = 50

# 时间范围
MAX_AGE_DAYS_RSS = 7    # RSS 文章最多 7 天
MAX_AGE_DAYS_ARXIV = 3  # ArXiv 论文最多 3 天

# AI Coding 关键词
AI_KEYWORDS = {
    "agent", "agents", "agentic", "coding", "llm", "copilot",
    "claude", "gpt", "gemini", "cursor", "code generation", "code assistant",
    "mcp", "tool use", "memory", "rag", "context", "prompt", "inference",
    "transformer", "anthropic", "openai", "deepmind", "huggingface",
    "langchain", "mistral", "llama", "deepseek", "qwen",
    "codeium", "devin", "opencode", "multi-agent", "function calling",
    "fine-tuning", "synthetic data", "recursive self-improvement",
    "large language model", "language model", "ai coding",
    "software engineering", "program synthesis", "automated coding"
}

# 优先级 3 的信息源（所有文章都纳入，不过滤关键词）
HIGH_PRIORITY_SOURCES = {"Anthropic Blog", "Anthropic Research", "OpenAI Blog",
                          "Google DeepMind", "GitHub Blog", "Cursor Changelog",
                          "Simon Willison", "Lilian Weng Blog", "The Verge"}


def fetch_url(url, timeout=15):
    """获取 URL 内容，优先用 curl（绕过 403），失败时回退到 urllib"""
    # 优先用 curl，避免 Python urllib 被网站屏蔽
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout),
             "-H", "Accept: application/rss+xml, application/xml, text/xml, */*",
             "-H", "Accept-Encoding: identity",
             url],
            capture_output=True, timeout=timeout + 5
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.decode("utf-8", errors="replace")
        # curl 失败，记录原因
        if result.returncode != 0:
            print(f"[WARN] curl({url}) exit={result.returncode}", file=sys.stderr)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"[WARN] curl not available or timed out: {e}", file=sys.stderr)

    # 回退到 urllib
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError) as e:
        print(f"[WARN] fetch_url({url}) failed: {e}", file=sys.stderr)
        return None


def get_text(el):
    """获取元素文本，兼容 CDATA 和混合内容（用 itertext 拼接）"""
    if el is None:
        return ""
    return "".join(el.itertext()).strip()


def parse_date(date_str):
    """解析多种日期格式"""
    if not date_str:
        return None
    date_str = date_str.strip()

    # RFC 2822 格式（RSS 常用）
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    # 尝试去掉时区名称后解析
    cleaned = re.sub(r"\s+[A-Z]{2,4}$", "", date_str)
    try:
        dt = datetime.strptime(cleaned, "%a, %d %b %Y %H:%M:%S")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    return None


def is_recent(dt, max_age_days):
    """判断是否在时间范围内"""
    if not dt:
        return True  # 无法判断时间，默认纳入
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    return dt >= cutoff


def is_ai_related(title, description=""):
    """判断是否与 AI 相关"""
    text = (title + " " + description).lower()
    for kw in AI_KEYWORDS:
        if kw in text:
            return True
    return False


def parse_rss(xml_content, source_name, priority):
    """解析 RSS XML，返回文章列表"""
    articles = []
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"[WARN] parse_rss({source_name}) XML error: {e}", file=sys.stderr)
        return articles

    # 支持 RSS 2.0 和 Atom
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # RSS 2.0
    items = root.findall(".//item")
    if not items:
        # Atom
        items = root.findall(".//atom:entry", ns) or root.findall(".//entry")

    for item in items:
        # 标题（注意：不能用 or，Element 无子元素时布尔值为 False）
        title_el = item.find("title")
        if title_el is None:
            title_el = item.find("atom:title", ns)
        title = get_text(title_el)

        # 链接
        link_el = item.find("link")
        if link_el is None:
            link_el = item.find("atom:link", ns)
        if link_el is not None:
            link = link_el.get("href") or get_text(link_el)
        else:
            link = ""
        link = link.strip()

        # 日期
        date_el = item.find("pubDate")
        if date_el is None:
            date_el = item.find("published")
        if date_el is None:
            date_el = item.find("atom:published", ns)
        if date_el is None:
            date_el = item.find("updated")
        if date_el is None:
            date_el = item.find("atom:updated", ns)
        date_str = get_text(date_el)
        pub_date = parse_date(date_str)

        # 描述/摘要
        desc_el = item.find("description")
        if desc_el is None:
            desc_el = item.find("summary")
        if desc_el is None:
            desc_el = item.find("atom:summary", ns)
        description = ""
        if desc_el is not None:
            raw = get_text(desc_el)
            # 去除 HTML 标签
            description = re.sub(r"<[^>]+>", "", raw).strip()[:300]

        if not title or not link:
            continue

        # 时间过滤
        if not is_recent(pub_date, MAX_AGE_DAYS_RSS):
            continue

        # 关键词过滤（高优先级信息源全部纳入）
        if source_name not in HIGH_PRIORITY_SOURCES:
            if not is_ai_related(title, description):
                continue

        articles.append({
            "title": title,
            "url": link,
            "source": source_name,
            "priority": priority,
            "published_at": pub_date.isoformat() if pub_date else "",
            "description": description
        })

    return articles


def fetch_arxiv():
    """采集 ArXiv 最新论文"""
    params = f"search_query={ARXIV_QUERY}&sortBy=submittedDate&sortOrder=descending&max_results={ARXIV_MAX}"
    url = f"{ARXIV_API}?{params}"

    print("[INFO] 采集 ArXiv 论文...", file=sys.stderr)
    # ArXiv 需要 User-Agent，否则 429；最多重试 2 次
    content = None
    for attempt in range(2):
        try:
            result = subprocess.run(
                ["curl", "-sL", "--max-time", "30",
                 "-H", "User-Agent: Mozilla/5.0 (compatible; research-bot/1.0; +https://arxiv.org/help/api)",
                 "-H", "Accept-Encoding: identity",
                 url],
                capture_output=True, timeout=35
            )
            if result.returncode == 0 and result.stdout:
                content = result.stdout.decode("utf-8", errors="replace")
                if content.strip().startswith("<"):
                    break
                content = None
        except subprocess.TimeoutExpired:
            pass
        if attempt == 0:
            time.sleep(3)
    if not content:
        print("[WARN] ArXiv 采集失败，跳过", file=sys.stderr)
        return []

    papers = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"[WARN] ArXiv XML parse error: {e}", file=sys.stderr)
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    for entry in entries:
        title_el = entry.find("atom:title", ns)
        title = get_text(title_el).replace("\n", " ")

        summary_el = entry.find("atom:summary", ns)
        abstract = get_text(summary_el).replace("\n", " ")[:400]

        # 链接（不能用 or，Element 无子元素时布尔值为 False）
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry.find("atom:link", ns)
        url = link_el.get("href", "") if link_el is not None else ""

        # 日期
        published_el = entry.find("atom:published", ns)
        date_str = get_text(published_el)
        pub_date = parse_date(date_str)

        # 作者
        authors = []
        for author_el in entry.findall("atom:author", ns):
            name_el = author_el.find("atom:name", ns)
            if name_el is not None:
                name = get_text(name_el)
                if name:
                    authors.append(name)

        if not title:
            continue

        # 时间过滤
        if not is_recent(pub_date, MAX_AGE_DAYS_ARXIV):
            continue

        # 关键词过滤（更严格）
        if not is_ai_related(title, abstract):
            continue

        papers.append({
            "title": title,
            "url": url,
            "authors": authors[:5],  # 最多 5 位作者
            "abstract": abstract,
            "source": "ArXiv",
            "published_at": pub_date.isoformat() if pub_date else ""
        })

    return papers


def main():
    all_articles = []
    failed_sources = []

    # 采集 RSS
    for source in RSS_SOURCES:
        name = source["name"]
        url = source["url"]
        priority = source["priority"]

        print(f"[INFO] 采集 {name}...", file=sys.stderr)
        content = fetch_url(url)
        if content:
            articles = parse_rss(content, name, priority)
            all_articles.extend(articles)
            print(f"[INFO]   → {len(articles)} 篇相关文章", file=sys.stderr)
        else:
            failed_sources.append(name)
            print(f"[WARN]   → 采集失败，跳过", file=sys.stderr)

        time.sleep(0.5)  # 避免请求过快

    # 采集 ArXiv
    papers = fetch_arxiv()
    print(f"[INFO] ArXiv → {len(papers)} 篇相关论文", file=sys.stderr)

    # 按日期降序排列
    all_articles.sort(
        key=lambda x: x.get("published_at", ""),
        reverse=True
    )

    result = {
        "source": "rss_and_arxiv",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "articles_count": len(all_articles),
        "papers_count": len(papers),
        "failed_sources": failed_sources,
        "articles": all_articles,
        "papers": papers
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[INFO] 完成：{len(all_articles)} 篇文章，{len(papers)} 篇论文", file=sys.stderr)
    if failed_sources:
        print(f"[WARN] 以下信息源采集失败：{', '.join(failed_sources)}", file=sys.stderr)


if __name__ == "__main__":
    main()
