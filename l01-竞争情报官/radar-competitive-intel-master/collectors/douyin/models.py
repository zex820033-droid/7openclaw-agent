"""抖音采集数据模型 — 从 super_aigc_collectors 提取，独立可用。

提供:
  - 枚举: PlatformType, ContentType, DataStrategy
  - 抖音模型: DouyinUserProfile, DouyinContentItem, DouyinHotItem
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PlatformType(str, Enum):
    DOUYIN = "douyin"
    BILIBILI = "bilibili"
    KUAISHOU = "kuaishou"
    ZHIHU = "zhihu"
    TOUTIAO = "toutiao"
    CSDN = "csdn"
    XIAOHONGSHU = "xiaohongshu"


class ContentType(str, Enum):
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"


class DataStrategy(str, Enum):
    PUBLIC = "public"
    COOKIE = "cookie"
    HEADER = "header"
    INTERCEPT = "intercept"
    UI = "ui"


# ── 基类 ──────────────────────────────────────────


@dataclass
class BaseUserProfile:
    platform_uid: str = ""
    platform_url: str = ""
    nickname: str = ""
    avatar_url: str = ""
    bio: str = ""
    top_photo_url: str = ""
    fans_count: int = 0
    following_count: int = 0
    content_count: int = 0
    like_count_total: int = 0
    last_published_at: str = ""


@dataclass
class BaseContentItem:
    content_id: str = ""
    title: str = ""
    url: str = ""
    play_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    collect_count: int = 0
    duration: str = ""
    duration_seconds: int = 0
    resolution: Optional[str] = None
    topics: list = field(default_factory=list)
    published_at: str = ""
    cover_url: Optional[str] = None
    is_top: bool = False
    video_download_url: Optional[str] = None
    video_download_urls: dict = field(default_factory=dict)
    image_urls: list = field(default_factory=list)
    music_url: Optional[str] = None
    music_title: Optional[str] = None
    author_name: str = ""
    author_uid: str = ""


@dataclass
class BaseHotItem:
    platform: PlatformType = PlatformType.DOUYIN
    rank: int = 0
    title: str = ""
    hot_value: int = 0
    cover_url: str = ""
    url: str = ""
    event_time: str = ""
    event_time_at: int = 0
    active_time: str = ""
    active_time_at: int = 0


# ── 抖音模型 ───────────────────────────────────────


@dataclass
class DouyinUserProfile(BaseUserProfile):
    """抖音用户主页信息"""
    douyin_id: str = ""


@dataclass
class DouyinContentItem(BaseContentItem):
    """抖音内容条目（视频/图文）"""
    video_id_raw: Optional[str] = None
    author_sec_uid: str = ""
    video_type: str = "视频"
    audio_download_url: Optional[str] = None
    is_fullscreen: bool = False
    has_cart: bool = False
    cart_info: Optional[str] = None
    is_local_life: bool = False
    local_life_info: Optional[str] = None
    image_live_urls: list = field(default_factory=list)


@dataclass
class DouyinHotItem(BaseHotItem):
    """抖音热点条目"""
    pass
