---
name: "cookie-auto-login"
description: "从Chrome/Edge/Firefox浏览器自动提取知乎/小红书/B站的登录Cookie，突破登录墙。免扫码免手工。"
---

# Cookie Auto-Login Skill

## 触发条件
当 Agent 遇到以下场景时激活：
- L2 直连 API 返回 401/403（需要登录）
- L3 Playwright 页面显示"请登录"或"注册后查看"
- 用户问："怎么登录""需要Cookie""扫码登录"
- 搜索知乎/小红书/快手时返回空结果（登录墙）

## 前置条件
- `pip install rookiepy`（推荐，Rust 实现，更稳定）
- 备选：`pip install browser-cookie3`
- 在 Chrome/Edge/Firefox 中**至少登录过一次**目标平台

## 支持的平台

| 平台 | 需要的Cookie | 配置键 |
|------|-------------|--------|
| XiaoHongShu | 全部 Cookie | `xhs_cookie` |
| Bilibili | SESSDATA + bili_jct | `bilibili_sessdata`, `bilibili_csrf` |
| 雪球 | xq_a_token | `xueqiu_cookie` |
| Twitter/X | auth_token + ct0 | `twitter_auth_token`, `twitter_ct0` |

## 工作流程

### Step 1: 提取 Cookie
```python
from tools.cookie_extractor import extract_all

# 浏览器必须关闭（SQLite 文件锁）
cookies = extract_all("chrome")
# → {"xhs": {"cookie_string": "a1=...; web_session=..."}, "bilibili": {"SESSDATA": "xxx"}}
```

### Step 2: 注入到 HTTP 请求
```python
import requests

headers = {"User-Agent": UA, "Referer": "https://www.zhihu.com/"}
if 'zhihu' in cookies:
    headers["Cookie"] = cookies['zhihu']['cookie_string']

resp = requests.get("https://www.zhihu.com/api/v4/search_v3?q=keyword", headers=headers)
```

### Step 3: 注入到 Playwright
```python
context = browser.new_context()
context.add_cookies([
    {"name": k, "value": v, "domain": ".zhihu.com", "path": "/"}
    for k, v in cookies['zhihu'].items()
])
```

## 安全约束
- Cookie 仅在当前 Agent 会话中使用，不持久化到磁盘（除非用户明确要求）
- 提取完成后提示用户重新打开浏览器
- 不提取密码、支付信息等敏感 Cookie
- 注意 `cookie_string` 写入配置时使用 0o600 权限

## 降级路径
- rookiepy 不可用 → 尝试 browser-cookie3
- 浏览器未登录 → 提示用户手动登录一次
- Linux 无桌面 → 提示用 xiaohongshu-mcp 扫码登录

## Skill调用报告格式
```
【Cookie Auto-Login 调用报告】
浏览器: Chrome
提取平台: 小红书(32个Cookie), B站(SESSDATA)
注入目标: 知乎搜索API
结果: ✅ 搜索返回 15 条结果（之前返回空）
```
