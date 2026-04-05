import { test as setup, expect } from "@playwright/test";
import path from "path";

/**
 * One-time auth setup — logs in once and saves browser state.
 * All authenticated tests reuse this state instead of logging in per-test,
 * which prevents Supabase rate-limiting from killing the test suite.
 */

export const AUTH_FILE = path.join(__dirname, ".auth/user.json");

const TEST_EMAIL = process.env.TEST_USER_EMAIL ?? "";
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD ?? "";

setup("authenticate", async ({ page }) => {
  if (!TEST_EMAIL || !TEST_PASSWORD) {
    // Nothing to set up — authenticated tests will skip themselves
    return;
  }

  await page.goto("/login");
  await page.waitForLoadState("networkidle");

  // Switch to login mode if the form defaults to signup
  const switchBtn = page
    .locator('button:has-text("Log in"), button:has-text("log in")')
    .first();
  if (await switchBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await switchBtn.click();
  }

  await page.locator('input[type="email"]').fill(TEST_EMAIL);
  await page.locator('input[type="password"]').fill(TEST_PASSWORD);
  await page.locator('button[type="submit"]').click();

  // Wait for successful redirect to any authenticated page
  await page.waitForURL(/\/dashboard|\/estimate|\/similar|\/library/, {
    timeout: 15000,
  });

  // Save cookies + localStorage so all authenticated tests reuse this session
  await page.context().storageState({ path: AUTH_FILE });
});
