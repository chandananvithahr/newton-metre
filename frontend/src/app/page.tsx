import Link from "next/link";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

// ─── Static data ────────────────────────────────────────────────────────────

const STATS = [
  { value: "±5–10%", label: "Accuracy vs actual PO" },
  { value: "<60s",   label: "Per estimate" },
  { value: "4",      label: "Part types" },
  { value: "164",    label: "Physics tests" },
];

// Table pattern from dns.toys — named row, description, monospace value
const FEATURES: { name: string; desc: string }[] = [
  {
    name: "Physics-based, not guesswork",
    desc: "MRR calculations, Sandvik kc1 cutting data, Taylor tool life. The same formulas your supplier uses — before they add margin.",
  },
  {
    name: "Indian job-shop economics",
    desc: "Real INR rates for 15 cities. CNC turning ₹800/hr, milling ₹1,000/hr, labour ₹250/hr. Not US or EU benchmarks.",
  },
  {
    name: "Similarity search",
    desc: "Find past estimates for similar parts. Compare what you paid vs. what it should have cost. Build institutional cost memory.",
  },
  {
    name: "AI validation loop",
    desc: "Physics engine and Gemini run in parallel. When they disagree > 15%, an AI arbitrator resolves the gap line by line.",
  },
];

// Single comparison table — Kailash Nadh pattern: one table beats two cards
const COMPARISON: { label: string; without: string; with: string }[] = [
  { label: "Time to benchmark",        without: "2–3 days (3 supplier quotes)",  with: "Under 60 seconds"                  },
  { label: "Negotiation leverage",      without: "Gut feel, no data",             with: "Line-by-line breakdown"            },
  { label: "Accuracy",                  without: "Unknown until PO is signed",    with: "±5–10% physics-based"              },
  { label: "Institutional memory",      without: "Lost when people leave",        with: "Every estimate saved"              },
  { label: "Cross-team consistency",    without: "Each engineer's own benchmark", with: "Same physics model for everyone"   },
];

const PARTS = ["Turned parts", "Milled parts", "Sheet metal", "PCB assemblies", "Cable assemblies"];

// ─── Page ────────────────────────────────────────────────────────────────────

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0F1117]">

      {/* ── Nav ── */}
      <nav className="sticky top-0 z-50 bg-[#0F1117]/95 backdrop-blur border-b border-[#2A3140]">
        <div className="max-w-5xl mx-auto flex items-center justify-between px-4 sm:px-8 py-4">
          <span className="text-xl tracking-tight text-[#22D3EE]" style={{ fontFamily: "var(--font-heading)" }}>
            Costrich
          </span>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm font-medium text-[#64748B] hover:text-[#94A3B8] transition-colors">
              Sign in
            </Link>
            <Link
              href="/login"
              className="bg-[#22D3EE] text-[#0F1117] px-4 py-2 rounded-lg text-sm font-semibold hover:bg-[#06B6D4] transition-colors"
            >
              Try it free →
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="border-b border-[#2A3140]">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 pt-16 pb-12 sm:pt-24 sm:pb-20">
          <div
            className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 bg-[#22D3EE]/10 text-[#22D3EE] rounded-full text-sm font-medium border border-[#22D3EE]/20"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            <span className="w-2 h-2 rounded-full bg-[#22D3EE] inline-block" />
            Physics-based should-cost estimation
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl mb-6 leading-[1.1] tracking-tight text-[#E2E8F0]">
            Know what a part<br />
            <span className="text-[#22D3EE]">should cost.</span><br />
            Before you negotiate.
          </h1>
          <p className="text-lg sm:text-xl text-[#64748B] mb-10 max-w-2xl leading-relaxed">
            Upload a drawing. Get a line-by-line cost breakdown in under 60 seconds —
            material, machining, labour, overhead. Accurate to ±5–10%.
            Built for Indian procurement teams.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              href="/login"
              className="inline-flex items-center justify-center gap-2 bg-[#22D3EE] text-[#0F1117] px-8 py-4 rounded-lg text-base font-semibold hover:bg-[#06B6D4] transition-colors"
            >
              Get your first estimate free
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center justify-center gap-2 bg-[#161B27] text-[#94A3B8] px-8 py-4 rounded-lg text-base font-semibold border border-[#2A3140] hover:border-[#475569] transition-colors"
            >
              See how it works
            </a>
          </div>
        </div>
      </section>

      {/* ── Stats bar ── */}
      <section className="border-b border-[#2A3140] bg-[#161B27]">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-6 grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-0 sm:divide-x divide-[#2A3140]">
          {STATS.map((s) => (
            <div key={s.label} className="text-center sm:px-6">
              <div className="text-2xl sm:text-3xl font-medium text-[#22D3EE] mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {s.value}
              </div>
              <div className="text-sm text-[#64748B]">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Sample output ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="grid md:grid-cols-2 gap-12 items-start">
          <div>
            <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
              Sample output
            </div>
            <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight leading-tight text-[#E2E8F0]">
              Line by line.<br />No black box.
            </h2>
            <p className="text-[#64748B] leading-relaxed mb-6">
              Every rupee is explained. Machining time from physics. Material weight from geometry.
              Labour from real Indian shop floor rates. Click any value in the table to copy it.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 text-[#22D3EE] font-semibold hover:text-[#06B6D4] transition-colors"
            >
              Run your own estimate →
            </Link>
          </div>

          <CostBreakdownTable />
        </div>
      </section>

      {/* ── How it works ── */}
      <section id="how-it-works" className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            How it works
          </div>
          <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-[#E2E8F0]">
            From drawing to negotiation
          </h2>

          {/* Table pattern from dns.toys — step | action | what happens */}
          <table className="w-full text-sm border border-[#2A3140] rounded-xl overflow-hidden">
            <thead>
              <tr className="bg-[#1C2235] border-b border-[#2A3140]">
                <th className="text-left px-5 py-3 text-[#475569] font-medium w-16" style={{ fontFamily: "var(--font-mono)" }}>#</th>
                <th className="text-left px-5 py-3 text-[#94A3B8] font-medium w-48">Action</th>
                <th className="text-left px-5 py-3 text-[#94A3B8] font-medium">What happens</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A3140]">
              <tr className="hover:bg-[#1C2235] transition-colors">
                <td className="px-5 py-4 text-[#22D3EE] font-medium" style={{ fontFamily: "var(--font-mono)" }}>01</td>
                <td className="px-5 py-4 text-[#E2E8F0] font-semibold">Upload drawing</td>
                <td className="px-5 py-4 text-[#64748B] leading-relaxed">PDF or image — any format, any CAD software. GPT-4o vision reads it; Gemini cross-checks.</td>
              </tr>
              <tr className="hover:bg-[#1C2235] transition-colors">
                <td className="px-5 py-4 text-[#22D3EE] font-medium" style={{ fontFamily: "var(--font-mono)" }}>02</td>
                <td className="px-5 py-4 text-[#E2E8F0] font-semibold">AI extracts & calculates</td>
                <td className="px-5 py-4 text-[#64748B] leading-relaxed">Vision AI reads dimensions, tolerances, material, processes. Physics engine computes real costs using Sandvik cutting data and Indian job-shop rates.</td>
              </tr>
              <tr className="hover:bg-[#1C2235] transition-colors">
                <td className="px-5 py-4 text-[#22D3EE] font-medium" style={{ fontFamily: "var(--font-mono)" }}>03</td>
                <td className="px-5 py-4 text-[#E2E8F0] font-semibold">Negotiate with confidence</td>
                <td className="px-5 py-4 text-[#64748B] leading-relaxed">Line-by-line breakdown: material, machining, setup, labour, overhead. Know exactly where your supplier is adding margin.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Why Costrich — comparison table ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
          Why Costrich
        </div>
        <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-[#E2E8F0]">Built differently</h2>

        {/* Comparison table — one table beats two separate cards */}
        <div className="border border-[#2A3140] rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-[#1C2235] border-b border-[#2A3140]">
                <th className="text-left px-5 py-3 text-[#475569] font-medium w-48"></th>
                <th className="text-left px-5 py-3 font-semibold text-red-400 w-[35%]">
                  <span className="flex items-center gap-2">
                    <span className="text-red-600">✗</span> Without Costrich
                  </span>
                </th>
                <th className="text-left px-5 py-3 font-semibold text-emerald-400">
                  <span className="flex items-center gap-2">
                    <span className="text-emerald-500">✓</span> With Costrich
                  </span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A3140]">
              {COMPARISON.map((row) => (
                <tr key={row.label} className="hover:bg-[#161B27] transition-colors">
                  <td className="px-5 py-3.5 text-[#94A3B8] font-medium">{row.label}</td>
                  <td className="px-5 py-3.5 text-red-400/70">{row.without}</td>
                  <td className="px-5 py-3.5 text-emerald-400/80">{row.with}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Under the hood — feature table ── */}
      <section className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-5xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            Under the hood
          </div>
          <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-[#E2E8F0]">
            Not another AI wrapper
          </h2>

          {/* Feature table — name | description, dns.toys pattern */}
          <table className="w-full text-sm border border-[#2A3140] rounded-xl overflow-hidden">
            <thead>
              <tr className="bg-[#1C2235] border-b border-[#2A3140]">
                <th className="text-left px-5 py-3 text-[#94A3B8] font-medium w-64">Feature</th>
                <th className="text-left px-5 py-3 text-[#94A3B8] font-medium">What it means</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A3140]">
              {FEATURES.map((f) => (
                <tr key={f.name} className="hover:bg-[#1C2235] transition-colors">
                  <td className="px-5 py-4 font-semibold text-[#E2E8F0] align-top">{f.name}</td>
                  <td className="px-5 py-4 text-[#64748B] leading-relaxed">{f.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Coverage ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
          Coverage
        </div>
        <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-[#E2E8F0]">
          Defense · Aerospace · Automobile
        </h2>
        <p className="text-[#64748B] mb-8 max-w-lg mx-auto leading-relaxed">
          Built for Indian job shops. Covers the parts your procurement team buys most.
        </p>
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {PARTS.map((tag) => (
            <span key={tag} className="px-4 py-2 bg-[#161B27] border border-[#2A3140] rounded-full text-sm font-medium text-[#94A3B8]">
              {tag}
            </span>
          ))}
        </div>
      </section>

      {/* ── Pricing ── */}
      <section className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-8 text-center">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            Pricing
          </div>
          <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-[#E2E8F0]">Simple. Start free.</h2>
          <p className="text-[#64748B] mb-12">No credit card required. No commitment.</p>

          <div className="grid sm:grid-cols-2 gap-6 text-left">
            {/* Free */}
            <div className="bg-[#1C2235] border border-[#2A3140] rounded-2xl p-8">
              <div className="text-sm font-medium text-[#64748B] mb-1" style={{ fontFamily: "var(--font-mono)" }}>Free</div>
              <div className="text-4xl font-medium text-[#E2E8F0] mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹0</div>
              <div className="text-sm text-[#475569] mb-6">Forever free</div>
              <table className="w-full text-sm mb-8">
                <tbody className="divide-y divide-[#2A3140]">
                  {[
                    "10 estimates / month",
                    "Mechanical + sheet metal parts",
                    "PDF & image uploads",
                    "Cost breakdown export",
                    "Similarity search (session-scoped)",
                  ].map((f) => (
                    <tr key={f}>
                      <td className="py-2 text-[#64748B]">
                        <span className="text-[#22D3EE] mr-2">✓</span>{f}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <Link
                href="/login"
                className="block text-center bg-[#22D3EE] text-[#0F1117] px-6 py-3 rounded-lg font-semibold hover:bg-[#06B6D4] transition-colors"
              >
                Get started free
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-[#0D1520] border border-[#22D3EE]/20 rounded-2xl p-8 relative overflow-hidden">
              <div className="absolute top-4 right-4 bg-amber-400 text-amber-900 text-xs font-bold px-2 py-0.5 rounded-full">
                Coming soon
              </div>
              <div className="text-sm font-medium text-[#22D3EE]/70 mb-1" style={{ fontFamily: "var(--font-mono)" }}>Pro</div>
              <div className="text-4xl font-medium text-[#E2E8F0] mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</div>
              <div className="text-sm text-[#475569] mb-6">per user / month</div>
              <table className="w-full text-sm mb-8">
                <tbody className="divide-y divide-[#2A3140]">
                  {[
                    "Unlimited estimates",
                    "PCB + cable assembly support",
                    "Persistent similarity index",
                    "Team cost memory",
                    "Export to Excel / PDF",
                    "Priority support",
                  ].map((f) => (
                    <tr key={f}>
                      <td className="py-2 text-[#64748B]">
                        <span className="text-[#22D3EE]/50 mr-2">✓</span>{f}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <button
                disabled
                className="block w-full text-center bg-[#22D3EE]/10 text-[#22D3EE]/50 px-6 py-3 rounded-lg font-semibold cursor-not-allowed border border-[#22D3EE]/20"
              >
                Join waitlist
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ── Final CTA ── */}
      <section className="max-w-3xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-[#E2E8F0]">
          Stop negotiating blind.
        </h2>
        <p className="text-[#64748B] mb-8 text-lg leading-relaxed">
          Your first estimate is free. Upload a drawing and see what it should cost in under 60 seconds.
        </p>
        <Link
          href="/login"
          className="inline-flex items-center gap-2 bg-[#22D3EE] text-[#0F1117] px-10 py-4 rounded-lg text-lg font-semibold hover:bg-[#06B6D4] transition-colors"
        >
          Try Costrich free
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Link>
        <p className="text-sm text-[#475569] mt-4">No credit card. No setup. Just upload and go.</p>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-[#2A3140] py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-[#475569]">
          <span className="font-medium text-[#22D3EE]" style={{ fontFamily: "var(--font-heading)" }}>Costrich</span>
          <p>&copy; 2026 Costrich. Should-cost intelligence for manufacturing.</p>
          <div className="flex gap-4">
            <Link href="/login" className="hover:text-[#64748B] transition-colors">Sign in</Link>
            <Link href="/login" className="hover:text-[#64748B] transition-colors">Get started</Link>
          </div>
        </div>
      </footer>

    </div>
  );
}
