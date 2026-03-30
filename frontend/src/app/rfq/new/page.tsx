"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { AppNav } from "@/components/app-nav";
import {
  extractRFQ,
  estimateRFQ,
  type RFQExtractResponse,
  type RFQLineItemResult,
  type RFQEstimateResponse,
  type RFQLineItemEstimate,
} from "@/lib/api";

type Step = "upload" | "extracting" | "review" | "estimating" | "result";

const DOC_TYPE_LABEL: Record<string, string> = {
  rfq: "Request for Quotation",
  drawing: "Engineering Drawing",
  contract: "Contract / PO",
  spec_sheet: "Spec / Tech Sheet",
  other: "Unknown Document",
};

const CONFIDENCE_COLOR: Record<string, string> = {
  high: "bg-emerald-950/60 text-emerald-400 border-emerald-800",
  medium: "bg-amber-950/60 text-amber-400 border-amber-800",
  low: "bg-red-950/60 text-red-400 border-red-800",
};

function fmt(n: number) {
  return n.toLocaleString("en-IN", { maximumFractionDigits: 0 });
}

export default function RFQNewPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [step, setStep] = useState<Step>("upload");
  const [error, setError] = useState("");

  // upload step
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  // extract result
  const [extracted, setExtracted] = useState<RFQExtractResponse | null>(null);
  // editable line items (copy for editing)
  const [lineItems, setLineItems] = useState<RFQLineItemResult[]>([]);

  // estimate result
  const [estimateResult, setEstimateResult] = useState<RFQEstimateResponse | null>(null);

  function handleFileSelect(f: File) {
    if (f.type !== "application/pdf") {
      setError("Only PDF files are accepted.");
      return;
    }
    setError("");
    setFile(f);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFileSelect(f);
  }

  async function handleExtract() {
    if (!file) return;
    setStep("extracting");
    setError("");
    try {
      const result = await extractRFQ(file);
      setExtracted(result);
      setLineItems(result.line_items.map((item) => ({ ...item })));
      setStep("review");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed. Please try again.");
      setStep("upload");
    }
  }

  async function handleEstimate() {
    setStep("estimating");
    setError("");
    try {
      const result = await estimateRFQ(lineItems);
      setEstimateResult(result);
      setStep("result");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Estimation failed. Please try again.");
      setStep("review");
    }
  }

  function updateItem(index: number, field: keyof RFQLineItemResult, value: unknown) {
    setLineItems((prev) => prev.map((item, i) => (i === index ? { ...item, [field]: value } : item)));
  }

  function removeItem(index: number) {
    setLineItems((prev) => prev.filter((_, i) => i !== index));
  }

  // ── UPLOAD STEP ──────────────────────────────────────────────────────────
  if (step === "upload") {
    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav>
          <button
            onClick={() => router.push("/dashboard")}
            className="text-[#64748B] hover:text-[#94A3B8] text-sm font-medium transition-colors py-2 px-3"
          >
            ← Dashboard
          </button>
        </AppNav>
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 className="text-3xl font-semibold tracking-tight mb-1">RFQ Extractor</h1>
          <p className="text-[#64748B] text-sm mb-8">Upload a customer RFQ PDF — extract all line items and get should-cost for each part in seconds.</p>

          {error && (
            <div role="alert" className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-6">
              {error}
            </div>
          )}

          <div
            className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors ${
              dragging ? "border-[#22D3EE] bg-[#22D3EE]/5" : "border-[#2A3140] hover:border-[#3A4150] bg-[#161B27]"
            }`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="w-14 h-14 bg-[#22D3EE]/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-[#22D3EE]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            {file ? (
              <div>
                <p className="text-[#E2E8F0] font-medium mb-1">{file.name}</p>
                <p className="text-[#64748B] text-sm">{(file.size / 1024).toFixed(0)} KB · Click to change</p>
              </div>
            ) : (
              <div>
                <p className="text-[#E2E8F0] font-medium mb-1">Drop RFQ PDF here</p>
                <p className="text-[#64748B] text-sm">or click to browse · PDF only · max 20MB</p>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFileSelect(f); }}
            />
          </div>

          {file && (
            <button
              onClick={handleExtract}
              className="mt-6 w-full bg-[#22D3EE] text-[#0F1117] py-4 rounded-xl font-semibold text-base hover:bg-[#06B6D4] transition-colors"
            >
              Extract Line Items →
            </button>
          )}
        </div>
      </div>
    );
  }

  // ── EXTRACTING STEP ──────────────────────────────────────────────────────
  if (step === "extracting") {
    return (
      <div className="min-h-screen bg-[#0F1117] flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-[#2A3140] border-t-[#22D3EE] rounded-full animate-spin mx-auto mb-4" />
          <p className="text-[#E2E8F0] font-medium">Extracting RFQ line items...</p>
          <p className="text-[#64748B] text-sm mt-1">Reading PDF and identifying parts</p>
        </div>
      </div>
    );
  }

  // ── REVIEW STEP ──────────────────────────────────────────────────────────
  if (step === "review" && extracted) {
    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav>
          <button
            onClick={() => { setStep("upload"); setExtracted(null); setLineItems([]); }}
            className="text-[#64748B] hover:text-[#94A3B8] text-sm font-medium transition-colors py-2 px-3"
          >
            ← Upload Again
          </button>
        </AppNav>
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-8">
          {/* Document meta */}
          <div className="bg-[#161B27] border border-[#2A3140] rounded-xl p-5 mb-6">
            <div className="flex flex-wrap gap-4 items-start justify-between">
              <div>
                <h1 className="text-xl font-semibold text-[#E2E8F0] mb-1">
                  {extracted.rfq_number ? `RFQ ${extracted.rfq_number}` : "RFQ Document"}
                </h1>
                <div className="flex flex-wrap gap-3 text-sm text-[#64748B]">
                  {extracted.customer && <span>Customer: <span className="text-[#94A3B8]">{extracted.customer}</span></span>}
                  {extracted.date && <span>Date: <span className="text-[#94A3B8]">{extracted.date}</span></span>}
                  <span>{extracted.page_count} page{extracted.page_count !== 1 ? "s" : ""}</span>
                </div>
              </div>
              <div className="flex gap-2 items-center">
                <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${CONFIDENCE_COLOR[extracted.confidence] || CONFIDENCE_COLOR.low}`} style={{ fontFamily: "var(--font-mono)" }}>
                  {extracted.confidence} confidence
                </span>
                <span className="px-2.5 py-1 rounded-full text-xs font-semibold border bg-[#1C2235] text-[#94A3B8] border-[#2A3140]" style={{ fontFamily: "var(--font-mono)" }}>
                  {DOC_TYPE_LABEL[extracted.document_type] || extracted.document_type}
                </span>
              </div>
            </div>
          </div>

          {error && (
            <div role="alert" className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-6">
              {error}
            </div>
          )}

          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-[#E2E8F0]">
              Line Items <span className="text-[#475569] font-normal text-sm ml-2" style={{ fontFamily: "var(--font-mono)" }}>{lineItems.length} extracted</span>
            </h2>
          </div>

          {lineItems.length === 0 ? (
            <div className="bg-[#161B27] border border-[#2A3140] rounded-xl p-10 text-center mb-6">
              <p className="text-[#94A3B8] mb-1">No line items extracted</p>
              <p className="text-[#475569] text-sm">The PDF may not be an RFQ, or the text may not be machine-readable.</p>
            </div>
          ) : (
            <div className="space-y-3 mb-6">
              {lineItems.map((item, index) => (
                <div
                  key={item.line_number}
                  className="animate-fade-in-up"
                  style={{ animationDelay: `${Math.min(index * 40, 300)}ms` }}
                >
                  <ReviewLineItem
                    item={item}
                    index={index}
                    onChange={updateItem}
                    onRemove={removeItem}
                  />
                </div>
              ))}
            </div>
          )}

          {lineItems.length > 0 && (
            <button
              onClick={handleEstimate}
              className="w-full bg-[#22D3EE] text-[#0F1117] py-4 rounded-xl font-semibold text-base hover:bg-[#06B6D4] transition-colors"
            >
              Run Should-Cost on All {lineItems.length} Parts →
            </button>
          )}
        </div>
      </div>
    );
  }

  // ── ESTIMATING STEP ──────────────────────────────────────────────────────
  if (step === "estimating") {
    return (
      <div className="min-h-screen bg-[#0F1117] flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-[#2A3140] border-t-[#22D3EE] rounded-full animate-spin mx-auto mb-4" />
          <p className="text-[#E2E8F0] font-medium">Running should-cost on {lineItems.length} parts...</p>
          <p className="text-[#64748B] text-sm mt-1">Physics engine calculating each line item</p>
        </div>
      </div>
    );
  }

  // ── RESULT STEP ──────────────────────────────────────────────────────────
  if (step === "result" && estimateResult && extracted) {
    const failed = estimateResult.line_items.filter((i) => i.error);
    return (
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav>
          <button
            onClick={() => { setStep("review"); setEstimateResult(null); }}
            className="text-[#64748B] hover:text-[#94A3B8] text-sm font-medium transition-colors py-2 px-3"
          >
            ← Back to Review
          </button>
        </AppNav>
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-8">
          {/* Summary header */}
          <div className="bg-[#161B27] border border-[#2A3140] rounded-xl p-6 mb-6">
            <div className="flex flex-wrap gap-4 items-center justify-between">
              <div>
                <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                  {extracted.rfq_number ? `RFQ ${extracted.rfq_number}` : "Quote Sheet"}
                  {extracted.customer ? ` · ${extracted.customer}` : ""}
                </p>
                <p className="text-[#E2E8F0] text-sm">
                  {estimateResult.line_items.length} parts estimated
                  {failed.length > 0 && <span className="text-amber-400 ml-2">({failed.length} failed)</span>}
                </p>
              </div>
              <div className="text-right">
                <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Total Order Value</p>
                <p className="text-3xl font-semibold text-[#22D3EE]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
                  ₹{fmt(estimateResult.total_order_cost)}
                </p>
              </div>
            </div>
          </div>

          {/* Quote table */}
          <div className="animate-scale-in bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden overflow-x-auto mb-6">
            <table className="w-full min-w-[700px]">
              <thead>
                <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                  <th className="text-left px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider w-8" style={{ fontFamily: "var(--font-mono)" }}>#</th>
                  <th className="text-left px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider">Description</th>
                  <th className="text-left px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider">Material</th>
                  <th className="text-right px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Qty</th>
                  <th className="text-right px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Unit (₹)</th>
                  <th className="text-right px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Total (₹)</th>
                  <th className="text-center px-4 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Conf.</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A3140]">
                {estimateResult.line_items.map((item) => (
                  <QuoteRow key={item.line_number} item={item} />
                ))}
              </tbody>
              <tfoot>
                <tr className="border-t-2 border-[#2A3140] bg-[#1C2235]">
                  <td colSpan={5} className="px-4 py-4 text-right text-sm font-semibold text-[#E2E8F0]">Total Order Value</td>
                  <td className="px-4 py-4 text-right font-bold text-[#22D3EE]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
                    ₹{fmt(estimateResult.total_order_cost)}
                  </td>
                  <td />
                </tr>
              </tfoot>
            </table>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => router.push("/dashboard")}
              className="flex-1 bg-[#161B27] border border-[#2A3140] text-[#94A3B8] py-3 rounded-xl font-medium hover:bg-[#1C2235] transition-colors"
            >
              Dashboard
            </button>
            <button
              onClick={() => { setStep("upload"); setFile(null); setExtracted(null); setLineItems([]); setEstimateResult(null); }}
              className="flex-1 bg-[#22D3EE] text-[#0F1117] py-3 rounded-xl font-semibold hover:bg-[#06B6D4] transition-colors"
            >
              New RFQ
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

// ── Sub-components ──────────────────────────────────────────────────────────

interface ReviewLineItemProps {
  item: RFQLineItemResult;
  index: number;
  onChange: (index: number, field: keyof RFQLineItemResult, value: unknown) => void;
  onRemove: (index: number) => void;
}

function ReviewLineItem({ item, index, onChange, onRemove }: ReviewLineItemProps) {
  const [open, setOpen] = useState(false);
  const [qtyStr, setQtyStr] = useState(String(item.quantity));

  function dimSummary() {
    const d = item.dimensions || {};
    const parts: string[] = [];
    if (d.outer_diameter_mm != null) parts.push(`Ø${d.outer_diameter_mm}mm`);
    if (d.length_mm != null) parts.push(`L${d.length_mm}mm`);
    if (d.width_mm != null) parts.push(`W${d.width_mm}mm`);
    if (d.height_mm != null) parts.push(`H${d.height_mm}mm`);
    return parts.length ? parts.join(" × ") : "No dimensions";
  }

  return (
    <div className="bg-[#161B27] border border-[#2A3140] rounded-xl overflow-hidden">
      <button
        className="w-full flex items-center gap-4 px-5 py-4 text-left hover:bg-[#1C2235] transition-colors"
        onClick={() => setOpen((o) => !o)}
      >
        <span className="text-xs font-medium text-[#475569] w-5 shrink-0" style={{ fontFamily: "var(--font-mono)" }}>
          {item.line_number}
        </span>
        <div className="flex-1 min-w-0">
          <p className="text-[#E2E8F0] text-sm font-medium truncate">{item.description}</p>
          <p className="text-[#475569] text-xs mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>
            {item.material || "Material TBD"} · Qty {item.quantity} · {dimSummary()}
          </p>
        </div>
        <svg
          className={`w-4 h-4 text-[#475569] shrink-0 transition-transform ${open ? "rotate-180" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="px-5 pb-5 border-t border-[#2A3140] pt-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1.5">Description</label>
              <input
                type="text"
                value={item.description}
                onChange={(e) => onChange(index, "description", e.target.value)}
                className="w-full bg-[#0F1117] border border-[#2A3140] rounded-lg px-3 py-2 text-sm text-[#E2E8F0] focus:outline-none focus:border-[#22D3EE]"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1.5">Material</label>
              <input
                type="text"
                value={item.material || ""}
                onChange={(e) => onChange(index, "material", e.target.value || null)}
                placeholder="e.g. SS304, EN8, Al6061"
                className="w-full bg-[#0F1117] border border-[#2A3140] rounded-lg px-3 py-2 text-sm text-[#E2E8F0] focus:outline-none focus:border-[#22D3EE] placeholder-[#475569]"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1.5">Quantity</label>
              <input
                type="number"
                min={1}
                value={qtyStr}
                onChange={(e) => {
                  setQtyStr(e.target.value);
                  const n = parseInt(e.target.value);
                  if (!isNaN(n) && n >= 1) onChange(index, "quantity", n);
                }}
                onBlur={() => {
                  const n = parseInt(qtyStr);
                  const valid = isNaN(n) || n < 1 ? 1 : n;
                  setQtyStr(String(valid));
                  onChange(index, "quantity", valid);
                }}
                className="w-full bg-[#0F1117] border border-[#2A3140] rounded-lg px-3 py-2 text-sm text-[#E2E8F0] focus:outline-none focus:border-[#22D3EE]"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-[#64748B] mb-1.5">Delivery (weeks)</label>
              <input
                type="number"
                min={1}
                value={item.delivery_weeks ?? ""}
                onChange={(e) => onChange(index, "delivery_weeks", e.target.value ? parseInt(e.target.value) : null)}
                placeholder="e.g. 4"
                className="w-full bg-[#0F1117] border border-[#2A3140] rounded-lg px-3 py-2 text-sm text-[#E2E8F0] focus:outline-none focus:border-[#22D3EE] placeholder-[#475569]"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>
          </div>

          {/* Dimensions */}
          <p className="text-xs font-medium text-[#64748B] mb-2">Dimensions (mm) — edit if extracted incorrectly</p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            {(["outer_diameter_mm", "length_mm", "width_mm", "height_mm"] as const).map((key) => (
              <div key={key}>
                <label className="block text-xs text-[#475569] mb-1">
                  {key.replace(/_mm$/, "").replace(/_/g, " ")}
                </label>
                <input
                  type="number"
                  min={0}
                  step={0.1}
                  value={(item.dimensions as Record<string, number | null>)[key] ?? ""}
                  onChange={(e) =>
                    onChange(index, "dimensions", {
                      ...item.dimensions,
                      [key]: e.target.value ? parseFloat(e.target.value) : null,
                    })
                  }
                  placeholder="—"
                  className="w-full bg-[#0F1117] border border-[#2A3140] rounded-lg px-3 py-2 text-sm text-[#E2E8F0] focus:outline-none focus:border-[#22D3EE] placeholder-[#475569]"
                  style={{ fontFamily: "var(--font-mono)" }}
                />
              </div>
            ))}
          </div>

          {item.notes && (
            <p className="text-xs text-[#64748B] mb-4">
              <span className="text-[#475569]">Notes: </span>{item.notes}
            </p>
          )}

          <button
            onClick={() => onRemove(index)}
            className="text-xs text-red-400 hover:text-red-300 transition-colors"
          >
            Remove this line item
          </button>
        </div>
      )}
    </div>
  );
}

function QuoteRow({ item }: { item: RFQLineItemEstimate }) {
  const confColor = item.confidence_tier ? CONFIDENCE_COLOR[item.confidence_tier] || "" : "";

  return (
    <tr className="hover:bg-[#1C2235] transition-colors">
      <td className="px-4 py-4 text-xs text-[#475569]" style={{ fontFamily: "var(--font-mono)" }}>{item.line_number}</td>
      <td className="px-4 py-4">
        <p className="text-sm text-[#E2E8F0] font-medium">{item.description}</p>
        {item.part_number && (
          <p className="text-xs text-[#475569] mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>
            PN: {item.part_number}
          </p>
        )}
        {item.error && (
          <p className="text-xs text-amber-400 mt-0.5">{item.error}</p>
        )}
      </td>
      <td className="px-4 py-4 text-sm text-[#94A3B8]">{item.material || "—"}</td>
      <td className="px-4 py-4 text-sm text-right text-[#94A3B8]" style={{ fontFamily: "var(--font-mono)" }}>{item.quantity}</td>
      <td className="px-4 py-4 text-sm text-right text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
        {item.error ? "—" : `₹${fmt(item.unit_cost)}`}
      </td>
      <td className="px-4 py-4 text-sm text-right font-semibold text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
        {item.error ? "—" : `₹${fmt(item.order_cost)}`}
      </td>
      <td className="px-4 py-4 text-center">
        {item.confidence_tier ? (
          <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold border ${confColor}`} style={{ fontFamily: "var(--font-mono)" }}>
            {item.confidence_tier}
          </span>
        ) : (
          <span className="text-[#475569] text-xs">—</span>
        )}
      </td>
    </tr>
  );
}
