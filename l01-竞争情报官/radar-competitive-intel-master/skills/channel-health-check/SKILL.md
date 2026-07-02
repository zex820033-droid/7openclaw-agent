---
name: "channel-health-check"
description: "对所有已配置采集管道做自动化健康巡检，逐管道check→Tier分级报告，替代手动HEARTBEAT.md。"
---

# Channel Health Check Skill

## 触发条件
- 每日定时（建议 08:00，在 T5 日报生成前）
- 用户问："检查管道""健康检查""采集正常吗""doctor""管道状态"
- T5 日报产出为空时触发诊断

## 设计理念
每个采集管道**自检自身状态**，健康检查只做聚合。借鉴 Super-AIGC `doctor.py` 的 `check()` 模式。

## 工作流程

### Step 1: 逐管道自检
```
L1 autocli 管道:
  - autocli hn status        → 是否可用
  - autocli devto status     → 是否可用

L2 直连API 管道:
  - curl bilibili search API → code==0?
  - curl zhihu hot API       → data非空?
  - curl douyin hot API      → status_code==0?
  - curl weibo hot API       → 返回JSON?
  - xiaohongshu-mcp 服务     → localhost:18060 可达?

L3 Playwright 管道:
  - playwright-stealth 包    → import成功?
  - stealth.js 脚本          → 文件存在?
  - Chromium 二进制           → executable存在?
```

### Step 2: Tier 分级
```
Tier 0 (装好即用·零配置):
  ✅ web (Jina Reader)
  ✅ bilibili_search_v2 (纯HTTP)
  
Tier 1 (免费密钥/登录·一次性配置):
  ✅ bilibili (bili-cli / OpenCLI)
  🔧 xiaohongshu (MCP·未安装)
  🔧 zhihu_search (需Cookie)
  
Tier 2 (付费API·可选):
  ⬜ exa_search (需API Key)
```

### Step 3: 输出健康报告
```
📊 采集管道健康报告 [2026-06-29 08:00]

✅ 可用: 8/12 (67%)
  L1: hn, devto, lobsters, stackoverflow, v2ex
  L2: bilibili_search, weibo_hot, douyin_hot
  L3: Playwright+Stealth

🔧 需配置: 3/12 (25%)
  xiaohongshu: xiaohongshu-mcp 未安装
  zhihu_search: z_c0 Cookie 未配置
  kuaishou_works: 浏览器登录态缺失

❌ 不可用: 1/12 (8%)
  google_search: GFW拦截(预期·非故障)

⚠️ 建议: 安装 xiaohongshu-mcp → npm i -g xiaohongshu-mcp
```

### Step 4: 注入到 T5 日报
在每日简报末尾附加一行管道状态摘要：
```
---
📡 管道: ✅8 🔧3 ❌1 | 建议: 装 xiaohongshu-mcp
```

## 降级路径
- 单个管道 check() 失败 → 不阻断其他管道，标记后继续
- 所有管道失败 → 报告"全部采集管道异常" → 触发 P1 预警

## Skill调用报告格式
```
【Channel Health Check 报告】
执行时间: 2026-06-29 08:00 CST
管道总数: 12
可用: 8 ✅ | 需配置: 3 🔧 | 不可用: 1 ❌
健康度: 67%
建议: [按优先级排序的修复建议]
```
