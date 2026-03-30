"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getEstimates, getUsage } from "@/lib/api";
import { createClient } from "@/lib/supabase";
import { AppNav } from "@/components/app-nav";

interface Estimate {
  id: string;
  part_type: string;
  total_cost: number;
  confidence_tier: string | null;
  currency: string;
  created_at: string;
}

interface Usage {
  total_estimates: number;
  total_similarity: number;
  joined: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [estimates, setEstimates] = useState<Estimate[]>([]);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [est, usg] = await Promise.all([getEstimates(), getUsage()]);
        setEstimates(est);
        setUsage(usg);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load data. Please try again.");
      }
      setLoading(false);
    }
    load();
  }, []);

  async function handleLogout() {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/");
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0F1117]">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-[#2A3140] border-t-[#22D3EE] rounded-full animate-spin mx-auto mb-3" />
          <p className="text-[#64748B] text-sm">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // oat Skill #13 — lookup map replaces branching className function
  const CONFIDENCE_CLASS: Record<string, string> = {
    high:   "bg-emerald-950/60 text-emerald-400 border-emerald-800",
    medium: "bg-amber-950/60 text-amber-400 border-amber-800",
    low:    "bg-red-950/60 text-red-400 border-red-800",
  };
  const confidenceColor = (tier: string | null) =>
    CONFIDENCE_CLASS[tier ?? ""] ?? "bg-[#1C2235] text-[#64748B] border-[#2A3140]";

  return (
    <div className="min-h-screen bg-[#0F1117]">
      <AppNav>
        <button
          onClick={handleLogout}
          className="text-[#64748B] hover:text-[#94A3B8] text-sm font-medium transition-colors py-2 px-3"
        >
          Log out
        </button>
      </AppNav>

      <div className="max-w-5xl mx-auto px-4 sm:px-8 py-8">
        <h1 className="text-3xl mb-1 tracking-tight">Dashboard</h1>
        <p className="text-[#64748B] text-sm mb-8">Your cost estimation workspace.</p>

        {error && (
          <div role="alert" className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-6">
            {error}
          </div>
        )}

        {/* Stats */}
        {usage && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            <div className="animate-fade-in-up stagger-1 bg-[#161B27] rounded-xl border border-[#2A3140] p-6">
              <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2" style={{ fontFamily: "var(--font-mono)" }}>Estimates</p>
              <p className="text-3xl font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{usage.total_estimates}</p>
            </div>
            <div className="animate-fade-in-up stagger-2 bg-[#161B27] rounded-xl border border-[#2A3140] p-6">
              <p className="text-xs font-medium text-[#64748B] uppercase tracking-wider mb-2" style={{ fontFamily: "var(--font-mono)" }}>Similarity Searches</p>
              <p className="text-3xl font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{usage.total_similarity}</p>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10 animate-fade-in-up stagger-3">
          <button
            onClick={() => router.push("/estimate/new")}
            className="flex items-center justify-center gap-3 bg-[#22D3EE] text-[#0F1117] px-6 py-5 rounded-xl hover:bg-[#06B6D4] transition-colors text-base font-semibold"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            New Estimate
          </button>
          <button
            onClick={() => router.push("/rfq/new")}
            className="flex items-center justify-center gap-3 bg-[#161B27] border-2 border-[#22D3EE] text-[#22D3EE] px-6 py-5 rounded-xl hover:bg-[#22D3EE]/10 transition-colors text-base font-semibold"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
            RFQ Extractor
          </button>
          <button
            onClick={() => router.push("/similar")}
            className="flex items-center justify-center gap-3 bg-[#161B27] border border-[#2A3140] text-[#94A3B8] px-6 py-5 rounded-xl hover:bg-[#1C2235] transition-colors text-base font-semibold"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
            </svg>
            Similar Parts
          </button>
        </div>

        {/* Recent estimates */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold tracking-tight text-[#E2E8F0]">Recent Estimates</h2>
          <span className="text-xs text-[#475569]" style={{ fontFamily: "var(--font-mono)" }}>{estimates.length} total</span>
        </div>

        {estimates.length === 0 ? (
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-12 text-center">
            <div className="w-12 h-12 bg-[#22D3EE]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-[#22D3EE]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            <p className="text-[#94A3B8] font-medium mb-1">No estimates yet</p>
            <p className="text-[#475569] text-sm">Upload your first engineering drawing to get started.</p>
          </div>
        ) : (
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden overflow-x-auto">
            <table className="w-full min-w-[500px]">
              <thead>
                <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Date</th>
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Type</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Total Cost</th>
                  <th className="text-center px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A3140]">
                {estimates.map((est) => (
                  <tr
                    key={est.id}
                    role="link"
                    tabIndex={0}
                    onClick={() => router.push(`/estimate/${est.id}`)}
                    onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); router.push(`/estimate/${est.id}`); } }}
                    className="hover:bg-[#1C2235] cursor-pointer transition-colors focus:outline-none focus:bg-[#1C2235]"
                  >
                    <td className="px-6 py-4 text-sm text-[#64748B]" style={{ fontFamily: "var(--font-mono)" }}>
                      {new Date(est.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
                    </td>
                    <td className="px-6 py-4 text-sm capitalize font-medium text-[#E2E8F0]">{est.part_type}</td>
                    <td className="px-6 py-4 text-sm text-right font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
                      {est.currency} {est.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold border ${confidenceColor(est.confidence_tier)}`} style={{ fontFamily: "var(--font-mono)" }}>
                        {est.confidence_tier || "—"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
