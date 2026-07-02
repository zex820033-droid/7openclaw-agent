# SPA穿透修复报告 — 可灵+Vidu补全 + T2扩展

> **时间**: 2026-06-23 13:05 CST  
> **工具**: Playwright+Chrome (Chrome 149.0.7827.115)  
> **问题**: D-028(凌晨) 7/7 SPA穿透成功 → 数小时后退化到0/4

---

## 一、Playwright穿透结果

| 站点 | web_fetch | Playwright | 关键发现 |
|:----|:---------:|:----------:|:---------|
| **klingai.com** | ❌ SPA空壳 | ✅ **穿透** | "Kling's global website has migrated to kling.ai" — 视频3.0+3.0 Omni, 多模态, 超长视频, 音画同步 |
| **klingai.com/pricing** | ❌ SPA空壳 | ⚠️ 同首页 | 定价页重定向到同一SPA首页 — 定价需登录 |
| **vidu.cn** | ❌ SPA空壳 | ✅ **穿透** | "全球领先的AI内容生产平台", Vidu Claw, 多主体参考生视频, 首帧尾帧, 漫画, 数千万用户 |

### Vidu关键情报（Playwright穿透获得）

| 功能 | 详情 |
|:----|:------|
| **Vidu Claw** | AI创意员工，输入想法即刻解锁无限场景 |
| **参考生视频** | 全球首个，保持角色/物体/场景一致性 |
| **主体库** | 保存角色/道具/场景，一键选择参考 |
| **首帧尾帧** | 自动填充流畅过渡 |
| **漫画功能** | 图片→动画视频 |
| **视频模板** | 亲吻/拥抱/万物生花/AI换装等爆款模板 |
| **社区"多参宗"** | 教程/比赛/创作者舞台 |
| **用户评价** | 多主体参考生视频解决了AI视频角色一致性问题，在2D动画方面表现出色 |

### 可灵Kling关键情报（Playwright穿透获得）

| 功能 | 详情 |
|:----|:------|
| **视频3.0 & 3.0 Omni** | 全面升级底层架构，原生支持多模态指令的深度解析与跨任务融合 |
| **超长视频** | 精准分镜，音画同步的特征解耦 |
| **视觉主体+听觉音色双重绑定** | 复杂场景的跨时空调度 |
| **国际化** | Global网站已迁移至kling.ai |

### 2条PI信号更新

- Kling 3.0 Omni: 多模态指令解析+音画同步 → 中国AI视频技术实力超预期
- Vidu Claw: AI创意员工+多主体参考 → 中国企业端AI视频创新

---

## 二、T2扩展 — 从4条→8条

| # | 信号 | 来源URL | 日期 | 信号 |
|:-:|:-----|:--------|:----:|:----:|
| 1 | Sora关停(官方确认) | https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 官方 | S1 |
| 2 | Alibaba HappyHorse #2全球 | https://venturebeat.com/technology/alibabas-ai-video-model-rises-to-no-2-in-global-rankings/ | Jun 22 | S1 |
| 3 | Seedance因好莱坞版权被参议员要求关停 | https://www.cnbc.com/2026/03/17/bytedance-seedance-shut-down-tiktok-marsha-blackburn-peter-welch.html | Mar 17 | S1 |
| 4 | 挪威AI学校禁令(1-7年级禁用) | https://www.reuters.com/technology/norway-imposes-near-ban-ai-elementary-school-2026-06-19/ + theverge.com | Jun 19 | S1 |
| 5 | Cursor Automations + $2B年收入 | https://techcrunch.com/2026/03/05/cursor-is-rolling-out-a-new-system-for-agentic-coding/ | Mar 5 | S1 |
| 6 | Runway Gen-4.5详细介绍(NVIDIA+Hollywood) | https://runwayml.com/research/introducing-runway-gen-4.5 | Dec 1 2025 | S1 |
| 7 | Runway GWM-1世界模型(实时交互模拟) | https://runwayml.com/research/introducing-runway-gwm-1 | Dec 11 2025 | S1 |
| 8 | Runway Characters实时视频Agent | https://runwayml.com/product/characters | 现时 | S1 |

---

## 三、修复报告

修复完成。已补全可灵+Vidu Playwright穿透数据到 `stage2-fresh-video-gen-2026-06-23.md`。

已写I-009到EVOLUTION.md。已更新AGENTS.md T1 SOP。自省文已写入。
