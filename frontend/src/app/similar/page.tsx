"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { embedDrawing, searchSimilar } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

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
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/similar" />
        <div className="max-w-2xl mx-auto px-4 sm:px-8 py-12">
          <h1 style={{ fontFamily: "var(--font-headline)" }} className="text-[32px] tracking-tight text-[var(--color-text-primary)] mb-2">Similar Parts</h1>
          <p className="text-[var(--color-text-muted)] mb-8 text-[14px]" style={{ fontFamily: "var(--font-body)" }}>Upload 2 or more drawings to find similar parts from your company&apos;s history.</p>

          <div className="bg-white rounded-2xl border border-black/10 p-8">
            <div
              className="border-2 border-dashed border-black/15 rounded-xl p-10 text-center mb-6 hover:border-[var(--color-nm-primary)]/30 hover:bg-[var(--color-nm-primary)]/5 transition-colors cursor-pointer"
              role="button"
              tabIndex={0}
              onClick={() => document.getElementById("multi-file-input")?.click()}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); document.getElementById("multi-file-input")?.click(); } }}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add("border-[var(--color-nm-primary)]/40"); }}
              onDragLeave={(e) => { e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40"); }}
              onDrop={(e) => { e.preventDefault(); e.currentTarget.classList.remove("border-[var(--color-nm-primary)]/40"); const newFiles = Array.from(e.dataTransfer.files); if (newFiles.length > 0) setFiles(newFiles); }}
            >
              <div className="w-12 h-12 bg-[var(--color-nm-primary)]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-[var(--color-nm-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              {files.length > 0 ? (
                <p className="text-sm font-medium text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-mono)" }}>{files.length} file(s) selected</p>
              ) : (
                <>
                  <p className="text-sm font-medium text-[var(--color-text-description)] mb-1">Click to select multiple files</p>
                  <p className="text-xs text-[var(--color-text-muted)]">PDF, PNG, or JPG — minimum 2 drawings</p>
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
              <div className="bg-[var(--color-surface-container-low)] rounded-lg px-4 py-3 mb-6">
                <p className="text-xs text-[var(--color-text-muted)] font-medium mb-1" style={{ fontFamily: "var(--font-mono)" }}>Selected files:</p>
                <p className="text-sm text-[var(--color-text-description)]">{files.map((f) => f.name).join(", ")}</p>
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
              className="w-full bg-[var(--color-brand-dark)] text-white py-3.5 rounded-full font-medium hover:bg-[var(--color-brand-dark-hover)] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 text-[14px]"
              style={{ fontFamily: "var(--font-body)" }}
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
      <AppNav active="/similar">
        <button
          onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}
          className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] text-sm font-medium transition-colors py-2 px-3"
        >
          New Search
        </button>
      </AppNav>
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        <h1 style={{ fontFamily: "var(--font-headline)" }} className="text-[32px] tracking-tight text-[var(--color-text-primary)] mb-1">Similar Parts</h1>
        <p className="text-[var(--color-text-muted)] text-[13px] mb-6" style={{ fontFamily: "var(--font-mono)" }}>{matches.length} match{matches.length !== 1 ? "es" : ""} found</p>

        {matches.length === 0 ? (
          <div className="bg-white rounded-xl border border-black/10 p-12 text-center">
            <div className="w-12 h-12 bg-[var(--color-surface-container-low)] rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </div>
            <p className="text-[var(--color-text-primary)] font-medium mb-1">No similar parts found</p>
            <p className="text-[var(--color-text-muted)] text-sm">Upload more drawings to build your comparison library.</p>
          </div>
        ) : (
          <>
          <div className="bg-white rounded-xl border border-black/10 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-black/5 bg-[var(--color-surface-container-low)]">
                  <th className="text-left px-6 py-3.5 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Drawing</th>
                  <th className="text-right px-6 py-3.5 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Similarity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/5">
                {matches.map((m) => {
                  const pct = m.score * 100;
                  const barColor = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : "bg-[var(--color-text-disabled)]";
                  return (
                    <tr key={m.drawing_id} className="hover:bg-[var(--color-surface-hover)] transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-[var(--color-text-primary)]">
                        {(m.metadata.filename as string) || m.drawing_id}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-3">
                          <div className="w-20 h-2 bg-[var(--color-surface-container)] rounded-full overflow-hidden">
                            <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
                          </div>
                          <span className="text-sm font-medium text-[var(--color-text-primary)] w-14 text-right" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>
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

          {/* Flywheel actions */}
          <div className="bg-white ghost-border rounded-xl p-5 mt-4">
            <h2
              className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
              style={{ fontFamily: "var(--font-label)" }}
            >
              Next steps
            </h2>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => router.push("/estimate/new")}
                className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
                style={{ fontFamily: "var(--font-body)" }}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
                Get should-cost
              </button>
              <button
                onClick={() => router.push("/workflows/new?type=rfq")}
                className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
                style={{ fontFamily: "var(--font-body)" }}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                </svg>
                Generate RFQ
              </button>
              <button
                onClick={() => router.push("/workflows/new?type=full_procurement")}
                className="flex items-center gap-2 px-4 py-2.5 rounded-full text-white text-[13px] font-medium transition-colors"
                style={{ fontFamily: "var(--font-body)", background: "var(--color-brand-dark)" }}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                </svg>
                Full procurement
              </button>
            </div>
          </div>
          </>
        )}
      </div>
    </div>
  );
}
