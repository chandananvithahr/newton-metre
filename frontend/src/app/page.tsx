import Link from "next/link";

const STATS = [
  { value: "±5–10%", label: "Accuracy vs actual PO" },
  { value: "<60s", label: "Per estimate" },
  { value: "4", label: "Part types supported" },
  { value: "164", label: "Physics tests passing" },
];

const STEPS = [
  {
    num: "01",
    title: "Upload drawing",
    desc: "PDF or image of your engineering drawing — any format, any CAD software.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
      </svg>
    ),
  },
  {
    num: "02",
    title: "AI extracts & calculates",
    desc: "Vision AI reads dimensions, tolerances, material, and processes. Physics engine computes real costs using Indian job-shop rates.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
      </svg>
    ),
  },
  {
    num: "03",
    title: "Negotiate with confidence",
    desc: "Line-by-line cost breakdown: material, machining, setup, labour, overhead. Know exactly where to push back.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
      </svg>
    ),
  },
];

const COST_LINES = [
  { label: "Raw material (EN8 Steel, 0.38 kg)", value: "₹228" },
  { label: "CNC Turning (8.4 min @ ₹800/hr)", value: "₹112" },
  { label: "Drilling × 4 holes (3.2 min)", value: "₹32" },
  { label: "Threading (2.1 min)", value: "₹21" },
  { label: "Setup cost (amortised / 100 qty)", value: "₹45" },
  { label: "Tooling", value: "₹18" },
  { label: "Labour", value: "₹38" },
  { label: "Power", value: "₹9" },
  { label: "Overhead (15%)", value: "₹76" },
  { label: "Profit margin (20%)", value: "₹116" },
];

const PARTS = ["Turned parts", "Milled parts", "Sheet metal", "PCB assemblies", "Cable assemblies"];

const FEATURES = [
  {
    title: "Physics-based, not AI hallucination",
    desc: "MRR calculations, Sandvik cutting data, Taylor tool life. The same formulas your supplier uses — before they add margin.",
  },
  {
    title: "Indian job-shop economics",
    desc: "Real INR rates for 15 cities. CNC turning ₹800/hr, milling ₹1000/hr, labour ₹250/hr. Not US or EU benchmarks.",
  },
  {
    title: "Similarity search",
    desc: "Find past estimates for similar parts. See what you paid vs. what it should cost. Build institutional cost memory.",
  },
  {
    title: "AI validation loop",
    desc: "Physics engine and Gemini run in parallel. When they disagree >15%, an AI arbitrator resolves the gap line by line.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0F1117]">
      {/* Nav */}
      <nav className="sticky top-0 z-50 bg-[#0F1117]/95 backdrop-blur border-b border-[#2A3140]">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-4 sm:px-8 py-4">
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

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-[#2A3140]">
        <div className="absolute inset-0 bg-gradient-to-br from-[#0F1117] via-[#161B27] to-[#0F1117]" />
        <div className="relative max-w-5xl mx-auto px-4 sm:px-8 pt-16 pb-12 sm:pt-24 sm:pb-20">
          <div className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 bg-[#22D3EE]/10 text-[#22D3EE] rounded-full text-sm font-medium border border-[#22D3EE]/20 animate-fade-in-up" style={{ fontFamily: "var(--font-mono)" }}>
            <span className="w-2 h-2 rounded-full bg-[#22D3EE] inline-block" />
            Physics-based should-cost estimation
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl mb-6 leading-[1.1] tracking-tight text-[#E2E8F0] animate-fade-in-up-delay-1">
            Know what a part<br />
            <span className="text-[#22D3EE]">should cost.</span><br />
            Before you negotiate.
          </h1>
          <p className="text-lg sm:text-xl text-[#64748B] mb-10 max-w-2xl leading-relaxed animate-fade-in-up-delay-2">
            Upload a drawing. Get a line-by-line cost breakdown in under 60 seconds —
            material, machining, labour, overhead. Accurate to ±5–10%.
            Built for Indian procurement teams.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 animate-fade-in-up-delay-3">
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

      {/* Stats bar */}
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

      {/* Mock cost breakdown */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>Sample output</div>
            <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight leading-tight text-[#E2E8F0]">
              Line by line.<br />No black box.
            </h2>
            <p className="text-[#64748B] leading-relaxed mb-6">
              Every rupee is explained. Machining time from physics. Material weight from geometry.
              Labour from real Indian shop floor rates. You see exactly what you should pay — and where your supplier is adding margin.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 text-[#22D3EE] font-semibold hover:text-[#06B6D4] transition-colors"
            >
              Run your own estimate →
            </Link>
          </div>

          {/* Mock breakdown card */}
          <div className="bg-[#161B27] border border-[#2A3140] rounded-2xl overflow-hidden">
            <div className="bg-[#1C2235] px-5 py-4 flex items-center justify-between border-b border-[#2A3140]">
              <div>
                <div className="text-[#E2E8F0] text-sm font-semibold">EN8 Steel Shaft — Ø50×100mm</div>
                <div className="text-[#64748B] text-xs mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>Qty 100 · CNC Turning + Drilling + Threading</div>
              </div>
              <span className="bg-emerald-950/60 text-emerald-400 text-xs font-semibold px-2 py-1 rounded-full border border-emerald-800" style={{ fontFamily: "var(--font-mono)" }}>
                HIGH
              </span>
            </div>
            <div className="divide-y divide-[#2A3140]">
              {COST_LINES.map((line) => (
                <div key={line.label} className="flex items-center justify-between px-5 py-2.5">
                  <span className="text-sm text-[#64748B]">{line.label}</span>
                  <span className="text-sm font-medium text-[#E2E8F0]" style={{ fontFamily: "var(--font-mono)", fontVariantNumeric: "tabular-nums" }}>{line.value}</span>
                </div>
              ))}
            </div>
            <div className="bg-[#22D3EE] px-5 py-4 flex items-center justify-between">
              <span className="font-bold text-[#0F1117] text-sm">Should cost / unit</span>
              <span className="text-xl font-bold text-[#0F1117]" style={{ fontFamily: "var(--font-mono)" }}>₹695</span>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>How it works</div>
          <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-[#E2E8F0]">From drawing to negotiation</h2>
          <p className="text-[#64748B] mb-12 max-w-xl leading-relaxed">
            Upload a drawing, get a detailed cost breakdown. No manual data entry, no spreadsheets.
          </p>
          <div className="space-y-0">
            {STEPS.map((step, i) => (
              <div key={step.num} className="flex gap-6 group">
                <div className="flex flex-col items-center">
                  <div className="w-10 h-10 rounded-full bg-[#22D3EE] text-[#0F1117] flex items-center justify-center flex-shrink-0">
                    {step.icon}
                  </div>
                  {i < STEPS.length - 1 && (
                    <div className="w-px flex-1 bg-[#2A3140] my-2" />
                  )}
                </div>
                <div className={`flex-1 pb-10 ${i === STEPS.length - 1 ? "pb-0" : ""}`}>
                  <div className="text-xs font-medium text-[#475569] mb-1" style={{ fontFamily: "var(--font-mono)" }}>{step.num}</div>
                  <h3 className="text-lg font-semibold mb-1.5 text-[#E2E8F0]">{step.title}</h3>
                  <p className="text-[#64748B] leading-relaxed text-sm">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* vs manual quoting */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3 text-center" style={{ fontFamily: "var(--font-mono)" }}>Why Costrich</div>
        <h2 className="text-3xl sm:text-4xl mb-12 tracking-tight text-center text-[#E2E8F0]">Built differently</h2>
        <div className="grid sm:grid-cols-2 gap-6">
          {/* Before */}
          <div className="border border-red-900/50 bg-red-950/20 rounded-2xl p-6">
            <div className="text-sm font-semibold text-red-400 mb-4 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Without Costrich
            </div>
            <ul className="space-y-3 text-sm text-red-400/80">
              {[
                "2–3 days to get 3 quotes from suppliers",
                "No idea if quotes are fair or inflated",
                "Negotiation based on gut feel",
                "Tribal knowledge leaves when people do",
                "Different engineers use different cost benchmarks",
              ].map((t) => (
                <li key={t} className="flex items-start gap-2">
                  <span className="mt-0.5 text-red-600">✗</span>
                  {t}
                </li>
              ))}
            </ul>
          </div>
          {/* After */}
          <div className="border border-emerald-900/50 bg-emerald-950/20 rounded-2xl p-6">
            <div className="text-sm font-semibold text-emerald-400 mb-4 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              With Costrich
            </div>
            <ul className="space-y-3 text-sm text-emerald-400/80">
              {[
                "Should-cost in under 60 seconds",
                "Line-by-line breakdown to challenge every rupee",
                "Walk into negotiation knowing the floor price",
                "Every estimate saved — builds institutional memory",
                "Consistent physics-based benchmarks across team",
              ].map((t) => (
                <li key={t} className="flex items-start gap-2">
                  <span className="mt-0.5 text-emerald-500">✓</span>
                  {t}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-5xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>Under the hood</div>
          <h2 className="text-3xl sm:text-4xl mb-12 tracking-tight text-[#E2E8F0]">
            Not another AI wrapper
          </h2>
          <div className="grid sm:grid-cols-2 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="bg-[#1C2235] rounded-xl border border-[#2A3140] p-6">
                <h3 className="font-semibold text-[#E2E8F0] mb-2">{f.title}</h3>
                <p className="text-[#64748B] text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Industries / part types */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>Coverage</div>
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

      {/* Pricing */}
      <section className="bg-[#161B27] border-y border-[#2A3140] py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-8 text-center">
          <div className="text-xs font-medium text-[#22D3EE] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-mono)" }}>Pricing</div>
          <h2 className="text-3xl sm:text-4xl mb-4 tracking-tight text-[#E2E8F0]">Simple. Start free.</h2>
          <p className="text-[#64748B] mb-12">No credit card required. No commitment.</p>
          <div className="grid sm:grid-cols-2 gap-6 text-left">
            {/* Free */}
            <div className="bg-[#1C2235] border border-[#2A3140] rounded-2xl p-8">
              <div className="text-sm font-medium text-[#64748B] mb-1" style={{ fontFamily: "var(--font-mono)" }}>Free</div>
              <div className="text-4xl font-medium text-[#E2E8F0] mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹0</div>
              <div className="text-sm text-[#475569] mb-6">Forever free</div>
              <ul className="space-y-3 text-sm text-[#64748B] mb-8">
                {[
                  "10 estimates / month",
                  "Mechanical + sheet metal parts",
                  "PDF & image uploads",
                  "Cost breakdown export",
                  "Similarity search (session-scoped)",
                ].map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <span className="text-[#22D3EE]">✓</span> {f}
                  </li>
                ))}
              </ul>
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
              <ul className="space-y-3 text-sm text-[#64748B] mb-8">
                {[
                  "Unlimited estimates",
                  "PCB + cable assembly support",
                  "Persistent similarity index",
                  "Team cost memory",
                  "Export to Excel / PDF",
                  "Priority support",
                ].map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <span className="text-[#22D3EE]/50">✓</span> {f}
                  </li>
                ))}
              </ul>
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

      {/* Final CTA */}
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

      {/* Footer */}
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
