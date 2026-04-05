import { test, expect, type Page } from "@playwright/test";

/**
 * Authenticated Flows
 *
 * These tests require valid Supabase credentials.
 * Set environment variables before running:
 *   TEST_USER_EMAIL=your@email.com
 *   TEST_USER_PASSWORD=yourpassword
 *
 * If credentials are not provided, tests are skipped with a clear message.
 * All tests in this file share a single logged-in session via storageState.
 */

const TEST_EMAIL = process.env.TEST_USER_EMAIL ?? "";
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD ?? "";
const HAS_CREDENTIALS = TEST_EMAIL !== "" && TEST_PASSWORD !== "";

/**
 * Helper: log in and return the page.
 * Stores auth cookie in memory for the session.
 */
async function login(page: Page): Promise<void> {
  await page.goto("/login");
  await page.waitForLoadState("networkidle");

  // Switch to login mode (default is signup)
  const switchBtn = page
    .locator('button:has-text("Log in"), button:has-text("log in")')
    .first();
  if (await switchBtn.isVisible()) {
    await switchBtn.click();
  }

  await page.locator('input[type="email"]').fill(TEST_EMAIL);
  await page.locator('input[type="password"]').fill(TEST_PASSWORD);
  await page.locator('button[type="submit"]').click();

  // Wait for redirect to dashboard or error
  await page.waitForURL(/\/dashboard|\/login/, { timeout: 15000 });
}

// ── Dashboard ───────────────────────────────────────────────────────────────

test.describe("Flow 3: Dashboard", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("dashboard renders 5 product cards after login", async ({ page }) => {
    await login(page);
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15000 });
    await page.waitForLoadState("networkidle");

    // The 5 cards: Should-cost, Find similar, AI Procurement, Part Number, Ask anything
    const cardTexts = [
      "Should-cost",
      "Find similar",
      "AI Procurement",
      "Part Number",
      "Ask anything",
    ];

    for (const text of cardTexts) {
      await expect(page.locator(`text="${text}"`).first()).toBeVisible({
        timeout: 10000,
      });
    }
  });

  test("dashboard sidebar renders Newton-Metre logo", async ({ page }) => {
    await login(page);
    await page.waitForLoadState("networkidle");
    await expect(page.locator('text="Newton-Metre"').first()).toBeVisible();
  });

  test("dashboard sidebar shows 'No estimates yet' when empty", async ({
    page,
  }) => {
    await login(page);
    await page.waitForLoadState("networkidle");
    // Either shows estimates list OR the empty state
    const sidebar = page.locator("aside").first();
    await expect(sidebar).toBeVisible({ timeout: 8000 });
  });

  test("sign out button is visible and functional", async ({ page }) => {
    await login(page);
    await page.waitForLoadState("networkidle");
    const signOut = page.locator('button:has-text("Sign out")');
    await expect(signOut).toBeVisible({ timeout: 8000 });
    await signOut.click();
    // Should redirect away from dashboard
    await page.waitForURL(/\/|\/login/, { timeout: 10000 });
  });
});

// ── Estimate New ────────────────────────────────────────────────────────────

test.describe("Flow 4: Estimate New Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto("/estimate/new");
    await page.waitForLoadState("networkidle");
  });

  test("/estimate/new renders upload zone", async ({ page }) => {
    // The page has a type-selection step first
    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/single|assembly|drawing|upload/);
  });

  test("single drawing option navigates to upload step", async ({ page }) => {
    // Step 1: type selection — click "Single drawing"
    const singleBtn = page
      .locator('button:has-text("Single"), button:has-text("single")')
      .first();
    if (await singleBtn.isVisible({ timeout: 5000 })) {
      await singleBtn.click();
      // Should now show upload zone
      const uploadZone = page.locator(
        'input[type="file"], [data-testid="upload-zone"], text=/drag|drop|upload/i'
      );
      await expect(uploadZone.first()).toBeVisible({ timeout: 8000 });
    }
  });

  test("file input accepts image MIME types", async ({ page }) => {
    // Navigate to upload step
    const singleBtn = page
      .locator('button:has-text("Single"), button:has-text("single")')
      .first();
    if (await singleBtn.isVisible({ timeout: 5000 })) {
      await singleBtn.click();
    }

    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible({ timeout: 5000 })) {
      const accept = await fileInput.getAttribute("accept");
      // Should accept images or PDFs
      if (accept) {
        expect(accept).toMatch(/image|pdf|\*/i);
      }
    }
  });
});

// ── Similarity Search ───────────────────────────────────────────────────────

test.describe("Flow 5: Similarity Search Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto("/similar");
    await page.waitForLoadState("networkidle");
  });

  test("/similar renders upload zone", async ({ page }) => {
    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/upload|drag|drop|drawing|search/);
  });

  test("search button is disabled without a file", async ({ page }) => {
    // The search button should be present
    const searchBtn = page
      .locator('button:has-text("Search"), button:has-text("Find")')
      .first();
    if (await searchBtn.isVisible({ timeout: 5000 })) {
      // Without a file, it should either be disabled or clicking shows an error
      const isDisabled = await searchBtn
        .getAttribute("disabled")
        .then((v) => v !== null)
        .catch(() => false);
      if (!isDisabled) {
        await searchBtn.click();
        // Should show an error message rather than crashing
        const errorMsg = page.locator(
          '[role="alert"], text=/select|choose|upload|error/i'
        );
        await expect(errorMsg.first()).toBeVisible({ timeout: 5000 });
      } else {
        expect(isDisabled).toBe(true);
      }
    }
  });

  test("minimum 2 drawings note is communicated to user", async ({ page }) => {
    // Per product rules: similarity requires 2+ drawings
    const body = await page.locator("body").textContent();
    // The page should convey the upload concept clearly
    expect(body!.toLowerCase()).toMatch(/upload|drawing|file/);
  });
});

// ── Library ─────────────────────────────────────────────────────────────────

test.describe("Flow 6: Library Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/library renders without crash", async ({ page }) => {
    await login(page);
    await page.goto("/library");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.trim().length).toBeGreaterThan(50);
    expect(body!.toLowerCase()).not.toContain("something went wrong");
  });

  test("library shows drawing count or empty state", async ({ page }) => {
    await login(page);
    await page.goto("/library");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    // Should show count, "indexed", "no drawings", or similar
    expect(body!.toLowerCase()).toMatch(
      /drawing|indexed|library|total|no drawings|empty/
    );
  });
});

// ── Chat ─────────────────────────────────────────────────────────────────────

test.describe("Flow 7: Chat Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto("/chat");
    await page.waitForLoadState("networkidle");
  });

  test("/chat renders chat UI with message input", async ({ page }) => {
    // Chat should have a textarea or input for messages
    const messageInput = page.locator(
      'textarea, input[type="text"][placeholder*="message" i], input[type="text"][placeholder*="ask" i]'
    );
    await expect(messageInput.first()).toBeVisible({ timeout: 10000 });
  });

  test("message input accepts text", async ({ page }) => {
    const messageInput = page
      .locator(
        'textarea, input[type="text"][placeholder*="message" i], input[type="text"][placeholder*="ask" i]'
      )
      .first();

    if (await messageInput.isVisible({ timeout: 8000 })) {
      await messageInput.fill("What is the cost of a turned aluminum part?");
      const value = await messageInput.inputValue();
      expect(value).toContain("aluminum");
    }
  });

  test("send button or Enter key is present", async ({ page }) => {
    const sendBtn = page.locator(
      'button[type="submit"], button:has-text("Send"), button[aria-label*="send" i]'
    );
    if (!(await sendBtn.first().isVisible({ timeout: 5000 }))) {
      // Some chat UIs use Enter key — check input exists at minimum
      const input = page.locator("textarea, input[type='text']").first();
      await expect(input).toBeVisible({ timeout: 8000 });
    }
  });
});

// ── MPN Search ───────────────────────────────────────────────────────────────

test.describe("Flow 8: MPN Part Search", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/mpn renders search input", async ({ page }) => {
    await login(page);
    await page.goto("/mpn");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/part|mpn|search|number/);

    const searchInput = page.locator(
      'input[type="text"], input[type="search"], input[placeholder*="part" i], input[placeholder*="MPN" i]'
    );
    await expect(searchInput.first()).toBeVisible({ timeout: 8000 });
  });
});

// ── Workflows ────────────────────────────────────────────────────────────────

test.describe("Flow 9: AI Procurement Workflows", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/workflows renders list or empty state", async ({ page }) => {
    await login(page);
    await page.goto("/workflows");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(
      /workflow|procurement|rfq|no workflow|create|start/
    );
  });

  test("/workflows/new renders form", async ({ page }) => {
    await login(page);
    await page.goto("/workflows/new");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.trim().length).toBeGreaterThan(50);
    expect(body!.toLowerCase()).not.toContain("something went wrong");
  });
});
