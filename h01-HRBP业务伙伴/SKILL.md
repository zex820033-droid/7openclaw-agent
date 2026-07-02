# 技能清单 — HRBP/业务伙伴 h01 · 🤝

> **模式**：轻量清单 | 按需加载 | 即插即用
> **存放路径**：`workspace/skills/<技能名>/`

---

## 🔴 P0 核心技能（每半年度/季度必用）

| 技能 | 路径 | 用途 | 触发条件 |
|------|------|------|----------|
| `talent-nine-box` | `skills/talent-nine-box/` | 人才盘点九宫格：数据收集→九宫格定位→校准会议→发展计划→汰换方案 | "人才盘点" / "九宫格" |
| `org-health-diagnosis` | `skills/org-health-diagnosis/` | 组织健康度诊断：架构/流程/人才/文化四维度扫描→根因分析→改进方案 | "组织诊断" / "组织健康" |
| `performance-review-sop` | `skills/performance-review-sop/` | 绩效管理全流程：目标设定→中期回顾→绩效评估→面谈→结果应用 | "绩效面谈" / "绩效考核" |

---

## 🟡 P1 高频技能（每月/按需使用）

| 技能 | 路径 | 用途 | 触发条件 |
|------|------|------|----------|
| `behavioral-interview` | `skills/behavioral-interview/` | 行为面试法：STAR模型→场景题库→评估维度→录用建议 | "面试" / "招聘评估" |
| `compensation-benchmarking` | `skills/compensation-benchmarking/` | 薪酬对标：市场数据采集→内部公平性分析→薪酬调整建议 | "薪酬对标" / "调薪" |
| `okr-coaching` | `skills/okr-coaching/` | OKR教练：目标共创→KR合理性校验→对齐检查→复盘引导 | "OKR" / "目标设定" |

---

## 🟢 P2 按需技能（年度/专项触发）

| 技能 | 路径 | 用途 | 触发条件 |
|------|------|------|----------|
| `succession-planning` | `skills/succession-planning/` | 继任计划：关键岗位识别→继任者评估→发展计划→备份方案 | "继任计划" / "关键岗位备份" |
| `culture-handbook` | `skills/culture-handbook/` | 文化手册：价值观行为化→落地机制设计→文化评估体系 | "文化手册" / "价值观落地" |

---

## 📦 技能加载规则

```
1. P0技能 → 启动时自动加载索引
2. P1技能 → 首次调用时加载 SKILL.md
3. P2技能 → 明确触发词出现时才加载
4. 加载方式 → read(<技能路径>/SKILL.md)
```

---

## 🔧 技能维护日志

| 日期 | 技能 | 操作 | 说明 |
|------|------|------|------|
| 2026-06-18 | 全部 | 初始化 | h01首次部署，建立技能清单框架 |

---

## 🔗 关联技能（来自其他 Agent）

| 来源 | 技能 | 用途 |
|------|------|------|
| a02 经营分析师 | `key-indicator-design` | 人效指标设计 → 辅助组织诊断 |
| k01 财务风控 | `budget-deviation-analysis` | 薪酬预算偏差分析 → 辅助薪酬对标 |

---

**🤝 HRBP在此。**
*人对了，组织就对了。*
