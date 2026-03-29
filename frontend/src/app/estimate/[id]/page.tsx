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

  if (loading) return <div className="min-h-screen flex items-center justify-center"><p>Loading...</p></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center"><p>Estimate not found.</p></div>;

  const breakdown = data.cost_breakdown as Record<string, unknown> | undefined;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
        <span className="text-xl font-bold cursor-pointer" onClick={() => router.push("/dashboard")}>Costimize</span>
      </nav>
      <div className="max-w-3xl mx-auto px-8 py-8">
        <h1 className="text-3xl font-bold mb-4">Estimate Details</h1>
        <div className="bg-white rounded-xl shadow p-6 mb-6">
          <p className="mb-2"><span className="font-semibold">Created:</span> {new Date(data.created_at as string).toLocaleString()}</p>
          <p className="mb-2"><span className="font-semibold">Total:</span> {data.currency as string} {Number(data.total_cost).toLocaleString("en-IN")}</p>
          <p className="mb-2"><span className="font-semibold">Confidence:</span> {(data.confidence_tier as string) || "—"}</p>
        </div>

        {breakdown && (
          <div className="bg-white rounded-xl shadow p-6 mb-6">
            <h2 className="font-semibold mb-3">Cost Breakdown</h2>
            <pre className="text-sm bg-gray-50 p-4 rounded-lg overflow-auto">
              {JSON.stringify(breakdown, null, 2)}
            </pre>
          </div>
        )}

        <button onClick={() => router.push("/dashboard")} className="border px-6 py-3 rounded-lg hover:bg-gray-50">
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}
