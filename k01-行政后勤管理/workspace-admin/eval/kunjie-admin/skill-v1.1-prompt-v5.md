# Eval v5 后续：新增 Skill v1.1 优化草案提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入「Eval v5 后续：新增 Skill v1.1 优化草案」阶段。

唯一工作区：
/home/xiaoai/.openclaw/workspace-admin

本轮目标：
根据 Codex 老师的 v5 批改反馈，为 3 个新增 Skill 生成 v1.1 优化草案。

重要限制：
1. 本轮只写优化草案，不修改正式 Skill 文件。
2. 不修改 /home/xiaoai/.openclaw/workspace-admin/workspace/skills/ 下任何文件。
3. 不修改根目录 SKILL.md。
4. 不自评，不打分。

必须读取：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/feedback-v5.md
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/answers-v5.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/inventory-replenishment/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/supplier-risk-review/SKILL.md
/home/xiaoai/.openclaw/workspace-admin/workspace/skills/onboarding-offboarding-sop/SKILL.md

输出文件：
/home/xiaoai/.openclaw/workspace-admin/eval/kunjie-admin/skill-v1.1-drafts-v5.md

请分别为以下 3 个 Skill 写 v1.1 优化草案：

1. inventory-replenishment
   必须补：
   - 消耗异常分析子流程
   - 安全库存数据源优先级
   - 安防耗材补货上限规则
   - 命令验证结果标准格式

2. supplier-risk-review
   必须补：
   - SLA 量化整改标准
   - 供应商替换触发条件表
   - 月度供应商风险报告模板
   - 回扣/风控状态下供应商等级不得擅改的强化句式

3. onboarding-offboarding-sop
   必须补：
   - 入职资产不足处理分支
   - T+7 入职回访清单
   - 候选人接待 vs 正式入职边界
   - 权限开通“确认后开通”句式
   - 统计题口径：总题数 = 命令验证题 + 非命令验证实操题 + 复盘/统计题

每个 Skill 的草案格式：

## <skill-name> v1.1 草案

### 1. 修改目标
### 2. 需要新增到 SKILL.md 的内容
### 3. 建议替换的旧表述
### 4. 新增 Guardrails
### 5. 新增 Eval v6 验证题建议（3-5题）

最后写《本轮执行总结》，包含：
- 草案写入路径
- 读取了哪些文件
- 没有修改哪些正式文件
- 哪些 v5 错点被吸收进草案
```
