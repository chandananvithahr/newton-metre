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
      <div className="min-h-screen bg-[#0F1117]">
        <AppNav />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 className="text-3xl mb-2 tracking-tight">Similar Parts Search</h1>
          <p className="text-[#64748B] mb-8 text-sm">Upload 2 or more engineering drawings to find similar parts and compare costs.</p>

          <div className="bg-[#161B27] rounded-2xl border border-[#2A3140] p-8">
            <div
              className="border-2 border-dashed border-[#2A3140] rounded-xl p-10 text-center mb-6 hover:border-[#22D3EE]/50 hover:bg-[#22D3EE]/5 transition-colors cursor-pointer"
              role="button"
              tabIndex={0}
              onClick={() => document.getElementById("multi-file-input")?.click()}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("multi-file-input")?.click(); } }}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-[#22D3EE]", "bg-[#22D3EE]/5"); }}
              onDragLeave={(e) => { e.currentTarget.classList.remove("border-[#22D3EE]", "bg-[#22D3EE]/5"); }}
              onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-[#22D3EE]", "bg-[#22D3EE]/5"); const newFiles = Array.from(e.dataTransfer.files); if (newFiles.length > 0) setFiles(newFiles); }}
            >
              <div className="w-12 h-12 bg-[#22D3EE]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-[#22D3EE]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              {files.length > 0 ? (
                <p className="text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)" }}>{files.length} file(s) selected</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-[#94A3B8] mb-1">Click to select multiple files</p>
                  <p className="text-xs text-[#475569]">PDF, PNG, or JPG — minimum 2 drawings</p>
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
              <div className="bg-[#1C2235] rounded-lg px-4 py-3 mb-6">
                <p className="text-xs text-[#475569] font-medium mb-1" style={{ fontFamily: "var(--font-mono)" }}>Selected files:</p>
                <p className="text-sm text-[#94A3B8]">{files.map((f) => f.name).join(", ")}</p>
              </div>
            )}

            {error && (
              <div role="alert" className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm mb-4">
                {error}
              </div>
            )}

            <button
              onClick={handleSearch}
              disabled={loading || files.length < 2}
              className="w-full bg-[#22D3EE] text-[#0F1117] py-3.5 rounded-lg font-semibold hover:bg-[#06B6D4] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-[#0F1117]/30 border-t-[#0F1117] rounded-full animate-spin" />
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
    <div className="min-h-screen bg-[#0F1117]">
      <AppNav>
        <button
          onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}
          className="text-[#64748B] hover:text-[#94A3B8] text-sm font-medium transition-colors py-2 px-3"
        >
          New Search
        </button>
      </AppNav>
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <h1 className="text-3xl mb-1 tracking-tight">Similarity Results</h1>
        <p className="text-[#64748B] text-sm mb-6" style={{ fontFamily: "var(--font-mono)" }}>{matches.length} match{matches.length !== 1 ? "es" : ""} found</p>

        {matches.length === 0 ? (
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] p-12 text-center">
            <div className="w-12 h-12 bg-[#1C2235] rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-[#475569]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </div>
            <p className="text-[#94A3B8] font-medium mb-1">No similar parts found</p>
            <p className="text-[#475569] text-sm">Upload more drawings to build your comparison library.</p>
          </div>
        ) : (
          <div className="bg-[#161B27] rounded-xl border border-[#2A3140] overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-[#2A3140] bg-[#1C2235]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Drawing</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[#64748B] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Similarity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A3140]">
                {matches.map((m) => {
                  const pct = m.score * 100;
                  const barColor = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : "bg-[#475569]";
                  return (
                    <tr key={m.drawing_id} className="hover:bg-[#1C2235] transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-[#E2E8F0]">
                        {(m.metadata.filename as string) || m.drawing_id}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-3">
                          <div className="w-20 h-2 bg-[#2A3140] rounded-full overflow-hidden">
                            <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
                          </div>
                          <span className="text-sm font-medium text-[#E2E8F0] w-14 text-right" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
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
