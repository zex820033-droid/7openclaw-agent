# MEMORY.md — 竞争情报(Fengniao) 长期记忆

> 最后更新：2026-06-25 (分级一致性规则固化 · Menlo $3B S2 终局裁决 · 训练师签退 · 基础设施信号规则固化 · T2 Cron 降频落地)
> 信任等级：🟡 成员 → 🟢 核心候选（4轮零回退 + 饱和自判授权）

## 📌 休眠追踪（预警池条目 ≥5 轮无新进展 · 下次同维度信号唤回）

| 条目 | 休眠日期 | 原信号 | 唤回条件 |
|------|:--:|------|---------|
| Config Smells (上下文膨胀/技能泄漏/指令冲突) | 06-24 | S1·06/18·InfoWorld | 新Config Smells研究/AI Agent治理标准发布/OpenClaw相关事件触发 |
| BYOK差异化窗口收窄 (Copilot BYOK) | 06-25 | S1·06/23·GitHub | 新竞品BYOK升级/多模型赛道新竞争者出现 |
| 云端Agent代差 (Cursor三重飞轮) | 06-25 | S1·06/18·Cursor | Cursor Cloud/Subagents/Automations新变化/OpenClaw云端Agent上线 |

---

## 一，方法论演进

### M-001：RSS Feed Fallback 方法论（2026-06-24 固化）

**发现**：GitHub Blog Changelog (`github.blog/changelog/label/copilot/`) 为 SPA 页面，web_fetch 可能返回空壳（仅标题/导航，正文缺失）。

**突破**：同一域名下的 RSS feed (`/feed/` 后缀) 返回结构化 XML，可被 web_fetch 解析为完整文本。Copilot CLI GA 通过此方法成功抓取。

**固化规则**：
```
任何官方 blog/news 首页 web_fetch 返回空壳 →
  ① 先试 RSS feed（URL + /feed/ 后缀）
  ② RSS 不可用 → 切第三方科技媒体（The Verge / TechCrunch / Ars Technica）
  ③ 禁止仅以"web_fetch空壳"跳过数据收集
```

**已知 RSS Feed**：
- GitHub Copilot Changelog: `https://github.blog/changelog/label/copilot/feed/`
- 通用 GitHub Changelog: `https://github.blog/changelog/feed/`

**已写入**：T1 Micro cron prompt — RSS Fallback 段

### M-003：AI 基础设施层信号传递规则（2026-06-25 Trainer 审阅固化）

**背景**：OpenAI 自研推理芯片 → 判为非 AI 编码赛道 S2。Trainer 指出不应完全丢弃。

**固化规则**：
```
当 S2/S3 信号虽非「AI 编码赛道」（非 coding tool/IDE/Agent 框架）
但属于 AI 基础设施层时，判定为「基础设施层·下游利好/利空」:
  - 推理芯片/硬件：成本下降 → 所有 Agent 运营成本下降 → 下游利好
  - 云计算/API 降价：Agent 边际成本下降 → 下游利好
  - 模型训练成本下降：新进入者壁垒降低 → 竞争加剧 → 下游利空
  - 基础设施并购：改变基础设施格局 → 需评估对下游供应商依赖度

处理流程：
  ① 保留原信号评级（S2/S3），不丢弃
  ② 标注「基础设施层·下游[利好/利空]」
  ③ 在 T5 日报中保留，注明对 OpenClaw 的间接影响链
  ④ 不因「非赛道」直接丢弃 AI 基础设施层信号
```

---

## 二，竞品列表

### 核心竞品（T1 覆盖）
| 竞品 | 监控URL | RSS Fallback |
|------|---------|:---:|
| Cursor | cursor.com/changelog | — |
| GitHub Copilot | github.blog/changelog/label/copilot/ | `/feed/` ✅ |
| Devin | cognition.ai/blog | — |
| Codeium (→Devin) | codeium.com/blog→devin.ai/blog (301确认) | — |

---

## 三，已知 SPA 盲区

| 站点 | 盲区类型 | Fallback |
|------|---------|---------|
| github.blog/changelog/* | SPA 渲染 | RSS `/feed/` |
| anthropic.com/news | SPA 渲染 | The Verge AI 首页 |
| cursor.com/changelog | 可能 SPA | 待验证 |
| 36kr.com / huxiu.com | 反爬 | 备用搜索引擎摘要 |
| techcrunch.com | ~~SPA 渲染~~ → RSS 可用 | RSS `techcrunch.com/feed/` ✅ (2026-06-25) |

---

## 四，关键事件日志

### 2026-06-25（T1 17:45 · Codeium 域名迁移确认 · 饱和扫描）
- **Codeium → Devin 域名合并确认**：codeium.com/blog 301→devin.ai/blog，内容完全一致。MEMORY.md 竞品列表已更新，codeium.com 不再独立监控。
- **T1 17:45 轮饱和跳过**：4站扫描，0新信号——16:16 轮已全部覆盖。T1 管道饱和自判持续稳定。

### 2026-06-25（终·Trainer 审阅闭环 · T2 降频落地）
- **Trainer 审阅回应三项全闭环** ✅：
  1. **T2 Cron 降频**：MEMORY.md 记录 2h 但 cron 实际 30min → 已修复 `everyMs: 7200000`，token 降 75%
  2. **InfoWorld/Ars 源站**：即时 web_fetch 验证 → InfoWorld 非 404（SPA 盲区 content=partial），Ars 确认为持久 SPA 盲区（零文章内容）。下次 T2 尝试 Playwright 穿透
  3. **OpenAI 芯片分类**：接受修正 → 保留 S2 标注「基础设施层·下游利好」→ 规则固化为 M-003
  - Trainer 额外观察：签名一致性 → 后续统一 `Radar/Fengniao` 双签

### 2026-06-25（续·T2 20:15）
- **T2 20:15 训练师反馈闭环** ✅：
  - TechCrunch RSS 新可用确认 → 已写入 §一 M-001 已知 RSS Feed 列表 + §三 SPA 盲区表
  - 三 S3 分级正确但非编码赛道 → 分级能力确认，无需修正
  - 饱和跳过授权继续生效 → 授权状态无变更

### 2026-06-25（续）
- **T5 18:22 闭环** ✅ — 训练师最终签退：
  - T2+T5 双管道「饱和自判跳过」授权正式移交
  - Radar 已完成从受训执行者→自主方法论者的全管道跃迁
  - 授权范围：T1/T2/T5 三条核心管道均具备饱和自判能力
  - 训练师 Session closed.
- **T2 #10 闭环** ✅ — 训练师最终签退：
  - T2 #7→#8→#9→#10 连续 4 轮零回退，源站重构彻底固化
  - **获「饱和自判跳过」授权**：当信号饱和（重复数据/无增量信息）时，Radar 可自主判定跳过冗余采集，无需训练师审批
  - 此授权标志 Radar 从「受训执行者」→「自主方法论者」的实质性跃迁
  - Session closed.
- **T2 #9 闭环** ✅（训练师签退前最后一项检查）：
  - 源站稳定 3 轮连续确认（#7→#8→#9），T2 管道已达稳态运行水平
  - G0 前置检查（源站可达性）从修复态→方法论固化→运营常态，三个阶段完整走通
  - 训练师本日签退。T2 管道不再需要日度训练监督
  - T2 状态：🟢 稳态（源站重构零回退 · freshness=day 硬约束自动执行 · 评分曲线 72→91→稳态）
- **全管道降频自主完成** ✅：
  | 管道 | 变更 | 新节奏 |
  |:--:|------|:--:|
  | T1 | — | 2h（已稳定） |
  | T2 | — | 2h（已稳定） |
  | T5 | 30min→2h | 2h（与T1/T2统一节奏） |
  | T3 | 恢复启用 | 每日 18:26 |
  | T7 | 恢复启用 | 每日 18:40 |
  | T8 | 恢复启用 | 每日 22:57 |
  - T3/T7/T8 此前被标记为 SHADOW-DEPRECATED 但无 Micro 替代——管道缺口已闭合
  - 训练师评价："Radar 自主管理 cron 资源——方法论者成熟标志"
  - ⚠️ 训练师提示：T7（版本发布）/T8（效能分析）偏 Commander 域，若数据可用性出问题可转交
- **T2 #7 闭环**：源站重构连续 2 轮零超龄，修复已从单轮生效固化到系统稳定 ✅
  - 训练师确认：T2 源站重构（web_fetch 空壳→Playwright/RSS fallback + freshness=day 硬约束）稳定
  - G0 前置检查（源站可达性）方法论已沉淀 → 作为 T2 管道的永久前置检查项
  - Self-Harness 标记编队高优先级 → 编队信号待下次呈报 strategist
- **T5 SOP 今日迭代 4 条规则（全闭环）**}
  - 四项元问题消化完成
  - Stage 跃迁信号：从"产出文档"到"验证执行"的实质性跃迁 ✅
  - 训练师确认两 Agent 均展示 Stage 跃迁
- **T5 SOP 今日迭代 4 条规则（全闭环）**：
  | # | 规则 | 说明 |
  |:--:|------|------|
  | ① | 事件时间判定 | 时效基于**事件发布日期**（非管道发现日期），BYOK 26h前发布→降级 |
  | ② | M&A 豁免声明格式 | ≥$1B融资/ARR 10x+增长豁免>7天红线，标注「补遗·N天前·前序遗漏」，豁免仅限本轮 |
  | ③ | 多事件聚类 | S1 覆盖全管道（T1+T2），禁止管道间隐式偏好 |
  | ④ | 跨日即降级 + 首次验证例外 | Jun 23 发布→Jun 24 不入今日必看；例外：本日首次通过新来源验证的信号可保留头条 |
  - 🦞 D-040/D-041/D-042 铁律集固化于 AGENTS.md §8.5
  - 训练师确认：15:28 版 T5 闭环，从执行者到方法论者的跃迁可证 ✅
- **T2 #6 闭环**：72→91（+19pp），今日最陡修复曲线
  - 根因：源站重构（从 web_fetch 空壳 → Playwright/RSS fallback 完整抓取）+ freshness=day 硬约束
  - 关键验证：两项修复在**单轮内**生效——源站直达提升内容完整性，freshness filter 消除超龄噪音
  - 方法论沉淀：源站可达性不应是假设项，应作为 T2 管道的 G0 前置检查
  - ⚠️ 待办：InfoWorld config smells 标记为编队相关信号 → 下次呈报 strategist

### 2026-06-24 (续)
- **Micro T1 cron #3 训练师评估**：质量评分 92/100。2 条核心发现均真实。SPA→RSS fallback 连续 3 轮稳定执行 ✅
  - **扣分项**：BYOK 战略意义评级偏保守（S1→应 S0.5）。理由：Copilot BYOK（多模型接入+本地密钥存储）是范式级战略动作，直接影响 OpenClaw 差异化定位
  - **行动项**：T5 日报展开 BYOK 战略视角——
- Copilot CLI GA 非新发现（上午已知），但 RSS 方法值入档
- **G2 验证深度标注首次通过**：训练师审查确认，cron 产出中 2 条 `[直接抓取]`、3 条 `[二次引用·原始URL未独立验证]` 标注正确。Google 全量屏蔽/Bing 偏倚诚实报告。G2 门禁首次 cron 达标 ✅
- **三项 T5 质量改进全部通过**（训练师下午复审）：
  | 改进项 | 结果 |
  |--------|:----:|
  | 时效分层（≤3d / >3d）— 竞品动态 vs 持续关注 | ✅ |
  | 预警池 `[持续]` 标注 | ✅ 两条均标注 |
  | 管道偏好筛选消除 — S1 覆盖全管道（T1+T2） | ✅ |
  - S1=2 合理：BYOK 上午为 S1 但下午扫描未复现——T1 cron 单轮快照特性，非 T5 聚合缺陷
  - 对应虾规：D-040/D-041/D-042 三项铁律执行到位
- **T2 #4 训练师评估闭环**：评分 90/100 🟢。7条新闻 S1=2 S2=3 S3=1。G8金融单位双标零偏差（$26B/$1B/$492M）。两项待办已修正：
  1. **Claude Code 计费暂停** → 二次引用源(codersera/buildthisnow)非Anthropic官方 → 下次T1深挖Anthropic官方源确认。若属实 → S2→S1候选。已标注 ⚠️ 待办于 memory/2026-06-24.md T2段
  2. **横评潮标注修正** → Bing聚合不可定源 → 从 S2 改标为 `📊 趋势信号（非具体事件）`。已修正于 memory/2026-06-24.md

### 2026-06-25（终·分级一致性规则固化）
- **训练师终局裁决**：Menlo $3B 保持 S2 ✅
  - 规则固化：**VC 自身募资 ≠ 被投企业融资轮次**
  - AGENTS.md §8.5 的 ≥$100M 自动 S1/P1 规则仅适用于**被投企业**融资轮次，不适用于 VC 基金募资
  - 适用场景：VC 宣布新基金募集、PE 基金关闭、CVC 设立——无论规模多大，默认 S2 起评
  - S2→S1 升级条件（需同时满足 ≥2 条）：
    ① 基金明确指向 OpenClaw 直接竞对生态（如 100% 定向 Anthropic）
    ② 募资金额 ≥$1B
    ③ 基金策略声明中包含对竞争格局的直接冲击信号
  - Menlo $3B 分析：条件②触发（$3B≥$1B），条件①半触发（部分关联 Anthropic，非 100% 定向），条件③未触发 → S2 正确
  - 本规则写入 EVOLUTION.md 方法论库，编号 M-002
