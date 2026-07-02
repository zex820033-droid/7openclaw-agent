"""
国内大厂新闻聚合抓取器 v3.1
============================
最终策略：uapis.cn 统一 API 串行调用，间隔 1.5 秒避免触发限流

为什么用 uapis.cn 而不是直接抓：
- 百度/知乎/B站/抖音官方页都加了 Cloudflare 验证或反爬（返回 403）
- uapis.cn 是个公益热榜聚合服务，无 API Key、无频率限制正常
- 串行调用可以避免 2000/h IP 限流（9 个信源 × 1.5 秒 = 14 秒，1 小时 3600 秒能跑 250 次完整）
"""

import argparse
import json
import sys
import os
import re
import time
import hashlib
import warnings
from datetime import datetime
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# ============== 配置 ==============

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json,text/html,*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
REQUEST_TIMEOUT = 15

# 公共热榜 API（uapis.cn，v3.0 测试确认：单信源 OK，并发 12 个会 429）
HOTBOARD_API = "https://uapis.cn/api/v1/misc/hotboard"

# 简单磁盘缓存
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.cache')
CACHE_TTL = 600  # 10 分钟
os.makedirs(CACHE_DIR, exist_ok=True)

# 平台中文名
PLATFORM_CN = {
    "weibo": "微博热搜", "zhihu": "知乎热榜", "bilibili": "B站热门",
    "baidu": "百度热搜", "douyin": "抖音热点", "toutiao": "头条热榜",
    "huxiu": "虎嗅", "36kr": "36氪", "ithome": "IT之家",
    "juejin": "掘金热榜", "thepaper": "澎湃新闻", "sspai": "少数派",
    "csdn": "CSDN", "netease-news": "网易新闻",
    "qq-news": "腾讯新闻", "sina-news": "新浪新闻", "kuaishou": "快手",
    "tieba": "百度贴吧", "v2ex": "V2EX", "hupu": "虎扑",
    "douban-movie": "豆瓣电影",
}


# ============== 工具函数 ==============

def safe_log(source, msg):
    sys.stderr.write(f"[{source}] {msg}\n")
    sys.stderr.flush()


def _cache_key(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def _get_cached(url):
    path = os.path.join(CACHE_DIR, _cache_key(url) + '.json')
    if os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < CACHE_TTL:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def _set_cache(url, data):
    path = os.path.join(CACHE_DIR, _cache_key(url) + '.json')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def _hotboard_request(platform, no_cache=False):
    """调用热榜 API"""
    url = f"{HOTBOARD_API}?type={platform}"
    if not no_cache:
        cached = _get_cached(url)
        if cached:
            return cached.get('data', [])

    try:
        r = requests.get(HOTBOARD_API, params={"type": platform}, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            safe_log(platform, f"HTTP {r.status_code}")
            _set_cache(url, {'data': []})
            return []
        data = r.json()
        if data.get("code"):
            safe_log(platform, f"API {data.get('code')}: {data.get('message')}")
            _set_cache(url, {'data': []})
            return []
        items = data.get("list", [])
        _set_cache(url, {'data': items})
        return items
    except Exception as e:
        safe_log(platform, f"API 异常: {e}")
        return []


def _build_hotboard_fetcher(platform_key, display_name=None):
    """工厂：把 uapis.cn 的平台 key 包成 fetcher"""
    name = display_name or PLATFORM_CN.get(platform_key, platform_key)
    def fetcher(limit=10, keyword=None, no_cache=False):
        raw = _hotboard_request(platform_key, no_cache=no_cache)
        items = []
        for entry in raw[:limit]:
            title = (entry.get('title') or '').strip()
            url = (entry.get('url') or '').strip()
            heat = entry.get('hot_value', '')
            if not title or not url:
                continue
            items.append({
                "source": name,
                "title": title,
                "url": url,
                "heat": str(heat) if heat else "",
                "time": "Real-time",
            })
        return filter_items(items, keyword)
    return fetcher


def filter_items(items, keyword=None):
    if not keyword or not items:
        return items
    keywords = [k.strip() for k in keyword.split(',') if k.strip()]
    pattern = '|'.join([re.escape(k) for k in keywords])
    regex = r'(?i)(' + pattern + r')'
    return [it for it in items if re.search(regex, (it.get('title', '') or '') + ' ' + (it.get('summary', '') or ''))]


# ============== 热榜信源 ==============

# 核心 9 个热榜（uapis.cn 串行调用，每个间隔 1.5 秒）
HOT_RANK_SOURCES = {
    'weibo': _build_hotboard_fetcher('weibo', '微博热搜'),
    'zhihu_hot': _build_hotboard_fetcher('zhihu', '知乎热榜'),
    'bilibili_hot': _build_hotboard_fetcher('bilibili', 'B站热门'),
    'baidu_hot': _build_hotboard_fetcher('baidu', '百度热搜'),
    'douyin_hot': _build_hotboard_fetcher('douyin', '抖音热点'),
    'toutiao_hot': _build_hotboard_fetcher('toutiao', '头条热榜'),
    'huxiu': _build_hotboard_fetcher('huxiu', '虎嗅'),
    '36kr': _build_hotboard_fetcher('36kr', '36氪'),
    'ithome': _build_hotboard_fetcher('ithome', 'IT之家'),
    'juejin': _build_hotboard_fetcher('juejin', '掘金热榜'),
    'thepaper': _build_hotboard_fetcher('thepaper', '澎湃新闻'),
    'sspai': _build_hotboard_fetcher('sspai', '少数派'),
    'csdn': _build_hotboard_fetcher('csdn', 'CSDN'),
}

# tmtpost 已被 uapis.cn 移除（HTTP 400），改用 sspai/csdn/ithome 替代


# ============== 大厂技术博客（混合：官方 RSS + 掘金/腾讯云标签页） ==============

def fetch_rss_feed(url, source_name, limit=5, referer=None, no_cache=False):
    """通用 RSS 抓取 + 缓存 + 重试"""
    if not no_cache:
        cached = _get_cached(url)
        if cached:
            return cached.get('data', [])

    for attempt in range(2):
        try:
            headers = dict(HEADERS)
            headers['Accept'] = 'application/rss+xml,application/xml,text/xml,*/*'
            if referer:
                headers["Referer"] = referer
            r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                from rss_parser import parse_rss_content
                items = parse_rss_content(r.content, source_name, limit)
                _set_cache(url, {'data': items})
                return items
            else:
                safe_log(source_name, f"RSS HTTP {r.status_code} (attempt {attempt+1})")
                time.sleep(1)
        except Exception as e:
            safe_log(source_name, f"RSS 抓取失败: {e}")
            time.sleep(0.5)
    return []


def _build_rss_fetcher(url, name, referer=None):
    def fetcher(limit=5, keyword=None, no_cache=False):
        items = fetch_rss_feed(url, name, limit, referer=referer, no_cache=no_cache)
        return filter_items(items, keyword)[:limit]
    return fetcher


def fetch_juejin_tag(tag, source_name, limit=5, no_cache=False):
    """掘金标签页（替代网易/小米/华为等没公开 RSS 的大厂）"""
    url = f"https://juejin.cn/tag/{quote(tag)}"
    if not no_cache:
        cached = _get_cached(url)
        if cached:
            return cached.get('data', [])

    items = []
    try:
        r = requests.get(url, headers={**HEADERS, "Referer": "https://juejin.cn/"}, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'html.parser')
            for item in soup.select('.entry-list .item, .article-item, .entry'):
                try:
                    title_tag = item.select_one('a.title, .title a, h4 a, a')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    if not title or len(title) < 4:
                        continue
                    href = title_tag.get('href', '')
                    # 提取作者
                    author_tag = item.select_one('.user-name, .author, .meta-user')
                    author = author_tag.get_text(strip=True) if author_tag else ""
                    items.append({
                        "source": source_name,
                        "title": title,
                        "url": f"https://juejin.cn{href}" if href.startswith('/') else href,
                        "heat": f"✍ {author}" if author else "",
                        "time": "Today",
                    })
                except Exception:
                    continue
    except Exception as e:
        safe_log(source_name, str(e))

    _set_cache(url, {'data': items})
    return filter_items(items, '')[:limit]


# 11 个大厂技术博客：3 个有官方 RSS + 8 个用掘金标签页
# 3 个有官方 RSS 的大厂（2026 年实测可用）+ 9 个通过 uapis.cn 抓的
# 大厂技术博客 = 程序员社区（CSDN）+ 媒体号（量子位、机器之心）+ RSS 大厂
TECH_BLOG_SOURCES = {
    # 官方 RSS（2026 年实测可用）
    'meituan': _build_rss_fetcher("https://tech.meituan.com/feed/", "美团技术", referer="https://tech.meituan.com/"),
    'qbitai': _build_rss_fetcher("https://www.qbitai.com/feed", "量子位", referer="https://www.qbitai.com/"),
    'jiqizhixin': _build_rss_fetcher("https://www.jiqizhixin.com/rss", "机器之心", referer="https://www.jiqizhixin.com/"),

    # uapis.cn 上的程序员/科技社区（覆盖"大厂动态"）
    'csdn': _build_hotboard_fetcher('csdn', 'CSDN热文'),
    'juejin': _build_hotboard_fetcher('juejin', '掘金热榜'),
    'sspai': _build_hotboard_fetcher('sspai', '少数派'),
    'ithome': _build_hotboard_fetcher('ithome', 'IT之家'),
    '36kr': _build_hotboard_fetcher('36kr', '36氪'),
    'thepaper': _build_hotboard_fetcher('thepaper', '澎湃新闻'),
}


def fetch_hot_rank(limit=10, keyword=None, no_cache=False):
    """热榜聚合：12 个国内一线热榜（串行调用，间隔 1.5 秒避免限流）"""
    all_items = []
    for name, func in HOT_RANK_SOURCES.items():
        try:
            items = func(limit, keyword, no_cache=no_cache)
            all_items.extend(items)
        except Exception as e:
            safe_log(name, f"聚合失败: {e}")
        time.sleep(1.5)  # 礼貌限流
    return all_items


def fetch_tech_blogs(limit=10, keyword=None, no_cache=False):
    """大厂技术博客聚合：11 个国内一线大厂"""
    all_items = []
    for name, func in TECH_BLOG_SOURCES.items():
        try:
            items = func(limit, keyword, no_cache=no_cache)
            all_items.extend(items)
        except Exception as e:
            safe_log(name, f"聚合失败: {e}")
        time.sleep(1.0)
    return all_items


# ============== Deep 抓取 ==============

def fetch_url_content(url, max_len=2000):
    if not url or not url.startswith('http'):
        return ""
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(r.content, 'html.parser')
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.extract()
        text = soup.get_text(separator=' ', strip=True)
        return text[:max_len]
    except Exception:
        return ""


def enrich_items_with_content(items, max_workers=5):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(fetch_url_content, item['url']): item for item in items}
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                content = future.result()
                if content:
                    item['content'] = content
            except Exception:
                item['content'] = ""
    return items


# ============== 保存 ==============

def save_report(data, source_name, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    safe_name = "".join([c if c.isalnum() else "_" for c in source_name]).lower()
    timestamp = datetime.now().strftime("%H%M")
    json_path = os.path.join(out_dir, f"{safe_name}_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return json_path


# ============== CLI ==============

ALL_SOURCES = {}
ALL_SOURCES.update(HOT_RANK_SOURCES)
ALL_SOURCES.update(TECH_BLOG_SOURCES)
ALL_SOURCES['hot_rank'] = fetch_hot_rank
ALL_SOURCES['tech_blogs'] = fetch_tech_blogs


def main():
    parser = argparse.ArgumentParser(
        description="国内大厂新闻聚合 v3.1 — uapis.cn 统一 API + 串行 + 缓存"
    )
    parser.add_argument('--source', default='all', help='信源 key（逗号分隔）')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--keyword', help='关键词过滤')
    parser.add_argument('--deep', action='store_true', help='抓详情页正文')
    parser.add_argument('--save', action='store_true', help='保存到 reports/')
    parser.add_argument('--no-save', action='store_true', dest='no_save', help='不保存到磁盘')
    parser.add_argument('--outdir', help='自定义输出目录')
    parser.add_argument('--list-sources', action='store_true', help='列出所有信源')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')

    args = parser.parse_args()

    if args.list_sources:
        print(f"{'Source Key':<22} | 名称 / 来源")
        print("-" * 60)
        for group_name, sources in [
            ("🥇 国民级热榜（uapis.cn 统一 API）", HOT_RANK_SOURCES),
            ("🥈 一线大厂技术博客", TECH_BLOG_SOURCES),
            ("📊 聚合层", {"hot_rank": "热榜聚合", "tech_blogs": "大厂博客聚合"}),
        ]:
            print(f"\n{group_name}")
            for key in sorted(sources.keys()):
                print(f"  {key:<20}")
        return

    to_run = []
    if args.source == 'all':
        to_run = list(ALL_SOURCES.values())
    else:
        requested = [s.strip() for s in args.source.split(',')]
        for s in requested:
            if s in ALL_SOURCES:
                to_run.append(ALL_SOURCES[s])
            else:
                safe_log("main", f"未知信源: {s}（已忽略）")

    results = []

    def run_fetchers(fetchers, limit, kw):
        out = []
        for func in fetchers:
            try:
                if callable(func):
                    out.extend(func(limit, kw, no_cache=args.no_cache))
            except Exception as e:
                safe_log(getattr(func, '__name__', 'agg'), f"异常: {e}")
        return out

    results = run_fetchers(to_run, args.limit, args.keyword)

    MIN_ITEMS = 5
    if args.keyword and len(results) < MIN_ITEMS:
        sys.stderr.write(f"Smart Fill: {len(results)} < {MIN_ITEMS}，补充抓取...\n")
        fill_results = run_fetchers(to_run, limit=MIN_ITEMS, kw=None)
        existing_urls = {item.get('url') for item in results}
        existing_titles = {item.get('title') for item in results}
        for item in fill_results:
            if len(results) >= MIN_ITEMS:
                break
            if item.get('url') not in existing_urls and item.get('title') not in existing_titles:
                item['smart_fill'] = True
                if 'time' in item:
                    item['time'] = f"⚠️ {item['time']}"
                results.append(item)
                existing_urls.add(item.get('url'))
                existing_titles.add(item.get('title'))

    if args.deep and results:
        sys.stderr.write(f"Deep 抓取 {len(results)} 条详情...\n")
        results = enrich_items_with_content(results)

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(json.dumps(results, indent=2, ensure_ascii=False))

    if not args.no_save and (args.save or args.source != 'all'):
        if args.outdir:
            out_dir = args.outdir
        else:
            today = datetime.now().strftime('%Y-%m-%d')
            out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', today)
        json_file = save_report(results, args.source, out_dir)
        sys.stderr.write(f"\n[Saved] {json_file}\n")


if __name__ == "__main__":
    main()
