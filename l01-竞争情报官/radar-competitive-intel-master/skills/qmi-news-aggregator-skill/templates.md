# 🇨🇳 国内大厂情报虾 菜单（v3.1）

> 21 个国内信源（13 个热榜 + 8 个科技/大厂），统一走 uapis.cn 公共 API + 3 个官方 RSS
> 回复 **序号** 或直接用自然语言描述需求。

---

## 🥇 国民级热榜（30 秒看完今天发生啥）

| # | 名称 | 命令 |
|---|---|---|
| 1 | 🔍 百度热搜 | `--source baidu_hot` |
| 2 | 💭 知乎热榜 | `--source zhihu_hot` |
| 3 | 📺 B 站热门 | `--source bilibili_hot` |
| 4 | 🔴 微博热搜 | `--source weibo` |
| 5 | 🎵 抖音热点 | `--source douyin_hot` |
| 6 | 📰 头条热榜 | `--source toutiao_hot` |
| 7 | 🦊 虎嗅 24h | `--source huxiu` |
| 8 | ⚡ 36 氪快讯 | `--source 36kr` |
| 9 | 💻 IT 之家 | `--source ithome` |
| 10 | ⚛️ 掘金热榜 | `--source juejin` |
| 11 | 📜 澎湃新闻 | `--source thepaper` |
| 12 | 🎯 少数派 | `--source sspai` |
| 13 | 📚 CSDN 热文 | `--source csdn` |
| 14 | 🔀 13 个热榜聚合 | `--source hot_rank` |

---

## 🏢 科技 / 大厂动态（深度读国内大厂在搞什么）

| # | 名称 | 命令 |
|---|---|---|
| 15 | 🍱 美团技术 | `--source meituan` (官方 RSS) |
| 16 | 🤖 量子位 | `--source qbitai` (官方 RSS) |
| 17 | 🧠 机器之心 | `--source jiqizhixin` (官方 RSS) |
| 18 | 💻 CSDN 热文 | `--source csdn` |
| 19 | ⚛️ 掘金热榜 | `--source juejin` |
| 20 | 🎯 少数派 | `--source sspai` |
| 21 | 💻 IT 之家 | `--source ithome` |
| 22 | ⚡ 36 氪 | `--source 36kr` |
| 23 | 📜 澎湃新闻 | `--source thepaper` |
| 24 | 🔀 8 个科技信源聚合 | `--source tech_blogs` |

---

## 📋 场景化早报（一键出整份日报）

| # | 名称 | 命令 |
|---|---|---|
| 25 | 🌅 综合早报（热榜+科技） | `daily_briefing.py --profile general --no-save` |
| 26 | 🤖 科技大厂早报 | `daily_briefing.py --profile tech --no-save` |
| 27 | 🍉 社交吃瓜早报 | `daily_briefing.py --profile social --no-save` |
| 28 | 🧠 AI 行业早报 | `daily_briefing.py --profile ai_focus --no-save` |
| 29 | 💰 商业资讯早报 | `daily_briefing.py --profile business --no-save` |
| 30 | ☕ 8 点精简早报 | `daily_briefing.py --profile morning --no-save` |

---

## 🆘 不会用？直接说人话

| 你说的话 | Agent 会帮你做 |
|---|---|
| "看下今天的热搜" | 跑 `hot_rank` |
| "大厂今天有啥新闻" | 跑 `tech_blogs` |
| "AI 行业今天发生了什么" | 跑 `ai_focus` 早报 |
| "给我一份完整早报" | 跑 `general` 早报 |
| "查一下 DeepSeek 相关的" | 关键词过滤 "DeepSeek" |
| "把今天的报告存下来" | 加 `--save` |
| "只要微博的内容" | `--source weibo` |
| "微博 + 知乎" | `--source weibo,zhihu_hot` |
| "美团今天的技术博客" | `--source meituan` |
| "程序员社区最近在讨论什么" | `--source csdn,juejin` |
| "AI 媒体怎么说" | `--source qbitai,jiqizhixin` |

---

## 🔀 自由组合

多个信源用逗号分隔：
```
weibo,zhihu_hot,baidu_hot
```
例如：*"给我看看百度 + 知乎 + 微博现在什么最火"* → Agent 自动执行 `--source baidu_hot,zhihu_hot,weibo`

---

**✨ 回复序号 (1-30) 或直接说你的需求即可**
