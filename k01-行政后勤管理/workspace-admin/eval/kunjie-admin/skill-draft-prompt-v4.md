# Eval v4 后续：候选 Skill 草案生成提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入「Eval v4 后续：候选 Skill 草案生成」阶段。

唯一工作区：
/home/xiaoai/.openclaw/workspace-admin

本轮目标：
根据 Codex 老师的 v4 批改反馈，把 3 个候选新 Skill 写成草案。

重要限制：
1. 本轮只写草案，不创建正式 Skill 文件夹。
2. 不修改 `/home/xiaoai/.openclaw/workspace-admin/workspace/skills/` 下的任何正式 Skill。
3. 不修改根目录 `SKILL.md`。
4. 不自评，不打分，不说“本轮通过”。
5. 所有引用数字、库存、合同、资产状态，必须回读或命令验证，不凭记忆。

必须先读取：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/feedback-v4.md
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/answers-v4.md
/home/xiaoai/.openclaw/workspace-admin/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/expense-review-sop/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/authority-guardrail/SKILL.md

按需读取：
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/01-行政SOP.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/02-预算口径与报销规则.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/03-资产台账.csv
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/04-差旅平台-OA-报销系统账号.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/05-供应商清单.csv

输出文件：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/skill-drafts-v4.md

需要写 3 个候选 Skill 草案：

1. inventory-replenishment
   主题：库存扫描、办公用品领用、安全库存、补货建议、采购阈值。

2. supplier-risk-review
   主题：供应商合同到期、等级风险、SLA、续约/替换、回扣/舞弊衔接 authority-guardrail。

3. onboarding-offboarding-sop
   主题：入职工位/资产/门禁/权限准备，离职资产回收、账号关闭、异常处理。

每个 Skill 草案必须包含：

## <skill-name>

### 1. Description
一句话说明这个 Skill 解决什么问题，什么时候触发。

### 2. Trigger
列出 5-8 个典型触发语句或场景。

### 3. Inputs
列出必需输入字段和可选输入字段。

### 4. Source Files
列出需要读取的制度/台账文件。

### 5. Workflow
写成 5-8 步流程，必须可执行。

### 6. Output Format
给出标准输出模板。

### 7. Guardrails
写清楚不能做什么，哪些情况必须升级上报。

### 8. Ledger Updates
写清楚需要更新哪些台账字段。

### 9. Related Skills
说明和现有 `expense-review-sop`、`authority-guardrail` 何时联动。

### 10. Eval v5 Test Plan
每个 Skill 设计 5 道验证题，写出题目覆盖点，不要作答。

最后写《本轮执行总结》，必须包含：
- 草案写入路径
- 读取了哪些文件
- 调用了哪些工具或命令
- 哪些数字经过命令验证
- 没有修改哪些正式文件
```
