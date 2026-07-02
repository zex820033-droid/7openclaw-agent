# 抖音采集 — 用户配置指南

> 本文档写给**最终使用者**。照着做，三步走完就能用。

---

## 提前看：三条路径选哪条

| 你要什么 | 走路径 | 需要做什么 | 耗时 |
|----------|:--:|------|:--:|
| 抖音热搜榜（"现在什么话题火"） | 路径 ① | 什么都不用做 | 0 分钟 |
| 按关键词搜索抖音内容、看某个用户主页 | 路径 ② | 给一条 Cookie 字符串 | 2 分钟 |
| 采集某用户的全部作品（视频+图文，完整字段） | 路径 ③ | 装 Playwright + 扫码登录一次 | 15 分钟 |

**不确定选哪条？** 先试 ①，不够再走 ②。

---

## 路径 ①：热搜榜（零门槛）

**无需登录、无需安装任何东西。** 对竞争情报说：

> "查抖音热搜"

即可。背后调用 `60s.viki.moe` 聚合 API（主）或抖音公开 API（兜底）。

---

## 路径 ②：搜索/用户信息（需要你的 Cookie）

### 你需要做什么

**在 Windows 电脑上的 Chrome 浏览器里操作：**

```
第1步：打开 Chrome，访问 https://www.douyin.com
第2步：确保已经登录（右上角能看到你的头像）—— 如果没登录，手机扫码登录
第3步：按 F12 打开开发者工具
第4步：点击 Console（控制台）标签
第5步：在底部输入框粘贴这行代码，按回车：
        document.cookie
第6步：复制输出的那一长串文字（类似下面这样），发给竞争情报：

        passport_csrf_token=xxx; passport_csrf_token_default=xxx; s_v_web_id=xxx; sessionid=xxx; ...

        ⚠️ 注意：
          - 整段复制，不要漏任何字符
          - 不要用微信/飞书直接发给别人——这里面包含你的登录凭证
          - 浏览器关闭后 Cookie 会变，届时需要重新获取
```

### 验证 Cookie 是否有效

发给我后，我会立刻测试一次搜索，确认能用。如果过期了会告诉你重新取。

### 有效期

一般 **24 小时**。如果发现搜索失败，重新执行第 1~6 步即可。

### 替代方案：自动提取（不需手动复制）

如果你的 WSL 能访问 Windows 的 Chrome 数据目录：

```bash
pip install rookiepy
python3 -c "
from tools.cookie_extractor import extract_all
c = extract_all('chrome')
print(c.get('douyin', {}).get('cookie_string', '❌ 无抖音Cookie'))
"
```

> 注意：执行前必须**关闭 Chrome 浏览器**，否则 rookiepy 读不到 Cookie 文件。

---

## 路径 ③：深度作品采集（需要 Playwright）

### 前提条件

| 条件 | 说明 |
|------|------|
| 操作系统 | Windows 10/11（有显示器）或 WSL2 + X11 |
| Python | 3.10+ |
| 磁盘空间 | ~1GB（Chromium 浏览器） |

### 第一步：安装依赖

```bash
pip install playwright playwright-stealth
playwright install chromium
```

### 第二步：扫码登录（仅首次）

```bash
cd 12_radar
python3 -c "
from collectors.douyin.works_collector import DouyinAdvancedCollector4

collector = DouyinAdvancedCollector4(headless=False)
ok = collector.login()
print('登录成功！' if ok else '登录失败/超时')
"
```

执行后会弹出一个 Chromium 浏览器窗口，自动打开 `douyin.com`：
1. 在窗口内用**手机抖音扫码**登录
2. 登录成功后采集器自动检测到 → 关闭窗口 → 输出"登录成功"
3. 登录态已自动保存到 `.browser-data/douyin/`，以后不用再登

### 第三步：采集作品

```bash
python3 -c "
from collectors.douyin.works_collector import DouyinAdvancedCollector4

collector = DouyinAdvancedCollector4(headless=True)  # 无头模式，后台静默跑

# 替换 douyin_id 为目标用户的抖音号
profile, videos = collector.fetch_user_works(
    douyin_id='要采集的抖音号',
    max_videos=20,  # 0=全部
)

print(f'用户: {profile.nickname} | 粉丝: {profile.fans_count:,} | 作品: {len(videos)}')
for v in videos[:5]:
    print(f'  [{v.video_type}] {v.title[:40]} | ❤️{v.like_count:,} 💬{v.comment_count:,}')
"
```

### 接口参数说明

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `douyin_id` | str | `""` | 抖音号（如 `"1049401268"`） |
| `max_videos` | int | `0` | 最多采集条数，`0`=全部 |
| `sec_uid` | str | `""` | 如果已知 sec_uid 可跳过搜索，加速采集 |
| `headless` | bool | `False` | `True`=后台无窗口，`False`=显示浏览器 |

### 返回字段一览

**用户信息（`profile`）：** nickname, douyin_id, fans_count, following_count, like_count_total, content_count, bio, avatar_url, ip_location, gender

**每条作品（`videos[i]`）：** content_id, title, like_count, comment_count, collect_count, share_count, play_count, duration, published_at, is_top, cover_url, video_download_url, video_download_urls, music_url, music_title, topics, video_type(视频/图文), image_urls, has_cart, cart_info, is_local_life, local_life_info

### 注意事项

1. **不要太快**：内置了自适应频率控制（4秒基础 + 随机抖动 + 翻页递增），不要试图去掉延迟——抖音风控很敏感
2. **不要并发**：同一时间只采集一个用户
3. **验证码**：如果触发验证码，采集器会停止并提示——等半小时再试
4. **登录态过期**：一般 7~30 天，过期后重新执行第二步扫码即可
5. **WSL 无 GUI**：需要 `export DISPLAY=:0` 或用 `channel="chrome"` 复用 Windows 原生 Chrome

---

## 常见问题

### Q: Cookie 里面有没有隐私风险？
A: Cookie 里包含你的抖音登录凭证。只通过私聊发给我（竞争情报 Agent），不要发到群聊。我仅用于 `web_fetch` 带 cookie 请求抖音 API，不会存储到任何外部服务。

### Q: 会不会被封号？
A: 路径 ① 零风险（纯公开 API）。路径 ② 低风险（低频搜索，模拟正常使用）。路径 ③ 有内置防风控策略（自适应延迟+指数退避+验证码检测），按正常频率使用不会触发封号。

### Q: Mac 能用吗？
A: 可以。所有脚本跨平台。`cookie_extractor.py` 支持 Chrome/Firefox/Edge/Brave/Opera 五种浏览器。

### Q: 手机端 Cookie 能用吗？
A: 手机抖音 APP 的 Cookie 和网页版（`douyin.com`）是两套体系。目前只支持网页版 Cookie。如果你需要手机 APP 的数据，可以通过路径 ③ 在电脑浏览器登录后采集——网页版和 APP 看的是同一批作品数据。

---

*最后更新：2026-06-30*
