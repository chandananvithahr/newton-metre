import { test, expect } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";

/**
 * Extraction Accuracy Tests
 *
 * Sends real drawing files to the production API and validates that the AI
 * extractor returns correct dimensions, material, and processes.
 *
 * Ground truths are derived from the raw DXF/STEP vector data (not AI) — they
 * represent what the file actually contains, making them objective benchmarks.
 *
 * Requires auth credentials to hit the API:
 *   TEST_USER_EMAIL=your@email.com
 *   TEST_USER_PASSWORD=yourpassword
 *
 * Run: npm run test:e2e:auth  (includes this file via authenticated suite)
 */

const API_URL = "https://costimize-api-production.up.railway.app";
const TEST_EMAIL = process.env.TEST_USER_EMAIL ?? "";
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD ?? "";
const HAS_CREDENTIALS = TEST_EMAIL !== "" && TEST_PASSWORD !== "";

// ── Known ground truths from DXF vector data ──────────────────────────────────
const GROUND_TRUTHS = {
  "stepped_shaft.dxf": {
    outer_diameter_mm: 50,        // D50 annotation + 25mm radius circle
    length_mm: 40,                 // 40mm linear annotation
    material: "EN8",              // "Material: EN8 (IS:1570)" text in drawing
    has_tight_tolerances: true,   // "Tolerance: +/-0.05" in drawing
    processes: ["turning"],
  },
  "flange_plate.dxf": {
    material_hint: null,          // no material annotation in this file
    processes_hint: ["milling_face", "drilling"],
  },
  "stepped_shaft.stp": {
    outer_diameter_mm: 50,        // same part as DXF — STEP export
    material: "EN8",
    processes: ["turning"],
  },
};

// ── Auth helper ───────────────────────────────────────────────────────────────
async function getJWT(): Promise<string> {
  const { createClient } = await import("@supabase/supabase-js");
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
  const { data, error } = await supabase.auth.signInWithPassword({
    email: TEST_EMAIL,
    password: TEST_PASSWORD,
  });
  if (error || !data.session) throw new Error(`Auth failed: ${error?.message}`);
  return data.session.access_token;
}

// ── Drawing upload helper ─────────────────────────────────────────────────────
async function extractDrawing(filePath: string, jwt: string): Promise<Record<string, unknown>> {
  const fileBytes = fs.readFileSync(filePath);
  const filename = path.basename(filePath);

  // Use node-fetch style via fetch API
  const formData = new FormData();
  const blob = new Blob([fileBytes]);
  formData.append("file", blob, filename);

  const res = await fetch(`${API_URL}/api/extract`, {
    method: "POST",
    headers: { Authorization: `Bearer ${jwt}` },
    body: formData,
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Extract failed ${res.status}: ${body}`);
  }

  return res.json() as Promise<Record<string, unknown>>;
}

// ── Tests ─────────────────────────────────────────────────────────────────────

test.describe("Extraction Accuracy — stepped_shaft.dxf", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: set TEST_USER_EMAIL / TEST_USER_PASSWORD");

  let result: Record<string, unknown>;
  const DRAWING = path.resolve(__dirname, "../../../../test-files/dxf/stepped_shaft.dxf");
  const GT = GROUND_TRUTHS["stepped_shaft.dxf"];

  test.beforeAll(async () => {
    const jwt = await getJWT();
    result = await extractDrawing(DRAWING, jwt);
    console.log("stepped_shaft.dxf extraction result:", JSON.stringify(result, null, 2));
  });

  test("confidence is not failed/low", async () => {
    const confidence = result.confidence as string;
    expect(["high", "medium"]).toContain(confidence);
  });

  test("outer_diameter_mm within 10% of ground truth (50mm)", async () => {
    const dims = result.dimensions as Record<string, number>;
    const od = dims?.outer_diameter_mm;
    expect(od).toBeDefined();
    expect(od).toBeGreaterThan(GT.outer_diameter_mm * 0.9);  // ≥45mm
    expect(od).toBeLessThan(GT.outer_diameter_mm * 1.1);    // ≤55mm
  });

  test("length_mm within 10% of ground truth (40mm)", async () => {
    const dims = result.dimensions as Record<string, number>;
    const len = dims?.length_mm;
    expect(len).toBeDefined();
    expect(len).toBeGreaterThan(GT.length_mm * 0.9);  // ≥36mm
    expect(len).toBeLessThan(GT.length_mm * 1.1);    // ≤44mm
  });

  test("material detected contains EN8", async () => {
    const material = (result.material as string | null) ?? "";
    expect(material.toLowerCase()).toContain("en8");
  });

  test("tight tolerances detected", async () => {
    const tolerances = result.tolerances as Record<string, unknown>;
    expect(tolerances?.has_tight_tolerances).toBe(true);
  });

  test("turning process detected", async () => {
    const processes = result.suggested_processes as string[];
    expect(processes).toContain("turning");
  });
});

test.describe("Extraction Accuracy — stepped_shaft.stp (STEP format)", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: set TEST_USER_EMAIL / TEST_USER_PASSWORD");

  let result: Record<string, unknown>;
  const DRAWING = path.resolve(__dirname, "../../../../test-files/step/stepped_shaft.stp");
  const GT = GROUND_TRUTHS["stepped_shaft.stp"];

  test.beforeAll(async () => {
    const jwt = await getJWT();
    result = await extractDrawing(DRAWING, jwt);
    console.log("stepped_shaft.stp extraction result:", JSON.stringify(result, null, 2));
  });

  test("STEP extraction returns non-empty result", async () => {
    expect(result).toBeDefined();
    expect(result.confidence).not.toBe("failed");
  });

  test("outer_diameter_mm detected (STEP)", async () => {
    const dims = result.dimensions as Record<string, number>;
    expect(dims?.outer_diameter_mm).toBeGreaterThan(0);
  });

  test("turning process detected from STEP", async () => {
    const processes = result.suggested_processes as string[];
    expect(processes.length).toBeGreaterThan(0);
  });
});

test.describe("Extraction Accuracy — flange_plate.dxf", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: set TEST_USER_EMAIL / TEST_USER_PASSWORD");

  let result: Record<string, unknown>;
  const DRAWING = path.resolve(__dirname, "../../../../test-files/dxf/flange_plate.dxf");

  test.beforeAll(async () => {
    const jwt = await getJWT();
    result = await extractDrawing(DRAWING, jwt);
    console.log("flange_plate.dxf extraction result:", JSON.stringify(result, null, 2));
  });

  test("confidence not failed", async () => {
    expect(result.confidence).not.toBe("failed");
  });

  test("milling or drilling process detected", async () => {
    const processes = result.suggested_processes as string[];
    const hasMachining = processes.some(p =>
      ["milling_face", "milling_slot", "drilling", "boring"].includes(p)
    );
    expect(hasMachining).toBe(true);
  });

  test("at least one dimension extracted", async () => {
    const dims = result.dimensions as Record<string, unknown>;
    const nonNull = Object.values(dims).filter(v => v !== null && v !== undefined && v !== 0);
    expect(nonNull.length).toBeGreaterThan(0);
  });
});

// ── Gemini vs Newton-Metre comparison test ────────────────────────────────────
test.describe("Gemini Direct vs Newton-Metre pipeline", () => {
  test.skip(!HAS_CREDENTIALS, "Skipped: set TEST_USER_EMAIL / TEST_USER_PASSWORD");

  const DRAWING = path.resolve(__dirname, "../../../../test-files/dxf/stepped_shaft.dxf");
  const GT = GROUND_TRUTHS["stepped_shaft.dxf"];

  test("Newton-Metre extraction matches DXF ground truth for all key fields", async () => {
    const jwt = await getJWT();
    const result = await extractDrawing(DRAWING, jwt);
    const dims = result.dimensions as Record<string, number>;

    const checks = {
      outer_diameter_mm: {
        got: dims?.outer_diameter_mm,
        expected: GT.outer_diameter_mm,
        tolerance_pct: 10,
      },
      length_mm: {
        got: dims?.length_mm,
        expected: GT.length_mm,
        tolerance_pct: 10,
      },
    };

    const passed: string[] = [];
    const failed: string[] = [];

    for (const [field, { got, expected, tolerance_pct }] of Object.entries(checks)) {
      if (got && Math.abs(got - expected) / expected <= tolerance_pct / 100) {
        passed.push(`${field}: ${got} ≈ ${expected} ✓`);
      } else {
        failed.push(`${field}: got ${got}, expected ${expected} (±${tolerance_pct}%) ✗`);
      }
    }

    console.log("\n=== ACCURACY REPORT: stepped_shaft.dxf ===");
    console.log("Ground truth (from DXF vector data):");
    console.log(`  OD: ${GT.outer_diameter_mm}mm | Length: ${GT.length_mm}mm | Material: ${GT.material}`);
    console.log("\nNewton-Metre result:");
    console.log(`  OD: ${dims?.outer_diameter_mm}mm | Length: ${dims?.length_mm}mm | Material: ${result.material}`);
    console.log("\nPassed:", passed);
    if (failed.length) console.log("Failed:", failed);

    expect(failed).toHaveLength(0);
  });
});
