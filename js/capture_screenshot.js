// const puppeteer = require('puppeteer');

// (async () => {
//   const browser = await puppeteer.launch();
//   const page = await browser.newPage();
//   await page.goto('file:///Users/shota/programs/rand/Hackathon/Hackathon_vol.10/html/deck_map.html');
//   await page.waitForSelector('canvas');  // canvas要素の存在を待機

//   // 2秒待機
//   await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 2000)));

//   // スクリーンショットを撮る
//   await page.screenshot({ path: '/Users/shota/programs/rand/Hackathon/Hackathon_vol.10/js/pic/deck_map_screenshot.png' });
//   await browser.close();
// })();

const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  
  for (let i = 0; i <= 100; i++) {
    const filePath = `file:///Users/shota/programs/rand/Hackathon/Hackathon_vol.10/html/deck_map_${i}.html`;
    const screenshotPath = `/Users/shota/programs/rand/Hackathon/Hackathon_vol.10/js/picv4/deck_map_${i}_screenshot.png`;

    await page.goto(filePath);
    await page.waitForSelector('canvas');  // canvas要素の存在を待機

    // 2秒待機
    await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 2000)));

    // スクリーンショットを撮る
    await page.screenshot({ path: screenshotPath });
    console.log(`Screenshot saved to ${screenshotPath}`);
  }

  await browser.close();
})();
