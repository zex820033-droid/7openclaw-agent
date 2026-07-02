# 📊 团队效能指标定义 · 竞争情报版 (v1.0)

> **定义时间**: 2026-06-23 17:44 CST  
> **适用范围**: Top 5 竞品团队效能分析  
> **数据来源**: GitHub REST API (公开仓库) / web_search (闭源仓库代理指标)  
> **方法论**: 改编自 DORA 指标 × 公开情报可采集性约束

---

## 一、指标体系

### 1.1 Cycle Time — 周期时间

**定义**: 从 PR(拉取请求)创建到 PR Merge(合并)的平均时间。

**竞争情报测量方式**:
```
进入: PR created_at    (GitHub API)
交付: PR merged_at     (GitHub API: pulls?state=closed)
Cycle Time = merged_at - created_at  (取中位数, 近30天滑动窗口)
```

**数据来源**: `GET /repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=30`

**信号解读**:
| Cycle Time | 解读 | 对OpenClaw的意义 |
|:----------:|------|----------------|
| < 8h | 极高工程效率，可能牺牲代码审查质量 | 竞品迭代快，需警惕功能差距扩大 |
| 8-48h | 健康水平，平衡效率与质量 | 对标基线 |
| 48h-1周 | 中等，可能有发布周期或审批瓶颈 | 可竞争的时间窗口 |
| > 1周 | 慢，可能存在工程阻塞或重型审批流程 | 竞品灵活度低，OpenClaw可加速超越 |

### 1.2 Lead Time — 前置时间

**定义**: 从需求提出(Feature Request Issue)到功能交付(PR Merge)的平均时间。

**竞争情报测量方式** (近似值):
```
Method A (Feature Issue → Merge):
  进入: Issue created_at  (label: "feature" | "enhancement")
  交付: 关联PR merged_at
  Lead Time A = linked_PR.merged_at - Issue.created_at

Method B (Release Timeline → Proxy):
  Lead Time B = 上一个 minor 版本发布时间 → 当前 minor 版本发布时间
  (适用于未公开发布 Feature Issue 的竞品)
```

**数据来源**: 
- `GET /repos/{owner}/{repo}/issues?labels=feature,enhancement&state=closed&per_page=30`
- Release 时间戳: `GET /repos/{owner}/{repo}/releases?per_page=10`

**信号解读**:
| Lead Time | 解读 |
|:---------:|------|
| < 2周 | 极致敏捷，Feature Factory 模式 |
| 2-6周 | 行业平均水平 |
| 6-12周 | 偏慢，可能有季度规划约束 |
| > 12周 | 重型流程，多数大企业模式 |

### 1.3 Throughput — 吞吐量

**定义**: 单位时间内交付的工作单元数量。

**竞争情报测量方式** (三个维度):
```
PR 吞吐量:    PRs merged / week        (近4周平均)
Release 吞吐量: Releases / month        (近3月平均)
Issue 解决率:   Issues closed / week    (近4周平均)
```

**数据来源**:
- `GET /repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=50` (统计近4周)
- `GET /repos/{owner}/{repo}/releases?per_page=20` (统计近3月)
- `GET /repos/{owner}/{repo}/issues?state=closed&per_page=50` (统计近4周)

**信号解读**:
| 指标 | 低 | 中 | 高 |
|:----:|:--:|:--:|:--:|
| PR 吞吐量 | < 20 PRs/周 | 20-80 PRs/周 | > 80 PRs/周 |
| Release 吞吐量 | < 2 版本/月 | 2-6 版本/月 | > 6 版本/月 |
| Issue 解决率 | < 50 个/周 | 50-200 个/周 | > 200 个/周 |

---

## 二、Top 5 竞品效能基线 (初始化)

| 排名 | 竞品 | GitHub | 预计PR/周 | 预计Release/月 | 备注 |
|:---:|------|:------:|:--------:|:-------------:|------|
| **1** | **Dify** | 公开 ✅ | ~60-100 | ~2-4 | 社区贡献活跃，PR量大 |
| **2** | **LangChain** | 公开 ✅ | ~80-150 | ~2-3 | 最大活跃社区 |
| **3** | **CrewAI** | 公开 ✅ | ~30-60 | ~1-2 | 规模较小但增长快 |
| **4** | **Cursor** | 闭源 ❌ | 不可直接测量 | ~1-2 (Changelog观测) | 用 web_fetch changelog 替代 |
| **5** | **GitHub Copilot** | 闭源 ❌ | 不可直接测量 | ~2-4 (MS发布节奏) | 用 Release Notes 替代 |

> ⚠️ 预计值为初步估算，首次扫描后将更新为精确值

---

## 三、Top 5 效能扫描 Cron 设计

### 扫描频率
| 层级 | 频率 | 竞品 | 说明 |
|:----:|:----:|------|------|
| 高频 | 每日 | Dify, LangChain, CrewAI | 开源仓库实时可见 |
| 低频 | 每周 | Cursor, Copilot | 闭源，依赖 Changelog/博客 |

### 触发方式
- 每日 18:00 (T1/T2/T5 管道完成之后)
- 产出 → `reports/team-efficiency-{date}.md`
- P1 触发条件: 
  - Cycle Time 翻倍或减半 (> 50% 变化)
  - PR 吞吐量骤降 > 30%
  - Release 节奏骤变 (月Release数变化 > 50%)

---

## 四、数据质量声明

| 指标 | 开源竞品 | 闭源竞品 |
|:----:|:--------:|:--------:|
| Cycle Time | 🟢 精确测量 (GitHub API) | 🟡 代理估算 (Changelog 间隙) |
| Lead Time | 🟡 近似值 (Feature Issue → PR关联可能不完整) | 🟠 粗糙估算 (版本间时间差) |
| Throughput | 🟢 精确 (PR计数) | 🟠 低精度 (用户报告/博客中估算) |

**底线**: 开源竞品(3/5)可获取高置信度工程效能数据；闭源竞品(2/5)仅能获取外部可见信号，置信度B级。

---

*竞争情报在此。* 🐦
