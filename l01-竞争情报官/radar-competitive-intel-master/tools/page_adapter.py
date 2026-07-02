"""页面操作适配器 — 统一 Playwright/Selenium 接口

提供一致的页面操作接口，屏蔽底层浏览器驱动差异。
"""

import time
from typing import Union

from playwright.sync_api import Page as PlaywrightPage

try:
    from selenium.webdriver.remote.webdriver import WebDriver
except ImportError:
    WebDriver = None


class PageAdapter:
    """统一页面操作接口

    底层可能是 Playwright Page（Chromium）或 Selenium WebDriver（Firefox），
    对外提供一致的 .goto() / .evaluate() / .wait_for_selector() 等方法。
    """

    def __init__(self, driver: Union[PlaywrightPage, "WebDriver"]):
        self._driver = driver
        # 根据类型判断底层驱动
        from playwright.sync_api import Page as _PW
        self._is_playwright = isinstance(driver, _PW)
        # 网络响应拦截: {url_pattern: on_response_handler}
        self._capture_handlers: dict[str, object] = {}

    @property
    def is_playwright(self) -> bool:
        return self._is_playwright

    def goto(self, url: str, wait_until: str = "domcontentloaded",
             timeout: int = 20000) -> None:
        if self._is_playwright:
            self._driver.goto(url, wait_until=wait_until, timeout=timeout)
        else:
            # Selenium
            self._driver.set_page_load_timeout(timeout)
            self._driver.get(url)
            time.sleep(2)

    def evaluate(self, script: str):
        """执行 JS 并返回结果

        注意: Selenium 的 execute_script 不支持箭头函数 () => {...}，
        会返回空 dict。需要将箭头函数转为普通 function IIFE。
        """
        if self._is_playwright:
            return self._driver.evaluate(script)
        else:
            expr = script.strip()
            if expr.startswith("() =>"):
                # 将 () => ... 转为 (function() { return ... })()
                body = expr[5:].strip()
                if body.startswith("{") and body.endswith("}"):
                    # 多行块: () => { ... } → (function() { ... })()
                    inner = body[1:-1].strip()
                    expr = f"(function() {{ {inner} }})()"
                else:
                    # 单表达式: () => expr → (function() { return expr })()
                    expr = f"(function() {{ return {body} }})()"
            result = self._driver.execute_script("return " + expr)
            return result

    def execute_script(self, script: str) -> None:
        """执行 JS，不关心返回值"""
        if self._is_playwright:
            self._driver.evaluate(script)
        else:
            self._driver.execute_script(script)

    def wait_for_selector(self, selector: str, timeout: int = 10000) -> bool:
        if self._is_playwright:
            try:
                self._driver.wait_for_selector(selector, timeout=timeout)
                return True
            except Exception:
                return False
        else:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            try:
                WebDriverWait(self._driver, timeout / 1000).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                return True
            except Exception:
                return False

    # ── 网络响应拦截 ──

    def capture_responses(self, url_pattern: str) -> list[dict]:
        """拦截匹配 URL 模式的网络响应

        注册 response 事件监听器，在页面导航和滚动期间自动收集匹配的
        JSON 响应。返回的列表会被持续填充，调用方在操作完成后读取。

        仅 Playwright 模式可用；Selenium 模式返回空列表（调用方应回退到 DOM）。

        Args:
            url_pattern: URL 子串匹配，如 "/graphql" 或 "/rest/v/profile/get"

        Returns:
            可变的 captured 列表，元素为响应 JSON dict
        """
        if not self._is_playwright:
            return []
        captured: list[dict] = []
        self._capture_handlers[url_pattern] = []

        def on_response(response):
            try:
                if url_pattern in response.url:
                    captured.append(response.json())
            except Exception:
                pass

        self._driver.on("response", on_response)
        self._capture_handlers[url_pattern] = on_response
        return captured

    def stop_capture(self, url_pattern: str) -> None:
        """停止拦截指定 URL 模式的响应（移除事件监听）

        Args:
            url_pattern: capture_responses 时传入的相同 URL 模式
        """
        if not self._is_playwright:
            return
        handler = self._capture_handlers.pop(url_pattern, None)
        if handler:
            try:
                self._driver.remove_listener("response", handler)
            except Exception:
                pass

    def get_cookies(self) -> list[dict]:
        """获取浏览器当前所有 cookies"""
        if self._is_playwright:
            return self._driver.context.cookies()
        else:
            return self._driver.get_cookies()

    def api_request(self, url: str, headers: dict = None, timeout: int = 10000) -> dict:
        """通过 Playwright 原生 HTTP 请求 API（绕过页面 JS 安全拦截）

        仅在 Playwright 模式下可用。请求会携带浏览器的 cookie。
        timeout 默认 10s（Playwright 默认 30s 太长，首次 DNS+TLS 偶尔超时，
        快速失败后由调用方重试更高效）。
        """
        if self._is_playwright:
            resp = self._driver.context.request.fetch(
                url, headers=headers or {}, timeout=timeout,
            )
            try:
                return resp.json()
            except Exception:
                return {
                    "code": -999,
                    "message": "Non-JSON response",
                    "body": resp.text()[:500],
                    "status": resp.status,
                }
        else:
            raise NotImplementedError("api_request 仅在 Playwright 模式下可用")
