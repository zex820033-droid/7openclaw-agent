# 参考资料目录（references/）

> **来源**：蓝血军团-最佳实践手册 v4.0 第 2.3 节
> **原则**：所有只读参考文档集中存放，绝不分散到各虾目录
> **用途**：每次被唤醒、每次需要构建新 Agent、每次不确定文件架构时**先读此目录**

---

## 📂 三层 references 结构

```
references/
├── 蓝血军团-最佳实践手册/   ← 架构锚点（每次唤醒必读）
├── silicon-life-handbook/    ← 八卷体系（方法论）
└── agi-super-team/          ← 开源实战（参考）
```

---

## 🎯 三层 references 的角色

| 层级 | 角色 | 何时读 |
|---|---|---|
| **蓝血军团-最佳实践手册** | **架构锚点** | **每次唤醒必读**——确认 7 件套结构、12 虾命名、6 门禁 |
| **silicon-life-handbook** | **方法论** | 训练时读——4 根问题、6 层漂移、3 证验真 |
| **agi-super-team** | **开源参考** | 实际场景参考——Work-to-Skill、5 派区分 |

---

## 🔗 当前文件状态

### 蓝血军团-最佳实践手册
- **路径**：`D:\硅基生命手册\蓝血军团-最佳实践手册.md`
- **关联目录**：`references/蓝血军团-最佳实践手册/`
- **核心内容**：12 虾命名+5 小队编制+7 件套标准+6 周训练+6 门禁+Work-to-Skill
- **状态**：✅ 已建入口文件

### silicon-life-handbook
- **路径**：`/mnt/d/硅基生命手册/silicon-life-handbook-main/`
- **关联目录**：`references/silicon-life-handbook/`
- **核心内容**：8 卷 50+ 文件（4 根问题+6 漂移+三证+OODA+自进化）
- **状态**：✅ 已建入口文件

### agi-super-team
- **路径**：开源项目
- **关联目录**：`references/agi-super-team/`
- **核心内容**：Work-to-Skill 机制、5 派区分、5 数据喂养
- **状态**：✅ 已建入口文件

---

## 📋 使用建议

### 场景 1：每次 session 启动
1. 读 `references/蓝血军团-最佳实践手册/README.md`（架构锚点）
2. 读 `MEMORY.md`（精选长期记忆）
3. 读 `memory/2026-06-22.md`（最新 daily log）
4. 读任务相关 7 件套

### 场景 2：训练新技能
1. 读 `references/silicon-life-handbook/00-跨卷核心原则.md`（方法论）
2. 读 `references/silicon-life-handbook/04-卷四-训练流程.md`（6 阶段）
3. 读 `references/agi-super-team/Work-to-Skill.md`（封装机制）

### 场景 3：诊断漂移
1. 读 `references/silicon-life-handbook/05-卷五-长期表现.md`（6 层漂移）
2. 读 `references/蓝血军团-最佳实践手册/README.md`（6 门禁）

---

## 🔧 维护规则

- 每次 session 启动先读 `references/蓝血军团-最佳实践手册/README.md`
- 每次新增 skill 后更新 `references/agi-super-team/`
- 每次漂移事件记录到 `references/silicon-life-handbook/`

---

**核心金句**：
> "每次被唤醒、每次需要构建新 Agent、每次不确定文件架构时，请先读此文件。"
