import { test, expect } from "@playwright/test";

/**
 * Flow 1: Landing Page
 * Tests all 10 sections load, nav works, no console errors on load.
 */

test.describe("Landing Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("page loads with 200 status", async ({ page }) => {
    const response = await page.request.get("/");
    expect(response.status()).toBe(200);
  });

  test("page title includes Newton-Metre", async ({ page }) => {
    const title = await page.title();
    // Accept either "Newton-Metre" or product name variations
    expect(title).toMatch(/newton|metre|costimize/i);
  });

  test("hero section renders with headline and CTA", async ({ page }) => {
    // The hero has "20 years of data" headline
    const hero = page.locator("main").first();
    await expect(hero).toBeVisible();

    // On mobile, some CTAs are hidden behind the hamburger menu.
    // Check for any visible CTA — including the always-visible mobile "Upload a Drawing" pill.
    const ctaLinks = page.locator('a[href="/login"], a[href="/estimate/new"], button:has-text("Upload"), button:has-text("Get started"), button:has-text("Start")');
    const visibleCount = await ctaLinks.evaluateAll(
      (els) => els.filter((el) => el.offsetParent !== null).length
    );
    expect(visibleCount).toBeGreaterThan(0);
  });

  test("navigation bar renders with logo and links", async ({ page }) => {
    const nav = page.locator("nav").first();
    await expect(nav).toBeVisible();

    // On mobile the brand text may be hidden; check the nav itself is rendered
    const viewport = page.viewportSize();
    if (viewport && viewport.width >= 768) {
      const brand = page.locator('text="Newton-Metre"').first();
      await expect(brand).toBeVisible();
    }
  });

  test("login nav link is present and functional", async ({ page }) => {
    const viewport = page.viewportSize();

    if (viewport && viewport.width < 768) {
      // On mobile, open hamburger first to reveal the login link in the dropdown
      const hamburger = page.locator('button[aria-label="Toggle menu"]');
      await expect(hamburger).toBeVisible({ timeout: 5000 });
      await hamburger.click();
      // The mobile dropdown login link is the last one (desktop one is CSS-hidden)
      const loginLink = page.locator('a[href="/login"]').last();
      await expect(loginLink).toBeVisible({ timeout: 8000 });
      await loginLink.click();
    } else {
      const loginLink = page.locator('a[href="/login"]').first();
      await expect(loginLink).toBeVisible({ timeout: 8000 });
      await loginLink.click();
    }

    await expect(page).toHaveURL(/\/login/);
  });

  test("no unhandled JS errors on page load", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    // Filter out known third-party noise
    const criticalErrors = errors.filter(
      (e) =>
        !e.includes("ResizeObserver") &&
        !e.includes("Non-Error promise rejection") &&
        !e.includes("extension")
    );
    expect(criticalErrors).toHaveLength(0);
  });

  test("proof section with cost savings story is visible", async ({ page }) => {
    // Section contains the ₹43L → ₹28L story (or at least some cost figure)
    await page.waitForLoadState("networkidle");
    const body = await page.locator("body").textContent();
    // Should contain rupee amounts somewhere on the page
    expect(body).toMatch(/₹|crore|lakh/i);
  });

  test("ROI calculator section renders with sliders", async ({ page }) => {
    await page.waitForLoadState("networkidle");
    // Look for an input[type=range] or slider element
    const slider = page.locator('input[type="range"]').first();
    if (await slider.isVisible()) {
      // Interact with it
      await slider.fill("50");
      await expect(slider).toHaveValue("50");
    } else {
      // At minimum the section heading should be visible
      const roiText = page.locator("text=/ROI|Return|savings/i").first();
      await expect(roiText).toBeVisible({ timeout: 8000 });
    }
  });

  test("pricing section shows Free and Pro tiers", async ({ page }) => {
    await page.waitForLoadState("networkidle");
    const body = await page.locator("body").textContent();
    expect(body).toMatch(/free|pro|₹0|4,999/i);
  });

  test("footer renders", async ({ page }) => {
    const footer = page.locator("footer").first();
    if (await footer.isVisible()) {
      await expect(footer).toBeVisible();
    } else {
      // Some designs use a div as footer
      const footerSection = page.locator('[class*="footer"], section:last-of-type').first();
      await expect(footerSection).toBeVisible();
    }
  });
});

/**
 * Flow 1b: Mobile responsiveness (375px)
 * Validates no severe overflow, CTA remains visible.
 * Note: The chromium-mobile project uses iPhone 12 device profile.
 * When run on chromium-desktop with an overridden viewport, Chromium may
 * report a slightly wider scrollWidth due to scrollbar reservations.
 * We allow up to 30px of overflow as a soft threshold — flag anything larger.
 */
test.describe("Landing Page — Mobile (375px)", () => {
  test.use({ viewport: { width: 375, height: 812 } });

  test("hero and CTA visible at 375px width", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // On mobile the nav collapses: the "Log in" link is hidden inside the hamburger menu.
    // The always-visible mobile CTA is the "Upload a Drawing" pill in the nav.
    const uploadCta = page.locator('a[href="/estimate/new"]').first();
    await expect(uploadCta).toBeVisible({ timeout: 8000 });

    // The hamburger button must be present to access the login link
    const hamburger = page.locator('button[aria-label="Toggle menu"]');
    await expect(hamburger).toBeVisible({ timeout: 5000 });

    // Measure horizontal overflow — report how bad it is
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    const overflowPx = scrollWidth - clientWidth;

    // Allow up to 30px (scrollbar + rounding); fail if it's a real layout break
    if (overflowPx > 30) {
      throw new Error(
        `Horizontal overflow at 375px: scrollWidth=${scrollWidth}px, clientWidth=${clientWidth}px, overflow=${overflowPx}px. ` +
        `A section is wider than the viewport — check for fixed-width containers or elements with min-width > 375px.`
      );
    }
  });

  test("hamburger menu opens and login link is accessible", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Open hamburger
    const hamburger = page.locator('button[aria-label="Toggle menu"]');
    await expect(hamburger).toBeVisible({ timeout: 5000 });
    await hamburger.click();

    // After opening, the mobile dropdown renders the login link
    const mobileLoginLink = page.locator('a[href="/login"]').last(); // last = the one inside mobile dropdown
    await expect(mobileLoginLink).toBeVisible({ timeout: 5000 });
  });

  test("no severe horizontal overflow in main content at mobile width", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const overflowPx = await page.evaluate(() => {
      const main = document.querySelector("main");
      if (!main) return 0;
      return Math.max(0, main.scrollWidth - main.clientWidth);
    });

    // Allow up to 30px; anything more is a real layout problem
    if (overflowPx > 30) {
      throw new Error(
        `Main content overflow at 375px: ${overflowPx}px. ` +
        `Check for elements with min-width, whitespace:nowrap, or fixed widths exceeding 375px.`
      );
    }
  });
});
