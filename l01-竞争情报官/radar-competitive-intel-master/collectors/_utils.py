"""采集器共享工具函数。

从 Super-AIGC collectors/_utils.py 适配，移除 app 层依赖。
"""

import logging
import random
import time

from collectors.page_adapter import PageAdapter


def _parse_count(text: str) -> int:
    """将 '2399.2万' / '1.0万' / '531' 等中文计数转为整数"""
    text = str(text).strip().replace(",", "")
    if "万" in text:
        return int(float(text.replace("万", "")) * 10000)
    if "亿" in text:
        return int(float(text.replace("亿", "")) * 100000000)
    try:
        return int(text)
    except ValueError:
        return 0


def _random_delay(min_sec: float = 2.0, max_sec: float = 5.0) -> None:
    """随机延迟，模拟人类操作间隔，降低反爬触发概率"""
    time.sleep(random.uniform(min_sec, max_sec))


def check_kuaishou_login(page: PageAdapter) -> bool:
    """检测快手页面是否已登录"""
    logged_in = page.evaluate(
        """(function() {
            var bodyText = document.body.innerText || '';
            if (bodyText.indexOf('快去登录') >= 0 ||
                bodyText.indexOf('登录即可') >= 0 ||
                bodyText.indexOf('登录后查看') >= 0) {
                return false;
            }
            if (window.location.href.indexOf('passport') >= 0 ||
                window.location.href.indexOf('/login') >= 0) {
                return false;
            }
            var allEls = document.querySelectorAll('span, div, a, button');
            for (var i = 0; i < allEls.length; i++) {
                var text = (allEls[i].innerText || '').trim();
                if (text === '上传作品') return true;
            }
            var avatar = document.querySelector('img[alt*="头像"], img[class*="avatar"]');
            if (avatar) return true;
            var upload = document.querySelector('a[href*="upload"], [class*="upload"]');
            if (upload) return true;
            if (window.location.pathname.indexOf('/profile/') >= 0) {
                var h1 = document.querySelector('h1');
                if (h1 && h1.innerText.trim().length > 0) return true;
            }
            return true;
        })()"""
    )
    return bool(logged_in)


class RateLimiter:
    """自适应请求频率控制器（douyin/kuaishou 共用）

    策略:
      - 基础延迟: 3~6 秒
      - 翻页递增: 每翻 10 页增加 1 秒
      - 随机抖动: ±50% 范围随机化
      - 冷却退避: API 空响应时 30~60 秒冷却
      - 指数退避: 连续失败时 2^n * 5 秒等待
    """

    def __init__(self, base_delay: float = 4.0, page_increment: float = 0.5):
        self.base_delay = base_delay
        self.page_increment = page_increment
        self._consecutive_failures = 0
        self._total_requests = 0

    def wait(self, page_num: int = 0) -> float:
        """计算并执行自适应等待"""
        self._total_requests += 1
        extra = (page_num // 10) * self.page_increment
        base = self.base_delay + extra
        jitter = random.uniform(-0.5 * base, 0.5 * base)
        delay = max(2.0, base + jitter)
        if self._consecutive_failures > 0:
            backoff = (2 ** min(self._consecutive_failures, 5)) * 5.0
            delay += backoff
        time.sleep(delay)
        return delay

    def cooldown(self, reason: str = "") -> float:
        """触发冷却等待"""
        cooldown_sec = random.uniform(30.0, 60.0)
        if self._consecutive_failures > 0:
            cooldown_sec *= (1 + self._consecutive_failures * 0.5)
        time.sleep(cooldown_sec)
        return cooldown_sec

    def on_success(self) -> None:
        self._consecutive_failures = 0

    def on_failure(self) -> None:
        self._consecutive_failures += 1

    @property
    def failure_count(self) -> int:
        return self._consecutive_failures

    @property
    def total_requests(self) -> int:
        return self._total_requests


def http_get_with_retry(
    url: str,
    *,
    headers: dict | None = None,
    timeout: int = 15,
    max_retries: int = 3,
    backoff_base: float = 3.0,
) -> "httpx.Response":
    """带指数退避重试的 HTTP GET"""
    import httpx

    common = {
        "headers": headers or {},
        "timeout": timeout,
        "follow_redirects": True,
    }
    last_error: Exception | None = None
    with httpx.Client(**common) as client:
        for attempt in range(1, max_retries + 1):
            try:
                resp = client.get(url)
                resp.raise_for_status()
                return resp
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    wait = min(backoff_base * attempt, 10.0)
                    time.sleep(wait)
    assert last_error is not None
    raise last_error


# ── 策略降级工具 ─────────────────────────────────────


def skip_unavailable_strategy(
    target_strategy: str,
    available_strategies: set[str] | None = None,
    *,
    browser_available: bool = False,
    proxy_available: bool = True,
) -> bool:
    """判断某个数据源策略是否应在降级时跳过。

    降级链: PUBLIC -> COOKIE -> HEADER -> INTERCEPT -> UI
    """
    from collectors.douyin.models import DataStrategy

    try:
        strategy = DataStrategy(target_strategy)
    except ValueError:
        return True

    if available_strategies is not None:
        return target_strategy not in available_strategies

    if strategy == DataStrategy.PUBLIC:
        return not proxy_available
    return not browser_available


def log_strategy_fallback(source_name: str, strategy: str, reason: str) -> None:
    """记录策略降级日志"""
    logger = logging.getLogger("benchmark.strategy")
    logger.info("[strategy] %s 跳过 %s: %s", source_name, strategy, reason)
