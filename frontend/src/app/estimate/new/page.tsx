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

  if (step === "upload") {
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
          <span className="text-xl font-bold cursor-pointer" onClick={() => router.push("/dashboard")}>Costimize</span>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-16">
          <h1 className="text-3xl font-bold mb-2">New Estimate</h1>
          <p className="text-gray-600 mb-8">Upload an engineering drawing to get a should-cost breakdown.</p>

          <div className="bg-white rounded-xl shadow p-8">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
              <input
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mx-auto"
              />
              <p className="text-gray-500 text-sm mt-2">PDF, PNG, or JPG (max 10MB)</p>
            </div>

            <div className="flex items-center gap-4 mb-6">
              <label className="text-sm font-medium">Quantity:</label>
              <input
                type="number"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                className="w-24 px-3 py-2 border rounded-lg"
              />
            </div>

            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            <button
              onClick={handleUpload}
              disabled={!file}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              Analyze Drawing
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (step === "extracting") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold mb-2">Analyzing Drawing...</h1>
          <p className="text-gray-600">AI is extracting dimensions, tolerances, and processes.</p>
        </div>
      </div>
    );
  }

  if (step === "review" && extractedData) {
    const dims = extractedData.dimensions as Record<string, unknown> || {};
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
          <span className="text-xl font-bold">Costimize</span>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-8">
          <h1 className="text-3xl font-bold mb-6">Review Extracted Data</h1>

          <div className="bg-white rounded-xl shadow p-6 mb-6">
            <h2 className="font-semibold mb-3">Dimensions</h2>
            <table className="w-full">
              <tbody>
                {Object.entries(dims).map(([key, val]) =>
                  val != null && (
                    <tr key={key} className="border-b last:border-0">
                      <td className="py-2 text-gray-600 capitalize">{key.replace(/_/g, " ")}</td>
                      <td className="py-2 text-right font-mono">{String(val)}</td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>

          <div className="bg-white rounded-xl shadow p-6 mb-6">
            <p><span className="font-semibold">Material:</span> {String(extractedData.material || "Not detected")}</p>
            <p><span className="font-semibold">Processes:</span> {(extractedData.suggested_processes as string[] || []).join(", ")}</p>
            <p><span className="font-semibold">AI Confidence:</span> {String(extractedData.confidence || "—")}</p>
          </div>

          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          <div className="flex gap-4">
            <button onClick={handleCalculate} className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700">
              Calculate Cost
            </button>
            <button onClick={() => setStep("upload")} className="px-6 py-3 border rounded-lg hover:bg-gray-50">
              Re-upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (step === "calculating") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold mb-2">Calculating Cost...</h1>
          <p className="text-gray-600">Physics engine computing line-by-line breakdown.</p>
        </div>
      </div>
    );
  }

  if (step === "result" && result) {
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
          <span className="text-xl font-bold cursor-pointer" onClick={() => router.push("/dashboard")}>Costimize</span>
        </nav>
        <div className="max-w-3xl mx-auto px-8 py-8">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold">Should-Cost Estimate</h1>
            {result.confidence_tier && (
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                result.confidence_tier === "high" ? "bg-green-100 text-green-700" :
                result.confidence_tier === "medium" ? "bg-yellow-100 text-yellow-700" :
                "bg-red-100 text-red-700"
              }`}>
                {result.confidence_tier.toUpperCase()} confidence
              </span>
            )}
          </div>

          <div className="bg-white rounded-xl shadow overflow-hidden mb-6">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Cost Component</th>
                  <th className="text-right px-6 py-3 text-sm font-medium text-gray-500">Amount ({result.currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                <tr>
                  <td className="px-6 py-3">Material ({result.material_name})</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.material_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Machining</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.total_machining_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Setup & Tooling</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.total_setup_cost + result.total_tooling_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Labour</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.total_labour_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Power</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.total_power_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Overhead</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.overhead)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3">Profit</td>
                  <td className="px-6 py-3 text-right font-mono">{fmt(result.profit)}</td>
                </tr>
                <tr className="bg-blue-50 font-bold">
                  <td className="px-6 py-4">TOTAL (per unit)</td>
                  <td className="px-6 py-4 text-right font-mono text-lg">
                    {result.currency} {fmt(result.unit_cost)}
                  </td>
                </tr>
                {result.quantity > 1 && (
                  <tr className="bg-blue-50 font-bold">
                    <td className="px-6 py-4">ORDER TOTAL ({result.quantity} units)</td>
                    <td className="px-6 py-4 text-right font-mono text-lg">
                      {result.currency} {fmt(result.order_cost)}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <button
            onClick={() => setExpanded(!expanded)}
            className="text-blue-600 hover:underline mb-6 inline-block"
          >
            {expanded ? "Hide" : "Show"} full process breakdown
          </button>

          {expanded && (
            <div className="bg-white rounded-xl shadow overflow-hidden mb-6">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="text-left px-4 py-2">Process</th>
                    <th className="text-right px-4 py-2">Time</th>
                    <th className="text-right px-4 py-2">Machine</th>
                    <th className="text-right px-4 py-2">Setup</th>
                    <th className="text-right px-4 py-2">Tooling</th>
                    <th className="text-right px-4 py-2">Labour</th>
                    <th className="text-right px-4 py-2">Power</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {result.process_lines.map((pl) => (
                    <tr key={pl.process_id}>
                      <td className="px-4 py-2">{pl.process_name}</td>
                      <td className="px-4 py-2 text-right font-mono">{pl.time_min.toFixed(1)} min</td>
                      <td className="px-4 py-2 text-right font-mono">{fmt(pl.machine_cost)}</td>
                      <td className="px-4 py-2 text-right font-mono">{fmt(pl.setup_cost_per_unit)}</td>
                      <td className="px-4 py-2 text-right font-mono">{fmt(pl.tooling_cost)}</td>
                      <td className="px-4 py-2 text-right font-mono">{fmt(pl.labour_cost)}</td>
                      <td className="px-4 py-2 text-right font-mono">{fmt(pl.power_cost)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="flex gap-4">
            <button onClick={() => router.push("/dashboard")} className="flex-1 border py-3 rounded-lg hover:bg-gray-50">
              Back to Dashboard
            </button>
            <button onClick={() => { setStep("upload"); setResult(null); setExtractedData(null); }} className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700">
              New Estimate
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
