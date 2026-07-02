# 鲲界行政 Eval v1

## 目的

验证 k01 行政虾是否具备以下能力：

- 报销合规初审
- 差旅审批与预订方案
- 资产台账读取与生命周期判断
- 供应商与合同风险识别
- 越权请求拦截
- 员工自助指引
- Eval 后 Skill 沉淀反思

## 文件

| 文件 | 用途 |
|------|------|
| `kunjie-admin-eval-v1.jsonl` | 31 条 Eval 题目 |
| `answer-prompt-v1.md` | 给 OpenClaw 的作答提示词 |
| `answers-v1.md` | OpenClaw 作答后应生成的答卷 |
| `rubric-v1.md` | Codex 老师评分规则 |

## 分类

| 分类 | 数量 |
|------|------|
| expense | 7 |
| travel | 5 |
| asset | 5 |
| supplier | 4 |
| authority | 5 |
| self_help | 3 |
| skill_review | 2 |

## 训练纪律

- OpenClaw 只作答，不自评。
- Codex 老师负责批改和打分。
- 每轮 Eval 后判断是否沉淀 Skill。
- 只有高频、固定步骤、可复用的能力才沉淀 Skill。
