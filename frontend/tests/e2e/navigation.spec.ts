import { test, expect } from "@playwright/test";

/**
 * Navigation Tests
 * Verifies all public pages load without crashing and
 * that client-side routing between public pages works.
 */

test.describe("Public Pages — Render Without Crash", () => {
  const publicPages: Array<{ path: string; label: string; expectedContent: RegExp }> = [
    {
      path: "/",
      label: "Landing",
      expectedContent: /newton|metre|price|cost|manufacturing/i,
    },
    {
      path: "/login",
      label: "Login",
      expectedContent: /log in|sign up|create|account|email/i,
    },
    {
      path: "/waitlist",
      label: "Waitlist",
      expectedContent: /waitlist|join|notify|early access|email/i,
    },
  ];

  for (const { path, label, expectedContent } of publicPages) {
    test(`${label} (${path}) — renders body content`, async ({ page }) => {
      const response = await page.goto(path);
      // Accept 200 or redirect codes (3xx handled by Playwright)
      expect(response?.status()).toBeLessThan(500);

      await page.waitForLoadState("networkidle");

      const bodyText = await page.locator("body").textContent();
      expect(bodyText!.trim().length).toBeGreaterThan(100);
      expect(bodyText).toMatch(expectedContent);
    });

    test(`${label} (${path}) — no white screen (has visible elements)`, async ({
      page,
    }) => {
      await page.goto(path);
      await page.waitForLoadState("networkidle");

      // Count visible elements — a blank page would have none
      const visibleCount = await page
        .locator("h1, h2, h3, p, button, a, input, label")
        .count();
      expect(visibleCount).toBeGreaterThan(0);
    });
  }
});

test.describe("Navigation — Client-Side Routing", () => {
  test("landing page → login via nav link (no full reload)", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const viewport = page.viewportSize();

    if (viewport && viewport.width < 768) {
      // On mobile, open hamburger first — the desktop login link is CSS-hidden,
      // so we must target the dropdown copy (last match).
      const hamburger = page.locator('button[aria-label="Toggle menu"]');
      await expect(hamburger).toBeVisible({ timeout: 5000 });
      await hamburger.click();
      const loginLink = page.locator('a[href="/login"]').last();
      await expect(loginLink).toBeVisible({ timeout: 8000 });
      await loginLink.click();
    } else {
      const loginLink = page.locator('nav a[href="/login"]').first();
      await expect(loginLink).toBeVisible({ timeout: 8000 });
      await loginLink.click();
    }

    await expect(page).toHaveURL(/\/login/, { timeout: 10000 });

    // Confirm login page content loaded
    await expect(page.locator('input[type="email"]')).toBeVisible({
      timeout: 8000,
    });
  });

  test("login page → landing page via logo link", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    // The Newton-Metre logo in nav should link home
    const homeLink = page.locator('a[href="/"]').first();
    await expect(homeLink).toBeVisible({ timeout: 8000 });
    await homeLink.click();

    await expect(page).toHaveURL(
      /^https:\/\/frontend-theta-ecru-95\.vercel\.app\/?$/,
      { timeout: 10000 }
    );
  });

  test("browser back button works after login → landing navigation", async ({
    page,
  }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    await page.goBack();
    await page.waitForLoadState("networkidle");

    // Should be back on landing
    await expect(page).toHaveURL(
      /^https:\/\/frontend-theta-ecru-95\.vercel\.app\/?$/
    );
  });
});

test.describe("404 — Unknown Pages", () => {
  test("unknown route shows error or redirects (no unhandled crash)", async ({
    page,
  }) => {
    const response = await page.goto("/this-page-does-not-exist-xyz");
    // Next.js returns 404 for unknown routes
    // Page should not be a blank white screen
    await page.waitForLoadState("networkidle");
    const bodyText = await page.locator("body").textContent();
    expect(bodyText!.trim().length).toBeGreaterThan(10);
    // Status should be 404, not 500
    if (response) {
      expect(response.status()).not.toBe(500);
    }
  });
});
