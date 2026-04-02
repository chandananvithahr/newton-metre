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
    <div className="flex h-screen bg-[#faf8ff] overflow-hidden">

      {/* ── Sidebar — history ─────────────────────────────────── */}
      <aside className="w-60 bg-white border-r border-[#c4c5d5]/20 flex flex-col h-full shrink-0">

        {/* Logo */}
        <div className="px-4 pt-5 pb-4 border-b border-[#c4c5d5]/15">
          <Link href="/dashboard" className="flex items-center gap-2.5">
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={32} height={32} className="rounded-lg" />
            <span className="text-[18px] text-[#00288e] italic tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>Newton-Metre</span>
          </Link>
        </div>

        {/* History */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-4">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="w-4 h-4 border-2 border-[#c4c5d5] border-t-[#00288e] rounded-full animate-spin" />
            </div>
          ) : estimates.length === 0 ? (
            <p className="text-[11px] text-[#757684] text-center py-6" style={{ fontFamily: "var(--font-mono)" }}>
              No estimates yet
            </p>
          ) : (
            <>
              {today.length > 0 && (
                <div>
                  <p className="text-[10px] text-[#757684] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Today</p>
                  <div className="space-y-0.5">
                    {today.map((e) => (
                      <HistoryItem key={e.id} estimate={e} onClick={() => router.push(`/estimate/${e.id}`)} />
                    ))}
                  </div>
                </div>
              )}
              {yesterday.length > 0 && (
                <div>
                  <p className="text-[10px] text-[#757684] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Yesterday</p>
                  <div className="space-y-0.5">
                    {yesterday.map((e) => (
                      <HistoryItem key={e.id} estimate={e} onClick={() => router.push(`/estimate/${e.id}`)} />
                    ))}
                  </div>
                </div>
              )}
              {older.length > 0 && (
                <div>
                  <p className="text-[10px] text-[#757684] uppercase tracking-[0.2em] px-2 mb-1.5 font-bold" style={{ fontFamily: "var(--font-label)" }}>Earlier</p>
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
        <div className="px-3 pb-4 border-t border-[#c4c5d5]/15 pt-3">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[12px] text-[#757684] hover:text-[#1a1b20] hover:bg-[#f4f3fa] transition-colors"
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

          <h1 className="text-[clamp(28px,4vw,42px)] text-[#1a1b20] tracking-tight text-center mb-2" style={{ fontFamily: "var(--font-headline)" }}>
            What are we doing today?
          </h1>
          <p className="text-center text-[15px] text-[#515f74] mb-12" style={{ fontFamily: "var(--font-body)" }}>
            Upload a drawing to get a should-cost breakdown, or search your company&apos;s part history.
          </p>

          <div className="grid sm:grid-cols-2 gap-5">

            {/* Should-Cost */}
            <button
              onClick={() => router.push("/estimate/new")}
              className="group bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200"
            >
              <div className="w-10 h-10 gradient-cta rounded-lg flex items-center justify-center mb-5">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
              </div>
              <h2 className="text-[16px] font-bold text-[#1a1b20] mb-2 group-hover:text-[#00288e]" style={{ fontFamily: "var(--font-body)" }}>
                Get a should-cost
              </h2>
              <p className="text-[14px] text-[#515f74] leading-relaxed mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Upload a drawing. Newton-Metre reads it, calculates every cost line — material, machining, finishing, margin.
              </p>
              <span className="text-[12px] text-[#00288e] font-bold uppercase tracking-widest group-hover:underline" style={{ fontFamily: "var(--font-label)" }}>
                Upload a drawing →
              </span>
            </button>

            {/* Similarity Search */}
            <button
              onClick={() => router.push("/similar")}
              className="group bg-white ghost-border rounded-xl p-8 text-left hover:ambient-shadow transition-all duration-200"
            >
              <div className="w-10 h-10 bg-[#1e40af] rounded-lg flex items-center justify-center mb-5">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
              </div>
              <h2 className="text-[16px] font-bold text-[#1a1b20] mb-2 group-hover:text-[#00288e]" style={{ fontFamily: "var(--font-body)" }}>
                Find similar parts
              </h2>
              <p className="text-[14px] text-[#515f74] leading-relaxed mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Upload drawings, POs, contracts, or QA docs. Newton-Metre searches your company&apos;s history for matches.
              </p>
              <span className="text-[12px] text-[#00288e] font-bold uppercase tracking-widest group-hover:underline" style={{ fontFamily: "var(--font-label)" }}>
                Search drawings →
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
      className="w-full text-left px-2 py-2 rounded-lg hover:bg-[#f4f3fa] transition-colors group"
    >
      <p className="text-[12px] text-[#444653] group-hover:text-[#1a1b20] truncate leading-snug" style={{ fontFamily: "var(--font-body)" }}>
        {label}
      </p>
      <p className="text-[10px] text-[#757684] tabular-nums mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>
        {cost}
      </p>
    </button>
  );
}
