// Vue Pinia/Vuex Store状态提取
// 来源: Super-AIGC collectors/_stealth.py
// 用法: page.evaluate(open('tools/pinia_extract.js').read())

(() => {
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
}
