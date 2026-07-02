// playwright-anti-detection.js
// 来源：Super-AIGC/collectors/playwright_session.py — 2026-06-27 提取
// 用途：Playwright page.add_init_script() 注入 → 伪造真实Chrome环境指纹
// 调用：page.add_init_script(path="data/playwright-anti-detection.js")

// ═══ 第一组：navigator 检测点 ═══

// 最关键 — 覆盖 webdriver 标记
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

// 覆盖 plugins 数量（真实Chrome有插件）
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
});

// 覆盖 languages
Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'zh', 'en'],
});

// 覆盖硬件信息（常见检测点）
Object.defineProperty(navigator, 'hardwareConcurrency', {
    get: () => 8,
});

Object.defineProperty(navigator, 'deviceMemory', {
    get: () => 8,
});

// ═══ 第二组：chrome 对象伪造 ═══

if (!window.chrome) window.chrome = {};

window.chrome.runtime = {
    id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    connect: () => {},
    sendMessage: () => {},
};

window.chrome.webstore = {
    install: function() {},
};

window.chrome.app = {
    isInstalled: false,
    InstallState: { DISABLED: 0, INSTALLED: 1, NOT_INSTALLED: 2 },
    RunningState: { CANNOT_RUN: 0, READY_TO_RUN: 1, RUNNING: 2 },
};

window.chrome.loadTimes = function() {
    return {
        requestTime: Date.now() / 1000,
        startLoadTime: Date.now() / 1000,
        commitLoadTime: Date.now() / 1000,
        finishLoadTime: Date.now() / 1000,
    };
};

window.chrome.csi = function() {
    return {
        onloadT: Date.now(),
        startE: Date.now(),
    };
};

// ═══ 第三组：permissions 拦截 ═══

const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (params) => (
    params.name === 'notifications'
        ? Promise.resolve({ state: 'denied' })
        : originalQuery(params)
);

// ═══ 第四组：WebGL 指纹伪造 ═══

const getParameterProxyHandler = {
    apply: function(target, thisArg, args) {
        const param = args[0];
        // UNMASKED_VENDOR_WEBGL
        if (param === 37445) return 'Google Inc. (NVIDIA)';
        // UNMASKED_RENDERER_WEBGL
        if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)';
        return target.apply(thisArg, args);
    }
};
try {
    const rawGetParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = new Proxy(rawGetParameter, getParameterProxyHandler);
} catch(e) {}
