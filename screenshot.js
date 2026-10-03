const { chromium } = require('playwright');
const path = require('path');

// Usage: node screenshot.js <htmlFile> <outName> [width]
const htmlFile = process.argv[2] || 'index.html';
const outName = process.argv[3] || 'current';
const width = parseInt(process.argv[4] || '1440', 10);

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const fileUrl = 'file://' + path.resolve(htmlFile).split(path.sep).join('/');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: `screenshots/${outName}.png`, fullPage: true });
  await browser.close();
  console.log('saved screenshots/' + outName + '.png');
})();
