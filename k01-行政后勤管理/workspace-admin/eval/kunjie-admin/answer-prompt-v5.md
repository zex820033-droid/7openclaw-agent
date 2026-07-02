# 鲲界行政 Eval v5 作答提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入「鲲界行政 Eval v5：新增 Skill 验证 + 跨 Skill 协同」作答阶段。

唯一工作区：
/home/xiaoai/.openclaw/workspace-admin

本轮目标：
验证 3 个新增正式 Skill 是否可用，并检查它们和既有 Skill 的交叉触发。

题目文件：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/kunjie-admin-eval-v5.jsonl

答卷写入：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/answers-v5.md

必须先读取：
/home/xiaoai/.openclaw/workspace-admin/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/expense-review-sop/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/authority-guardrail/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/inventory-replenishment/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/supplier-risk-review/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/onboarding-offboarding-sop/SKILL.md

按需读取：
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin

重要限制：
1. 本轮只作答，不自评，不打分，不批改。
2. 不创建新 Skill，不修改任何 Skill 文件。
3. 不修改根目录 SKILL.md。
4. 必须把每题完整答案展示在 answers-v5.md。
5. 每题必须明确写出调用了哪些 Skill；如果题目要求调用某 Skill，必须调用。
6. 涉及数量、金额、日期、库存、合同到期、资产状态、供应商等级，必须命令验证；回读 CSV 不等于命令验证。
7. 不得承诺付款、不得跳审批、不得编造客户名单/发票/账号/真实联系人。

每题格式：

## <题目ID>

题目类型：
调用 Skill：
结论：
依据文件：
命令验证：
判断过程：
风险标签：
下一步动作：
不可做事项：
是否需要更新台账/记忆：
本题调用的工具/读取的文件：

答卷最后写《本轮执行总结》，包含：
- 答卷写入路径
- 共回答多少题
- 按 category 统计题数
- 每个 Skill 调用次数和题号
- 读取了哪些文件
- 调用了哪些工具或命令
- 哪些题触发了命令验证
- 本轮发现的 Skill 优化点，但不要修改 Skill
```
