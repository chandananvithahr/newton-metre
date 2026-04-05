import { defineConfig, devices } from "@playwright/test";

/**
 * Newton-Metre E2E Test Configuration
 * Tests run against the live Vercel deployment.
 */
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
    {
      name: "chromium-desktop",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "chromium-mobile",
      use: { ...devices["Pixel 5"] },
    },
  ],
  outputDir: "test-results/artifacts",
});
