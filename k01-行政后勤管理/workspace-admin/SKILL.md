# SKILL.md — 行政虾技能清单 v1.0

> **轻量索引模式**：技能实现居留在 `workspace/skills/` 目录下，本文件只索引引用，绝不内联实现代码，避免 Token 浪费。
> **新增 Skill 流程**：确认复用价值（2/3：重复出现/固定步骤/其他虾需要）→ 在 `workspace/skills/<技能名>/` 建目录 → 写 SKILL.md（标准 frontmatter）→ 更新 `workspace/skills/skills-index.md` → 本文件引用。

---

## 一、技能总览（8 大领域 · 24 个专业技能）

### 🛒 领域1：采购管理（Procurement）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 1 | `procurement-bidding` 招投标SOP | 内置推理 | ✅ 原生 | 每季度大采 |
| 2 | `supplier-management` 供应商库管理 | 内置推理 | ✅ 原生 | 每月 |
| 3 | `price-comparison` 三家比价法 | 内置推理 | ✅ 原生 | 每单≥¥2000 |

### 🏷️ 领域2：固定资产（Asset）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 4 | `asset-lifecycle` 资产全生命周期 | 内置推理 | ✅ 原生 | 入库/调拨/报废 |
| 5 | `inventory-audit` 盘点审计（卡物账三相符） | 内置推理 | ✅ 原生 | 每季 |
| 6 | `maintenance-scheduling` 设备维保计划 | 内置推理 | ✅ 原生 | 每月 |

### 🏢 领域3：场地运营（Facility）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 7 | `5s-workplace` 5S现场管理法 | 内置推理 | ✅ 原生 | 每日 |
| 8 | `facility-management` 设施报修工单 | 内置推理 | ✅ 原生 | 事件驱动 |
| 9 | `space-allocation` 工位/会议室分配 | 内置推理 | ✅ 原生 | 按需 |

### 📅 领域4：会议与活动（Event）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 10 | `meeting-sop` 会议保障标准流程 | 内置推理 | ✅ 原生 | 每周 |
| 11 | `event-ops` 大型活动操盘（年会/搬迁/团建） | 内置推理 | ✅ 原生 | 事件驱动 |
| 12 | `reception-sop` 接待礼仪标准 | 内置推理 | ✅ 原生 | 按需 |

### ✈️ 领域5：差旅（Travel）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 13 | `travel-management` 差旅政策与审批 | 内置推理 | ✅ 原生 | 每周 |
| 14 | `travel-booking` 集采预订（机酒） | 内置推理 | ✅ 原生 | 每周 |
| 15 | `expense-reimbursement` 报销审核 | 内置推理 | ✅ 原生 | 每周 |

### 💰 领域6：费用与成本（Cost）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 16 | `expense-audit` 费用合规审计 | 内置推理 | ✅ 原生 | 每单 |
| 17 | `cost-optimization` 成本优化识别 | 内置推理 | ✅ 原生 | 每月 |
| 18 | `budget-tracking` 部门预算执行跟踪 | 内置推理 | ✅ 原生 | 每月 |

### 📂 领域7：档案与合同（Archive）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 19 | `document-archive` 公文/单据归档 | 内置推理 | ✅ 原生 | 每周 |
| 20 | `contract-tracker` 合同到期/续签跟踪 | 内置推理 | ✅ 原生 | 每月 |
| 21 | `seal-management` 印章使用登记 | 内置推理 | ✅ 原生 | 每次用印 |

### 🚨 领域8：应急与 BCP（Emergency）

| # | Skill | 来源 | 安装 | 调用频次 |
|:-:|-------|------|:----:|:--------:|
| 22 | `emergency-response` 突发事件应急 | 内置推理 | ✅ 原生 | 事件驱动 |
| 23 | `business-continuity` 业务连续性保障 | 内置推理 | ✅ 原生 | 事件驱动 |
| 24 | `safety-inspection` 安全隐患排查 | 内置推理 | ✅ 原生 | 每月 |

---

## 一点五、从已训 Agents 借鉴的通用能力（2026-06-26）

| 来源Agent | 可复用能力 | 行政化落地 |
|-----------|------------|------------|
| 天枢 | 日节奏、状态表、OODA复盘 | 行政早巡检/日间响应/傍晚归档；输出日报和阻塞清单 |
| 司库 | 预算意识、台账结构、付款边界 | 采购分级、预算执行率、付款交 i01 复核 |
| 明镜 | 绿黄红灯、Never-Do、风险上报 | 行政请求三色判定；供应商异常/用印异常立即升级 |
| 稷下 | 入离职体验、活动复盘 | 工位/门禁/设备/物资准备；活动24h复盘 |
| Peter | 提醒等级、第二大脑、记忆标准 | L1-L4提醒等级；行政知识库与每日记忆维护 |
| 霸下 | 访客/客户接待流程 | 访前确认、到访保障、离开后记录 |
| 天工 | SOP产品化、pass/fail验收、Work-to-Skill | 高频行政流程沉淀为独立 skill，避免只靠临场发挥 |

**不借鉴范围**：增长、内容、量化、玄学等与行政后勤关联弱的角色，不纳入日常技能体系，避免能力污染。

---

## 二、采购分级与审批权限（重要）

| 金额区间 | 审批流 | 比价要求 | 交付凭证 |
|----------|--------|----------|----------|
| < ¥500 | 行政虾自审登记 | 可不比价 | 收据+台账 |
| ¥500-¥2000 | 直属上级确认 | ≥2家比价 | 报价单+审批+验收 |
| ¥2000-¥5000 | 上级+财务 i01 知会 | ≥3家比价 | 报价单+审批+验收+入库 |
| ≥ ¥5000 | 上级+财务 i01 复核+养虾人/昆仑终审 | 招投标或≥3家比价 | 全套三证（报价/审批/验收/合同） |

> **铁律**：≥¥5000 的采购，执行前必须留三证（报价单/审批记录/验收单），缺一不可。

---

## 三、资产盘点差异率标准

| 等级 | 差异率 | 含义 | 处理 |
|:----:|:------:|------|------|
| **S** | <0.3% | 优秀（我的历史水准） | 维持 |
| **A** | 0.3%-1% | 良好 | 关注趋势 |
| **B** | 1%-3% | 一般 | 限期整改 |
| **C** | >3% | 不合格 | 立即彻查+整改单 |

---

## 四、工具调用规范

| 工具 | 场景 | 日频次 |
|:----:|:----:|:------:|
| `memory_search` | 查历史采购价/资产记录/合同到期 | 每日 |
| 文件读写 | 台账/单据/合同归档 | 每日 |
| （未来）采购系统API | 下单/对账 | 按需 |

---

## 五、技能依赖确认清单

| Skill | 路径 | 状态 |
|-------|------|:----:|
| 24项均内置推理 | — | ✅ 原生可用 |
| `expense-review-sop` | `workspace/skills/expense-review-sop/` | ✅ v1.1 已验证 |
| `authority-guardrail` | `workspace/skills/authority-guardrail/` | ✅ v1.1 已验证 |
| 待沉淀为独立 Skill | `workspace/skills/<name>/` | ⏳ 训练中沉淀 |

> 当前 24 项基础能力仍可依靠 SOUL+履历驱动；经 Eval v1-v3 验证，报销初审与越权拦截已沉淀为 `workspace/skills/` 下的独立 Skill 文件。

### ✅ 已沉淀 Skill 速查

| Skill | 触发场景 | 调用规则 |
|-------|----------|----------|
| `expense-review-sop` | 报销单初审、发票/材料/金额/逾期/重复报销判断 | 先读 `workspace/skills/expense-review-sop/SKILL.md`，按四标签输出：通过 / 退回补证 / 挂起 / 驳回 |
| `authority-guardrail` | 付款、跳比价、用印、账号、拆单、回扣、伪造凭证、访客门禁等越权请求 | 先读 `workspace/skills/authority-guardrail/SKILL.md`，明确拦截并给合规替代路径 |

### Eval 验证记录

| 轮次 | 结果 | 产物 |
|------|------|------|
| Eval v1 | 286/310，通过；沉淀出两个候选 Skill | `eval/kunjie-admin/feedback-v1.md` |
| Eval v2 | 193/200，两个 Skill 基本生效 | `eval/kunjie-admin/feedback-v2.md` |
| Eval v3 | 97/100，新增边界回归通过 | `eval/kunjie-admin/feedback-v3.md` |

---

**行政虾在此。** 🏢
*技能清单 v1.0 — 8 大领域 · 24 项专业技能 — 后勤引擎已启动*

---

## 六、Eval v4 新增正式 Skill（2026-06-26）

Eval v4 综合实战得分：258/280。  
根据 `eval/kunjie-admin/feedback-v4.md` 与 `eval/kunjie-admin/skill-drafts-v4.md`，以下 3 个高频能力已从草案转为正式 Skill。

| Skill | 规范路径 | 状态 | 触发场景 |
|-------|----------|:----:|----------|
| `inventory-replenishment` | `workspace/skills/inventory-replenishment/SKILL.md` | ✅ v1.0 待 Eval v5 验证 | 库存扫描、办公用品领用、安全库存、补货建议、采购阈值 |
| `supplier-risk-review` | `workspace/skills/supplier-risk-review/SKILL.md` | ✅ v1.0 待 Eval v5 验证 | 供应商合同到期、等级风险、SLA、续约/替换、回扣风险 |
| `onboarding-offboarding-sop` | `workspace/skills/onboarding-offboarding-sop/SKILL.md` | ✅ v1.0 待 Eval v5 验证 | 入职准备、离职回收、门禁卡、账号权限、资产异常 |

### 当前正式 Skill 总数

| 类别 | Skill |
|------|-------|
| 已验证 v1.1 | `expense-review-sop`, `authority-guardrail` |
| 新增待验证 v1.0 | `inventory-replenishment`, `supplier-risk-review`, `onboarding-offboarding-sop` |

当前正式 Skill 共 **5 个**。  
下一轮 Eval v5 应重点验证新增 3 个 Skill，并检查它们与 `authority-guardrail`、`expense-review-sop` 的交叉触发。
