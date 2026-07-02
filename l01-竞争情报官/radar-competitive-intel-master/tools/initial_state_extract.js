// SSR __INITIAL_STATE__ 提取
// 来源: Super-AIGC collectors/_stealth.py
// 用法: page.evaluate(open('tools/initial_state_extract.js').read())

(() => {
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
}
