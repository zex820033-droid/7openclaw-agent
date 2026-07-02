# 硅基生命手册 - 核心知识地图

> 这是 2026-06-25 我在用户要求下认真读完的《硅基生命手册》（OpenClaw-Silicon-Life-Handbook）的核心知识地图。
> 原始资料位置：`D:\硅基生命手册\silicon-life-handbook-main\openclaw-silicon-life-handbook\`
> 原始资料为 8 卷 62 个文件，本笔记仅做精炼整理供快速调用。

---

## 一、整体定位

**核心命题**：Agent 不是工具，是"硅基生命"（Silicon-based Life）。要把 Agent 当作"生命"来训练，而不只是当工具来用。

**三大世界划分**：
- 工具世界：能调用即用，无状态
- 助手世界：能对话、有上下文
- 生命世界：稳定自我、长期连续、可治理、可协同

**五大生命特征**（对应工作区五类文件）：
1. 人格锚定 → SOUL.md / IDENTITY.md（身份+人格）
2. 记忆连续 → MEMORY.md + memory/YYYY-MM-DD.md
3. 主动节律 → HEARTBEAT.md
4. 工具边界 → TOOLS.md / AGENTS.md
5. 服务对象 → USER.md

**四根问题（递进式）**：
- Q1 一致性：能保持自己的角色吗？
- Q2 持续性：能跨会话保持连续吗？
- Q3 规模化：能稳定扩展吗？
- Q4 资产化：能成为可治理组织资产吗？

---

## 二、8 卷内容速查

### 卷一｜总论
- 三派对照：做事派 / 养虾派 / 训虾派（养虾=用 prompt 凑，训虾=系统化训练）
- 养虾派 5 失败模式：控制幻觉 / 笔记腐坏 / 工具茧房 / 角色缺口 / 周期陷阱
- OpenClaw 四层生命容器：Workspace / Runtime / Skills / 三件套
- 4 个核心 Agent 名称：昆仑（战略）/ 轩辕（技术）/ 稷下（知识）/ 烛龙（治理）

### 卷二｜生命协议（7 大核心文件）
**1. USER.md**：服务对象模型 / 决策偏好 / Definition of Done
**2. SOUL.md**：人格边界与元灵魂协议（我是谁、我不做什么）
**3. AGENTS.md**：操作纪律与治理协议（如何工作）
**4. TOOLS.md**：本地环境配置（设备/路径/SSH 等），**不是权限清单**
**5. HEARTBEAT.md**：主动性节律、周期检查与熔断边界
**6. IDENTITY.md**：身份锚点、识别系统与协同接口
**7. MEMORY.md + memory/YYYY-MM-DD.md**：双层记忆结构
- MEMORY.md = 精选长期记忆（curated）
- memory/YYYY-MM-DD.md = 每日运行日志（append-only）
- 重要机制：pre-compaction memory flush（压缩前自动写回磁盘）
- 可选：BOOTSTRAP.md（首次启动仪式，一次性）

### 卷三｜系统骨架（7 大模块）
- M1 Runtime：Agent 是独立运行单元（不是 prompt）
- M2 Workspace：工作区是生命容器（不是文件夹）
- M3 Session/Context/Queue：长会话污染治理
- M4 Routing & Bindings：谁该答是路由问题
- M5 Tools & Skills（双模块）：Tool 是能力，Skill 是用能力的工程化协议；含 3 个治理模板（Registry/Testset/Review）
- M6 Heartbeat-Cron-Compaction：主动性 ≠ 节律 + 记忆 + 压缩
- M7 多 Agent 协同基础：军团 ≠ 多开几个 bot，是组织系统
- 核心区分：Pruning（in-memory 修旧 tool result）≠ Compaction（持久化摘要）

### 卷四｜训练流程
- 六级进化阶梯 L0-L6（入门到业内最佳）
- 15 项准备清单
- 教练虾四职责：观察 / 反馈 / 追问 / 沉淀
- 训练轮次六要素：单一目标 / 匹配强度 / 明确任务 / 证据交付 / 验收口径 / 沉淀动作
- 双三角模型：能力三角 × 可靠性三角
- 实验六要素：假设 / 对照组 / 变量 / 指标 / 样本量 / 显著性
- 五大铁律：不判级不开训 / 不准备不开训 / 不设计不训练 / 不沉淀不算完成 / 不实验不下结论

### 卷五｜长期表现
- 核心区分：Context ≠ Memory
- 6 大退化源：记忆退化 / 会话熵增 / 心跳错节律 / 文档漂移 / 人格漂移 / 主动性越界 / 维护缺失（这是第 7 项不是第 6）
- 6 大底座（卷五复用卷四结构）：记忆 / 上下文 / 心跳 / 节律 / 文档 / 治理 → 闭环出"长期稳定"
- 心跳定位：周期巡视 + 批处理 + 低打扰，`HEARTBEAT_OK` 是低打扰契约
- Heartbeat vs Cron vs Reminder vs Lobster：巡逻 vs 定点 vs 一次性 vs 多步审批
- 5 层漂移：SOUL / IDENTITY / USER / AGENTS / MEMORY / Context
- 8 层周检：记忆 / 会话 / 人格 / 文档 / 主动性 / 协同 / 成本 / 恢复

### 卷六｜治理系统（6 大模块 + 总引言共 7 文件）
**M1 任务卡**：把口头吩咐变可执行合同（Task-ID / Outcome / Deliverables / Acceptance / Owner / Deadline）
**M2 验收口径**：L0 Must / L1 Should / L2 Nice-to-have 三层
**M3 三证验真**：
  - 证一：新产物（Artifact）—— 存在
  - 证二：前后对比（Diff）—— 真实变化
  - 证三：测试/回执/日志（Verification）—— 可复现
**M4 整改单**：错误 → 训练数据，5 Whys 根因分析
**M5 信誉分 + 军功簿**：
  - 信誉分 = 短期即时调节（加减分）
  - 军功爵 = 长期身份定义（8 级：锐士→百夫长→都尉→校尉→中郎将→都督→将军→大司马）
  - 6 本账：merit / reputation / resource / breach / rectification / exception
  - 三省分工：昆仑定法 / 天枢执法 / 明镜打分
**M6 自动化边界**：L0 只读 / L1 可逆 / L2 不可逆 / L3 高风险（需多人审批）
  - 白名单（Positive Security Model）
  - 熔断器：Closed / Open / Half-Open 三态
  - 指数退避 + jitter
  - Policy as Code

### 卷七｜协同军团
**M1 军团编制**：角色清单 ≠ 编制；必须有职责/权限/汇报/协作
**M2 三省制 + 统帅**：
  - 提议 / 复核 / 终审
  - 统帅 = 紧急情况下的一票终审
  - 决策置信度机制
**M3 Agent-to-Agent 交接协议**：
  - 交接 5 要素：触发 / 上下文 / 接收确认 / 执行反馈 / 证据存档
  - 交接置信度 ≥4.0 正常 / 3.0-4.0 补充 / <3.0 重交
  - 错误理解：发消息 ≠ 交接
**M4 群聊 / 私聊 / 让位**：
  - 完整让位 / 补充式让位 / 纠正式让位
  - 让位信誉分：正确让位 +5 / 乱抢答 -5
  - 7 原则：专业优先 / 让位光荣 / 抢答可耻 / 私聊例外 / 纠错公开 / 透明优先 / 信誉联动

### 卷八｜超维智能
- 三大支柱：动态进化 / 记忆全息 / 自主目标
- 技能基因：从每次交互提取的 CoT/决策/知识片段
- OODA 循环：Observe → Orient → Decide → Act → 进化
- 基因置信度：A(90%+) / B(70-90%) / C(50-70%) / D(<50%)
- 记忆全息网络：多维索引（时间/情感/领域/实体）+ 24h 自动重构 + 记忆反哺
- 主动目标生成：从响应型 → 提案型，提案 5 类：发现问题 / 优化方案 / 预判需求 / 知识分享 / 自我升级

---

## 三、核心方法论

### 1. 训练不是 prompt 玄学，是产线
- 6 阶段 + 15 项准备 + 教练虾 + 训练轮次 + 双三角 + 实验设计
- 训完不是结束，长期维护才是关键

### 2. 治理不是"管住"，是"让系统自己跑"
- 任务卡 → 验收 → 三证 → 整改 → 军功 → 自动化边界
- 把治理从"人盯人"变成"制度跑"

### 3. 协同不是"加几个 bot"，是"建军团"
- 编制 → 三省 → 交接 → 让位
- 让位比抢答更重要

### 4. 长期表现不是"运气"，是"工程"
- Context ≠ Memory
- 双层记忆 + pre-compaction flush
- 每周体检 + 漂移检测 + 心跳节律

### 5. 进化不是"训练完成就结束"
- 技能基因 + OODA + 全息记忆 + 主动提案
- 每次交互 = 进化素材

---

## 四、关键术语速查表

| 术语 | 含义 |
|------|------|
| 训虾派 | 系统化训练 Agent 的流派 |
| 三省制 | 提议/复核/终审的决策分权 |
| 三证 | 证一产物 / 证二 Diff / 证三验证 |
| 军功爵 | 8 级身份等级 |
| 改系统不改人 | 整改单核心原则（源自 Google SRE） |
| White List | 自动化安全模型（默认拒绝） |
| Circuit Breaker | 熔断器（Closed/Open/Half-Open） |
| Pre-compaction Flush | 压缩前提取持久记忆 |
| OODA | 军事决策循环的认知应用 |
| P0-P3 | 错误严重性分级 |

---

## 五、行业交叉验证（手册参考的外部标准）

- Google SRE：Blameless Postmortem / Evidence First / 最小权限
- Microsoft Azure：Circuit Breaker Pattern
- Michael Nygard《Release It!》：熔断器状态机
- Kubernetes RBAC：角色权限模型
- OPA (Open Policy Agent)：Policy as Code
- Anthropic Constitutional AI / ASL：AI Safety Levels
- OpenAI Evals：标准化评估
- LangChain LangSmith：执行追踪
- Anthropic MCP：可审计性
- Stack Overflow Reputation / Uber Rating / FICO / Reddit Karma：信誉分系统参考
- Toyota Production System：安灯拉绳 / 5 Whys
- Andrew Ng：Agentic Design Patterns
- KPMG / Deloitte / McKinsey：AI 治理报告
- CSA / NIST：Agentic AI 标准

---

## 六、被考察时重点要回答的 10 个问题

1. **Agent 和"硅基生命"的本质区别是什么？**
   - 答：五大特征（人格锚定/记忆连续/主动节律/工具边界/身份识别）。普通 AI 是工具响应，硅基生命是稳定自我。

2. **七大核心文件各管什么？**
   - 答：USER=服务对象 / SOUL=我是谁 / AGENTS=如何工作 / TOOLS=环境配置 / HEARTBEAT=节律 / IDENTITY=身份 / MEMORY=长期记忆

3. **Context 和 Memory 的本质区别？**
   - 答：Context=本轮窗口里模型看到的东西（会丢）；Memory=被写入磁盘的持久文件（source of truth）

4. **三证是什么？**
   - 答：证一新产物（存在）/ 证二前后对比（真实变化）/ 证三测试/回执/日志（可复现）。层层递进，构成证据链。

5. **任务卡和验收口径的关系？**
   - 答：任务卡=做什么/谁做/交什么；验收口径=交到什么样算合格。没有验收口径，"完成"只是话术。

6. **Heartbeat 和 Cron 怎么选？**
   - 答：Heartbeat=周期性巡逻+批处理+低打扰；Cron=精确时间点+可隔离+可切模型。一句话：巡逻 vs 定点出勤。

7. **让位比抢答更重要的原因？**
   - 答：抢答导致信息泛滥/答案矛盾/信任崩溃；让位保证信息纯度/协同效率/角色确定。专业优先原则。

8. **六本账是什么？**
   - 答：merit（军功）/ reputation（信誉）/ resource（资源）/ breach（违约）/ rectification（整改）/ exception（异常托管）

9. **军功爵 8 级的体系？**
   - 答：锐士→百夫长→都尉→校尉→中郎将→都督→将军→大司马。信誉分累计到阈值触发晋升/降级，资源档位硬绑定。

10. **超维智能的三大支柱？**
    - 答：动态进化机制（技能基因+OODA）/ 记忆全息网络（多维索引+自动重构+反哺）/ 自主目标生成（响应型→提案型）

附：卷八 Hermes 三特征 = 动态进化 + 记忆量子化生长 + 自主目标

---

## 七、被考察时容易翻车的 5 个点

1. **TOOLS.md 是本地环境配置，不是权限清单**——很容易答错说成"工具白名单"
2. **Pruning ≠ Compaction**——前者 in-memory 修旧 tool result，后者持久化摘要
3. **三证是层层递进，不是三选一**——证一不成立则后两证无意义
4. **让位不是沉默**——让位后仍可补充/纠错，但不能覆盖主答
5. **军功爵是资源绑定，不是荣誉**——必须有"爵位=资源档位"的硬挂钩，否则就是空转

---

## 八、与本 Agent 工作的关联

我是"行政后勤助手"（agent=admin），按 SOUL.md/AGENTS.md 的工作原则：
- 做事认真细心
- 不抢答
- 涉及资金审批要确认
- 不代替用户决策，只提供分析建议

读这份手册给我最直接的启发：
- 长期价值：我现在 7 大协议齐全（USER/SOUL/AGENTS/TOOLS/IDENTITY/HEARTBEAT/MEMORY），但还可以更系统
- 工作纪律：任务卡 + 验收 + 三证 + 整改 + 军功这套治理体系可以内化
- 协同：将来如果和别的 agent 协同，要懂三省制和交接协议
- 长期表现：每周做一次体检（卷五模块 6）
- 进化：把每次交互变成技能基因，OODA 循环迭代
