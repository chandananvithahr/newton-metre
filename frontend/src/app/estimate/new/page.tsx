"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  extractDrawing,
  extractMultiViewDrawing,
  createEstimate,
  createAssemblyEstimate,
  getMaterialPrice,
} from "@/lib/api";
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

const JOINING_METHODS = [
  { id: "mig_welding",  label: "MIG Welding" },
  { id: "tig_welding",  label: "TIG Welding" },
  { id: "spot_welding", label: "Spot Welding" },
  { id: "bolting",      label: "Bolting (Nut & Bolt)" },
  { id: "riveting",     label: "Riveting" },
  { id: "press_fit",    label: "Press Fit / Interference Fit" },
];

type DrawingType = "single" | "assembly";

type Step =
  | "type"
  | "upload"
  | "extracting"
  | "review"
  | "calculating"
  | "result"
  | "assembly-upload"
  | "assembly-extracting"
  | "assembly-review"
  | "assembly-joining"
  | "assembly-result";

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
  unit_cost_low: number;
  unit_cost_high: number;
  uncertainty_pct: number;
  order_cost: number;
  quantity: number;
  confidence_tier: string | null;
  currency: string;
}

interface AssemblyComponent {
  id: string;
  file: File;
  name: string;
  extractedData: Record<string, unknown> | null;
  materialOverride: string;
  customMaterial: string;
  error: string;
}

interface ComponentCostResult {
  name: string;
  material_name: string;
  material_cost: number;
  machining_cost: number;
  setup_cost: number;
  tooling_cost: number;
  labour_cost: number;
  power_cost: number;
  subtotal: number;
  unit_cost: number;
}

interface AssemblyResult {
  components: ComponentCostResult[];
  joining_cost: number;
  joining_method_label: string;
  joining_material_cost: number;
  joining_machine_cost: number;
  joining_labour_cost: number;
  assembly_subtotal: number;
  overhead: number;
  profit: number;
  unit_cost: number;
  order_cost: number;
  quantity: number;
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

  // Shared
  const [step, setStep] = useState<Step>("type");
  const [drawingType, setDrawingType] = useState<DrawingType>("single");
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");

  // Single-part state
  const [file, setFile] = useState<File | null>(null);
  const [extraSheets, setExtraSheets] = useState<File[]>([]); // additional views/sheets of the same part
  const [extractedData, setExtractedData] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<EstimateResult | null>(null);
  const [expanded, setExpanded] = useState(false);
  const [materialOverride, setMaterialOverride] = useState("");
  const [customMaterial, setCustomMaterial] = useState("");
  const [materialPrice, setMaterialPrice] = useState<{ price_inr: number; source: string } | null>(null);
  const [fetchingPrice, setFetchingPrice] = useState(false);
  const [supplierQuoteStr, setSupplierQuoteStr] = useState("");
  const [supplierQuoteSaved, setSupplierQuoteSaved] = useState(false);

  // Assembly state
  const [asmComponents, setAsmComponents] = useState<AssemblyComponent[]>([]);
  const [currentExtractingIdx, setCurrentExtractingIdx] = useState(0);
  const [joiningMethod, setJoiningMethod] = useState("mig_welding");
  const [numJoints, setNumJoints] = useState(4);
  const [assemblyResult, setAssemblyResult] = useState<AssemblyResult | null>(null);
  const [expandedComponent, setExpandedComponent] = useState<string | null>(null);

  // ─── Helpers ──────────────────────────────────────────────────────────────

  function fmt(n: number) {
    return n.toLocaleString("en-IN", { maximumFractionDigits: 0 });
  }

  function confidenceBadge(tier: string | null) {
    if (!tier) return null;
    const styles: Record<string, string> = {
      high:         "bg-emerald-50 text-emerald-700 border-emerald-200",
      medium:       "bg-amber-50 text-amber-700 border-amber-200",
      low:          "bg-red-50 text-red-700 border-red-200",
      insufficient: "bg-[var(--color-surface-hover)] text-[var(--color-text-description)] border-black/20",
    };
    return (
      <span
        className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${styles[tier] ?? styles.insufficient}`}
        style={{ fontFamily: "var(--font-mono)" }}
      >
        {tier.toUpperCase()} confidence
      </span>
    );
  }

  function newAsmComponent(file: File): AssemblyComponent {
    const stem = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ").trim();
    return {
      id: Math.random().toString(36).slice(2),
      file,
      name: stem || `Component ${asmComponents.length + 1}`,
      extractedData: null,
      materialOverride: "",
      customMaterial: "",
      error: "",
    };
  }

  function updateAsmComponent(id: string, patch: Partial<AssemblyComponent>) {
    setAsmComponents((prev) =>
      prev.map((c) => (c.id === id ? { ...c, ...patch } : c))
    );
  }

  // ─── Single-part handlers ─────────────────────────────────────────────────

  async function handleUpload() {
    if (!file) return;
    setError("");
    setStep("extracting");
    try {
      const allSheets = [file, ...extraSheets];
      const data = allSheets.length > 1
        ? await extractMultiViewDrawing(allSheets)
        : await extractDrawing(file);
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
    const name =
      materialOverride === "__custom__" ? customMaterial.trim() : materialOverride;
    if (!name) return;
    setFetchingPrice(true);
    setMaterialPrice(null);
    try {
      const res = await getMaterialPrice(name);
      setMaterialPrice({ price_inr: res.price_inr, source: res.source });
    } catch {
      // non-critical
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
    const parsedQuote = supplierQuoteStr ? parseFloat(supplierQuoteStr) : undefined;
    try {
      const est = await createEstimate(dataToSend, quantity, parsedQuote);
      setResult(est);
      setSupplierQuoteSaved(!!parsedQuote);
      setStep("result");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Calculation failed");
      setStep("review");
    }
  }

  // ─── Assembly handlers ────────────────────────────────────────────────────

  async function handleAsmFilesAdded(files: FileList | null) {
    if (!files) return;
    const DRAWING_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".dxf", ".dwg", ".step", ".stp", ".tiff", ".webp"];
    const allFiles: File[] = [];

    for (const f of Array.from(files)) {
      if (f.name.toLowerCase().endsWith(".zip")) {
        try {
          const JSZip = (await import("jszip")).default;
          const zip = await JSZip.loadAsync(f);
          const entries = Object.values(zip.files).filter(
            (entry) => !entry.dir && DRAWING_EXTS.some((ext) => entry.name.toLowerCase().endsWith(ext))
          );
          for (const entry of entries) {
            const blob = await entry.async("blob");
            const name = entry.name.split("/").pop() || entry.name;
            allFiles.push(new File([blob], name, { type: blob.type || "application/octet-stream" }));
          }
        } catch {
          setError(`Failed to extract ${f.name}. Make sure it's a valid ZIP file.`);
        }
      } else {
        allFiles.push(f);
      }
    }

    if (allFiles.length > 0) {
      const next = allFiles.map(newAsmComponent);
      setAsmComponents((prev) => [...prev, ...next]);
    }
  }

  function handleAsmRemoveComponent(id: string) {
    setAsmComponents((prev) => prev.filter((c) => c.id !== id));
  }

  async function handleAsmExtractAll() {
    setError("");
    setCurrentExtractingIdx(0);
    setStep("assembly-extracting");

    const updated = [...asmComponents];
    for (let i = 0; i < updated.length; i++) {
      setCurrentExtractingIdx(i);
      try {
        const data = await extractDrawing(updated[i].file);
        updated[i] = { ...updated[i], extractedData: data, error: "" };
      } catch (e) {
        updated[i] = {
          ...updated[i],
          extractedData: null,
          error: e instanceof Error ? e.message : "Extraction failed",
        };
      }
      setAsmComponents([...updated]);
    }
    setStep("assembly-review");
  }

  async function handleAsmCalculate() {
    setError("");
    setStep("calculating");

    const components = asmComponents.map((c) => {
      const extracted = { ...c.extractedData } as Record<string, unknown>;
      const effectiveMaterial =
        c.materialOverride === "__custom__"
          ? c.customMaterial.trim() || null
          : c.materialOverride || (extracted.material as string | null);
      if (effectiveMaterial) extracted.material = effectiveMaterial;
      return { name: c.name, extracted_data: extracted };
    });

    try {
      const res = await createAssemblyEstimate(
        components,
        joiningMethod,
        numJoints,
        quantity,
      );
      setAssemblyResult(res);
      setStep("assembly-result");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Assembly calculation failed");
      setStep("assembly-joining");
    }
  }

  // ─── Shared UI ────────────────────────────────────────────────────────────

  const SINGLE_STEPS = ["Upload", "Review", "Result"];
  const ASM_STEPS = ["Upload", "Review", "Joining", "Result"];

  function stepIndex(): number {
    if (step === "type" || step === "upload" || step === "assembly-upload") return 0;
    if (step === "extracting" || step === "assembly-extracting" || step === "review" || step === "assembly-review") return 1;
    if (step === "calculating" || step === "assembly-joining") return 2;
    if (step === "result") return 2;
    if (step === "assembly-result") return 3;
    return 0;
  }

  function StepProgress() {
    const steps = drawingType === "assembly" ? ASM_STEPS : SINGLE_STEPS;
    const current = stepIndex();
    return (
      <div className="flex items-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              i < current ? "bg-[var(--color-brand-dark)]/5 text-[var(--color-neutral-gray)]" :
              i === current ? "bg-[var(--color-brand-dark)] text-white" :
              "bg-[var(--color-surface-container)] text-[var(--color-text-muted)]"
            }`} style={{ fontFamily: "var(--font-mono)" }}>
              {i < current ? (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}><path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
              ) : (
                <span>{i + 1}</span>
              )}
              {s}
            </div>
            {i < steps.length - 1 && (
              <div className={`w-8 h-px ${i < current ? "bg-[var(--color-brand-dark)]/40" : "bg-[#c4c5d5]/20"}`} />
            )}
          </div>
        ))}
      </div>
    );
  }

  function MissionLog({ lines, subtitle }: { lines: string[]; subtitle?: string }) {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <StepProgress />
          <div className="bg-white rounded-xl ghost-border ambient-shadow p-10">
            <p className="text-sm font-medium text-[var(--color-text-primary)] mb-1">Newton-Metre is working...</p>
            <p className="text-xs text-[var(--color-text-muted)] mb-6">{subtitle || "Sit back — this takes a few seconds."}</p>
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
                      <span className="w-4 h-4 border-2 border-black/20 border-t-[var(--color-brand-dark)] rounded-full animate-spin shrink-0" />
                    ) : (
                      <span className="text-emerald-500 text-base leading-none shrink-0">✓</span>
                    )}
                    <span className={isLast ? "text-[var(--color-text-primary)]" : "text-[var(--color-text-muted)]"}>{line}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: type selection ─────────────────────────────────────────────────

  if (step === "type") {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 className="text-4xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>What are we costing?</h1>
          <p className="text-[var(--color-text-description)] mb-8 text-base leading-relaxed">
            Upload a drawing. Newton-Metre reads it, calculates every cost line, and hands you a negotiation-ready breakdown.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button
              onClick={() => { setDrawingType("single"); setStep("upload"); }}
              className="bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200 group"
            >
              <div className="w-12 h-12 bg-[var(--color-brand-dark)]/5 rounded-xl flex items-center justify-center mb-5 group-hover:bg-[var(--color-brand-dark)]/10 transition-colors">
                <svg className="w-6 h-6 text-[var(--color-brand-dark)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">Single Part</h2>
              <p className="text-sm text-[var(--color-text-description)]">
                One drawing, one component — turned shaft, milled housing, sheet metal bracket, etc.
              </p>
            </button>

            <button
              onClick={() => { setDrawingType("assembly"); setStep("assembly-upload"); }}
              className="bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200 group"
            >
              <div className="w-12 h-12 bg-[var(--color-brand-dark)]/5 rounded-xl flex items-center justify-center mb-5 group-hover:bg-[var(--color-brand-dark)]/10 transition-colors">
                <svg className="w-6 h-6 text-[var(--color-brand-dark)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">Assembly</h2>
              <p className="text-sm text-[var(--color-text-description)]">
                Multiple component drawings joined by welding, bolting, riveting, or press fit.
              </p>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: single-part upload ─────────────────────────────────────────────

  if (step === "upload") {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <StepProgress />
          <button
            onClick={() => setStep("type")}
            className="flex items-center gap-2 text-[var(--color-text-muted)] hover:text-[var(--color-text-description)] text-xs mb-4 transition-colors"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            BACK
          </button>
          <h1 className="text-4xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Upload your drawing</h1>
          <p className="text-[var(--color-text-description)] mb-8 text-base leading-relaxed">Newton-Metre will read the drawing, extract dimensions, material, and processes — no templates, no manual entry.</p>

          <div className="bg-white rounded-xl ghost-border p-8">

            {/* Sheet 1 — primary drawing */}
            <p className="text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider mb-2" style={{ fontFamily: "var(--font-mono)" }}>
              Sheet 1 {extraSheets.length === 0 ? "(required)" : ""}
            </p>
            <div
              className="border-2 border-dashed border-black/20 rounded-xl p-8 text-center mb-4 hover:border-[var(--color-nm-primary)]/30 hover:bg-[var(--color-brand-dark)]/10/5 transition-colors cursor-pointer"
              role="button"
              tabIndex={0}
              onClick={() => document.getElementById("file-input")?.click()}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("file-input")?.click(); } }}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); }}
              onDragLeave={(e) => { e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); }}
              onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); const f = e.dataTransfer.files[0]; if (f) setFile(f); }}
            >
              {file ? (
                <p className="text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{file.name}</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-[var(--color-text-description)] mb-1">Click to upload or drag and drop</p>
                  <p className="text-xs text-[var(--color-text-muted)]">PDF · DXF · DWG · STEP · PNG · JPG (max 20MB)</p>
                </>
              )}
              <input id="file-input" type="file" accept=".pdf,.png,.jpg,.jpeg,.dxf,.dwg,.step,.stp" onChange={(e) => setFile(e.target.files?.[0] || null)} className="hidden" />
            </div>

            {/* Extra sheets */}
            {extraSheets.map((sheet, idx) => (
              <div key={idx} className="flex items-center gap-3 bg-[var(--color-surface-hover)] border border-black/20 rounded-lg px-4 py-3 mb-2">
                <svg className="w-4 h-4 text-[var(--color-text-muted)] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5" />
                </svg>
                <span className="text-xs text-[var(--color-text-description)] font-medium shrink-0" style={{ fontFamily: "var(--font-mono)" }}>Sheet {idx + 2}</span>
                <span className="text-sm text-[var(--color-text-primary)] truncate flex-1" style={{ fontFamily: "var(--font-mono)" }}>{sheet.name}</span>
                <button
                  onClick={() => setExtraSheets((prev) => prev.filter((_, i) => i !== idx))}
                  className="text-[var(--color-text-muted)] hover:text-red-400 transition-colors shrink-0"
                  aria-label="Remove sheet"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}

            {/* Add sheet button */}
            {file && extraSheets.length < 4 && (
              <div className="mb-4">
                <button
                  onClick={() => document.getElementById("extra-sheet-input")?.click()}
                  className="flex items-center gap-2 text-[var(--color-brand-dark)] text-sm hover:text-[var(--color-neutral-gray)] transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                  </svg>
                  Add another view / sheet
                </button>
                <input
                  id="extra-sheet-input"
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg,.dxf,.dwg,.step,.stp"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) setExtraSheets((prev) => [...prev, f]);
                    e.target.value = "";
                  }}
                />
                {extraSheets.length > 0 && (
                  <p className="text-xs text-[var(--color-text-muted)] mt-1">All sheets must be views of the same part — mismatched drawings will be rejected.</p>
                )}
              </div>
            )}

            <div className="flex items-center gap-4 mb-6">
              <label className="text-sm font-medium text-[var(--color-text-description)]">Quantity:</label>
              <input
                type="text" inputMode="numeric" pattern="[0-9]*"
                value={quantity === 0 ? "" : quantity}
                onChange={(e) => {
                  const raw = e.target.value.replace(/[^0-9]/g, "");
                  setQuantity(raw === "" ? 0 : parseInt(raw));
                }}
                onFocus={(e) => e.target.select()}
                onBlur={() => { if (quantity === 0) setQuantity(1); }}
                placeholder="e.g. 500"
                className="w-28 px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] outline-none text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-disabled)] [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>

            {error && <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">{error}</div>}

            <button
              onClick={handleUpload}
              disabled={!file}
              className="w-full bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200"
            >
              {extraSheets.length > 0 ? `Analyze ${extraSheets.length + 1} Sheets` : "Analyze Drawing"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (step === "extracting") return <MissionLog lines={EXTRACT_LOG} subtitle="Reading your drawing and extracting every detail automatically." />;

  // ─── Step: single-part review ─────────────────────────────────────────────

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
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-8">
          <StepProgress />
          <h1 className="text-4xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Here&apos;s what we found</h1>
          <p className="text-[var(--color-text-description)] text-base mb-6 leading-relaxed">Newton-Metre extracted these details from your drawing. Confirm and we&apos;ll calculate the should-cost.</p>

          <div className="bg-white rounded-xl border border-black/20 p-6 mb-4">
            <h2 className="text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider mb-4" style={{ fontFamily: "var(--font-mono)" }}>Dimensions</h2>
            <table className="w-full">
              <tbody>
                {Object.entries(dims).map(([key, val]) =>
                  val != null ? (
                    <tr key={key} className="border-b border-black/20 last:border-0">
                      <td className="py-2.5 text-sm text-[var(--color-text-description)] capitalize">{key.replace(/_/g, " ")}</td>
                      <td className="py-2.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{String(val)}</td>
                    </tr>
                  ) : null
                )}
              </tbody>
            </table>
          </div>

          <div className="bg-white rounded-xl border border-black/20 p-6 mb-4">
            <div className="flex items-start justify-between mb-3">
              <span className="text-sm font-medium text-[var(--color-text-description)]">Material</span>
              {detectedMaterial !== null && matConfidence === "high" ? (
                <span className="text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{detectedMaterial}</span>
              ) : (
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${detectedMaterial === null ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-amber-50 text-amber-600 border border-amber-200"}`} style={{ fontFamily: "var(--font-mono)" }}>
                  {detectedMaterial === null ? "Not detected" : "Low confidence"}
                </span>
              )}
            </div>
            {needsMaterialInput && (
              <div className="space-y-3">
                <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2.5 text-amber-700 text-sm">
                  {detectedMaterial === null ? "Material not found in the drawing. Select from the list or enter manually." : `AI detected "${detectedMaterial}" with low confidence. Please confirm or correct it.`}
                </div>
                <select value={materialOverride} onChange={(e) => { setMaterialOverride(e.target.value); setMaterialPrice(null); }} className="w-full px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none">
                  <option value="">{detectedMaterial !== null ? `Keep detected: ${detectedMaterial}` : "— Select material —"}</option>
                  {KNOWN_MATERIALS.map((m) => <option key={m} value={m}>{m}</option>)}
                  <option value="__custom__">Other (enter manually)…</option>
                </select>
                {materialOverride === "__custom__" && (
                  <input type="text" placeholder="e.g. EN31 Steel, Bronze, AISI 4140" value={customMaterial} onChange={(e) => { setCustomMaterial(e.target.value); setMaterialPrice(null); }} className="w-full px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none" />
                )}
                <div className="flex items-center gap-3">
                  <button onClick={handleFetchPrice} disabled={!activeMaterial || fetchingPrice} className="text-sm text-[var(--color-brand-dark)] hover:text-[var(--color-neutral-gray)] font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                    {fetchingPrice ? "Fetching…" : "Look up market price (INR/kg)"}
                  </button>
                  {materialPrice !== null && (
                    <span className="text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>
                      ₹{materialPrice.price_inr.toLocaleString("en-IN")}/kg
                      <span className="text-xs text-[var(--color-text-muted)] ml-1">({materialPrice.source})</span>
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>

          <div className="bg-white rounded-xl border border-black/20 p-6 mb-6 space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-[var(--color-text-description)]">Processes</span>
              <span className="text-sm font-medium text-[var(--color-text-primary)]">{(extractedData.suggested_processes as string[] || []).join(", ")}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-[var(--color-text-description)]">AI Confidence</span>
              <span className="text-sm font-medium text-[var(--color-text-primary)] capitalize">{String(extractedData.confidence || "—")}</span>
            </div>
          </div>

          {error && <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">{error}</div>}

          <div className="flex gap-3">
            <button onClick={handleCalculate} disabled={needsMaterialInput && !activeMaterial} className="flex-1 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200">
              Calculate Cost
            </button>
            <button onClick={() => setStep("upload")} className="px-6 py-3.5 border border-black/20 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors">
              Re-upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (step === "calculating") return <MissionLog lines={CALC_LOG} subtitle="Running physics-based cost models with real Indian manufacturing rates." />;

  // ─── Step: single-part result ─────────────────────────────────────────────

  if (step === "result" && result) {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
          <StepProgress />
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-4xl tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Your should-cost is ready</h1>
              <p className="text-[var(--color-text-description)] text-base mt-1 leading-relaxed">{result.material_name} · {result.quantity} unit{result.quantity > 1 ? "s" : ""} — use this breakdown to negotiate line by line.</p>
            </div>
            {confidenceBadge(result.confidence_tier)}
          </div>

          {/* Uncertainty band callout */}
          <div className="bg-white border border-black/20 rounded-xl px-6 py-5 mb-4">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-xs text-[var(--color-text-description)] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Should-Cost Range (±{result.uncertainty_pct}%)</p>
                <p className="text-2xl font-bold text-[var(--color-brand-dark)]" style={{ fontFamily: "var(--font-mono)" }}>
                  {result.currency} {fmt(result.unit_cost_low)} – {fmt(result.unit_cost_high)}
                </p>
                <p className="text-sm text-[var(--color-text-muted)] mt-1">Physics estimate: <span className="text-[var(--color-text-description)] font-medium">{result.currency} {fmt(result.unit_cost)}</span> per unit</p>
              </div>
              {result.quantity > 1 && (
                <div className="text-right">
                  <p className="text-xs text-[var(--color-text-description)] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Order ({result.quantity} units)</p>
                  <p className="text-xl font-bold text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{result.currency} {fmt(result.order_cost)}</p>
                </div>
              )}
            </div>
            <p className="text-xs text-[var(--color-text-muted)] mt-3">Use the lower bound as your negotiation target. Supplier price above the upper bound = overpriced.</p>
          </div>

          <div className="bg-white rounded-xl border border-black/20 overflow-hidden mb-4">
            <table className="w-full">
              <thead>
                <tr className="border-b border-black/20 bg-[var(--color-surface-hover)]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Amount ({result.currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#c4c5d5]/10">
                {[
                  [`Material (${result.material_name})`, result.material_cost],
                  ["Machining", result.total_machining_cost],
                  ["Setup & Tooling", result.total_setup_cost + result.total_tooling_cost],
                  ["Labour", result.total_labour_cost],
                  ["Power", result.total_power_cost],
                  ["Overhead (15%)", result.overhead],
                  ["Profit (20%)", result.profit],
                ].map(([label, val]) => (
                  <tr key={String(label)}>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">{label}</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(Number(val))}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Supplier quote capture */}
          <div className="bg-white border border-black/20 rounded-xl px-6 py-5 mb-4">
            <p className="text-sm font-medium text-[var(--color-text-primary)] mb-1">What did the supplier actually quote?</p>
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Optional — helps us calibrate accuracy over time.</p>
            {supplierQuoteSaved ? (
              <p className="text-sm text-emerald-400 font-medium">✓ Quote saved. Thank you — this helps improve future estimates.</p>
            ) : (
              <div className="flex gap-3">
                <div className="relative flex-1">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-[var(--color-text-muted)]">₹</span>
                  <input
                    type="number"
                    min="0"
                    placeholder="e.g. 3800"
                    value={supplierQuoteStr}
                    onChange={(e) => setSupplierQuoteStr(e.target.value)}
                    className="w-full pl-7 pr-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none focus:border-[var(--color-nm-primary)]/40 transition-colors"
                  />
                </div>
                <button
                  onClick={async () => {
                    const q = parseFloat(supplierQuoteStr);
                    if (!q || !result) return;
                    try {
                      await createEstimate(extractedData!, quantity, q);
                      setSupplierQuoteSaved(true);
                    } catch { /* non-critical */ }
                  }}
                  disabled={!supplierQuoteStr || !parseFloat(supplierQuoteStr)}
                  className="px-5 py-2.5 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white rounded-lg text-sm font-bold tracking-wider uppercase disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200"
                >
                  Save
                </button>
              </div>
            )}
          </div>

          <button onClick={() => setExpanded(!expanded)} className="flex items-center gap-2 text-[var(--color-brand-dark)] hover:text-[var(--color-neutral-gray)] text-sm font-medium mb-4 transition-colors">
            <svg className={`w-4 h-4 transition-transform ${expanded ? "rotate-90" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
            {expanded ? "Hide" : "Show"} full process breakdown
          </button>

          {expanded && (
            <div className="bg-white rounded-xl border border-black/20 overflow-hidden mb-6 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-black/20 bg-[var(--color-surface-hover)]">
                    {["Process", "Time", "Machine", "Setup", "Tooling", "Labour", "Power"].map((h) => (
                      <th key={h} className={`${h === "Process" ? "text-left" : "text-right"} px-4 py-3 text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider`} style={{ fontFamily: "var(--font-mono)" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#c4c5d5]/10">
                  {result.process_lines.map((pl) => (
                    <tr key={pl.process_id} className="hover:bg-[var(--color-surface-hover)] transition-colors">
                      <td className="px-4 py-3 font-medium text-[var(--color-text-primary)]">{pl.process_name}</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{pl.time_min.toFixed(1)} min</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.machine_cost)}</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.setup_cost_per_unit)}</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.tooling_cost)}</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.labour_cost)}</td>
                      <td className="px-4 py-3 text-right text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(pl.power_cost)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="flex gap-3 mt-6">
            <button onClick={() => router.push("/dashboard")} className="flex-1 border border-black/20 py-3.5 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors">
              Back to Dashboard
            </button>
            <button onClick={() => { setStep("type"); setResult(null); setExtractedData(null); setFile(null); setSupplierQuoteStr(""); setSupplierQuoteSaved(false); }} className="flex-1 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm transition-all duration-200">
              New Estimate
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: assembly upload ────────────────────────────────────────────────

  if (step === "assembly-upload") {
    const canAnalyze = asmComponents.length >= 2;
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <button onClick={() => setStep("type")} className="flex items-center gap-2 text-[var(--color-text-description)] hover:text-[var(--color-text-description)] text-sm mb-6 transition-colors">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
            Change type
          </button>

          <h1 className="text-3xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Assembly Drawing</h1>
          <p className="text-[var(--color-text-description)] mb-8 text-sm">
            Upload one drawing per component. Add at least 2 components, then label each one.
          </p>

          {/* Component list */}
          {asmComponents.length > 0 && (
            <div className="space-y-3 mb-6">
              {asmComponents.map((comp, i) => (
                <div key={comp.id} className="bg-white border border-black/20 rounded-xl px-5 py-4 flex items-center gap-4">
                  <span className="text-xs font-medium text-[var(--color-text-muted)] w-5 text-center" style={{ fontFamily: "var(--font-mono)" }}>{i + 1}</span>
                  <div className="flex-1 min-w-0">
                    <input
                      value={comp.name}
                      onChange={(e) => updateAsmComponent(comp.id, { name: e.target.value })}
                      className="w-full bg-transparent text-sm font-medium text-[var(--color-text-primary)] outline-none border-b border-transparent hover:border-black/20 focus:border-[var(--color-nm-primary)]/40 transition-colors py-0.5"
                      placeholder="Component name"
                    />
                    <p className="text-xs text-[var(--color-text-muted)] mt-1 truncate" style={{ fontFamily: "var(--font-mono)" }}>{comp.file.name}</p>
                  </div>
                  <button onClick={() => handleAsmRemoveComponent(comp.id)} className="text-[var(--color-text-muted)] hover:text-red-400 transition-colors p-1">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Add more files */}
          <div
            className="border-2 border-dashed border-black/20 rounded-xl p-8 text-center mb-6 hover:border-[var(--color-nm-primary)]/30 hover:bg-[var(--color-brand-dark)]/10/5 transition-colors cursor-pointer"
            role="button"
            tabIndex={0}
            onClick={() => document.getElementById("asm-file-input")?.click()}
            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("asm-file-input")?.click(); } }}
            onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); }}
            onDragLeave={(e) => { e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); }}
            onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40", "bg-[var(--color-brand-dark)]/5/50"); handleAsmFilesAdded(e.dataTransfer.files); }}
          >
            <div className="w-10 h-10 bg-[var(--color-brand-dark)]/5 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg className="w-5 h-5 text-[var(--color-brand-dark)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
            </div>
            <p className="text-sm text-[var(--color-text-description)]">{asmComponents.length === 0 ? "Add component drawings" : "Add more components"}</p>
            <p className="text-xs text-[var(--color-text-muted)] mt-1">PDF, PNG, DXF, DWG, STEP — or a ZIP file containing all component drawings</p>
            <input id="asm-file-input" type="file" accept=".pdf,.png,.jpg,.jpeg,.dxf,.dwg,.step,.stp,.zip" multiple onChange={(e) => handleAsmFilesAdded(e.target.files)} className="hidden" />
          </div>

          <div className="flex items-center gap-4 mb-6">
            <label className="text-sm font-medium text-[var(--color-text-description)]">Quantity (assemblies):</label>
            <input
              type="text" inputMode="numeric" pattern="[0-9]*"
              value={quantity === 0 ? "" : quantity}
              onChange={(e) => {
                const raw = e.target.value.replace(/[^0-9]/g, "");
                setQuantity(raw === "" ? 0 : parseInt(raw));
              }}
              onFocus={(e) => e.target.select()}
              onBlur={() => { if (quantity === 0) setQuantity(1); }}
              className="w-24 px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] outline-none text-sm text-[var(--color-text-primary)] [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              style={{ fontFamily: "var(--font-mono)" }}
            />
          </div>

          {!canAnalyze && asmComponents.length > 0 && (
            <p className="text-amber-400 text-sm mb-4">Add at least one more component to proceed.</p>
          )}
          {error && <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">{error}</div>}

          <button
            onClick={handleAsmExtractAll}
            disabled={!canAnalyze}
            className="w-full bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200"
          >
            Analyze All Components ({asmComponents.length})
          </button>
        </div>
      </div>
    );
  }

  // ─── Step: assembly extracting (per-file progress) ────────────────────────

  if (step === "assembly-extracting") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-full max-w-md px-8">
          <p className="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-widest mb-5" style={{ fontFamily: "var(--font-mono)" }}>
            ANALYZING ASSEMBLY
          </p>
          <div className="space-y-4">
            {asmComponents.map((comp, i) => {
              const isDone = comp.extractedData !== null || comp.error !== "";
              const isActive = i === currentExtractingIdx && !isDone;
              const isPending = i > currentExtractingIdx && !isDone;
              return (
                <div key={comp.id} className="flex items-start gap-3">
                  <div className="mt-0.5 w-5 flex-shrink-0 flex justify-center">
                    {comp.error ? (
                      <span className="text-red-400 text-base leading-none">✗</span>
                    ) : isDone ? (
                      <span className="text-emerald-400 text-base leading-none">✓</span>
                    ) : isActive ? (
                      <span className="text-[var(--color-brand-dark)] text-base leading-none">›</span>
                    ) : (
                      <span className="text-[var(--color-text-disabled)] text-base leading-none">·</span>
                    )}
                  </div>
                  <div>
                    <p className={`text-sm font-medium ${isDone && !comp.error ? "text-[var(--color-text-muted)]" : isActive ? "text-[var(--color-text-primary)]" : isPending ? "text-[var(--color-text-disabled)]" : "text-[var(--color-text-primary)]"}`} style={{ fontFamily: "var(--font-mono)" }}>
                      {comp.name}
                    </p>
                    <p className={`text-xs mt-0.5 ${comp.error ? "text-red-400" : isDone ? "text-emerald-400/60" : isActive ? "text-[var(--color-text-muted)]" : "text-[var(--color-text-disabled)]"}`} style={{ fontFamily: "var(--font-mono)" }}>
                      {comp.error ? comp.error : isDone ? "extracted" : isActive ? "extracting…" : "pending"}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: assembly review ────────────────────────────────────────────────

  if (step === "assembly-review") {
    const allExtracted = asmComponents.every((c) => c.extractedData !== null);
    const hasErrors = asmComponents.some((c) => c.error !== "");

    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-8">
          <h1 className="text-3xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Review Components</h1>
          <p className="text-[var(--color-text-description)] text-sm mb-6">
            Verify extracted data and correct materials where needed.
          </p>

          <div className="space-y-4 mb-6">
            {asmComponents.map((comp, i) => {
              const dims = (comp.extractedData?.dimensions as Record<string, unknown>) || {};
              const detectedMat = comp.extractedData?.material as string | null;
              const matConf = comp.extractedData?.material_confidence as string | undefined;
              const needsMat = detectedMat === null || matConf === "low";

              return (
                <div key={comp.id} className="bg-white border border-black/20 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setExpandedComponent(expandedComponent === comp.id ? null : comp.id)}
                    className="w-full flex items-center justify-between px-5 py-4 hover:bg-[var(--color-surface-hover)] transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-[var(--color-text-muted)] w-4 text-center" style={{ fontFamily: "var(--font-mono)" }}>{i + 1}</span>
                      <span className="text-sm font-semibold text-[var(--color-text-primary)]">{comp.name}</span>
                      {comp.error && <span className="text-xs text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full">Extraction failed</span>}
                      {needsMat && !comp.error && <span className="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full">Material needed</span>}
                    </div>
                    <svg className={`w-4 h-4 text-[var(--color-text-muted)] transition-transform ${expandedComponent === comp.id ? "rotate-180" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {expandedComponent === comp.id && (
                    <div className="px-5 pb-5 border-t border-black/20 pt-4 space-y-4">
                      {comp.error ? (
                        <p className="text-sm text-red-400">{comp.error}</p>
                      ) : (
                        <>
                          <div>
                            <p className="text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider mb-2" style={{ fontFamily: "var(--font-mono)" }}>Dimensions</p>
                            <div className="space-y-1">
                              {Object.entries(dims).filter(([, v]) => v != null).map(([k, v]) => (
                                <div key={k} className="flex justify-between text-sm">
                                  <span className="text-[var(--color-text-description)] capitalize">{k.replace(/_/g, " ")}</span>
                                  <span className="text-[var(--color-text-primary)] font-medium" style={{ fontFamily: "var(--font-mono)" }}>{String(v)}</span>
                                </div>
                              ))}
                            </div>
                          </div>

                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <p className="text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Material</p>
                              {detectedMat && matConf === "high" && (
                                <span className="text-sm text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{detectedMat}</span>
                              )}
                            </div>
                            {needsMat && (
                              <div className="space-y-2">
                                <select
                                  value={comp.materialOverride}
                                  onChange={(e) => updateAsmComponent(comp.id, { materialOverride: e.target.value })}
                                  className="w-full px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none"
                                >
                                  <option value="">{detectedMat ? `Keep: ${detectedMat}` : "— Select material —"}</option>
                                  {KNOWN_MATERIALS.map((m) => <option key={m} value={m}>{m}</option>)}
                                  <option value="__custom__">Other (enter manually)…</option>
                                </select>
                                {comp.materialOverride === "__custom__" && (
                                  <input
                                    type="text"
                                    placeholder="e.g. EN31 Steel"
                                    value={comp.customMaterial}
                                    onChange={(e) => updateAsmComponent(comp.id, { customMaterial: e.target.value })}
                                    className="w-full px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none"
                                  />
                                )}
                              </div>
                            )}
                          </div>

                          <div className="text-sm text-[var(--color-text-description)]">
                            <span className="font-medium text-[var(--color-text-description)]">Processes: </span>
                            {(comp.extractedData?.suggested_processes as string[] || []).join(", ")}
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {hasErrors && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-amber-700 text-sm mb-4">
              Some components failed extraction. Go back to re-upload those drawings.
            </div>
          )}
          {error && <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">{error}</div>}

          <div className="flex gap-3">
            <button
              onClick={() => setStep("assembly-joining")}
              disabled={!allExtracted || hasErrors}
              className="flex-1 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200"
            >
              Next: Joining Method
            </button>
            <button onClick={() => setStep("assembly-upload")} className="px-6 py-3.5 border border-black/20 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors">
              Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: assembly joining method ────────────────────────────────────────

  if (step === "assembly-joining") {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-8">
          <h1 className="text-3xl mb-2 tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Joining Method</h1>
          <p className="text-[var(--color-text-description)] text-sm mb-8">
            How are the {asmComponents.length} components joined together?
          </p>

          <div className="bg-white rounded-xl border border-black/20 p-6 mb-4 space-y-5">
            <div>
              <label className="text-sm font-medium text-[var(--color-text-description)] block mb-2">Joining process</label>
              <select
                value={joiningMethod}
                onChange={(e) => setJoiningMethod(e.target.value)}
                className="w-full px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] text-sm text-[var(--color-text-primary)] outline-none"
              >
                {JOINING_METHODS.map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-[var(--color-text-description)] block mb-2">
                {joiningMethod === "mig_welding" || joiningMethod === "tig_welding" ? "Number of weld joints" :
                 joiningMethod === "spot_welding" ? "Number of spot welds" :
                 joiningMethod === "bolting" ? "Number of bolts" :
                 joiningMethod === "riveting" ? "Number of rivets" :
                 "Number of press-fit joints"}
              </label>
              <input
                type="number"
                min={1}
                value={numJoints}
                onChange={(e) => setNumJoints(parseInt(e.target.value) || 1)}
                className="w-32 px-3 py-2.5 border border-black/20 rounded-lg bg-[var(--color-surface-hover)] outline-none text-sm text-[var(--color-text-primary)]"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>
          </div>

          {/* Component summary */}
          <div className="bg-white rounded-xl border border-black/20 p-5 mb-6">
            <p className="text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider mb-3" style={{ fontFamily: "var(--font-mono)" }}>Assembly summary</p>
            <div className="space-y-1.5">
              {asmComponents.map((c, i) => (
                <div key={c.id} className="flex items-center gap-2 text-sm">
                  <span className="text-[var(--color-text-muted)] w-4 text-center" style={{ fontFamily: "var(--font-mono)" }}>{i + 1}</span>
                  <span className="text-[var(--color-text-primary)]">{c.name}</span>
                  <span className="text-[var(--color-text-muted)]">·</span>
                  <span className="text-[var(--color-text-description)]" style={{ fontFamily: "var(--font-mono)" }}>
                    {c.materialOverride === "__custom__" ? c.customMaterial :
                     c.materialOverride || (c.extractedData?.material as string) || "unknown material"}
                  </span>
                </div>
              ))}
              <div className="border-t border-black/20 pt-2 mt-2 flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
                </svg>
                {JOINING_METHODS.find((m) => m.id === joiningMethod)?.label} &middot; {numJoints} joint{numJoints > 1 ? "s" : ""} &middot; qty {quantity}
              </div>
            </div>
          </div>

          {error && <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">{error}</div>}

          <div className="flex gap-3">
            <button
              onClick={handleAsmCalculate}
              className="flex-1 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm transition-all duration-200"
            >
              Calculate Assembly Cost
            </button>
            <button onClick={() => setStep("assembly-review")} className="px-6 py-3.5 border border-black/20 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors">
              Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Step: assembly result ────────────────────────────────────────────────

  if (step === "assembly-result" && assemblyResult) {
    const r = assemblyResult;
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/estimate/new" />
        <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
          <div className="mb-6">
            <h1 className="text-3xl tracking-tight text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>Assembly Should-Cost</h1>
            <p className="text-[var(--color-text-description)] text-sm mt-1">
              {r.components.length} components &middot; {r.joining_method_label} &middot; {r.quantity} unit{r.quantity > 1 ? "s" : ""}
            </p>
          </div>

          {/* Per-component accordion */}
          <div className="space-y-3 mb-6">
            {r.components.map((comp) => (
              <div key={comp.name} className="bg-white border border-black/20 rounded-xl overflow-hidden">
                <button
                  onClick={() => setExpandedComponent(expandedComponent === comp.name ? null : comp.name)}
                  className="w-full flex items-center justify-between px-5 py-4 hover:bg-[var(--color-surface-hover)] transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-[var(--color-text-primary)]">{comp.name}</span>
                    <span className="text-xs text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>{comp.material_name}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>₹ {fmt(comp.unit_cost)}</span>
                    <svg className={`w-4 h-4 text-[var(--color-text-muted)] transition-transform ${expandedComponent === comp.name ? "rotate-180" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                {expandedComponent === comp.name && (
                  <div className="border-t border-black/20">
                    <table className="w-full text-sm">
                      <tbody className="divide-y divide-[#c4c5d5]/10">
                        {[
                          [`Material (${comp.material_name})`, comp.material_cost],
                          ["Machining", comp.machining_cost],
                          ["Setup", comp.setup_cost],
                          ["Tooling", comp.tooling_cost],
                          ["Labour", comp.labour_cost],
                          ["Power", comp.power_cost],
                        ].map(([label, val]) => (
                          <tr key={String(label)}>
                            <td className="px-5 py-2.5 text-[var(--color-text-description)]">{label}</td>
                            <td className="px-5 py-2.5 text-right text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(Number(val))}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Assembly rollup table */}
          <div className="bg-white rounded-xl border border-black/20 overflow-hidden mb-6">
            <table className="w-full">
              <thead>
                <tr className="border-b border-black/20 bg-[var(--color-surface-hover)]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Assembly Cost Rollup</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[var(--color-text-description)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>INR</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#c4c5d5]/10">
                {r.components.map((comp) => (
                  <tr key={comp.name}>
                    <td className="px-6 py-3 text-sm text-[var(--color-text-description)]">{comp.name}</td>
                    <td className="px-6 py-3 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(comp.subtotal)}</td>
                  </tr>
                ))}
                <tr className="bg-[var(--color-surface-hover)]">
                  <td className="px-6 py-3 text-sm text-[var(--color-text-description)]">
                    {r.joining_method_label} ({r.joining_cost > 0 ? `material ₹${fmt(r.joining_material_cost)} + machine ₹${fmt(r.joining_machine_cost)} + labour ₹${fmt(r.joining_labour_cost)}` : "no consumables"})
                  </td>
                  <td className="px-6 py-3 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(r.joining_cost)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3 text-sm text-[var(--color-text-description)]">Overhead (15%)</td>
                  <td className="px-6 py-3 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(r.overhead)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-3 text-sm text-[var(--color-text-description)]">Profit (20%)</td>
                  <td className="px-6 py-3 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(r.profit)}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr className="bg-[var(--color-brand-dark)] text-white">
                  <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>TOTAL ASSEMBLY (per unit)</td>
                  <td className="px-6 py-4 text-right font-bold text-lg" style={{ fontFamily: "var(--font-mono)" }}>₹ {fmt(r.unit_cost)}</td>
                </tr>
                {r.quantity > 1 && (
                  <tr className="bg-[#1e40af] text-white">
                    <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>ORDER TOTAL ({r.quantity} assemblies)</td>
                    <td className="px-6 py-4 text-right font-bold text-lg" style={{ fontFamily: "var(--font-mono)" }}>₹ {fmt(r.order_cost)}</td>
                  </tr>
                )}
              </tfoot>
            </table>
          </div>

          <div className="flex gap-3">
            <button onClick={() => router.push("/dashboard")} className="flex-1 border border-black/20 py-3.5 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors">
              Back to Dashboard
            </button>
            <button
              onClick={() => { setStep("type"); setAssemblyResult(null); setAsmComponents([]); setResult(null); setFile(null); }}
              className="flex-1 bg-[var(--color-brand-dark)] hover:bg-[var(--color-brand-dark-hover)] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm transition-all duration-200"
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
