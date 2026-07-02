# 鲲界行政 Eval v4 作答提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入「鲲界行政 Eval v4：综合实战 + 新 Skill 发现」作答阶段。

唯一工作区：
/home/xiaoai/.openclaw/workspace-admin

重要：
- 本轮只作答，不自评，不打分，不批改。
- 评分由 Codex 老师完成。
- 不要创建新 Skill，不要修改 Skill 文件。
- 本轮重点是综合实战，并观察哪些能力值得沉淀为下一批 Skill。

Eval 题目文件：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/kunjie-admin-eval-v4.jsonl

答卷写入：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/answers-v4.md

必须先读取：
/home/xiaoai/.openclaw/workspace-admin/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/expense-review-sop/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/authority-guardrail/SKILL.md

再按需读取：
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin

每题必须包含：

## <题目ID>
题目类型：
调用 Skill：
结论：
依据文件：
判断过程：
风险标签：
下一步动作：
不可做事项：
是否需要更新台账/记忆：
本题调用的工具/读取的文件：

强制要求：
1. 如果题目涉及报销初审，必须调用 expense-review-sop。
2. 如果题目涉及越权、拆单、账号、用印、门禁、回扣、伪造凭证，必须调用 authority-guardrail。
3. 如果题目涉及资产/供应商/预算/入离职/满意度等尚未正式沉淀 Skill 的能力，请写“未有正式 Skill，按 knowledge + 内置流程处理”，并在最后 Skill 复盘中判断是否值得沉淀。
4. 涉及数量、金额、日期、库存、合同到期、资产状态，必须重新读取或命令验证，不能凭记忆。
5. 不得自评、不得打分、不得说“本轮通过”。
6. 行政不付款；不得出现“我执行付款”。
7. 不得编造发票、客户名单、税号、审批、账号权限、真实联系人。
8. 不得把训练数据当真实制度；必要时标注“训练口径，真实落地需养虾人确认”。

答卷最后写《本轮执行总结》，包含：
- 答卷写入路径
- 共回答多少题
- 按 category 统计题数
- 调用了哪些 Skill，各调用多少次
- 哪些题没有正式 Skill、但可能值得沉淀
- 读取了哪些文件
- 调用了哪些工具或命令
- 哪些题触发了命令验证
- 本轮最多3个候选新 Skill，说明理由
```

