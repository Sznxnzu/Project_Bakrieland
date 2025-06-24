const { chromium } = require('playwright');
const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');

(async () => {
  console.log("🚀 Launching Chromium...");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Catch page errors
  page.on('pageerror', (err) => {
    console.error("❌ Page error:", err);
  });

  // Log console messages from the page
  page.on('console', msg => {
    console.log("📣 Console:", msg.text());
  });

  const url = process.env.STREAMLIT_URL;
  if (!url) {
    console.error("❌ STREAMLIT_URL not defined");
    process.exit(1);
  }

  console.log("🌐 Navigating to:", url);
  try {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000); // Wait 3 seconds to ensure rendering
  } catch (err) {
    console.error("❌ Failed to load page:", err);
    await browser.close();
    process.exit(1);
  }

  const screenshotPath = `screenshot_${Date.now()}.png`;
  console.log("📸 Capturing screenshot:", screenshotPath);
  try {
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log("✅ Screenshot saved:", fs.existsSync(screenshotPath));
  } catch (err) {
    console.error("❌ Screenshot failed:", err);
    await browser.close();
    process.exit(1);
  }

  await browser.close();

  if (!fs.existsSync(screenshotPath)) {
    console.error("❌ Screenshot file not found after capture.");
    process.exit(1);
  }

  // Upload to Supabase
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_KEY;
  if (!supabaseUrl || !supabaseKey) {
    console.error("❌ Missing Supabase URL or KEY.");
    process.exit(1);
  }

  console.log("📤 Uploading to Supabase...");
  const supabase = createClient(supabaseUrl, supabaseKey);

  const fileBuffer = fs.readFileSync(screenshotPath);
  const { data, error } = await supabase
    .storage
    .from('screenshoots')
    .upload(screenshotPath, fileBuffer, {
      contentType: 'image/png',
      upsert: true
    });

  if (error) {
    console.error("❌ Upload failed:", error.message);
    process.exit(1);
  }

  console.log("✅ Uploaded successfully:");
  console.log(data);

})();
