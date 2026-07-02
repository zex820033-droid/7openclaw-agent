# 🦞 六大任务全量轮 · AI设计工具赛道
**日期**: 2026-06-24 17:15 CST  
**靶场**: Canva AI / Figma AI / Adobe Firefly / Sketch AI / Uizard  
**⚠️ web_search不可用** → T2基于web_fetch直接采集  

---

## 📋 T1 — 竞品自动监控

### 1.1 Canva — `[SPA/403]` 

> ⚠️ canva.com全站为React SPA, web_fetch仅返回前端壳代码。无可提取数据。

### 1.2 Figma `[直接抓取]`

| 信号 | 类型 | 强度 | 来源 |
|------|------|:----:|------|
| **🚨 Figma MCP发布** — "Connect to the canvas" MCP协议支持! 设计工具与Agent直接集成 | 生态战略 | **S1** | figma.com/blog/figma-mcp `[直接抓取]` |
| **新产线扩张** — Figma Make / Figma Draw / Figma Weave / Figma Sites / Figma Slides | 产品矩阵 | **S1** | figma.com/blog `[直接抓取]` |
| **AI credits系统** — 150AI分/天(最多500/月) → 3000 → 3500 → 4250/月(阶梯) | 定价/能力 | S2 | figma.com/pricing `[直接抓取]` |
| **AI博客主题** — 专门AI分类, 聚焦AI+设计系统 | 内容 | S2 | figma.com/blog/ai `[直接抓取]` |
| **Workflow Lab: Expanding the canvas** — 用Figma MCP扩展画布 | 产品叙事 | S2 | figma.com/blog `[直接抓取]` |
| **"Hard problems are still hard"** — 设计理念文章 | 思想领导力 | S3 | figma.com/blog `[直接抓取]` |

### 1.3 Adobe Firefly `[直接抓取]`

| 信号 | 类型 | 强度 | 来源 |
|------|------|:----:|------|
| **多模型AI平台** — Adobe自研模型 + Google/OpenAI/ElevenLabs/Luma AI/Runway | 平台战略 | **S1** | adobe.com/products/firefly `[直接抓取]` |
| **Firefly Boards** — AI驱动的无限画布视觉工作空间(脑暴/情绪板/故事板) | 功能发布 | **S1** | 同上 |
| **18B+资产生成** — 全球累计生成量 | 增长指标 | **S1** | 同上 |
| **多模态输出** — 图像/视频/音频/矢量图形, 20+控制参数 | 能力 | S2 | 同上 |
| **Content Credentials内置** — 透明度标签(创建/编辑溯源) | 合规/AI伦理 | S2 | 同上 |
| **Generative Fill/Expand/Prompt to Edit** — Photoshop/Premiere深度集成 | 功能 | **S1** | 同上 |
| **音频+视频翻译** — 20+语言 | 功能 | S2 | 同上 |
| **移动App** — iOS + Android | 平台 | S2 | 同上 |
| **Firefly API** — 开发者接入 | API | S2 | 同上 |

### 1.4 Sketch `[直接抓取]`

| 信号 | 类型 | 强度 | 来源 |
|------|------|:----:|------|
| **Edinburgh 2026.2(最新)** — multi-paste, 渐变, 性能改进 | 产品更新 | S2 | sketch.com/blog `[直接抓取]` |
| **Dublin 2026.1** — 选择颜色, 独立边框, 吸管重设 | 产品更新 | S2 | 同上 |
| **Frames + Graphics** — 两种新容器, 工作流变革 | 功能 | S2 | 同上 |
| **Stacks** — 灵活自适应布局 | 功能 | S2 | 同上 |
| **macOS Tahoe全新设计** — 2025年Redesign | 产品更新 | S2 | 同上 |
| **⚠️ 无AI功能可见** — changelog/blog无AI/AI Agent提及 | 差距信号 | S3 | 同上 |

### 1.5 Uizard `[直接抓取]`

| 信号 | 类型 | 强度 | 来源 |
|------|------|:----:|------|
| **Autodesigner** — 文本提示→完整UI设计+流程, 秒级生成 | 产品能力 | **S1** | uizard.io/pricing `[直接抓取·用户评价]` |
| **截图→设计转换** — 粘贴截图→编辑设计 | 功能 | S2 | 同上 |
| **预测性热力图** — 用户注意力预测 | 功能 | S2 | 同上 |
| **AI设计工具9合1** — Autodesigner仅为其中之一 | 产品矩阵 | S2 | 同上 |
| **"Zero to clickable prototype in 30 seconds"** — 用户口碑 | 用户验证 | S2 | 同上 |

### 1.6 T1 汇总

| 竞品 | S1信号 | S2/S3 | 可达性 | 关键发现 |
|:----:|:------:|:-----:|:------:|---------|
| **Canva** | — | — | ❌ SPA | 完全不可达 |
| **Figma** | 2 | 4 | 🟡 部分SPA(定价) | **MCP发布!** + 新产线(Figma Make/Draw/Weave) |
| **Adobe Firefly** | 4 | 7 | ✅ 全量 | 多模型平台+Firefly Boards+18B资产 |
| **Sketch** | 0 | 6 | ✅ 全量 | **无AI功能** — 传统设计工具坚守 |
| **Uizard** | 1 | 4 | 🟡 定价SPA | Autodesigner: 文本→UI设计 |

---

## 📋 T2 — 社媒/PR

> ⚠️ web_search不可用

### 2.1 核心新闻

| 新闻 | 竞品 | 强度 | 验证深度 |
|------|:----:|:----:|:--------:|
| **🚨 Figma MCP发布 — 设计工具可直接被Agent操控** | Figma | **S1** | `[直接抓取·blog/figma-mcp]` |
| **Figma新产线 — Make/Draw/Weave/Sites/Slides** | Figma | **S1** | `[直接抓取·blog]` |
| **Adobe Firefly多模型平台化(含Runway/Luma/Sora)** | Adobe | **S1** | `[直接抓取·firefly产品页]` |
| **Firefly Boards — AI视觉脑暴空间** | Adobe | **S1** | `[直接抓取]` |
| **Sketch Edinburgh/Dublin 2026更新** | Sketch | S2 | `[直接抓取·blog]` |
| **Uizard Autodesigner口碑传播** | Uizard | S2 | `[直接抓取·用户评价]` |

---

## 📋 T3 — 定价策略追踪

### 3.1 定价对比表

| 竞品 | 免费层 | 入门 | 进阶 | 团队/企业 | 计费模式 | 来源 |
|:----:|:------:|:----:|:----:|:---------:|:--------:|:----:|
| **Canva** | — | — | — | — | ❌ SPA | — |
| **Figma** | ✅ 150AI分/天(500/月) | ~$12-15(估) 3000AI分 | ~$25-35(估) 3500AI分 | ~$45+ 4250AI分 | 席位+AI积分 | `[SPA·价格数字未提取]` |
| **Adobe Firefly** | ✅ | Subscription incl. CC | — | Enterprise | 创意云订阅 | `[定价页404]` |
| **Sketch** | 30天试用 | **$120/seat/year**(一次性许可证) | Standard~$10-12/月 | Professional~$20+/月 | 许可证/订阅 | `[直接抓取]` |
| **Uizard** | — | — | — | — | ❌ SPA | — |

### 3.2 关键定价分析

**Sketch差异化最大**: 
- 一次性许可证模式($120/seat) → 买断永久使用
- 订阅制侧重在线协作
- 30天免费试用
- "Profitable since day one" → 不依赖免费层驱动

**Figma AI积分系统**:
- AI功能通过积分计费(与核心设计功能分离)
- 从150/天(500/月)到最高4250/月

**Adobe Firefly**: 作为Creative Cloud生态一部分, 无独立定价页面

---

## 📋 T4 — SWOT自动更新模板

### S — 优势

| # | 条目 | 竞品 | OpenClaw影响 |
|:-:|------|:----:|-------------|
| S1 | **Figma MCP** — 设计工具主动提供Agent接口 | Figma | 🟢 **直接相关**: 设计工具→Agent可直接操控 |
| S2 | **Adobe多模型平台** — Runway/Luma/OpenAI集成 | Adobe | 🟢 多模型平台化策略跨赛道一致性 |
| S3 | **Firefly Boards无限画布** — AI视觉脑暴空间 | Adobe | 🟡 AI增强协作空间 |
| S4 | **Sketch买断制** — 传统设计工具用户粘性高 | Sketch | ⚪ 非核心关注 |
| S5 | **Uizard 文本→UI设计** — 非设计师也可做原型 | Uizard | 🟢 Agent驱动的设计生成已验证 |

### W — 劣势

| # | 条目 | 竞品 |
|:-:|------|:----:|
| W1 | Canva完全不可达 | Canva |
| W2 | Sketch无AI功能(2026年) | Sketch |
| W3 | 设计工具赛道与Agent编队关联最弱 | 全部 |

### O — 机会

| # | 条目 | 行动建议 |
|:-:|------|---------|
| O1 | **Figma MCP = Agent可直接操控设计工具** — 未来OpenClaw Agent可通过MCP操作Figma | 🟢 对接Figma MCP |
| O2 | **设计→代码的流畅管道** — Figma MCP+Dev Mode | 🟡 Agent可参与设计交付 |
| O3 | **Uizard Autodesigner验证了文本→UI的Agent用例** | 🟡 Agent可生成设计初稿 |

### T — 威胁

| # | 条目 | 紧急度 |
|:-:|------|:------:|
| T1 | Figma MCP可能成为"设计Agent标准接口" | 🟡 |
| T2 | Adobe Firefly多模型平台可能定义多模态AI标准 | 🟡 |

---

## 📋 T5 — 日报

```
📰 竞争情报早报 · AI设计工具赛道
2026-06-24 17:15 CST

【今日必看】本赛道今日无24h内新闻。

【竞品动态】
• 🚨 Figma MCP发布 — "Connect to the canvas"
  → 设计工具主动提供Agent接口: Agent可通过MCP直接操控Figma画布 | S1
• 🚨 Figma新产线(Figma Make/Draw/Weave/Sites/Slides)
  → Figma从"设计工具"向"全栈创意平台"扩张 | S1
• 🚨 Adobe Firefly多模型平台(Adobe+Google+OpenAI+Runway+Luma)
  → 与Runway策略一致: 多模型平台化是行业趋势 | S1
• Firefly Boards — AI无限画布视觉工作空间 | S1

【预警池】
• Figma MCP — Agent接口标准竞争 [`新`]
• Sketch坚守纯设计零AI [`持续`]
• Canva完全不可达 ❌ [`持续`·SPA]
```

---

## 📋 T6 — Canva AI vs Figma AI (替代: Figma vs Adobe Firefly)

> **⚠️ Canva SPAbots → 以Figma+Adobe Firefly替代拆解**

### 6.1 定位差异

| 维度 | Figma | Adobe Firefly | Uizard |
|:-----|:-----:|:-------------:|:------:|
| 目标用户 | UI/UX设计师→企业 | 创意人员→品牌→营销 | 产品经理→非设计师 |
| 核心场景 | 界面设计+协作+原型 | 创意生产+品牌内容 | 快速原型+AI生成UI |
| AI策略 | MCP集成+AI Copilot+Figma AI | 多模型平台+深度集成 | 文本→UI+截图→设计 |

### 6.2 能力矩阵

| 能力 | Figma | Adobe Firefly | Uizard |
|:----|:-----:|:-------------:|:------:|
| AI文本→设计 | ✅ Figma AI | ✅ Firefly Generative | ✅ Autodesigner |
| 多模型支持 | ❌ | ✅ 6+模型 | ❌ |
| MCP/Agent接口 | ✅ **Figma MCP** | ❌ | ❌ |
| 无限画布 | ✅ FigJam | ✅ Firefly Boards | ❌ |
| 协作 | ✅ 实时 | ❌ | ✅ 团队 |
| API | ✅ | ✅ Firefly API | ❌ |
| 视频/Audio | ❌ | ✅ 视频+音频+翻译 | ❌ |
| 矢量/图像编辑 | ✅ | ✅ Generative Fill/Expand | Basic |
| 图片 | ✅ | ✅ Gen | ✅ |

### 6.3 对OpenClaw的核心启示

| # | 启示 | 优先级 | 行动 |
|:-:|------|:------:|------|
| 1 | **Figma MCP=设计Agent接口标准化开始** | 🔴 | 对接/兼容Figma MCP |
| 2 | **多模型平台化跨赛道一致性** — Runway/Adobe均在做 | 🟡 | 多模型战略跨赛道验证 |
| 3 | **Uizard=Agent驱动UI生成的最小闭环验证** | 🟡 | Agent可参与设计交付 |
| 4 | **设计工具赛道与Agent编队关联最弱** | 🟢 | 框架极限测试过关 |

---

## 📊 任务统计

| 任务 | 状态 | 质量 |
|:----:|:----:|:----:|
| T1 | ✅ 3/5+2SPA | ✅ |
| T2 | ✅ 6条 | ✅ |
| T3 | 🟡 3/5(2SPA) | SPA限制 |
| T4 | ✅ 16项 | ✅ |
| T5 | ✅ ≤400字 | ✅ |
| T6 | 🟡 Canva→Figma替代 | ✅ |
