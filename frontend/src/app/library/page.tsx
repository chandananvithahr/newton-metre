"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { listLibrary, type LibraryDrawing } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d ago`;
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function fileExtension(filename: string): string {
  return filename.split(".").pop()?.toUpperCase() || "DWG";
}

function DrawingCard({ drawing }: { drawing: LibraryDrawing }) {
  const ext = fileExtension(drawing.filename);
  const extColor =
    ext === "PDF" ? "bg-red-100 text-red-700" :
    ext === "DXF" ? "bg-blue-100 text-blue-700" :
    ext === "DWG" ? "bg-purple-100 text-purple-700" :
    ext === "STEP" || ext === "STP" ? "bg-emerald-100 text-emerald-700" :
    "bg-gray-100 text-gray-700";

  const name = drawing.filename.replace(/\.[^.]+$/, "");

  return (
    <div className="bg-white rounded-xl border border-black/8 p-5 hover:border-[var(--color-nm-primary)]/30 hover:shadow-sm transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span
              className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded ${extColor}`}
              style={{ fontFamily: "var(--font-mono)" }}
            >
              {ext}
            </span>
          </div>
          <h3
            className="text-[14px] font-semibold text-[var(--color-text-primary)] truncate"
            style={{ fontFamily: "var(--font-body)" }}
            title={drawing.filename}
          >
            {name}
          </h3>
        </div>
        <span
          className="text-[11px] text-[var(--color-text-disabled)] shrink-0 mt-0.5"
          style={{ fontFamily: "var(--font-mono)" }}
        >
          {timeAgo(drawing.created_at)}
        </span>
      </div>

      {drawing.description ? (
        <p
          className="text-[12px] text-[var(--color-text-description)] line-clamp-2 leading-relaxed"
          style={{ fontFamily: "var(--font-body)" }}
        >
          {drawing.description}
        </p>
      ) : (
        <p
          className="text-[12px] text-[var(--color-text-disabled)] italic"
          style={{ fontFamily: "var(--font-body)" }}
        >
          No description — search to find similar parts
        </p>
      )}
    </div>
  );
}

export default function LibraryPage() {
  const router = useRouter();
  const [drawings, setDrawings] = useState<LibraryDrawing[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    listLibrary()
      .then((d) => {
        setDrawings(d.drawings);
        setTotal(d.total);
      })
      .catch((e) => {
        const msg = e instanceof Error ? e.message : "";
        if (msg === "Not authenticated") {
          router.push("/login");
        } else {
          setError(msg || "Failed to load library.");
        }
      })
      .finally(() => setLoading(false));
  }, [router]);

  return (
    <div className="min-h-screen warm-gradient-page">
      <AppNav active="/library" />

      <div className="max-w-5xl mx-auto px-4 sm:px-8 py-12">

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-8">
          <div>
            <h1
              className="text-[32px] tracking-tight text-[var(--color-text-primary)] mb-1"
              style={{ fontFamily: "var(--font-headline)" }}
            >
              Drawing Library
            </h1>
            <p
              className="text-[14px] text-[var(--color-text-muted)]"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {loading ? "Loading your company brain…" : total === 0
                ? "No drawings indexed yet."
                : `${total} drawing${total === 1 ? "" : "s"} in your company brain`}
            </p>
          </div>

          <div className="flex gap-2 shrink-0">
            <Link
              href="/similar"
              className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-[var(--color-brand-dark)] text-white text-[13px] font-medium hover:bg-[var(--color-brand-dark-hover)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 15.803 7.5 7.5 0 0016.803 15.803z" />
              </svg>
              Search library
            </Link>
            <Link
              href="/similar"
              className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              Add drawing
            </Link>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-[var(--color-text-disabled)] border-t-[var(--color-nm-primary)] rounded-full animate-spin" />
          </div>
        )}

        {/* Error */}
        {!loading && error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-5 text-red-600 text-sm">
            {error}
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && total === 0 && (
          <div className="text-center py-24">
            <div className="w-16 h-16 rounded-2xl bg-[var(--color-surface-container-low)] flex items-center justify-center mx-auto mb-5">
              <svg className="w-8 h-8 text-[var(--color-text-disabled)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776" />
              </svg>
            </div>
            <h2
              className="text-[18px] font-semibold text-[var(--color-text-primary)] mb-2"
              style={{ fontFamily: "var(--font-headline)" }}
            >
              Your library is empty
            </h2>
            <p
              className="text-[14px] text-[var(--color-text-muted)] max-w-sm mx-auto mb-6 leading-relaxed"
              style={{ fontFamily: "var(--font-body)" }}
            >
              Upload drawings to build your company brain. Every drawing you
              estimate or search gets indexed — making future searches faster
              and smarter.
            </p>
            <Link
              href="/similar"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[var(--color-brand-dark)] text-white text-[14px] font-medium hover:bg-[var(--color-brand-dark-hover)] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              Upload your first drawing
            </Link>
          </div>
        )}

        {/* Drawing grid */}
        {!loading && !error && total > 0 && (
          <>
            {/* Stats bar */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              {[
                { label: "Drawings indexed", value: total },
                {
                  label: "First indexed",
                  value: timeAgo(drawings[0]?.created_at ?? ""),
                },
                {
                  label: "Last added",
                  value: timeAgo(drawings[drawings.length - 1]?.created_at ?? ""),
                },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="bg-white rounded-xl border border-black/8 px-5 py-4"
                >
                  <p
                    className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    {stat.label}
                  </p>
                  <p
                    className="text-[20px] font-bold text-[var(--color-text-primary)]"
                    style={{ fontFamily: "var(--font-headline)" }}
                  >
                    {stat.value}
                  </p>
                </div>
              ))}
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {drawings.map((d) => (
                <DrawingCard key={d.id} drawing={d} />
              ))}
            </div>

            {/* Bottom CTA */}
            <div className="mt-10 bg-white ghost-border rounded-xl p-6 flex items-center justify-between gap-4">
              <div>
                <h3
                  className="text-[15px] font-semibold text-[var(--color-text-primary)] mb-0.5"
                  style={{ fontFamily: "var(--font-headline)" }}
                >
                  Search your library
                </h3>
                <p
                  className="text-[13px] text-[var(--color-text-muted)]"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  Upload any drawing — find every similar part you&apos;ve ever estimated or indexed.
                </p>
              </div>
              <Link
                href="/similar"
                className="shrink-0 flex items-center gap-2 px-5 py-2.5 rounded-full bg-[var(--color-brand-dark)] text-white text-[13px] font-medium hover:bg-[var(--color-brand-dark-hover)] transition-colors"
                style={{ fontFamily: "var(--font-body)" }}
              >
                Search now
              </Link>
            </div>
          </>
        )}

      </div>
    </div>
  );
}
