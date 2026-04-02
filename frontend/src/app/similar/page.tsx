"use client";

import { useState } from "react";
import { embedDrawing, searchSimilar } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

interface Match {
  drawing_id: string;
  score: number;
  metadata: Record<string, unknown>;
}

export default function SimilarPartsPage() {
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
      <div className="min-h-screen warm-gradient-page">
        <AppNav />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[32px] tracking-tight text-slate-900 mb-2">Similar Parts</h1>
          <p className="text-slate-400 mb-8 text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>Upload 2 or more drawings to find similar parts from your company&apos;s history.</p>

          <div className="bg-white rounded-2xl border border-slate-200/80 p-8">
            <div
              className="border-2 border-dashed border-slate-200 rounded-xl p-10 text-center mb-6 hover:border-cyan-300 hover:bg-cyan-50/50 transition-colors cursor-pointer"
              role="button"
              tabIndex={0}
              onClick={() => document.getElementById("multi-file-input")?.click()}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("multi-file-input")?.click(); } }}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-cyan-300", "bg-cyan-50/50"); }}
              onDragLeave={(e) => { e.currentTarget.classList.remove("border-cyan-300", "bg-cyan-50/50"); }}
              onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-cyan-300", "bg-cyan-50/50"); const newFiles = Array.from(e.dataTransfer.files); if (newFiles.length > 0) setFiles(newFiles); }}
            >
              <div className="w-12 h-12 bg-cyan-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              {files.length > 0 ? (
                <p className="text-sm font-medium text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{files.length} file(s) selected</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-slate-600 mb-1">Click to select multiple files</p>
                  <p className="text-xs text-slate-400">PDF, PNG, or JPG — minimum 2 drawings</p>
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
              <div className="bg-slate-50 rounded-lg px-4 py-3 mb-6">
                <p className="text-xs text-slate-400 font-medium mb-1" style={{ fontFamily: "var(--font-mono)" }}>Selected files:</p>
                <p className="text-sm text-slate-600">{files.map((f) => f.name).join(", ")}</p>
              </div>
            )}

            {error && (
              <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4">
                {error}
              </div>
            )}

            <button
              onClick={handleSearch}
              disabled={loading || files.length < 2}
              className="w-full bg-slate-900 text-white py-3.5 rounded-full font-medium hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 text-[14px]"
            style={{ fontFamily: "var(--font-sans)" }}
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
    <div className="min-h-screen warm-gradient-page">
      <AppNav>
        <button
          onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}
          className="text-slate-500 hover:text-slate-700 text-sm font-medium transition-colors py-2 px-3"
        >
          New Search
        </button>
      </AppNav>
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[32px] tracking-tight text-slate-900 mb-1">Similar Parts</h1>
        <p className="text-slate-400 text-[13px] mb-6" style={{ fontFamily: "var(--font-mono)" }}>{matches.length} match{matches.length !== 1 ? "es" : ""} found</p>

        {matches.length === 0 ? (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
            <div className="w-12 h-12 bg-slate-50 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </div>
            <p className="text-slate-700 font-medium mb-1">No similar parts found</p>
            <p className="text-slate-400 text-sm">Upload more drawings to build your comparison library.</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Drawing</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-slate-500 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Similarity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {matches.map((m) => {
                  const pct = m.score * 100;
                  const barColor = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : "bg-slate-300";
                  return (
                    <tr key={m.drawing_id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-slate-900">
                        {(m.metadata.filename as string) || m.drawing_id}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-3">
                          <div className="w-20 h-2 bg-slate-200 rounded-full overflow-hidden">
                            <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
                          </div>
                          <span className="text-sm font-medium text-slate-900 w-14 text-right" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
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
      </div>
    </div>
  );
}
