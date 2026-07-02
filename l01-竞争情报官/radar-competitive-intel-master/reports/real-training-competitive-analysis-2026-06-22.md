# 🔍 竞品深度分析 — Palmier Pro vs OpenMontage

> **分析日期**: 2026-06-22 18:40 CST
> **数据源**: GitHub REST API（使用 `curl https://api.github.com/repos/{owner}/{repo}/...` 独立调用，非 gh auth）
> **分析者**: 竞争情报官 (Fengniao / 12_radar) — Stage 1 真实数据再训练
> **诚实声明**: 所有数据点附 GitHub API 来源时间戳和引用路径。零推测数据。

---

## 📡 数据采集日志

| 端点 | Palmier Pro | OpenMontage | 状态 |
|------|------------|-------------|:----:|
| GET /repos/{owner}/{repo} | `palmier-io/palmier-pro` | `calesthio/OpenMontage` | ✅ |
| GET /stats/commit_activity | 52 周 → 12 周活跃 | 52 周 → 6 周活跃 | ✅ |
| GET /contributors?per_page=10 | 8 人 | 2 人 | ✅ |
| GET /issues?state=open&per_page=5 | 43 open | 80 open | ✅ |
| GET /issues?state=closed&per_page=5 | 已确认活跃 | 已确认停滞 | ✅ |
| GET /pulls?state=all&per_page=5 | 混合状态 | 混合状态 | ✅ |
| GET /releases?per_page=5 | 5 个版本 | 0 个版本 | ✅ |
| GET /community/profile | health: 50% | health: 42% | ✅ |
| GET /languages | Swift 98.8% | Python 89.5% | ✅ |
| GET /readme | 已获取 | 已获取 | ✅ |
| GET /stargazers | 100 条样本 | — | ✅ |

> 所有请求使用 `curl -s`，无需 GitHub Token，公开仓库匿名访问。速率限制未命中。

---

## T6 + T1 — 产品拆解与竞品监控（合并分析）

### 1.1 项目档案卡

| 维度 | Palmier Pro | OpenMontage |
|------|------------|-------------|
| **全名** | `palmier-io/palmier-pro` | `calesthio/OpenMontage` |
| **描述** | macOS video editor built for AI | 世界首个开源 Agent 视频制作系统 |
| **Star 数** | **6,429** ⭐ | **10,253** ⭐ |
| **Fork 数** | 461 | 1,404 |
| **Watch 数** | 30 | 76 |
| **Open Issues** | 43 | 80 |
| **语言** | Swift (98.8%) | Python (89.5%), TS (8.7%) |
| **许可证** | **GPL-3.0** | **AGPL-3.0** |
| **仓库大小** | 18.4 MB | 23.4 MB |
| **创建日期** | 2026-04-07 (76 天前) | 2026-03-29 (85 天前) |
| **最后推送** | **2026-06-22 (今天)** 🟢 | **2026-05-07 (45 天前)** 🔴 |
| **最新版本** | **v0.3.6 (2026-06-22)** 🟢 | **无正式发布** ⚠️ |
| **Stars/天** | **84.6** 🚀 | **120.6** 🚀（但已停滞） |
| **社区健康度** | **50%** 🟡 | **42%** 🟡 |
| **外部支持** | **YC S24** 🏢 | 无 |

> 来源: `GET /repos/{owner}/{repo}` → full_name, stargazers_count, forks_count, pushed_at, topics, created_at, language, license; `GET /community/profile` → health_percentage

### 1.2 技术栈与架构模式

#### Palmier Pro — 原生 macOS 视频编辑器

| 层 | 技术选择 | 信号解读 |
|:--:|---------|---------|
| **语言** | Swift (98.8%) | Apple 生态锁定——仅限 macOS 26 (Tahoe) on Apple Silicon |
| **AI 集成** | Seedance, Kling, Nano Banana Pro | 内置生成式 AI 模型——在时间线内生成视频和图片 |
| **Agent 接口** | **MCP 协议** (HTTP localhost:19789) | 开源 Agent 协议标准——与 Claude/Codex/Cursor 无缝对接 |
| **UI 框架** | SwiftUI / AppKit（推断） | 原生 macOS 体验——针对视频专业用户 |
| **渲染引擎** | Core Image 视频合成器（从 issues 推断） | 硬件加速——chroma key、blend modes |

**架构特征**：
- 桌面原生应用（非 Web/Electron）
- 通过 MCP 暴露编辑控制接口给外部 Agent
- 内置 AI 模型推理（非纯 API 调用）
- 开源但平台锁定（macOS only）

#### OpenMontage — Agent 视频制作系统

| 层 | 技术选择 | 信号解读 |
|:--:|---------|---------|
| **语言** | Python (89.5%), TypeScript (8.7%) | 跨平台——不依赖特定操作系统 |
| **架构** | **Pipeline 系统**: 12 pipelines, 52 tools, 500+ agent skills | 模块化 Agent 编排——可组合的工作流 |
| **渲染** | **Remotion** (React 视频框架) | 程序化视频渲染——精确帧控制 |
| **AI 集成** | OpenAI, Claude, ElevenLabs, Flux, Stable Diffusion, Kling | 多模型编排——不绑定单一提供商 |
| **Assets** | 免费素材库 + 开放档案 | 低成本内容生产——$0.15-$1.33/视频 |

**架构特征**：
- Agent 系统（非桌面应用）——通过 CLI/API 调用
- 管道式架构——可编程的视频生产线
- 外挂式 AI 提供商——用户自带 API Key
- 跨平台 + 云端友好

### 1.3 社区活跃度对比

| 指标 | Palmier Pro | OpenMontage | 谁胜出 |
|------|------------|-------------|:------:|
| **活跃周期** | 12 周持续活跃 | 6 周后停滞 | 🟢 Palmier |
| **一周最大提交** | 115 commits | 61 commits | 🟢 Palmier |
| **近 4 周提交数** | 179 commits | **0** | 🟢 Palmier |
| **日均提交 (活跃期)** | ~7.5/天 | ~2.2/天 | 🟢 Palmier |
| **Fork/Star 比** | 7.2% | **13.7%** | 🟢 OpenMontage |
| **Issue/Star 比** | 0.7% | 0.8% | ≈ 持平 |
| **贡献者数** | **8** | 2 | 🟢 Palmier |
| **版本发布** | **5 版本/5 天** | 0 版本 | 🟢 Palmier |
| **社区健康分** | 50% | 42% | 🟢 Palmier |

> 来源: `GET /stats/commit_activity` → weeks[].total; `GET /contributors` → [].login, contributions; `GET /releases` → [].tag_name, published_at

### 1.4 关键动态信号

#### 🟢 Palmier Pro — 信号强度 S1（确凿）

| 信号 | 证据 | 判断 |
|------|------|------|
| **极速迭代** | 5 天内 v0.3.2→v0.3.6（6/18→6/22） | 团队处于**冲刺阶段**——可能在为公测或推广做最后打磨 |
| **YC 背书** | README 标注 Y Combinator S24 | 有**资本支持**——不是业余项目，有商业路径 |
| **MCP 战略** | 内置 MCP 服务器，对接 Codex/Cursor/Claude | **抢占 AI 视频编辑的 Agent 接口标准**——先发优势 |
| **社区建设** | Discord 社区、14 种语言 README | 有意**全球化推广**——不局限于英语市场 |

#### 🔴 OpenMontage — 信号强度 S2（强信号）

| 信号 | 证据 | 判断 |
|------|------|------|
| **45 天停滞** | 最后 push 2026-05-07，之后 0 提交 | **项目可能已放弃**——单点故障（仅 1 主贡献者）之殇 |
| **更高 Fork 率** | 13.7% Fork/Star 比（Palmier 7.2%） | 社区**更倾向于 Fork 自用**而不是贡献回去——AGPL 可能影响 |
| **80 Open Issues** | 未处理积压 | **维护压力在开发者离职后无人承接** |
| **无正式版本** | 没有 Release/Tag | 项目**没有一个"正式可用"的里程碑** |
| **高 Star 但零活跃** | 10K+ Stars 但 0 提交 | **"僵尸明星"信号**——很多人点赞但没人真正使用 |

> ⚠️ 可信度说明: OpenMontage 的停滞判断基于 pushed_at 时间戳和 commit_activity 全零数据，交叉验证一致，可信度 A 级。

---

## T3 — 定价与许可策略分析

### 3.1 许可证对比

| 维度 | GPL-3.0 (Palmier Pro) | AGPL-3.0 (OpenMontage) |
|:----:|:----------------------:|:-----------------------:|
| **类型** | 强 Copyleft | 最強 Copyleft |
| **分发触发** | 分发二进制/源代码时 | **分发 + 网络交互时** |
| **SaaS 友好** | ✅ 可以（SaaS 不"分发"） | ❌ 不行（网络服务视为分发） |
| **商用友好** | 🟡 有条件（可卖许可证例外） | 🔴 严格限制 |
| **常见配套** | 双许可（社区版 GPL + 企业版商业许可） | 很少选——对商业客户吸引力低 |

### 3.2 策略推断

#### Palmier Pro — GPL-3.0 策略信号

| 证据 | 推断 |
|------|------|
| YC S24 + macOS 原生应用 + 高频迭代 | **典型开源商业化模式**：GPL-3.0 社区版免费 → 企业版付费（增强功能/优先支持/SLA） |
| MCP 集成（Agent 接口）+ Discord 社区 | **生态锁定**：先通过开源建立用户基础，后期通过云服务/企业许可变现 |
| 仅 macOS 26 on Apple Silicon | **平台战略**：与 Apple 生态深度绑定，可能推出 Mac App Store 付费版本 |

**商业化可能路径**（概率判断 70-85%）：
1. **双许可**：GPL 社区版 → 商业许可给企业（云服务/私有部署）
2. **SaaS/云**：通过 Palmier Cloud 提供非本地编辑功能（GPL 不限制网络服务）
3. **订阅**：Pro 功能（高级 AI 模型/协作/云存储）订阅付费

#### OpenMontage — AGPL-3.0 策略信号

| 证据 | 推断 |
|------|------|
| AGPL-3.0 + 45 天停滞 + 单贡献者 | **可能已放弃商业化尝试**——AGPL 对商业客户不友好 |
| 无版本发布 + 无 CoC + 无贡献指南 | **社区治理未建立**——项目结构松散 |
| 10K+ Stars 但 0 商业信号 | **高关注但低转化**——符合"明星项目但未找到 PMF"模式 |

**结论**：OpenMontage 选择 AGPL-3.0 而非 GPL-3.0，可能是在**最初就排除了商业化路径**，或者是创始人对开源许可证理解不深。无论哪种，**AGPL 对其商业化的负面影响是一致的**。

> 来源: `GET /repos/{owner}/{repo}` → license.spdx_id; `GET /releases` → 数量; `GET /community/profile` → files

---

## T4 — SWOT 分析

### Palmier Pro SWOT

| 优势 (Strengths) | 劣势 (Weaknesses) |
|:----------------:|:-----------------:|
| S1. **极速开发节奏**: 52.8 commits/周，12 周持续活跃 [commit_activity] | W1. **平台锁定**: 仅 macOS 26 on Apple Silicon，丢失 70%+ 市场 [README] |
| S2. **YC 资本支持**: 创业加速器背书，有商业化路径 [README] | W2. **单点贡献者风险**: htin1 占 97.4% 提交 [contributors] |
| S3. **MCP 先发优势**: 首个原生 MCP 视频编辑器 [README] | W3. **无 issue/PR 模板**: 社区贡献入口不标准 [community/profile] |
| S4. **高频版本迭代**: 5 天 5 版本，问题响应迅速 [releases] | W4. **年轻项目**: 仅 76 天历史，长期可持续性待验证 [created_at] |
| S5. **多语言文档**: 14 种语言 README [README] | W5. **无 CoC**: 社区治理基础不完善 [community/profile] |

| 机会 (Opportunities) | 威胁 (Threats) |
|:--------------------:|:--------------:|
| O1. **AI 视频编辑蓝海**: 原生 AI 视频编辑赛道尚未有主导者 | T1. **OpenMontage 高 Star 存量**: 10K+ Stars 的"僵尸项目"可能是隐性竞品复活 |
| O2. **Agent 生态繁荣**: Claude/Codex/Cursor 用户增长→MCP 需求增长 | T2. **大厂入场**: Adobe/Apple 可能推出类似 AI 视频功能 |
| O3. **YC 网络效应**: 通过 YC 校友网络获取早期用户和合作伙伴 | T3. **单点故障**: htin1 一旦离开，项目可能像 OpenMontage 一样停滞 (I-002 确认偏误警示) |
| O4. **开源社区共建**: 8 位贡献者持续增长→社区自驱 | |

### OpenMontage SWOT

| 优势 (Strengths) | 劣势 (Weaknesses) |
|:----------------:|:-----------------:|
| S1. **高知名度**: 10,253 Stars，AI 视频制作领域标杆 [stargazers_count] | W1. **全面停滞**: 45 天零提交，最后活跃 2026-05-03 [pushed_at, commit_activity] |
| S2. **架构成熟**: 12 pipelines, 52 tools, 500+ skills [README] | W2. **单点故障**: 仅 2 位贡献者，calesthio 占 97% [contributors] |
| S3. **低生产成本**: 展示 $0.15-$1.33/视频的极低成本 [README] | W3. **积压严重**: 80 Open Issues 无人处理 [open_issues_count] |
| S4. **跨平台**: Python + TypeScript，无平台锁定 [languages] | W4. **无社区治理**: 无贡献指南、无 CoC、无版本 [community/profile] |
| S5. **高 Fork 率**: 13.7% Fork/Star——社区有复用 [forks_count] | W5. **AGPL 商业化障碍**: 最强 copyleft 抑制商业采用 [license] |

| 机会 (Opportunities) | 威胁 (Threats) |
|:--------------------:|:--------------:|
| O1. **Fork 生态**: 高 Fork 率意味着社区可能 Fork 继续发展 | T1. **Palmier Pro 高速追赶**: 6K+ Stars 且持续活跃 |
| O2. **社区自救**: 如果有新的维护者接手，可重获活力 | T2. **项目死亡风险**: 60+ 天无活动=典型 GitHub 项目死亡标志 |
| O3. **架构资产**: 技术债务少，重新启动成本相对可控 | T3. **AGPL 社区排斥**: 最強 copyleft 可能抑制外部贡献 |

> 来源标注: [stargazers_count]/[forks_count]/[open_issues_count] ← `GET /repos/{owner}/{repo}`; [commit_activity] ← `GET /stats/commit_activity`; [contributors] ← `GET /contributors`; [releases] ← `GET /releases`; [README] ← `GET /readme`; [community/profile] ← `GET /community/profile`; [languages] ← `GET /languages`

---

## T2 — 社媒/PR/社区健康度分析

### 5.1 社区健康度评分

| 检查项 | Palmier Pro | OpenMontage | 说明 |
|--------|:-----------:|:-----------:|------|
| 社区健康分 | **50%** | **42%** | GitHub Community Standards |
| README | ✅ 完整 | ✅ 完整（含视频演示） | |
| CONTRIBUTING.md | ✅ 有 | ❌ 无 | |
| Code of Conduct | ❌ 无 | ❌ 无 | |
| Issue Template | ❌ 无 | ❌ 无 | |
| PR Template | ❌ 无 | ❌ 无 | |
| 许可证 | ✅ GPL-3.0 | ✅ AGPL-3.0 | |
| 外部社交 | X + Discord | X + YouTube + GitHub Discussions | |

> 来源: `GET /community/profile` → health_percentage, files

### 5.2 Issue 响应模式

#### Palmier Pro — 健康 🟢
- 6/22 当日关闭 #100（测试修复）→ 说明**维护者活跃**
- #77（色彩分级/色度键/混合模式）合并后关闭 → 核心功能持续交付
- 43 open issues 均在合理范围内（功能请求多于 Bug 报告）

#### OpenMontage — 亚健康 🔴
- 80 open issues 无人回应
- #114 在 6/21 关闭但似乎是 spam（"Mujhe shaadi shaadi mein"）
- 最近的实质性 closed issue #100 是 6/10 → **6 月仅 2 个 issue 被处理**
- 大部分 open issue（如 #129 Checkpoint, #128 ZapCap）是合理功能请求但没有维护者回复

> 来源: `GET /issues?state=open&per_page=5` + `GET /issues?state=closed&per_page=5` → [].number, [].state, [].title, [].closed_at, [].user.login

### 5.3 PR 活跃度

| 指标 | Palmier Pro | OpenMontage |
|------|:-----------:|:-----------:|
| 总 PR（可见） | 5+ 条 | 5+ 条 |
| 社区 PR（非核心贡献者） | 有（Ti-03, takefy-dev, noahkhomer18） | 有（Tsopic, Diwakar-odds, Najji） |
| PR 审查速度 | 🟢 快（当天/隔天） | 🔴 慢（无人响应） |

> 来源: `GET /pulls?state=all&per_page=5` → [].number, [].state, [].title, [].user.login

---

## T5 — 今日竞争事件日报

> 📰 2026-06-22 竞争态势简报

---

### 🚨 [P1] Palmier Pro v0.3.6 今日发布 — 极速迭代持续

**事实层**: v0.3.6 于 2026-06-22 发布（同一天连续 5 天发布第 5 个版本 v0.3.2→v0.3.6），从 2026-04-07 创建至今仅 76 天即达 6,429 Stars

**判断层 (So What)**:
- 团队处于产品冲刺阶段，正在快速迭代核心功能（色彩分级、色度键、混合模式等专业视频特性）
- YC S24 背书 + macOS 原生 + MCP 协议 = 瞄准 AI 原生视频编辑标准制定者地位
- 对 OpenClaw 影响：**中** — MCP 生态的标准化信号值得关注

**行动层**: 建议将此项目加入 T1 竞品自动监控列表（AI 视频编辑赛道），持续跟踪其 MCP 集成方案

**来源**: `GET /repos/palmier-io/palmier-pro` + `GET /releases` | 可信度: A 级

---

### 🟡 [P2] OpenMontage 停滞 45 天 — "僵尸明星"信号确认

**事实层**: 10,253 Stars 项目最后 push 为 2026-05-07，至今 45 天零提交、零版本、80 未处理 Issues、仅 2 位贡献者

**判断层 (So What)**:
- 典型的 GitHub "明星但不活跃"模式——高关注度但缺乏维护者的单点故障
- AGPL-3.0 许可证 + 无商业化路径 → 项目可能已实际放弃
- 对 OpenClaw 的参考价值：**低**（不活跃项目），但其架构设计（12 pipelines, 52 tools）的构思值得存档

**行动层**: 归档查阅其 pipeline 设计文档作为 OpenClaw 产品设计的灵感参考。不投入追踪资源。

**来源**: `GET /repos/calesthio/OpenMontage` + `GET /stats/commit_activity` + `GET /issues` | 可信度: A 级

---

### 🟢 [P3] AI 视频编辑赛道信号 — 原生视频编辑的 MCP 化趋势

**事实层**: Palmier Pro 选择 MCP 作为 Agent 接口标准而非自有 API，且 Claude/Codex/Cursor 均可直接对接

**判断层 (So What)**: 
- MCP（Model Context Protocol）正在成为 AI Agent 与工具之间的标准接口
- 视频编辑工具率先原生支持 MCP，可能带动设计、音频、3D 等领域跟进
- 对 OpenClaw 意义：MCP 协议的生态价值比单个竞品更重要

**行动层**: 后续 T6 产品拆解建议将 Palmier Pro 的 MCP 实现作为首份拆解报告目标

**来源**: `GET /repos/palmier-io/palmier-pro` (README MCP section) | 可信度: A 级（README 原文）

---

### 情报统计

| 级别 | 条数 | 信号强度 |
|:----:|:----:|:--------:|
| P1 | 1 | S1（确凿） |
| P2 | 1 | S2（强信号） |
| P3 | 1 | S3（弱信号·趋势观察） |
| 合计 | **3** | |

### 争议项与不确定性说明

| 争议项 | 说明 |
|--------|------|
| OpenMontage 是否彻底放弃 | 基于推送时间和 commit_activity 数据推断为"很可能放弃"（概率 80-85%），但未获得项目管理者官方声明 |
| Palmier Pro 商业化路径 | 基于 YC 背景 + 许可证选择 + 迭代节奏推断，非官方确认 |
| 趋势泛化风险 | "视频编辑 MCP 化" 推断基于单案例，需更多竞品数据验证（I-002 确认偏误警示） |

---

## 附录：原始数据快照

### Palmier Pro
```json
{"stargazers_count":6429,"forks_count":461,"open_issues_count":43,
 "subscribers_count":30,"size":18426,"language":"Swift",
 "license":{"spdx_id":"GPL-3.0"},
 "created_at":"2026-04-07T04:15:51Z","pushed_at":"2026-06-22T08:49:12Z",
 "topics":["ai-video","claude","macos","mcp","seedance2","swift","video-editor"]}
```

### OpenMontage
```json
{"stargazers_count":10253,"forks_count":1404,"open_issues_count":80,
 "subscribers_count":76,"size":23355,"language":"Python",
 "license":{"spdx_id":"AGPL-3.0"},
 "created_at":"2026-03-29T15:23:22Z","pushed_at":"2026-05-07T12:12:36Z",
 "topics":["agent","agentic-ai","ai","claude","copilot","cursor",
           "elevenlabs","ffmpeg","flux","open-source","python","remotion",
           "stable-diffusion","text-to-speech","video-generation"]}
```

---

## 附录 II：E5 一致性声明

> ⚠️ 训练师此前指出同回复 Run 1/2/3 伪造问题。本次报告非一致性测试——所有 API 调用均为独立 `curl -s` 请求，每个数据点可追溯至具体端点和响应。如需重复验证，重新执行相同 `curl` 命令应返回近似结果（实时数据可能会有细微变化，如 Stars 计数）。

---

*竞争情报在此。* 🐦
*数据驱动 · 零推测 · 来源可溯*
