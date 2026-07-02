// 10层浏览器隐身脚本
// 来源: Super-AIGC collectors/_stealth.py
// 用法: page.add_init_script(open('tools/stealth.js').read())

(() => {
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
}
