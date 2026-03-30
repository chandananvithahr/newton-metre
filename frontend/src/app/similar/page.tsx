"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { embedDrawing, searchSimilar } from "@/lib/api";

interface Match {
  drawing_id: string;
  score: number;
  metadata: Record<string, unknown>;
}

export default function SimilarPartsPage() {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<"upload" | "results">("upload");
  const [matches, setMatches] = useState<Match[]>([]);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (files.length < 2) {
      setError("Upload at least 2 drawings to compare.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      for (const file of files) {
        await embedDrawing(file);
      }
      const result = await searchSimilar(files[0]);
      setMatches(result.matches);
      setStep("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
    }

    setLoading(false);
  }

  if (step === "upload") {
    return (
      <div className="min-h-screen bg-slate-50">
        <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
          <Link href="/dashboard" className="text-xl font-bold tracking-tight text-primary-700 py-2">
            Costrich
          </Link>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-12">
          <h1 className="text-3xl font-bold mb-2 tracking-tight">Similar Parts Search</h1>
          <p className="text-gray-500 mb-8">Upload 2 or more engineering drawings to find similar parts and compare costs.</p>

          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
            <div
              className="border-2 border-dashed border-gray-200 rounded-xl p-10 text-center mb-6 hover:border-primary-300 hover:bg-primary-50/30 transition-colors cursor-pointer"
              onClick={() => document.getElementById("multi-file-input")?.click()}
            >
              <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              {files.length > 0 ? (
                <p className="text-sm font-medium text-gray-900">{files.length} file(s) selected</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-gray-700 mb-1">Click to select multiple files</p>
                  <p className="text-xs text-gray-400">PDF, PNG, or JPG — minimum 2 drawings</p>
                </>
              )}
              <input
                id="multi-file-input"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                multiple
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
                className="hidden"
              />
            </div>

            {files.length > 0 && (
              <div className="bg-gray-50 rounded-lg px-4 py-3 mb-6">
                <p className="text-xs text-gray-500 font-medium mb-1">Selected files:</p>
                <p className="text-sm text-gray-700">{files.map((f) => f.name).join(", ")}</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-700 text-sm mb-4">
                {error}
              </div>
            )}

            <button
              onClick={handleSearch}
              disabled={loading || files.length < 2}
              className="w-full bg-primary-600 text-white py-3.5 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Processing drawings...
                </span>
              ) : "Find Similar Parts"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Results view
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="flex items-center px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
        <span
          className="text-xl font-bold tracking-tight text-primary-700 cursor-pointer"
          onClick={() => router.push("/dashboard")}
        >
          Costrich
        </span>
      </nav>
      <div className="max-w-3xl mx-auto px-8 py-8">
        <h1 className="text-3xl font-bold mb-2 tracking-tight">Similarity Results</h1>
        <p className="text-gray-500 text-sm mb-6">{matches.length} match{matches.length !== 1 ? "es" : ""} found</p>

        {matches.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
            <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </div>
            <p className="text-gray-500 font-medium mb-1">No similar parts found</p>
            <p className="text-gray-400 text-sm">Upload more drawings to build your comparison library.</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50/50">
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Drawing</th>
                  <th className="text-right px-6 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">Similarity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {matches.map((m) => {
                  const pct = m.score * 100;
                  const barColor = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : "bg-gray-400";
                  return (
                    <tr key={m.drawing_id} className="hover:bg-gray-50/50">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {(m.metadata.filename as string) || m.drawing_id}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-3">
                          <div className="w-20 h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
                          </div>
                          <span className="font-mono text-sm font-medium text-gray-900 w-14 text-right">
                            {pct.toFixed(1)}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        <button
          onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}
          className="mt-6 border border-gray-200 px-6 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors"
        >
          New Search
        </button>
      </div>
    </div>
  );
}
