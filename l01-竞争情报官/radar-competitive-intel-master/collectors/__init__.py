"""采集器包 — 从 Super-AIGC/backend/app/services/benchmark/collectors 适配独立运行。

子包:
  - douyin/:  抖音采集（热搜 + 作品深度采集）
  - (more platforms coming)

共享模块:
  - page_adapter.py:      统一 Playwright/Selenium 页面接口
  - playwright_session.py: Playwright 内置 Chromium 会话管理
  - _utils.py:            工具函数（计数解析/频率控制/重试）
  - _stealth.py:          反检测隐身脚本
"""
