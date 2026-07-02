#!/usr/bin/env python3
"""
竞争情报增强版 Playwright Runner — Phase 1 产物
基于 Super-AIGC 开源项目的 STEALTH_JS + playwright-stealth + WebGL 欺骗
"""

from playwright.sync_api import sync_playwright
import json, sys, os, time

TOOLS = os.path.dirname(os.path.abspath(__file__))

def load_js(filename):
    with open(os.path.join(TOOLS, filename), 'r', encoding='utf-8') as f:
        return f.read()

STEALTH_JS = load_js('stealth.js')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

def search_platform(name, url, wait_ms=5000):
    """增强版平台搜索：stealth + stealth.js + WebGL 欺骗"""
    print(f'\n{"="*50}')
    print(f'🔍 {name}: {url}')
    
    result = {'platform': name, 'status': '???', 'items': []}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=UA,
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
        )
        page = context.new_page()
        
        try:
            # === 三层隐身 ===
            # Layer 1: playwright-stealth 包
            from playwright_stealth import Stealth
            Stealth().apply_stealth_sync(page)
            
            # Layer 2: 自定义 STEALTH_JS（10层反向检测覆盖）
            page.add_init_script(STEALTH_JS)
            
            # Layer 3: WebGL GPU 欺骗
            page.add_init_script("""
                const getParameterProxyHandler = {
                    apply: function(target, thisArg, args) {
                        const param = args[0];
                        if (param === 37445) return 'Google Inc. (NVIDIA)';
                        if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)';
                        return target.apply(thisArg, args);
                    }
                };
                try {
                    const raw = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = new Proxy(raw, getParameterProxyHandler);
                } catch(e) {}
            """)
            
            # === 导航 ===
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(wait_ms)
            
            # === 提取内容 ===
            body_text = page.inner_text('body')
            lines = [l.strip() for l in body_text.split('\n') if l.strip() and len(l.strip()) > 8]
            
            # 过滤平台UI噪声
            noise = ['登录', '注册', 'APP', '打开App', '扫码', '验证', '用户协议', 
                     '隐私政策', '营业执照', 'ICP', '公网安备', '网络文化经营',
                     '增值电信', '医疗器械', '药品信息', '举报', '版权所有',
                     'Copyright', 'All Rights', '我知道了', '立即登录',
                     'server error', '服务器出错', '刷新重试']
            
            clean = []
            for line in lines[:50]:
                is_noise = any(n in line for n in noise)
                if not is_noise and len(line) > 10:
                    clean.append(line)
            
            result['status'] = 'OK' if len(clean) > 5 else 'EMPTY'
            result['total_lines'] = len(lines)
            result['clean_lines'] = len(clean)
            result['items'] = clean[:25]
            
            print(f'  📊 总行:{len(lines)} | 有效行:{len(clean)} | 状态:{result["status"]}')
            for i, item in enumerate(clean[:8]):
                print(f'  {i+1}. {item[:120]}')
                
        except Exception as e:
            result['status'] = f'ERROR: {str(e)[:150]}'
            print(f'  ❌ {result["status"]}')
        finally:
            page.close()
            context.close()
            browser.close()
    
    return result

# ===== 执行四平台搜索 =====
results = {}

# 1. 知乎搜索
results['zhihu'] = search_platform(
    '知乎', 
    'https://www.zhihu.com/search?type=content&q=%E5%B7%A6%E5%8F%B3%E6%B8%B8%E6%88%8F',
    wait_ms=6000
)

# 2. 小红书搜索
results['xiaohongshu'] = search_platform(
    '小红书',
    'https://www.xiaohongshu.com/search_result?keyword=%E5%B7%A6%E5%8F%B3%E6%B8%B8%E6%88%8F&source=web_search_result_notes',
    wait_ms=6000
)

# 3. 快手搜索
results['kuaishou'] = search_platform(
    '快手',
    'https://www.kuaishou.com/search/video?searchKey=%E5%B7%A6%E5%8F%B3%E6%B8%B8%E6%88%8F',
    wait_ms=6000
)

# 4. 抖音搜索
results['douyin'] = search_platform(
    '抖音',
    'https://www.douyin.com/search/%E5%B7%A6%E5%8F%B3%E6%B8%B8%E6%88%8F?type=general',
    wait_ms=6000
)

# ===== 汇总 =====
print(f'\n{"="*60}')
print('📊 Phase 1 验证报告')
print(f'{"="*60}')
for platform, r in results.items():
    status_icon = '✅' if r['status'] == 'OK' else '❌' if 'ERROR' in r['status'] else '🟡'
    print(f'{status_icon} {platform}: {r["status"]} ({r["clean_lines"]}有效行/{r["total_lines"]}总行)')

success = sum(1 for r in results.values() if r['status'] == 'OK')
print(f'\n🏆 封锁率: {(4-success)}/4 → 目标 0/4')
print(f'💉 注入: playwright-stealth + STEALTH_JS (10层) + WebGL欺骗 (RTX 3060)')
