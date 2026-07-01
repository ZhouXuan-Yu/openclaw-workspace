const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1440 } });
  await p.goto('file:///C:/Users/ZhouXuan/.openclaw/workspace/output-daily/cards-06026.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(2000);
  const cards = await p.$$('.card');
  console.log('Found ' + cards.length + ' cards');
  for (let i = 0; i < cards.length; i++) {
    const fname = 'output-daily/assets/xhs-' + String(i+1).padStart(2,'0') + '.png';
    await cards[i].screenshot({ path: fname });
    console.log('  ' + fname);
  }
  await b.close();
})();
