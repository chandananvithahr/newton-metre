import Link from "next/link";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

const FEATURES = [
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: "Physics engine, not prompts",
    desc: "MRR, Sandvik kc1 cutting data, Taylor tool life. The formulas your supplier uses — before margin.",
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
      </svg>
    ),
    title: "Indian job-shop economics",
    desc: "Real INR rates for 15 cities. CNC turning ₹800/hr, milling ₹1,000/hr. Not US benchmarks.",
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
      </svg>
    ),
    title: "Similarity search",
    desc: "Match current parts to past estimates. Build institutional cost memory that survives personnel changes.",
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
      </svg>
    ),
    title: "AI validation loop",
    desc: "Physics + Gemini run in parallel. When they disagree > 15%, an AI arbitrator resolves it line by line.",
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
      </svg>
    ),
    title: "Any drawing format",
    desc: "PDF, image, any CAD software. GPT-4o reads it; no pre-processing, no templates.",
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
      </svg>
    ),
    title: "4 part types covered",
    desc: "Turned, milled, sheet metal, PCB, cable assemblies. Defense, aerospace, automobile.",
  },
];

const STEPS = [
  {
    n: "01",
    title: "Upload your drawing",
    desc: "PDF or image — any format, any CAD software. Takes under 10 seconds.",
  },
  {
    n: "02",
    title: "AI extracts, physics calculates",
    desc: "Vision AI reads dimensions, tolerances, material. Physics engine computes costs from Sandvik cutting data and Indian job-shop rates.",
  },
  {
    n: "03",
    title: "Negotiate with numbers",
    desc: "Line-by-line: material, machining, setup, labour, overhead. Know exactly where margin is hiding.",
  },
];

const STATS = [
  { value: "±5–10%", label: "Accuracy" },
  { value: "<60s",   label: "Per estimate" },
  { value: "164",    label: "Physics tests" },
  { value: "4",      label: "Part types" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900 overflow-x-hidden">

      {/* ── Nav ── */}
      <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
          <span className="text-xl tracking-tight text-slate-900" style={{ fontFamily: "var(--font-heading)" }}>
            Costrich
          </span>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors hidden sm:block">
              Sign in
            </Link>
            <Link
              href="/login"
              className="bg-slate-900 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-slate-700 transition-colors"
            >
              Get started free
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative">
        {/* Dot grid background */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage: "radial-gradient(circle, #e2e8f0 1px, transparent 1px)",
            backgroundSize: "28px 28px",
          }}
        />
        {/* Fade out at bottom */}
        <div className="absolute inset-0 pointer-events-none bg-gradient-to-b from-transparent via-transparent to-white" />

        <div className="relative max-w-5xl mx-auto px-6 pt-20 pb-24 sm:pt-28 sm:pb-32 text-center">
          <div
            className="inline-flex items-center gap-2 mb-8 px-3 py-1.5 bg-white border border-slate-200 rounded-full text-sm text-slate-500 shadow-sm"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 inline-block" />
            Physics-based · Indian job-shop rates · ±5–10% accuracy
          </div>

          <h1
            className="text-5xl sm:text-6xl md:text-7xl mb-7 leading-[1.05] tracking-tight text-slate-900"
            style={{ fontFamily: "var(--font-heading)" }}
          >
            Know what every part<br />
            <span
              className="inline-block"
              style={{
                background: "linear-gradient(135deg, #0891b2 0%, #6366f1 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              should cost.
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-500 mb-10 max-w-2xl mx-auto leading-relaxed">
            Upload a drawing. Get a line-by-line cost breakdown in under 60 seconds.
            Material, machining, labour, overhead — before you negotiate.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              href="/login"
              className="inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-8 py-3.5 rounded-lg text-base font-semibold hover:bg-slate-700 transition-colors shadow-lg shadow-slate-900/10"
            >
              Try it free — no card needed
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <a
              href="#demo"
              className="inline-flex items-center justify-center gap-2 bg-white text-slate-600 px-8 py-3.5 rounded-lg text-base font-semibold border border-slate-200 hover:border-slate-400 transition-colors"
            >
              See a live output ↓
            </a>
          </div>

          <p className="text-xs text-slate-400 mt-5" style={{ fontFamily: "var(--font-mono)" }}>
            Built for defense · aerospace · automobile procurement teams in India
          </p>
        </div>
      </section>

      {/* ── Stats ── */}
      <section className="border-y border-slate-100 bg-slate-50">
        <div className="max-w-4xl mx-auto px-6 py-8 grid grid-cols-2 sm:grid-cols-4 sm:divide-x divide-slate-200">
          {STATS.map((s) => (
            <div key={s.label} className="text-center py-2 sm:py-0 sm:px-8">
              <div
                className="text-3xl font-bold text-slate-900 mb-0.5"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {s.value}
              </div>
              <div className="text-sm text-slate-400">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Product demo ── */}
      <section id="demo" className="max-w-6xl mx-auto px-6 py-20 sm:py-28">
        <div className="grid md:grid-cols-[1fr_1.1fr] gap-16 items-center">
          <div>
            <p
              className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-4"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              Live output
            </p>
            <h2
              className="text-4xl sm:text-5xl mb-5 tracking-tight leading-tight"
              style={{ fontFamily: "var(--font-heading)" }}
            >
              Every rupee,<br />explained.
            </h2>
            <p className="text-slate-500 leading-relaxed mb-6 text-lg">
              Machining time from physics. Material weight from geometry.
              Labour from real Indian shop floor rates.
              No black box — click any number to copy it.
            </p>
            <div className="space-y-3">
              {[
                "Sandvik kc1 cutting force data",
                "Taylor tool life equation",
                "15-city Indian labour rates",
                "40+ surface treatment processes",
              ].map((item) => (
                <div key={item} className="flex items-center gap-2.5 text-sm text-slate-600">
                  <span className="w-4 h-4 rounded-full bg-cyan-100 text-cyan-600 flex items-center justify-center text-xs font-bold flex-shrink-0">✓</span>
                  {item}
                </div>
              ))}
            </div>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 mt-8 text-sm font-semibold text-cyan-600 hover:text-cyan-800 transition-colors"
            >
              Run your own estimate →
            </Link>
          </div>

          {/* Browser chrome mockup */}
          <div className="rounded-2xl border border-slate-200 shadow-2xl shadow-slate-200/80 overflow-hidden">
            <div className="bg-slate-100 border-b border-slate-200 px-4 py-3 flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-red-400" />
              <div className="w-2.5 h-2.5 rounded-full bg-amber-400" />
              <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
              <div
                className="flex-1 mx-3 bg-white rounded px-3 py-1 text-xs text-slate-400"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                costrich.ai/estimate/en8-shaft-100qty
              </div>
            </div>
            <CostBreakdownTable />
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="bg-slate-50 border-y border-slate-100 py-20 sm:py-28">
        <div className="max-w-6xl mx-auto px-6">
          <div className="max-w-xl mb-14">
            <p
              className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-4"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              Under the hood
            </p>
            <h2
              className="text-4xl sm:text-5xl tracking-tight leading-tight"
              style={{ fontFamily: "var(--font-heading)" }}
            >
              Not another<br />AI wrapper.
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURES.map((f) => (
              <div
                key={f.title}
                className="bg-white rounded-xl p-6 border border-slate-200 hover:border-slate-300 hover:shadow-md transition-all"
              >
                <div className="w-9 h-9 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center mb-4">
                  {f.icon}
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-sm text-slate-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="max-w-6xl mx-auto px-6 py-20 sm:py-28">
        <div className="text-center max-w-xl mx-auto mb-16">
          <p
            className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-4"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            How it works
          </p>
          <h2
            className="text-4xl sm:text-5xl tracking-tight"
            style={{ fontFamily: "var(--font-heading)" }}
          >
            Drawing to negotiation<br />in three steps.
          </h2>
        </div>

        <div className="grid sm:grid-cols-3 gap-6">
          {STEPS.map((s) => (
            <div key={s.n} className="relative p-8 rounded-2xl border border-slate-200 bg-white">
              <div
                className="text-6xl font-bold text-slate-100 mb-6 leading-none"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {s.n}
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-3">{s.title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Comparison ── */}
      <section className="bg-slate-50 border-y border-slate-100 py-20 sm:py-28">
        <div className="max-w-5xl mx-auto px-6">
          <div className="max-w-xl mb-12">
            <p
              className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-4"
              style={{ fontFamily: "var(--font-mono)" }}
            >
              Why Costrich
            </p>
            <h2
              className="text-4xl sm:text-5xl tracking-tight leading-tight"
              style={{ fontFamily: "var(--font-heading)" }}
            >
              Stop negotiating<br />on gut feel.
            </h2>
          </div>

          <div className="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-white border-b border-slate-200">
                  <th className="text-left px-6 py-4 text-slate-400 font-medium w-44"></th>
                  <th className="text-left px-6 py-4 font-semibold text-red-500 w-[38%]">Without Costrich</th>
                  <th className="text-left px-6 py-4 font-semibold text-emerald-600">With Costrich</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-100">
                {[
                  { label: "Time to benchmark",      without: "2–3 days, 3 quotes",           with: "Under 60 seconds"               },
                  { label: "Negotiation basis",       without: "Gut feel",                      with: "Line-by-line breakdown"         },
                  { label: "Accuracy",                without: "Unknown until PO signed",       with: "±5–10% physics-based"           },
                  { label: "Institutional memory",    without: "Lost when people leave",        with: "Every estimate saved"           },
                  { label: "Team consistency",        without: "Each engineer's own estimate",  with: "Same physics model for all"     },
                ].map((row) => (
                  <tr key={row.label} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 text-slate-600 font-medium">{row.label}</td>
                    <td className="px-6 py-4 text-red-400">{row.without}</td>
                    <td className="px-6 py-4 text-emerald-600 font-medium">{row.with}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ── Pricing ── */}
      <section className="max-w-5xl mx-auto px-6 py-20 sm:py-28">
        <div className="text-center mb-14">
          <p
            className="text-xs font-semibold text-cyan-600 uppercase tracking-widest mb-4"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            Pricing
          </p>
          <h2
            className="text-4xl sm:text-5xl tracking-tight"
            style={{ fontFamily: "var(--font-heading)" }}
          >
            Start free. Scale when ready.
          </h2>
        </div>

        <div className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto">
          {/* Free */}
          <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
            <p className="text-sm font-medium text-slate-400 mb-1" style={{ fontFamily: "var(--font-mono)" }}>Free</p>
            <p className="text-4xl font-bold text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹0</p>
            <p className="text-sm text-slate-400 mb-8">Forever free, no card</p>
            <div className="space-y-3 mb-8">
              {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Cost breakdown view", "Similarity search"].map((f) => (
                <div key={f} className="flex items-center gap-2.5 text-sm text-slate-600">
                  <span className="text-cyan-500 font-bold">✓</span> {f}
                </div>
              ))}
            </div>
            <Link href="/login" className="block text-center bg-slate-900 text-white px-6 py-3 rounded-lg font-semibold hover:bg-slate-700 transition-colors">
              Get started free
            </Link>
          </div>

          {/* Pro */}
          <div className="bg-slate-900 text-white rounded-2xl p-8 relative overflow-hidden">
            <div className="absolute top-4 right-4 bg-amber-400 text-amber-900 text-xs font-bold px-2 py-0.5 rounded-full">
              Coming soon
            </div>
            <p className="text-sm font-medium text-slate-400 mb-1" style={{ fontFamily: "var(--font-mono)" }}>Pro</p>
            <p className="text-4xl font-bold text-white mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</p>
            <p className="text-sm text-slate-400 mb-8">per user / month</p>
            <div className="space-y-3 mb-8">
              {["Unlimited estimates", "PCB + cable assembly", "Persistent similarity index", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                <div key={f} className="flex items-center gap-2.5 text-sm text-slate-300">
                  <span className="text-cyan-400 font-bold">✓</span> {f}
                </div>
              ))}
            </div>
            <button disabled className="block w-full text-center bg-white/10 text-white/40 px-6 py-3 rounded-lg font-semibold cursor-not-allowed">
              Join waitlist
            </button>
          </div>
        </div>
      </section>

      {/* ── Final CTA — dark band ── */}
      <section className="bg-slate-950 text-white">
        <div className="max-w-3xl mx-auto px-6 py-20 sm:py-28 text-center">
          <h2
            className="text-4xl sm:text-5xl mb-5 tracking-tight leading-tight"
            style={{ fontFamily: "var(--font-heading)" }}
          >
            Stop negotiating blind.
          </h2>
          <p className="text-slate-400 mb-10 text-lg leading-relaxed">
            Your first estimate is free. Upload a drawing and see<br className="hidden sm:block" />
            what it should cost in under 60 seconds.
          </p>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 bg-white text-slate-900 px-10 py-4 rounded-lg text-base font-semibold hover:bg-slate-100 transition-colors"
          >
            Try Costrich free
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
          <p className="text-sm text-slate-600 mt-5" style={{ fontFamily: "var(--font-mono)" }}>
            No credit card · No setup · Just upload and go
          </p>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="bg-slate-950 border-t border-white/5 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-600">
          <span className="font-semibold text-white/60" style={{ fontFamily: "var(--font-heading)" }}>Costrich</span>
          <p>&copy; 2026 Costrich. Should-cost intelligence for manufacturing.</p>
          <div className="flex gap-5">
            <Link href="/login" className="hover:text-slate-400 transition-colors">Sign in</Link>
            <Link href="/login" className="hover:text-slate-400 transition-colors">Get started</Link>
          </div>
        </div>
      </footer>

    </div>
  );
}
