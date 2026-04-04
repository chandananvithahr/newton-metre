"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
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

const PART_LABEL: Record<string, string> = {
  mechanical:  "Mechanical",
  sheet_metal: "Sheet Metal",
  pcb:         "PCB",
  cable:       "Cable",
};

function groupByDate(estimates: Estimate[]) {
  const now = new Date();
  const today: Estimate[] = [];
  const yesterday: Estimate[] = [];
  const older: Estimate[] = [];

  for (const e of estimates) {
    const d = new Date(e.created_at);
    const diffDays = Math.floor((now.getTime() - d.getTime()) / 86400000);
    if (diffDays < 1) today.push(e);
    else if (diffDays < 2) yesterday.push(e);
    else older.push(e);
  }
  return { today, yesterday, older };
}

function IconLogout() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
    </svg>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const [estimates, setEstimates] = useState<Estimate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [est] = await Promise.all([getEstimates(), getUsage()]);
        setEstimates(est);
      } catch (e) {
        const msg = e instanceof Error ? e.message : "";
        if (msg === "Not authenticated") { router.push("/login"); return; }
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

  const { today, yesterday, older } = groupByDate(estimates);

  return (
    <div className="flex h-screen warm-gradient-page overflow-hidden">

      {/* ── Sidebar — history ─────────────────────────────────── */}
      <aside className="w-60 bg-white/80 backdrop-blur-sm border-r border-black/10 flex flex-col h-full shrink-0">

        {/* Logo */}
        <div className="px-4 pt-5 pb-4 border-b border-black/5">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative w-9 h-9 flex items-center justify-center shrink-0">
              <div className="absolute inset-0 bg-[var(--color-brand-dark)] rounded-xl" />
              <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
            </div>
            <span className="text-[var(--color-brand-dark)] text-lg font-semibold tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>Newton-Metre</span>
          </Link>
        </div>

        {/* History */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-4">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="w-4 h-4 border-2 border-black/5 border-t-[var(--color-brand-dark)] rounded-full animate-spin" />
            </div>
          ) : estimates.length === 0 ? (
            <p className="text-[11px] text-[var(--color-text-muted)] text-center py-6" style={{ fontFamily: "var(--font-mono)" }}>
              No estimates yet
            </p>
          ) : (
            <>
              {today.length > 0 && (
                <div>
                  <p className="text-[10px] text-[var(--color-text-muted)] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Today</p>
                  <div className="space-y-0.5">
                    {today.map((e) => (
                      <HistoryItem key={e.id} estimate={e} onClick={() => router.push(`/estimate/${e.id}`)} />
                    ))}
                  </div>
                </div>
              )}
              {yesterday.length > 0 && (
                <div>
                  <p className="text-[10px] text-[var(--color-text-muted)] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Yesterday</p>
                  <div className="space-y-0.5">
                    {yesterday.map((e) => (
                      <HistoryItem key={e.id} estimate={e} onClick={() => router.push(`/estimate/${e.id}`)} />
                    ))}
                  </div>
                </div>
              )}
              {older.length > 0 && (
                <div>
                  <p className="text-[10px] text-[var(--color-text-muted)] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Earlier</p>
                  <div className="space-y-0.5">
                    {older.map((e) => (
                      <HistoryItem key={e.id} estimate={e} onClick={() => router.push(`/estimate/${e.id}`)} />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Sign out */}
        <div className="px-3 pb-4 border-t border-black/5/15 pt-3">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12px] text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-hover)] transition-colors"
            style={{ fontFamily: "var(--font-body)" }}
          >
            <IconLogout />
            Sign out
          </button>
        </div>
      </aside>

      {/* ── Main — two actions ────────────────────────────────── */}
      <main className="flex-1 flex items-center justify-center p-10 overflow-y-auto">
        <div className="w-full max-w-2xl">

          <h1 className="text-[clamp(28px,4vw,42px)] text-[var(--color-text-primary)] tracking-tight text-center mb-2" style={{ fontFamily: "var(--font-headline)" }}>
            What are we doing today?
          </h1>
          <p className="text-center text-[15px] text-[var(--color-text-description)] mb-12" style={{ fontFamily: "var(--font-body)" }}>
            Upload a drawing to get a should-cost breakdown, or search your company&apos;s part history.
          </p>

          <div className="grid sm:grid-cols-3 gap-5">

            {/* Should-Cost */}
            <button
              onClick={() => router.push("/estimate/new")}
              className="group bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200"
            >
              <div className="w-10 h-10 bg-[var(--color-brand-dark)] rounded-lg flex items-center justify-center mb-5">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
              </div>
              <h2 className="text-[16px] font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-brand-dark)]" style={{ fontFamily: "var(--font-body)" }}>
                Get a should-cost
              </h2>
              <p className="text-[14px] text-[var(--color-text-description)] leading-relaxed mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Upload a drawing. Newton-Metre reads it, calculates every cost line — material, machining, finishing, margin.
              </p>
              <span className="text-[12px] text-[var(--color-brand-dark)] font-bold uppercase tracking-widest group-hover:underline" style={{ fontFamily: "var(--font-label)" }}>
                Upload a drawing →
              </span>
            </button>

            {/* Similarity Search */}
            <button
              onClick={() => router.push("/similar")}
              className="group bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200"
            >
              <div className="w-10 h-10 bg-[var(--color-brand-dark)] rounded-lg flex items-center justify-center mb-5">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              <h2 className="text-[16px] font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-brand-dark)]" style={{ fontFamily: "var(--font-body)" }}>
                Find similar parts
              </h2>
              <p className="text-[14px] text-[var(--color-text-description)] leading-relaxed mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Upload drawings, POs, contracts, or QA docs. Newton-Metre searches your company&apos;s history for matches.
              </p>
              <span className="text-[12px] text-[var(--color-brand-dark)] font-bold uppercase tracking-widest group-hover:underline" style={{ fontFamily: "var(--font-label)" }}>
                Search drawings →
              </span>
            </button>

            {/* AI Chat */}
            <button
              onClick={() => router.push("/chat")}
              className="group bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200"
            >
              <div className="w-10 h-10 bg-[var(--color-brand-dark)] rounded-lg flex items-center justify-center mb-5">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                </svg>
              </div>
              <h2 className="text-[16px] font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-brand-dark)]" style={{ fontFamily: "var(--font-body)" }}>
                Ask anything
              </h2>
              <p className="text-[14px] text-[var(--color-text-description)] leading-relaxed mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Ask about costs, materials, processes, or get help optimizing your manufacturing decisions.
              </p>
              <span className="text-[12px] text-[var(--color-brand-dark)] font-bold uppercase tracking-widest group-hover:underline" style={{ fontFamily: "var(--font-label)" }}>
                Start a conversation →
              </span>
            </button>
          </div>

        </div>
      </main>

    </div>
  );
}

function HistoryItem({ estimate, onClick }: { estimate: Estimate; onClick: () => void }) {
  const label = PART_LABEL[estimate.part_type] ?? estimate.part_type;
  const cost = `${estimate.currency} ${estimate.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
  return (
    <button
      onClick={onClick}
      className="w-full text-left px-2 py-2 rounded-lg hover:bg-[var(--color-surface-hover)] transition-colors group"
    >
      <p className="text-[12px] text-[var(--color-text-secondary)] group-hover:text-[var(--color-text-primary)] truncate leading-snug" style={{ fontFamily: "var(--font-body)" }}>
        {label}
      </p>
      <p className="text-[10px] text-[var(--color-text-muted)] tabular-nums mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>
        {cost}
      </p>
    </button>
  );
}
