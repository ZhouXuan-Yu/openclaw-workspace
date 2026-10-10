const https = require('https');
function get(u) {
  return new Promise((res, rej) => {
    https.get(u, { headers: { 'User-Agent': 'Mozilla/5.0' } }, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(d));
    }).on('error', rej);
  });
}
(async () => {
  for (const since of ['daily', 'weekly']) {
    const html = await get('https://github.com/trending?since=' + since);
    const re = /<h2 class="h3 lh-condensed">\s*<a href="\/([^"]+)"/g;
    let m, names = [];
    while ((m = re.exec(html))) names.push(m[1]);
    console.log('== ' + since + ' (' + names.length + ') ==');
    console.log(names.join('\n'));
  }
})();
