---
name: admin-satisfaction-analysis
description: Use for administrative satisfaction survey analysis, score summaries, theme extraction, cross-file evidence checks, root-cause hypotheses, and improvement plans. Trigger when asked to summarize admin satisfaction, identify common complaints, compare survey feedback with operations data, or propose Q3/Q4 improvement actions.
---

# admin-satisfaction-analysis

Version: v1.0  
Owner: k01 行政虾  
Created: 2026-06-26 from Eval v5

## Purpose

Summarize satisfaction data while preserving the boundary between facts, evidence, hypotheses, and recommendations.

## Source Files

- Satisfaction survey responses and score tables.
- `workspace/skills/inventory-replenishment/SKILL.md`: use when feedback mentions office supplies or stockouts.
- `workspace/skills/admin-dispatch-sop/SKILL.md`: use when feedback mentions visitors, meeting rooms, or repairs.
- `workspace/skills/supplier-risk-review/SKILL.md`: use when feedback mentions suppliers, SLA, or contract expiry.
- `workspace/skills/expense-review-sop/SKILL.md`: use when feedback mentions reimbursement material quality or approval delays.

## Mandatory Verification

Calculate response counts, dimension averages, department averages, issue counts, and trend claims from the survey file. Do not infer company headcount, department population, response coverage, or impact percentage unless the data provides it.

If 8 survey responses contain 9 distinct issue points, say "8 responses produced 9 issue points." Do not mix response count with issue count.

## Workflow

1. Verify survey scope.
   - Response count, departments represented, dimensions, score scale, date range.

2. Calculate score summaries.
   - Dimension averages.
   - Department averages when department data exists.
   - Lowest-scoring dimensions and repeated low scores.

3. Extract text themes.
   - Preserve the number of responses and the number of issue points separately.
   - Group related feedback into themes.

4. Cross-check with operational data.
   - Inventory shortage, repair ticket, visitor log, supplier expiry, reimbursement backlog.
   - Mark each cross-check as confirmed, partially supported, or unverified.

5. State root causes carefully.
   - Use "possible cause" or "hypothesis" unless files directly prove causality.
   - Do not say a supplier failed to repair because payment was blocked unless the evidence explicitly says so.

6. Recommend improvements.
   - Tie each action to a verified theme.
   - Mark targets as suggested targets unless approved goals are provided.

## Output Format

```markdown
## 行政满意度分析

样本：
结论：

### 分数
| 维度 | 均分 | 证据 |

### 反馈主题
| 主题 | 问题点数 | 代表反馈 | 跨表印证 | 状态 |

### 可能根因
| 根因假设 | 支撑证据 | 仍需确认 |

### 改进建议
| 优先级 | 动作 | 关联问题 | 建议目标 | 责任人/建议责任人 |

### 边界说明
- 未提供公司/部门人数时，不推导影响人数或占比。
- 推断原因不写成事实。
```

## Guardrails

- Do not invent organization size, department size, response coverage, or trend history.
- Do not overstate cross-file correlation as causation.
- Do not call an improvement target official unless it is provided or approved.
- Do not merge response count, issue count, and record count into a single inflated total.
