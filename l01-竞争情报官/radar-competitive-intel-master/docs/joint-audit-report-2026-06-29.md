# 竞争情报采集管道 — 联合审计报告 v2.0

> Fengniao 编制 | 2026-06-29 10:27-10:45  
> 审计范围：`F:\000WORK\AIGC\Super-AIGC\backend\app\services\benchmark\collectors\` 完整目录  
> 产物：9 个可复制模块 + 3 个可提取 Skill + 5 条配置文件更新

---

## 一、审计总览

| 指标 | Phase 1 已知 | 本轮新发现 | 合计 |
|------|:--:|:--:|:--:|
| 可复制代码模块 | 4 | **5** | 9 |
| 可提取 Skill | 0 | **3** | 3 |
| API 端点补全 | 6 | **9** | 15 |
| 配置文件更新行 | 0 | **5** | 5 |
| 方法论/模式 | 3 | **4** | 7 |

---

## 二、新发现模块（本轮重点·5个）

### M1: API 自动发现引擎 (`_api_discovery/`)

**价值**: 🔥🔥🔥 极高 — 能动态发现任意站点的隐藏API端点

```python
# 核心能力：6 种 API 发现策略
ApiDiscoverer(page).discover(url)
  ├── 1. Performance API 资源捕获（从浏览器资源时间线提取）
  ├── 2. Refetch + 验证（对发现的URL发起fetch确认可用性）
  ├── 3. .json 后缀探测（Reddit 风格：/r/xxx.json）
  ├── 4. __INITIAL_STATE__ SSR数据提取
  ├── 5. Pinia/Vuex Store 状态直接读取
  └── 6. 搜索端点盲探测（/search?q=test, /api/search?q=test, /api/v1/search?q=test）
```

**对我的价值**: 以后遇到新平台，不再需要手动猜API端点。`ApiDiscoverer` 自动找出所有可用的JSON API。

**复制路径**: `_api_discovery/discoverer.py` + `_api_discovery/js_snippets.py` → `tools/api_discoverer.py`

---

### M2: Cookie 自动提取器 (`cookie_extract.py`)

**价值**: 🔥🔥🔥 极高 — 突破登录墙的终极方案

```python
# 从本地浏览器自动提取Cookie（Chrome/Firefox/Edge/Brave/Opera）
agent-reach configure --from-browser chrome

# 支持的平台:
#   Twitter/X: auth_token + ct0
#   XiaoHongShu: 全部Cookie → cookie_string
#   Bilibili: SESSDATA + bili_jct
#   Xueqiu: xq_a_token
```

**对我的价值**: 知乎/小红书/快手的登录墙，可以用这个方案绕过——在本机浏览器登录一次，自动提取Cookie注入Playwright。

**复制路径**: `cookie_extract.py` → `tools/cookie_extractor.py`  
**依赖**: `pip install rookiepy`（推荐，Rust实现，更稳定）

---

### M3: RateLimiter + HTTP重试 (`_utils.py`)

**价值**: 🔥🔥 高 — 完整生产级实现

```python
limiter = RateLimiter(base_delay=4.0, page_increment=0.5)
limiter.wait(page_num=5)  # 自适应: 基础4s + 翻页增量 + 随机jitter ±50% + 指数退避
limiter.on_success()       # 重置失败计数
limiter.cooldown("触发风控")  # 30-60秒冷却

# HTTP 重试（带指数退避，复用连接池）
resp = http_get_with_retry(url, max_retries=3, backoff_base=3.0)
```

**对我的价值**: 替代我目前简陋的 `time.sleep(5)`。直接复制到所有API调用中，防止被风控。

**复制路径**: `_utils.py` → `tools/rate_limiter.py`

---

### M4: 页面适配器模式 (`page_adapter.py`)

**价值**: 🔥 中 — 架构模式，Playwright/Selenium 统一接口

```python
# 统一封装的 page 操作，屏蔽底层驱动差异
page = PageAdapter(playwright_page)
page.goto(url)
data = page.evaluate("document.title")  # 自动转换箭头函数为function IIFE(Selenium兼容)
page.wait_for_selector(".result-item")
```

**对我的价值**: 如果将来需要切换到底层驱动（如用Selenium替代Playwright），这个适配器让切换成本降为零。

**复制路径**: `page_adapter.py` → `tools/page_adapter.py`

---

### M5: 渠道健康检查 (`doctor.py` + `probe.py`)

**价值**: 🔥 中 — 生产运维模式

```python
# 对所有采集渠道做健康检查（每个渠道自己知道怎么check）
results = check_all(config)
# → { "bilibili": {"status":"ok", "active_backend":"bili-cli"}, ... }

# 探测系统命令是否存在及可用
probe = probe_command("bili", ["--version"], timeout=10)
# → probe.ok, probe.status, probe.output
```

**对我的价值**: 这是我 `HEARTBEAT.md` 检查C 的理想替代——自动检测每个管道是否健康，而不是靠我手动检查。

---

## 三、可提取为 Skill 的完整模块（3个）

### S1: `api-discovery` Skill

**提取自**: `_api_discovery/` + `_stealth.py` 中的辅助JS  
**功能**: 对任意给定URL，自动发现其隐藏的 JSON API 端点  
**适用场景**: T1 竞品扫描遇到新站点时自动发现数据源；T6 产品拆解时快速获取结构化数据  
**产出格式**: JSON manifest `{framework, api_endpoints, initial_state, stores}`

---

### S2: `cookie-auto-login` Skill

**提取自**: `cookie_extract.py`  
**功能**: 从本地Chrome/Firefox/Edge自动提取指定平台的登录Cookie  
**适用场景**: 所有需要登录态的平台（知乎/小红书/快手/微博/雪球等）  
**前置条件**: `pip install rookiepy`；在浏览器中至少登录过一次目标平台

---

### S3: `channel-health-check` Skill

**提取自**: `doctor.py` + `probe.py` + 各 `channel/*.py` 的 `check()` 方法  
**功能**: 对已配置的所有采集管道做自动化健康检查，按Tier分级报告  
**适用场景**: 替换我现有的 `HEARTBEAT.md` 手动检查流程  
**产出格式**: Rich格式健康报告 `[✅ 可用] [⚠️ 需配置] [❌ 不可用]`

---

## 四、配置文件更新清单

### 4.1 `data/direct-crawler-apis.json` — 新增 9 个端点

```json
{
  "additions": [
    {"id": "zhihu_search", "api": "zhihu.com/api/v4/search_v3", "note": "需要登录Cookie"},
    {"id": "zhihu_article", "api": "zhihu.com/api/v4/articles/{id}?include=content", "auth": "public"},
    {"id": "zhihu_answer", "api": "zhihu.com/api/v4/answers/{id}?include=content", "auth": "public"},
    {"id": "bilibili_search_v2", "api": "api.bilibili.com/x/web-interface/search/all/v2", "auth": "public", "verified": true},
    {"id": "bilibili_search_type", "api": "api.bilibili.com/x/web-interface/search/type", "auth": "public"},
    {"id": "bilibili_ranking_v2", "api": "api.bilibili.com/x/web-interface/ranking/v2?rid=0", "auth": "WBI签名"},
    {"id": "douyin_hot_search", "api": "douyin.com/aweme/v1/web/hot/search/list/", "auth": "Referer"},
    {"id": "toutiao_hotboard", "api": "toutiao.com/hot-event/hot-board/", "auth": "Referer"},
    {"id": "xiaohongshu_mcp", "api": "localhost:18060 (MCP)", "auth": "扫码一次", "backend": "xiaohongshu-mcp"}
  ]
}
```

### 4.2 `data/autocli-commands.json` — 修正

```json
{
  "corrections": [
    {"platform": "bilibili", "fix": "已验证 search/all/v2 纯HTTP可用，无需Browser模式"},
    {"platform": "xiaohongshu", "fix": "Browser模式不可用。替换为 xiaohongshu-mcp 后端"}
  ]
}
```

### 4.3 `tools/` 目录新文件

```
tools/
├── api_discoverer.py       ← 来自 _api_discovery/ (M1)
├── cookie_extractor.py      ← 来自 cookie_extract.py (M2)
├── rate_limiter.py          ← 来自 _utils.py RateLimiter (M3)
├── page_adapter.py          ← 来自 page_adapter.py (M4)
└── http_retry.py            ← 来自 _utils.py http_get_with_retry (M3)
```

---

## 五、方法论/模式沉淀（7个总）

| # | 模式 | 来源 | 一句话 |
|:--:|------|------|--------|
| P1 | **API拦截模式** | douyin_works_collector.py | page.on('request') 拦截浏览器发出的API请求，提取签名URL |
| P2 | **浏览器守护进程** | _browser_daemon.py | FastAPI 常驻Playwright，多任务复用避免启动开销 |
| P3 | **三层降级链** | zhihu.py | API → HTML解析 → 抛异常，每层独立try/except |
| P4 | **Cookie本地提取** | cookie_extract.py | 从Chrome SQLite直接读Cookie，跳过登录流程 |
| P5 | **自适应限速** | _utils.py RateLimiter | 基础延迟+翻页增量+随机jitter+指数退避+冷却 |
| P6 | **API自动发现** | _api_discovery/ | Performance API + Refetch + .json探测 + Store读取 |
| P7 | **渠道自检** | doctor.py + check() | 每个Channel用check()报告自身状态，doctor只做聚合 |

---

## 六、平台覆盖矩阵（全量 15 API）

| 平台 | 热榜 | 关键词搜索 | 内容详情 | 用户作品 | 免登录 | 端点来源 |
|------|:--:|:--:|:--:|:--:|:--:|------|
| B站 | ✅ v2 | ✅ all/v2 | — | — | ✅ | 纯HTTP |
| 知乎 | ✅ v3 | 🔧 v3(需Cookie) | ✅ v4 articles/answers | 🔧 Playwright | 🟡 | 混合 |
| 微博 | ✅ ajax | — | — | — | ✅ | Referer |
| 抖音 | ✅ aweme | 🔧 ApiUrlCapture | — | 🔧 Playwright | 🟡 | 混合 |
| 快手 | ✅ Apollo | 🔧 Playwright | — | 🔧 Playwright | 🟡 | HTML+JS |
| 小红书 | — | 🔧 xiaohongshu-mcp | 🔧 MCP | — | 🟡 | MCP扫码 |
| 头条 | ✅ hot-board | — | — | 🔧 Playwright | ✅ | Referer |
| CSDN | ✅ hot-rank | — | — | 🔧 Playwright | ✅ | Referer |
| V2EX | ✅ hot.json | — | — | — | ✅ | 纯HTTP |
| 雪球 | 🔧 直连 | — | — | 🔧 Playwright | 🟡 | Referer+Cookie |

> 图例：✅=已就绪 | 🔧=可实施(计划中) | 🟡=需认证 | —=不需要

---

## 七、优先级路线图

### 立即执行（今天）

| 优先级 | 动作 | 耗时 | 影响 |
|:--:|------|:--:|------|
| 🔴 P0 | 复制 `_utils.py` RateLimiter → `tools/rate_limiter.py` | 5min | 所有API调用不再裸奔 |
| 🔴 P0 | 复制 `cookie_extract.py` → `tools/cookie_extractor.py` | 10min | 解锁知乎/小红书登录 |

### 本周

| 优先级 | 动作 | 耗时 |
|:--:|------|:--:|
| 🟡 P1 | 复制 `_api_discovery/` → `tools/api_discoverer.py` | 20min |
| 🟡 P1 | 更新 `data/direct-crawler-apis.json` 补全9个端点 | 10min |
| 🟡 P1 | 更新 `data/autocli-commands.json` 修正B站/小红书 | 5min |

### 可提取 Skill（通过 skill_workshop）

| 优先级 | Skill | 基础模块 |
|:--:|------|---------|
| 🟢 P2 | `api-discovery` | M1 + S1 |
| 🟢 P2 | `cookie-auto-login` | M2 + S2 |
| 🟢 P2 | `channel-health-check` | M5 + S3 |

---

## 八、本次审计的行动清单

- [ ] P0-1: 复制 RateLimiter → `tools/rate_limiter.py`
- [ ] P0-2: 复制 cookie_extract → `tools/cookie_extractor.py`  
- [ ] P1-1: 复制 ApiDiscoverer → `tools/api_discoverer.py`
- [ ] P1-2: 更新 `data/direct-crawler-apis.json` (9个新端点)
- [ ] P1-3: 更新 `data/autocli-commands.json` (B站/小红书修正)
- [ ] P2-1: skill_workshop 创建 `api-discovery` Skill
- [ ] P2-2: skill_workshop 创建 `cookie-auto-login` Skill
- [ ] P2-3: skill_workshop 创建 `channel-health-check` Skill

---

*Fengniao 竞争情报官 | 联合审计完成 | 9模块+3Skill+15API端点*
*从开源项目中提取，零成本复用。*
