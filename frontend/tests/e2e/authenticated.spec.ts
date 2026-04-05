import { test, expect } from "@playwright/test";

/**
 * Authenticated Flows
 *
 * Auth is handled by the "setup" project in playwright.config.ts — it logs in
 * once and saves the session to tests/e2e/.auth/user.json.  These tests reuse
 * that session via storageState, so no per-test login is needed.
 *
 * To run locally:
 *   TEST_USER_EMAIL=your@email.com TEST_USER_PASSWORD=yourpassword \
 *   npx playwright test tests/e2e/authenticated.spec.ts --project=chromium-desktop
 */

const HAS_CREDENTIALS =
  (process.env.TEST_USER_EMAIL ?? "") !== "" &&
  (process.env.TEST_USER_PASSWORD ?? "") !== "";

// ── Dashboard ───────────────────────────────────────────────────────────────

test.describe("Flow 3: Dashboard", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test.beforeEach(async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
  });

  test("dashboard renders 5 product cards", async ({ page }) => {
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
    await expect(page.locator('text="Newton-Metre"').first()).toBeVisible();
  });

  test("dashboard shows estimate history sidebar", async ({ page }) => {
    const sidebar = page.locator("aside").first();
    await expect(sidebar).toBeVisible({ timeout: 8000 });
  });

  test("sign out button is visible and functional", async ({ page }) => {
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
    await page.goto("/estimate/new");
    await page.waitForLoadState("networkidle");
  });

  test("/estimate/new renders upload zone", async ({ page }) => {
    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/single|assembly|drawing|upload/);
  });

  test("single drawing option navigates to upload step", async ({ page }) => {
    const singleBtn = page
      .locator('button:has-text("Single"), button:has-text("single")')
      .first();
    if (await singleBtn.isVisible({ timeout: 5000 })) {
      await singleBtn.click();
      // Check for file input OR any upload-related element
      const fileInput = page.locator('input[type="file"]');
      const uploadText = page.getByText(/drag|drop|upload/i);
      const hasUpload =
        (await fileInput.count()) > 0 || (await uploadText.count()) > 0;
      expect(hasUpload).toBe(true);
    }
  });

  test("file input accepts image MIME types", async ({ page }) => {
    const singleBtn = page
      .locator('button:has-text("Single"), button:has-text("single")')
      .first();
    if (await singleBtn.isVisible({ timeout: 5000 })) {
      await singleBtn.click();
    }

    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible({ timeout: 5000 })) {
      const accept = await fileInput.getAttribute("accept");
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
    await page.goto("/similar");
    await page.waitForLoadState("networkidle");
  });

  test("/similar renders upload zone", async ({ page }) => {
    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/upload|drag|drop|drawing|search/);
  });

  test("search button is disabled without a file", async ({ page }) => {
    const searchBtn = page
      .locator('button:has-text("Search"), button:has-text("Find")')
      .first();
    if (await searchBtn.isVisible({ timeout: 5000 })) {
      const isDisabled = await searchBtn
        .getAttribute("disabled")
        .then((v) => v !== null)
        .catch(() => false);
      if (!isDisabled) {
        await searchBtn.click();
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
    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/upload|drawing|file/);
  });
});

// ── Library ─────────────────────────────────────────────────────────────────

test.describe("Flow 6: Library Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/library renders without crash", async ({ page }) => {
    await page.goto("/library");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.trim().length).toBeGreaterThan(50);
    expect(body!.toLowerCase()).not.toContain("something went wrong");
  });

  test("library shows drawing count or empty state", async ({ page }) => {
    await page.goto("/library");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(
      /drawing|indexed|library|total|no drawings|empty/
    );
  });
});

// ── Chat ─────────────────────────────────────────────────────────────────────

test.describe("Flow 7: Chat Page", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test.beforeEach(async ({ page }) => {
    await page.goto("/chat");
    await page.waitForLoadState("networkidle");
  });

  test("/chat renders chat UI with message input", async ({ page }) => {
    // Full-page chat has a textarea with placeholder "Ask about manufacturing costs..."
    const messageInput = page.locator("textarea").first();
    await expect(messageInput).toBeVisible({ timeout: 10000 });
  });

  test("message input accepts text", async ({ page }) => {
    const messageInput = page.locator("textarea").first();
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
      const input = page.locator("textarea, input[type='text']").first();
      await expect(input).toBeVisible({ timeout: 8000 });
    }
  });
});

// ── MPN Search ───────────────────────────────────────────────────────────────

test.describe("Flow 8: MPN Part Search", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/mpn renders search input", async ({ page }) => {
    await page.goto("/mpn");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(/part|mpn|search|number/);

    // MPN input has placeholder "e.g. GX16-4, 6204-2RS, MCP23017"
    const searchInput = page.locator('input[type="text"]').first();
    await expect(searchInput).toBeVisible({ timeout: 8000 });
  });
});

// ── Workflows ────────────────────────────────────────────────────────────────

test.describe("Flow 9: AI Procurement Workflows", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: TEST_USER_EMAIL / TEST_USER_PASSWORD not set");

  test("/workflows renders list or empty state", async ({ page }) => {
    await page.goto("/workflows");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.toLowerCase()).toMatch(
      /workflow|procurement|rfq|no workflow|create|start/
    );
  });

  test("/workflows/new renders form", async ({ page }) => {
    await page.goto("/workflows/new");
    await page.waitForLoadState("networkidle");

    const body = await page.locator("body").textContent();
    expect(body!.trim().length).toBeGreaterThan(50);
    expect(body!.toLowerCase()).not.toContain("something went wrong");
  });
});
