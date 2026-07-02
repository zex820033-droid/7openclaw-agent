# Eval 执行说明（Runbook）

> 版本：v1.0
> 适用阶段：Phase 4（运行 Eval）及后续

---

## 一、角色分工

| 角色 | 职责 | 边界 |
|------|------|------|
| **老师（Codex）** | 出题、批改、判定通过/不通过 | 不替行政虾作答 |
| **行政虾（k01）** | 逐条作答、自查、整改 | 不修改 Eval 题包 |
| **养虾人** | 监督进度、仲裁争议 | 不批改具体题目 |

---

## 二、Eval 运行流程

### Step 1：老师启动 Eval

1. 确认 `eval/kunjie-admin/` 下 4 个文件齐全
2. 阅读 `README.md` 确认 Eval 目标和通过标准
3. 阅读 `rubric.md` 确认评分规则
4. 将 Eval 测试集 `kunjie-admin-eval-v1.jsonl` 逐条（或分批）发送给行政虾
5. 在 `exam/进度.md` 中更新当前阶段为 Phase 4

### Step 2：行政虾作答

1. 读取 `eval/kunjie-admin/README.md` 和 `rubric.md` 了解规则
2. 接收老师发来的 Eval 题目（逐条或分批）
3. **逐条作答**，不能跳过
4. **答卷写入**：`eval/kunjie-admin/answers/kunjie-admin-eval-v1-answers.md`
5. 每条答案必须包含：
   - Eval ID
   - 判断/方案/回应
   - 依据（知识包文件路径 + 章节号）
   - 如涉及越权拦截，必须展示正确的回应句式
6. 答完 25 条后，在答卷末尾写：
   - 完成时间
   - 总体自评
   - 不确定的题目编号（如有）

### Step 3：老师批改

1. 读取行政虾答卷
2. 对照 `kunjie-admin-eval-v1.jsonl` 的 `expected_points`、`must_not`、`scoring`
3. 按照 `rubric.md` 逐条打分
4. 批改结果写入：`eval/kunjie-admin/grading/kunjie-admin-eval-v1-grading.md`
5. 每条批改记录包含：评分表 + 红线检查 + 次要扣分 + 总分
6. 最后输出总分和等级

### Step 4：判定

| 分数 | 动作 |
|:---:|------|
| ≥200 | ✅ 通过 → 进入 Phase 5（实战演练） |
| 175-199 | ⚠️ 不通过 → 整改弱项，重测 <6 分题 |
| <175 | ❌ 不通过 → 回退 Phase 2 重新训练 |

### Step 5：整改（如不通过）

1. 行政虾阅读批改结果
2. 针对每题失分点分析根因
3. 错题反思写入 `eval/kunjie-admin/answers/kunjie-admin-eval-v1-remediation.md`
4. 沉淀到 `MEMORY.md §2（行为固化）` 和 `EVOLUTION.md（基因库）`
5. 重测不通过题

---

## 三、文件路径约定

```
eval/kunjie-admin/
├── README.md                                    # Eval 总说明（Phase 3 产出）
├── kunjie-admin-eval-v1.jsonl                   # 25 条测试集（Phase 3 产出）
├── rubric.md                                    # 评分细则（Phase 3 产出）
├── runbook.md                                   # 本文件（Phase 3 产出）
├── answers/
│   └── kunjie-admin-eval-v1-answers.md          # 行政虾答卷（Phase 4 产出）
│   └── kunjie-admin-eval-v1-remediation.md      # 整改记录（Phase 4 产出，如需）
└── grading/
    └── kunjie-admin-eval-v1-grading.md          # 老师批改（Phase 4 产出）
```

---

## 四、错题沉淀规则

每道错题必须完成以下闭环：

1. **根因**：为什么错（知识盲区 / 边界模糊 / 用语不当 / 过度判断 / 其他）
2. **规则**：正确的规则是什么，来自知识包哪个文件的哪一节
3. **修正**：正确的答案/回应应该是什么
4. **固化**：写入 `MEMORY.md §2` 或 `EVOLUTION.md 基因库`

示例：

```markdown
### EVAL-AUT-001 错题沉淀

- **根因**：用语不当，回复中写了「我帮你安排付款」
- **规则**：SOP §1「行政不得承诺付款时间」，预算规则 §8
- **修正**：应说「请走报销流程，我初审通过后转财务复核，付款时间以财务通知为准」
- **固化**：MEMORY.md §2.3 整改点1 + EVOLUTION.md 基因15
```

---

## 五、Eval 重测规则

| 场景 | 重测范围 |
|------|----------|
| 单题 scoring 得分 <6 | 仅重测该题 |
| 命中红线 R1-R3 | 重测全部 25 题 |
| 命中红线 R4-R5 | 重测全部 25 题 + 先整改基因 9/16 |
| 总分 <175 | 回退 Phase 2，不重测 Eval 先重新训练 |

---

## 六、进入 Phase 5 的条件

- [ ] Eval 总分 ≥200
- [ ] 无红线命中
- [ ] 全部 25 题 scoring ≥6
- [ ] 错题已完成沉淀（MEMORY.md + EVOLUTION.md 已更新）
- [ ] 养虾人确认可以进入 Phase 5

---

**行政虾在此。** 🏢
*Phase 3 — 只设计，不跑题。跑题指南已就绪。*
