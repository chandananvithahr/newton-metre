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

  useEffect(() => {
    async function load() {
      try {
        const [est, usg] = await Promise.all([getEstimates(), getUsage()]);
        setEstimates(est);
        setUsage(usg);
      } catch {
        // Auth might have expired
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
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
        <span className="text-xl font-bold">Costimize</span>
        <button onClick={handleLogout} className="text-gray-500 hover:text-gray-700">
          Log out
        </button>
      </nav>

      <div className="max-w-5xl mx-auto px-8 py-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>

        {usage && (
          <div className="flex gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-4 flex-1">
              <p className="text-3xl font-bold">{usage.total_estimates}</p>
              <p className="text-gray-500 text-sm">Estimates</p>
            </div>
            <div className="bg-white rounded-lg shadow p-4 flex-1">
              <p className="text-3xl font-bold">{usage.total_similarity}</p>
              <p className="text-gray-500 text-sm">Similarity searches</p>
            </div>
          </div>
        )}

        <div className="flex gap-4 mb-8">
          <button
            onClick={() => router.push("/estimate/new")}
            className="bg-blue-600 text-white px-6 py-4 rounded-lg hover:bg-blue-700 text-lg flex-1"
          >
            New Estimate
          </button>
          <button
            onClick={() => router.push("/similar")}
            className="bg-white border-2 border-blue-600 text-blue-600 px-6 py-4 rounded-lg hover:bg-blue-50 text-lg flex-1"
          >
            Similar Parts
          </button>
        </div>

        <h2 className="text-xl font-semibold mb-4">Recent Estimates</h2>
        {estimates.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
            No estimates yet. Upload your first drawing.
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Date</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Type</th>
                  <th className="text-right px-6 py-3 text-sm font-medium text-gray-500">Total Cost</th>
                  <th className="text-center px-6 py-3 text-sm font-medium text-gray-500">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {estimates.map((est) => (
                  <tr
                    key={est.id}
                    onClick={() => router.push(`/estimate/${est.id}`)}
                    className="hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-6 py-4 text-sm">{new Date(est.created_at).toLocaleDateString()}</td>
                    <td className="px-6 py-4 text-sm capitalize">{est.part_type}</td>
                    <td className="px-6 py-4 text-sm text-right font-mono">
                      {est.currency} {est.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                    </td>
                    <td className="px-6 py-4 text-sm text-center">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        est.confidence_tier === "high" ? "bg-green-100 text-green-700" :
                        est.confidence_tier === "medium" ? "bg-yellow-100 text-yellow-700" :
                        "bg-gray-100 text-gray-700"
                      }`}>
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
