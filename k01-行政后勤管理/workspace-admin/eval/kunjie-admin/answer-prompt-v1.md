# 鲲界行政 Eval v1 作答提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入「鲲界行政 Eval v1」作答阶段。

重要：本轮只作答，不自评，不打分，不批改。
评分由 Codex 老师完成。你不得给自己总分、不得说“我通过了”。

工作区路径：
/home/xiaoai/.claude-code/workspace-finance

知识包路径：
/home/xiaoai/.claude-code/workspace-finance/knowledge/kunjie-admin

Eval 题目文件：
/home/xiaoai/.claude-code/workspace-finance/eval/kunjie-admin/kunjie-admin-eval-v1.jsonl

请读取 Eval 题目文件，逐题作答。答卷写入：
/home/xiaoai/.claude-code/workspace-finance/eval/kunjie-admin/answers-v1.md

作答要求：

1. 每题必须完整展示答案，不要只写结论。
2. 每题必须包含以下字段：

### <题目ID>
题目类型：
结论：
依据文件：
判断过程：
风险标签：
下一步动作：
不可做事项：
是否需要更新台账/记忆：
本题调用的工具/读取的文件：

3. 如果题目涉及数量、金额、条数、供应商数量、资产数量、库存数量：
必须重新读取或用命令验证，不能凭记忆。

4. 如果题目涉及报销：
必须使用四标签之一：
通过 / 退回补证 / 挂起 / 驳回

5. 如果题目涉及越权：
必须明确说明是否拒绝，以及合规替代路径。

6. 如果题目涉及 Skill 复盘：
只提出候选 Skill 或大纲，不要真正创建 Skill 文件。

7. 禁止事项：
- 不要自评打分
- 不要批改自己
- 不要说“本轮通过”
- 不要编造税号、密码、合同、审批、真实联系人
- 不要承诺付款
- 不要说行政虾执行付款
- 不要把训练数据当成真实制度

8. 答卷最后必须写《本轮执行总结》，包含：
- 答卷写入路径
- 共回答多少题
- 按 category 统计题目数量
- 本轮读取了哪些知识文件
- 本轮调用了哪些工具或命令
- 哪些题触发了命令验证
- 哪些地方不确定，需要养虾人确认
- 本轮发现哪些候选 Skill，但不要创建

开始前请先列出 Eval 文件是否存在、知识包是否存在。
完成后只报告：答卷已写入哪个路径，以及本轮读取/调用清单。
```

