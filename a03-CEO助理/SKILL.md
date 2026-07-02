# 技能清单 — CEO助理 a03 · 📋

> **模式**：轻量清单 | 按需加载 | 即插即用
> **存放路径**：`workspace/skills/<技能名>/`
> **更新时间**：2026-06-22 | 5 个专属 skill 已落地 ✅

---

## 🔴 P0 核心技能（已安装 ✅）

| 技能 | 路径 | 用途 | 触发条件 |
|------|------|------|----------|
| `daily-briefing` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/daily-briefing/` | 每日简报：日程+待办+速报+阻塞项 | "早上好" / "今天有什么" / 每日自动 |
| `task-prioritization` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/task-prioritization/` | 任务优先级排序：4级逻辑+冲突处理 | "排优先级" / "先做什么" |
| `meeting-notes` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/meeting-notes/` | 会议纪要：决定+行动项+讨论要点 | "做会议纪要" / 会后整理 |
| `task-supervisor` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/task-supervisor/` | 任务监工：巡检虾群执行状态 | 定时巡检 / "检查进度" |
| `summarize` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/summarize/` | 摘要生成：长文→一句话/要点/详细 | "帮我总结" / "太长给摘要" |

---

## 🤖 通用技能（已安装 ✅）

| 技能 | 路径 | 用途 |
|------|------|------|
| `first-principles-thinking` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/first-principles-thinking/` | 第一性原理思考 |
| `humanize-zh` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/humanize-zh/` | 去AI味润色 |
| `self-reflection` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/self-reflection/` | 自我复盘 |
| `memory-hygiene` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/memory-hygiene/` | 记忆清理 |
| `planning-with-files` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/planning-with-files/` | 文件驱动规划 |
| `context-compression` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/context-compression/` | 上下文压缩 |

---

## 🟠 P1 扩展技能（已安装 ✅）

| 技能 | 路径 | 用途 | 触发条件 |
|------|------|------|----------|
| `agent-team-orchestration` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/agent-team-orchestration/` | 多 Agent 编排：任务路由/生命周期/handoff/质量门 | 分发复杂任务 / 多虾协作 |
| `team-coordinator` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/team-coordinator/` | 团队协调：拆解→匹配 Agent→并行→汇总审核 | 跨虾任务 / 资源协调 |
| `agent-task-confirm` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/agent-task-confirm/` | 任务确认：验证分发后是否被接收+执行 | sessions_send 后 / 任务无响应 |
| `team-daily-report` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/team-daily-report/` | 日报汇总：agent/cron/skill 进展+关键事件 | 每日 18:00 / "今日汇总" |
| `verification-before-completion` | `.openclaw/workspace/十二虾/a03-CEO助理/skills/verification-before-completion/` | 完成前验证：执行验证命令+确认产出后才宣告完成 | 任务闭环 / 提交产出前 |

---

## 🟡 待建专属 skill

| 技能 | 用途 |
|------|------|
| `blocker-escalation` | 阻塞升级上呈 |
| `schedule-optimizer` | 日程优化 |
| `cross-dept-coordination` | 跨部门协调 |
| `weekly-integration-report` | 周度整合汇报 |
| `stakeholder-communication` | 干系人沟通 |

---

## 📦 技能加载规则

```
1. 已安装 skill → 触发条件匹配时自动加载 SKILL.md
2. 待建 skill → 用通用能力临时替代
3. 加载方式 → read(workspace/skills/<技能名>/SKILL.md)
```

---

## 🔧 技能维护日志

| 日期 | 技能 | 操作 | 说明 |
|------|------|------|------|
| 2026-06-22 | 5 个 P1 skill | 安装 | 从 AGI Super Team 参考库：agent-team-orchestration / team-coordinator / agent-task-confirm / team-daily-report / verification-before-completion |
| 2026-06-18 | 全部 | 初始化 | a03首次部署，建立技能清单框架 |

---

**📋 CEO助理在此。**
