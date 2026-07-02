"""抖音作品采集器 — 字段补完版（对齐江湖工具箱 ArtworkInfo.json）

基于三层策略混合 + 自适应频率控制的成熟方案。
完全独立实现，不依赖 old_douyin_collector/ 目录。

字段对齐江湖工具箱 ArtworkInfo.json，覆盖：
  作者名称/作者uid/作者secUid/作品类型/全屏/购物车/本地生活/图文图片/live图片

用法:
  from collectors.douyin.works_collector import (
      DouyinAdvancedCollector4,
      DouyinVideoAdvanced4,
      DouyinUserProfileV4,
  )

  collector = DouyinAdvancedCollector4(headless=False)
  collector.login()
  profile, videos = collector.fetch_user_works(
      sec_uid="MS4wLjABAAAAYY48wncTf9OP5QwMW7_nMrqkwx-1Blak4uTS-4FZCMc",
      douyin_id="1049401268",
      max_videos=20,
  )
"""

import json
import os
import random
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Optional
from urllib.parse import urlparse, parse_qs, urlencode

from collectors.page_adapter import PageAdapter
from collectors._utils import _parse_count
from collectors.playwright_session import PlaywrightSession
from collectors.douyin.models import (
    DouyinContentItem,
    DouyinUserProfile,
    ContentType,
)

SCRIPT_DIR = os.path.dirname(__file__)


# ──────────────────────────────────────────────────────────────
# 自适应频率控制器（从 _utils 统一导入，消除重复实现）
# ──────────────────────────────────────────────────────────────

from collectors._utils import RateLimiter
# API 请求/响应拦截器（从 old_douyin_collector/advanced_2.py 内联）
# ──────────────────────────────────────────────────────────────


class ApiUrlCapture:
    """拦截第一次 API 请求的完整 URL（含 a_bogus 签名）"""

    POST_API_PATTERN = "/aweme/v1/web/aweme/post/"

    def __init__(self):
        self.captured_url: Optional[str] = None
        self.captured_headers: dict[str, Any] = {}
        self.first_response_data: Optional[dict[str, Any]] = None
        self.all_responses: list[dict[str, Any]] = []
        self.all_awemes: list[dict[str, Any]] = []

    def on_request(self, request) -> None:
        """Playwright request 事件回调"""
        url = request.url
        if "/aweme/v1/web/" in url:
            import urllib.parse as up
            parsed = up.urlparse(url)
            path = parsed.path
            print(f"  [API请求] {path}", flush=True)
        if self.POST_API_PATTERN not in url:
            return
        if not self.captured_url:
            self.captured_url = url
            self.captured_headers = dict(request.headers)

    def on_response(self, response) -> None:
        """Playwright response 事件回调"""
        url = response.url
        if self.POST_API_PATTERN not in url:
            return
        if response.status != 200:
            return
        try:
            # 用 text() 代替 json()：text() 底层走 CDP Network.getResponseBody 但
            # 返回原始字符串，比 json() 更不容易遇到 "resource not found" 竞态
            body = response.text()
            data = json.loads(body)
            if not isinstance(data, dict):
                return
            self.all_responses.append(data)
            if not self.first_response_data:
                self.first_response_data = data
            aweme_list = data.get("aweme_list", [])
            if aweme_list:
                self.all_awemes.extend(aweme_list)
            print(f"  [API响应] status_code={data.get('status_code')}, "
                  f"aweme_list={len(aweme_list)} 条, "
                  f"has_more={data.get('has_more', 0)}, "
                  f"max_cursor={data.get('max_cursor', 0)}, "
                  f"has_aweme_list={'aweme_list' in data}",
                  flush=True)
        except Exception as e:
            print(f"  [API响应] 解析失败: {e}", flush=True)

    def get_base_url_and_params(self) -> tuple[str, dict[str, Any]]:
        """解析捕获的 URL，返回 base_url 和扁平化参数"""
        if not self.captured_url:
            return "", {}
        parsed = urlparse(self.captured_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = parse_qs(parsed.query)
        flat_params: dict[str, Any] = {k: v[0] for k, v in params.items()}
        return base_url, flat_params

    @property
    def has_more(self) -> bool:
        if not self.all_responses:
            return False
        return self.all_responses[-1].get("has_more", 0) == 1

    @property
    def max_cursor(self) -> int:
        if not self.all_responses:
            return 0
        return self.all_responses[-1].get("max_cursor", 0)

    def reset(self) -> None:
        self.all_responses.clear()
        self.all_awemes.clear()
        self.first_response_data = None


# ──────────────────────────────────────────────────────────────
# 增强数据结构 V4（继承统一基类 DouyinContentItem / DouyinUserProfile）
# ──────────────────────────────────────────────────────────────


class DouyinVideoAdvanced4(DouyinContentItem):
    """抖音视频条目（V4）— 继承统一基类，扩展抖音特有字段

    继承自 BaseContentItem 的共有字段:
      content_id(原video_id), title, url, play_count, like_count, comment_count,
      share_count, collect_count, duration, duration_seconds, resolution,
      topics, published_at(原create_time), cover_url, is_top,
      video_download_url, video_download_urls, image_urls, music_url, music_title,
      author_name, author_uid

    抖音特有字段（继承自 DouyinContentItem）:
      has_cart, cart_info, is_local_life, local_life_info, is_fullscreen, image_live_urls
    """

    # === 抖音 API 特有字段 ===
    video_id_raw: Optional[str] = None  # 原始视频ID
    author_sec_uid: str = ""  # 作者secUid
    video_type: str = "视频"  # 作品类型显示文本：视频/图文


class DouyinUserProfileV4(DouyinUserProfile):
    """抖音用户主页信息（V4）— 继承统一基类，扩展抖音特有字段

    继承自 BaseUserProfile 的共有字段:
      platform_uid(原sec_uid), nickname, avatar_url, bio, top_photo_url,
      fans_count, following_count, content_count(原video_count),
      like_count_total(原like_count), last_published_at
    """

    # === 抖音 API 特有字段 ===
    douyin_id: str = ""  # 抖音号


# ──────────────────────────────────────────────────────────────
# 采集器 V4（完全独立实现）
# ──────────────────────────────────────────────────────────────


class DouyinAdvancedCollector4:
    """抖音高级采集器 V4 — 字段补完版（完全独立实现）

    不依赖 old_douyin_collector/ 目录。
    基于 PlaywrightSession + API 拦截 + 三层策略混合采集。

    策略优先级:
      A: page.evaluate(fetch) + SDK 自动签名（最快，绕过安全 SDK）
      B: 精准滚动触发 + 网络层拦截（兼容性好）
      C: 键盘导航兜底（最后手段）
    """

    USER_URL = "https://www.douyin.com/user/{sec_uid}"
    POST_API = "https://www.douyin.com/aweme/v1/web/aweme/post/"

    # 登录等待超时（秒）
    LOGIN_WAIT_TIMEOUT = 600
    LOGIN_POLL_INTERVAL = 3.0

    def __init__(
        self,
        headless: bool = False,
        data_dir: str = "",
        scroll_wait: float = 4.0,
        proxy: Optional[dict[str, Any]] = None,
        channel: Optional[str] = None,
    ):
        self.headless = headless
        self.data_dir = data_dir or os.path.join(SCRIPT_DIR, ".browser-data", "douyin")
        self.scroll_wait = scroll_wait
        self.proxy = proxy
        self.channel = channel  # None=内置Chromium, "chrome"=系统Chrome

    # ── 登录态检测 ──────────────────────────────────────────

    def _check_login_status(self, page: PageAdapter) -> dict[str, Any]:
        """检测抖音登录态"""
        try:
            pw_page = page._driver

            try:
                login_btn = pw_page.query_selector('button:has-text("登录")')
                if login_btn:
                    return {"is_login": False, "uid": "", "username": ""}
            except Exception:
                pass

            try:
                avatar = pw_page.query_selector('[data-e2e="avatar"]')
                if avatar:
                    return {"is_login": True, "uid": "", "username": ""}
            except Exception:
                pass

            try:
                cookies = pw_page.context.cookies()
                for cookie in cookies:
                    if cookie.get("name") == "sessionid" and cookie.get("value"):
                        return {"is_login": True, "uid": "", "username": ""}
            except Exception:
                pass

            url = pw_page.url or ""
            if "login" in url.lower():
                return {"is_login": False, "uid": "", "username": ""}

            return {"is_login": True, "uid": "", "username": ""}
        except Exception as e:
            print(f"  [LOGIN] 检测异常: {e}，假设已登录", flush=True)
            return {"is_login": True, "uid": "", "username": ""}

    def _wait_for_login(self, page: PageAdapter) -> bool:
        """未登录时等待用户手动登录"""
        time.sleep(3)

        try:
            status = self._check_login_status(page)
            if status["is_login"]:
                print("  [LOGIN] 已登录抖音，自动继续", flush=True)
                return True
        except Exception as e:
            print(f"  [LOGIN] 初次检测异常（页面可能导航中）: {e}", flush=True)

        print("\n  [LOGIN] ============================================", flush=True)
        print("  [LOGIN]  采集器已打开内置 Chromium 浏览器窗口!", flush=True)
        print("  [LOGIN]  请在浏览器窗口中登录抖音。", flush=True)
        print("  [LOGIN]  登录后采集器将自动继续。", flush=True)
        print(f"  [LOGIN]  等待超时: {self.LOGIN_WAIT_TIMEOUT}s", flush=True)
        print("  [LOGIN]  登录态将持久化到下次运行。", flush=True)
        print("  [LOGIN] ============================================\n", flush=True)

        deadline = time.time() + self.LOGIN_WAIT_TIMEOUT
        while time.time() < deadline:
            time.sleep(self.LOGIN_POLL_INTERVAL)
            remaining = int(deadline - time.time())
            try:
                status = self._check_login_status(page)
                if status["is_login"]:
                    print(f"  [LOGIN] 登录成功!", flush=True)
                    return True
                if remaining % 30 == 0 and remaining > 0:
                    print(f"  [LOGIN] 未检测到登录态，剩余 {remaining}s...", flush=True)
            except Exception as e:
                print(f"  [LOGIN] 检测异常: {e}，剩余 {remaining}s...", flush=True)

        print("  [LOGIN] 登录超时，请下次先登录再运行采集器", flush=True)
        return False

    # ── 独立登录流程 ────────────────────────────────────────

    @property
    def cookie_file(self) -> str:
        return os.path.join(self.data_dir, "cookies.json")

    def login(self) -> bool:
        """独立登录流程：开浏览器 → 检测/等待登录 → 保存 cookie"""
        os.makedirs(self.data_dir, exist_ok=True)

        session = PlaywrightSession(
            headless=self.headless,
            data_dir=self.data_dir,
            proxy=self.proxy,
            channel=self.channel,
        )
        try:
            page = session.__enter__()
            page.goto(
                "https://www.douyin.com",
                wait_until="load",
                timeout=120000,
            )
            time.sleep(10)

            try:
                status = self._check_login_status(page)
            except Exception as e:
                print(f"  [LOGIN] 检测登录态异常: {e}", flush=True)
                status = {"is_login": False, "uid": "", "username": ""}

            if status["is_login"]:
                print(f"  [LOGIN] 已登录抖音", flush=True)
                self._export_cookies(session)
                return True

            print(f"  [LOGIN] 当前未登录，请在浏览器窗口中登录抖音", flush=True)
            if not self._wait_for_login(page):
                return False

            self._export_cookies(session)
            return True
        finally:
            session.__exit__(None, None, None)

    def _export_cookies(self, session: PlaywrightSession) -> None:
        """导出当前 context 的 cookie 到 JSON 文件（可选备份）"""
        try:
            session.save_cookies(self.cookie_file)
            cookie_count = 0
            if os.path.isfile(self.cookie_file):
                with open(self.cookie_file, "r", encoding="utf-8") as f:
                    cookie_count = len(json.load(f))
            print(f"  [COOKIE] 已导出 {cookie_count} 条 cookie → {self.cookie_file}", flush=True)
        except Exception as e:
            print(f"  [COOKIE] 导出失败（不影响采集）: {e}", flush=True)

    def is_logged_in(self) -> bool:
        """快速检测当前是否已有持久化的登录态（不开浏览器窗口）"""
        return os.path.isfile(self.cookie_file)

    # ── 搜索用户 ────────────────────────────────────────────

    def _search_user(self, page: PageAdapter, douyin_id: str) -> str:
        """通过抖音号搜索用户，返回 sec_uid"""
        search_url = f"https://www.douyin.com/search/{douyin_id}?type=user"
        page.goto(search_url, wait_until="load", timeout=120000)
        time.sleep(10)

        sec_uid = page.evaluate(
            f"""(function() {{
                var douyinId = {json.dumps(douyin_id)};
                var allLinks = document.querySelectorAll('a[href*="/user/"]');
                for (var i = 0; i < allLinks.length; i++) {{
                    var link = allLinks[i];
                    var href = link.getAttribute('href') || '';
                    if (href.indexOf('/user/self') >= 0) continue;
                    var linkText = link.innerText || '';
                    if (linkText.indexOf(douyinId) >= 0) {{
                        var match = href.match(/\\/user\\/([^/?#]+)/);
                        if (match && match[1].length > 20) return match[1];
                    }}
                }}
                for (var i = 0; i < allLinks.length; i++) {{
                    var link = allLinks[i];
                    var href = link.getAttribute('href') || '';
                    if (href.indexOf('/user/self') >= 0) continue;
                    var match = href.match(/\\/user\\/([^/?#]+)/);
                    if (match && match[1].length > 20) return match[1];
                }}
                return '';
            }})()"""
        )
        return sec_uid or ""

    # ── 用户信息采集 ────────────────────────────────────────

    def _fetch_profile(self, page: PageAdapter, sec_uid: str, douyin_id: str) -> DouyinUserProfileV4:
        """通过 DOM 提取用户主页信息（V4 字段补完版）"""
        data = page.evaluate(
            """(function() {
                var userInfo = document.querySelector('[data-e2e="user-info"]');
                var fullText = userInfo ? userInfo.innerText : '';
                var lines = fullText.split('\\n');

                var nickname = lines[0] ? lines[0].trim() : '';

                var followEl = document.querySelector('[data-e2e="user-info-follow"]');
                var following = followEl ?
                    followEl.innerText.trim().split('\\n').pop() : '';

                var fansEl = document.querySelector('[data-e2e="user-info-fans"]');
                var fans = fansEl ?
                    fansEl.innerText.trim().split('\\n').pop() : '';

                var likeEl = document.querySelector('[data-e2e="user-info-like"]');
                var likes = likeEl ?
                    likeEl.innerText.trim().split('\\n').pop() : '';

                var tabEl = document.querySelector('[data-e2e="user-tab-count"]');
                var videoCount = tabEl ? tabEl.innerText.trim() : '';

                var idMatch = fullText.match(/抖音号[：:]\\s*([A-Za-z0-9_]+)/);
                var douyinId = idMatch ? idMatch[1] : '';

                var bio = '';
                var lastEmptyIdx = -1;
                for (var i = lines.length - 1; i >= 0; i--) {
                    if (lines[i].trim() === '') {
                        lastEmptyIdx = i;
                        break;
                    }
                }
                if (lastEmptyIdx >= 0 && lastEmptyIdx < lines.length - 1) {
                    bio = lines.slice(lastEmptyIdx + 1).join('\\n').trim();
                }

                var avatarImg = document.querySelector(
                    '[data-e2e="user-avatar"] img, .avatar img, img[src*="avatar"]'
                );
                var avatarUrl = avatarImg
                    ? (avatarImg.src || avatarImg.getAttribute('data-src') || '')
                    : '';

                var topPhotoEl = document.querySelector(
                    '[data-e2e="user-info"] img, .user-info .top-photo img, img[src*="background"]'
                );
                var topPhotoUrl = topPhotoEl
                    ? (topPhotoEl.src || topPhotoEl.getAttribute('data-src') || '')
                    : '';

                return {
                    nickname: nickname, bio: bio, douyinId: douyinId,
                    following: following, fans: fans, likes: likes,
                    videoCount: videoCount,
                    avatarUrl: avatarUrl, topPhotoUrl: topPhotoUrl
                };
            })()"""
        )

        return DouyinUserProfileV4(
            platform_uid=sec_uid,
            platform_url=f"https://www.douyin.com/user/{sec_uid}",
            nickname=data.get("nickname", ""),
            douyin_id=data.get("douyinId", "") or douyin_id,
            fans_count=_parse_count(data.get("fans", "")),
            following_count=_parse_count(data.get("following", "")),
            like_count_total=_parse_count(data.get("likes", "")),
            content_count=_parse_count(data.get("videoCount", "")),
            bio=data.get("bio") or "",
            avatar_url=data.get("avatarUrl") or "",
            top_photo_url=data.get("topPhotoUrl") or "",
        )

    # ── 视频条目解析 ────────────────────────────────────────

    @staticmethod
    def _format_duration(duration_ms: int) -> str:
        """将毫秒时长格式化为 MM:SS 或 HH:MM:SS"""
        if not duration_ms:
            return ""
        total_sec = duration_ms // 1000
        hours = total_sec // 3600
        minutes = (total_sec % 3600) // 60
        seconds = total_sec % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def _parse_aweme(self, aweme: dict[str, Any]) -> Optional[DouyinVideoAdvanced4]:
        """将 API 返回的 aweme 条目解析为 V4 数据对象"""
        def first_url(value: Any) -> str:
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                url_list = value.get("url_list") or []
                if url_list:
                    return str(url_list[0])
                uri = value.get("uri")
                if isinstance(uri, str) and uri.startswith(("http://", "https://")):
                    return uri
            if isinstance(value, list) and value:
                return first_url(value[0])
            return ""

        try:
            aweme_id = aweme.get("aweme_id", "")
            if not aweme_id:
                return None

            desc = aweme.get("desc", "") or aweme.get("item_title", "") or ""

            stats = aweme.get("statistics", {})
            digg_count = stats.get("digg_count", 0)
            comment_count = stats.get("comment_count", 0)
            collect_count = stats.get("collect_count", 0)
            share_count = stats.get("share_count", 0)
            play_count = stats.get("play_count", 0)

            video_info = aweme.get("video", {})
            duration_ms = video_info.get("duration", 0)

            _debug = os.environ.get("COLLECTOR_DEBUG", "")
            if _debug:
                print(
                    f"  [DEBUG-PARSE] aweme={aweme_id} | "
                    f"play={play_count} | "
                    f"ratio={video_info.get('ratio', 'N/A')} | "
                    f"bit_rate_count={len(video_info.get('bit_rate') or [])} | "
                    f"author_uid={aweme.get('author', {}).get('uid', 'N/A')} | "
                    f"has_commerce={bool(aweme.get('commerce_info'))} | "
                    f"images_count={len(aweme.get('images') or [])}",
                    flush=True,
                )
            duration_sec = duration_ms // 1000 if duration_ms else 0
            duration_str = self._format_duration(duration_ms)

            cover_url = ""
            cover = video_info.get("cover", {})
            if cover and cover.get("url_list"):
                cover_url = cover["url_list"][0]

            ratio = video_info.get("ratio", "")
            resolution = ratio if ratio else None

            download_urls: dict[str, str] = {}
            bit_rate_list = video_info.get("bit_rate") or []
            for br in bit_rate_list:
                gear = br.get("gear_name", "")
                play_addr = br.get("play_addr", {})
                if play_addr and play_addr.get("url_list"):
                    download_urls[gear] = play_addr["url_list"][-1]

            # 主下载地址优先级：
            # 1. video.download_addr（带水印 CDN 直链，urllib 可直拉，最可靠）
            # 2. bit_rate 各档 play_addr（无水印跳转地址，需 cookie + 302 跟随）
            # 3. 顶层 video.play_addr（兜底）
            video_download_url = ""
            download_addr = video_info.get("download_addr") or {}
            if download_addr.get("url_list"):
                video_download_url = first_url(download_addr["url_list"])

            if not video_download_url and download_urls:
                for res in ["normal_1080_0", "normal_720_0", "normal_540_0"]:
                    if res in download_urls:
                        video_download_url = download_urls[res]
                        break
            if not video_download_url:
                play_addr = video_info.get("play_addr", {})
                if play_addr and play_addr.get("url_list"):
                    video_download_url = play_addr["url_list"][-1]

            video_id_raw = ""
            play_addr = video_info.get("play_addr", {})
            if play_addr:
                video_id_raw = play_addr.get("uri", "")

            music = aweme.get("music", {})
            music_url = ""
            play_url = music.get("play_url", {})
            if play_url:
                music_url = first_url(play_url)
            music_title = music.get("title", "")
            audio_download_url = first_url(music.get("audio_track") or music.get("download_url") or music.get("play_url")) or None

            create_time = aweme.get("create_time", 0)
            create_time_str = ""
            if create_time:
                tz = timezone(timedelta(hours=8))
                create_time_str = datetime.fromtimestamp(
                    create_time, tz
                ).strftime("%Y-%m-%d %H:%M:%S")

            is_top = aweme.get("is_top", 0) == 1

            topics: list[str] = []
            text_extra = aweme.get("text_extra") or []
            for extra in text_extra:
                hashtag = extra.get("hashtag_name", "")
                if hashtag:
                    topics.append(hashtag)

            # === 对齐江湖工具箱的补完字段 ===
            author_info = aweme.get("author", {})
            author_name = author_info.get("nickname", "")
            author_uid = author_info.get("uid", "")
            author_sec_uid = author_info.get("sec_uid", "")

            images = aweme.get("images") or []
            video_type = "图文" if images else "视频"

            is_fullscreen = bool(video_info.get("is_fullscreen", False))

            commerce_info = aweme.get("commerce_info", {}) or {}
            has_cart = True if commerce_info.get("has_cart", False) else False
            cart_info: Optional[str] = None
            if has_cart:
                cart_items = commerce_info.get("cart_items", []) or []
                if cart_items:
                    cart_info = "; ".join(
                        item.get("title", "")
                        for item in cart_items
                        if item.get("title")
                    )

            local_life = aweme.get("local_life_info", {}) or {}
            is_local_life = True if local_life.get("is_local_life", False) else False
            local_life_info: Optional[str] = None
            if is_local_life:
                poi_info = local_life.get("poi_info", {}) or {}
                if poi_info:
                    local_life_info = poi_info.get("name", "")

            image_urls: list[str] = []
            image_live_urls: list[str] = []
            if video_type == "图文":
                for img in images:
                    url_list = img.get("url_list") or []
                    if url_list:
                        image_urls.append(url_list[-1])
                    live_image = img.get("live_image", {}) or {}
                    live_url_list = live_image.get("url_list") or []
                    if live_url_list:
                        image_live_urls.append(live_url_list[-1])

            return DouyinVideoAdvanced4(
                content_id=aweme_id,
                title=desc,
                url=f"https://www.douyin.com/video/{aweme_id}",
                play_count=play_count,
                like_count=digg_count,
                duration=duration_str,
                cover_url=cover_url or None,
                comment_count=comment_count,
                collect_count=collect_count,
                share_count=share_count,
                published_at=create_time_str,
                is_top=is_top,
                video_download_url=video_download_url or None,
                video_download_urls=download_urls,
                music_url=music_url or None,
                music_title=music_title or None,
                audio_download_url=audio_download_url,
                resolution=resolution,
                duration_seconds=duration_sec,
                topics=topics,
                video_id_raw=video_id_raw or None,
                author_name=author_name,
                author_uid=author_uid,
                author_sec_uid=author_sec_uid,
                video_type=video_type,
                is_fullscreen=is_fullscreen,
                has_cart=has_cart,
                cart_info=cart_info,
                is_local_life=is_local_life,
                local_life_info=local_life_info,
                image_urls=image_urls,
                image_live_urls=image_live_urls,
            )

        except Exception as e:
            print(
                f"  [解析异常] aweme_id={aweme.get('aweme_id','')}, "
                f"aweme_type={aweme.get('aweme_type','?')}, "
                f"error={type(e).__name__}: {e}",
                flush=True,
            )
            return None

    # ── 视频列表解析辅助 ────────────────────────────────────

    def _parse_new_videos(
        self,
        capture: ApiUrlCapture,
        seen_ids: set[str],
        videos: list[DouyinVideoAdvanced4],
        max_videos: int,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """解析 capture 中尚未处理的新视频"""
        for aweme in capture.all_awemes:
            aweme_id = aweme.get("aweme_id", "")
            if not aweme_id or aweme_id in seen_ids:
                continue
            video = self._parse_aweme(aweme)
            if video:
                videos.append(video)
                seen_ids.add(aweme_id)
            if progress_callback:
                progress_callback(len(videos), max_videos)

    # ── 三层策略混合采集 ────────────────────────────────────

    def _collect_with_strategies(
        self,
        page: PageAdapter,
        pw_page,
        context,
        capture: ApiUrlCapture,
        rate_limiter: RateLimiter,
        sec_uid: str,
        target: int,
        progress_callback: Optional[Callable] = None,
    ) -> list[DouyinVideoAdvanced4]:
        """三层策略混合采集"""
        seen_ids: set[str] = set()
        videos: list[DouyinVideoAdvanced4] = []

        self._parse_new_videos(capture, seen_ids, videos, target, progress_callback)
        print(f"  [INIT] 初始加载: {len(videos)} 条视频", flush=True)

        if len(videos) >= target:
            return videos[:target]

        # 策略 A: page.evaluate(fetch) + SDK 自动签名
        print(f"\n  [策略A] 尝试 page.evaluate(fetch)...", flush=True)
        strategy_a_success = self._strategy_a_fetch(
            pw_page, capture, rate_limiter, sec_uid,
            seen_ids, videos, target, progress_callback,
        )

        if strategy_a_success:
            print(f"  [策略A] 成功! 共 {len(videos)} 条视频", flush=True)
            return videos[:target] if target > 0 else videos

        # 策略 B: 精准滚动触发
        print(f"\n  [策略B] 策略A失败，尝试精准滚动触发...", flush=True)
        strategy_b_success = self._strategy_b_scroll(
            page, pw_page, capture, rate_limiter,
            seen_ids, videos, target, progress_callback,
        )

        if strategy_b_success:
            print(f"  [策略B] 成功! 共 {len(videos)} 条视频", flush=True)
            return videos[:target] if target > 0 else videos

        # 策略 C: 键盘导航兜底
        print(f"\n  [策略C] 策略B失败，尝试键盘导航...", flush=True)
        self._strategy_c_keyboard(
            pw_page, capture, rate_limiter,
            seen_ids, videos, target, progress_callback,
        )

        print(f"  [最终] 共 {len(videos)} 条视频", flush=True)
        return videos[:target] if target > 0 else videos

    # ── 策略 A: SDK fetch ──────────────────────────────────

    def _strategy_a_fetch(
        self,
        pw_page,
        capture: ApiUrlCapture,
        rate_limiter: RateLimiter,
        sec_uid: str,
        seen_ids: set[str],
        videos: list[DouyinVideoAdvanced4],
        target: int,
        progress_callback: Optional[Callable],
    ) -> bool:
        """策略 A: 用 page.evaluate(fetch) 翻页"""
        if not capture.captured_url:
            print("  [策略A] 未捕获到 API URL，跳过", flush=True)
            return False

        base_url, params = capture.get_base_url_and_params()
        if not base_url:
            print("  [策略A] 无法解析 URL", flush=True)
            return False

        print(f"  [策略A] 捕获到 URL，参数:", flush=True)
        for k, v in sorted(params.items()):
            print(f"    {k}={v[:60]}...", flush=True)

        if not capture.first_response_data:
            print("  [策略A] 无首次响应数据", flush=True)
            return False

        current_cursor = capture.first_response_data.get("max_cursor", 0)
        has_more = capture.first_response_data.get("has_more", 0) == 1

        if not has_more:
            print("  [策略A] 首次响应 has_more=0，无需翻页", flush=True)
            return True

        sign_params = {"a_bogus", "msToken", "verifyFp", "fp",
                       "x-secsdk-web-signature", "_signature"}
        clean_params = {k: v for k, v in params.items() if k not in sign_params}
        print(f"  [策略A] 移除签名参数: {sign_params}", flush=True)
        print(f"  [策略A] 保留参数: {len(clean_params)} 个", flush=True)

        if "publish_video_strategy_type" in clean_params:
            old_val = clean_params["publish_video_strategy_type"]
            clean_params["publish_video_strategy_type"] = "1"
            print(f"  [策略A] publish_video_strategy_type: {old_val} → 1 (获取全部)",
                  flush=True)
            current_cursor = 0
            print(f"  [策略A] 重置 cursor=0，从头获取全部作品", flush=True)

        consecutive_failures = 0
        page_num = 0

        while has_more and len(videos) < target:
            current_url = pw_page.url
            if "verify" in current_url or "captcha" in current_url:
                print(f"  [策略A] 检测到验证码页面，立即停止: {current_url}", flush=True)
                return False

            delay = rate_limiter.wait(page_num) + 2.0
            print(f"  [策略A] 第{page_num+2}页: cursor={current_cursor}, "
                  f"等待{delay:.1f}s", flush=True)
            time.sleep(delay)

            next_params = clean_params.copy()
            next_params["max_cursor"] = str(current_cursor)
            next_url = f"{base_url}?{urlencode(next_params)}"

            try:
                body = pw_page.evaluate("""async (url) => {
                    try {
                        const resp = await fetch(url, {
                            credentials: 'include',
                            headers: {
                                'Accept': 'application/json, text/plain, */*',
                            },
                        });
                        const text = await resp.text();
                        return {status: resp.status, body: text, method: 'fetch'};
                    } catch (e) {
                        return {status: 0, body: e.toString(), method: 'error'};
                    }
                }""", next_url)

                status = body.get("status", 0) if isinstance(body, dict) else 0
                resp_text = body.get("body", "") if isinstance(body, dict) else ""
                method = body.get("method", "?") if isinstance(body, dict) else "?"

                if status != 200:
                    print(f"  [策略A] HTTP {status}, "
                          f"body[:200]={resp_text[:200]}", flush=True)
                    rate_limiter.on_failure()
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        print("  [策略A] 连续3次失败，切换策略", flush=True)
                        return False
                    continue

                data = json.loads(resp_text)
                aweme_list = data.get("aweme_list") or []
                has_more = data.get("has_more", 0) == 1
                current_cursor = data.get("max_cursor", 0)
                status_code = data.get("status_code", 0)

                print(f"  [策略A] 响应({method}): status_code={status_code}, "
                      f"aweme_list={len(aweme_list)} 条, "
                      f"has_more={has_more}, "
                      f"cursor={current_cursor}",
                      flush=True)

                if status_code != 0:
                    print(f"  [策略A] API status_code={status_code}, "
                          f"可能被风控", flush=True)
                    post_url = pw_page.url
                    if "verify" in post_url or "captcha" in post_url:
                        print(f"  [策略A] 检测到验证码页面，立即停止: {post_url}", flush=True)
                        return False
                    rate_limiter.on_failure()
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        return False
                    continue

                if aweme_list:
                    capture.all_responses.append(data)
                    capture.all_awemes.extend(aweme_list)
                    self._parse_new_videos(capture, seen_ids, videos,
                                           target, progress_callback)
                    rate_limiter.on_success()
                    consecutive_failures = 0
                    print(f"  [策略A] +{len(aweme_list)} 条, "
                          f"总计 {len(videos)}/{target}, "
                          f"has_more={has_more}", flush=True)
                else:
                    print(f"  [策略A] 空响应, status_code={status_code}", flush=True)
                    rate_limiter.on_failure()
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        return False

                page_num += 1
                if page_num > 50:
                    print("  [策略A] 达到50页上限", flush=True)
                    break

            except json.JSONDecodeError as e:
                print(f"  [策略A] JSON解析失败: {e}", flush=True)
                rate_limiter.on_failure()
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    return False
            except Exception as e:
                print(f"  [策略A] 请求异常: {type(e).__name__}: {e}", flush=True)
                rate_limiter.on_failure()
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    return False

        return len(videos) > 20

    # ── 策略 B: 精准滚动触发 ──────────────────────────────

    def _strategy_b_scroll(
        self,
        page: PageAdapter,
        pw_page,
        capture: ApiUrlCapture,
        rate_limiter: RateLimiter,
        seen_ids: set[str],
        videos: list[DouyinVideoAdvanced4],
        target: int,
        progress_callback: Optional[Callable],
    ) -> bool:
        """策略 B: 精准滚动触发 API 请求"""
        prev_count = len(videos)
        consecutive_no_new = 0
        scroll_attempts = 0
        max_scroll_attempts = 30

        while len(videos) < target and scroll_attempts < max_scroll_attempts:
            scroll_attempts += 1
            delay = rate_limiter.wait(scroll_attempts)
            before_count = len(videos)
            before_api_count = len(capture.all_responses)

            self._scroll_container(pw_page)
            time.sleep(5)

            self._parse_new_videos(capture, seen_ids, videos,
                                   target, progress_callback)

            new_count = len(videos) - before_count
            new_api_count = len(capture.all_responses) - before_api_count

            if new_count > 0:
                print(f"  [策略B] 滚动#{scroll_attempts}: +{new_count} 条, "
                      f"总计 {len(videos)}/{target}, "
                      f"API响应: +{new_api_count}", flush=True)
                rate_limiter.on_success()
                consecutive_no_new = 0
            else:
                consecutive_no_new += 1
                print(f"  [策略B] 滚动#{scroll_attempts}: 无新视频 "
                      f"(连续{consecutive_no_new}次) "
                      f"API响应: +{new_api_count}", flush=True)
                rate_limiter.on_failure()

                if consecutive_no_new >= 5:
                    print("  [策略B] 连续5次无新视频，切换策略", flush=True)
                    break

                if consecutive_no_new >= 3:
                    cooldown = rate_limiter.cooldown("滚动无新视频")
                    print(f"  [策略B] 冷却 {cooldown:.1f}s", flush=True)

            if not capture.has_more and capture.all_responses:
                print("  [策略B] has_more=0, 采集完成", flush=True)
                break

        return len(videos) > prev_count

    def _scroll_container(self, pw_page) -> None:
        """精准滚动 route-scroll-container 触发 IntersectionObserver"""
        debug_info = pw_page.evaluate("""() => {
            const container = document.querySelector(
                '[class*="route-scroll"]'
            );
            if (!container) return {found: false};

            const children = container.querySelectorAll('*');
            const videoCards = [];
            for (const child of children) {
                const cls = child.className.toString();
                if (cls.includes('video') || cls.includes('card') ||
                    cls.includes('item') || cls.includes('aweme')) {
                    videoCards.push({
                        tag: child.tagName,
                        className: cls.substring(0, 80),
                        rect: child.getBoundingClientRect(),
                    });
                }
            }

            return {
                found: true,
                className: container.className.toString().substring(0, 100),
                scrollHeight: container.scrollHeight,
                clientHeight: container.clientHeight,
                scrollTop: container.scrollTop,
                childCount: children.length,
                videoCardCount: videoCards.length,
                lastVideoCard: videoCards.length > 0 ?
                    videoCards[videoCards.length - 1] : null,
            };
        }""")
        if debug_info and debug_info.get("found"):
            print(f"  [DEBUG] route-scroll-container: "
                  f"scrollH={debug_info['scrollHeight']}, "
                  f"clientH={debug_info['clientHeight']}, "
                  f"scrollTop={debug_info['scrollTop']}, "
                  f"children={debug_info['childCount']}, "
                  f"videoCards={debug_info['videoCardCount']}",
                  flush=True)
        else:
            print(f"  [DEBUG] route-scroll-container 未找到!", flush=True)

        pw_page.evaluate("""() => {
            const container = document.querySelector('[class*="route-scroll"]');
            if (!container) return;
            const totalScroll = container.scrollHeight - container.clientHeight;
            const steps = 5;
            const stepSize = totalScroll / steps;
            for (let i = 1; i <= steps; i++) {
                container.scrollTop = stepSize * i;
                container.dispatchEvent(new Event('scroll', {bubbles: true}));
                requestAnimationFrame(() => {});
            }
        }""")

        pw_page.evaluate("""() => {
            const container = document.querySelector('[class*="route-scroll"]');
            if (!container) return;
            const children = container.children;
            if (children.length > 0) {
                const lastChild = children[children.length - 1];
                lastChild.scrollIntoView({behavior: 'smooth', block: 'end'});
            }
            const allCards = container.querySelectorAll(
                'a[href*="/video/"], [class*="video"], [class*="card"]'
            );
            if (allCards.length > 0) {
                allCards[allCards.length - 1].scrollIntoView({
                    behavior: 'smooth', block: 'end'
                });
            }
        }""")

        try:
            pw_page.mouse.move(640, 400)
            steps = random.randint(2, 4)
            for step in range(steps):
                pw_page.mouse.wheel(0, random.randint(300, 800))
                time.sleep(random.uniform(0.3, 1.0))
        except Exception:
            pass

        if random.random() < 0.3:
            try:
                pw_page.mouse.wheel(0, -random.randint(50, 200))
            except Exception:
                pass
            time.sleep(random.uniform(0.5, 1.5))

    # ── 策略 C: 键盘导航 ──────────────────────────────────

    def _strategy_c_keyboard(
        self,
        pw_page,
        capture: ApiUrlCapture,
        rate_limiter: RateLimiter,
        seen_ids: set[str],
        videos: list[DouyinVideoAdvanced4],
        target: int,
        progress_callback: Optional[Callable],
    ) -> None:
        """策略 C: 用键盘导航触发滚动"""
        prev_count = len(videos)
        consecutive_no_new = 0
        max_attempts = 20

        for attempt in range(max_attempts):
            delay = rate_limiter.wait(attempt)
            before_count = len(videos)

            keys = ["End", "PageDown", " ", "ArrowDown"]
            key = random.choice(keys)
            try:
                pw_page.keyboard.press(key)
            except Exception:
                pass
            time.sleep(3)

            self._parse_new_videos(capture, seen_ids, videos,
                                   target, progress_callback)

            new_count = len(videos) - before_count
            if new_count > 0:
                print(f"  [策略C] 按键{key}: +{new_count} 条, "
                      f"总计 {len(videos)}/{target}", flush=True)
                rate_limiter.on_success()
                consecutive_no_new = 0
            else:
                consecutive_no_new += 1
                if consecutive_no_new >= 5:
                    print("  [策略C] 连续5次无新视频，停止", flush=True)
                    break

            if not capture.has_more and capture.all_responses:
                break

        if len(videos) > prev_count:
            print(f"  [策略C] 获取了 {len(videos) - prev_count} 条新视频",
                  flush=True)

    # ── 主采集流程 ──────────────────────────────────────────

    def fetch_user_works(
        self,
        douyin_id: str = "",
        max_videos: int = 0,
        login_callback: Optional[Callable[[PageAdapter], None]] = None,
        sec_uid: str = "",
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> tuple[DouyinUserProfileV4, list[DouyinVideoAdvanced4]]:
        """采集用户主页信息 + 作品列表（V4 字段补完版）

        Args:
            douyin_id: 抖音号（如 "1049401268"）
            max_videos: 最多采集多少条作品，0 = 全部
            login_callback: 登录等待回调函数
            sec_uid: 抖音安全ID，若已知可直接传入跳过搜索
            progress_callback: 进度回调 (current, total)

        Returns:
            (用户主页信息, 作品列表)
        """
        with PlaywrightSession(
            headless=self.headless,
            data_dir=self.data_dir,
            proxy=self.proxy,
            channel=self.channel,
        ) as page:
            pw_page = page._driver
            context = pw_page.context

            # 关键：在导航之前就挂载 API 捕获器。
            # 抖音是 SPA，已登录时 goto() 不会真正重新加载页面，首屏视频列表 API
            # 请求在 goto 返回前几秒就发出了；若监听器在 goto 之后才挂，会完全错过，
            # 导致 capture.captured_url 为空、策略A 被迫跳过、初始加载空转 60 秒。
            capture = ApiUrlCapture()
            # 只在 page 级注册，不重复注册 context 级（否则每个事件触发两次回调，
            # 第二次 response.json() 因 body 已被消费而抛 CDP 竞态错误）
            pw_page.on("request", capture.on_request)
            pw_page.on("response", capture.on_response)

            # 直接导航到用户主页，如果未登录会自动跳转登录页
            # 这样比先加载抖音首页快很多
            if sec_uid:
                url = self.USER_URL.format(sec_uid=sec_uid)
                print(f"  [导航] 直接访问用户主页: {url[:60]}...", flush=True)
            else:
                # 没有sec_uid时才需要先搜索
                url = "https://www.douyin.com"
                print(f"  [导航] 访问抖音首页...", flush=True)

            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            time.sleep(10)

            if login_callback:
                login_callback(page)
            else:
                if not self._wait_for_login(page):
                    raise RuntimeError("登录超时，无法继续采集")

            # 如果之前没有sec_uid，现在需要搜索获取
            if not sec_uid:
                sec_uid = self._search_user(page, douyin_id)

            # 登录后等待页面稳定，然后检查是否需要重新导航
            time.sleep(10)
            try:
                current_url = pw_page.url or ""
            except Exception:
                current_url = ""
            if sec_uid and ("/user/" not in current_url or "login" in current_url):
                print(f"  [导航] 登录后重新访问用户主页...", flush=True)
                url = self.USER_URL.format(sec_uid=sec_uid)
                page.goto(url, wait_until="domcontentloaded", timeout=120000)
                time.sleep(10)
            elif sec_uid:
                # 已在用户主页且未发生跳转：此时监听器虽已挂载，但首屏 API 早已发完，
                # 强制 reload 触发全新的 API 请求，让上面的捕获器能抓到 captured_url。
                print(f"  [导航] 页面已在用户主页，reload 触发 API 以便捕获器抓取...",
                      flush=True)
                # 清空可能残留的早期响应，避免把 reload 前的脏数据算进去
                capture.all_responses.clear()
                capture.all_awemes.clear()
                try:
                    pw_page.reload(wait_until="domcontentloaded", timeout=120000)
                except Exception as e:
                    print(f"  [导航] reload 异常(忽略): {e}", flush=True)
                time.sleep(8)

            rate_limiter = RateLimiter(base_delay=self.scroll_wait, page_increment=0.5)
            from collectors._utils import _random_delay
            _random_delay(2.0, 4.0)

            for wait_round in range(8):  # 8×3s=24s（原 12×5s=60s）
                time.sleep(3)
                # 优先检查 body 已解析成功的响应
                if capture.all_responses:
                    print(f"  [加载] 第{wait_round+1}轮: "
                          f"捕获到 {len(capture.all_responses)} 个 API 响应, "
                          f"{len(capture.all_awemes)} 条视频",
                          flush=True)
                    break
                # body 解析可能失败，但只要拿到了 URL（含 a_bogus 签名），
                # 策略A 就能用 page.evaluate(fetch) 直接发请求，无需空转等 body
                if capture.captured_url:
                    print(f"  [加载] 第{wait_round+1}轮: "
                          f"已捕获 API URL（body 尚未就绪），直接进入策略采集",
                          flush=True)
                    break
                current_url = pw_page.url
                if "verify" in current_url or "captcha" in current_url:
                    print(f"  [加载] 检测到验证码页面: {current_url}",
                          flush=True)
                    print(f"  [加载] 请手动完成验证码后继续", flush=True)
                    time.sleep(30)
                    break
                print(f"  [加载] 第{wait_round+1}轮: 等待 API 响应... "
                      f"(当前URL: {current_url[:80]})",
                      flush=True)
            else:
                print(f"  [加载] 警告: 24秒内未捕获到 API 响应!", flush=True)

            profile = self._fetch_profile(page, sec_uid, douyin_id)

            target = max_videos if max_videos > 0 else profile.video_count
            videos = self._collect_with_strategies(
                page, pw_page, context, capture, rate_limiter,
                sec_uid, target, progress_callback,
            )

            try:
                pw_page.remove_listener("request", capture.on_request)
                pw_page.remove_listener("response", capture.on_response)
            except Exception:
                pass

            # V4 扩展：补完 last_published_at
            if videos:
                profile.last_published_at = videos[0].published_at

            return profile, videos


# ──────────────────────────────────────────────────────────────
# 兼容别名
# ──────────────────────────────────────────────────────────────

DouyinAdvancedCollectorFieldComplete = DouyinAdvancedCollector4
