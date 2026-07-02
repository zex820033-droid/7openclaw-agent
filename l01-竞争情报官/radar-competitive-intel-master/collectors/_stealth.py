"""反检测隐身脚本 — 借鉴 AutoCLI crates/autocli-browser/src/stealth.rs

提供一组 JS 代码片段，在 Playwright 页面加载前注入，隐藏自动化痕迹。

用法:
    from app.services.benchmark.collectors._stealth import STEALTH_JS, PINIA_STORE_JS

    page.add_init_script(STEALTH_JS)
    # 对 Vue SPA 站点额外注入 Pinia 探测
    page.add_init_script(PINIA_STORE_JS)
"""

# ── 核心隐身脚本（借鉴 autocli stealth.rs）─────────────────

STEALTH_JS = """(() => {
  // 1. 移除 webdriver 属性
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
  });

  // 2. 伪造 plugins 长度（真实 Chrome 至少有 3 个插件）
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
  });

  // 3. 伪造 languages 数组
  Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'zh', 'en-US', 'en'],
  });

  // 4. 绕过 Permissions API 检测
  if (navigator.permissions) {
    var origQuery = navigator.permissions.query;
    navigator.permissions.query = function(params) {
      if (params.name === 'notifications') {
        return Promise.resolve({ state: Notification.permission });
      }
      return origQuery.call(navigator.permissions, params);
    };
  }

  // 5. 伪造 chrome.runtime
  if (window.chrome && !window.chrome.runtime) {
    window.chrome.runtime = {};
  }

  // 6. 修复 iframe contentWindow 属性描述符
  var origDesc = Object.getOwnPropertyDescriptor(
    HTMLIFrameElement.prototype, 'contentWindow'
  );
  if (origDesc) {
    Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
      get: function() {
        return origDesc.get.call(this);
      },
    });
  }

  // 7. 隐藏 Playwright 特有属性
  delete window.__playwright;
  delete window.__pw_manual;
  delete window.__PW_inspect;

  // 8. 伪造 chrome.app（部分站点检测是否存在）
  if (!window.chrome) { window.chrome = {}; }
  if (!window.chrome.app) {
    window.chrome.app = {
      isInstalled: false,
      InstallState: { DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' },
      RunningState: { CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' },
    };
  }

  // 9. 覆盖 headless 检测
  Object.defineProperty(navigator, 'platform', {
    get: function() { return 'Win32'; },
  });
  Object.defineProperty(navigator, 'hardwareConcurrency', {
    get: function() { return 8; },
  });
  Object.defineProperty(navigator, 'deviceMemory', {
    get: function() { return 8; },
  });
})()"""


# ── Performance API 网络请求捕获（借鉴 autocli explore.rs smart_api_discovery）─

NETWORK_CAPTURE_JS = """(() => {
  var entries = performance.getEntriesByType('resource');
  return entries
    .filter(function(e) {
      var lower = e.name.toLowerCase();
      return (lower.indexOf('/api/') !== -1 || lower.indexOf('/v1/') !== -1
        || lower.indexOf('/v2/') !== -1 || lower.indexOf('/v3/') !== -1
        || lower.indexOf('/x/') !== -1 || lower.indexOf('.json') !== -1
        || lower.indexOf('graphql') !== -1 || lower.indexOf('search') !== -1
        || lower.indexOf('feed') !== -1 || lower.indexOf('hot') !== -1
        || lower.indexOf('trending') !== -1 || lower.indexOf('list') !== -1)
        && lower.indexOf('.js') === -1 && lower.indexOf('.css') === -1
        && lower.indexOf('.png') === -1 && lower.indexOf('.jpg') === -1
        && lower.indexOf('.svg') === -1 && lower.indexOf('.woff') === -1;
    })
    .map(function(e) {
      return { url: e.name, method: 'GET', initiatorType: e.initiatorType };
    });
})()"""


# ── Pinia/Vuex Store 状态读取（借鉴 autocli explore.rs store_discover）─

PINIA_STORE_JS = """(() => {
  var stores = [];
  try {
    var app = document.querySelector('#app');
    if (!app || !app.__vue_app__) return stores;
    var gp = app.__vue_app__.config && app.__vue_app__.config.globalProperties;

    // Pinia stores
    var pinia = gp && gp.$pinia;
    if (pinia && pinia._s) {
      pinia._s.forEach(function(store, id) {
        var state = {};
        for (var k in store) {
          try {
            if (k.startsWith('$') || k.startsWith('_')) continue;
            if (typeof store[k] === 'function') continue;
            state[k] = store[k];
          } catch(e) {}
        }
        stores.push({ type: 'pinia', id: id, state: state });
      });
    }

    // Vuex stores
    var vuex = gp && gp.$store;
    if (vuex && vuex._modules && vuex._modules.root && vuex._modules.root._children) {
      var children = vuex._modules.root._children;
      for (var modName in children) {
        if (children.hasOwnProperty(modName)) {
          stores.push({
            type: 'vuex',
            id: modName,
            state: children[modName].state || {},
          });
        }
      }
    }
  } catch(e) {}
  return stores;
})()"""


# ── 框架检测（借鉴 autocli explore.rs framework_detect）─

FRAMEWORK_DETECT_JS = """(() => {
    var r = {};
    try {
        var app = document.querySelector('#app');
        r.vue3 = !!(app && app.__vue_app__);
        r.vue2 = !!(app && app.__vue__);
        r.react = !!(window.__REACT_DEVTOOLS_GLOBAL_HOOK__) || !!document.querySelector('[data-reactroot]');
        r.nextjs = !!(window.__NEXT_DATA__);
        r.nuxt = !!(window.__NUXT__);
        if (r.vue3 && app.__vue_app__) {
            var gp = app.__vue_app__.config && app.__vue_app__.config.globalProperties;
            r.pinia = !!(gp && gp.$pinia);
            r.vuex = !!(gp && gp.$store);
        }
    } catch(e) {}
    return r;
})()"""


# ── __INITIAL_STATE__ 提取（借鉴 autocli explore.rs probe_initial_state）─

INITIAL_STATE_JS = """(() => {
    var scripts = document.querySelectorAll('script:not([src])');
    for (var i = 0; i < scripts.length; i++) {
        var text = scripts[i].textContent || '';
        var idx = text.indexOf('__INITIAL_STATE__');
        if (idx !== -1) {
            try {
                return window.__INITIAL_STATE__;
            } catch(e) {}
        }
    }
    return null;
})()"""


# ── 交互式模糊测试（借鉴 autocli explore.rs interact_fuzz）─

INTERACT_FUZZ_JS = """(function() {
    var sleep = function(ms) {
        return new Promise(function(r) { setTimeout(r, ms); });
    };
    var clickables = [];
    var all = document.querySelectorAll(
        'button, [role="button"], [role="tab"], .tab, .btn, a[href="javascript:void(0)"]'
    );
    for (var i = 0; i < Math.min(all.length, 15); i++) {
        clickables.push(all[i]);
    }
    var clicked = 0;
    function next(idx) {
        if (idx >= clickables.length) return clicked;
        var el = clickables[idx];
        if (el.offsetParent === null) return next(idx + 1);
        try {
            el.dispatchEvent(new MouseEvent('click', {
                bubbles: true, cancelable: true, view: window
            }));
            clicked++;
        } catch(e) {}
        return sleep(300).then(function() { return next(idx + 1); });
    }
    return next(0);
})()"""
