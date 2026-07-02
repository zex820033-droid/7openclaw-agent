"""抖音采集器包 — 从 Super-AIGC 适配独立运行。

包含:
  - hotspot_collector.py: 热点热搜（无登录，纯HTTP）
  - works_collector.py:  用户作品深度采集（需Playwright+登录）
  - direct_crawler.py:   抖音热搜直连API（无登录，纯HTTP+JSON）
  - models.py:           数据模型
"""

from collectors.douyin.hotspot_collector import DouyinHotspotCollector
from collectors.douyin.works_collector import (
    DouyinAdvancedCollector4,
    DouyinVideoAdvanced4,
    DouyinUserProfileV4,
)
from collectors.douyin.models import (
    DouyinContentItem,
    DouyinUserProfile,
    DouyinHotItem,
    PlatformType,
)

__all__ = [
    "DouyinHotspotCollector",
    "DouyinAdvancedCollector4",
    "DouyinVideoAdvanced4",
    "DouyinUserProfileV4",
    "DouyinContentItem",
    "DouyinUserProfile",
    "DouyinHotItem",
    "PlatformType",
]
