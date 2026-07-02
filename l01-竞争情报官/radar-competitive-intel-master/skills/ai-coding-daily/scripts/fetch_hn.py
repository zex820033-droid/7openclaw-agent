#!/usr/bin/env python3
"""
Hacker News 采集脚本
采集 Top Stories 中 AI Coding 相关的高分帖子
使用官方 Firebase API，无需爬虫
输出 JSON 到 stdout
"""

import json
import sys
import time
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
from urllib.error import URLError
from concurrent.futures import ThreadPoolExecutor, as_completed

# HN 官方 API
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
HN_TOP_URL = f"{HN_API_BASE}/topstories.json"
HN_ITEM_URL = f"{HN_API_BASE}/item/{{id}}.json"

# 过滤阈值
MIN_SCORE = 100
MAX_STORIES = 200  # 只检查前 200 条（Top Stories 按分数排序）
MAX_AGE_DAYS = 3   # 只保留最近 3 天的帖子

# AI 相关关键词（标题命中任一即纳入）
AI_KEYWORDS = {
    "ai", "llm", "gpt", "claude", "gemini", "copilot", "cursor",
    "agent", "coding assistant", "code generation", "anthropic", "openai",
    "google deepmind", "huggingface", "mcp", "tool use", "agentic",
    "rag", "context window", "inference", "transformer", "llama",
    "mistral", "deepseek", "qwen", "devin", "codeium", "tabnine",
    "langchain", "llamaindex", "recursive self-improvement",
    "multi-agent", "function calling", "fine-tuning", "synthetic data",
    "large language model", "language model", "neural network",
    "machine learning", "deep learning", "diffusion model",
    "stable diffusion", "midjourney", "dall-e", "sora",
    "opencode", "spec-driven development", "ai coding"
}

# 核心信息源域名（这些域名的帖子即使标题不含关键词也纳入）
CORE_DOMAINS = {
    "anthropic.com", "openai.com", "deepmind.google", "github.blog",
    "huggingface.co", "cursor.com", "mistral.ai", "langchain.com",
    "blog.langchain.dev", "arxiv.org"
}


def fetch_json(url, timeout=10):
    """获取 JSON 数据"""
    try:
        with urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError) as e:
        print(f"[WARN] fetch_json({url}) failed: {e}", file=sys.stderr)
        return None


def fetch_item(item_id):
    """获取单个帖子详情"""
    url = HN_ITEM_URL.format(id=item_id)
    return fetch_json(url)


def is_ai_related(item):
    """判断帖子是否与 AI 相关"""
    title = (item.get("title") or "").lower()
    url = (item.get("url") or "").lower()

    # 检查域名
    for domain in CORE_DOMAINS:
        if domain in url:
            return True

    # 检查标题关键词
    for kw in AI_KEYWORDS:
        if kw in title:
            return True

    return False


def is_recent(item, max_age_days=MAX_AGE_DAYS):
    """判断帖子是否在时间范围内"""
    ts = item.get("time", 0)
    if not ts:
        return False
    post_time = datetime.fromtimestamp(ts, tz=timezone.utc)
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    return post_time >= cutoff


def format_item(item):
    """格式化帖子数据"""
    ts = item.get("time", 0)
    post_time = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None
    return {
        "id": item.get("id"),
        "title": item.get("title", ""),
        "url": item.get("url", f"https://news.ycombinator.com/item?id={item.get('id')}"),
        "hn_url": f"https://news.ycombinator.com/item?id={item.get('id')}",
        "score": item.get("score", 0),
        "comments": item.get("descendants", 0),
        "by": item.get("by", ""),
        "time": post_time.isoformat() if post_time else "",
        "time_ago": _time_ago(ts) if ts else ""
    }


def _time_ago(ts):
    """计算相对时间"""
    delta = datetime.now(timezone.utc) - datetime.fromtimestamp(ts, tz=timezone.utc)
    hours = int(delta.total_seconds() / 3600)
    if hours < 1:
        return "刚刚"
    elif hours < 24:
        return f"{hours}小时前"
    else:
        days = hours // 24
        return f"{days}天前"


def main():
    print("[INFO] 获取 HN Top Stories ID 列表...", file=sys.stderr)
    top_ids = fetch_json(HN_TOP_URL)
    if not top_ids:
        print(json.dumps({"source": "hacker_news", "error": "无法获取 Top Stories", "items": []}))
        return

    # 只检查前 MAX_STORIES 条
    check_ids = top_ids[:MAX_STORIES]
    print(f"[INFO] 检查前 {len(check_ids)} 条帖子...", file=sys.stderr)

    # 并发获取帖子详情
    items = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_item, id_): id_ for id_ in check_ids}
        for i, future in enumerate(as_completed(futures)):
            item = future.result()
            if item and item.get("type") == "story":
                items.append(item)
            if (i + 1) % 50 == 0:
                print(f"[INFO] 已获取 {i+1}/{len(check_ids)} 条...", file=sys.stderr)
            time.sleep(0.05)  # 轻微限速

    # 过滤：分数 + 时间 + AI 相关
    filtered = []
    for item in items:
        if item.get("score", 0) >= MIN_SCORE and is_recent(item) and is_ai_related(item):
            filtered.append(format_item(item))

    # 按分数降序
    filtered.sort(key=lambda x: x["score"], reverse=True)

    result = {
        "source": "hacker_news",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "checked_count": len(check_ids),
        "ai_related_count": len(filtered),
        "items": filtered
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[INFO] 完成：检查 {len(check_ids)} 条，过滤后 {len(filtered)} 条 AI 相关高分帖子", file=sys.stderr)


if __name__ == "__main__":
    main()
