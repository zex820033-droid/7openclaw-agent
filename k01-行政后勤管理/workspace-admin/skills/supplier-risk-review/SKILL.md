---
name: supplier-risk-review
description: Use for supplier contract-expiry scans, supplier level and risk review, SLA or satisfaction review, procurement supplier selection, renewal-or-replacement recommendations, and supplier risk incidents. Trigger when asked which suppliers are expiring, whether to renew a supplier, how to choose among suppliers, how to handle supplier service problems, or how to respond to kickbacks or abnormal supplier behavior.
---

# supplier-risk-review

Version: v1.1  
Owner: k01 行政虾  
Created: 2026-06-26 from Eval v4

## Purpose

Turn supplier information into a clear risk decision:

1. Is the supplier usable now?
2. Is the contract expired or nearing expiry?
3. Should the company renew, replace, compare quotes, freeze, or escalate?

## Source Files

- `knowledge/kunjie-admin/05-供应商清单.csv`: supplier ID, category, level, contract dates, SLA, risk.
- `knowledge/kunjie-admin/01-行政SOP.md`: procurement and supplier workflow.
- `workspace/skills/authority-guardrail/SKILL.md`: use for kickbacks, bypassing bidding, split orders, or fraud.
- `workspace/skills/inventory-replenishment/SKILL.md`: use when replenishment depends on a supplier.

## Required Inputs

- Scenario: expiry scan, supplier choice, renewal review, service complaint, or risk incident.
- Current date.
- Supplier ID, category, purchase amount, or requested service.
- Evidence for complaints or risk events, if any.

## Mandatory Verification

Use commands for supplier counts, level distribution, contract expiry dates, risk levels, and supplier identity.

Recommended command patterns:

```bash
awk -F',' '...' knowledge/kunjie-admin/05-供应商清单.csv
cut -d',' -f1,2,3,4,8,9 knowledge/kunjie-admin/05-供应商清单.csv
```

Do not say "20 suppliers", "A11/B7/C2", or "expires in N days" without command verification in the current run.

When reporting supplier totals, level distributions, expiry buckets, SLA averages, or risk counts, show the command or calculation basis. If the data contains 18 suppliers, never round or infer a larger total from context.

## Workflow

1. Identify supplier task type.
   - Contract expiry scan.
   - Supplier selection for a purchase.
   - Renewal or replacement decision.
   - Service/SLA complaint.
   - Risk event such as kickback or abnormal private contact.

2. Verify supplier data with commands.
   - Supplier ID, name, category, level, risk, contract start/end, SLA.
   - For expiry scans, calculate days to expiry from the current date.
   - Keep the original supplier level unless the source file or approved policy defines a changed level. Do not invent levels such as B+ or B-.

3. Classify risk.
   - Expired: immediate action.
   - <=30 days: urgent renewal or replacement review.
   - <=60 days: early warning.
   - High risk, C-level, or expired contract: do not recommend automatic renewal.

4. Build recommendation.
   - Renew only after reviewing price, SLA, service record, risk level, and business necessity.
   - Replace when supplier is expired, C-level with poor service, high risk, or involved in misconduct.
   - For purchases above procurement thresholds, ensure quote comparison and approval chain.
   - Recommend a substitute only when the supplier ledger confirms category capability. If no category-capable substitute exists, recommend sourcing at least two options instead.

5. Link guardrails.
   - Kickback, rebate, gift, or private benefit: call `authority-guardrail` type G.
   - "Use familiar supplier, no comparison": call `authority-guardrail` type B.
   - Split procurement: call `authority-guardrail` type F.

6. Output ledger updates.
   - Supplier ledger: expiry status, risk status, renewal decision.
   - Procurement ledger: quote comparison, selected supplier rationale.
   - Risk ledger: incident, evidence, escalation status.

## Output Format

```markdown
## 供应商风险评估

结论：
风险标签：

### 命令验证
- 命令：
- 确认结果：

### 供应商信息
| ID | 名称 | 品类 | 等级 | 风险 | 合同到期 | 距今天数 |

### 判断过程
1. 合同状态：
2. 等级/SLA/风险：
3. 采购或续约要求：
4. 是否触发 authority-guardrail：

### 建议动作
- 续约/替换/冻结/比价/上报：
- 责任人：
- 截止时间：

### 台账更新
- ...
```

## Guardrails

- Do not choose suppliers only by lowest price.
- Do not renew expired suppliers automatically.
- Do not let administration make the final supplier decision when approval is required.
- Do not modify supplier level before risk/compliance conclusion.
- Do not ignore evidence requirements for service complaints.
- Do not handle kickback or rebate events privately.
- Do not create supplier counts, levels, categories, or replacement capabilities that are not present in the data.
- Do not state causal explanations as facts when the data only shows correlation; mark them as possible and requiring confirmation.

## Escalate When

- A supplier offers kickbacks, rebates, gifts, or private benefits.
- A high-risk supplier is connected to security, access control, network, or payment.
- A contract is expired and service continuity is affected.
- A procurement request tries to bypass comparison or approval.

## Eval v5 Coverage

Validate this skill with:

- Contract expiry scan by current date.
- Supplier selection with C-level low-price supplier.
- SLA complaint and整改 path.
- Kickback event linkage to `authority-guardrail`.
- Monthly supplier risk report.
