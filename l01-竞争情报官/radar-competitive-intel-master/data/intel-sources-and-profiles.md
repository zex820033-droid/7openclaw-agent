## 一、情报来源可信度数据库

| 来源 | 域名 | 初始可信度 | 备注 |
|------|------|-----------|------|
| 网信办 | cac.gov.cn | A(98%) | 官方权威 |
| 工信部 | miit.gov.cn | A(97%) | 官方权威 |
| 科技部 | most.gov.cn | A(97%) | 官方权威 |
| 中国信通院 | caict.ac.cn | A(95%) | 官方智库 |
| 36氪 | 36kr.com | A(92%) | 创投权威媒体 |
| 澎湃新闻 | thepaper.cn | A(91%) | 官方背景媒体 |
| TechCrunch | techcrunch.com | A(93%) | 全球科技权威 |
| Bloomberg | bloomberg.com | A(95%) | 全球财经权威 |
| 晚点LatePost | latepost.com | B(85%) | 深度行业媒体 |
| 虎嗅 | huxiu.com | B(80%) | 行业媒体 |
| 机器之心 | jiqizhixin.com | B(82%) | AI专业媒体 |
| 知乎 | zhihu.com | C(65%) | 需验证 |

## 二、竞品/关键企业情报档案

### 2.1 竞品档案 v2.0（28竞品 × 3类别 × 3级）

> 2026-06-22 更新：从17竞品扩展至28竞品，新增 Agent开发平台 + AIGC平台 两大类别
> ⚠️ 下表为参考文档。实时数据以 `data/competitors.json` 为准（T1:5 + T2:12 + T3:11 = 28）

**T1 核心竞品（5家，每日全维度监控）**：

| 公司 | 类别 | 关注维度 |
|------|------|---------|
| OpenAI | 大模型 + Agent平台 | GPT/Operator/Assistants API/GPTs/定价 |
| 字节跳动 | 大模型 + Agent + AIGC | 豆包/Coze扣子/即梦/火山引擎 |
| Anthropic | 大模型 + Agent平台 | Claude/Computer Use/MCP协议/企业战略 |
| 阿里巴巴 | 大模型 + Agent平台 | 通义千问/百炼Agent/钉钉AI |
| 百度 | 大模型 + Agent平台 | 文心一言/千帆AppBuilder/自动驾驶 |

**T2 关注竞品（10家，每日关键维度）**：

| 公司 | 类别 | 关注维度 |
|------|------|---------|
| 智谱AI | 大模型 + Agent | GLM/AutoGLM/融资 |
| 月之暗面 | 大模型 | Kimi/Agent/融资 |
| 深度求索 | 大模型 | 模型发布/开源/定价 |
| MiniMax | 大模型 | 产品矩阵/出海 |
| Dify | Agent平台 | 开源Agent编排/RAG/企业版 |
| LangChain | Agent平台 | LangGraph/LangSmith/LangGraph Cloud |
| 微软Copilot Studio | Agent平台 + 大模型 | Copilot Studio/AutoGen/Azure AI Agent |
| CrewAI | Agent平台 | 多Agent编排/企业版/开源 |
| 阶跃星辰 | 大模型 | 模型能力/企业客户 |
| 百川智能 | 大模型 | 医疗AI/融资 |

**T3 全球对标（11家，每周战略扫描）**：

| 公司 | 类别 | 关注维度 |
|------|------|---------|
| Google DeepMind | 大模型 + Agent | Gemini/Vertex AI Agent |
| Meta AI | 大模型 | LLaMA开源/AI产品 |
| Mistral AI | 大模型 + Agent | Le Chat/开源/欧洲市场 |
| xAI | 大模型 | Grok/X平台集成 |
| Cohere | 大模型 | 企业AI/RAG |
| Amazon Bedrock | Agent平台 + 大模型 | 多模型Agent/AWS生态 |
| AutoGPT | Agent平台 | 自主Agent框架/社区 |
| Midjourney | AIGC | 图像生成/产品迭代 |
| Runway | AIGC | 视频生成/Gen-4 |
| Stability AI | AIGC | Stable Diffusion/开源 |
| 可灵(快手) | AIGC | 视频生成/商业化 |
| Pika Labs | AIGC | 视频生成/产品创新 |

### 2.2 训练分析对象（2026-06-22 真实数据再训练）

> ⚠️ 非持续监控竞品。已通过GitHub API完成深度分析（21+独立curl调用），归档为知识库参考。

| 项目 | 类别 | 分析结论 | 数据来源 |
|------|------|---------|:-------:|
| **Palmier Pro** (`palmier-io/palmier-pro`) | macOS AI视频编辑器 | **活跃** 🟢 — YC S24, Swift, GPL-3.0, 6,429★, 52.8 commits/周, MCP协议集成, 5天5版本 | GitHub REST API |
| **OpenMontage** (`calesthio/OpenMontage`) | Agent视频制作系统 | **僵尸明星** 🔴 — 10,253★但45天停滞, Python, AGPL-3.0, 2贡献者, 0版本, 80未处理Issues | GitHub REST API |

**核心洞察**: Palmier Pro 的 MCP 集成策略 → Agent 与工具接口标准化趋势；GPL-3.0 vs AGPL-3.0 → 许可证选择直接影响商业化可行性

