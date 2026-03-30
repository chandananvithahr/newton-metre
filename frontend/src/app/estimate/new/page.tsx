"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { extractDrawing, createEstimate, getMaterialPrice } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

const KNOWN_MATERIALS = [
  "Mild Steel IS2062",
  "EN8 Steel",
  "EN24 Steel",
  "Stainless Steel 304",
  "Aluminum 6061",
  "Brass IS319",
  "Copper",
  "Cast Iron",
  "Titanium Grade 5",
];

type Step = "upload" | "extracting" | "review" | "calculating" | "result";

interface ProcessLine {
  process_id: string;
  process_name: string;
  time_min: number;
  machine_cost: number;
  setup_cost_per_unit: number;
  tooling_cost: number;
  labour_cost: number;
  power_cost: number;
}

interface EstimateResult {
  material_name: string;
  material_cost: number;
  process_lines: ProcessLine[];
  total_machining_cost: number;
  total_setup_cost: number;
  total_tooling_cost: number;
  total_labour_cost: number;
  total_power_cost: number;
  subtotal: number;
  overhead: number;
  profit: number;
  unit_cost: number;
  order_cost: number;
  quantity: number;
  confidence_tier: string | null;
  currency: string;
}

const EXTRACT_LOG = [
  "Reading drawing file...",
  "Identifying part geometry...",
  "Extracting dimensions and tolerances...",
  "Detecting material specifications...",
  "Analyzing manufacturing processes...",
];

const CALC_LOG = [
  "Loading material database...",
  "Running MRR calculations...",
  "Computing tool life (Taylor model)...",
  "Applying overhead and profit margins...",
  "Generating line-by-line breakdown...",
];

export default function NewEstimatePage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [extractedData, setExtractedData] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<EstimateResult | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [materialOverride, setMaterialOverride] = useState<string>("");
  const [customMaterial, setCustomMaterial] = useState<string>("");
  const [materialPrice, setMaterialPrice] = useState<{ price_inr: number; source: string } | null>(null);
  const [fetchingPrice, setFetchingPrice] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setError("");
    setStep("extracting");

    try {
      const data = await extractDrawing(file);
      setExtractedData(data);
      setMaterialOverride("");
      setCustomMaterial("");
      setMaterialPrice(null);
      setStep("review");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed");
      setStep("upload");
    }
  }

  async function handleFetchPrice() {
    const name = materialOverride === "__custom__" ? customMaterial.trim() : materialOverride;
    if (!name) return;
    setFetchingPrice(true);
    setMaterialPrice(null);
    try {
      const res = await getMaterialPrice(name);
      setMaterialPrice({ price_inr: res.price_inr, source: res.source });
    } catch {
      // non-critical — price lookup is best-effort
    } finally {
      setFetchingPrice(false);
    }
  }

  async function handleCalculate() {
    if (!extractedData) return;
    setError("");
    setStep("calculating");

    const effectiveMaterial =
      materialOverride === "__custom__"
        ? customMaterial.trim() || null
        : materialOverride || extractedData.material;

    const dataToSend = effectiveMaterial
      ? { ...extractedData, material: effectiveMaterial }
      : extractedData;

    try {
      const est = await createEstimate(dataToSend, quantity);
      setResult(est);
      setStep("result");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Calculation failed");
      setStep("review");
    }
  }

  function fmt(n: number) {
    return n.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  }

  const confidenceBadge = (tier: string | null) => {
    if (!tier) return null;
    const styles: Record<string, string> = {
      high:        "bg-emerald-950/60 text-emerald-400 border-emerald-800",
      medium:      "bg-amber-950/60 text-amber-400 border-amber-800",
      low:         "bg-red-950/60 text-red-400 border-red-800",
      insufficient:"bg-[#1C2235] text-[#64748B] border-[#2A3140]",
    };
    return (
      <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${styles[tier] ?? styles.insufficient}`} style={{ fontFamily: "var(--font-mono)" }}>
        {tier.toUpperCase()} confidence
      </span>
    );
  };

  // Mission intake log UI (shared between extracting + calculating)
  function MissionLog({ lines }: { lines: string[] }) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0F1117]">
        <div className="w-full max-w-md px-8">
          <p className="text-xs font-medium text-[#475569] uppercase tracking-widest mb-5" style={{ fontFamily: "var(--font-mono)" }}>
            MISSION INTAKE
          </p>
          <div className="space-y-3">
            {lines.map((line, i) => {
              const isLast = i === lines.length - 1;
              return (
                <div
                  key={line}
                  className={`flex items-center gap-3 text-sm ${isLast ? "log-line-active" : "log-line-done"}`}
                  style={{ animationDelay: `${i * 0.35}s`, fontFamily: "var(--font-mono)" }}
                >
                  {isLast ? (
                    <span className="text-[#22D3EE] text-base leading-none">›</span>
                  ) : (
                    <span className="text-emerald-400 text-base leading-none">✓</span>
                  )}
                  <span className={isLast ? "text-[#E2E8F0]" : "text-[#475569]"}>{line}</span>
                  {isLast && <span className="cursor-blink" />}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // Upload step
  if (step === "upload") {
    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 className="text-3xl mb-2 tracking-tight">New Estimate</h1>
          <p className="text-[#64748B] mb-8 text-sm">Upload an engineering drawing to get a should-cost breakdown.</p>

          <div className="bg-[#161B27] rounded-2xl border border-[#2A3140] p-8">
            <div
              className="border-2 border-dashed border-[#2A3140] rounded-xl p-10 text-center mb-6 hover:border-[#22D3EE]/50 hover:bg-[#22D3EE]/5 transition-colors cursor-pointer"
              role="button"
              tabIndex={0}
              onClick={() => document.getElementById("file-input")?.click()}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("file-input")?.click(); } }}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-[#22D3EE]", "bg-[#22D3EE]/5"); }}
              onDragLeave={(e) => { e.currentTarget.classList.remove("border-[#22D3EE]", "bg-[#22D3EE]/5"); }}
              onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-[#22D3EE]", "bg-[#22D3EE]/5"); const f = e.dataTransfer.files[0]; if (f) setFile(f); }}
            >
              <div className="w-12 h-12 bg-[#22D3EE]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-[#22D3EE]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              </div>
              {file ? (
                <p className="text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{file.name}</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-[#94A3B8] mb-1">Click to upload or drag and drop</p>
                  <p className="text-xs text-[#475569]">PDF, PNG, or JPG (max 10MB)</p>
                </>
              )}
              <input
                id="file-input"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
              />
            </div>

            <div className="flex items-center gap-4 mb-6">
              <label className="text-sm font-medium text-[#94A3B8]">Quantity:</label>
              <input
                type="number"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                className="w-24 px-3 py-2.5 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0]"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>

            {error && (
              <div className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-4">
                {error}
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file}
              className="w-full bg-[#22D3EE] text-[#0F1117] py-3.5 rounded-lg font-semibold hover:bg-[#06B6D4] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              Analyze Drawing
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Extracting step — mission intake log
  if (step === "extracting") {
    return <MissionLog lines={EXTRACT_LOG} />;
  }

  // Review step
  if (step === "review" && extractedData) {
    const dims = (extractedData.dimensions as Record<string, unknown>) || {};
    const detectedMaterial = extractedData.material as string | null;
    const matConfidence = extractedData.material_confidence as string | undefined;
    const needsMaterialInput = detectedMaterial === null || matConfidence === "low";
    const activeMaterial =
      materialOverride === "__custom__"
        ? customMaterial.trim()
        : materialOverride || detectedMaterial;

    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-8">
          <h1 className="text-3xl mb-2 tracking-tight">Review Extracted Data</h1>
          <p className="text-[#64748B] text-sm mb-6">Verify the AI-extracted data before calculating costs.</p>

          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-6 mb-4">
            <h2 className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-4" style={{ fontFamily: "var(--font-mono)" }}>Dimensions</h2>
            <table className="w-full">
              <tbody>
                {Object.entries(dims).map(([key, val]) =>
                  val != null ? (
                    <tr key={key} className="border-b border-[#2A3140] last:border-0">
                      <td className="py-2.5 text-sm text-[#64748B] capitalize">{key.replace(/_/g, " ")}</td>
                      <td className="py-2.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{String(val)}</td>
                    </tr>
                  ) : null
                )}
              </tbody>
            </table>
          </div>

          {/* Material section */}
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-6 mb-4">
            <div className="flex items-start justify-between mb-3">
              <span className="text-sm font-medium text-[#94A3B8]">Material</span>
              {detectedMaterial !== null && matConfidence === "high" ? (
                <span className="text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{detectedMaterial}</span>
              ) : (
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  detectedMaterial === null
                    ? "bg-amber-950/60 text-amber-400 border border-amber-800"
                    : "bg-amber-950/40 text-amber-400 border border-amber-900"
                }`} style={{ fontFamily: "var(--font-mono)" }}>
                  {detectedMaterial === null ? "Not detected" : "Low confidence"}
                </span>
              )}
            </div>

            {needsMaterialInput ? (
              <div className="space-y-3">
                <div className="bg-amber-950/30 border border-amber-900/50 rounded-lg px-3 py-2.5 text-amber-400 text-sm">
                  {detectedMaterial === null
                    ? "Material not found in the drawing. Select from the list or enter manually."
                    : `AI detected "${detectedMaterial}" with low confidence. Please confirm or correct it.`}
                </div>

                <select
                  value={materialOverride}
                  onChange={(e) => { setMaterialOverride(e.target.value); setMaterialPrice(null); }}
                  className="w-full px-3 py-2.5 border border-[#2A3140] rounded-lg bg-[#1C2235] text-sm text-[#E2E8F0] outline-none"
                >
                  <option value="">
                    {detectedMaterial !== null ? `Keep detected: ${detectedMaterial}` : "— Select material —"}
                  </option>
                  {KNOWN_MATERIALS.map((m) => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                  <option value="__custom__">Other (enter manually)…</option>
                </select>

                {materialOverride === "__custom__" && (
                  <input
                    type="text"
                    placeholder="e.g. EN31 Steel, Bronze, AISI 4140"
                    value={customMaterial}
                    onChange={(e) => { setCustomMaterial(e.target.value); setMaterialPrice(null); }}
                    className="w-full px-3 py-2.5 border border-[#2A3140] rounded-lg bg-[#1C2235] text-sm text-[#E2E8F0] outline-none"
                  />
                )}

                <div className="flex items-center gap-3">
                  <button
                    onClick={handleFetchPrice}
                    disabled={!activeMaterial || fetchingPrice}
                    className="text-sm text-[#22D3EE] hover:text-[#06B6D4] font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                  >
                    {fetchingPrice ? "Fetching…" : "Look up market price (INR/kg)"}
                  </button>
                  {materialPrice !== null && (
                    <span className="text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>
                      ₹{materialPrice.price_inr.toLocaleString("en-IN")}/kg
                      <span className="text-xs text-[#475569] ml-1">({materialPrice.source})</span>
                    </span>
                  )}
                </div>
              </div>
            ) : null}
          </div>

          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-6 mb-6 space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-[#64748B]">Processes</span>
              <span className="text-sm font-medium text-[#E2E8F0]">{(extractedData.suggested_processes as string[] || []).join(", ")}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-[#64748B]">AI Confidence</span>
              <span className="text-sm font-medium text-[#E2E8F0] capitalize">{String(extractedData.confidence || "—")}</span>
            </div>
          </div>

          {error && (
            <div className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-4">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleCalculate}
              disabled={needsMaterialInput && !activeMaterial}
              className="flex-1 bg-[#22D3EE] text-[#0F1117] py-3.5 rounded-lg font-semibold hover:bg-[#06B6D4] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              Calculate Cost
            </button>
            <button
              onClick={() => setStep("upload")}
              className="px-6 py-3.5 border border-[#2A3140] rounded-lg hover:bg-[#1C2235] text-sm font-medium text-[#94A3B8] transition-colors"
            >
              Re-upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Calculating step — mission intake log
  if (step === "calculating") {
    return <MissionLog lines={CALC_LOG} />;
  }

  // Result step
  if (step === "result" && result) {
    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav />
        <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl tracking-tight">Should-Cost Estimate</h1>
              <p className="text-[#64748B] text-sm mt-1">
                {result.material_name} &middot; {result.quantity} unit{result.quantity > 1 ? "s" : ""}
              </p>
            </div>
            {confidenceBadge(result.confidence_tier)}
          </div>

          {/* Summary table */}
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden mb-4">
            <table className="w-full">
              <thead>
                <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Amount ({result.currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A3140]">
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Material ({result.material_name})</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.material_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Machining</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.total_machining_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Setup & Tooling</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.total_setup_cost + result.total_tooling_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Labour</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.total_labour_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Power</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.total_power_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Overhead (15%)</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.overhead)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Profit (20%)</td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(result.profit)}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr className="bg-[#22D3EE] text-[#0F1117]">
                  <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>TOTAL (per unit)</td>
                  <td className="px-6 py-4 text-right font-bold text-lg" style={{ fontFamily: "var(--font-mono)" }}>
                    {result.currency} {fmt(result.unit_cost)}
                  </td>
                </tr>
                {result.quantity > 1 && (
                  <tr className="bg-[#06B6D4] text-[#0F1117]">
                    <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>ORDER TOTAL ({result.quantity} units)</td>
                    <td className="px-6 py-4 text-right font-bold text-lg" style={{ fontFamily: "var(--font-mono)" }}>
                      {result.currency} {fmt(result.order_cost)}
                    </td>
                  </tr>
                )}
              </tfoot>
            </table>
          </div>

          {/* Expand/collapse process detail */}
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-2 text-[#22D3EE] hover:text-[#06B6D4] text-sm font-medium mb-4 transition-colors"
          >
            <svg
              className={`w-4 h-4 transition-transform ${expanded ? "rotate-90" : ""}`}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
            {expanded ? "Hide" : "Show"} full process breakdown
          </button>

          {expanded && (
            <div className="bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden mb-6 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                    <th className="text-left px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Process</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Time</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Machine</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Setup</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Tooling</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Labour</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Power</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#2A3140]">
                  {result.process_lines.map((pl) => (
                    <tr key={pl.process_id} className="hover:bg-[#1C2235] transition-colors">
                      <td className="px-4 py-3 font-medium text-[#E2E8F0]">{pl.process_name}</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{pl.time_min.toFixed(1)} min</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.machine_cost)}</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.setup_cost_per_unit)}</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.tooling_cost)}</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.labour_cost)}</td>
                      <td className="px-4 py-3 text-right text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.power_cost)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 mt-6">
            <button
              onClick={() => router.push("/dashboard")}
              className="flex-1 border border-[#2A3140] py-3.5 rounded-lg hover:bg-[#1C2235] text-sm font-medium text-[#94A3B8] transition-colors"
            >
              Back to Dashboard
            </button>
            <button
              onClick={() => { setStep("upload"); setResult(null); setExtractedData(null); }}
              className="flex-1 bg-[#22D3EE] text-[#0F1117] py-3.5 rounded-lg font-semibold hover:bg-[#06B6D4] transition-colors"
            >
              New Estimate
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
