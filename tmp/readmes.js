const https = require('https');
function get(u, raw) {
  return new Promise((res, rej) => {
    https.get(u, { headers: { 'User-Agent': 'trend-bot', 'Accept': raw ? 'application/vnd.github.raw' : 'application/vnd.github+json' } }, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(d));
    }).on('error', rej);
  });
}
const repos = ['mattpocock/skills', 'msitarzewski/agency-agents', 'thedotmack/claude-mem', 'Panniantong/Agent-Reach', 'NVIDIA/OpenShell', 'pbakaus/impeccable'];
(async () => {
  for (const r of repos) {
    try {
      const t = await get('https://raw.githubusercontent.com/' + r + '/HEAD/README.md', true);
      console.log('\n############ ' + r + ' ############');
      console.log(t.split('\n').slice(0, 55).join('\n'));
    } catch (e) { console.log(r + ' ERR ' + e.message); }
  }
})();
