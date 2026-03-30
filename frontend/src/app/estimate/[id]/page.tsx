"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getEstimate } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

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
      <div className="min-h-screen flex items-center justify-center bg-[#0F1117]">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-[#2A3140] border-t-[#22D3EE] rounded-full animate-spin mx-auto mb-3" />
          <p className="text-[#64748B] text-sm">Loading estimate...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0F1117]">
        <p className="text-[#64748B]">Estimate not found.</p>
      </div>
    );
  }

  const breakdown = data.cost_breakdown as Record<string, unknown> | undefined;
  const confidenceTier = data.confidence_tier as string | null;
  const confidenceStyle =
    confidenceTier === "high"   ? "bg-emerald-950/60 text-emerald-400 border-emerald-800" :
    confidenceTier === "medium" ? "bg-amber-950/60 text-amber-400 border-amber-800" :
    confidenceTier === "low"    ? "bg-red-950/60 text-red-400 border-red-800" :
    "bg-[#1C2235] text-[#64748B] border-[#2A3140]";

  const fmt = (v: unknown) => Number(v ?? 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });
  const currency = (data.currency as string) || "INR";
  const hasBreakdownRows = breakdown && Object.values(breakdown).some((v) => v != null);

  return (
    <div className="min-h-screen bg-[#0F1117]">
      <AppNav />

      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl tracking-tight">Estimate Details</h1>
          {confidenceTier && (
            <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${confidenceStyle}`} style={{ fontFamily: "var(--font-mono)" }}>
              {confidenceTier.toUpperCase()}
            </span>
          )}
        </div>

        <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-6 mb-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div>
              <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Created</p>
              <p className="text-sm font-medium text-[#E2E8F0]">{new Date(data.created_at as string).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Total Cost</p>
              <p className="text-lg font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{data.currency as string} {Number(data.total_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-1" style={{ fontFamily: "var(--font-mono)" }}>Type</p>
              <p className="text-sm font-medium capitalize text-[#E2E8F0]">{(data.part_type as string) || "mechanical"}</p>
            </div>
          </div>
        </div>

        {hasBreakdownRows && (
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden mb-6">
            <table className="w-full">
              <thead>
                <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Amount ({currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A3140]">
                {breakdown.material_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Material</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.material_cost)}</td>
                  </tr>
                )}
                {breakdown.total_machining_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Machining</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_machining_cost)}</td>
                  </tr>
                )}
                {(breakdown.total_setup_cost != null || breakdown.total_tooling_cost != null) && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Setup & Tooling</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(Number(breakdown.total_setup_cost ?? 0) + Number(breakdown.total_tooling_cost ?? 0))}</td>
                  </tr>
                )}
                {breakdown.total_labour_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Labour</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_labour_cost)}</td>
                  </tr>
                )}
                {breakdown.total_power_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Power</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_power_cost)}</td>
                  </tr>
                )}
                {breakdown.overhead != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Overhead</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.overhead)}</td>
                  </tr>
                )}
                {breakdown.profit != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-[#94A3B8]">Profit</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.profit)}</td>
                  </tr>
                )}
              </tbody>
              <tfoot>
                <tr className="bg-[#22D3EE] text-[#0F1117]">
                  <td className="px-6 py-4 font-bold text-sm" style={{ fontFamily: "var(--font-mono)" }}>TOTAL (per unit)</td>
                  <td className="px-6 py-4 text-right font-bold text-lg" style={{ fontFamily: "var(--font-mono)" }}>
                    {currency} {fmt(breakdown.unit_cost ?? data.total_cost)}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        )}

        <button
          onClick={() => router.push("/dashboard")}
          className="border border-[#2A3140] px-6 py-3 rounded-lg hover:bg-[#1C2235] text-sm font-medium text-[#94A3B8] transition-colors"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}
