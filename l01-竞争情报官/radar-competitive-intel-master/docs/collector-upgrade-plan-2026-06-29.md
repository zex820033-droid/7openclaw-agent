# 竞争情报采集管道升级计划 v1.0

> **编制**：Fengniao 竞争情报官 | **日期**：2026-06-29  
> **依据**：Super-AIGC `collectors/` 开源代码审计（58个.py文件，含 Agent-Reach 子项目）  
> **目标**：将今日4/5 SPA站点封锁率（知乎❌·小红书❌·快手❌·抖音🟡）降至 0/5

---

## 一、现状诊断

### 1.1 当前采集管道架构

```
L1: autocli Public 命令      → 覆盖: HN/devto/lobsters/stackoverflow/v2ex (5个)
L2: 直连API (curl/python)     → 覆盖: B站/微博/知乎热榜/抖音热搜/快手热点/头条/CSDN/V2EX (8个)
L3: web_fetch / Playwright    → 覆盖: 任意URL (但今日实测 4/5 SPA 被反爬)
```

### 1.2 今日封锁复盘

| 平台 | 封锁原因 | 本应可用的方法 | 为什么没用上 |
|------|---------|-------------|------------|
| **知乎搜索** | SPA+反爬 | `search_v3` API → 返回 `HitLabels:null` | API端点不正确，需要Playwright+登录态 |
| **小红书** | SPA+强登录墙 | `xiaohongshu-mcp` | 未安装；且我不知此工具存在 |
| **快手搜索** | SPA+登录墙 | Playwright+Stealth | 我的Playwright调用了**裸Chromium**，无隐身 |
| **抖音搜索** | SPA+反爬 | Playwright+ApiUrlCapture | 同上；且搜索需要拦截签名API URL |

### 1.3 根因

> **我的 Playwright 是裸奔的。** 没有注入 `STEALTH_JS`，没有 `playwright-stealth` 包，没有 WebGL 欺骗，没有持久化上下文。反爬系统一眼识别出自动化痕迹。

---

## 二、武器清单（从开源项目直接复制）

### 2.1 核心武器（必装·3件）

| # | 武器 | 源文件 | 复制到 | 功能 |
|:--:|------|--------|--------|------|
| **W1** | `STEALTH_JS` | `collectors/_stealth.py` | `tools/stealth.js` | 10层浏览器隐身脚本 |
| **W2** | `PlaywrightSession` | `collectors/playwright_session.py` | `tools/playwright_session.py` | 生产级Playwright会话管理器 |
| **W3** | `NETWORK_CAPTURE_JS` | `collectors/_stealth.py` | `tools/api_discovery.js` | API端点自动发现 |

### 2.2 扩展武器（选装·3件）

| # | 武器 | 源文件 | 集成方式 | 功能 |
|:--:|------|--------|---------|------|
| **W4** | `xiaohongshu-mcp` | Agent-Reach引用 | 安装外部包 `npm i -g xiaohongshu-mcp` | 小红书搜索/笔记详情 |
| **W5** | `PINIA_STORE_JS` | `collectors/_stealth.py` | `tools/pinia_extract.js` | Vue SPA状态直接提取 |
| **W6** | `RateLimiter` | `collectors/_utils.py` | `tools/rate_limiter.py` | 自适应请求频率控制 |

### 2.3 参考架构（不复制·学习模式）

| # | 模式 | 源文件 | 学习什么 |
|:--:|------|--------|---------|
| **P1** | API拦截模式 | `douyin/douyin_works_collector.py` | `ApiUrlCapture` 类：通过 `page.on('request')` 拦截浏览器发出的API请求，提取完整签名URL |
| **P2** | 浏览器守护进程 | `collectors/_browser_daemon.py` | FastAPI + Playwright 长生命周期，多任务复用同一浏览器进程 |
| **P3** | 三层回退 | `_direct_crawlers/zhihu.py` | API → HTML → 抛异常的降级链模式 |

---

## 三、三级管道升级方案

### 3.1 L1 管道（autocli Public）— 无需改动

当前状态：✅ 正常  
现有5个Public命令已验证可用，不涉及SPA反爬问题。

### 3.2 L2 管道（直连API）— 补全端点

**现有缺口**：

| 平台 | 当前状态 | 补全动作 |
|------|---------|---------|
| 知乎搜索 | ❌ 端点错误 (`search_v3` 失效) | 🔧 改用 `search_v2` 或 Playwright 方案 |
| 小红书 | ❌ 无端点 | 🔧 接入 `xiaohongshu-mcp` (W4) |
| B站搜索 | ✅ 正常 | — |
| 微博热搜 | ✅ 正常 | — |

**新增端点配置** (`data/direct-crawler-apis.json`)：

```json
{
  "id": "zhihu_search",
  "name": "知乎搜索（备用端点）",
  "endpoints": {
    "primary": "https://www.zhihu.com/api/v4/search_v3?q={keyword}&type=content&t=general&limit=20",
    "fallback_playwright": "Playwright+Stealth → 拦截真实搜索请求"
  }
}
```

### 3.3 L3 管道（Playwright/web_fetch）— 🔥 核心改造

这是本次升级的重中之重。当前 L3 是"裸Playwright"，改造后变为：

```
L3 新架构:
  PlaywrightSession (W2)
  ├── playwright-stealth 包 (自动)
  ├── STEALTH_JS 注入 (W1)
  ├── WebGL 欺骗 (内置)
  ├── 持久化上下文 (Cookie保存)
  └── 系统浏览器回退 (Edge→WebView2→Chrome)
```

**改造前后对比**：

| 维度 | 改造前（今天） | 改造后 |
|------|:---:|------|
| navigator.webdriver | `true` ❌ | `undefined` ✅ |
| WebGL 渲染器 | `SwiftShader` ❌ | `NVIDIA RTX 3060` ✅ |
| Chrome插件数 | 0 ❌ | 5 ✅ |
| headless 检测 | 可检测 ❌ | 伪装 Win32/8核/8GB ✅ |
| 登录态持久化 | 无 | Cookie自动保存到磁盘 |
| 请求频率控制 | 无 | 随机延迟3-6秒 + 指数退避 |
| 小红书可采集 | ❌ | 🟡 需 xiaohongshu-mcp |

---

## 四、分阶段执行计划

### Phase 1：立即见效（今天·30分钟）

| 步 | 动作 | 产出 | 验证方式 |
|:--:|------|------|---------|
| 1.1 | 从 `_stealth.py` 提取 `STEALTH_JS` → `tools/stealth.js` | 10层隐身脚本文件 | `wc -l tools/stealth.js` |
| 1.2 | 改造我的 Playwright 调用模板，注入 `STEALTH_JS` | `tools/playwright_stealth_runner.py` | 跑知乎搜索→有结果≠空 |
| 1.3 | 安装 `playwright-stealth` 包 | `pip install playwright-stealth` | `python -c "import playwright_stealth"` |
| 1.4 | 用改造后的Playwright重跑今日4个失败平台 | 实际采集结果 | 至少知乎/小红书有内容输出 |
| 1.5 | 将 `NETWORK_CAPTURE_JS` 独立保存 | `tools/api_discovery.js` | 文件存在 |

### Phase 2：管道加固（本周·2小时）

| 步 | 动作 | 产出 |
|:--:|------|------|
| 2.1 | 复制 `PlaywrightSession` 核心逻辑 → `tools/playwright_session.py` | 独立可用的会话管理器 |
| 2.2 | 复制 `RateLimiter` → `tools/rate_limiter.py` | 所有API调用统一限速 |
| 2.3 | 更新 `data/direct-crawler-apis.json`，补全搜索端点 | 管道配置完整 |
| 2.4 | 安装 `xiaohongshu-mcp`，测试小红书搜索 | 小红书采集合规 |
| 2.5 | 更新 `SKILL.md` §六 状态机，加入增强L3路径 | 文档同步 |

### Phase 3：架构升级（下周·4小时）

| 步 | 动作 | 产出 |
|:--:|------|------|
| 3.1 | 学习 `ApiUrlCapture` 模式，实现抖音搜索 | 抖音关键词搜索可用 |
| 3.2 | 研究 `_browser_daemon.py`，评估是否需要常驻浏览器 | 架构决策文档 |
| 3.3 | 将已验证的模式写回 `SKILL.md` 和 `AGENTS.md` | 知识固化 |
| 3.4 | 全量28竞品扫描压力测试 | 确认管道稳定性 |

---

## 五、平台覆盖矩阵（升级后预期）

| 平台 | 热榜 | 关键词搜索 | 内容详情 | 免登录 | 认证方式 |
|------|:--:|:--:|:--:|:--:|------|
| **B站** | ✅ API | ✅ API | ✅ API | ✅ | 无 |
| **知乎** | ✅ API | 🟡 Playwright+Stealth | ✅ API | 🟡 | 搜索需登录态 |
| **微博** | ✅ API | — | — | ✅ | Referer |
| **抖音** | ✅ API | 🔧 ApiUrlCapture (P3) | — | 🟡 | 搜索需拦截签名 |
| **快手** | ✅ HTML解析 | 🔧 Playwright+Stealth (P3) | — | 🟡 | 搜索需登录 |
| **小红书** | — | 🔧 xiaohongshu-mcp (P2) | 🔧 xiaohongshu-mcp | 🟡 | MCP扫码一次 |
| **头条** | ✅ API | — | — | ✅ | Referer |
| **V2EX** | ✅ API | — | — | ✅ | 无 |
| **CSDN** | ✅ API | — | — | ✅ | Referer |

> 图例：✅=已就绪 | 🟡=Phase 1后可用 | 🔧=P2/P3计划中 | —=不需要

---

## 六、风险与熔断

| 风险 | 概率 | 影响 | 缓解 |
|------|:--:|------|------|
| `playwright-stealth` 装不上 | 低 | 中 | 已有 `STEALTH_JS` 兜底 |
| `xiaohongshu-mcp` 上游停更 | 中 | 低 | 保留 Playwright+Stealth 降级路径 |
| 知乎更新反爬导致 Playwright 也失效 | 中 | 高 | 监控+降级标注 `[BLOCKED]` |
| 复制代码的依赖冲突 | 低 | 低 | 最小化依赖：仅 `playwright` + `playwright-stealth` + `requests` |

---

## 七、验收标准

| # | 标准 | 当前值 | 目标值 |
|:--:|------|:--:|:--:|
| 1 | SPA站点封锁率 | 4/5 (80%) | 0/5 (0%) |
| 2 | 五平台搜索平均响应时间 | 35s | <20s |
| 3 | 搜索数据完整度（有实际内容 vs 空返回） | 1/5 (20%) | 5/5 (100%) |
| 4 | 管道代码复用率（从开源项目直接复制） | 0% | ≥60% |

---

*Fengniao 竞争情报官 | 2026-06-29 | v1.0*
*让采集管道不再是瓶颈。*
