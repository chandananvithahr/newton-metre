import { defineConfig, devices } from "@playwright/test";

/**
 * Newton-Metre E2E Test Configuration
 * Tests run against the live Vercel deployment.
 *
 * Auth strategy: a single "setup" project logs in once and saves storageState.
 * All authenticated projects depend on setup and reuse the saved session —
 * preventing Supabase rate-limits from firing on repeated per-test logins.
 */

const AUTH_FILE = "tests/e2e/.auth/user.json";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: 1,
  timeout: 30000,
  reporter: [
    ["html", { outputFolder: "playwright-report", open: "never" }],
    ["list"],
    ["junit", { outputFile: "test-results/results.xml" }],
  ],
  use: {
    baseURL: "https://frontend-theta-ecru-95.vercel.app",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "on-first-retry",
    actionTimeout: 15000,
    navigationTimeout: 20000,
  },
  projects: [
    // ── Auth setup (runs once, saves session) ────────────────────────────────
    {
      name: "setup",
      testMatch: /auth\.setup\.ts/,
      use: { ...devices["Desktop Chrome"] },
    },

    // ── Public pages (no auth needed) ────────────────────────────────────────
    {
      name: "chromium-desktop-public",
      testMatch: /\/(landing|navigation)\.spec\.ts/,
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "chromium-mobile-public",
      testMatch: /\/(landing|navigation)\.spec\.ts/,
      use: { ...devices["Pixel 5"] },
    },

    // ── Authenticated pages (reuse saved session) ─────────────────────────────
    {
      name: "chromium-desktop",
      testMatch: /authenticated\.spec\.ts/,
      dependencies: ["setup"],
      use: {
        ...devices["Desktop Chrome"],
        storageState: AUTH_FILE,
      },
    },
    {
      name: "chromium-mobile",
      testMatch: /authenticated\.spec\.ts/,
      dependencies: ["setup"],
      use: {
        ...devices["Pixel 5"],
        storageState: AUTH_FILE,
      },
    },
  ],
  outputDir: "test-results/artifacts",
});
