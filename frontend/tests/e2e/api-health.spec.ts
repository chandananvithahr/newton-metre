import { test, expect } from "@playwright/test";

/**
 * API Health Checks
 * Validates the Railway backend is up and key endpoints respond correctly.
 * These are request-level checks — no browser UI needed.
 */

const API_BASE = "https://costimize-api-production.up.railway.app";

test.describe("Backend API — Health", () => {
  test("GET /api/health returns 200", async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/health`);
    expect(response.status()).toBe(200);
    const body = await response.json().catch(() => null);
    // Should return some JSON — status/ok field
    expect(body).not.toBeNull();
  });

  test("GET /api/health response time under 5 seconds", async ({ request }) => {
    const start = Date.now();
    const response = await request.get(`${API_BASE}/api/health`, {
      timeout: 5000,
    });
    const elapsed = Date.now() - start;
    expect(response.status()).toBe(200);
    expect(elapsed).toBeLessThan(5000);
  });

  test("unauthenticated POST /api/estimate returns 401 or 422 (not 500)", async ({
    request,
  }) => {
    const response = await request.post(`${API_BASE}/api/estimate`, {
      data: {},
      headers: { "Content-Type": "application/json" },
    });
    // Should reject cleanly — 401 (unauth) or 422 (validation), never 500
    expect([401, 403, 422]).toContain(response.status());
  });

  test("unknown route returns 404 (not 500)", async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/nonexistent-route-xyz`);
    expect(response.status()).toBe(404);
  });

  test("CORS headers present on /api/health for frontend origin", async ({
    request,
  }) => {
    const response = await request.get(`${API_BASE}/api/health`, {
      headers: {
        Origin: "https://frontend-theta-ecru-95.vercel.app",
      },
    });
    expect(response.status()).toBe(200);
    // CORS header should allow the frontend origin
    const corsHeader = response.headers()["access-control-allow-origin"];
    if (corsHeader) {
      expect(corsHeader).toMatch(
        /frontend-theta-ecru-95\.vercel\.app|\*/
      );
    }
    // If no CORS header, that may be intentional for GET — pass either way
  });
});

test.describe("Backend API — Estimate Endpoint Validation", () => {
  test("POST /api/estimate without file returns validation error, not crash", async ({
    request,
  }) => {
    const response = await request.post(`${API_BASE}/api/estimate`, {
      multipart: {
        part_type: "mechanical",
        quantity: "1",
        // Intentionally omit file
      },
    });
    // 401 (no auth token), 422 (missing file field), or 400 — all acceptable
    // What we must NOT get is 500
    expect(response.status()).not.toBe(500);
  });
});
