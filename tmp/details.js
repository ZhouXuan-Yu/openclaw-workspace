const https = require('https');
function get(u) {
  return new Promise((res, rej) => {
    https.get(u, { headers: { 'Accept': 'application/vnd.github+json', 'User-Agent': 'trend-bot' } }, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(d));
    }).on('error', rej);
  });
}
const repos = [
  'tester-army/e2e', 'mattpocock/skills', 'earthtojake/text-to-cad', 'boykopovar/AnyPS5',
  'pbakaus/impeccable', 'thedotmack/claude-mem', 'ayghri/i-have-adhd', 'morluto/rea',
  'deepseek-ai/DeepGEMM', 'msitarzewski/agency-agents', 'DuarteSantos8/openGym', 'cathrynlavery/diagram-design',
  'mvschwarz/openrig', 'heygen-com/hyperframes', 'cursor/plugins', 'NVIDIA/OpenShell',
  'VectifyAI/PageIndex', 'pablostanley/yoinks', 'HunxByts/GhostTrack', 'Anil-matcha/open-dots',
  'Panniantong/Agent-Reach', 'byoungd/up'
];
(async () => {
  for (const r of repos) {
    try {
      const j = JSON.parse(await get('https://api.github.com/repos/' + r));
      console.log(r + ' | *' + j.stargazers_count + ' | +' + j.forks_count + ' | ' + (j.language || '-') + ' | created ' + (j.created_at || '').slice(0, 10) + ' | pushed ' + (j.pushed_at || '').slice(0, 10));
      console.log('   ' + (j.description || '(no desc)'));
      console.log('   topics: ' + (j.topics || []).join(','));
    } catch (e) { console.log(r + ' | ERROR ' + e.message); }
  }
})();
