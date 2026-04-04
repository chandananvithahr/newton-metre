"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import {
  createWorkflow,
  type ExecutionMode,
} from "@/lib/api";
import { AppNav } from "@/components/app-nav";

interface WorkflowTypeOption {
  type: string;
  label: string;
  description: string;
  inputHint: string;
  fields: FieldDef[];
}

interface FieldDef {
  key: string;
  label: string;
  type: "text" | "number" | "textarea" | "file";
  placeholder?: string;
  required?: boolean;
}

const WORKFLOW_TYPES: WorkflowTypeOption[] = [
  {
    type: "estimate",
    label: "Should-Cost Estimate",
    description: "Upload a drawing to get a line-by-line cost breakdown.",
    inputHint: "Upload a manufacturing drawing (PDF, DXF, or image).",
    fields: [
      { key: "file", label: "Drawing file", type: "file", required: true },
      { key: "quantity", label: "Quantity", type: "number", placeholder: "1" },
    ],
  },
  {
    type: "rfq",
    label: "RFQ Generation",
    description: "Extract drawing, estimate cost, and generate RFQ emails for suppliers.",
    inputHint: "Upload a drawing. The AI will extract, estimate, and draft RFQs.",
    fields: [
      { key: "file", label: "Drawing file", type: "file", required: true },
      { key: "quantity", label: "Quantity", type: "number", placeholder: "1" },
      { key: "supplier_names", label: "Supplier names (comma-separated)", type: "text", placeholder: "Vendor A, Vendor B" },
    ],
  },
  {
    type: "compare_quotes",
    label: "Quote Comparison",
    description: "Compare vendor quotes — normalize, detect anomalies, rank.",
    inputHint: "Enter vendor quotes to compare.",
    fields: [
      { key: "quotes_json", label: "Quotes (JSON array)", type: "textarea", placeholder: '[{"supplier": {"name": "Vendor A"}, "unit_price": 250, "delivery_weeks": 4}]', required: true },
      { key: "should_cost", label: "Should-cost (optional)", type: "number", placeholder: "0" },
    ],
  },
  {
    type: "negotiate",
    label: "Negotiation",
    description: "Compare quotes then generate AI-powered counter-offers.",
    inputHint: "Enter vendor quotes. The AI will compare and draft counter-offers.",
    fields: [
      { key: "quotes_json", label: "Quotes (JSON array)", type: "textarea", placeholder: '[{"supplier": {"name": "Vendor A"}, "unit_price": 250, "delivery_weeks": 4}]', required: true },
      { key: "should_cost", label: "Should-cost (optional)", type: "number", placeholder: "0" },
    ],
  },
  {
    type: "full_procurement",
    label: "Full Procurement",
    description: "End-to-end: extract, estimate, find similar parts, and generate RFQs.",
    inputHint: "Upload a drawing for the complete procurement workflow.",
    fields: [
      { key: "file", label: "Drawing file", type: "file", required: true },
      { key: "quantity", label: "Quantity", type: "number", placeholder: "1" },
      { key: "supplier_names", label: "Supplier names (comma-separated)", type: "text", placeholder: "Vendor A, Vendor B" },
    ],
  },
  {
    type: "proposal",
    label: "Proposal",
    description: "Generate a management-ready procurement proposal from vendor quotes.",
    inputHint: "Enter vendor quotes to generate a proposal.",
    fields: [
      { key: "quotes_json", label: "Quotes (JSON array)", type: "textarea", placeholder: '[{"supplier": {"name": "Vendor A"}, "unit_price": 250, "delivery_weeks": 4}]', required: true },
    ],
  },
  {
    type: "meeting_brief",
    label: "Meeting Brief",
    description: "Generate a pre-meeting brief or analyze post-meeting notes.",
    inputHint: "Enter supplier name for a brief, or paste meeting notes for analysis.",
    fields: [
      { key: "supplier_name", label: "Supplier name", type: "text", placeholder: "Vendor A" },
      { key: "meeting_notes", label: "Meeting notes (optional — for post-meeting analysis)", type: "textarea", placeholder: "Paste your meeting notes here..." },
    ],
  },
];

const MODE_OPTIONS: { value: ExecutionMode; label: string; description: string }[] = [
  { value: "hitl", label: "Human-in-the-loop", description: "AI pauses at key steps for your review" },
  { value: "auto", label: "Autonomous", description: "AI runs end-to-end, you approve the final output" },
  { value: "manual", label: "Manual", description: "AI generates analysis only, you lead the process" },
];

export default function NewWorkflowPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center warm-gradient-page">
        <div className="w-6 h-6 border-2 border-black/5 border-t-[var(--color-brand-dark)] rounded-full animate-spin" />
      </div>
    }>
      <NewWorkflowContent />
    </Suspense>
  );
}

function NewWorkflowContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const preselectedType = searchParams.get("type");
  const prefilledCost = searchParams.get("should_cost");

  const [selectedType, setSelectedType] = useState<string | null>(
    WORKFLOW_TYPES.some((w) => w.type === preselectedType) ? preselectedType : null,
  );
  const [mode, setMode] = useState<ExecutionMode>("hitl");
  const [fieldValues, setFieldValues] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    if (prefilledCost) initial.should_cost = prefilledCost;
    return initial;
  });
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const selectedConfig = WORKFLOW_TYPES.find((w) => w.type === selectedType);

  function updateField(key: string, value: string) {
    setFieldValues((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit() {
    if (!selectedConfig) return;
    setSubmitting(true);
    setError("");

    try {
      const inputs: Record<string, unknown> = {};

      for (const field of selectedConfig.fields) {
        if (field.type === "file") continue;
        const val = fieldValues[field.key]?.trim();
        if (!val && field.required) {
          setError(`${field.label} is required.`);
          setSubmitting(false);
          return;
        }
        if (!val) continue;

        if (field.key === "quotes_json") {
          try {
            inputs.quotes = JSON.parse(val);
          } catch {
            setError("Invalid JSON in quotes field.");
            setSubmitting(false);
            return;
          }
        } else if (field.key === "supplier_names") {
          inputs.suppliers = val.split(",").map((s: string) => ({
            name: s.trim(),
            email: "",
          }));
        } else if (field.key === "should_cost") {
          const n = parseFloat(val);
          if (!isNaN(n) && n > 0) inputs.cost = { unit_cost: n };
        } else if (field.type === "number") {
          inputs[field.key] = parseFloat(val) || 1;
        } else {
          inputs[field.key] = val;
        }
      }

      // For file-based workflows, we'd normally upload via FormData.
      // The agent API currently expects image_bytes in inputs, so for MVP
      // we convert the file to base64.
      const hasFileField = selectedConfig.fields.some((f) => f.type === "file");
      if (hasFileField) {
        if (!file) {
          setError("Please upload a drawing file.");
          setSubmitting(false);
          return;
        }
        const bytes = await file.arrayBuffer();
        const base64 = btoa(
          new Uint8Array(bytes).reduce((s, b) => s + String.fromCharCode(b), ""),
        );
        inputs.file_bytes = base64;
        inputs.filename = file.name;
      }

      const result = await createWorkflow(selectedConfig.type, inputs, mode);
      router.push(`/workflows/${result.workflow_id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create workflow.");
    }
    setSubmitting(false);
  }

  return (
    <div className="min-h-screen warm-gradient-page">
      <AppNav active="/workflows" />
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-10">

        {/* Back link */}
        <Link
          href="/workflows"
          className="inline-flex items-center gap-1.5 text-[12px] text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] mb-6 transition-colors"
          style={{ fontFamily: "var(--font-body)" }}
        >
          <span>&larr;</span> All workflows
        </Link>

        <h1
          className="text-2xl font-medium text-[var(--color-brand-dark)] tracking-tight mb-2"
          style={{ fontFamily: "var(--font-headline)" }}
        >
          New workflow
        </h1>
        <p
          className="text-sm text-[var(--color-text-description)] mb-8"
          style={{ fontFamily: "var(--font-body)" }}
        >
          Choose a workflow type and provide the inputs. The AI handles the rest.
        </p>

        {/* Step 1: Type selection */}
        <div className="mb-8">
          <h2
            className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
            style={{ fontFamily: "var(--font-label)" }}
          >
            Workflow type
          </h2>
          <div className="grid gap-2">
            {WORKFLOW_TYPES.map((wt) => (
              <button
                key={wt.type}
                onClick={() => {
                  setSelectedType(wt.type);
                  setFieldValues({});
                  setFile(null);
                  setError("");
                }}
                className={`text-left bg-white ghost-border rounded-xl px-5 py-4 transition-all ${
                  selectedType === wt.type
                    ? "ring-2 ring-[var(--color-brand-dark)] shadow-sm"
                    : "hover:ambient-shadow"
                }`}
              >
                <p
                  className="text-[14px] font-medium text-[var(--color-text-primary)]"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  {wt.label}
                </p>
                <p
                  className="text-[12px] text-[var(--color-text-muted)] mt-0.5"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  {wt.description}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Configuration (shown after type selection) */}
        {selectedConfig && (
          <>
            {/* Execution mode */}
            <div className="mb-8">
              <h2
                className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Execution mode
              </h2>
              <div className="flex gap-2 flex-wrap">
                {MODE_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setMode(opt.value)}
                    className={`px-4 py-2.5 rounded-xl border text-left transition-all ${
                      mode === opt.value
                        ? "border-[var(--color-brand-dark)] bg-[var(--color-brand-dark)] text-white"
                        : "border-black/10 bg-white hover:border-black/20"
                    }`}
                  >
                    <p
                      className={`text-[13px] font-medium ${mode === opt.value ? "text-white" : "text-[var(--color-text-primary)]"}`}
                      style={{ fontFamily: "var(--font-body)" }}
                    >
                      {opt.label}
                    </p>
                    <p
                      className={`text-[11px] mt-0.5 ${mode === opt.value ? "text-white/70" : "text-[var(--color-text-muted)]"}`}
                      style={{ fontFamily: "var(--font-body)" }}
                    >
                      {opt.description}
                    </p>
                  </button>
                ))}
              </div>
            </div>

            {/* Input fields */}
            <div className="mb-8">
              <h2
                className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-1"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Inputs
              </h2>
              <p
                className="text-[12px] text-[var(--color-text-muted)] mb-4"
                style={{ fontFamily: "var(--font-body)" }}
              >
                {selectedConfig.inputHint}
              </p>

              <div className="space-y-4">
                {selectedConfig.fields.map((field) => (
                  <div key={field.key}>
                    <label
                      className="block text-[12px] font-medium text-[var(--color-text-secondary)] mb-1.5"
                      style={{ fontFamily: "var(--font-body)" }}
                    >
                      {field.label}
                      {field.required && <span className="text-red-500 ml-0.5">*</span>}
                    </label>

                    {field.type === "file" ? (
                      <div>
                        <input
                          type="file"
                          accept=".pdf,.dxf,.dwg,.png,.jpg,.jpeg,.tif,.tiff,.step,.stp"
                          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                          className="block w-full text-sm text-[var(--color-text-secondary)] file:mr-3 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-[var(--color-surface-container-low)] file:text-[var(--color-text-secondary)] hover:file:bg-[var(--color-surface-container)]"
                        />
                        {file && (
                          <p className="text-[11px] text-[var(--color-text-muted)] mt-1" style={{ fontFamily: "var(--font-mono)" }}>
                            {file.name} ({(file.size / 1024).toFixed(0)} KB)
                          </p>
                        )}
                      </div>
                    ) : field.type === "textarea" ? (
                      <textarea
                        value={fieldValues[field.key] ?? ""}
                        onChange={(e) => updateField(field.key, e.target.value)}
                        placeholder={field.placeholder}
                        rows={4}
                        className="w-full border border-black/10 rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-dark)]/20 focus:border-[var(--color-brand-dark)]"
                        style={{ fontFamily: "var(--font-mono)" }}
                      />
                    ) : (
                      <input
                        type={field.type}
                        value={fieldValues[field.key] ?? ""}
                        onChange={(e) => updateField(field.key, e.target.value)}
                        placeholder={field.placeholder}
                        className="w-full border border-black/10 rounded-lg px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-dark)]/20 focus:border-[var(--color-brand-dark)]"
                        style={{ fontFamily: "var(--font-body)" }}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-4">
                <p className="text-sm text-red-700" style={{ fontFamily: "var(--font-body)" }}>{error}</p>
              </div>
            )}

            {/* Submit */}
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="px-6 py-3 rounded-full text-white text-xs font-bold uppercase tracking-widest transition-colors disabled:opacity-50"
              style={{ background: "var(--color-brand-dark)" }}
            >
              {submitting ? "Starting workflow..." : "Start workflow"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
