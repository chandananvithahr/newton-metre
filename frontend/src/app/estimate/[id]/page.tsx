"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getEstimate } from "@/lib/api";
import { AppNav } from "@/components/app-nav";
import { CopyValue } from "@/components/landing/CopyValue";

export default function ViewEstimatePage() {
  const { id } = useParams();
  const router = useRouter();
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const est = await getEstimate(id as string);
        setData(est);
      } catch {
        router.push("/dashboard");
      }
      setLoading(false);
    }
    load();
  }, [id, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center warm-gradient-page">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-[var(--color-text-disabled)] border-t-[var(--color-nm-primary)] rounded-full animate-spin mx-auto mb-3" />
          <p className="text-[var(--color-text-muted)] text-sm">Loading estimate...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center warm-gradient-page">
        <p className="text-[var(--color-text-muted)]">Estimate not found.</p>
      </div>
    );
  }

  const breakdown = data.cost_breakdown as Record<string, unknown> | undefined;
  const confidenceTier = data.confidence_tier as string | null;
  const confidenceStyle =
    confidenceTier === "high"   ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
    confidenceTier === "medium" ? "bg-amber-50 text-amber-700 border-amber-200" :
    confidenceTier === "low"    ? "bg-red-50 text-red-700 border-red-200" :
    "bg-[var(--color-surface-hover)] text-[var(--color-text-muted)] border-[var(--color-text-disabled)]";

  const fmt = (v: unknown) => Number(v ?? 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });
  const currency = (data.currency as string) || "INR";
  const hasBreakdownRows = breakdown && Object.values(breakdown).some((v) => v != null);

  return (
    <div className="min-h-screen warm-gradient-page">
      <AppNav active="/estimate/new" />

      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl tracking-tight text-[var(--color-text-primary)]">Estimate Details</h1>
          {confidenceTier && (
            <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${confidenceStyle}`} style={{ fontFamily: "var(--font-mono)" }}>
              {confidenceTier.toUpperCase()}
            </span>
          )}
        </div>

        {/* Meta table */}
        <div className="bg-white rounded-xl border border-black/10 overflow-hidden mb-4">
          <table className="w-full text-sm">
            <tbody className="divide-y divide-black/5">
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)] w-36" style={{ fontFamily: "var(--font-mono)" }}>Created</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)] font-medium">
                  {new Date(data.created_at as string).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>Part type</td>
                <td className="px-5 py-3 text-[var(--color-text-primary)] font-medium capitalize">
                  {(data.part_type as string) || "mechanical"}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>Total cost</td>
                <td className="px-5 py-3">
                  <CopyValue
                    value={`${data.currency} ${Number(data.total_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}`}
                    className="text-lg font-medium text-[var(--color-text-primary)] rounded px-1 -mx-1"
                  >
                    <span style={{ fontFamily: "var(--font-mono)" }}>
                      {data.currency as string} {Number(data.total_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                    </span>
                  </CopyValue>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {hasBreakdownRows && (
          <div className="bg-white rounded-xl border border-black/10 overflow-hidden mb-6">
            <table className="w-full">
              <thead>
                <tr className="border-b border-black/5 bg-[var(--color-surface-container-low)]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Amount ({currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/5">
                {breakdown.material_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Material</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.material_cost)}</td>
                  </tr>
                )}
                {breakdown.total_machining_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Machining</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_machining_cost)}</td>
                  </tr>
                )}
                {(breakdown.total_setup_cost != null || breakdown.total_tooling_cost != null) && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Setup & Tooling</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(Number(breakdown.total_setup_cost ?? 0) + Number(breakdown.total_tooling_cost ?? 0))}</td>
                  </tr>
                )}
                {breakdown.total_labour_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Labour</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_labour_cost)}</td>
                  </tr>
                )}
                {breakdown.total_power_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Power</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_power_cost)}</td>
                  </tr>
                )}
                {breakdown.overhead != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Overhead</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.overhead)}</td>
                  </tr>
                )}
                {breakdown.profit != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[var(--color-text-description)]">Profit</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.profit)}</td>
                  </tr>
                )}
              </tbody>
              <tfoot>
                <tr className="bg-[var(--color-brand-dark)] text-white">
                  <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>TOTAL (per unit)</td>
                  <CopyValue
                    as="td"
                    value={`${currency} ${fmt(breakdown.unit_cost ?? data.total_cost)}`}
                    className="px-6 py-4 text-right font-bold text-lg rounded"
                  >
                    <span style={{ fontFamily: "var(--font-mono)" }}>
                      {currency} {fmt(breakdown.unit_cost ?? data.total_cost)}
                    </span>
                  </CopyValue>
                </tr>
              </tfoot>
            </table>
          </div>
        )}

        {/* Flywheel actions */}
        <div className="bg-white ghost-border rounded-xl p-5 mb-6">
          <h2
            className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
            style={{ fontFamily: "var(--font-label)" }}
          >
            Next steps
          </h2>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => router.push("/similar")}
              className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
              </svg>
              Find similar parts
            </button>
            <button
              onClick={() => {
                const cost = Number(data.total_cost ?? 0);
                const params = new URLSearchParams();
                params.set("type", "rfq");
                if (cost > 0) params.set("should_cost", String(cost));
                router.push(`/workflows/new?${params}`);
              }}
              className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
              </svg>
              Generate RFQ
            </button>
            <button
              onClick={() => router.push(`/workflows/new?type=negotiate`)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Start negotiation
            </button>
          </div>
        </div>

        <button
          onClick={() => router.push("/estimate/new")}
          className="border border-black/10 px-6 py-3 rounded-lg hover:bg-[var(--color-surface-hover)] text-sm font-medium text-[var(--color-text-description)] transition-colors"
        >
          New Estimate
        </button>
      </div>

    </div>
  );
}
