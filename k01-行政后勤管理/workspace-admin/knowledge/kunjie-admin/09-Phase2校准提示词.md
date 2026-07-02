# Phase 2 行政虾资料校准提示词

把下面整段复制给 OpenClaw / k01 行政虾。

```text
你是 k01 行政虾。现在进入 Phase 2：资料一致性验收与索引校准阶段。

本阶段目标：
不是跑 Eval，不是继续扩写制度。
目标是验证 Phase 1 学到的资料是否准确，尤其是数量、路径、表格记录、规则边界是否与原始文件一致。

工作区路径：
/home/xiaoai/.openclaw/workspace-admin

知识包路径：
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin

请严格执行：

1. 重新读取以下文件，不要凭 Phase 1 记忆作答：
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/00-README.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/01-行政SOP.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/02-预算口径与报销规则.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/03-资产台账.csv
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/04-差旅平台-OA-报销系统账号.md
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/05-供应商清单.csv
/home/xiaoai/.openclaw/workspace-admin/knowledge/kunjie-admin/06-训练任务建议.md

2. 输出一份《Phase 2 资料校准报告》，必须包含：

一、文件存在性校验
- knowledge/kunjie-admin 下共有几个文件？
- 00-09 中哪些是数据资料，哪些是老师提示词/清单？

二、CSV 记录数校验
- 03-资产台账.csv 实际有多少条资产记录？
- 05-供应商清单.csv 实际有多少条供应商记录？
- 如果你之前报告过不同数字，必须明确承认并修正。

三、关键规则校验
请逐项给出原始文件依据路径：
- 采购金额分档
- 报销四标签
- 预算预警分档
- 资产盘点差异分级
- 账号安全禁止事项

四、索引是否正确
请回答：
- 报销问题查哪个文件？
- 资产问题查哪个文件？
- 供应商问题查哪个文件？
- 账号权限问题查哪个文件？
- 会议/访客/报修问题查哪个文件？

五、修正 MEMORY.md
如果发现 Phase 1 写入 MEMORY.md 的数字、数量、路径、表述有误，请修正。
尤其检查供应商数量，不允许把 20 家写成 19 家。

六、修正 EVOLUTION.md
如果发现 Phase 1 方法论中有“凭印象引用数量”的问题，请强化自评前回读机制。

七、阶段结论
只判断是否可以进入 Phase 3：Eval 测试集设计。
不要自行生成 Eval。

重要边界：
- 不要跑 R02/R03。
- 不要生成 Eval。
- 不要扩写知识包正文。
- 本阶段只做校准、纠错、索引确认。
- 所有数量结论必须来自重新读取原始文件。
```

