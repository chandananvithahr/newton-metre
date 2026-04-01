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
      <div className="min-h-screen flex items-center justify-center bg-[#F8F8F6]">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-slate-200 border-t-cyan-600 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-slate-500 text-sm">Loading estimate...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8F8F6]">
        <p className="text-slate-500">Estimate not found.</p>
      </div>
    );
  }

  const breakdown = data.cost_breakdown as Record<string, unknown> | undefined;
  const confidenceTier = data.confidence_tier as string | null;
  const confidenceStyle =
    confidenceTier === "high"   ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
    confidenceTier === "medium" ? "bg-amber-50 text-amber-700 border-amber-200" :
    confidenceTier === "low"    ? "bg-red-50 text-red-700 border-red-200" :
    "bg-slate-50 text-slate-500 border-slate-200";

  const fmt = (v: unknown) => Number(v ?? 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });
  const currency = (data.currency as string) || "INR";
  const hasBreakdownRows = breakdown && Object.values(breakdown).some((v) => v != null);

  return (
    <div className="min-h-screen bg-[#F8F8F6]">
      <AppNav />

      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl tracking-tight text-slate-900">Estimate Details</h1>
          {confidenceTier && (
            <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${confidenceStyle}`} style={{ fontFamily: "var(--font-mono)" }}>
              {confidenceTier.toUpperCase()}
            </span>
          )}
        </div>

        {/* Meta table */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-4">
          <table className="w-full text-sm">
            <tbody className="divide-y divide-slate-100">
              <tr>
                <td className="px-5 py-3 text-slate-500 w-36" style={{ fontFamily: "var(--font-mono)" }}>Created</td>
                <td className="px-5 py-3 text-slate-900 font-medium">
                  {new Date(data.created_at as string).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-slate-500" style={{ fontFamily: "var(--font-mono)" }}>Part type</td>
                <td className="px-5 py-3 text-slate-900 font-medium capitalize">
                  {(data.part_type as string) || "mechanical"}
                </td>
              </tr>
              <tr>
                <td className="px-5 py-3 text-slate-500" style={{ fontFamily: "var(--font-mono)" }}>Total cost</td>
                <td className="px-5 py-3">
                  <CopyValue
                    value={`${data.currency} ${Number(data.total_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}`}
                    className="text-lg font-medium text-slate-900 rounded px-1 -mx-1"
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
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-6">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Cost Component</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Amount ({currency})</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {breakdown.material_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Material</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.material_cost)}</td>
                  </tr>
                )}
                {breakdown.total_machining_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Machining</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_machining_cost)}</td>
                  </tr>
                )}
                {(breakdown.total_setup_cost != null || breakdown.total_tooling_cost != null) && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Setup & Tooling</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(Number(breakdown.total_setup_cost ?? 0) + Number(breakdown.total_tooling_cost ?? 0))}</td>
                  </tr>
                )}
                {breakdown.total_labour_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Labour</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_labour_cost)}</td>
                  </tr>
                )}
                {breakdown.total_power_cost != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Power</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.total_power_cost)}</td>
                  </tr>
                )}
                {breakdown.overhead != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Overhead</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.overhead)}</td>
                  </tr>
                )}
                {breakdown.profit != null && (
                  <tr>
                    <td className="px-6 py-3.5 text-sm text-slate-600">Profit</td>
                    <td className="px-6 py-3.5 text-right text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{fmt(breakdown.profit)}</td>
                  </tr>
                )}
              </tbody>
              <tfoot>
                <tr className="bg-slate-900 text-white">
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

        <button
          onClick={() => router.push("/dashboard")}
          className="border border-slate-200 px-6 py-3 rounded-lg hover:bg-slate-50 text-sm font-medium text-slate-600 transition-colors"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}
