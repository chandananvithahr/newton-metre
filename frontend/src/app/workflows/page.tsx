"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  listWorkflows,
  type WorkflowSummary,
  type WorkflowState,
} from "@/lib/api";

const STATE_BADGE: Record<WorkflowState, { label: string; color: string }> = {
  created:           { label: "Created",     color: "bg-gray-100 text-gray-700" },
  planning:          { label: "Planning",    color: "bg-blue-100 text-blue-700" },
  awaiting_approval: { label: "Needs Review", color: "bg-amber-100 text-amber-700" },
  executing:         { label: "Running",     color: "bg-blue-100 text-blue-700" },
  completed:         { label: "Completed",   color: "bg-emerald-100 text-emerald-700" },
  failed:            { label: "Failed",      color: "bg-red-100 text-red-700" },
  rejected:          { label: "Rejected",    color: "bg-red-100 text-red-700" },
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
  const d = new Date(iso);
  return d.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function WorkflowsPage() {
  const router = useRouter();
  const [workflows, setWorkflows] = useState<WorkflowSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<WorkflowState | "all">("all");

  useEffect(() => {
    async function load() {
      try {
        const data = await listWorkflows(
          filter === "all" ? undefined : filter,
          50,
        );
        setWorkflows(data);
      } catch (e) {
        const msg = e instanceof Error ? e.message : "";
        if (msg === "Not authenticated") {
          router.push("/login");
          return;
        }
      }
      setLoading(false);
    }
    load();
  }, [filter, router]);

  const pendingCount = workflows.filter(
    (w) => w.state === "awaiting_approval",
  ).length;

  return (
    <div className="min-h-screen warm-gradient-page">
      <div className="max-w-4xl mx-auto px-4 sm:px-8 py-10">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1
              className="text-2xl font-medium text-[var(--color-brand-dark)] tracking-tight"
              style={{ fontFamily: "var(--font-headline)" }}
            >
              AI Workflows
            </h1>
            <p
              className="text-sm text-[var(--color-text-description)] mt-1"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {pendingCount > 0
                ? `${pendingCount} workflow${pendingCount > 1 ? "s" : ""} awaiting your review`
                : "Your procurement workflows — RFQs, negotiations, proposals"}
            </p>
          </div>
          <Link
            href="/workflows/new"
            className="px-5 py-2.5 rounded-full text-white text-xs font-bold uppercase tracking-widest transition-colors"
            style={{ background: "var(--color-brand-dark)" }}
          >
            New workflow
          </Link>
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-1">
          {(
            [
              ["all", "All"],
              ["awaiting_approval", "Needs Review"],
              ["executing", "Running"],
              ["completed", "Completed"],
              ["failed", "Failed"],
            ] as const
          ).map(([value, label]) => (
            <button
              key={value}
              onClick={() => { setFilter(value); setLoading(true); }}
              className={`px-4 py-1.5 rounded-full text-[12px] font-medium border transition-colors whitespace-nowrap ${
                filter === value
                  ? "bg-[var(--color-brand-dark)] text-white border-transparent"
                  : "bg-white text-[var(--color-text-secondary)] border-black/10 hover:border-black/20"
              }`}
              style={{ fontFamily: "var(--font-body)" }}
            >
              {label}
            </button>
          ))}
        </div>

        {/* List */}
        {loading ? (
          <div className="flex justify-center py-20">
            <div className="w-5 h-5 border-2 border-black/5 border-t-[var(--color-brand-dark)] rounded-full animate-spin" />
          </div>
        ) : workflows.length === 0 ? (
          <div className="text-center py-20">
            <p
              className="text-sm text-[var(--color-text-muted)]"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {filter === "all"
                ? "No workflows yet. Start one to automate RFQs, negotiations, or proposals."
                : "No workflows match this filter."}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {workflows.map((w) => {
              const badge = STATE_BADGE[w.state];
              return (
                <Link
                  key={w.id}
                  href={`/workflows/${w.id}`}
                  className="block bg-white ghost-border rounded-xl px-5 py-4 hover:ambient-shadow transition-all group"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div className="min-w-0">
                      <p
                        className="text-[14px] font-medium text-[var(--color-text-primary)] group-hover:text-[var(--color-brand-dark)] truncate"
                        style={{ fontFamily: "var(--font-body)" }}
                      >
                        {TYPE_LABEL[w.workflow_type] ?? w.workflow_type}
                      </p>
                      <p
                        className="text-[11px] text-[var(--color-text-muted)] mt-0.5"
                        style={{ fontFamily: "var(--font-mono)" }}
                      >
                        {formatDate(w.created_at)}
                        {w.execution_mode === "auto" && " · Auto"}
                        {w.execution_mode === "manual" && " · Manual"}
                      </p>
                    </div>
                    <span
                      className={`shrink-0 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${badge.color}`}
                      style={{ fontFamily: "var(--font-label)" }}
                    >
                      {badge.label}
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
