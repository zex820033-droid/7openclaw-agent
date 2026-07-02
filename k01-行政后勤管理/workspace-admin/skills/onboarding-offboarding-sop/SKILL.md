---
name: onboarding-offboarding-sop
description: Use for employee onboarding and offboarding logistics, including workspace preparation, asset assignment, access-card handling, office supplies, account/permission opening or closing, asset return, and exception handling. Trigger when HR sends a new-hire or resignation list, when employees join or leave, when access or travel accounts must be opened/closed, or when offboarding assets or permissions are abnormal.
---

# onboarding-offboarding-sop

Version: v1.1  
Owner: k01 行政虾  
Created: 2026-06-26 from Eval v4

## Purpose

Make入职 and离职 predictable:

1. Prepare the right workspace, assets, access, and supplies before onboarding.
2. Close accounts and recover assets safely during offboarding.
3. Detect and escalate missing assets, access-card loss, and permission residue.

## Source Files

- `knowledge/kunjie-admin/04-差旅平台-OA-报销系统账号.md`: account opening/closing and HR handoff.
- `knowledge/kunjie-admin/01-行政SOP.md`: asset lifecycle and admin workflows.
- `knowledge/kunjie-admin/03-资产台账.csv`: assignable assets and returned assets.
- `workspace/skills/authority-guardrail/SKILL.md`: use for retained leaver permissions, shared accounts, and access-card security.
- `workspace/skills/inventory-replenishment/SKILL.md`: use when onboarding supplies or access cards affect inventory.

## Required Inputs

- Employee name, department, role, location, join/leave date.
- For onboarding: required equipment, workspace, access, and system permissions.
- For offboarding: asset list, account list, last working day, returned/missing items.
- HRBP contact and IT contact when available.

## Mandatory Verification

Use commands for exact asset counts, idle assets, asset status, inventory counts, and account lists when represented in files.

Recommended command patterns:

```bash
grep -n "闲置\\|待分配\\|门禁卡" knowledge/kunjie-admin/03-资产台账.csv
awk -F',' '...' knowledge/kunjie-admin/03-资产台账.csv
```

Do not decide that enough laptops, monitors, or access cards exist without verification.

Do not infer headcount, spare capacity, or weekend handling rules from context. Verify from files or state the missing data.

## Onboarding Workflow

1. Confirm HRBP input.
   - Name, department, role, location, start date, manager.

2. Verify assignable assets.
   - Scan idle or pending-allocation computers, monitors, and required accessories.
   - Match by role: sales, R&D, operations, or manager needs may differ.

3. Prepare workspace and supplies.
   - Desk, monitor, keyboard/mouse, access card, onboarding pack.
   - If supplies fall below safety stock after issue, call `inventory-replenishment`.

4. Coordinate accounts and permissions.
   - Notify IT for email/SSO.
   - Open travel, reimbursement, meeting, or car permissions only as role requires.

5. Complete day-one signoff.
   - Employee signs asset receipt.
   - Verify login and access-card usability.

6. Follow up.
   - T+1 permission check.
   - T+7 onboarding experience check.

## Offboarding Workflow

1. T-3: receive HRBP offboarding notice and list all assets/accounts.
2. T-1: remind employee to return equipment and access card; notify IT.
3. T day: recover physical assets, inspect condition, sign return confirmation, disable access card.
4. T+1: close all system permissions. If any permission remains active, call `authority-guardrail` type D.
5. T+3: complete exception review and update ledgers.

If T+1 falls on a weekend or holiday, do not automatically move closure to the next workday. Arrange scheduled closure, administrator closure, or IT duty closure in advance.

## Exception Handling

- Missing laptop/monitor: record exception, set return deadline, notify HRBP and owner, escalate if overdue.
- Lost access card: immediately disable or挂失; call `authority-guardrail` type I.
- Active leaver account: immediate closure; P1 escalation to IT and养虾人 if not closed.
- Damaged asset: record condition, evaluate repair/compensation path with finance/HR.
- Business history, orders, files, or code needed after offboarding must be exported by an administrator or an active owner using their own permissions. Do not keep, share, or borrow the leaver account.
- Asset gaps that depend on future returns must be marked as dependency risks, not guaranteed availability.

## Output Format

```markdown
## 入离职后勤处理单

结论：
风险标签：

### 命令验证
- 命令：
- 确认结果：

### 时间线
| 时间 | 动作 | 责任人 | 状态 |

### 资产/权限清单
| 项目 | 当前状态 | 动作 | 台账更新 |

### 异常处理
- 异常：
- 升级对象：
- 截止时间：

### 不可做事项
- ...
```

## Ledger Updates

- Asset ledger: owner, department, location, status, return condition.
- Access-card ledger: holder, status, issue/return/loss.
- Permission audit: opened/closed systems, executor, date.
- Issue ledger: onboarding supplies.
- Offboarding exception record: missing or damaged assets, residual accounts.

## Guardrails

- Do not keep leaver permissions after T+1.
- Do not share or borrow leaver accounts.
- Do not transfer assets without receipt or return confirmation.
- Do not issue access cards without registration.
- Do not ignore lost access cards.
- Do not open permissions that the role does not need.
- Do not rely on memory for assignable asset counts.

## Related Skills

- Call `authority-guardrail` for leaver permissions, shared accounts, and access-card security.
- Call `inventory-replenishment` when onboarding/offboarding changes supply or access-card inventory.
- Call `expense-review-sop` if emergency onboarding procurement later enters reimbursement review.

## Eval v5 Coverage

Validate this skill with:

- Batch onboarding with insufficient idle laptops.
- Offboarding with missing monitor and lost access card.
- T+1 residual permission audit.
- Access-card inventory changes from onboarding/offboarding.
- T+7 onboarding follow-up with device and workspace issues.
