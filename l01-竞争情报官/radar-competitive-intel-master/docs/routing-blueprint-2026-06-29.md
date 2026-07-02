# 采集管道升级·路由注册与实施蓝图 v1.0

> Fengniao 编制 | 2026-06-29 10:36  
> 涵盖：Skill创建·配置文件更新·管道状态机重写·工具注册

---

## 一、总体架构

```
                    ┌──────────────────────────────────┐
                    │        SKILL.md §六 状态机        │
                    │   START → L1 → L2 → L3 → DONE    │
                    └──────────┬───────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     ┌────▼─────┐      ┌──────▼──────┐      ┌─────▼──────┐
     │ 3个新Skill│      │ 2个配置文件  │      │ 4个新工具   │
     │ (workshop)│      │ (data/*.json)│      │ (tools/*.py)│
     └──────────┘      └─────────────┘      └────────────┘
     api-discovery      direct-crawler       rate_limiter.py
     cookie-auto-login  autocli-commands     cookie_extractor.py
     channel-health                          api_discoverer.py
                                             page_adapter.py
```

---

## 二、Skill 创建清单（3个·通过 skill_workshop）

### S1: `api-discovery` — API端点自动发现

```yaml
名称: api-discovery
描述: 对任意URL自动发现隐藏JSON API端点。6策略: Performance API/Refetch/.json探测/SSR/Pinia/搜索盲探
触发词: "发现API" "找端点" "API探测" "数据接口" "怎么看这个站的数据"
前置: Playwright + playwright-stealth + tools/api_discoverer.py
```

**路由位置**: SKILL.md §一 任务×Skill映射表 → 新增行：通用工具类（非T1-T6专属）

**注册到管道**: 作为 L3 管道的预检步骤——遇到新站点时，在 Playwright 加载页面后先跑 ApiDiscoverer，获取真实API端点，再决定用L2直连还是 L3 Playwright。

---

### S2: `cookie-auto-login` — 浏览器Cookie提取登录

```yaml
名称: cookie-auto-login
描述: 从Chrome/Edge/Firefox浏览器自动提取知乎/小红书/B站/雪球的登录Cookie，突破登录墙
触发词: "登录" "认证" "Cookie" "需要登录" "登录态" "扫码"
前置: pip install rookiepy + 浏览器中至少登录过一次目标平台
```

**路由位置**: SKILL.md §六 状态机 → 新增降级路径：L3 遇到登录墙 → 触发 `cookie-auto-login` → 注入 Cookie → 重试

**注册到管道**: 作为 L2↔L3 之间的中间层——`L2.5: Cookie注入`。当 L2 API 返回 401/403/需要登录时，自动触发 Cookie 提取并重试。

---

### S3: `channel-health-check` — 管道健康自动巡检

```yaml
名称: channel-health-check
描述: 对所有已配置采集管道做自动化健康检查，替代手动HEARTBEAT.md。逐管道check()→分级报告
触发词: "检查管道" "健康检查" "管道状态" "采集是否正常" "doctor"
前置: 无额外依赖，各管道自带 check() 方法
```

**路由位置**: HEARTBEAT.md → 替换检查C的"来源健康度"手动流程，改为自动巡检。

**注册到管道**: 作为独立定时任务——每日 08:00 在 T5 日报生成前先跑健康检查，报告在日报末尾附注。

---

## 三、配置文件更新清单

### 3.1 `data/direct-crawler-apis.json` — 新增 9 端点

当前文件有 10 个 `pipelines`，需新增以下条目：

```json
{
  "pipelines_additions": [
    {
      "id": "bilibili_search_v2",
      "name": "B站综合搜索",
      "priority": 1,
      "auth": "public",
      "endpoints": {
        "primary": "https://api.bilibili.com/x/web-interface/search/all/v2?keyword={keyword}&page=1"
      },
      "headers": {"User-Agent":"Chrome/125...", "Referer":"https://search.bilibili.com/"},
      "use_case": ["关键词搜索", "竞品提及追踪", "舆情热词"],
      "verified": true
    },
    {
      "id": "bilibili_search_type",
      "name": "B站分类搜索",
      "priority": 2,
      "auth": "public",
      "endpoints": {
        "primary": "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={keyword}&page=1"
      },
      "headers": {"User-Agent":"Chrome/125...", "Referer":"https://search.bilibili.com/"},
      "use_case": ["视频搜索", "UP主内容发现"]
    },
    {
      "id": "zhihu_article",
      "name": "知乎文章正文",
      "priority": 2,
      "auth": "public",
      "endpoints": {
        "primary": "https://www.zhihu.com/api/v4/articles/{article_id}?include=content",
        "fallback": "https://zhuanlan.zhihu.com/p/{article_id} → __INITIAL_STATE__"
      },
      "headers": {"User-Agent":"Chrome/125...", "Referer":"https://www.zhihu.com/"},
      "use_case": ["竞品技术拆解", "产品评测原文"]
    },
    {
      "id": "zhihu_answer",
      "name": "知乎回答正文",
      "priority": 2,
      "auth": "public",
      "endpoints": {
        "primary": "https://www.zhihu.com/api/v4/answers/{answer_id}?include=content,voteup_count,comment_count"
      },
      "headers": {"User-Agent":"Chrome/125...", "Referer":"https://www.zhihu.com/"},
      "use_case": ["产品口碑", "用户评价提取"]
    },
    {
      "id": "zhihu_search",
      "name": "知乎搜索（需Cookie）",
      "priority": 3,
      "auth": "cookie",
      "auth_detail": "需 z_c0 + _xsrf Cookie，通过 cookie-auto-login Skill 提取",
      "endpoints": {
        "primary": "https://www.zhihu.com/api/v4/search_v3?q={keyword}&type=content&t=general&limit=20"
      },
      "headers": {"User-Agent":"Chrome/125...", "Referer":"https://www.zhihu.com/", "Cookie":"z_c0={cookie}"},
      "use_case": ["竞品相关讨论", "关键词舆情"],
      "note": "search_v3 在无Cookie时返回 HitLabels:null"
    },
    {
      "id": "toutiao_hotboard",
      "name": "今日头条热榜",
      "priority": 1,
      "auth": "public",
      "endpoints": {
        "primary": "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
      },
      "headers": {"User-Agent":"Chrome/128...", "Referer":"https://www.toutiao.com/"},
      "use_case": ["信息流热点", "公司快讯", "政策监管信号"],
      "fields_rich": true
    },
    {
      "id": "xiaohongshu_mcp",
      "name": "小红书搜索（MCP）",
      "priority": 2,
      "auth": "qr_login",
      "auth_detail": "xiaohongshu-mcp 扫码一次，运行在 localhost:18060",
      "endpoints": {
        "primary": "mcporter call 'xiaohongshu.search_feeds(keyword: \"{keyword}\")'"
      },
      "install": "npm i -g xiaohongshu-mcp (github.com/xpzouying/xiaohongshu-mcp)",
      "use_case": ["C端用户口碑", "产品种草热度", "竞品舆情"]
    },
    {
      "id": "csdn_hotrank",
      "name": "CSDN热榜",
      "priority": 2,
      "auth": "public",
      "endpoints": {
        "primary": "https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&period=day"
      },
      "headers": {"User-Agent":"Chrome/128...", "Referer":"https://blog.csdn.net/"},
      "use_case": ["AI技术话题热度", "开发者风向"]
    },
    {
      "id": "v2ex_hot",
      "name": "V2EX热帖",
      "priority": 1,
      "auth": "public",
      "endpoints": {
        "primary": "https://www.v2ex.com/api/topics/hot.json"
      },
      "headers": {"User-Agent":"Chrome/128..."},
      "use_case": ["中国开发者讨论", "AI工具口碑"]
    }
  ]
}
```

### 3.2 `data/autocli-commands.json` — 修正 2 条

```json
{
  "corrections": [
    {
      "platform": "bilibili",
      "field": "browser_required",
      "old": "需要Chrome + Extension（Browser模式）",
      "new": "已降级。search/all/v2 纯HTTP API可为Public模式，不需要Browser",
      "action": "将 bilibili 从 browser_required 数组移至 public_verified 数组"
    },
    {
      "platform": "xiaohongshu",
      "field": "browser_required",
      "old": "Browser模式",
      "new": "Browser模式不可用。替换为 xiaohongshu-mcp 后端",
      "action": "从 browser_required 中移除 xiaohongshu，在 competitive_intel_queries 中新增引用"
    }
  ]
}
```

---

## 四、管道状态机重写（SKILL.md §六）

### 4.1 当前状态机

```
START → 读配置JSON → L1 autocli → [L1 fail?] → L2 直连HTTP → [L2 fail?] → L3 Playwright/web_fetch → DONE
```

### 4.2 升级后状态机

```
START
  │
  ├─ 读 direct-crawler-apis.json   (15+端点)
  ├─ 读 autocli-commands.json      (修正后)
  │
  ├─ L1: autocli Public命令        (5平台)
  │    └─ fail → L2
  │
  ├─ L2: 直连HTTP API              (15+端点)
  │    ├─ success → DONE
  │    ├─ 401/403 → L2.5 Cookie注入
  │    └─ timeout/network error → L3
  │
  ├─ L2.5: cookie-auto-login       🆕
  │    ├─ 提取浏览器Cookie
  │    ├─ 注入到L2请求头
  │    └─ 重试L2 → success/fail
  │
  ├─ L3: Playwright + Stealth      (增强版)
  │    ├─ 预检: ApiDiscoverer      🆕 (新站点自动发现API)
  │    ├─ 注入: STEALTH_JS + WebGL
  │    ├─ 渲染: domcontentloaded + 滚动
  │    ├─ 提取: 选择器 + API拦截 + INITIAL_STATE
  │    └─ fail → 降级标注 [BLOCKED]
  │
  └─ L∞: 诚实标注                    (不变)
       └─ 标注平台+原因+建议替代方案
```

### 4.3 状态转移表（写入 SKILL.md §六）

| 当前状态 | 触发条件 | 下一状态 | 动作 |
|---------|---------|:--:|------|
| L1 autocli | 命令不存在/超时 | L2 | exec curl直连 |
| L2 直连API | 200 OK | ✅ DONE | 写入 memory |
| L2 直连API | 401/403 (认证错误) | L2.5 | 触发 cookie-auto-login |
| L2 直连API | timeout/网络错误 | L3 | Playwright fallback |
| L2.5 Cookie | Cookie提取成功 | L2(重试) | 注入Cookie → 重试API |
| L2.5 Cookie | Cookie提取失败 | L3 | Playwright (可能有隐身的无登录可用性) |
| L3 Playwright | 新域名/无缓存 | L3预检 | 运行 ApiDiscoverer |
| L3 Playwright | 页面加载+内容>5行 | ✅ DONE | 写入 memory |
| L3 Playwright | 页面加载但内容≤5行 | L∞ | 标注 [BLOCKED·登录墙] |
| L3 Playwright | 网络错误/timeout | L∞ | 标注 [BLOCKED·网络/反爬] |

---

## 五、工具文件注册清单

| 文件 | 来源 | 状态 | 注册到 |
|------|------|:--:|------|
| `tools/stealth.js` | _stealth.py | ✅ 已完成 | L3 Playwright 自动注入 |
| `tools/api_discovery.js` | _stealth.py | ✅ 已完成 | api-discovery Skill |
| `tools/pinia_extract.js` | _stealth.py | ✅ 已完成 | api-discovery Skill |
| `tools/initial_state_extract.js` | _stealth.py | ✅ 已完成 | api-discovery Skill |
| `tools/stealth_runner.py` | 自编 | ✅ 已完成 | L3 Playwright 模板 |
| `tools/rate_limiter.py` | _utils.py | ⬜ 待复制 | L1/L2/L3 全局限速 |
| `tools/cookie_extractor.py` | cookie_extract.py | ⬜ 待复制 | L2.5 cookie-auto-login |
| `tools/api_discoverer.py` | _api_discovery/ | ⬜ 待复制 | L3预检 api-discovery Skill |
| `tools/page_adapter.py` | page_adapter.py | ⬜ 待复制 | L3 Playwright 封装 |

---

## 六、执行顺序（依赖图）

```
Phase A: 基础工具（无依赖，15分钟）
  ├── A1: 复制 rate_limiter.py
  ├── A2: 复制 page_adapter.py
  └── A3: 复制 cookie_extractor.py

Phase B: 配置文件（依赖Phase A，10分钟）
  ├── B1: 更新 direct-crawler-apis.json (9端点)
  └── B2: 修正 autocli-commands.json (2条)

Phase C: API发现（依赖 A1+A2，20分钟）
  └── C1: 复制 api_discoverer.py

Phase D: Skill 创建（依赖 A-C，30分钟）
  ├── D1: skill_workshop create api-discovery
  ├── D2: skill_workshop create cookie-auto-login
  └── D3: skill_workshop create channel-health-check

Phase E: 状态机重写（依赖 D，15分钟）
  └── E1: 更新 SKILL.md §六 状态机 + 状态转移表
```

---

## 七、Skill Workshop 参数准备

### D1: api-discovery

```
name: api-discovery
description: 对任意URL自动发现隐藏JSON API端点。6策略: Performance API/Refetch/.json探测/SSR/Pinia/搜索盲探。用于新站点无需手动猜API。
proposal_content: (将基于 _api_discovery/ 源码编写)
triggers: ["发现API", "找端点", "API探测", "怎么看这个站的数据", "数据接口", "api discovery"]
```

### D2: cookie-auto-login

```
name: cookie-auto-login
description: 从Chrome/Edge/Firefox浏览器自动提取知乎/小红书/B站的登录Cookie，突破登录墙。免扫码免手工。
proposal_content: (将基于 cookie_extract.py 编写)
triggers: ["登录", "认证", "Cookie", "需要登录", "登录态", "扫码登录"]
```

### D3: channel-health-check

```
name: channel-health-check
description: 对所有已配置采集管道做自动化健康巡检，逐管道check→分级报告，替代手动HEARTBEAT.md。
proposal_content: (将基于 doctor.py + channel check() 模式编写)
triggers: ["检查管道", "健康检查", "管道状态", "采集是否正常", "doctor"]
```

---

## 八、SKILL.md §一 任务×Skill映射表更新

在现有 T1-T6 映射表下方新增 **"通用工具类"** 区块：

```markdown
### 通用工具类 (非T1-T6专属，按需调用)

| 工具 | 核心Skill | 典型触发词 |
|:--:|------|------|
| **API发现** | api-discovery | "发现API"/"找端点"/"怎么看这个站的"/"数据接口" |
| **Cookie登录** | cookie-auto-login | "登录"/"需要登录"/"登录态"/"扫码" |
| **管道巡检** | channel-health-check | "检查管道"/"健康检查"/"采集正常吗"/"doctor" |
```

---

*Fengniao 竞争情报官 | 路由注册蓝图 | 2026-06-29 v1.0*
