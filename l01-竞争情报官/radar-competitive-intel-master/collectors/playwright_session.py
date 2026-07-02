"""Playwright 内置 Chromium 会话管理器

替代 RoxyBrowserSession — 不依赖任何外部指纹浏览器，
使用 Playwright 自带的 Chromium 二进制包 + Stealth 反检测插件。

安装:
    pip install playwright playwright-stealth
    playwright install chromium

用法:
    with PlaywrightSession() as page:
        page.goto("https://www.bilibili.com")
        data = page.evaluate("document.title")
"""

import logging
import os
import random
import sys
import time
from typing import Optional

logger = logging.getLogger(__name__)

from collectors.page_adapter import PageAdapter

DEFAULT_VIEWPORT = {"width": 1920, "height": 1080}


#region debug-point collector-playwright-exe-session
def _debug_report(event: str, **payload) -> None:
    try:
        import json
        import urllib.request
        endpoint = os.environ.get("TRAE_DEBUG_ENDPOINT", "").strip()
        if not endpoint:
            return
        body = json.dumps({"event": event, "payload": payload}, ensure_ascii=False, default=str).encode("utf-8")
        request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(request, timeout=1).close()
    except Exception:
        pass
#endregion


# ── PyInstaller 打包兼容 ────────────────────────────────────

def _is_pyinstaller_bundle() -> bool:
    """检测是否在 PyInstaller 打包环境中运行"""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def _playwright_default_executable_exists(playwright_instance) -> bool:
    """检测 Playwright 默认浏览器可执行文件是否存在。"""
    try:
        executable_path = playwright_instance.chromium.executable_path
    except Exception:
        return False
    return bool(executable_path) and os.path.isfile(executable_path)


def _detect_system_browser_exe() -> str:
    """在 PyInstaller 打包环境下，检测用户系统已安装的浏览器 exe 路径。

    优先级：
    1. MS Edge    — Windows 10/11 不可卸载的系统组件
    2. WebView2   — Edge 相同 Chromium 引擎，系统独立组件，Teams/Office 等大量依赖
    3. Chrome     — 主流浏览器

    返回浏览器 exe 的绝对路径；若均不可用则抛 RuntimeError。
    """
    if sys.platform == "win32":
        # 1. MS Edge
        for p in ["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                   "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"]:
            if os.path.isfile(p):
                print(f"  [INFO] 检测到系统 Edge: {p}")
                return p

        # 2. WebView2 运行时
        for base in ["C:\\Program Files (x86)\\Microsoft\\EdgeWebView\\Application",
                      "C:\\Program Files\\Microsoft\\EdgeWebView\\Application"]:
            if os.path.isdir(base):
                try:
                    versions = sorted(os.listdir(base), reverse=True)
                except Exception:
                    continue
                for v in versions:
                    exe = os.path.join(base, v, "msedgewebview2.exe")
                    if os.path.isfile(exe):
                        # WebView2 是独立系统组件，无法通过 channel 启动，
                        # 但可以找到同版本的 Edge 安装目录（通常在 sibling）
                        print(f"  [INFO] 检测到 WebView2 运行时，查找 Edge...")
                        break
                break

        # 3. Chrome
        for p in ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                   "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"]:
            if os.path.isfile(p):
                print(f"  [INFO] 检测到系统 Chrome: {p}")
                return p

    elif sys.platform == "darwin":
        # macOS: 通过 mdfind 或标准路径查找
        for p in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                   "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]:
            if os.path.isfile(p):
                print(f"  [INFO] 检测到系统浏览器: {p}")
                return p

    raise RuntimeError(
        "未检测到任何可用浏览器。请安装 Microsoft Edge 或 Google Chrome。"
    )


# ────────────────────────────────────────────────────────

# 常见的 Windows Chrome UA（2026年）
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)

# Chrome 启动参数 — 去除自动化痕迹
CHROMIUM_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-features=ChromeWhatsNewUI",
    "--disable-sync",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-component-update",
    "--disable-domain-reliability",
    "--disable-features=TranslateUI",
    "--disable-hang-monitor",
    "--disable-ipc-flooding-protection",
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-renderer-backgrounding",
    "--force-color-profile=srgb",
    "--hide-scrollbars",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-default-browser-check",
    "--no-first-run",
    "--no-pings",
    "--no-zygote",
    "--no-proxy-server",
    "--password-store=basic",
]




class PlaywrightNotInstalledError(RuntimeError):
    """Playwright 或 playwright-stealth 未安装"""


class PlaywrightSession:
    """Playwright 内置 Chromium 会话管理器

    替代 RoxyBrowserSession，不需要 RoxyBrowser 服务。
    自动管理 Playwright 实例和 Chromium 浏览器进程。

    用法:
        with PlaywrightSession(
            headless=False,
            data_dir="./browser-data/bilibili",
        ) as page:
            page.goto("https://www.bilibili.com")

    Args:
        headless: 是否无头模式（默认 False，有头更接近真实用户）
        data_dir: 用户数据目录，用于持久化登录态 cookie。
                  不同平台用不同目录可隔离登录状态。
        viewport: 视口尺寸
        user_agent: 自定义 UA，None 则使用默认 UA
        locale: 浏览器语言（默认 zh-CN）
        timezone: 时区（默认 Asia/Shanghai）
        stealth: 是否启用 playwright-stealth 反检测（默认 True）
        proxy: 代理配置，格式如 {"server": "http://127.0.0.1:8080"}
    """

    def __init__(
        self,
        headless: bool = False,
        data_dir: Optional[str] = None,
        viewport: Optional[dict] = None,
        user_agent: Optional[str] = None,
        locale: str = "zh-CN",
        timezone: str = "Asia/Shanghai",
        stealth: bool = True,
        proxy: Optional[dict] = None,
        channel: Optional[str] = None,
    ):
        self.headless = headless
        self.data_dir = data_dir
        self.viewport = viewport or DEFAULT_VIEWPORT
        self.user_agent = user_agent or DEFAULT_UA
        self.locale = locale
        self.timezone = timezone
        self.stealth = stealth
        self.proxy = proxy
        # channel: 用户显式指定（如 "chrome", "msedge"），Playwright 自动定位
        # None 则使用 Playwright 自带的 Chromium（开发环境）
        self.channel = channel
        self._system_browser_exe: Optional[str] = None

        self._playwright = None
        self._browser = None
        self._context = None
        self._pw_page = None
        self._page_adapter: Optional[PageAdapter] = None

    def __enter__(self) -> PageAdapter:
        """启动 Playwright + Chromium，返回 PageAdapter"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise PlaywrightNotInstalledError(
                "playwright 未安装。请运行: pip install playwright && playwright install chromium"
            )

        _debug_report(
            "session-enter-start",
            frozen=getattr(sys, "frozen", False),
            meipass=getattr(sys, "_MEIPASS", ""),
            data_dir=self.data_dir,
            headless=self.headless,
            channel=self.channel,
            stealth=self.stealth,
        )
        self._playwright = sync_playwright().start()
        _debug_report(
            "sync-playwright-started",
            executable_path=getattr(self._playwright.chromium, "executable_path", ""),
            executable_exists=_playwright_default_executable_exists(self._playwright),
        )

        # 上下文参数（viewport/UA/locale 等在 launch_persistent_context 和 new_context 通用）
        context_args = {
            "viewport": self.viewport,
            "user_agent": self.user_agent,
            "locale": self.locale,
            "timezone_id": self.timezone,
            "ignore_https_errors": True,
        }
        if self.proxy:
            context_args["proxy"] = self.proxy

        if self.data_dir:
            # 使用持久化上下文（保存登录态 cookie）
            # 注意：launch_persistent_context 会直接返回 BrowserContext，不需要再 new_context
            launch_args = {
                "headless": self.headless,
                "args": CHROMIUM_ARGS,
                **context_args,
            }
            # 默认内置 Chromium（稳定带 --no-proxy-server）
            self._context = self._launch_with_fallback(
                launcher=lambda ch: self._playwright.chromium.launch_persistent_context(
                    self.data_dir,
                    **ch,
                ),
                launch_args=launch_args,
                for_persistent=True,
            )
            self._browser = None  # 持久化上下文没有独立 Browser 对象
            self._pw_page = self._context.new_page()
        else:
            # 非持久化模式：launch + new_context
            launch_args = {
                "headless": self.headless,
                "args": CHROMIUM_ARGS,
            }
            self._browser = self._launch_with_fallback(
                launcher=lambda ch: self._playwright.chromium.launch(**ch),
                launch_args=launch_args,
                for_persistent=False,
            )
            self._context = self._browser.new_context(**context_args)
            self._pw_page = self._context.new_page()

        # 注入反检测隐身脚本（借鉴 AutoCLI stealth.rs）
        if self.stealth:
            try:
                _debug_report("stealth-apply-start", package="playwright_stealth")
                # playwright-stealth 2.x: Stealth().apply_stealth_sync(page)
                from playwright_stealth import Stealth
                Stealth().apply_stealth_sync(self._pw_page)
                _debug_report("stealth-apply-success", package="playwright_stealth", api="Stealth.apply_stealth_sync")
            except ImportError:
                try:
                    _debug_report("stealth-apply-importerror", package="playwright_stealth", api="Stealth.apply_stealth_sync")
                    # playwright-stealth 1.x: stealth_sync(page)
                    from playwright_stealth import stealth_sync
                    stealth_sync(self._pw_page)
                    _debug_report("stealth-apply-success", package="playwright_stealth", api="stealth_sync")
                except ImportError:
                    logger.warning(
                        "playwright-stealth 未安装，跳过增强反检测。"
                        "建议安装: pip install playwright-stealth"
                    )
            except Exception as exc:
                _debug_report("stealth-apply-error", package="playwright_stealth", error=repr(exc))
                raise

        # 额外: 注入完整的反检测隐身脚本（STEALTH_JS）
        from collectors._stealth import STEALTH_JS
        self._pw_page.add_init_script(STEALTH_JS)

        # WebGL 反检测（真实 GPU 信息，避免被检测为自动化）
        # WebGL 反检测（真实 GPU 信息，避免被检测为自动化）
        self._pw_page.add_init_script("""
            // WebGL 反检测
            const getParameterProxyHandler = {
                apply: function(target, thisArg, args) {
                    const param = args[0];
                    // UNMASKED_VENDOR_WEBGL
                    if (param === 37445) return 'Google Inc. (NVIDIA)';
                    // UNMASKED_RENDERER_WEBGL
                    if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)';
                    return target.apply(thisArg, args);
                }
            };
            try {
                const rawGetParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = new Proxy(rawGetParameter, getParameterProxyHandler);
            } catch(e) {}
        """)

        self._page_adapter = PageAdapter(self._pw_page)
        return self._page_adapter

    def __exit__(self, exc_type, exc_val, exc_tb):
        """安全清理 Playwright 资源"""
        # 先关闭页面，释放正在进行的请求/响应监听
        if self._pw_page:
            try:
                self._pw_page.close()
            except Exception:
                pass
        if self._context:
            try:
                self._context.close()
            except Exception:
                pass
        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass
        return False

    def _launch_with_fallback(self, launcher, launch_args: dict, for_persistent: bool = True):
        """启动浏览器。

        优先使用 Playwright 内置 Chromium；当 exe 打包后内置浏览器缺失时，回退到系统浏览器。
        """
        if self.channel:
            args_with_channel = {**launch_args, "channel": self.channel}
            try:
                _debug_report("browser-launch-attempt", mode="channel", channel=self.channel, persistent=for_persistent)
                result = launcher(args_with_channel)
                _debug_report("browser-launch-success", mode="channel", channel=self.channel, persistent=for_persistent)
                return result
            except Exception as e:
                print(f"  [WARN] 系统 {self.channel} 不可用 ({e})")
                _debug_report("browser-launch-error", mode="channel", channel=self.channel, persistent=for_persistent, error=repr(e))
                raise

        if _playwright_default_executable_exists(self._playwright):
            args_with_builtin = {
                **launch_args,
                "executable_path": self._playwright.chromium.executable_path,
            }
            _debug_report("browser-launch-attempt", mode="builtin", executable_path=args_with_builtin["executable_path"], persistent=for_persistent)
            result = launcher(args_with_builtin)
            _debug_report("browser-launch-success", mode="builtin", executable_path=args_with_builtin["executable_path"], persistent=for_persistent)
            return result

        if not self._system_browser_exe:
            self._system_browser_exe = _detect_system_browser_exe()

        args_with_exe = {**launch_args, "executable_path": self._system_browser_exe}
        _debug_report("browser-launch-attempt", mode="system", executable_path=self._system_browser_exe, persistent=for_persistent)
        result = launcher(args_with_exe)
        _debug_report("browser-launch-success", mode="system", executable_path=self._system_browser_exe, persistent=for_persistent)
        return result

    @property
    def browser(self):
        """获取底层 Playwright Browser 对象（高级操作）"""
        return self._browser

    @property
    def context(self):
        """获取底层 Playwright BrowserContext 对象（高级操作）"""
        return self._context

    @property
    def pw_page(self):
        """获取底层 Playwright Page 对象（高级操作）"""
        return self._pw_page

    def save_cookies(self, filepath: str) -> None:
        """将当前上下文的 cookies 保存到文件（用于持久化登录态）"""
        if self._context:
            cookies = self._context.cookies()
            import json
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)

    def load_cookies(self, filepath: str) -> bool:
        """从文件加载 cookies 到当前上下文"""
        if not os.path.isfile(filepath) or not self._context:
            return False
        import json
        with open(filepath, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        self._context.add_cookies(cookies)
        return len(cookies) > 0


# ── 便捷函数 ────────────────────────────────────────────────────

def random_delay(min_sec: float = 2.0, max_sec: float = 5.0) -> None:
    """随机延迟，模拟人类操作间隔"""
    time.sleep(random.uniform(min_sec, max_sec))
