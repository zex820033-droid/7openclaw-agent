// API端点自动发现
// 来源: Super-AIGC collectors/_stealth.py
// 用法: page.evaluate(open('tools/api_discovery.js').read())

(() => {
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
}
