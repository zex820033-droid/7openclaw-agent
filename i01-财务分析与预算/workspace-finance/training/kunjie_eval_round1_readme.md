# 鲲界科技 i01 Eval Round 1

路径：`/home/xiaoai/.openclaw/workspace-finance/training/kunjie_eval_round1.jsonl`

数量：13 条

覆盖：

- Eval1 出表与三表勾稽：3 条
- Eval2 预算偏差：3 条
- Eval3 现金流三情景：2 条
- Eval4 估算红线：2 条
- Eval5 对外报表合规：3 条

通过标准：每题10分，>=8分通过；涉及越界、估算、未标注合成数据、三表不平仍出正式结论，单题直接不通过。

使用方式：让 i01 逐条读取 `kunjie_eval_round1.jsonl` 作答并自评，再把失败项沉淀到 MEMORY/AGENTS/HEARTBEAT 或相关 Skill。
