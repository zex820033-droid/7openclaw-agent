"""抖音热点直连爬虫 — 无第三方依赖，纯 Python HTTP + JSON

数据来源: https://www.douyin.com/aweme/v1/web/hot/search/list/
无需 Cookie，仅需 Referer 头

复刻自 DailyHotApi src/routes/douyin.ts（简化版，去除已失效的 passport cookie 逻辑）

注意：此爬虫仅作为 60s.viki.moe 的兜底降级方案。
      主采集器仍使用 douyin_hotspot_collector.py 中的 60s API。
"""

import logging
import time

import requests

logger = logging.getLogger(__name__)

HOT_SEARCH_URL = (
    "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    "?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1"
)

COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def fetch_list() -> list[dict]:
    """获取抖音热搜榜单

    Returns:
        [
            {
                "title": "...",
                "url": "https://www.douyin.com/hot/...",
                "hot": 1234567,
                "rank": 1,
                "event_time": "2026-06-23 10:00",
            },
            ...
        ]

    Raises:
        RuntimeError: 请求失败或数据解析异常
    """
    try:
        resp = requests.get(
            HOT_SEARCH_URL,
            headers={
                **COMMON_HEADERS,
                "Referer": "https://www.douyin.com",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"抖音热榜 API 请求失败: {e}") from e

    # 响应结构: {"data": {"word_list": [...]}}
    word_list = data.get("data", {}).get("word_list", [])
    if not word_list:
        if (
            isinstance(data, dict)
            and data.get("status_code")
            and data.get("status_code") != 0
        ):
            raise RuntimeError(
                f"抖音热榜 API 风控: "
                f"status_code={data.get('status_code')} "
                f"msg={data.get('status_msg')}"
            )
        raise RuntimeError("抖音热榜 API 返回空列表")

    result = []
    for idx, item in enumerate(word_list, start=1):
        sentence_id = item.get("sentence_id", "")
        event_time = item.get("event_time", "")
        if isinstance(event_time, (int, float)):
            event_time_str = time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(event_time)
            )
        else:
            event_time_str = str(event_time) if event_time else ""

        result.append({
            "title": item.get("word", ""),
            "url": (
                f"https://www.douyin.com/hot/{sentence_id}"
                if sentence_id
                else ""
            ),
            "hot": int(item.get("hot_value", 0)),
            "rank": idx,
            "event_time": event_time_str,
        })

    logger.info(f"[douyin-direct] 获取 {len(result)} 条热搜")
    return result


# ── 命令行自测 ──
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        items = fetch_list()
        print(f"获取 {len(items)} 条抖音热搜:")
        for item in items[:5]:
            print(f"  {item['rank']}. {item['title'][:30]} | hot={item['hot']}")
    except RuntimeError as e:
        print(f"失败: {e}")
