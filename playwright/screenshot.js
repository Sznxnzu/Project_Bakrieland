const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');

(async () => {
  const STREAMLIT_URL = process.env.STREAMLIT_URL;
  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SUPABASE_KEY = process.env.SUPABASE_KEY;

  if (!STREAMLIT_URL || !SUPABASE_URL || !SUPABASE_KEY) {
    console.error("❌ Missing one or more required environment variables.");
    process.exit(1);
  }

  console.log(`🌐 Launching Chromium to visit: ${STREAMLIT_URL}`);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log(`🗨️  PAGE LOG: ${msg.text()}`));
  page.on('pageerror', err => console.error(`🚨 PAGE ERROR: ${err}`));

  try {
    await page.goto(STREAMLIT_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000); // let dynamic content settle
  } catch (e) {
    console.error("❌ Failed to load Streamlit page:", e);
    await browser.close();
    process.exit(1);
  }

  const timestamp = Date.now();
  const filename = `screenshot_${timestamp}.png`;
  const filepath = path.join(process.cwd(), filename);

  console.log(`📸 Capturing screenshot to ${filepath}`);
  try {
    await page.screenshot({ path: filepath, fullPage: true });
  } catch (e) {
    console.error("❌ Screenshot capture failed:", e);
    await browser.close();
    process.exit(1);
  }

  await browser.close();

  const fileSizeKB = (fs.statSync(filepath).size / 1024).toFixed(2);
  console.log(`✅ Screenshot saved (${fileSizeKB} KB)`);

  // Uploading to Supabase
  const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
  const fileBuffer = fs.readFileSync(filepath);

  console.log("☁️ Uploading to Supabase...");
  const { data, error } = await supabase.storage
    .from('screenshoots')
    .upload(filename, fileBuffer, {
      contentType: 'image/png',
      upsert: true
    });

  if (error) {
    console.error("❌ Upload failed:", error.message);
    process.exit(1);
  }

  const { data: publicData, error: pubErr } = supabase
    .storage
    .from('screenshoots')
    .getPublicUrl(filename);

  if (pubErr) {
    console.error("⚠️ Could not get public URL:", pubErr.message);
  }

  console.log("\n✅✅✅ All Steps Completed Successfully!");
  console.log("📄 Final Report:");
  console.log(`  • Visited:       ${STREAMLIT_URL}`);
  console.log(`  • Screenshot:    ${filename}`);
  console.log(`  • File Size:     ${fileSizeKB} KB`);
  console.log(`  • Supabase URL:  ${SUPABASE_URL}`);
  console.log(`  • Uploaded to:   bucket 'screenshoots'`);
  console.log(`  • Supabase Path: ${data?.path || "(unknown)"}`);
  if (publicData?.publicUrl) {
    console.log(`  • Public URL:    ${publicData.publicUrl}`);
  }

  console.log("\n🚀 Done.\n");

})();
