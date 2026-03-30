"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getEstimates, getUsage } from "@/lib/api";
import { createClient } from "@/lib/supabase";

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
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-500 text-sm">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const confidenceColor = (tier: string | null) => {
    if (tier === "high") return "bg-emerald-50 text-emerald-700 border-emerald-200";
    if (tier === "medium") return "bg-amber-50 text-amber-700 border-amber-200";
    if (tier === "low") return "bg-red-50 text-red-700 border-red-200";
    return "bg-gray-50 text-gray-500 border-gray-200";
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Nav */}
      <nav className="flex items-center justify-between px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
        <span className="text-xl font-bold tracking-tight text-primary-700">Costrich</span>
        <button onClick={handleLogout} className="text-gray-400 hover:text-gray-600 text-sm font-medium transition-colors">
          Log out
        </button>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-8 py-8">
        <h1 className="text-3xl font-bold mb-1 tracking-tight">Dashboard</h1>
        <p className="text-gray-500 text-sm mb-8">Your cost estimation workspace.</p>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-700 text-sm mb-6">
            {error}
          </div>
        )}

        {/* Stats */}
        {usage && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <p className="text-sm font-medium text-gray-500 mb-1">Estimates</p>
              <p className="text-3xl font-bold text-gray-900">{usage.total_estimates}</p>
            </div>
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <p className="text-sm font-medium text-gray-500 mb-1">Similarity Searches</p>
              <p className="text-3xl font-bold text-gray-900">{usage.total_similarity}</p>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
          <button
            onClick={() => router.push("/estimate/new")}
            className="flex items-center justify-center gap-3 bg-primary-600 text-white px-6 py-5 rounded-xl hover:bg-primary-700 transition-colors shadow-sm text-lg font-semibold"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            New Estimate
          </button>
          <button
            onClick={() => router.push("/similar")}
            className="flex items-center justify-center gap-3 bg-white border-2 border-primary-600 text-primary-600 px-6 py-5 rounded-xl hover:bg-primary-50 transition-colors text-lg font-semibold"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
            </svg>
            Similar Parts
          </button>
        </div>

        {/* Recent estimates */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold tracking-tight">Recent Estimates</h2>
          <span className="text-xs text-gray-400">{estimates.length} total</span>
        </div>

        {estimates.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
            <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            <p className="text-gray-500 font-medium mb-1">No estimates yet</p>
            <p className="text-gray-400 text-sm">Upload your first engineering drawing to get started.</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden overflow-x-auto">
            <table className="w-full min-w-[500px]">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50/50">
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Type</th>
                  <th className="text-right px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Total Cost</th>
                  <th className="text-center px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {estimates.map((est) => (
                  <tr
                    key={est.id}
                    onClick={() => router.push(`/estimate/${est.id}`)}
                    className="hover:bg-primary-50/30 cursor-pointer transition-colors"
                  >
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(est.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
                    </td>
                    <td className="px-6 py-4 text-sm capitalize font-medium text-gray-900">{est.part_type}</td>
                    <td className="px-6 py-4 text-sm text-right font-mono font-medium text-gray-900">
                      {est.currency} {est.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold border ${confidenceColor(est.confidence_tier)}`}>
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
