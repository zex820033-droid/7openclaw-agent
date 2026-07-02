"""浏览器 Cookie 自动提取工具。

移植自 Agent-Reach cookie_extract.py，适配本项目平台。
优先使用 rookiepy（Rust 实现，更稳定），回退 browser_cookie3。

支持平台:
  - 小红书 (.xiaohongshu.com) — 全量 Cookie 字符串
  - B站 (.bilibili.com) — SESSDATA + bili_jct
  - 知乎 (.zhihu.com) — z_c0 + _xsrf
  - 抖音 (.douyin.com) — 全量 Cookie 字符串

用法:
  from app.services.benchmark.collectors._cookie_extract import (
      extract_all, get_cookie_string, get_cookie_dict
  )
  cookies = extract_all("chrome")
  xhs_cookie = get_cookie_string("xhs", "chrome")
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# ── 平台规格 ──────────────────────────────────────────

PLATFORM_SPECS: list[dict[str, Any]] = [
    {
        "name": "XiaoHongShu",
        "domains": [".xiaohongshu.com"],
        "cookies": None,  # None = 抓取全部 Cookie 拼成字符串
        "config_key": "xhs",
    },
    {
        "name": "Bilibili",
        "domains": [".bilibili.com"],
        "cookies": ["SESSDATA", "bili_jct"],
        "config_key": "bilibili",
    },
    {
        "name": "Zhihu",
        "domains": [".zhihu.com"],
        "cookies": ["z_c0", "_xsrf"],
        "config_key": "zhihu",
    },
    {
        "name": "Douyin",
        "domains": [".douyin.com"],
        "cookies": None,
        "config_key": "douyin",
    },
]


# ── Cookie 提取核心 ────────────────────────────────────


def _load_browser_cookies(browser: str = "chrome"):
    """加载浏览器 Cookie，rookiepy 优先，browser_cookie3 兜底。

    Args:
        browser: chrome / firefox / edge / brave / opera

    Returns:
        list of cookie objects（带 .name / .value / .domain 属性）

    Raises:
        RuntimeError: 两个库都不可用
    """
    try:
        import rookiepy

        browser_map = {
            "chrome": rookiepy.chrome,
            "firefox": rookiepy.firefox,
            "edge": rookiepy.edge,
            "brave": rookiepy.brave,
            "opera": rookiepy.opera,
        }
        loader = browser_map.get(browser)
        if loader is None:
            raise ValueError(f"不支持的浏览器: {browser}")
        return loader()
    except ImportError:
        logger.debug("rookiepy 不可用，回退 browser_cookie3")
    except Exception as e:
        logger.warning(f"rookiepy 加载失败: {e}，回退 browser_cookie3")

    try:
        import browser_cookie3

        bc_map = {
            "chrome": browser_cookie3.chrome,
            "firefox": browser_cookie3.firefox,
            "edge": browser_cookie3.edge,
            "brave": browser_cookie3.brave,
            "opera": browser_cookie3.opera,
        }
        loader = bc_map.get(browser)
        if loader is None:
            raise ValueError(f"不支持的浏览器: {browser}")
        return list(loader())
    except ImportError:
        raise RuntimeError(
            "Cookie 提取需要安装 rookiepy 或 browser_cookie3:\n"
            "  pip install rookiepy   # 推荐，Rust 实现\n"
            "  pip install browser_cookie3  # 备选"
        )


def extract_all(browser: str = "chrome") -> dict[str, dict]:
    """从指定浏览器提取所有支持平台的 Cookie。

    Args:
        browser: 浏览器名称

    Returns:
        {
            "xhs": {"cookie_string": "a=1; b=2; ..."},
            "bilibili": {"SESSDATA": "xxx", "bili_jct": "yyy"},
            "zhihu": {"z_c0": "xxx", "_xsrf": "yyy"},
            "douyin": {"cookie_string": "..."},
        }

    Raises:
        RuntimeError: Cookie 库不可用
    """
    cookies = _load_browser_cookies(browser)

    result: dict[str, dict] = {}

    for spec in PLATFORM_SPECS:
        domains = spec["domains"]
        wanted = spec["cookies"]
        config_key = spec["config_key"]

        # 过滤出该域名的 Cookie
        matched = [
            c for c in cookies
            if _domain_matches(getattr(c, "domain", ""), domains)
        ]

        if not matched:
            logger.debug(f"[_cookie_extract] {spec['name']} 无 Cookie")
            continue

        if wanted is None:
            # 全量拼接成字符串
            cookie_str = "; ".join(
                f"{c.name}={c.value}" for c in matched
            )
            result[config_key] = {"cookie_string": cookie_str}
        else:
            # 只提取指定 name
            picked = {}
            for c in matched:
                if c.name in wanted:
                    picked[c.name] = c.value
            if picked:
                result[config_key] = picked

    return result


def get_cookie_string(platform: str, browser: str = "chrome") -> str:
    """便捷函数：获取指定平台的 Cookie 字符串。

    Args:
        platform: 平台 config_key（xhs / bilibili / zhihu / douyin）
        browser: 浏览器名称

    Returns:
        Cookie 字符串（"a=1; b=2; ..."），无数据时返回 ""
    """
    all_cookies = extract_all(browser)
    plat_data = all_cookies.get(platform, {})

    if "cookie_string" in plat_data:
        return plat_data["cookie_string"]

    # 拼接成字符串
    return "; ".join(f"{k}={v}" for k, v in plat_data.items())


def get_cookie_dict(platform: str, browser: str = "chrome") -> dict[str, str]:
    """便捷函数：获取指定平台的 Cookie 字典。

    Args:
        platform: 平台 config_key
        browser: 浏览器名称

    Returns:
        {"SESSDATA": "xxx", "bili_jct": "yyy", ...}
    """
    all_cookies = extract_all(browser)
    plat_data = all_cookies.get(platform, {})

    if "cookie_string" in plat_data:
        # 解析回字典
        result = {}
        for pair in plat_data["cookie_string"].split("; "):
            if "=" in pair:
                k, v = pair.split("=", 1)
                result[k] = v
        return result

    return plat_data


def _domain_matches(cookie_domain: str, target_domains: list[str]) -> bool:
    """检查 Cookie 的 domain 是否匹配目标域名列表。"""
    if not cookie_domain:
        return False
    for d in target_domains:
        if cookie_domain == d or cookie_domain.endswith(d):
            return True
        # 去掉前导点再匹配
        bare = d.lstrip(".")
        if cookie_domain == bare or cookie_domain.endswith(bare):
            return True
    return False
