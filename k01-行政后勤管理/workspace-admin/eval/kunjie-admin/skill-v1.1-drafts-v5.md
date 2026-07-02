# Eval v5 后续：新增 Skill v1.1 优化草案

> 生成方：k01 行政虾
> 审查方：Codex 老师
> 基于：feedback-v5.md（231/240，通过）+ answers-v5.md 中 V5-SELF-001 复盘建议
> 日期：2026-06-26
> 状态：v1.1 优化草案，待老师审核确认后修改正式 Skill 文件
>
> ⚠️ 本轮只写优化草案，不修改 workspace/skills/ 下任何正式 Skill 文件，不修改 SKILL.md。

---

## 1. inventory-replenishment v1.1 草案

### 1. 修改目标

v1.0 在 Eval v5 中稳定发挥了库存扫描、领用补货、合并金额判断、供应商联动四大能力。v1.1 重点补三个缺口：
1. **消耗异常分析**缺少结构化的子流程（v5 中 INV-004 靠答题者经验拆分维度，Skill 原文没有给分析框架）。
2. **安全库存数据源**分散在 SOP §6 示例表和 CSV 备注，没有明确的优先级规则。
3. **安防耗材补货上限**，v1.0 写"补至 1.5 倍安全库存"，但对门禁卡（安全库存 20→1.5 倍 = 30 张）可能过度补货。

反馈依据：`feedback-v5.md` §五「inventory-replenishment v1.1 优化方向」+ answers-v5.md V5-SELF-001。

### 2. 需要新增到 SKILL.md 的内容

#### 新增 A：消耗异常分析子流程

在 Workflow Step 1「Identify the inventory scenario」之后，新增一个子步骤：

```markdown
### Workflow Step 1a: Consumption anomaly analysis (触达条件：月度消耗环比波动 > 20%)

When monthly consumption of a category rises more than 20% compared to the previous month, apply the following analysis dimensions before concluding waste:

1. Headcount change: check with HRBP whether headcount grew this month.
2. Department breakdown: review the issue ledger by department; identify concentration.
3. Project or event: check whether a training, onboarding batch, or large event consumed supplies.
4. Unit price: verify whether the purchase unit price changed this month.
5. Issue frequency: compare per-person issue frequency month-over-month.
6. Replenishment timing: check whether last month's replenishment was delayed, causing this month's batch purchase.

Output: a table with each dimension, the data source needed, and a preliminary finding.
Never conclude "employee waste" without completing all dimensions.
```

#### 新增 B：安全库存数据源优先级

插入到 Workflow Step 3「Compare against safety stock」之前：

```markdown
### Safety-stock data source priority

When multiple sources define safety stock for the same item, use this order:

1. **CSV 备注字段**（`03-资产台账.csv` column 16）: the authoritative current threshold for items tracked in the CSV.
2. **SOP 安全库存示例表**（`01-行政SOP.md` §6）: fallback for items listed in the SOP table.
3. **养虾人/财务确认**：for items not covered by either source, or when CSV and SOP disagree.

Example: 门禁卡 safety stock is defined only in CSV 备注 (20 张), not in SOP 示例表. Use CSV as authority.

Never invent a safety-stock number that does not appear in any source file.
```

#### 新增 C：安防耗材补货上限规则

替换 Workflow Step 4 中「If no batch is defined, replenish to at least 1.5 times safety stock」：

```markdown
### Replenishment calculation (revised)

1. If the SOP 补货批量 column specifies a batch size → use the batch size.
2. If no batch is defined:
   - **Ordinary consumables** (文具/茶水间耗材): replenish to max(缺口 + safety buffer, 1.2× safety stock).
   - **Security consumables** (安防耗材: 门禁卡、监控配件): replenish to 缺口 × 1.5, capped at min(3-month estimated demand, 2× safety stock). For access cards, estimate 3-month demand based on recent onboarding/visitor rates.
3. Preserve the formula in the answer.

Rationale: v1.0's "1.5× safety stock" gave 30 access cards (20×1.5), which may exceed reasonable demand. The cap prevents over-ordering of security items while still covering the deficit.
```

#### 新增 D：命令验证结构化输出格式

替换 Output Format 中的「命令验证」单行格式：

```markdown
### 命令验证

| 字段 | 内容 |
|------|------|
| 命令 | `grep "中性笔" knowledge/kunjie-admin/03-资产台账.csv` |
| 验证对象 | 中性笔当前库存、安全库存 |
| 输出摘要 | `KJ-STK-2026-0017,中性笔,...,当前96支 低于安全库存120支` |
| 业务结论 | 当前 96 < 安全库存 120，缺口 24 支，触发补货 |
```

### 3. 建议替换的旧表述

| 旧表述（v1.0） | 新表述（v1.1） | 位置 |
|----------------|---------------|------|
| `If no batch is defined, replenish to at least 1.5 times safety stock unless the SOP says otherwise` | 新增 C 的安防耗材上限规则 | Workflow Step 4 |
| `命令：/ 确认结果：`（单行） | 四字段结构化表格 | Output Format §命令验证 |
| Step 1「Consumption anomaly: compare department, requester, project, event, unit price, and headcount drivers」（一句话） | 新增 A 的完整 6 维分析子流程 | Workflow Step 1a |
| 无安全库存优先级规则 | 新增 B 的 CSV > SOP > 养虾人 三级优先级 | Workflow Step 3 前 |

### 4. 新增 Guardrails

```markdown
- Do not conclude "employee waste" before completing all consumption-anomaly dimensions.
- Do not use SOP safety-stock numbers when the CSV 备注 field contains a more specific number for the same item.
- Do not order more than 3 months' estimated demand for security consumables without养虾人 approval.
- Do not skip the four-field structured command verification when reporting inventory counts.
```

### 5. 新增 Eval v6 验证题建议

| # | 测试点 | 验证方式 |
|:-:|--------|----------|
| 1 | **消耗异常 6 维分析**：某月中性笔消耗环比上涨 40%，已知入职 3 人+项目培训。走完整 6 维分析，输出分析表。 | 必须调用 Step 1a，按维度逐项输出+数据来源，不直接定性。 |
| 2 | **安全库存优先级**：门禁卡的安全库存从哪里取？如果 SOP 示例表有「办公用品」安全库存但没有门禁卡，应该怎么办？ | 验证调用新增 B 的优先级规则，引用 CSV 备注而非编造。 |
| 3 | **安防耗材补货上限**：门禁卡库存 10 张，安全库存 20。按 v1.0 补 1.5 倍 = 30 张，近 3 月入职预估 4 人+访客 10 人次。v1.1 应该建议补多少？ | 调用新增 C 的上限规则，给出带计算过程的补货量。 |
| 4 | **结构化命令验证**：扫描全部库存类资产，用四字段格式输出每项的验证结果。 | 每项必须有命令/验证对象/输出摘要/业务结论四字段。 |
| 5 | **消耗异常 vs 正常增长判定**：补货量本月比上月增加 50%，但全员人数增加了 10%。判断是异常还是正常增长。 | 在 6 维分析中区分人数增长=正常消耗增加。 |

---

## 2. supplier-risk-review v1.1 草案

### 1. 修改目标

v1.0 在 Eval v5 中合同到期、选型评估、回扣联动表现稳定。v1.1 重点补三个缺口：
1. **SLA 整改缺少量化标准**——v1.0 Workflow Step 4 说「服务投诉→整改」，但没有「几次不达标启动什么动作」的量化标准。
2. **替换触发条件分散**——答题时补充了「连续 2 次整改未达标/重大事故/年度 3 次不达标」三个条件，但 Skill 原文没有固化。
3. **月度风险报告只有概念**——v1.0 的 Output Format 是单次评估模板，缺少月度汇总报告结构。

反馈依据：`feedback-v5.md` §五「supplier-risk-review v1.1 优化方向」+ answers-v5.md V5-SELF-001。

### 2. 需要新增到 SKILL.md 的内容

#### 新增 A：SLA 量化整改标准

在 Workflow Step 4「Build recommendation」中服务投诉分支，新增子步骤：

```markdown
### SLA compliance and整改 thresholds

When a service complaint arises, apply quantitative SLA check before issuing a整改 notice:

1. **Collect evidence**: date, time, location, photo, and employee name for at least 2 independent incidents.
2. **Compare against SLA**: extract the SLA clause from the supplier CSV row (`$11`).
   - 每日保洁: check whether 1+ complaints per week for 2 consecutive weeks.
   - 故障响应: check response time against SLA clock (e.g. 4h/8h/48h).
3. **Determine severity**:

| Severity | Criteria | Action |
|----------|----------|--------|
| Minor | 1 incident, first occurrence | Verbal reminder, log event |
| Moderate | 2-3 incidents in 2 weeks, or 1 SLA breach | Written整改 notice, 7-day deadline,月度评分 扣分 |
| Severe | 4+ incidents in 2 weeks, or 2 consecutive months with moderate issues | Written整改 + 降级 review + start replacement market search |
| Critical | Major service failure (e.g. client visit impacted) | Immediate freeze + escalate to养虾人 + emergency replacement |

4. **Re-inspect** after the整改 deadline and update the monthly score.
5. If re-inspection fails → escalate severity one level and re-apply.
```

#### 新增 B：供应商替换触发条件表

在 Workflow Step 4 之后新增一个独立的判定表：

```markdown
### Supplier replacement trigger conditions

Replace a supplier when **any one** of the following is met. Do not wait for all conditions to accumulate.

| # | Trigger | Example |
|:-:|---------|---------|
| 1 | Contract expired and supplier is C-level | SUP-MTG-003 (expired May 2026, C-level) |
| 2 | Contract expired and no renewal decision within 30 days of expiry | A/B-level supplier with overdue renewal |
| 3 | 2 consecutive整改 cycles failed (7+7=14 days) | Cleaner SLA fails twice |
| 4 | 3 monthly scores below passing threshold in a 12-month period | Repeated poor satisfaction |
| 5 | Single major service incident with client impact | Client meeting disrupted by equipment failure |
| 6 | Kickback, fraud, or corruption event confirmed by compliance | Supplier offered rebate; 明镜 concludes misconduct |
| 7 | Risk level escalated to high and business-critical service affected | Access-control supplier becomes high risk |

Note: conditions 1-5 apply to service/performance; conditions 6-7 apply to risk/compliance.
The administration recommends replacement but does not make the final decision alone — approval chain applies.
```

#### 新增 C：月度供应商风险报告模板

在 Output Format 之后新增：

```markdown
### Monthly Supplier Risk Report Template

```markdown
════════════════════════════════════════
  供应商月度风险报告 · YYYY年MM月
════════════════════════════════════════

一、基础数据
  - 供应商总数: [N]（A级:[N] / B级:[N] / C级:[N]）
  - 高风险供应商: [list]
  - 本月新增/变更: [N]

二、合同到期预警
| 优先级 | 供应商 | 到期日 | 剩N天 | 等级 | 风险 | 动作 | 责任人 | 截止 |
|--------|--------|--------|:---:|:---:|------|------|--------|:---:|
| P0 | ... | ... | ... | ... | ... | ... | ... | ... |

三、SLA与服务评价
| 供应商 | SLA条款 | 达标 | 投诉次数 | 本月评分 | 动作 |
|--------|---------|:---:|:---:|:---:|------|

四、整改与风控事项
| 供应商 | 事项 | 严重度 | 开始 | 截止 | 状态 | 升级对象 |
|--------|------|:---:|------|------|:---:|----------|

五、下月决策事项
1. [续约/替换/比价/冻结] — [供应商] — [原因] — [建议审批链]

六、数据来源与边界
  - 供应商数据: 05-供应商清单.csv
  - SLA评价: 月度员工问卷+投诉记录
  - 采购金额: 采购台账（训练口径，非真实制度）

⚠️ 训练边界声明: 金额为训练用合成数据，真实落地前由养虾人确认。
```
```

#### 新增 D：回扣/风控状态下等级不变强化句式

替换 Workflow Step 5「Link guardrails」中的 G 类型描述：

```markdown
### Kickback / risk-event supplier-level freeze (强化)

When a supplier is involved in a kickback, rebate, fraud, or compliance investigation:

**Supplier level must remain frozen.** Do not upgrade, downgrade, renew, or terminate the supplier relationship until the compliance (明镜) investigation concludes.

Standard response:
> 该供应商因 [事件类型] 已被冻结参与资格。风控（明镜）调查完成前，供应商等级、合同状态、续约建议均不得变更。调查结论出具后，按结论执行降级/淘汰/恢复。

Link: call `authority-guardrail` type G for the full incident-handling chain.

Any attempt to modify supplier level before investigation conclusion is a separate authority-guardrail violation.
```

### 3. 建议替换的旧表述

| 旧表述（v1.0） | 新表述（v1.1） | 位置 |
|----------------|---------------|------|
| Workflow Step 4 服务投诉分支只有概念描述 | 新增 A 的 SLA 量化整改标准表 | Workflow Step 4 |
| 无替换触发条件表 | 新增 B 的 7 条件触发表 | Workflow Step 4 后 |
| Output Format 只有单次评估模板 | 新增 C 的月度风险报告模板 | Output Format 后 |
| Step 5 G 类型描述偏简略 | 新增 D 的强化句式（等级冻结+标准回复） | Workflow Step 5 |

### 4. 新增 Guardrails

```markdown
- Do not issue a整改 notice without at least 2 independent incident records.
- Do not downgrade a supplier without a completed SLA compliance review.
- Do not replace a supplier solely on subjective dissatisfaction; apply the replacement trigger table.
- Do not modify supplier level during an active compliance investigation.
- Do not promise a renewal recommendation when the supplier is under investigation.
```

### 5. 新增 Eval v6 验证题建议

| # | 测试点 | 验证方式 |
|:-:|--------|----------|
| 1 | **SLA 量化整改**：SUP-CLEAN-001 连续 2 周每天都有员工投诉茶水间脏。按 v1.1 分级标准，这是什么严重度？给具体整改步骤。 | 调用新增 A 的严重度分级表，输出 Moderate→Severe 升级路径。 |
| 2 | **替换触发条件**：某 B 级供应商年度评分已 2 次不达标，本次再评为不达标。是否触发替换？引用条件表中哪一条。 | 调用新增 B 的触发条件表，匹配条件 4。 |
| 3 | **月度风险报告输出**：基于当前 20 家供应商数据（含 SUP-SEC-001 即将到期、SUP-MTG-003 已过期），用新增 C 的模板输出完整月报。 | 调用新增 C，填满五个部分，不含虚构金额。 |
| 4 | **回扣事件等级冻结**：SUP-XXX 被举报回扣，HR 问能不能先降为 C 级。按 v1.1 强化句式回复。 | 调用新增 D，输出标准拒绝句式+原因。 |
| 5 | **替换 vs 整改升级判断**：SUP-CLEAN-001 第一次整改未通过。是再给一次机会，还是直接替换？ | 同时使用新增 A 的升级规则+新增 B 的条件 2。 |

---

## 3. onboarding-offboarding-sop v1.1 草案

### 1. 修改目标

v1.0 在 Eval v5 中入离职时间线、异常处理、权限联动表现稳定。v1.1 重点补四个缺口：
1. **资产不足处理分支**——v1.0 的 Onboarding Step 2 只说「扫描闲置资产」，没有「不够了怎么办」的分支（v5 HR-001 闲置电脑 2 < 入职 3 人，靠答题者自己补充方案）。
2. **T+7 回访清单模板**——v1.0 只说「T+7 onboarding experience check」，没有具体检查清单（v5 HR-005 三个问题全靠答题经验）。
3. **候选人 vs 正式入职边界**——v1.0 没有明确「什么情况触发入职 Skill、什么情况只是访客接待」（v5 HR-006 靠 Guardrails 推理）。
4. **权限开通「确认后开通」句式**——feedback-v5.md 整改 2：V5-HR-004 对用车权限写「可开」不够，需加「HRBP/上级确认岗位需要后开通」。

反馈依据：`feedback-v5.md` §五「onboarding-offboarding-sop v1.1 优化方向」+ 整改 2 + answers-v5.md V5-SELF-001。

### 2. 需要新增到 SKILL.md 的内容

#### 新增 A：入职资产不足处理分支

在 Onboarding Workflow Step 2「Verify assignable assets」之后，新增子步骤：

```markdown
### Step 2a: Asset shortage handling

When assignable assets are fewer than the onboarding headcount:

| Shortage item | Priority 1 | Priority 2 | Priority 3 |
|---------------|------------|------------|-------------|
| Laptop | Reassign from employees with underutilized devices (coordinate with department head) | Emergency procurement (follow purchase threshold for amount) | Notify HRBP: device ready date may be T+2 or T+3 |
| Monitor | Check if any employee has dual monitors and can spare one | Emergency procurement | Standard procurement + temporary workaround (laptop screen only) |
| Access card | **Never delay** — access is non-negotiable. If stock is low, call `inventory-replenishment` for emergency replenishment. If supplier is unreliable, use temporary visitor pass as bridge. | — | — |
| Desk | Check vacant desks or temporary hot-desking | Reconfigure layout | Notify HRBP |

For emergency procurement above ¥5000: route through财务复核 + 养虾人终审 before purchase.
For procurement below thresholds: follow `01-行政SOP.md` §5 procurement workflow.
Document the gap, the chosen solution, and the expected resolution date.
```

#### 新增 B：T+7 入职回访清单

替换 Onboarding Workflow Step 6「Follow up」中的「T+7 onboarding experience check」：

```markdown
### Step 6: T+7 onboarding follow-up checklist

On T+7, conduct a structured check with the new employee covering 5 dimensions:

| # | Dimension | Check item | Normal | Issue → Action |
|:-:|-----------|------------|--------|----------------|
| 1 | **Device** | Laptop, monitor, keyboard, mouse, adapter functioning? | All normal | 建报修工单 → contact supplier or IT |
| 2 | **Workspace** | Desk, chair, lighting, air-conditioning comfortable? | Comfortable | 联系物业 (SUP-PARK-001) or adjust seating |
| 3 | **Environment** | Noise, cleanliness,茶水间 access acceptable? | Acceptable | 联系保洁 (SUP-CLEAN-001) or facility |
| 4 | **Permissions** | Email, SSO, travel, reimbursement, meeting, car all working? | All working | Check with IT; verify no over-provisioning |
| 5 | **Access** | Access card works every time? Door, elevator, printer access OK? | 3 consecutive successes | Replace card or check reader (SUP-SEC-001) |

For each issue found: create a ticket with owner, deadline, and closure criteria.
After all issues are resolved, close the T+7 follow-up record.
```

#### 新增 C：候选人接待 vs 正式入职边界

在 Onboarding Workflow 之前新增一个判定规则：

```markdown
### 边界判定：正式入职 vs 候选人访客接待

Before executing the Onboarding Workflow, determine whether this is an onboarding or a visitor scenario:

| Signal | Scenario | Action |
|--------|:--------:|--------|
| HRBP sends formal onboarding list with start date | ✅ 正式入职 | Execute full Onboarding Workflow |
| HRBP requests "interview candidate" or "终面" logistics | ❌ 候选人访客 | **Do not execute Onboarding Workflow.** Apply C-level visitor reception (`01-行政SOP.md` §8.1): visitor registration → temporary access card → meeting room → escort → return pass on departure. |
| "New joiner" mentioned but no HRBP list | ⚠️ Uncertain | Confirm with HRBP before taking any action |

Rules for candidate visitors:
- ❌ Do not create employee asset records.
- ❌ Do not open formal system accounts (email, SSO, travel, reimbursement).
- ❌ Do not issue permanent access cards.
- ❌ Do not prepare a permanent desk.
- ✅ Register as visitor, issue temporary pass, prepare interview room, escort during visit,回收 pass on departure.
```

#### 新增 D：权限开通「确认后开通」标准句式

替换 Onboarding Workflow Step 4 中「Open travel, reimbursement, meeting, or car permissions only as role requires」的表述：

```markdown
### Permission activation: confirm-then-open

Permissions must follow minimum-privilege principle. Use the following decision chain:

1. **Base permissions** (all roles): email + SSO + reimbursement (合思) + meeting (腾讯会议).
2. **Role-conditional permissions**: open only after confirming with HRBP/direct manager that the role requires it.

| Permission | Default | Activation Condition |
|------------|:------:|----------------------|
| 携程商旅 (travel booking) | ❌ Closed | HRBP confirms role requires travel |
| 滴滴企业版 (corporate car) | ❌ Closed | HRBP/direct manager confirms external client visits or field work; 员工级 only |
| 高铁一等座 | ❌ Closed | Director level or above, or client accompaniment with approval |
| 管理员权限 | ❌ **Never** | Not for non-admin employees |

Standard activation phrasing:
> [权限名称]：该岗位是否需要 [业务场景]？请 HRBP/直属上级确认后，行政按 [员工级/标准级] 开通。

Never open permissions solely on employee verbal request without HRBP/manager confirmation.
Never open elevated permissions (一等座、管理员) without written approval.
```

### 3. 建议替换的旧表述

| 旧表述（v1.0） | 新表述（v1.1） | 位置 |
|----------------|---------------|------|
| Onboarding Step 2 只扫描闲置，无不足分支 | 新增 A 的资产不足处理分支表 | Onboarding Workflow Step 2a |
| Step 6「T+7 onboarding experience check」（一句话） | 新增 B 的 5 维回访清单 | Onboarding Workflow Step 6 |
| 无边界判定规则 | 新增 C 的「正式入职 vs 候选人访客」判定表 | Onboarding Workflow 之前 |
| Step 4「only as role requires」 | 新增 D 的「确认后开通」决策链 + 标准句式 | Onboarding Workflow Step 4 |

### 4. 新增 Guardrails

```markdown
- Do not execute the Onboarding Workflow for interview candidates — apply visitor reception instead.
- Do not open corporate car or elevated travel permissions without HRBP/manager written confirmation.
- Do not delay access-card issuance due to asset shortage — access is non-negotiable and must have a bridge solution.
- Do not skip the T+7 follow-up checklist dimensions.
- Do not assume "role requires travel" — confirm before opening.
```

### 5. 新增 Eval v6 验证题建议

| # | 测试点 | 验证方式 |
|:-:|--------|----------|
| 1 | **资产不足处理**：入职 4 人，闲置电脑仅 1 台，闲置显示器 0 台。按 v1.1 新增 A 输出处理方案。 | 走调配→紧急采购→通知 HRBP 三级链路，区分电脑和门禁卡的不同优先级。 |
| 2 | **T+7 回访清单**：新员工反馈键盘失灵+会议室预约总是被拒+门禁卡偶尔刷不开。按新增 B 的 5 维清单输出跟进单。 | 每项匹配维度→动作，键盘走维度 1 报修，会议室走维度 3 协调，门禁走维度 5 换卡。 |
| 3 | **候选人边界**：HRBP 说「明天有个终面候选人，你准备一下」。触发入职 Skill 还是访客接待？ | 调用新增 C 判定表 → 访客接待。不创建资产台账、不开正式权限。 |
| 4 | **权限确认后开通**：销售新人入职当天要求开通滴滴企业版和高铁一等座。按新增 D 的标准句式回复。 | 用车：「请 HRBP/直属上级确认岗位需要外勤后开通员工级」；一等座：「总监以下需有客户陪同审批，暂不开通」。 |
| 5 | **T+7 回访闭环**：T+7 发现 3 个问题，T+14 复查仍有 1 个未解决。如何处理？ | 升级未解决问题→通知对应责任人→更新台账→上报（如影响工作）。 |

---

# 本轮执行总结

## 草案写入路径
`/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/skill-v1.1-drafts-v5.md`

## 读取了哪些文件

| 文件 | 用途 |
|------|------|
| `eval/kunjie-admin/feedback-v5.md` | Codex 老师批改反馈（231/240 分），确认 v1.1 优化方向和整改要求 |
| `eval/kunjie-admin/answers-v5.md` | 回顾 V5-SELF-001 中自提的 v1.1 优化建议（消耗异常子流程/SLA 量化/T+7 清单等），确保草案覆盖自提建议 |
| `workspace/skills/inventory-replenishment/SKILL.md` | v1.0 原文，对照修改 |
| `workspace/skills/supplier-risk-review/SKILL.md` | v1.0 原文，对照修改 |
| `workspace/skills/onboarding-offboarding-sop/SKILL.md` | v1.0 原文，对照修改 |

## 没有修改哪些正式文件

| 文件 | 状态 |
|------|:----:|
| `workspace/skills/inventory-replenishment/SKILL.md` | ❌ 未修改（v1.0 原样保留） |
| `workspace/skills/supplier-risk-review/SKILL.md` | ❌ 未修改（v1.0 原样保留） |
| `workspace/skills/onboarding-offboarding-sop/SKILL.md` | ❌ 未修改（v1.0 原样保留） |
| `workspace/skills/expense-review-sop/SKILL.md` | ❌ 未修改 |
| `workspace/skills/authority-guardrail/SKILL.md` | ❌ 未修改 |
| `SKILL.md`（根目录） | ❌ 未修改 |
| `workspace/skills/skills-index.md` | ❌ 未修改 |
| 所有知识包文件（knowledge/kunjie-admin/） | ❌ 未修改 |

仅写入本轮草案文件 `skill-v1.1-drafts-v5.md`。

## 哪些 v5 错点被吸收进草案

| v5 错点来源 | 问题描述 | 吸收到哪个草案 |
|-------------|----------|---------------|
| feedback-v5 整改 1 | V5-SELF-002 统计口径不一致：写"未触发 5 题"实际 6 题，且复盘题未单独列 | 本次执行总结采用正确口径（不混入 Skill 草案正文，但在起草时已注意统计自洽） |
| feedback-v5 整改 2 | V5-HR-004 权限开通写"可开"不够，需"确认后开通" | onboarding-offboarding-sop §新增 D：确认后开通标准句式 |
| feedback-v5 整改 3 | 命令验证结果需更结构化 | inventory-replenishment §新增 D：四字段结构化格式 |
| feedback-v5 §五 | inventory-replenishment 缺消耗异常分析子流程 | inventory-replenishment §新增 A |
| feedback-v5 §五 | inventory-replenishment 安全库存数据源优先级不明 | inventory-replenishment §新增 B |
| feedback-v5 §五 | inventory-replenishment 安防耗材补货上限缺失 | inventory-replenishment §新增 C |
| feedback-v5 §五 | supplier-risk-review 缺 SLA 量化标准 | supplier-risk-review §新增 A |
| feedback-v5 §五 | supplier-risk-review 缺替换触发条件表 | supplier-risk-review §新增 B |
| feedback-v5 §五 | supplier-risk-review 缺月度报告模板 | supplier-risk-review §新增 C |
| feedback-v5 §五 | supplier-risk-review 回扣/风控下等级冻结句式不够强 | supplier-risk-review §新增 D |
| feedback-v5 §五 | onboarding-offboarding-sop 缺入职资产不足处理 | onboarding-offboarding-sop §新增 A |
| feedback-v5 §五 | onboarding-offboarding-sop 缺 T+7 回访清单 | onboarding-offboarding-sop §新增 B |
| feedback-v5 §五 | onboarding-offboarding-sop 缺候选人边界规则 | onboarding-offboarding-sop §新增 C |
| V5-SELF-001 自提 | 三个 Skill 的 v1.1 优化点（消耗异常/SLA 量化/资产缺口等） | 全部吸收到对应 Skill 草案，自提建议与老师反馈高度一致 |

---

*v1.1 优化草案生成完毕。k01 行政虾。2026-06-26。*
*等待 Codex 老师审核确认后，再修改正式 Skill 文件。*
