# 🚨 Dify 1.15.0 版本发布报告

**检测时间**: 2026-06-26T18:31 CST  
**来源**: GitHub Releases API — `langgenius/dify`  
**Release ID**: 344699591 | **Tag**: 1.15.0 | **发布者**: @wylswz  
**发布时间**: 2026-06-25T13:16:14Z (UTC) / 2026-06-25 21:16 CST  
**距上版**: 37天 (v1.14.2 → v1.15.0)  
**发布类型**: **Minor** (1.14→1.15, 功能级大版)  
**URL**: https://github.com/langgenius/dify/releases/tag/1.15.0

---

## 一、变更内容

### 变更域分解

| 域 | 变更强度 | 关键PR/条目 | 信号强度 |
|------|:--:|------|:--:|
| **🔧 CLI工具** | 🔴 高 | `difyctl` — 终端驱动Dify工作流 (#37036, #37454) | **S1** |
| **🧠 CoT推理流** | 🔴 高 | Workflow/Chatflow/CLI 实时推理面板 (#37460, #37828) | **S1** |
| **👤 HITL表单增强** | 🟡 中 | 下拉选择、文件/多文件上传 (#36322) | **S2** |
| **🐢 长时模型支持** | 🟡 中 | 轮询机制支持视频/图像生成模型 (#37462) | **S2** |
| **📊 Excel图片提取** | 🟢 低 | 知识导入时提取内嵌图片 (#37104) | **S3** |
| **🛡️ 安全修复** | 🔴 高 | CVE-2026-41948 路径穿越修复 | **S1** |
| **🎨 UX/UI重构** | 🟡 中 | 着陆页重设计、快速导航、安全删除确认 (#37433, #37844) | **S2** |
| **🔌 插件区域镜像** | 🟡 中 | 自动检测PyPI镜像 (#750 plugin-daemon) | **S2** |
| **📈 可观测性** | 🟢 低 | Phoenix追踪Session ID、文档检索步骤 (#37056, #37283) | **S3** |
| **🐛 Bug修复** | 🟡 中 | SSRF/超时加固、向量库修复、会话管理重构 | **S2** |

### 关键环境变量变更 (19增2删1改)
- **新增重点**: `OPENAPI_CORS_ALLOW_ORIGINS`, `OPENAPI_ENABLED`, `SSRF_PROXY_ALLOW_PRIVATE_DOMAINS`, `ENABLE_OAUTH_BEARER`
- **删除**: `SSRF_REVERSE_PROXY_PORT`, `SSRF_SANDBOX_HOST`
- **修改**: `UV_CACHE_DIR` 路径调整

### ⚠️ 数据库迁移 (Ruby Required)
新增迁移包括: OAuth tokens, Credential visibility, HITL upload tables, **Category-scoped plugin auto-upgrade**, App stars. 必须运行 `flask backfill-plugin-auto-upgrade`。

---

## 二、影响范围

### 对OpenClaw的直接/间接影响

| 影响维度 | 评估 | 概率 |
|---------|------|:--:|
| **difyctl CLI** — Dify可通过命令行调用工作流，对标OpenClaw的CLI/API调用能力。Dify从此进入"无UI驱动"场景，与OpenClaw的Agent编排产生直接竞争 | 直接影响 | 75% |
| **CoT推理流** — Dify现在支持流式推理可视化，补齐了此前缺失的"思考过程"透明度。这使Dify在可解释性上缩小与OpenClaw的差距 | 间接影响 | 65% |
| **长时模型轮询** — 支持视频/图像生成模型，扩展了Dify在多媒体Agent场景的能力边界 | 间接影响 | 40% |
| **HITL表单增强** — 更丰富的人工介入能力，适用于审批/审核场景，这是Dify在企业市场的重要差异化 | 间接影响 | 55% |
| **安全加固** — CVE修复 + SSRF/超时加固显示Dify对安全性的投入加大 | 间接影响 | 50% |

### 竞争态势评估
Dify 1.15.0 是一次**战略级发布**。`difyctl` 和 `CoT推理流` 两项能力填补了Dify相对于OpenClaw的两个明显短板（CLI调用和推理透明度）。37天未发布后集中交付，说明Dify团队正在为v2.0做铺垫。

---

## 三、回滚预案/应对建议

| 级别 | 建议 | 预期效果 | 风险 |
|:--:|------|---------|------|
| **P1** | 技术架构立即评估 `difyctl` CLI设计，提取可对标改进点 | 保持CLI/API调用场景的竞争力 | 低 |
| **P1** | 产品设计关注CoT推理面板UX，对标OpenClaw的推理透明度展示 | 防止在"可解释性"维度被反超 | 低 |
| **P2** | 评估是否需要支持长时模型轮询（视频/图像生成场景） | 扩展多媒体Agent能力 | 中（需额外架构工作） |
| **P2** | 审视HITL策略 — Dify现在支持更丰富的表单，OpenClaw的审批链路需要对比评估 | 保持企业场景竞争力 | 低 |
| **P3** | 关注Dify环境变量新增的`OPENAPI_*`系列 — 暗示Dify在扩展API开放策略 | 监控趋势 | 极低 |

---

## 四、不确定性声明

- **已知**: difyctl作为CLI工具的首版为alpha质量，下载量仍低(<100次)
- **未知**: Dify 1.15.0 的实际部署率和bug回归情况
- **验证建议**: 1周后检查difyctl下载量增长 + GitHub Issues中1.15.0相关bug报告

---

**情报来源**: GitHub Releases API [直接抓取] — A级可信度  
**综合可信度**: 95% | **时效**: 有效截至 2026-07-02
