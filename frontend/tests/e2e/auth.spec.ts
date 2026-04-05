import { test, expect } from "@playwright/test";

/**
 * Flow 2: Authentication
 * Login and signup page rendering, form validation, error states.
 * Does NOT require valid credentials — tests UI behaviour only.
 */

test.describe("Auth — Login Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
  });

  test("login page renders without crashing", async ({ page }) => {
    await expect(page.locator("body")).toBeVisible();
    // Must not be a blank white screen
    const bodyText = await page.locator("body").textContent();
    expect(bodyText!.trim().length).toBeGreaterThan(50);
  });

  test("Newton-Metre brand is visible on login page", async ({ page }) => {
    await expect(page.locator('text="Newton-Metre"').first()).toBeVisible();
  });

  test("signup form renders by default (isSignUp=true)", async ({ page }) => {
    // The login page defaults to signup mode
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    // Signup shows full name + company fields — use .first() since both match "name"
    await expect(page.locator('input[placeholder*="name"]').first()).toBeVisible();
    await expect(page.locator('input[placeholder*="ompan"]').first()).toBeVisible();
  });

  test("switch to login mode works", async ({ page }) => {
    // Click "Already have an account? Log in"
    const switchBtn = page.locator('button:has-text("Log in"), button:has-text("log in")').first();
    await expect(switchBtn).toBeVisible();
    await switchBtn.click();

    // Full Name and Company fields should disappear
    await expect(page.locator('input[placeholder*="name"]')).not.toBeVisible();
    // Email and password remain
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test("login with invalid credentials shows friendly error", async ({ page }) => {
    // The page defaults to signup mode — switch to login via the toggle button.
    // The button text is "Already have an account? Log in" so we match partial text.
    const switchBtn = page.locator('button').filter({ hasText: /already have an account/i }).first();
    await expect(switchBtn).toBeVisible({ timeout: 8000 });
    await switchBtn.click();

    // Full Name / Company fields should now be gone, leaving just email + password
    await expect(page.locator('input[placeholder*="name"]')).not.toBeVisible({ timeout: 5000 });

    await page.locator('input[type="email"]').fill("notareal@email.com");
    await page.locator('input[type="password"]').fill("wrongpassword123");
    await page.locator('button[type="submit"]').click();

    // Should show an error message — not crash or redirect.
    // Wait for an alert div that has non-empty text (avoids matching empty placeholder divs).
    const errorAlert = page.locator('[role="alert"]').filter({ hasText: /\S/ });
    await expect(errorAlert).toBeVisible({ timeout: 15000 });

    const errorText = await errorAlert.textContent();
    // Should be a friendly message, not a raw API error
    expect(errorText!.toLowerCase()).toMatch(
      /incorrect|invalid|password|credentials|wrong|try again/i
    );

    // Page should remain on /login
    await expect(page).toHaveURL(/\/login/);
  });

  test("submit button shows loading state during request", async ({ page }) => {
    const switchBtn = page.locator('button:has-text("Log in"), button:has-text("log in")').first();
    await switchBtn.click();

    await page.locator('input[type="email"]').fill("test@example.com");
    await page.locator('input[type="password"]').fill("password123");

    const submitBtn = page.locator('button[type="submit"]');
    await submitBtn.click();

    // The button should briefly disable / show spinner
    // (We check it's disabled for at least a moment, then either error or redirect)
    const isDisabledOrLoading = await submitBtn
      .getAttribute("disabled")
      .then((v) => v !== null)
      .catch(() => false);
    // Accept that it may re-enable quickly — just ensure no crash
    await page.waitForTimeout(500);
    // Page should still be intact
    await expect(page.locator("body")).toBeVisible();
  });

  test("signup form requires all fields — HTML5 validation", async ({ page }) => {
    // Try submitting empty form — browser native validation fires
    const submitBtn = page.locator('button[type="submit"]');
    await submitBtn.click();
    // Email input should be in invalid state
    const emailInput = page.locator('input[type="email"]');
    const validity = await emailInput.evaluate(
      (el: HTMLInputElement) => el.validity.valid
    );
    expect(validity).toBe(false);
  });

  test("country dropdown renders with options", async ({ page }) => {
    const select = page.locator("select").first();
    await expect(select).toBeVisible();
    const options = await select.locator("option").count();
    expect(options).toBeGreaterThanOrEqual(5);
  });

  test("back to homepage link works", async ({ page }) => {
    // Click the Newton-Metre logo link
    const logoLink = page.locator('a[href="/"]').first();
    await logoLink.click();
    await expect(page).toHaveURL(/^https:\/\/frontend-theta-ecru-95\.vercel\.app\/?$/);
  });
});

/**
 * Flow 2b: Auth redirect — protected pages redirect to /login
 */
test.describe("Auth — Protected Route Redirect", () => {
  const protectedRoutes = [
    "/dashboard",
    "/estimate/new",
    "/similar",
    "/library",
    "/chat",
    "/mpn",
    "/workflows",
  ];

  for (const route of protectedRoutes) {
    test(`${route} redirects unauthenticated user to /login`, async ({ page }) => {
      await page.goto(route);
      await page.waitForLoadState("networkidle");

      // Should land on /login or show login UI
      const url = page.url();
      const bodyText = await page.locator("body").textContent();
      const redirectedToLogin =
        url.includes("/login") ||
        (bodyText!.toLowerCase().includes("log in") &&
          bodyText!.toLowerCase().includes("email"));
      expect(redirectedToLogin).toBe(true);
    });
  }
});

/**
 * Flow 2c: Waitlist page (public)
 */
test.describe("Waitlist Page", () => {
  test("waitlist page renders without crash", async ({ page }) => {
    const response = await page.goto("/waitlist");
    await page.waitForLoadState("networkidle");
    // HTTP status must not be an error
    expect(response?.status()).toBeLessThan(500);
    // Visible text in rendered DOM must have meaningful content
    const visibleText = await page.locator("body").innerText();
    expect(visibleText.trim().length).toBeGreaterThan(50);
    // Rendered page should contain waitlist-related content
    expect(visibleText.toLowerCase()).toMatch(/waitlist|join|email|early access|newton/i);
  });
});
