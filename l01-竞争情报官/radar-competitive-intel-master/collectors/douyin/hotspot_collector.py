"""抖音热点采集器 — 双降级（60s API + 直连）

数据来源（按优先级）:
  1. 60s 聚合 API: https://60s.viki.moe/v2/douyin（主数据源）
  2. Python 直连爬虫: 抖音 hot/search/list API（兜底）

特点:
  - 纯 HTTP 请求，不需要 Playwright / 浏览器
  - 主数据源无需登录、无需 Cookie、无需 API Key
  - 免费使用，适合定时任务

从 Super-AIGC douyin_hotspot_collector.py 适配，移除 tianapi/hot_aggregator 依赖。
"""

from typing import Optional

import requests

from collectors.douyin.models import DouyinHotItem, PlatformType


class DouyinHotspotCollector:
    """抖音热点采集器 — 双降级

    使用两层数据源确保可用性:
      - 60s 聚合 API（主）
      - Python 直连爬虫（兜底）

    无需浏览器、无需登录、无需任何认证。
    """

    API_URL = "https://60s.viki.moe/v2/douyin"

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
        })

    def fetch_hot_list(self) -> list[DouyinHotItem]:
        """获取抖音热搜榜单（双降级）

        策略:
          1. 60s.viki.moe 公共聚合 API（主数据源）
          2. Python 直连爬虫（兜底）

        Returns:
            热点条目列表，按热度排序（rank 从1开始）
        """
        errors: list[str] = []
        for source, fetcher in [
            ("60s", self._fetch_from_60s),
            ("direct", self._fetch_from_direct),
        ]:
            try:
                return fetcher()
            except Exception as e:
                errors.append(f"[{source}] {type(e).__name__}: {e}")
                continue

        raise RuntimeError(
            "抖音热搜所有数据源均失败。各源错误:\n" + "\n".join(errors)
        )

    def _fetch_from_60s(self) -> list[DouyinHotItem]:
        """通过 60s 聚合 API 获取"""
        try:
            resp = self._session.get(self.API_URL, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"抖音60s API请求失败: {e}") from e

        if data.get("code") != 200:
            raise RuntimeError(
                f"抖音60s API返回错误: code={data.get('code')} "
                f"message={data.get('message')}"
            )

        items = []
        for idx, item in enumerate(data.get("data", []), start=1):
            items.append(DouyinHotItem(
                platform=PlatformType.DOUYIN,
                rank=idx,
                title=item.get("title", ""),
                hot_value=item.get("hot_value", 0),
                cover_url=item.get("cover", ""),
                url=item.get("link", ""),
                event_time=item.get("event_time", ""),
                event_time_at=item.get("event_time_at", 0),
                active_time=item.get("active_time", ""),
                active_time_at=item.get("active_time_at", 0),
            ))
        return items

    def _fetch_from_direct(self) -> list[DouyinHotItem]:
        """通过 Python 直连爬虫获取"""
        from collectors.douyin.direct_crawler import fetch_list

        raw_items = fetch_list()
        items = []
        for raw in raw_items:
            event_time = raw.get("event_time", "")
            items.append(DouyinHotItem(
                platform=PlatformType.DOUYIN,
                rank=raw["rank"],
                title=raw["title"],
                hot_value=raw.get("hot", 0),
                cover_url="",
                url=raw.get("url", ""),
                event_time=event_time,
                event_time_at=0,
                active_time="",
                active_time_at=0,
            ))
        return items
