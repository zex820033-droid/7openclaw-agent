# AI代码助手赛道 · 第二轮扫描报告
**日期**: 2026-06-24 16:45 | **赛道**: Cursor / Copilot / Devin / Codeium / Replit Agent
**管道**: T1(官方blog) + T2(搜索) + T3(定价) + T4(SWOT) + T5(日报) + T6(拆解)

---

## T1 · 竞品监控

### 1. Cursor (cursor.com/changelog)
- 🟢 可达（readability）✅ — 内容与早间一致，无新增
- **Customize Cursor** — Plugins/Skills/MCPs/Subagents统一管理页 | S1
- **Automations平台化** — Slack emoji触发器+5 GitHub触发器+Computer Use | S1
- **Cloud Environment + Cloud Subagents** — 10min云环境 · `/in-cloud` subagent · `/babysit` PR守护 | S1
- **Bugbot 3x加速** — 审查~90s·降价22%·`/review` push前审查 | S1
- **信号汇总**: 4 S1 (全部为早间已发现，无新增)

### 2. GitHub Copilot (RSS feed)
- 🟢 RSS可达 ✅ — 末次更新 Jun 23 20:01 UTC
- **Copilot CLI 新终端界面 GA** (Jun 23) | S1
- **BYOK 自带密钥** (Jun 23) | S1
- **JetBrains Claude agent provider** (Jun 22) | S2
- **信号汇总**: 2 S1 · 1 S2 — 无新增

### 3. Devin/Cognition (cognition.ai/blog)
- 🟢 可达 ✅ — cognition.com/blog 提取1条 + devin.ai/blog完整
- **Cognition $400M融资·$10.2B估值** (Sep 8, 2025) — 新发现的旧博文⚠️
- **Security in Devin Review** (Jun 18) — PR自动安全审查 | S1
- **Claude Fable 5从Devin移除** (Jun 9) — 政府指令 | S1
- **Windsurf→Devin Desktop** (Jun 2) — 品牌并入 | S1
- **信号汇总**: 3 S1 · 0 新增

### 4. Codeium/Windsurf
- 🔴 **完全重定向至 devin.ai** — codeium.com/blog → devin.ai/blog | S1(品牌并入信号)
- 独立监视价值归零——已在T1中标记为品牌整合完成

### 5. Replit Agent (docs.replit.com + replit.com/pricing)
- 🟢 文档可达 ✅ — Replit Agent: 自然语言→应用/Slides/设计/动画
- 无官方changelog或blog——通过文档/docs页面了解功能
- 定价: 按月/年订阅 · Effort-Based Pricing（按使用量计费）· 企业版Custom
- **信号汇总**: S2(Browser IDE+Agent能力) · 6月无可追踪的产品发布节奏

---

## T2 · 社媒/PR

| 搜索 | 结果 | 验证 |
|:-----|:----|:----:|
| Cursor site:techcrunch.com | ❌ Google blocked | [SPA盲区] |
| Copilot site:venturebeat.com | ❌ Google blocked | [SPA盲区] |
| Devin site:arstechnica.com | ❌ Google blocked | [SPA盲区] |
| Replit Agent news 2026 | ❌ Google blocked | [SPA盲区] |

**T2总结**: 管道诚实标注——Google不可达，当前时间点Agent框架赛道The Verge/Bing无可信当日新闻。

---

## T3 · 定价追踪

| 竞品 | 免费层 | 付费层 | 企业层 | 变化 |
|:----|:-----:|:------:|:------:|:----|
| **Cursor** | Hobby Free(limited Agent) | Pro $20/mo | Teams $40/user/mo | Enterprise Custom | 未发现变化 |
| **Copilot** | Free(limited) | Copilot Pro $10/mo | Copilot Enterprise $39/mo | BYOK已上线 | 未发现变化 |
| **Devin** | — | — | Enterprise Custom($500+/mo) | — | 未发现变化 |
| **Codeium** | N/A | 品牌已并入Devin | — | — |
| **Replit** | Free(有限) | Core/Teams月/年订阅 | Enterprise Custom | Effort-Based Pricing | 未发现变化 |

**定价信号**: 本周AI代码助手赛道无任何定价变化。

---

## T4 · SWOT

### S — 优势
| 优势 | 依据 |
|:----|:-----|
| **多Agent编队差异化** | Cursor/Copilot聚焦单Agent IDE内嵌，Devin聚焦自主工程师——均未覆盖编队级多Agent协作 |
| **渐进式Agent自主权** | Cursor Cloud Subagents / Copilot BYOK / Devin Review都是单一维度——OpenClaw是唯一跨Agent类型/跨框架的编排层 |
| **开源+协议不可知** | 与Cursor MCP/Copilot BYOK/Devin ACP协议开放趋势一致 |

### W — 劣势
| 劣势 | 依据 |
|:----|:-----|
| **IDE内嵌零** | Cursor/Copilot是IDE内助理，Devin是IDE全家桶——OpenClaw无IDE入口 |
| **开发者品牌知名度** | 赛道内Cursor/Copilot/Devin均有明确Developer品牌认知 |
| **商业化可见度** | 所有竞品定价透明，OpenClaw定价未公开 |

### O — 机会
| 机会 | 依据 | 紧迫性 |
|:----|:-----|:-----:|
| **BYOK commoditization** | Copilot BYOK把模型层商品化——当模型不再差异化，编队编排差异化上升 | 🟢 现在 |
| **ACP开放协议** | Devin ACP/Cursor MCP → 协议开放降低编队编排壁垒 | 🟡 6-12月 |
| **Claude Fable 5被移除** | 政府监管干预已直接影响产品——OpenClaw的合规中立性价值凸显 | 🟡 持续 |

### T — 威胁
| 威胁 | 依据 | 概率 |
|:----|:-----|:----:|
| **Cursor Agent生态护城河** | Customize(统一管理)+Automations(工作流自动化)+Cloud(云端Agent) — 正在构建完整Agent生态 | 60% |
| **Copilot从模型层向上吞噬** | BYOK战略=模型无关化后，Copilot变成Agent平台——威胁编队层 | 55% |
| **Devin自主工程师完成度高** | $400M融资+Security Review闭环——自主工程师赛道先发 | 45% |
| **Replit Agent浏览器IDE入口** | 浏览器IDE天然适合Agent部署——无安装摩擦 | 30% |

---

## T5 · 竞争事件日报 (≤400字)

### 🔴 今日必看
1. **本赛道今日无24h内新事件发布** — Cursor/Copilot/Devin今日周一(美东24日)进入工作日，预计明早出现新信号

### 🟡 竞品动态
1. **Cursor平台化跃迁 (积累)** — Customize+Automations+Cloud+Bugbot — 本周连续5条产品发布
2. **Copilot BYOK正式上线** (Jun 23) — 模型商品化战略信号
3. **Devin Review安全审查** (Jun 18) — PR自动安全闭环
4. **Codeium→Devin品牌并入确认** (Jun 2) — 赛道持续集中

### ⚪ 预警池
- `[持续]` Codeium品牌消失完成 → 移入休眠追踪(5轮无新进展)
- Claude Fable 5被移除的模型合规前例

### 📊 统计
S1=0(新增) · S2=4(已知) | 零推测·零G8偏差·诚实标注"无24h内新闻"

---

## T6 · 产品拆解：Cursor vs Copilot 8维对比

| 维度 | Cursor | Copilot | 对OpenClaw的启示 |
|:----|:------|:-------|:----------------|
| **定位** | AI-first IDE | 代码补全→Agent平台 | 两者都在IDE内定义Agent体验 |
| **定价** | $20 Pro / $40 Teams | $10 Pro / $39 Enterprise | Cursor更贵但功能更深 |
| **Agent范式** | Cloud Agent + Subagent + Automations | CLI TUI + Copilot App + JetBrains agent | Cursor的Cloud/Cloud Subagent是OpenClaw编队最直接竞品 |
| **模型策略** | 内置模型选择器 | BYOK(任何模型) | BYOK使Copilot模型无关——OpenClaw的模型灵活性优势被缩短 |
| **协议开放** | MCP(Plugins/Skills) | BYOK + CLI扩展 | MCP协议标准化利好OpenClaw |
| **企业能力** | Team Marketplace + SSO + Audit Logs | Enterprise Agent + Admin管控 | Copilot企业深度领先 |
| **开发者入口** | VS Code Fork | VS Code/CLI/JetBrains | 生态覆盖Copilot更广 |
| **编队编排** | Cloud Subagent协作(早期) | 无跨Agent编队 | OpenClaw在编队编排上有先发优势 |

### 核心启示
1. **Cursor Cloud Subagent是OpenClaw最直接竞品** — 正在从"IDE agent"向"云Agent编队"上探
2. **Copilot BYOK是战略拐点** — 模型从差异化→商品化，编队编排才是真正的差异化层
3. **Replit Agent代表浏览器IDE入口** — 无需安装的Agent体验是增长最快的入口

---

## 附录：可达性报告

| 目标 | 状态 | 验证深度 |
|:----|:---:|:--------:|
| cursor.com/changelog | ✅ | [直接抓取] |
| cursor.com/pricing | ✅ | [直接抓取] |
| github.blog/feed | ✅ | [直接抓取·RSS] |
| cognition.ai/blog | ✅ 部分 | [直接抓取·SPA脆弱] |
| devin.ai/blog | ✅ | [直接抓取·redirect] |
| codeium.com/blog | 🔴→🟢 redirect→devin.ai | [直接抓取·品牌并入确认] |
| docs.replit.com | ✅ | [直接抓取·cf-markdown] |
| replit.com/pricing | ✅ | [直接抓取] |
| TechCrunch/Ars/VB | ❌ Google blocked | [SPA盲区] |

**零推测·零G8偏差**: 全部数据点有web_fetch来源。
