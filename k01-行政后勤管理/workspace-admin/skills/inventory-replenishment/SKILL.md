---
name: inventory-replenishment
description: Use for administrative inventory scanning, office supply issuing, safety-stock checks, replenishment planning, and purchase-threshold routing. Trigger when asked to check whether supplies are enough, process office-supply requests, scan low-stock items, plan replenishment, analyze consumption spikes, or decide the approval path for replenishment purchases.
---

# inventory-replenishment

Version: v1.1  
Owner: k01 行政虾  
Created: 2026-06-26 from Eval v4

## Purpose

Answer three questions reliably:

1. What is low or will become low after issuing supplies?
2. How much should be replenished?
3. Which procurement approval path applies?

## Source Files

- `knowledge/kunjie-admin/03-资产台账.csv`: current inventory, asset status, stock-like items.
- `knowledge/kunjie-admin/01-行政SOP.md`: office-supply issue rules, safety stock, procurement workflow.
- `knowledge/kunjie-admin/05-供应商清单.csv`: supplier status and risk before purchasing.
- `workspace/skills/authority-guardrail/SKILL.md`: use when split-order, bypassing approval, or security inventory risks appear.

## Required Inputs

- Request type: stock scan, issue request, replenishment plan, or consumption analysis.
- Item names and quantities, if issuing supplies.
- Department, requester, and usage purpose for issue requests.
- Current date for weekly purchase timing or contract-date checks.

## Mandatory Verification

Use commands for every exact inventory count, asset status, supplier count, contract date, or total amount.

Recommended command patterns:

```bash
grep -n "中性笔\\|转接头\\|门禁卡" knowledge/kunjie-admin/03-资产台账.csv
awk -F',' '...' knowledge/kunjie-admin/03-资产台账.csv
```

Reading the CSV is not enough when reporting exact numbers. Say which command was used and what it confirmed.

Before writing any total, amount, post-issue stock, approval threshold, or risk count, verify the value from the file or show the calculation. If a required file or field is missing, state the data gap instead of estimating.

## Workflow

1. Identify the inventory scenario.
   - Issue request: calculate post-issue quantity.
   - Weekly scan: scan all inventory or consumable rows.
   - Consumption anomaly: compare department, requester, project, event, unit price, and headcount drivers.

2. Verify current stock with commands.
   - Report item, current quantity, safety stock, unit, and source row.
   - Do not quote counts from memory.

3. Compare against safety stock.
   - Current quantity >= safety stock: sufficient.
   - Current quantity < safety stock: low stock.
   - Post-issue quantity < safety stock: issue can be recorded, but replenishment must be triggered.

4. Calculate replenishment.
   - Use the replenishment batch in the SOP when available.
   - If no batch is defined, replenish to at least 1.5 times safety stock unless the SOP says otherwise.
   - Preserve a clear formula in the answer.

5. Decide procurement route.
   - Sum same-day or same-supplier replenishment needs.
   - Use the combined amount to choose the approval path.
   - Do not split orders to avoid approval. If split-order language appears, call `authority-guardrail`.
   - If combining items from the same supplier or category, say: "combine for control and use the higher approval threshold." Do not say combining reduces quote or approval requirements.

6. Check supplier risk.
   - If the item relies on a supplier with an expired or soon-expiring contract, flag it before purchasing.
   - For security items such as access cards, treat supplier disruption as a higher risk.
   - Do not recommend a replacement supplier unless the data confirms that supplier can cover the item category. If no substitute is present, recommend sourcing instead.

7. Output ledger updates.
   - Issue ledger after employee issue.
   - Inventory ledger after issue or inbound replenishment.
   - Procurement ledger after purchase request creation.

## Output Format

```markdown
## 库存/补货结论

结论：
风险标签：

### 命令验证
- 命令：
- 确认结果：

### 库存判断
| 物品 | 当前量 | 安全库存 | 领用后 | 状态 | 建议 |

### 补货建议
| 物品 | 建议补货量 | 预估单价 | 预估金额 | 供应商 | 风险 |

### 采购链路
- 合计金额：
- 审批档位：
- 比价要求：
- 是否触发 authority-guardrail：

### 台账更新
- 领用台账：
- 库存台账：
- 采购台账：

### 不可做事项
- ...
```

## Guardrails

- Do not report inventory counts from memory.
- Do not issue supplies without recording department, requester, quantity, and purpose.
- Do not promise immediate replenishment before approval or purchase routing.
- Do not split purchases to avoid approval thresholds.
- Do not ignore supplier contract risk for replenishment.
- Do not treat security consumables, such as access cards, as ordinary stationery.
- Do not claim a supplier can cover a category unless the supplier ledger shows that capability.
- Do not present inferred causes as facts; use "possible" or "needs confirmation" for causal links.

## Escalate When

- Combined replenishment reaches a higher approval threshold.
- The replenishment supplier is expired, high risk, or involved in a risk event.
- Security inventory may disrupt access control.
- Inventory data conflicts with the ledger or cannot be verified.

## Eval v5 Coverage

Validate this skill with:

- Low-stock scan using commands.
- Post-issue inventory calculation.
- Combined procurement threshold judgment.
- Supplier-risk linkage for security consumables.
- Monthly consumption anomaly analysis.
