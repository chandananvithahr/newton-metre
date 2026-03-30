"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
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

// ── Icons ────────────────────────────────────────────────────────────────────

function IconDashboard() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
    </svg>
  );
}
function IconTrending() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.51l-5.511-3.181" />
    </svg>
  );
}
function IconHandshake() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5a3.375 3.375 0 00-3.375-3.375H9.75" />
    </svg>
  );
}
function IconScience() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15M14.25 3.104c.251.023.501.05.75.082M19.8 15a2.25 2.25 0 01.45 1.318 2.25 2.25 0 01-2.25 2.25H5.25a2.25 2.25 0 01-2.25-2.25 2.25 2.25 0 01.45-1.318L6 14.5m13.5.5l.75 1.5M4.5 15l-.75 1.5" />
    </svg>
  );
}
function IconBolt() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  );
}
function IconAnalytics() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
    </svg>
  );
}
function IconRadar() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}
function IconGear() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}
function IconSearch() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
    </svg>
  );
}
function IconDoc() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
    </svg>
  );
}
function IconLogout() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
    </svg>
  );
}

// ── Confidence badge ──────────────────────────────────────────────────────────

const CONFIDENCE_BADGE: Record<string, { label: string; className: string }> = {
  high:   { label: "HIGH",   className: "bg-emerald-100 text-emerald-700" },
  medium: { label: "MEDIUM", className: "bg-amber-100 text-amber-700" },
  low:    { label: "LOW",    className: "bg-red-100 text-red-700" },
};

function confidenceBadge(tier: string | null) {
  return CONFIDENCE_BADGE[tier ?? ""] ?? { label: "—", className: "bg-slate-100 text-slate-500" };
}

// ── Part type icon color ──────────────────────────────────────────────────────

const PART_BG: Record<string, string> = {
  mechanical:   "bg-slate-900",
  sheet_metal:  "bg-teal-700",
  pcb:          "bg-blue-900",
  cable:        "bg-violet-800",
};

function partBg(partType: string) {
  return PART_BG[partType] ?? "bg-slate-700";
}

// ── Page ─────────────────────────────────────────────────────────────────────

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
        const msg = e instanceof Error ? e.message : "Failed to load data. Please try again.";
        if (msg === "Not authenticated") {
          router.push("/login");
          return;
        }
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
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-slate-200 border-t-blue-700 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-slate-500 text-sm font-mono uppercase tracking-widest text-xs">Loading...</p>
        </div>
      </div>
    );
  }

  const latestEstimate = estimates[0] ?? null;

  return (
    <div className="bg-white text-slate-900 antialiased min-h-screen" style={{ fontFamily: "var(--font-inter)" }}>

      {/* ── Top Nav ───────────────────────────────────────────────────────── */}
      <header className="bg-white border-b border-slate-200 shadow-sm flex justify-between items-center w-full px-6 py-3 h-16 fixed top-0 z-50">
        <div className="flex items-center gap-8">
          <div className="text-2xl font-black tracking-tighter text-blue-800">Costrich</div>
          <nav className="hidden md:flex items-center gap-6 text-sm font-semibold tracking-tight">
            <span className="text-blue-700 border-b-2 border-blue-700 pb-1">Dashboard</span>
            <button onClick={() => router.push("/estimate/new")} className="text-slate-500 hover:text-blue-700 transition-colors">New Analysis</button>
            <button onClick={() => router.push("/rfq/new")} className="text-slate-500 hover:text-blue-700 transition-colors">PDF Extractor</button>
            <button onClick={() => router.push("/similar")} className="text-slate-500 hover:text-blue-700 transition-colors">Similar Parts</button>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push("/estimate/new")}
            className="bg-blue-700 text-white px-4 py-2 rounded font-bold text-sm hover:bg-blue-800 transition-colors"
          >
            Launch Terminal
          </button>
          <button
            onClick={handleLogout}
            title="Log out"
            className="p-2 hover:bg-slate-50 rounded transition-colors text-slate-400 hover:text-slate-600"
          >
            <IconLogout />
          </button>
        </div>
      </header>

      {/* ── Sidebar ───────────────────────────────────────────────────────── */}
      <aside className="bg-slate-50 h-screen w-64 border-r border-slate-200 fixed left-0 top-16 flex flex-col pt-6 z-40 hidden md:flex">
        <div className="px-6 mb-6">
          <button
            onClick={() => router.push("/estimate/new")}
            className="w-full bg-slate-900 text-white py-2.5 px-4 rounded text-xs font-mono uppercase tracking-widest hover:bg-slate-700 transition-colors"
          >
            + New Analysis
          </button>
        </div>

        <nav className="flex-1 px-3 space-y-0.5 text-xs font-mono uppercase tracking-widest">
          <div className="flex items-center gap-3 px-3 py-3 bg-blue-50 text-blue-700 border-r-4 border-blue-700 font-bold">
            <IconDashboard />
            Dashboard
          </div>
          <button
            onClick={() => router.push("/estimate/new")}
            className="w-full flex items-center gap-3 px-3 py-3 text-slate-500 hover:bg-slate-100 hover:translate-x-1 transition-transform duration-200"
          >
            <IconTrending />
            Cost Analysis
          </button>
          <button
            onClick={() => router.push("/similar")}
            className="w-full flex items-center gap-3 px-3 py-3 text-slate-500 hover:bg-slate-100 hover:translate-x-1 transition-transform duration-200"
          >
            <IconSearch />
            Similar Parts
          </button>
          <button
            onClick={() => router.push("/rfq/new")}
            className="w-full flex items-center gap-3 px-3 py-3 text-slate-500 hover:bg-slate-100 hover:translate-x-1 transition-transform duration-200"
          >
            <IconDoc />
            PDF Extractor
          </button>
        </nav>

        <div className="p-3 border-t border-slate-200 text-xs font-mono uppercase tracking-widest">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2.5 text-slate-400 hover:bg-slate-100 transition-colors"
          >
            <IconLogout />
            Log Out
          </button>
        </div>
      </aside>

      {/* ── Main Content ──────────────────────────────────────────────────── */}
      <main
        className="md:ml-64 pt-20 p-8 min-h-screen"
        style={{
          backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke='rgb(241 245 249 / 0.8)'%3E%3Cpath d='M0 .5H31.5V32'/%3E%3C/svg%3E\")",
        }}
      >
        <div className="max-w-7xl mx-auto">

          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-end mb-10 border-l-4 border-blue-800 pl-6">
            <div>
              <h1
                className="text-4xl font-black tracking-tighter text-slate-900 mb-1"
                style={{ fontFamily: "var(--font-inter)" }}
              >
                COST INTELLIGENCE DASHBOARD
              </h1>
              <p className="text-slate-500 font-mono text-sm tracking-tight">
                &gt; Your should-cost analysis workspace.
              </p>
            </div>
            <div className="flex gap-3 mt-4 sm:mt-0">
              <button
                onClick={() => router.push("/estimate/new")}
                className="bg-blue-800 text-white px-5 py-3 rounded font-bold uppercase tracking-widest text-xs flex items-center gap-2 shadow-lg shadow-blue-900/20 hover:scale-[1.02] transition-transform"
              >
                <IconBolt />
                Analyse a Part
              </button>
              <button
                onClick={() => router.push("/rfq/new")}
                className="bg-white border-2 border-slate-900 text-slate-900 px-5 py-3 rounded font-bold uppercase tracking-widest text-xs flex items-center gap-2 hover:bg-slate-50 transition-colors"
              >
                <IconAnalytics />
                Extract from PDF
              </button>
            </div>
          </div>

          {error && (
            <div role="alert" className="bg-red-50 border border-red-200 rounded px-4 py-3 text-red-700 text-sm mb-6 font-mono">
              {error}
            </div>
          )}

          {/* Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            {/* Card 1 — Analyses */}
            <div className="bg-white p-6 border border-slate-200 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-blue-50 -mr-8 -mt-8 rounded-full transition-transform group-hover:scale-110" />
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">Analysis Profile</span>
                  <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-[10px] font-black rounded">
                    {(usage?.total_estimates ?? 0) > 0 ? "ACTIVE" : "READY"}
                  </span>
                </div>
                <div className="text-4xl font-mono font-bold text-slate-900 mb-1">
                  {usage?.total_estimates ?? 0}
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Analyses Run</div>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] text-slate-400 font-mono">Should-cost breakdowns</span>
                <IconAnalytics />
              </div>
            </div>

            {/* Card 2 — Similarity */}
            <div className="bg-white p-6 border border-slate-200 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-50 -mr-8 -mt-8 rounded-full transition-transform group-hover:scale-110" />
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">Supplier Intel</span>
                  <span className="px-2 py-0.5 bg-emerald-100 text-emerald-700 text-[10px] font-black rounded">SCANNED</span>
                </div>
                <div className="text-4xl font-mono font-bold text-slate-900 mb-1">
                  {usage?.total_similarity ?? 0}
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Parts Matched</div>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] text-slate-400 font-mono">Visual similarity searches</span>
                <IconSearch />
              </div>
            </div>

            {/* Card 3 — Leverage */}
            <div className="bg-white p-6 border border-slate-200 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-red-50 -mr-8 -mt-8 rounded-full transition-transform group-hover:scale-110" />
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">Latest Confidence</span>
                  <span className={`px-2 py-0.5 text-[10px] font-black rounded ${confidenceBadge(latestEstimate?.confidence_tier ?? null).className}`}>
                    {confidenceBadge(latestEstimate?.confidence_tier ?? null).label}
                  </span>
                </div>
                <div className="text-4xl font-mono font-bold text-slate-900 mb-1">
                  {latestEstimate
                    ? `${latestEstimate.currency}\u00A0${latestEstimate.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`
                    : "—"}
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Latest Should-Cost</div>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] text-slate-400 font-mono">
                  {latestEstimate
                    ? new Date(latestEstimate.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short" })
                    : "No estimates yet"}
                </span>
                <IconRadar />
              </div>
            </div>
          </div>

          {/* Intelligence Feed + Priority */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Intelligence Feed */}
            <div className="lg:col-span-2 space-y-6">
              <div className="flex items-center justify-between px-2">
                <h2 className="font-black text-lg tracking-tight flex items-center gap-2" style={{ fontFamily: "var(--font-inter)" }}>
                  <span className="w-2 h-6 bg-blue-800 rounded-full" />
                  RECENT ANALYSES
                </h2>
                <span className="text-[10px] font-mono text-blue-600 bg-blue-50 px-2 py-1 rounded animate-pulse">
                  LIVE
                </span>
              </div>

              {estimates.length === 0 ? (
                <div className="bg-white border border-slate-200 p-12 text-center">
                  <div className="w-12 h-12 bg-blue-50 rounded flex items-center justify-center mx-auto mb-4">
                    <IconBolt />
                  </div>
                  <p className="font-bold text-slate-900 mb-1">No analyses yet</p>
                  <p className="text-slate-500 text-sm mb-6">Upload your first engineering drawing to begin the margin attack.</p>
                  <button
                    onClick={() => router.push("/estimate/new")}
                    className="bg-blue-800 text-white px-6 py-2.5 rounded font-bold uppercase tracking-widest text-xs hover:bg-blue-900 transition-colors"
                  >
                    Upload your first drawing
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {estimates.slice(0, 5).map((est) => {
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
                        className="bg-white border border-slate-200 p-5 hover:border-blue-300 transition-colors cursor-pointer"
                        onClick={() => router.push(`/estimate/${est.id}`)}
                        role="link"
                        tabIndex={0}
                        onKeyDown={(e) => { if (e.key === "Enter") router.push(`/estimate/${est.id}`); }}
                      >
                        <div className="flex gap-4">
                          <div className={`${partBg(est.part_type)} text-white p-3 h-fit rounded`}>
                            <IconRadar />
                          </div>
                          <div className="flex-1">
                            <div className="flex justify-between items-start mb-1">
                              <h3 className="font-bold text-slate-900 capitalize">
                                Should-Cost Analysis: {est.part_type.replace("_", " ")}
                              </h3>
                              <span className="font-mono text-[10px] text-slate-400">{timeLabel}</span>
                            </div>
                            <p className="text-sm text-slate-600 mb-4 leading-relaxed">
                              Analysis complete. Should-cost established at{" "}
                              <span className="text-blue-700 font-mono font-bold">
                                {est.currency} {est.total_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                              </span>{" "}
                              per unit.
                            </p>
                            <div className="flex gap-2 items-center">
                              <button
                                className="text-[10px] font-bold uppercase tracking-widest bg-blue-50 text-blue-700 px-3 py-1.5 hover:bg-blue-100 transition-colors"
                                onClick={(e) => { e.stopPropagation(); router.push(`/estimate/${est.id}`); }}
                              >
                                View Breakdown
                              </button>
                              <span className={`text-[10px] font-bold px-2 py-1 rounded ${badge.className}`}>
                                {badge.label}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}

                  {estimates.length > 5 && (
                    <div className="text-center pt-2">
                      <span className="text-xs font-mono text-slate-400">{estimates.length - 5} more analyses in archive</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Priority Sidebar */}
            <div className="space-y-6">
              <h2 className="font-black text-lg tracking-tight flex items-center gap-2 px-2" style={{ fontFamily: "var(--font-inter)" }}>
                <span className="w-2 h-6 bg-slate-400 rounded-full" />
                YOUR SUMMARY
              </h2>

              {/* Dark priority card */}
              <div className="bg-slate-900 text-white p-6 rounded-lg shadow-xl">
                <div className="mb-6">
                  <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-blue-400 mb-2">Your Progress</div>
                  <h4 className="text-xl font-black mb-1" style={{ fontFamily: "var(--font-inter)" }}>
                    {estimates.length > 0 ? "Analysis Active" : "Ready to Deploy"}
                  </h4>
                  <p className="text-xs text-slate-400">
                    {estimates.length > 0
                      ? `${estimates.length} should-cost analyses complete. Use breakdowns in supplier negotiations.`
                      : "Upload your first engineering drawing to begin should-cost intelligence."}
                  </p>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-[10px] mb-1 font-bold uppercase">
                      <span>Analysis Coverage</span>
                      <span>{Math.min(100, (usage?.total_estimates ?? 0) * 20)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="bg-blue-500 h-full rounded-full"
                        style={{ width: `${Math.min(100, (usage?.total_estimates ?? 0) * 20)}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-[10px] mb-1 font-bold uppercase">
                      <span>Supplier Intel</span>
                      <span>{Math.min(100, (usage?.total_similarity ?? 0) * 25)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="bg-teal-500 h-full rounded-full"
                        style={{ width: `${Math.min(100, (usage?.total_similarity ?? 0) * 25)}%` }}
                      />
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => router.push("/estimate/new")}
                  className="w-full mt-8 border border-blue-400 text-blue-400 py-3 rounded font-mono text-xs font-bold uppercase tracking-widest hover:bg-blue-400 hover:text-slate-900 transition-colors"
                >
                  Start an Analysis
                </button>
              </div>

              {/* Quick actions */}
              <div className="bg-white border border-slate-200 p-6">
                <h4 className="font-bold text-sm uppercase tracking-widest mb-4 text-slate-900">Quick Actions</h4>
                <div className="space-y-2">
                  {[
                    { label: "New Drawing Analysis", onClick: () => router.push("/estimate/new"), icon: <IconBolt /> },
                    { label: "PDF / RFQ Extractor", onClick: () => router.push("/rfq/new"), icon: <IconDoc /> },
                    { label: "Similar Parts Search", onClick: () => router.push("/similar"), icon: <IconSearch /> },
                  ].map(({ label, onClick, icon }) => (
                    <button
                      key={label}
                      onClick={onClick}
                      className="w-full flex items-center gap-3 px-3 py-2.5 text-left text-xs font-bold uppercase tracking-widest text-slate-600 hover:bg-slate-50 hover:text-blue-700 transition-colors border border-slate-100 rounded"
                    >
                      <span className="text-slate-400">{icon}</span>
                      {label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Settings link */}
              <div className="text-center">
                <button className="flex items-center gap-2 text-[10px] font-mono text-slate-400 hover:text-slate-600 transition-colors mx-auto uppercase tracking-widest">
                  <IconGear />
                  System Configuration
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 px-6 py-3 flex justify-around items-center z-50">
        {[
          { label: "Ops", icon: <IconDashboard />, onClick: () => {} },
          { label: "Attack", icon: <IconTrending />, onClick: () => router.push("/estimate/new") },
          { label: "Intel", icon: <IconSearch />, onClick: () => router.push("/similar") },
          { label: "Labs", icon: <IconDoc />, onClick: () => router.push("/rfq/new") },
        ].map(({ label, icon, onClick }) => (
          <button key={label} onClick={onClick} className="flex flex-col items-center text-slate-500 gap-0.5">
            {icon}
            <span className="text-[10px] font-bold">{label}</span>
          </button>
        ))}
      </nav>
    </div>
  );
}
