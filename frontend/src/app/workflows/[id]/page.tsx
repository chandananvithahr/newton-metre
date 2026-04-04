"use client";

import { useEffect, useState } from "react";
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

  useEffect(() => {
    async function load() {
      try {
        const data = await getWorkflow(id as string);
        setWorkflow(data);
      } catch (e) {
        const msg = e instanceof Error ? e.message : "Failed to load workflow";
        if (msg === "Not authenticated") {
          router.push("/login");
          return;
        }
        setError(msg);
      }
      setLoading(false);
    }
    load();
  }, [id, router]);

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

        {/* Outputs */}
        <div className="bg-white ghost-border rounded-xl p-5 mb-6">
          <h2
            className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
            style={{ fontFamily: "var(--font-label)" }}
          >
            Outputs
          </h2>
          <JsonBlock data={workflow.outputs} />
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
