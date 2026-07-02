#!/usr/bin/env python3
"""
GitHub Trending 采集脚本
采集今日和本周 AI/Coding 相关 Trending 项目
输出 JSON 到 stdout
"""

import json
import sys
import time
import re
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

# AI Coding 相关关键词（命中任一即纳入）
AI_KEYWORDS = {
    "agent", "agents", "agentic", "coding", "llm", "ai", "copilot",
    "claude", "gpt", "gemini", "cursor", "code generation", "code assistant",
    "mcp", "tool use", "memory", "rag", "context", "prompt", "inference",
    "transformer", "anthropic", "openai", "deepmind", "huggingface",
    "langchain", "llamaindex", "mistral", "llama", "deepseek", "qwen",
    "codeium", "tabnine", "devin", "opencode", "spec-driven",
    "recursive self-improvement", "multi-agent", "function calling",
    "embedding", "vector", "fine-tuning", "synthetic data"
}

# 排除关键词（命中则跳过）
EXCLUDE_KEYWORDS = {
    "minecraft", "game engine", "crypto", "blockchain", "nft", "web3",
    "trading bot", "forex", "stock trading"
}


class TrendingParser(HTMLParser):
    """解析 GitHub Trending 页面"""

    def __init__(self):
        super().__init__()
        self.repos = []
        self._current = {}
        self._in_repo_name = False
        self._in_description = False
        self._in_stars = False
        self._depth = 0
        self._article_depth = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._depth += 1

        if tag == "article" and "Box-row" in attrs_dict.get("class", ""):
            self._current = {"name": "", "description": "", "stars_today": 0, "stars_week": 0, "url": "", "language": ""}
            self._article_depth = self._depth

        if self._current is not None:
            cls = attrs_dict.get("class", "")
            href = attrs_dict.get("href", "")

            # 项目名链接
            if tag == "a" and href and re.match(r"^/[^/]+/[^/]+$", href) and "lh-condensed" in cls:
                self._current["url"] = "https://github.com" + href
                self._current["name"] = href.lstrip("/")
                self._in_repo_name = True

            # 描述
            if tag == "p" and "col-9" in cls:
                self._in_description = True

            # Stars 数量（今日/本周）
            if tag == "span" and "d-inline-block" in cls and "float-sm-right" in cls:
                self._in_stars = True

    def handle_endtag(self, tag):
        if tag == "article" and self._article_depth == self._depth:
            if self._current.get("name"):
                self.repos.append(dict(self._current))
            self._current = {}
            self._article_depth = None
        self._depth -= 1
        if tag in ("a", "p", "span"):
            self._in_repo_name = False
            self._in_description = False
            self._in_stars = False

    def handle_data(self, data):
        data = data.strip()
        if not data or not self._current:
            return
        if self._in_description and not self._current.get("description"):
            self._current["description"] = data
        if self._in_stars and "star" in data.lower():
            # 提取数字
            nums = re.findall(r"[\d,]+", data)
            if nums:
                val = int(nums[0].replace(",", ""))
                if not self._current.get("stars_today"):
                    self._current["stars_today"] = val
                else:
                    self._current["stars_week"] = val


def fetch_trending(since="daily"):
    """采集 GitHub Trending 页面"""
    url = f"https://github.com/trending?since={since}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        parser = TrendingParser()
        parser.feed(html)
        return parser.repos
    except (URLError, HTTPError) as e:
        print(f"[WARN] fetch_trending({since}) failed: {e}", file=sys.stderr)
        return []


def is_ai_related(repo):
    """判断项目是否与 AI Coding 相关"""
    text = (repo.get("name", "") + " " + repo.get("description", "")).lower()

    # 排除
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return False

    # 命中
    for kw in AI_KEYWORDS:
        if kw in text:
            return True

    return False


def merge_trending(daily_repos, weekly_repos):
    """合并今日和本周数据，去重，补充本周 Star 数"""
    merged = {}
    for repo in daily_repos:
        name = repo["name"]
        merged[name] = dict(repo)

    for repo in weekly_repos:
        name = repo["name"]
        if name in merged:
            # 补充本周数据
            if repo.get("stars_today"):
                merged[name]["stars_week"] = repo["stars_today"]
        else:
            # 只在本周榜出现的项目，stars_today=0
            merged[name] = dict(repo)
            merged[name]["stars_week"] = repo.get("stars_today", 0)
            merged[name]["stars_today"] = 0

    return list(merged.values())


def main():
    print("[INFO] 采集 GitHub Trending (daily)...", file=sys.stderr)
    daily = fetch_trending("daily")
    time.sleep(2)  # 避免请求过快

    print("[INFO] 采集 GitHub Trending (weekly)...", file=sys.stderr)
    weekly = fetch_trending("weekly")

    all_repos = merge_trending(daily, weekly)

    # 过滤 AI 相关
    ai_repos = [r for r in all_repos if is_ai_related(r)]

    # 按今日 Star 降序排列
    ai_repos.sort(key=lambda x: x.get("stars_today", 0), reverse=True)

    result = {
        "source": "github_trending",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_trending": len(all_repos),
        "ai_related_count": len(ai_repos),
        "repos": ai_repos
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[INFO] 完成：共 {len(all_repos)} 个 Trending 项目，过滤后 {len(ai_repos)} 个 AI 相关", file=sys.stderr)


if __name__ == "__main__":
    main()
