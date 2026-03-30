import Link from "next/link";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

// ─── Static data ────────────────────────────────────────────────────────────

const STATS = [
  { value: "±5–10%", label: "Accuracy vs actual PO" },
  { value: "<60s",   label: "Per estimate" },
  { value: "4",      label: "Part types" },
  { value: "164",    label: "Physics tests passing" },
];

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

const COMPARISON: { label: string; without: string; with: string }[] = [
  { label: "Time to benchmark",     without: "2–3 days (3 supplier quotes)",  with: "Under 60 seconds"               },
  { label: "Negotiation leverage",  without: "Gut feel, no data",             with: "Line-by-line breakdown"         },
  { label: "Accuracy",              without: "Unknown until PO is signed",    with: "±5–10% physics-based"           },
  { label: "Institutional memory",  without: "Lost when people leave",        with: "Every estimate saved"           },
  { label: "Cross-team consistency",without: "Each engineer's own benchmark", with: "Same physics model for everyone"},
];

const PARTS = ["Turned parts", "Milled parts", "Sheet metal", "PCB assemblies", "Cable assemblies"];

// ─── Page ────────────────────────────────────────────────────────────────────

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900">

      {/* ── Nav ── */}
      <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-200">
        <div className="max-w-5xl mx-auto flex items-center justify-between px-4 sm:px-8 py-4">
          <span className="text-xl tracking-tight text-cyan-600" style={{ fontFamily: "var(--font-heading)" }}>
            Costrich
          </span>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm font-medium text-slate-500 hover:text-slate-700 transition-colors">
              Sign in
            </Link>
            <Link
              href="/login"
              className="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-slate-700 transition-colors"
            >
              Try it free →
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="border-b border-slate-100">
        {/* Subtle radial gradient from top */}
        <div className="relative overflow-hidden">
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background: "radial-gradient(ellipse 80% 40% at 50% -10%, rgba(6,182,212,0.08) 0%, transparent 70%)",
            }}
          />
          <div className="max-w-5xl mx-auto px-4 sm:px-8 pt-16 pb-14 sm:pt-24 sm:pb-20 relative">
            <div
              className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 bg-cyan-50 text-cyan-700 rounded-full text-sm font-medium border border-cyan-200"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 inline-block" />
              Physics-based should-cost estimation
            </div>

            <h1 className="text-4xl sm:text-5xl md:text-6xl mb-6 leading-[1.1] tracking-tight text-slate-900">
              Know what a part<br />
              <span className="text-cyan-600">should cost.</span><br />
              Before you negotiate.
            </h1>

            <p className="text-lg sm:text-xl text-slate-500 mb-10 max-w-2xl leading-relaxed">
              Upload a drawing. Get a line-by-line cost breakdown in under 60 seconds —
              material, machining, labour, overhead. Accurate to ±5–10%.
              Built for Indian procurement teams.
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/login"
                className="inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-8 py-4 rounded-lg text-base font-semibold hover:bg-slate-700 transition-colors"
              >
                Get your first estimate free
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <a
                href="#how-it-works"
                className="inline-flex items-center justify-center gap-2 bg-white text-slate-600 px-8 py-4 rounded-lg text-base font-semibold border border-slate-200 hover:border-slate-400 hover:text-slate-800 transition-colors"
              >
                See how it works
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats bar ── */}
      <section className="border-b border-slate-100 bg-slate-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-6 grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-0 sm:divide-x divide-slate-200">
          {STATS.map((s) => (
            <div key={s.label} className="text-center sm:px-6">
              <div className="text-2xl sm:text-3xl font-semibold text-cyan-600 mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {s.value}
              </div>
              <div className="text-sm text-slate-500">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Sample output ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="grid md:grid-cols-2 gap-12 items-start">
          <div>
            <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
              Sample output
            </div>
            <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight leading-tight text-slate-900">
              Line by line.<br />No black box.
            </h2>
            <p className="text-slate-500 leading-relaxed mb-6">
              Every rupee is explained. Machining time from physics. Material weight from geometry.
              Labour from real Indian shop floor rates. Click any value in the table to copy it.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 text-cyan-600 font-semibold hover:text-cyan-800 transition-colors"
            >
              Run your own estimate →
            </Link>
          </div>
          <CostBreakdownTable />
        </div>
      </section>

      {/* ── How it works ── */}
      <section id="how-it-works" className="bg-slate-50 border-y border-slate-100 py-16 sm:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            How it works
          </div>
          <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-slate-900">
            From drawing to negotiation
          </h2>

          <table className="w-full text-sm border border-slate-200 rounded-xl overflow-hidden shadow-sm">
            <thead>
              <tr className="bg-slate-100 border-b border-slate-200">
                <th className="text-left px-5 py-3 text-slate-400 font-medium w-16" style={{ fontFamily: "var(--font-mono)" }}>#</th>
                <th className="text-left px-5 py-3 text-slate-600 font-medium w-48">Action</th>
                <th className="text-left px-5 py-3 text-slate-600 font-medium">What happens</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-4 text-cyan-600 font-semibold" style={{ fontFamily: "var(--font-mono)" }}>01</td>
                <td className="px-5 py-4 text-slate-800 font-semibold">Upload drawing</td>
                <td className="px-5 py-4 text-slate-500 leading-relaxed">PDF or image — any format, any CAD software. GPT-4o vision reads it; Gemini cross-checks.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-4 text-cyan-600 font-semibold" style={{ fontFamily: "var(--font-mono)" }}>02</td>
                <td className="px-5 py-4 text-slate-800 font-semibold">AI extracts & calculates</td>
                <td className="px-5 py-4 text-slate-500 leading-relaxed">Vision AI reads dimensions, tolerances, material, processes. Physics engine computes real costs using Sandvik cutting data and Indian job-shop rates.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-4 text-cyan-600 font-semibold" style={{ fontFamily: "var(--font-mono)" }}>03</td>
                <td className="px-5 py-4 text-slate-800 font-semibold">Negotiate with confidence</td>
                <td className="px-5 py-4 text-slate-500 leading-relaxed">Line-by-line breakdown: material, machining, setup, labour, overhead. Know exactly where your supplier is adding margin.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Why Costrich — comparison table ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
          Why Costrich
        </div>
        <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-slate-900">Built differently</h2>

        <div className="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="text-left px-5 py-3 text-slate-400 font-medium w-48"></th>
                <th className="text-left px-5 py-3 font-semibold text-red-500 w-[35%]">
                  <span className="flex items-center gap-2">
                    <span>✗</span> Without Costrich
                  </span>
                </th>
                <th className="text-left px-5 py-3 font-semibold text-emerald-600">
                  <span className="flex items-center gap-2">
                    <span>✓</span> With Costrich
                  </span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {COMPARISON.map((row) => (
                <tr key={row.label} className="hover:bg-slate-50 transition-colors">
                  <td className="px-5 py-3.5 text-slate-600 font-medium">{row.label}</td>
                  <td className="px-5 py-3.5 text-red-400">{row.without}</td>
                  <td className="px-5 py-3.5 text-emerald-600">{row.with}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Under the hood ── */}
      <section className="bg-slate-50 border-y border-slate-100 py-16 sm:py-24">
        <div className="max-w-5xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            Under the hood
          </div>
          <h2 className="text-3xl sm:text-4xl mb-10 tracking-tight text-slate-900">
            Not another AI wrapper
          </h2>

          <table className="w-full text-sm border border-slate-200 rounded-xl overflow-hidden shadow-sm">
            <thead>
              <tr className="bg-slate-100 border-b border-slate-200">
                <th className="text-left px-5 py-3 text-slate-600 font-medium w-64">Feature</th>
                <th className="text-left px-5 py-3 text-slate-600 font-medium">What it means</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {FEATURES.map((f) => (
                <tr key={f.name} className="hover:bg-slate-50 transition-colors">
                  <td className="px-5 py-4 font-semibold text-slate-800 align-top">{f.name}</td>
                  <td className="px-5 py-4 text-slate-500 leading-relaxed">{f.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ── Coverage ── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
          Coverage
        </div>
        <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-slate-900">
          Defense · Aerospace · Automobile
        </h2>
        <p className="text-slate-500 mb-8 max-w-lg mx-auto leading-relaxed">
          Built for Indian job shops. Covers the parts your procurement team buys most.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {PARTS.map((tag) => (
            <span key={tag} className="px-4 py-2 bg-white border border-slate-200 rounded-full text-sm font-medium text-slate-600 shadow-sm">
              {tag}
            </span>
          ))}
        </div>
      </section>

      {/* ── Pricing ── */}
      <section className="bg-slate-50 border-y border-slate-100 py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-8 text-center">
          <div className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>
            Pricing
          </div>
          <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-slate-900">Simple. Start free.</h2>
          <p className="text-slate-500 mb-12">No credit card required. No commitment.</p>

          <div className="grid sm:grid-cols-2 gap-6 text-left">
            {/* Free */}
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
              <div className="text-sm font-medium text-slate-500 mb-1" style={{ fontFamily: "var(--font-mono)" }}>Free</div>
              <div className="text-4xl font-semibold text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹0</div>
              <div className="text-sm text-slate-400 mb-6">Forever free</div>
              <table className="w-full text-sm mb-8">
                <tbody className="divide-y divide-slate-100">
                  {[
                    "10 estimates / month",
                    "Mechanical + sheet metal parts",
                    "PDF & image uploads",
                    "Cost breakdown export",
                    "Similarity search (session-scoped)",
                  ].map((f) => (
                    <tr key={f}>
                      <td className="py-2 text-slate-600">
                        <span className="text-cyan-500 mr-2">✓</span>{f}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <Link
                href="/login"
                className="block text-center bg-slate-900 text-white px-6 py-3 rounded-lg font-semibold hover:bg-slate-700 transition-colors"
              >
                Get started free
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-white border-2 border-cyan-200 rounded-2xl p-8 shadow-sm relative overflow-hidden">
              <div className="absolute top-4 right-4 bg-amber-400 text-amber-900 text-xs font-bold px-2 py-0.5 rounded-full">
                Coming soon
              </div>
              <div className="text-sm font-medium text-cyan-600 mb-1" style={{ fontFamily: "var(--font-mono)" }}>Pro</div>
              <div className="text-4xl font-semibold text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</div>
              <div className="text-sm text-slate-400 mb-6">per user / month</div>
              <table className="w-full text-sm mb-8">
                <tbody className="divide-y divide-slate-100">
                  {[
                    "Unlimited estimates",
                    "PCB + cable assembly support",
                    "Persistent similarity index",
                    "Team cost memory",
                    "Export to Excel / PDF",
                    "Priority support",
                  ].map((f) => (
                    <tr key={f}>
                      <td className="py-2 text-slate-600">
                        <span className="text-cyan-400 mr-2">✓</span>{f}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <button
                disabled
                className="block w-full text-center bg-slate-100 text-slate-400 px-6 py-3 rounded-lg font-semibold cursor-not-allowed"
              >
                Join waitlist
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ── Final CTA ── */}
      <section className="max-w-3xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-slate-900">
          Stop negotiating blind.
        </h2>
        <p className="text-slate-500 mb-8 text-lg leading-relaxed">
          Your first estimate is free. Upload a drawing and see what it should cost in under 60 seconds.
        </p>
        <Link
          href="/login"
          className="inline-flex items-center gap-2 bg-slate-900 text-white px-10 py-4 rounded-lg text-lg font-semibold hover:bg-slate-700 transition-colors"
        >
          Try Costrich free
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Link>
        <p className="text-sm text-slate-400 mt-4">No credit card. No setup. Just upload and go.</p>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-100 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-400">
          <span className="font-semibold text-cyan-600" style={{ fontFamily: "var(--font-heading)" }}>Costrich</span>
          <p>&copy; 2026 Costrich. Should-cost intelligence for manufacturing.</p>
          <div className="flex gap-4">
            <Link href="/login" className="hover:text-slate-600 transition-colors">Sign in</Link>
            <Link href="/login" className="hover:text-slate-600 transition-colors">Get started</Link>
          </div>
        </div>
      </footer>

    </div>
  );
}
