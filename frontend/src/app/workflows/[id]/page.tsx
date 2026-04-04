"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  getWorkflow,
  approveWorkflow,
  rejectWorkflow,
  type WorkflowDetail,
  type WorkflowState,
} from "@/lib/api";
import { AppNav } from "@/components/app-nav";

const STATE_BADGE: Record<WorkflowState, { label: string; color: string }> = {
  created:           { label: "Created",      color: "bg-gray-100 text-gray-700" },
  planning:          { label: "Planning",     color: "bg-blue-100 text-blue-700" },
  awaiting_approval: { label: "Needs Review", color: "bg-amber-100 text-amber-700" },
  executing:         { label: "Running",      color: "bg-blue-100 text-blue-700" },
  completed:         { label: "Completed",    color: "bg-emerald-100 text-emerald-700" },
  failed:            { label: "Failed",       color: "bg-red-100 text-red-700" },
  rejected:          { label: "Rejected",     color: "bg-red-100 text-red-700" },
};

const TYPE_LABEL: Record<string, string> = {
  estimate: "Should-Cost Estimate",
  rfq: "RFQ Generation",
  compare_quotes: "Quote Comparison",
  negotiate: "Negotiation",
  full_procurement: "Full Procurement",
  proposal: "Proposal",
  meeting_brief: "Meeting Brief",
};

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function JsonBlock({ data }: { data: Record<string, unknown> }) {
  if (!data || Object.keys(data).length === 0) {
    return (
      <p
        className="text-sm text-[var(--color-text-muted)] italic"
        style={{ fontFamily: "var(--font-body)" }}
      >
        No data
      </p>
    );
  }

  return (
    <pre
      className="bg-[var(--color-surface-container-low)] rounded-lg p-4 text-[12px] leading-relaxed overflow-x-auto text-[var(--color-text-secondary)]"
      style={{ fontFamily: "var(--font-mono)" }}
    >
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}

/* ── Structured output renderers per workflow type ── */

function fmt(n: unknown): string {
  const v = Number(n);
  if (isNaN(v)) return "—";
  return v.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function CostOutputCard({ data }: { data: Record<string, unknown> }) {
  const costData = (data.cost_agent ?? data) as Record<string, unknown>;
  const processLines = (costData.process_lines ?? []) as Record<string, unknown>[];
  const hasLines = processLines.length > 0;

  return (
    <div className="space-y-4">
      {/* Summary row */}
      <div className="grid grid-cols-3 gap-3">
        {([
          { label: "Unit Cost", value: `₹${fmt(costData.unit_cost)}`, accent: true },
          { label: "Order Cost", value: `₹${fmt(costData.order_cost)}`, accent: false },
          { label: "Quantity", value: String(costData.quantity ?? "—"), accent: false },
        ] as { label: string; value: string; accent: boolean }[]).map((item) => (
          <div key={item.label} className="bg-[var(--color-surface-container-low)] rounded-lg p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>{item.label}</p>
            <p className={`text-lg font-semibold mt-0.5 ${item.accent ? "text-emerald-700" : "text-[var(--color-text-primary)]"}`} style={{ fontFamily: "var(--font-mono)" }}>{item.value}</p>
          </div>
        ))}
      </div>

      {/* Cost range band */}
      {!!costData.unit_cost_low && (
        <p className="text-[11px] text-[var(--color-text-muted)] text-center" style={{ fontFamily: "var(--font-body)" }}>
          Range: ₹{fmt(costData.unit_cost_low)} – ₹{fmt(costData.unit_cost_high)} (±{String(costData.uncertainty_pct ?? 15)}%)
        </p>
      )}

      {/* Cost breakdown table */}
      <div className="overflow-x-auto">
        <table className="w-full text-[12px]">
          <tbody className="divide-y divide-black/5">
            {([
              { label: "Material", value: costData.material_cost, sub: `${fmt(costData.raw_weight_kg)} kg ${String(costData.material_name ?? "")}` },
              ...(hasLines ? processLines.map((p) => ({
                label: String(p.process_name ?? p.process_id ?? "Process"),
                value: Number(p.machine_cost ?? 0) + Number(p.setup_cost_per_unit ?? 0) + Number(p.tooling_cost ?? 0) + Number(p.labour_cost ?? 0) + Number(p.power_cost ?? 0),
                sub: `${fmt(p.time_min)} min`,
              })) : []),
              { label: "Machining", value: costData.total_machining_cost, sub: null },
              { label: "Overhead (15%)", value: costData.overhead, sub: null },
              { label: "Profit (20%)", value: costData.profit, sub: null },
            ] as { label: string; value: unknown; sub: string | null }[]).filter(r => r.value !== undefined && r.value !== null).map((row) => (
              <tr key={row.label}>
                <td className="py-2 text-[var(--color-text-secondary)]" style={{ fontFamily: "var(--font-body)" }}>
                  {row.label}
                  {row.sub && <span className="text-[10px] text-[var(--color-text-muted)] ml-1.5">{row.sub}</span>}
                </td>
                <td className="py-2 text-right font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>₹{fmt(row.value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function RfqOutputCard({ data }: { data: Record<string, unknown> }) {
  const rfqData = (data.rfq_agent ?? data) as Record<string, unknown>;
  const drafts = (rfqData.email_drafts ?? []) as Record<string, unknown>[];
  const doc = (rfqData.rfq_document ?? {}) as Record<string, unknown>;

  return (
    <div className="space-y-4">
      {/* RFQ summary */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Suppliers", value: String(rfqData.draft_count ?? drafts.length) },
          { label: "Material", value: String(doc.material ?? "—") },
          { label: "Quantity", value: String(doc.quantity ?? "—") },
        ].map((item) => (
          <div key={item.label} className="bg-[var(--color-surface-container-low)] rounded-lg p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>{item.label}</p>
            <p className="text-sm font-medium mt-0.5 text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>{item.value}</p>
          </div>
        ))}
      </div>

      {/* Email drafts */}
      {drafts.map((draft, i) => {
        const supplier = (draft.supplier ?? {}) as Record<string, unknown>;
        const hasWarning = !!draft._warnings;
        return (
          <div key={i} className={`border rounded-lg overflow-hidden ${hasWarning ? "border-amber-200" : "border-black/5"}`}>
            <div className="bg-[var(--color-surface-container-low)] px-4 py-2 flex items-center justify-between">
              <p className="text-[12px] font-semibold text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>
                {String(supplier.name ?? `Supplier ${i + 1}`)}
              </p>
              {!!supplier.email && (
                <p className="text-[10px] text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>{String(supplier.email)}</p>
              )}
            </div>
            <div className="px-4 py-3">
              <p className="text-[11px] font-semibold text-[var(--color-text-muted)] mb-1" style={{ fontFamily: "var(--font-label)" }}>
                {String(draft.subject ?? "RFQ Email")}
              </p>
              <p className="text-[12px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                {String(draft.body ?? draft.error ?? "No email body")}
              </p>
              {hasWarning && (
                <p className="text-[10px] text-amber-600 mt-2" style={{ fontFamily: "var(--font-body)" }}>⚠ {String(draft._warnings)}</p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function QuoteComparisonCard({ data }: { data: Record<string, unknown> }) {
  const compData = (data.quote_comparison_agent ?? data) as Record<string, unknown>;
  const rows = (compData.comparison_table ?? []) as Record<string, unknown>[];
  const anomalies = (compData.anomalies ?? []) as Record<string, unknown>[];
  const recommendation = String(compData.recommendation ?? "");

  return (
    <div className="space-y-4">
      {/* Recommendation */}
      {recommendation && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
          <p className="text-[12px] text-emerald-800 font-medium" style={{ fontFamily: "var(--font-body)" }}>{recommendation}</p>
        </div>
      )}

      {/* Comparison table */}
      {rows.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-[12px]">
            <thead>
              <tr className="border-b border-black/10">
                {["#", "Supplier", "Unit Price", "Delivery", "vs Should-Cost", "Total"].map((h) => (
                  <th key={h} className="py-2 px-2 text-left text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-black/5">
              {rows.map((row) => {
                const deltaPct = Number(row.delta_pct ?? 0);
                const deltaColor = deltaPct > 10 ? "text-red-600" : deltaPct < -5 ? "text-emerald-600" : "text-[var(--color-text-secondary)]";
                return (
                  <tr key={String(row.supplier)} className={Number(row.rank) === 1 ? "bg-emerald-50/50" : ""}>
                    <td className="py-2 px-2 font-bold text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>{String(row.rank)}</td>
                    <td className="py-2 px-2 font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>{String(row.supplier)}</td>
                    <td className="py-2 px-2" style={{ fontFamily: "var(--font-mono)" }}>₹{fmt(row.unit_price)}</td>
                    <td className="py-2 px-2 text-[var(--color-text-muted)]">{String(row.delivery_weeks ?? "—")} wk</td>
                    <td className={`py-2 px-2 font-medium ${deltaColor}`} style={{ fontFamily: "var(--font-mono)" }}>
                      {deltaPct > 0 ? "+" : ""}{deltaPct.toFixed(1)}%
                    </td>
                    <td className="py-2 px-2 font-medium" style={{ fontFamily: "var(--font-mono)" }}>₹{fmt(row.total_cost)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Anomalies */}
      {anomalies.length > 0 && (
        <div className="space-y-1.5">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>Anomalies</p>
          {anomalies.map((a, i) => (
            <div key={i} className={`rounded-lg px-3 py-2 text-[11px] ${String(a.type) === "suspicious" ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"}`} style={{ fontFamily: "var(--font-body)" }}>
              <span className="font-semibold">{String(a.supplier)}</span>: {String(a.detail)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function NegotiationOutputCard({ data }: { data: Record<string, unknown> }) {
  const neg = (data.negotiation_agent ?? data) as Record<string, unknown>;

  return (
    <div className="space-y-4">
      {/* Key numbers */}
      <div className="grid grid-cols-4 gap-3">
        {([
          { label: "Vendor Quote", value: `₹${fmt(neg.vendor_quote)}`, accent: false },
          { label: "Should-Cost", value: `₹${fmt(neg.should_cost)}`, accent: false },
          { label: "Target Price", value: `₹${fmt(neg.target_price)}`, accent: true },
          { label: "Mode", value: String(neg.execution_mode ?? "—"), accent: false },
        ] as { label: string; value: string; accent: boolean }[]).map((item) => (
          <div key={item.label} className="bg-[var(--color-surface-container-low)] rounded-lg p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>{item.label}</p>
            <p className={`text-sm font-semibold mt-0.5 ${item.accent ? "text-emerald-700" : "text-[var(--color-text-primary)]"}`} style={{ fontFamily: "var(--font-mono)" }}>{item.value}</p>
          </div>
        ))}
      </div>

      {/* Counter offer / analysis */}
      {!!neg.counter_offer && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Counter Offer</p>
          <p className="text-[12px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof neg.counter_offer === "string" ? neg.counter_offer : JSON.stringify(neg.counter_offer, null, 2)}
          </p>
        </div>
      )}
      {!!neg.analysis && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Analysis</p>
          <p className="text-[12px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof neg.analysis === "string" ? neg.analysis : JSON.stringify(neg.analysis, null, 2)}
          </p>
        </div>
      )}
      {!!neg.talking_points && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Talking Points</p>
          <p className="text-[12px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof neg.talking_points === "string" ? neg.talking_points : JSON.stringify(neg.talking_points, null, 2)}
          </p>
        </div>
      )}
    </div>
  );
}

function ProposalOutputCard({ data }: { data: Record<string, unknown> }) {
  const proposal = (data.proposal_agent ?? data) as Record<string, unknown>;

  return (
    <div className="space-y-3">
      {!!proposal.title && (
        <h3 className="text-base font-semibold text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-headline)" }}>
          {String(proposal.title)}
        </h3>
      )}
      {!!proposal.summary && (
        <p className="text-[13px] text-[var(--color-text-secondary)] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
          {String(proposal.summary)}
        </p>
      )}
      {!!proposal.recommendation && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
          <p className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 mb-1" style={{ fontFamily: "var(--font-label)" }}>Recommendation</p>
          <p className="text-[12px] text-emerald-800" style={{ fontFamily: "var(--font-body)" }}>{String(proposal.recommendation)}</p>
        </div>
      )}
      {!!proposal.risks && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Risks</p>
          <p className="text-[12px] text-[var(--color-text-secondary)] whitespace-pre-line" style={{ fontFamily: "var(--font-body)" }}>
            {typeof proposal.risks === "string" ? proposal.risks : JSON.stringify(proposal.risks, null, 2)}
          </p>
        </div>
      )}
      {/* Fallback for any extra fields */}
      {!proposal.title && !proposal.summary && !proposal.recommendation && (
        <JsonBlock data={data} />
      )}
    </div>
  );
}

function MeetingOutputCard({ data }: { data: Record<string, unknown> }) {
  const meeting = (data.meeting_agent ?? data) as Record<string, unknown>;

  return (
    <div className="space-y-3">
      {!!meeting.brief && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Meeting Brief</p>
          <p className="text-[13px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof meeting.brief === "string" ? meeting.brief : JSON.stringify(meeting.brief, null, 2)}
          </p>
        </div>
      )}
      {!!meeting.agenda && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Agenda</p>
          <p className="text-[13px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof meeting.agenda === "string" ? meeting.agenda : JSON.stringify(meeting.agenda, null, 2)}
          </p>
        </div>
      )}
      {!!meeting.key_points && (
        <div className="border border-black/5 rounded-lg p-4">
          <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Key Points</p>
          <p className="text-[13px] text-[var(--color-text-secondary)] whitespace-pre-line leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            {typeof meeting.key_points === "string" ? meeting.key_points : JSON.stringify(meeting.key_points, null, 2)}
          </p>
        </div>
      )}
      {!meeting.brief && !meeting.agenda && !meeting.key_points && (
        <JsonBlock data={data} />
      )}
    </div>
  );
}

/** Route outputs to the right structured renderer, fall back to JSON */
function StructuredOutput({ workflowType, data }: { workflowType: string; data: Record<string, unknown> }) {
  if (!data || Object.keys(data).length === 0) {
    return <p className="text-sm text-[var(--color-text-muted)] italic" style={{ fontFamily: "var(--font-body)" }}>No outputs yet</p>;
  }

  switch (workflowType) {
    case "estimate":
      return <CostOutputCard data={data} />;
    case "rfq":
      return <RfqOutputCard data={data} />;
    case "compare_quotes":
      return <QuoteComparisonCard data={data} />;
    case "negotiate":
      return <NegotiationOutputCard data={data} />;
    case "full_procurement":
      // Full procurement has multiple stages — show cost if present, then RFQ
      return (
        <div className="space-y-6">
          {!!data.cost_agent && (
            <>
              <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>Cost Estimate</p>
              <CostOutputCard data={data} />
            </>
          )}
          {!!data.rfq_agent && (
            <>
              <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-label)" }}>RFQ Drafts</p>
              <RfqOutputCard data={data} />
            </>
          )}
          {!data.cost_agent && !data.rfq_agent && <JsonBlock data={data} />}
        </div>
      );
    case "proposal":
      return <ProposalOutputCard data={data} />;
    case "meeting_brief":
      return <MeetingOutputCard data={data} />;
    default:
      return <JsonBlock data={data} />;
  }
}

const PIPELINE_STEPS: Record<string, string[]> = {
  estimate:         ["Extraction", "Cost + Similarity"],
  rfq:              ["Extraction", "Cost + Similarity", "RFQ Draft"],
  compare_quotes:   ["Quote Comparison"],
  negotiate:        ["Quote Comparison", "Negotiation"],
  full_procurement: ["Extraction", "Cost + Similarity", "RFQ Draft"],
  proposal:         ["Quote Comparison", "Proposal"],
  meeting_brief:    ["Meeting Brief"],
};

function PipelineProgress({ workflowType, state, outputs }: { workflowType: string; state: string; outputs: Record<string, unknown> }) {
  const steps = PIPELINE_STEPS[workflowType];
  if (!steps || steps.length <= 1) return null;

  const completedKeys = Object.keys(outputs || {});
  const isCompleted = state === "completed";
  const isFailed = state === "failed" || state === "rejected";

  // Estimate how far we are based on output keys present
  let activeIndex = 0;
  if (isCompleted) activeIndex = steps.length;
  else if (isFailed) activeIndex = Math.max(0, completedKeys.length);
  else activeIndex = completedKeys.length;

  return (
    <div className="bg-white ghost-border rounded-xl p-5 mb-4">
      <h2
        className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-4"
        style={{ fontFamily: "var(--font-label)" }}
      >
        Pipeline
      </h2>
      <div className="flex items-center gap-1">
        {steps.map((step, i) => {
          const done = i < activeIndex;
          const current = i === activeIndex && !isCompleted && !isFailed;
          return (
            <div key={step} className="flex items-center gap-1 flex-1 min-w-0">
              <div className="flex flex-col items-center flex-1 min-w-0">
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
                    done
                      ? "bg-emerald-500 text-white"
                      : current
                        ? "bg-[var(--color-brand-dark)] text-white ring-2 ring-[var(--color-brand-dark)]/20"
                        : "bg-[var(--color-surface-container)] text-[var(--color-text-muted)]"
                  }`}
                  style={{ fontFamily: "var(--font-mono)" }}
                >
                  {done ? (
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  ) : (
                    i + 1
                  )}
                </div>
                <p
                  className={`text-[10px] mt-1.5 text-center leading-tight truncate w-full ${
                    done || current ? "text-[var(--color-text-primary)] font-medium" : "text-[var(--color-text-muted)]"
                  }`}
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  {step}
                </p>
              </div>
              {i < steps.length - 1 && (
                <div className={`h-0.5 flex-1 min-w-3 mt-[-14px] ${done ? "bg-emerald-500" : "bg-[var(--color-surface-container)]"}`} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function WorkflowDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [workflow, setWorkflow] = useState<WorkflowDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [rejectReason, setRejectReason] = useState("");
  const [showRejectInput, setShowRejectInput] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const ACTIVE_STATES = new Set<WorkflowState>(["created", "planning", "executing"]);
  const isPolling = workflow ? ACTIVE_STATES.has(workflow.state) : false;

  const fetchWorkflow = useCallback(async () => {
    try {
      const data = await getWorkflow(id as string);
      setWorkflow(data);
      return data;
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Failed to load workflow";
      if (msg === "Not authenticated") {
        router.push("/login");
        return null;
      }
      setError(msg);
      return null;
    }
  }, [id, router]);

  // Initial load
  useEffect(() => {
    fetchWorkflow().then(() => setLoading(false));
  }, [fetchWorkflow]);

  // Auto-refresh every 3s for active workflows
  useEffect(() => {
    if (pollRef.current) clearInterval(pollRef.current);
    if (!workflow || !ACTIVE_STATES.has(workflow.state)) return;

    pollRef.current = setInterval(async () => {
      const updated = await fetchWorkflow();
      if (updated && !ACTIVE_STATES.has(updated.state)) {
        if (pollRef.current) clearInterval(pollRef.current);
        pollRef.current = null;
      }
    }, 3000);

    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workflow?.state, fetchWorkflow]);

  async function handleApprove() {
    if (!workflow) return;
    setActionLoading(true);
    setError("");
    try {
      const result = await approveWorkflow(workflow.workflow_id);
      setWorkflow((prev) =>
        prev ? { ...prev, state: result.state, outputs: result.outputs } : prev,
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "Approval failed");
    }
    setActionLoading(false);
  }

  async function handleReject() {
    if (!workflow) return;
    setActionLoading(true);
    setError("");
    try {
      const result = await rejectWorkflow(workflow.workflow_id, rejectReason);
      setWorkflow((prev) =>
        prev ? { ...prev, state: result.state } : prev,
      );
      setShowRejectInput(false);
      setRejectReason("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Rejection failed");
    }
    setActionLoading(false);
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center warm-gradient-page">
        <div className="text-center">
          <div className="w-6 h-6 border-2 border-black/5 border-t-[var(--color-brand-dark)] rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-body)" }}>
            Loading workflow...
          </p>
        </div>
      </div>
    );
  }

  if (error && !workflow) {
    return (
      <div className="min-h-screen warm-gradient-page">
        <div className="max-w-3xl mx-auto px-4 sm:px-8 py-10 text-center">
          <p className="text-sm text-red-600 mb-4" style={{ fontFamily: "var(--font-body)" }}>
            {error}
          </p>
          <Link
            href="/workflows"
            className="text-sm text-[var(--color-text-description)] underline"
          >
            Back to workflows
          </Link>
        </div>
      </div>
    );
  }

  if (!workflow) return null;

  const badge = STATE_BADGE[workflow.state];
  const isAwaitingApproval = workflow.state === "awaiting_approval";

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

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-8">
          <div>
            <h1
              className="text-2xl font-medium text-[var(--color-brand-dark)] tracking-tight"
              style={{ fontFamily: "var(--font-headline)" }}
            >
              {TYPE_LABEL[workflow.workflow_type] ?? workflow.workflow_type}
            </h1>
            <p
              className="text-[11px] text-[var(--color-text-muted)] mt-1"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              {workflow.workflow_id}
            </p>
          </div>
          <span
            className={`shrink-0 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${badge.color}`}
            style={{ fontFamily: "var(--font-label)" }}
          >
            {badge.label}
          </span>
        </div>

        {/* Meta card */}
        <div className="bg-white ghost-border rounded-xl overflow-hidden mb-6">
          <table className="w-full text-sm">
            <tbody className="divide-y divide-black/5">
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)] w-36" style={{ fontFamily: "var(--font-mono)" }}>Type</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)] font-medium" style={{ fontFamily: "var(--font-body)" }}>
                  {TYPE_LABEL[workflow.workflow_type] ?? workflow.workflow_type}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>Mode</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)] font-medium capitalize" style={{ fontFamily: "var(--font-body)" }}>
                  {workflow.execution_mode === "hitl" ? "Human-in-the-loop" : workflow.execution_mode}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>Created</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>
                  {formatDate(workflow.created_at)}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>Updated</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>
                  {formatDate(workflow.updated_at)}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Pipeline progress */}
        <PipelineProgress workflowType={workflow.workflow_type} state={workflow.state} outputs={workflow.outputs} />

        {/* Inputs */}
        <div className="bg-white ghost-border rounded-xl p-5 mb-4">
          <h2
            className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
            style={{ fontFamily: "var(--font-label)" }}
          >
            Inputs
          </h2>
          <JsonBlock data={workflow.inputs} />
        </div>

        {/* Outputs — structured per workflow type */}
        <div className="bg-white ghost-border rounded-xl p-5 mb-6">
          <div className="flex items-center justify-between mb-3">
            <h2
              className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)]"
              style={{ fontFamily: "var(--font-label)" }}
            >
              Outputs
            </h2>
            {isPolling && (
              <span className="flex items-center gap-1.5 text-[10px] text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-body)" }}>
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
                Live
              </span>
            )}
          </div>
          <StructuredOutput workflowType={workflow.workflow_type} data={workflow.outputs} />
        </div>

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-4">
            <p className="text-sm text-red-700" style={{ fontFamily: "var(--font-body)" }}>{error}</p>
          </div>
        )}

        {/* Approval actions */}
        {isAwaitingApproval && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-6">
            <h2
              className="text-sm font-semibold text-amber-800 mb-2"
              style={{ fontFamily: "var(--font-body)" }}
            >
              This workflow needs your review
            </h2>
            <p
              className="text-[13px] text-amber-700 mb-4"
              style={{ fontFamily: "var(--font-body)" }}
            >
              Review the outputs above, then approve to continue or reject to stop.
            </p>

            {showRejectInput ? (
              <div className="space-y-3">
                <textarea
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Reason for rejection (optional)"
                  className="w-full border border-amber-300 rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400"
                  style={{ fontFamily: "var(--font-body)" }}
                  rows={2}
                />
                <div className="flex gap-2">
                  <button
                    onClick={handleReject}
                    disabled={actionLoading}
                    className="px-5 py-2 rounded-full bg-red-600 text-white text-xs font-bold uppercase tracking-widest hover:bg-red-700 transition-colors disabled:opacity-50"
                  >
                    {actionLoading ? "Rejecting..." : "Confirm reject"}
                  </button>
                  <button
                    onClick={() => { setShowRejectInput(false); setRejectReason(""); }}
                    className="px-5 py-2 rounded-full border border-black/10 text-xs font-medium text-[var(--color-text-description)] hover:bg-white transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleApprove}
                  disabled={actionLoading}
                  className="px-5 py-2.5 rounded-full text-white text-xs font-bold uppercase tracking-widest transition-colors disabled:opacity-50"
                  style={{ background: "var(--color-brand-dark)" }}
                >
                  {actionLoading ? "Approving..." : "Approve"}
                </button>
                <button
                  onClick={() => setShowRejectInput(true)}
                  disabled={actionLoading}
                  className="px-5 py-2.5 rounded-full border border-red-300 text-red-600 text-xs font-bold uppercase tracking-widest hover:bg-red-50 transition-colors disabled:opacity-50"
                >
                  Reject
                </button>
              </div>
            )}
          </div>
        )}

        {/* Back button */}
        <Link
          href="/workflows"
          className="inline-block border border-black/10 px-6 py-3 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors"
          style={{ fontFamily: "var(--font-body)" }}
        >
          Back to workflows
        </Link>
      </div>
    </div>
  );
}
