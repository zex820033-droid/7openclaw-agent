# 鲲界行政 Eval v2：Skill 验证

## 目标

验证两个已创建 Skill 是否真正生效：

- `expense-review-sop`
- `authority-guardrail`

## 文件

| 文件 | 用途 |
|------|------|
| `kunjie-admin-eval-v2.jsonl` | Eval v2 20 题 |
| `answer-prompt-v2.md` | 给 OpenClaw 的作答提示词 |
| `answers-v2.md` | OpenClaw 应写入的答卷 |
| `rubric-v2.md` | Codex 老师批改规则 |

## 题型

| 分类 | 数量 |
|------|------|
| expense | 10 |
| authority | 10 |

## 验证重点

- 是否主动调用正确 Skill。
- 报销四标签是否稳定。
- 越权拦截是否坚决。
- 付款、职级、发票、账号、用印等红线是否不再犯。

