---
name: "api-discovery"
description: "对任意URL自动发现隐藏JSON API端点。6策略：Performance API/Refetch/.json探测/SSR Store/Pinia/搜索盲探。用于新站点无需手动猜API。"
---

# API Discovery Skill

## 触发条件
当 Agent 遇到以下场景时激活此 Skill：
- 需要搜索/采集一个**新平台**（不在 direct-crawler-apis.json 中）
- 用户问："这个站怎么看数据？""找一下这个站的API""这个平台的数据接口是什么"
- 当前 L2 管道没有对应端点，需要发现 API

## 前置条件
- Playwright + playwright-stealth 已安装
- `tools/stealth.js` 可用（10层隐身）
- `tools/api_discoverer.py` 已就绪

## 工作流程

### Step 1: 启动隐身浏览器
```python
from tools.api_discoverer import ApiDiscoverer
from tools.page_adapter import PageAdapter
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

p = sync_playwright().start()
browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
context = browser.new_context(viewport={'width':1920,'height':1080}, user_agent=UA, locale='zh-CN')
page = context.new_page()
Stealth().apply_stealth_sync(page)
page.add_init_script(open('tools/stealth.js').read())

adapter = PageAdapter(page)
discoverer = ApiDiscoverer(adapter)
```

### Step 2: 执行 6 策略发现
```python
manifest = discoverer.discover(target_url)
```

### Step 3: 解析结果
```python
# manifest 结构:
{
  "framework": {"vue3": true, "pinia": false, "react": false},  # 前端框架
  "api_endpoints": [{"url": "...", "status": 200, "body": {...}}],  # 可用的JSON API
  "initial_state": {...},  # SSR __INITIAL_STATE__ 数据
  "stores": [{...}]  # Pinia/Vuex Store 数据
}
```

### Step 4: 注册到管道
将发现的 API 端点写入 `data/direct-crawler-apis.json`，供后续 L2 直连使用。

## 降级路径
- 若 Performance API 无结果 → 尝试 .json 后缀探测
- 若网站是 Vue SPA → 直接读 Pinia/Vuex Store
- 若网站是 SSR → 提取 `__INITIAL_STATE__`
- 全部无结果 → 退回 L3 Playwright 文本提取

## Skill调用报告格式
```
【API Discovery 调用报告】
目标URL: xxx
框架: Vue3/Pinia
发现端点: 5个
  ✅ /api/v1/search (200, JSON)
  ✅ /api/v2/feed (200, JSON)
  🟡 /api/search?q=test (200, HTML)
新端点已写入 direct-crawler-apis.json
```
