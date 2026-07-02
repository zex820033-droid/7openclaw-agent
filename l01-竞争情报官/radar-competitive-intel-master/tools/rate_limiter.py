"""
自适应请求频率控制器 — 从 Super-AIGC collectors/_utils.py 提取
生产级限速：基础延迟 + 翻页递增 + 随机抖动 + 指数退避 + 冷却
"""
import random
import time


class RateLimiter:
    """自适应请求频率控制器（douyin/kuaishou 共用，避免重复实现）

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
    """带指数退避重试的 HTTP GET（统一替代 toutiao 三份重复实现）

    在循环外创建单个 httpx.Client 复用连接池，避免每次重试都重新 TLS 握手。
    退避公式: backoff_base * attempt（3s, 6s），上限 10s。

    Args:
        url: 请求 URL
        headers: 请求头
        timeout: 单次请求超时秒数
        max_retries: 最大尝试次数（含首次）
        backoff_base: 退避基数，attempt=n 时等待 backoff_base*n 秒

    Returns:
        httpx.Response

    Raises:
        最后一次尝试的异常
    """
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


# ── 策略降级工具（借鉴 AutoCLI cascade.rs）─────────────────


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

def http_get_with_retry(
    url: str,
    *,
    headers: dict | None = None,
    timeout: int = 15,
    max_retries: int = 3,
    backoff_base: float = 3.0,
) -> "httpx.Response":
    """带指数退避重试的 HTTP GET（统一替代 toutiao 三份重复实现）

    在循环外创建单个 httpx.Client 复用连接池，避免每次重试都重新 TLS 握手。
    退避公式: backoff_base * attempt（3s, 6s），上限 10s。

    Args:
        url: 请求 URL
        headers: 请求头
        timeout: 单次请求超时秒数
        max_retries: 最大尝试次数（含首次）
        backoff_base: 退避基数，attempt=n 时等待 backoff_base*n 秒

    Returns:
        httpx.Response

    Raises:
        最后一次尝试的异常
    """
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
