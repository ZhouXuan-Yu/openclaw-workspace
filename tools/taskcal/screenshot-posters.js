const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 1440 });

  const htmlPath = path.resolve(__dirname, 'density-test.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });

  // Wait for fonts to load
  await page.waitForTimeout(2000);

  const posters = await page.$$('.poster.xhs');
  const outputFiles = [
    path.resolve(__dirname, 'output', 'test-kpi-tower.png'),
    path.resolve(__dirname, 'output', 'test-hbar.png'),
    path.resolve(__dirname, 'output', 'test-matrix.png'),
  ];

  for (let i = 0; i < posters.length; i++) {
    const poster = posters[i];
    const box = await poster.boundingBox();
    await poster.screenshot({
      path: outputFiles[i],
      type: 'png',
    });
    console.log(`Screenshot saved: ${outputFiles[i]} (${box.width}x${box.height})`);
  }

  await browser.close();
  console.log('Done.');
})();
