"""API端点自动发现引擎 — 6策略: Performance/Refetch/.json/SSR/Pinia/搜索盲探
来源: Super-AIGC collectors/_api_discovery/ + _stealth.py (FRAMEWORK_DETECT_JS)
依赖: Playwright + playwright-stealth
用法: manifest = ApiDiscoverer(page_adapter).discover(url)
"""
import logging, time
from typing import Any

# ===== JS 代码片段 =====

SMART_API_DISCOVERY_JS = """(async () => {
    var entries = performance.getEntriesByType('resource');
    var apiUrls = entries
        .map(function(e) { return e.name; })
        .filter(function(url) {
            var lower = url.toLowerCase();
            return (lower.indexOf('/api/') !== -1 || lower.indexOf('/v1/') !== -1
                || lower.indexOf('/v2/') !== -1 || lower.indexOf('/v3/') !== -1
                || lower.indexOf('/x/') !== -1 || lower.indexOf('.json') !== -1
                || lower.indexOf('graphql') !== -1 || lower.indexOf('search') !== -1
                || lower.indexOf('feed') !== -1 || lower.indexOf('hot') !== -1
                || lower.indexOf('trending') !== -1 || lower.indexOf('list') !== -1)
                && lower.indexOf('.js') === -1 && lower.indexOf('.css') === -1
                && lower.indexOf('.png') === -1 && lower.indexOf('.jpg') === -1
                && lower.indexOf('.svg') === -1 && lower.indexOf('.woff') === -1;
        });

    var seen = {};
    var unique = [];
    apiUrls.forEach(function(url) {
        try {
            var u = new URL(url);
            var key = u.pathname;
            if (!seen[key]) {
                seen[key] = true;
                unique.push(url);
            }
        } catch(e) {}
    });

    var results = [];
    for (var i = 0; i < Math.min(unique.length, 20); i++) {
        try {
            var url = unique[i];
            var resp = await fetch(url, { credentials: 'include' });
            if (!resp.ok) continue;
            var ct = resp.headers.get('content-type') || '';
            if (ct.indexOf('json') === -1 && ct.indexOf('javascript') === -1) continue;
            var json = await resp.json();
            results.push({ url: url, status: resp.status, body: json });
        } catch(e) {}
    }
    return results;
})()"""

PROBE_JSON_SUFFIX_JS = """(async () => {
    var currentUrl = window.location.href;
    if (currentUrl.indexOf('/api/') !== -1 || currentUrl.indexOf('/x/') !== -1) return null;

    var jsonUrl = currentUrl.indexOf('?') !== -1
        ? currentUrl.replace('?', '.json?')
        : currentUrl.replace(/\\/$/, '') + '.json';

    try {
        var r = await fetch(jsonUrl, { credentials: 'include' });
        if (!r.ok) return null;
        var ct = r.headers.get('content-type') || '';
        if (ct.indexOf('json') === -1) return null;
        return await r.json();
    } catch(e) { return null; }
})()"""

PROBE_SEARCH_JS = """(async () => {
    var origin = window.location.origin;
    var candidates = [
        origin + '/search?q=test',
        origin + '/api/search?q=test',
        origin + '/api/search?keyword=test',
        origin + '/api/v1/search?q=test',
    ];
    var results = [];
    for (var i = 0; i < candidates.length; i++) {
        try {
            var resp = await fetch(candidates[i]);
            if (resp.ok) {
                var ct = resp.headers.get('content-type') || '';
                results.push({ url: candidates[i], ok: true, isJson: ct.indexOf('json') !== -1 });
            }
        } catch(e) {}
    }
    return results;
})()"""

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

class ApiDiscoverer:
    """智能 API 发现器 — 借鉴 AutoCLI explore.rs"""

    def __init__(self, page: PageAdapter, timeout: int = 15):
        self._page = page
        self._timeout = timeout

    def discover(self, url: str) -> dict[str, Any]:
        """执行全量 API 发现

        Returns:
            {
                "url": str,
                "framework": dict,
                "api_endpoints": list[dict],
                "initial_state": dict | None,
                "stores": list[dict],
            }
        """
        self._page.goto(url, timeout=self._timeout * 1000)
        time.sleep(3)

        manifest: dict[str, Any] = {
            "url": url,
            "framework": self.detect_framework(),
            "api_endpoints": [],
            "initial_state": None,
            "stores": [],
        }

        fw = manifest["framework"]

        # SSR __INITIAL_STATE__
        manifest["initial_state"] = self._extract_initial_state()

        # Pinia/Vuex Store（Vue SPA）
        if fw.get("pinia") or fw.get("vuex"):
            manifest["stores"] = self._read_stores()

        # Smart API Discovery（Performance API）
        endpoints = self._discover_api_endpoints()
        manifest["api_endpoints"] = endpoints

        # .json 后缀探测
        json_data = self._probe_json_suffix()
        if json_data:
            manifest["api_endpoints"].append({
                "url": url.rstrip("/") + ".json",
                "method": "GET",
                "source": ".json_suffix",
                "has_data": True,
            })

        # 搜索端点探测
        search_endpoints = self._probe_search()
        manifest["api_endpoints"].extend(search_endpoints)

        logger.info(
            "[api-discovery] %s: %d endpoints, framework=%s",
            url,
            len(manifest["api_endpoints"]),
            [k for k, v in fw.items() if v],
        )
        return manifest

    def detect_framework(self) -> dict[str, bool]:
        """检测前端框架"""
        try:
            return self._page.evaluate(FRAMEWORK_DETECT_JS)
        except Exception:
            return {}

    def _extract_initial_state(self) -> Any:
        """提取 SSR __INITIAL_STATE__"""
        try:
            return self._page.evaluate(INITIAL_STATE_JS)
        except Exception:
            return None

    def _read_stores(self) -> list[dict]:
        """读取 Pinia/Vuex stores"""
        try:
            return self._page.evaluate(PINIA_STORE_JS)
        except Exception:
            return []

    def _discover_api_endpoints(self) -> list[dict]:
        """通过 Performance API + 智能 refetch 发现端点"""
        try:
            return self._page.evaluate(SMART_API_DISCOVERY_JS)
        except Exception:
            return []

    def _probe_json_suffix(self) -> Any:
        """探测 .json 后缀"""
        try:
            return self._page.evaluate(PROBE_JSON_SUFFIX_JS)
        except Exception:
            return None

    def _probe_search(self) -> list[dict]:
        """探测搜索端点"""
        try:
            return self._page.evaluate(PROBE_SEARCH_JS)
        except Exception:
            return []
