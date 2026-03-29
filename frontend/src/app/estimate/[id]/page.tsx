"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getEstimate } from "@/lib/api";

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
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-500 text-sm">Loading estimate...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-gray-500">Estimate not found.</p>
      </div>
    );
  }

  const breakdown = data.cost_breakdown as Record<string, unknown> | undefined;
  const confidenceTier = data.confidence_tier as string | null;
  const confidenceStyle =
    confidenceTier === "high" ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
    confidenceTier === "medium" ? "bg-amber-50 text-amber-700 border-amber-200" :
    confidenceTier === "low" ? "bg-red-50 text-red-700 border-red-200" :
    "bg-gray-50 text-gray-500 border-gray-200";

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
        <span
          className="text-xl font-bold tracking-tight text-primary-700 cursor-pointer"
          onClick={() => router.push("/dashboard")}
        >
          Costimize
        </span>
      </nav>

      <div className="max-w-3xl mx-auto px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold tracking-tight">Estimate Details</h1>
          {confidenceTier && (
            <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${confidenceStyle}`}>
              {confidenceTier.toUpperCase()}
            </span>
          )}
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Created</p>
              <p className="text-sm font-medium">{new Date(data.created_at as string).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}</p>
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Total Cost</p>
              <p className="text-lg font-bold font-mono">{data.currency as string} {Number(data.total_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</p>
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Type</p>
              <p className="text-sm font-medium capitalize">{(data.part_type as string) || "mechanical"}</p>
            </div>
          </div>
        </div>

        {breakdown && (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Cost Breakdown</h2>
            <pre className="text-xs font-mono bg-slate-50 border border-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-gray-700">
              {JSON.stringify(breakdown, null, 2)}
            </pre>
          </div>
        )}

        <button
          onClick={() => router.push("/dashboard")}
          className="border border-gray-200 px-6 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}
