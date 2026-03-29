"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { extractDrawing, createEstimate } from "@/lib/api";

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

export default function NewEstimatePage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [extractedData, setExtractedData] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<EstimateResult | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setError("");
    setStep("extracting");

    try {
      const data = await extractDrawing(file);
      setExtractedData(data);
      setStep("review");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed");
      setStep("upload");
    }
  }

  async function handleCalculate() {
    if (!extractedData) return;
    setError("");
    setStep("calculating");

    try {
      const est = await createEstimate(extractedData, quantity);
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
    const styles = {
      high: "bg-emerald-50 text-emerald-700 border-emerald-200",
      medium: "bg-amber-50 text-amber-700 border-amber-200",
      low: "bg-red-50 text-red-700 border-red-200",
      insufficient: "bg-gray-100 text-gray-500 border-gray-200",
    };
    return (
      <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${styles[tier as keyof typeof styles] || styles.insufficient}`}>
        {tier.toUpperCase()} confidence
      </span>
    );
  };

  // Upload step
  if (step === "upload") {
    return (
      <div className="min-h-screen bg-slate-50">
        <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
          <span
            className="text-xl font-bold tracking-tight text-primary-700 cursor-pointer"
            onClick={() => router.push("/dashboard")}
          >
            Costimize
          </span>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-12">
          <h1 className="text-3xl font-bold mb-2 tracking-tight">New Estimate</h1>
          <p className="text-gray-500 mb-8">Upload an engineering drawing to get a should-cost breakdown.</p>

          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
            <div
              className="border-2 border-dashed border-gray-200 rounded-xl p-10 text-center mb-6 hover:border-primary-300 hover:bg-primary-50/30 transition-colors cursor-pointer"
              onClick={() => document.getElementById("file-input")?.click()}
            >
              <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              </div>
              {file ? (
                <p className="text-sm font-medium text-gray-900">{file.name}</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-gray-700 mb-1">Click to upload or drag and drop</p>
                  <p className="text-xs text-gray-400">PDF, PNG, or JPG (max 10MB)</p>
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
              <label className="text-sm font-medium text-gray-700">Quantity:</label>
              <input
                type="number"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                className="w-24 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50/50 outline-none text-sm font-mono"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-700 text-sm mb-4">
                {error}
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file}
              className="w-full bg-primary-600 text-white py-3.5 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              Analyze Drawing
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Extracting step
  if (step === "extracting") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-12 h-12 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-5" />
          <h1 className="text-2xl font-bold mb-2 tracking-tight">Analyzing Drawing...</h1>
          <p className="text-gray-500">AI is extracting dimensions, tolerances, and processes.</p>
        </div>
      </div>
    );
  }

  // Review step
  if (step === "review" && extractedData) {
    const dims = (extractedData.dimensions as Record<string, unknown>) || {};
    return (
      <div className="min-h-screen bg-slate-50">
        <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
          <span className="text-xl font-bold tracking-tight text-primary-700">Costimize</span>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-8">
          <h1 className="text-3xl font-bold mb-2 tracking-tight">Review Extracted Data</h1>
          <p className="text-gray-500 text-sm mb-6">Verify the AI-extracted data before calculating costs.</p>

          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-4">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Dimensions</h2>
            <table className="w-full">
              <tbody>
                {Object.entries(dims).map(([key, val]) =>
                  val != null && (
                    <tr key={key} className="border-b border-gray-50 last:border-0">
                      <td className="py-2.5 text-sm text-gray-600 capitalize">{key.replace(/_/g, " ")}</td>
                      <td className="py-2.5 text-right font-mono text-sm font-medium text-gray-900">{String(val)}</td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6 space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Material</span>
              <span className="text-sm font-medium">{String(extractedData.material || "Not detected")}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Processes</span>
              <span className="text-sm font-medium">{(extractedData.suggested_processes as string[] || []).join(", ")}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">AI Confidence</span>
              <span className="text-sm font-medium">{String(extractedData.confidence || "—")}</span>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-700 text-sm mb-4">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleCalculate}
              className="flex-1 bg-primary-600 text-white py-3.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors shadow-sm"
            >
              Calculate Cost
            </button>
            <button
              onClick={() => setStep("upload")}
              className="px-6 py-3.5 border border-gray-200 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors"
            >
              Re-upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Calculating step
  if (step === "calculating") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-12 h-12 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-5" />
          <h1 className="text-2xl font-bold mb-2 tracking-tight">Calculating Cost...</h1>
          <p className="text-gray-500">Physics engine computing line-by-line breakdown.</p>
        </div>
      </div>
    );
  }

  // Result step
  if (step === "result" && result) {
    return (
      <div className="min-h-screen bg-slate-50">
        <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
          <span
            className="text-xl font-bold tracking-tight text-primary-700 cursor-pointer"
            onClick={() => router.push("/dashboard")}
          >
            Costimize
          </span>
        </nav>
        <div className="max-w-3xl mx-auto px-8 py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Should-Cost Estimate</h1>
              <p className="text-gray-500 text-sm mt-1">
                {result.material_name} &middot; {result.quantity} unit{result.quantity > 1 ? "s" : ""}
              </p>
            </div>
            {confidenceBadge(result.confidence_tier)}
          </div>

          {/* Summary table */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden mb-4">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50/50">
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Amount ({result.currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Material ({result.material_name})</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.material_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Machining</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.total_machining_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Setup &amp; Tooling</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.total_setup_cost + result.total_tooling_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Labour</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.total_labour_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Power</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.total_power_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Overhead (15%)</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.overhead)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3.5 text-sm text-gray-700">Profit (20%)</td>
                  <td className="px-6 py-3.5 text-right font-mono text-sm font-medium">{fmt(result.profit)}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr className="bg-primary-600 text-white">
                  <td className="px-6 py-4 font-bold text-sm">TOTAL (per unit)</td>
                  <td className="px-6 py-4 text-right font-mono font-bold text-lg">
                    {result.currency} {fmt(result.unit_cost)}
                  </td>
                </tr>
                {result.quantity > 1 && (
                  <tr className="bg-primary-700 text-white">
                    <td className="px-6 py-4 font-bold text-sm">ORDER TOTAL ({result.quantity} units)</td>
                    <td className="px-6 py-4 text-right font-mono font-bold text-lg">
                      {result.currency} {fmt(result.order_cost)}
                    </td>
                  </tr>
                )}
              </tfoot>
            </table>
          </div>

          {/* Expand/collapse */}
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-2 text-primary-600 hover:text-primary-700 text-sm font-medium mb-4 transition-colors"
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
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden mb-6 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-100 bg-gray-50/50">
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Process</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Time</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Machine</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Setup</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Tooling</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Labour</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Power</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {result.process_lines.map((pl) => (
                    <tr key={pl.process_id} className="hover:bg-gray-50/50">
                      <td className="px-4 py-3 font-medium text-gray-900">{pl.process_name}</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{pl.time_min.toFixed(1)} min</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{fmt(pl.machine_cost)}</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{fmt(pl.setup_cost_per_unit)}</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{fmt(pl.tooling_cost)}</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{fmt(pl.labour_cost)}</td>
                      <td className="px-4 py-3 text-right font-mono text-gray-600">{fmt(pl.power_cost)}</td>
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
              className="flex-1 border border-gray-200 py-3.5 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors"
            >
              Back to Dashboard
            </button>
            <button
              onClick={() => { setStep("upload"); setResult(null); setExtractedData(null); }}
              className="flex-1 bg-primary-600 text-white py-3.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors shadow-sm"
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
