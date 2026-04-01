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

interface Usage {
  total_estimates: number;
  total_similarity: number;
  joined: string;
}

// ── Icons ─────────────────────────────────────────────────────────────────────

function IconLogout() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
    </svg>
  );
}
function IconTrending() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.51l-5.511-3.181" />
    </svg>
  );
}
function IconSearch() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
    </svg>
  );
}
function IconSquares() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
    </svg>
  );
}

// ── Confidence badge ──────────────────────────────────────────────────────────

const CONFIDENCE_BADGE: Record<string, { label: string; className: string }> = {
  high:   { label: "HIGH",   className: "bg-emerald-50 text-emerald-700 border border-emerald-200" },
  medium: { label: "MEDIUM", className: "bg-amber-50 text-amber-700 border border-amber-200" },
  low:    { label: "LOW",    className: "bg-red-50 text-red-700 border border-red-200" },
};

function confidenceBadge(tier: string | null) {
  return CONFIDENCE_BADGE[tier ?? ""] ?? { label: "—", className: "bg-slate-50 text-slate-400 border border-slate-200" };
}

const PART_LABEL: Record<string, string> = {
  mechanical:  "Mechanical",
  sheet_metal: "Sheet Metal",
  pcb:         "PCB",
  cable:       "Cable",
};

// ── Page ──────────────────────────────────────────────────────────────────────

export default function DashboardPage() {
  const router = useRouter();
  const [estimates, setEstimates] = useState<Estimate[]>([]);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [est, usg] = await Promise.all([getEstimates(), getUsage()]);
        setEstimates(est);
        setUsage(usg);
      } catch (e) {
        const msg = e instanceof Error ? e.message : "Failed to load data.";
        if (msg === "Not authenticated") { router.push("/login"); return; }
        setError(msg);
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
      <div className="min-h-screen flex items-center justify-center bg-[#F8F8F6]">
        <div className="w-5 h-5 border-2 border-slate-200 border-t-slate-900 rounded-full animate-spin" />
      </div>
    );
  }

  const latestEstimate = estimates[0] ?? null;

  return (
    <div className="min-h-screen bg-[#F8F8F6]">

      {/* ── Top Nav ─────────────────────────────────────────────────────────── */}
      <header className="bg-white/90 backdrop-blur-md border-b border-slate-200/80 flex justify-between items-center w-full px-6 lg:px-8 h-16 fixed top-0 z-50">
        <div className="flex items-center gap-8">
          <Link href="/dashboard" className="flex items-center gap-2.5">
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={32} height={32} className="rounded-xl" />
            <span style={{ fontFamily: "var(--font-heading)" }} className="text-[18px] text-cyan-600 tracking-tight">Newton-Metre</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            <span className="text-[13px] font-medium text-slate-900" style={{ fontFamily: "var(--font-sans)" }}>Dashboard</span>
            <button onClick={() => router.push("/estimate/new")} className="text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>New Estimate</button>
            <button onClick={() => router.push("/similar")} className="text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Similar Parts</button>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push("/estimate/new")}
            className="hidden sm:flex px-5 py-2 bg-slate-900 text-white text-[13px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200 hover:shadow-md"
            style={{ fontFamily: "var(--font-sans)" }}
          >
            New estimate
          </button>
          <button
            onClick={handleLogout}
            title="Sign out"
            className="p-2 text-slate-300 hover:text-slate-600 transition-colors"
          >
            <IconLogout />
          </button>
        </div>
      </header>

      {/* ── Sidebar ─────────────────────────────────────────────────────────── */}
      <aside className="bg-white border-r border-slate-200/80 h-screen w-56 fixed left-0 top-16 hidden md:flex flex-col pt-6 z-40">
        <div className="px-4 mb-6">
          <button
            onClick={() => router.push("/estimate/new")}
            className="w-full bg-slate-900 text-white py-2.5 px-4 rounded-full text-[12px] font-medium hover:bg-slate-800 transition-all duration-200"
            style={{ fontFamily: "var(--font-sans)" }}
          >
            + New estimate
          </button>
        </div>

        <nav className="flex-1 px-3 space-y-0.5">
          {[
            { label: "Dashboard", icon: <IconSquares />, active: true, path: "/dashboard" },
            { label: "Cost Analysis", icon: <IconTrending />, active: false, path: "/estimate/new" },
            { label: "Similar Parts", icon: <IconSearch />, active: false, path: "/similar" },
          ].map(({ label, icon, active, path }) => (
            <button
              key={label}
              onClick={() => router.push(path)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-colors text-left ${
                active
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-400 hover:text-slate-700 hover:bg-slate-50"
              }`}
              style={{ fontFamily: "var(--font-sans)" }}
            >
              {icon}
              {label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-slate-300 hover:text-slate-600 hover:bg-slate-50 transition-colors text-left"
            style={{ fontFamily: "var(--font-sans)" }}
          >
            <IconLogout />
            Sign out
          </button>
        </div>
      </aside>

      {/* ── Main ────────────────────────────────────────────────────────────── */}
      <main className="md:ml-56 pt-16 min-h-screen">
        <div className="max-w-5xl mx-auto px-6 lg:px-8 py-10">

          {/* Page header */}
          <div className="mb-10">
            <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[32px] text-slate-900 tracking-tight mb-1">
              Dashboard
            </h1>
            <p className="text-[14px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>
              Your should-cost intelligence workspace.
            </p>
          </div>

          {error && (
            <div role="alert" className="bg-red-50 border border-red-200 rounded-xl px-4 py-3 text-red-600 text-[13px] mb-6" style={{ fontFamily: "var(--font-sans)" }}>
              {error}
            </div>
          )}

          {/* Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6">
              <p className="text-[10px] text-slate-300 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Estimates run</p>
              <p className="text-[36px] text-slate-900 font-bold tabular-nums leading-none mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {usage?.total_estimates ?? 0}
              </p>
              <p className="text-[12px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>Should-cost breakdowns</p>
            </div>

            <div className="bg-white border border-slate-200/80 rounded-2xl p-6">
              <p className="text-[10px] text-slate-300 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Parts matched</p>
              <p className="text-[36px] text-slate-900 font-bold tabular-nums leading-none mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {usage?.total_similarity ?? 0}
              </p>
              <p className="text-[12px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>Your company&apos;s brain — searchable</p>
            </div>

            <div className="bg-white border border-slate-200/80 rounded-2xl p-6">
              <p className="text-[10px] text-slate-300 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Latest should-cost</p>
              <p className="text-[36px] text-slate-900 font-bold tabular-nums leading-none mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {latestEstimate
                  ? `${latestEstimate.currency} ${latestEstimate.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`
                  : "—"}
              </p>
              {latestEstimate && (
                <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${confidenceBadge(latestEstimate.confidence_tier).className}`} style={{ fontFamily: "var(--font-mono)" }}>
                  {confidenceBadge(latestEstimate.confidence_tier).label}
                </span>
              )}
            </div>
          </div>

          {/* Main content + sidebar */}
          <div className="grid lg:grid-cols-3 gap-6">

            {/* Recent Estimates */}
            <div className="lg:col-span-2">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-[15px] font-semibold text-slate-900" style={{ fontFamily: "var(--font-sans)" }}>Recent estimates</h2>
                {estimates.length > 5 && (
                  <span className="text-[12px] text-slate-400" style={{ fontFamily: "var(--font-mono)" }}>{estimates.length} total</span>
                )}
              </div>

              {estimates.length === 0 ? (
                <div className="bg-white border border-slate-200/80 rounded-2xl p-12 text-center">
                  <div className="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <IconTrending />
                  </div>
                  <p className="text-[15px] font-medium text-slate-900 mb-2" style={{ fontFamily: "var(--font-sans)" }}>No estimates yet</p>
                  <p className="text-[13px] text-slate-400 mb-6" style={{ fontFamily: "var(--font-sans)" }}>Upload your first drawing to get a should-cost breakdown.</p>
                  <button
                    onClick={() => router.push("/estimate/new")}
                    className="bg-slate-900 text-white px-6 py-2.5 rounded-full text-[13px] font-medium hover:bg-slate-800 transition-all duration-200"
                    style={{ fontFamily: "var(--font-sans)" }}
                  >
                    Upload a drawing
                  </button>
                </div>
              ) : (
                <div className="space-y-2">
                  {estimates.slice(0, 6).map((est) => {
                    const badge = confidenceBadge(est.confidence_tier);
                    const date = new Date(est.created_at);
                    const now = new Date();
                    const diffH = Math.floor((now.getTime() - date.getTime()) / 3600000);
                    const timeLabel = diffH < 1 ? "Just now"
                      : diffH < 24 ? `${diffH}h ago`
                      : diffH < 48 ? "Yesterday"
                      : date.toLocaleDateString("en-IN", { day: "2-digit", month: "short" });

                    return (
                      <div
                        key={est.id}
                        className="bg-white border border-slate-200/80 rounded-xl px-5 py-4 hover:border-slate-300 transition-colors cursor-pointer group"
                        onClick={() => router.push(`/estimate/${est.id}`)}
                        role="link"
                        tabIndex={0}
                        onKeyDown={(e) => { if (e.key === "Enter") router.push(`/estimate/${est.id}`); }}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div>
                              <p className="text-[13px] font-medium text-slate-900" style={{ fontFamily: "var(--font-sans)" }}>
                                {PART_LABEL[est.part_type] ?? est.part_type} — ₹{est.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })} / unit
                              </p>
                              <p className="text-[11px] text-slate-400 mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>{timeLabel}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${badge.className}`} style={{ fontFamily: "var(--font-mono)" }}>
                              {badge.label}
                            </span>
                            <svg className="w-4 h-4 text-slate-300 group-hover:text-slate-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                            </svg>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="space-y-4">
              <h2 className="text-[15px] font-semibold text-slate-900" style={{ fontFamily: "var(--font-sans)" }}>Quick actions</h2>

              <div className="bg-slate-900 rounded-2xl p-6 text-white">
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Should-cost</p>
                <p className="text-[15px] font-medium mb-1" style={{ fontFamily: "var(--font-sans)" }}>Upload a drawing</p>
                <p className="text-[12px] text-slate-400 mb-6 leading-relaxed" style={{ fontFamily: "var(--font-sans)" }}>
                  Get a line-by-line breakdown in under 60 seconds.
                </p>
                <button
                  onClick={() => router.push("/estimate/new")}
                  className="w-full bg-white text-slate-900 py-2.5 rounded-full text-[13px] font-medium hover:bg-slate-100 transition-colors"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  New estimate →
                </button>
              </div>

              <div className="bg-white border border-slate-200/80 rounded-2xl p-6">
                <p className="text-[10px] text-slate-300 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Company brain</p>
                <p className="text-[15px] font-medium text-slate-900 mb-1" style={{ fontFamily: "var(--font-sans)" }}>Find similar parts</p>
                <p className="text-[12px] text-slate-400 mb-5 leading-relaxed" style={{ fontFamily: "var(--font-sans)" }}>
                  Search thousands of drawings, POs, and contracts.
                </p>
                <button
                  onClick={() => router.push("/similar")}
                  className="w-full border border-slate-200 text-slate-600 py-2.5 rounded-full text-[13px] font-medium hover:border-slate-300 hover:text-slate-900 transition-colors"
                  style={{ fontFamily: "var(--font-sans)" }}
                >
                  Search drawings →
                </button>
              </div>

              {estimates.length > 0 && (
                <div className="bg-white border border-slate-200/80 rounded-2xl p-6">
                  <p className="text-[10px] text-slate-300 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Coverage</p>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-[11px] mb-1.5 text-slate-400" style={{ fontFamily: "var(--font-mono)" }}>
                        <span>Estimates</span>
                        <span>{Math.min(100, (usage?.total_estimates ?? 0) * 20)}%</span>
                      </div>
                      <div className="w-full bg-slate-100 h-1 rounded-full overflow-hidden">
                        <div className="bg-slate-900 h-full rounded-full" style={{ width: `${Math.min(100, (usage?.total_estimates ?? 0) * 20)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-[11px] mb-1.5 text-slate-400" style={{ fontFamily: "var(--font-mono)" }}>
                        <span>Part library</span>
                        <span>{Math.min(100, (usage?.total_similarity ?? 0) * 25)}%</span>
                      </div>
                      <div className="w-full bg-slate-100 h-1 rounded-full overflow-hidden">
                        <div className="bg-cyan-500 h-full rounded-full" style={{ width: `${Math.min(100, (usage?.total_similarity ?? 0) * 25)}%` }} />
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

          </div>
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200/80 px-8 py-3 flex justify-around items-center z-50">
        {[
          { label: "Dashboard", icon: <IconSquares />, onClick: () => {} },
          { label: "Estimate", icon: <IconTrending />, onClick: () => router.push("/estimate/new") },
          { label: "Similar", icon: <IconSearch />, onClick: () => router.push("/similar") },
        ].map(({ label, icon, onClick }) => (
          <button key={label} onClick={onClick} className="flex flex-col items-center text-slate-400 gap-1">
            {icon}
            <span className="text-[10px]" style={{ fontFamily: "var(--font-mono)" }}>{label}</span>
          </button>
        ))}
      </nav>

    </div>
  );
}
