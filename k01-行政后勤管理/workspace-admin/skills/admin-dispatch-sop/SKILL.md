---
name: admin-dispatch-sop
description: Use for administrative dispatch across meeting rooms, visitor appointments, front-desk registration, facility repairs, urgent room conflicts, event logistics, and repair-to-meeting coordination. Trigger when asked how to arrange today's admin requests, resolve meeting or visitor conflicts, coordinate repairs, or decide what operational actions are needed.
---

# admin-dispatch-sop

Version: v1.0  
Owner: k01 行政虾  
Created: 2026-06-26 from Eval v5

## Purpose

Turn meeting, visitor, and repair requests into a grounded action plan without inventing resources.

## Source Files

- Admin request logs: meeting-room bookings, visitor appointments, repair records.
- `workspace/skills/authority-guardrail/SKILL.md`: use for visitor registration shortcuts or access-control risks.
- `workspace/skills/inventory-replenishment/SKILL.md`: use when room setup depends on supplies such as adapters, access cards, labels, or refreshments.
- `workspace/skills/expense-review-sop/SKILL.md`: use when a repair or service request is blocked by reimbursement/material issues.
- `workspace/skills/supplier-risk-review/SKILL.md`: use when the request involves a risky or expired supplier.

## Mandatory Verification

Verify exact dates, times, rooms, requester, visitor identity status, repair status, and linked ticket or reimbursement numbers from files before reporting them.

Do not create meeting-room names, capacity, equipment, availability, company headcount, or visitor details. If a room resource table is missing, state the data gap and ask for the room resource table before assigning an alternate room.

## Workflow

1. Classify each request.
   - Meeting room.
   - Visitor appointment.
   - Repair or facility issue.
   - Event support or supplies.
   - Security-sensitive access request.

2. Verify time and dependency.
   - Date/time, location, requester, expected attendees or visitors, equipment needs, current status.
   - Linked inventory item, supplier, reimbursement, or risk event.

3. Detect conflicts and blockers.
   - Same room and overlapping time.
   - Missing visitor identity or host.
   - Repair not closed before a scheduled meeting.
   - Required supplies below safety stock.
   - Supplier access or contract risk.

4. Apply boundaries.
   - No visitor enters before registration.
   - No substitute meeting room may be named unless the room resource table confirms it.
   - No causal claim such as "supplier will not repair because payment is blocked" unless the evidence says so. Use "possible impact, needs confirmation."

5. Build an action plan.
   - Immediate actions first.
   - Name the evidence source for each action.
   - Use "suggested owner" if the owner is inferred rather than present in the data.

## Output Format

```markdown
## 行政调度处理单

结论：
数据缺口：

### 请求清单
| 编号 | 类型 | 时间 | 地点 | 申请人 | 状态 | 证据 |

### 冲突/阻塞
| 风险 | 证据 | 判断 | 需要确认 |

### 今日动作
| 优先级 | 动作 | 责任人/建议责任人 | 截止时间 | 依赖 |

### 不可做事项
- 未登记访客不得进入办公区。
- 未提供会议室资源表时不得编造替代会议室。
- 未确认因果时不得把推断写成事实。
```

## Escalate When

- A visitor requests or has already bypassed registration.
- A high-risk or expired supplier needs office access.
- A repair issue blocks a same-day or next-day critical meeting.
- Required security consumables may fall below safe operating stock.
