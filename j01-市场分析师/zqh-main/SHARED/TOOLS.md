# TOOLS：共享工具与环境说明

## 工作区

- 当前工作区：`C:\Users\123\Desktop\市场分析师`
- 角色目录：`agents/`
- 共享 Skill 库：`workspace/skills/`
- 参考资料：`references/`
- 长期记忆：`memory/`
- 治理模板：`governance/`
- 训练资料：`project1/`

## 文件操作原则

- 角色 7 件套只放在 `agents/<id>/`。
- Skill 正文只放在 `workspace/skills/<skill-name>/SKILL.md`。
- 参考资料只放在 `references/`，不在角色文件中复制大段内容。
- 旧版草稿归档到 `archive/v0-draft/`，不直接删除。

## 技能调用原则

- 角色内 `SKILL.md` 只做清单索引。
- 任务需要能力时，读取对应 Skill。
- 任务完成后，如果方法可复用，按 Work-to-Skill 机制沉淀。

## 治理工具

- 任务卡：`governance/task-card.md`
- 三证验真：`governance/three-evidence-check.md`
- 整改单：`governance/rework-order.md`
- 军功簿：`governance/merit-ledger.md`
- 周检：`governance/weekly-healthcheck.md`
- 回归测试：`governance/regression-tests.md`

