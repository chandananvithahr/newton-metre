"use client";

import { useState, useCallback } from "react";
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
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<"upload" | "results">("upload");
  const [matches, setMatches] = useState<Match[]>([]);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const [queryFilename, setQueryFilename] = useState("");

  const handleSearch = useCallback(async () => {
    if (!file) {
      setError("Select a drawing to search.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // Embed the query drawing first, then search
      await embedDrawing(file);
      const result = await searchSimilar(file);
      setMatches(result.matches);
      setQueryFilename(file.name);
      setStep("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
    }

    setLoading(false);
  }, [file]);

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  }

  function resetSearch() {
    setStep("upload");
    setMatches([]);
    setFile(null);
    setError("");
    setQueryFilename("");
  }

  if (step === "upload") {
    return (
      <div className="min-h-screen warm-gradient-page">
        <AppNav active="/similar" />
        <div className="max-w-xl mx-auto px-4 sm:px-8 py-12">
          <h1
            style={{ fontFamily: "var(--font-headline)" }}
            className="text-[32px] tracking-tight text-[var(--color-text-primary)] mb-2"
          >
            Find Similar Parts
          </h1>
          <p
            className="text-[var(--color-text-muted)] mb-8 text-[14px] leading-relaxed"
            style={{ fontFamily: "var(--font-body)" }}
          >
            Upload a drawing and instantly find similar parts from your
            company&apos;s history — with materials, processes, and past costs.
          </p>

          <div className="bg-white rounded-2xl border border-black/10 p-8">
            {/* Drop zone */}
            <div
              className={`border-2 border-dashed rounded-xl p-10 text-center mb-6 transition-colors cursor-pointer ${
                dragOver
                  ? "border-[var(--color-nm-primary)]/40 bg-[var(--color-nm-primary)]/5"
                  : "border-black/15 hover:border-[var(--color-nm-primary)]/30 hover:bg-[var(--color-nm-primary)]/5"
              }`}
              role="button"
              tabIndex={0}
              onClick={() =>
                document.getElementById("similarity-file-input")?.click()
              }
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  document.getElementById("similarity-file-input")?.click();
                }
              }}
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
            >
              <div className="w-12 h-12 bg-[var(--color-nm-primary)]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-6 h-6 text-[var(--color-nm-primary)]"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={1.5}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
                  />
                </svg>
              </div>
              {file ? (
                <div>
                  <p
                    className="text-sm font-medium text-[var(--color-text-primary)]"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    {file.name}
                  </p>
                  <p className="text-xs text-[var(--color-text-muted)] mt-1">
                    {(file.size / 1024).toFixed(0)} KB — click to change
                  </p>
                </div>
              ) : (
                <>
                  <p className="text-sm font-medium text-[var(--color-text-description)] mb-1">
                    Drop a drawing here, or click to browse
                  </p>
                  <p className="text-xs text-[var(--color-text-muted)]">
                    PDF, PNG, or JPG
                  </p>
                </>
              )}
              <input
                id="similarity-file-input"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) setFile(f);
                }}
                className="hidden"
              />
            </div>

            {error && (
              <div
                role="alert"
                className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm mb-4"
              >
                {error}
              </div>
            )}

            <button
              onClick={handleSearch}
              disabled={loading || !file}
              className="w-full bg-[var(--color-brand-dark)] text-white py-3.5 rounded-full font-medium hover:bg-[var(--color-brand-dark-hover)] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 text-[14px]"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Searching your library...
                </span>
              ) : (
                "Find Similar Parts"
              )}
            </button>
          </div>

          {/* Value prop */}
          <div className="mt-8 grid grid-cols-3 gap-4">
            {[
              {
                icon: "M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5",
                label: "Visual match",
                desc: "AI compares geometry, features, and proportions",
              },
              {
                icon: "M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z",
                label: "Text match",
                desc: "Materials, processes, and specs compared via BM25",
              },
              {
                icon: "M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
                label: "Cost history",
                desc: "See what you paid last time for similar parts",
              },
            ].map((item) => (
              <div key={item.label} className="text-center">
                <div className="w-9 h-9 bg-[var(--color-surface-container-low)] rounded-lg flex items-center justify-center mx-auto mb-2">
                  <svg
                    className="w-4 h-4 text-[var(--color-text-muted)]"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d={item.icon}
                    />
                  </svg>
                </div>
                <p
                  className="text-[11px] font-bold text-[var(--color-text-secondary)] mb-0.5"
                  style={{ fontFamily: "var(--font-label)" }}
                >
                  {item.label}
                </p>
                <p
                  className="text-[10px] text-[var(--color-text-muted)] leading-snug"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ── Results view ──────────────────────────────────────────────────────
  return (
    <div className="min-h-screen warm-gradient-page">
      <AppNav active="/similar">
        <button
          onClick={resetSearch}
          className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] text-sm font-medium transition-colors py-2 px-3"
        >
          New Search
        </button>
      </AppNav>
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-8">
        {/* Header */}
        <div className="flex items-baseline justify-between mb-6">
          <div>
            <h1
              style={{ fontFamily: "var(--font-headline)" }}
              className="text-[28px] tracking-tight text-[var(--color-text-primary)] mb-1"
            >
              Similar Parts
            </h1>
            <p
              className="text-[var(--color-text-muted)] text-[13px]"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              {matches.length} match{matches.length !== 1 ? "es" : ""} for{" "}
              <span className="text-[var(--color-text-secondary)]">
                {queryFilename}
              </span>
            </p>
          </div>
        </div>

        {matches.length === 0 ? (
          <div className="bg-white rounded-xl border border-black/10 p-12 text-center">
            <div className="w-12 h-12 bg-[var(--color-surface-container-low)] rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 text-[var(--color-text-muted)]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.5}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
                />
              </svg>
            </div>
            <p className="text-[var(--color-text-primary)] font-medium mb-1">
              No similar parts found yet
            </p>
            <p className="text-[var(--color-text-muted)] text-sm mb-4">
              Your library grows every time you run a should-cost estimate.
            </p>
            <button
              onClick={() => router.push("/estimate/new")}
              className="text-[13px] font-medium text-[var(--color-brand-dark)] hover:underline"
              style={{ fontFamily: "var(--font-body)" }}
            >
              Create your first estimate to start building history →
            </button>
          </div>
        ) : (
          <>
            {/* Match cards */}
            <div className="space-y-3">
              {matches.map((m, i) => {
                const pct = m.score * 100;
                const description =
                  (m.metadata.text_description as string) ||
                  (m.metadata.description as string) ||
                  "";
                const filename =
                  (m.metadata.filename as string) || m.drawing_id;
                const breakdown = (m.metadata.score_breakdown || {}) as Record<string, number>;
                const material = (m.metadata.material as string) || "";

                return (
                  <div
                    key={m.drawing_id}
                    className="bg-white rounded-xl border border-black/10 p-5 hover:shadow-sm transition-shadow"
                  >
                    <div className="flex items-start justify-between gap-4">
                      {/* Left: info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2.5 mb-1.5">
                          <span
                            className="text-[11px] font-bold text-[var(--color-text-muted)]"
                            style={{ fontFamily: "var(--font-mono)" }}
                          >
                            #{i + 1}
                          </span>
                          <h3
                            className="text-[15px] font-semibold text-[var(--color-text-primary)] truncate"
                            style={{ fontFamily: "var(--font-body)" }}
                          >
                            {filename}
                          </h3>
                          {material && (
                            <span className="text-[11px] px-2 py-0.5 rounded-full bg-[var(--color-surface-container-low)] text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>
                              {material}
                            </span>
                          )}
                        </div>

                        {description && (
                          <p
                            className="text-[13px] text-[var(--color-text-description)] leading-relaxed mb-2.5 line-clamp-2"
                            style={{ fontFamily: "var(--font-body)" }}
                          >
                            {description}
                          </p>
                        )}

                        {/* Score breakdown bars */}
                        {Object.keys(breakdown).length > 0 && (
                          <div className="flex gap-3 flex-wrap">
                            {([
                              ["visual", "Visual"],
                              ["material", "Material"],
                              ["dimension", "Dims"],
                              ["process", "Process"],
                              ["tolerance", "Tolerance"],
                              ["finish", "Finish"],
                            ] as const).map(([key, label]) => {
                              const val = breakdown[key] ?? 0;
                              const barColor = val >= 0.8 ? "bg-emerald-400" : val >= 0.5 ? "bg-amber-400" : "bg-gray-300";
                              return (
                                <div key={key} className="flex items-center gap-1.5">
                                  <span className="text-[10px] text-[var(--color-text-muted)] w-[52px]" style={{ fontFamily: "var(--font-mono)" }}>{label}</span>
                                  <div className="w-[40px] h-[4px] bg-black/5 rounded-full overflow-hidden">
                                    <div className={`h-full rounded-full ${barColor}`} style={{ width: `${val * 100}%` }} />
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>

                      {/* Right: score badge */}
                      <div className="shrink-0 text-right">
                        <div
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[13px] font-bold ${
                            pct >= 80
                              ? "bg-emerald-50 text-emerald-700"
                              : pct >= 60
                                ? "bg-amber-50 text-amber-700"
                                : "bg-[var(--color-surface-container-low)] text-[var(--color-text-muted)]"
                          }`}
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontVariantNumeric: "tabular-nums",
                          }}
                        >
                          <span
                            className={`w-2 h-2 rounded-full ${
                              pct >= 80
                                ? "bg-emerald-500"
                                : pct >= 60
                                  ? "bg-amber-500"
                                  : "bg-[var(--color-text-disabled)]"
                            }`}
                          />
                          {pct.toFixed(1)}%
                        </div>
                        <p
                          className="text-[10px] text-[var(--color-text-muted)] mt-1"
                          style={{ fontFamily: "var(--font-mono)" }}
                        >
                          {pct >= 80
                            ? "High match"
                            : pct >= 60
                              ? "Moderate"
                              : "Low match"}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
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
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                    />
                  </svg>
                  Get should-cost
                </button>
                <button
                  onClick={() => router.push("/workflows/new?type=rfq")}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
                    />
                  </svg>
                  Generate RFQ
                </button>
                <button
                  onClick={() =>
                    router.push("/workflows/new?type=full_procurement")
                  }
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full text-white text-[13px] font-medium transition-colors"
                  style={{
                    fontFamily: "var(--font-body)",
                    background: "var(--color-brand-dark)",
                  }}
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
                    />
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
