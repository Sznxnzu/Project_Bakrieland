const { chromium } = require('playwright');
const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(process.env.STREAMLIT_URL, { waitUntil: 'networkidle' });

  const screenshotPath = `screenshot_${Date.now()}.png`;
  await page.screenshot({ path: screenshotPath, fullPage: true });

  await browser.close();

  // Upload to Supabase
  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
  const fileBuffer = fs.readFileSync(screenshotPath);
  const { data, error } = await supabase.storage.from('screenshoots').upload(screenshotPath, fileBuffer, {
    contentType: 'image/png',
    upsert: true
  });

  if (error) {
    console.error("❌ Upload failed:", error.message);
    process.exit(1);
  }

  console.log("✅ Uploaded:", data);
})();