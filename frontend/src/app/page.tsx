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
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-gray-100">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-4 sm:px-8 py-4">
          <span className="text-xl font-bold tracking-tight text-primary-700" style={{ fontFamily: "var(--font-heading)" }}>
            Costrich
          </span>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
              Sign in
            </Link>
            <Link
              href="/login"
              className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-primary-700 transition-colors shadow-sm"
            >
              Try it free →
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-gray-100">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-slate-50" />
        <div className="relative max-w-5xl mx-auto px-4 sm:px-8 pt-16 pb-12 sm:pt-24 sm:pb-20">
          <div className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 bg-primary-100 text-primary-700 rounded-full text-sm font-medium animate-fade-in-up">
            <span className="w-2 h-2 rounded-full bg-primary-500 inline-block" />
            Physics-based should-cost estimation
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-6 leading-[1.1] tracking-tight text-gray-900 animate-fade-in-up-delay-1">
            Know what a part<br />
            <span className="text-primary-600">should cost.</span><br />
            Before you negotiate.
          </h1>
          <p className="text-lg sm:text-xl text-gray-500 mb-10 max-w-2xl leading-relaxed animate-fade-in-up-delay-2">
            Upload a drawing. Get a line-by-line cost breakdown in under 60 seconds —
            material, machining, labour, overhead. Accurate to ±5–10%.
            Built for Indian procurement teams.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 animate-fade-in-up-delay-3">
            <Link
              href="/login"
              className="inline-flex items-center justify-center gap-2 bg-primary-600 text-white px-8 py-4 rounded-lg text-base font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20"
            >
              Get your first estimate free
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center justify-center gap-2 bg-white text-gray-700 px-8 py-4 rounded-lg text-base font-semibold border border-gray-200 hover:border-gray-300 transition-colors"
            >
              See how it works
            </a>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <section className="border-b border-gray-100 bg-slate-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-6 grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-0 sm:divide-x divide-gray-200">
          {STATS.map((s) => (
            <div key={s.label} className="text-center sm:px-6">
              <div className="text-2xl sm:text-3xl font-extrabold text-primary-600 mb-1" style={{ fontFamily: "var(--font-mono)" }}>
                {s.value}
              </div>
              <div className="text-sm text-gray-500">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Mock cost breakdown */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">Sample output</div>
            <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight leading-tight">
              Line by line.<br />No black box.
            </h2>
            <p className="text-gray-500 leading-relaxed mb-6">
              Every rupee is explained. Machining time from physics. Material weight from geometry.
              Labour from real Indian shop floor rates. You see exactly what you should pay — and where your supplier is adding margin.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 text-primary-600 font-semibold hover:text-primary-700 transition-colors"
            >
              Run your own estimate →
            </Link>
          </div>

          {/* Mock breakdown card */}
          <div className="bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-primary-700 px-5 py-4 flex items-center justify-between">
              <div>
                <div className="text-white text-sm font-semibold">EN8 Steel Shaft — Ø50×100mm</div>
                <div className="text-primary-300 text-xs mt-0.5">Qty 100 · CNC Turning + Drilling + Threading</div>
              </div>
              <span className="bg-green-400/20 text-green-300 text-xs font-semibold px-2 py-1 rounded-full border border-green-400/30">
                HIGH confidence
              </span>
            </div>
            <div className="divide-y divide-gray-100">
              {COST_LINES.map((line) => (
                <div key={line.label} className="flex items-center justify-between px-5 py-3">
                  <span className="text-sm text-gray-600">{line.label}</span>
                  <span className="text-sm font-semibold text-gray-900 font-mono tabular-nums">{line.value}</span>
                </div>
              ))}
            </div>
            <div className="bg-primary-50 border-t-2 border-primary-200 px-5 py-4 flex items-center justify-between">
              <span className="font-bold text-gray-900">Should cost / unit</span>
              <span className="text-xl font-extrabold text-primary-700 font-mono">₹695</span>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="bg-slate-50 border-y border-gray-100 py-16 sm:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">How it works</div>
          <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight">From drawing to negotiation</h2>
          <p className="text-gray-500 mb-12 max-w-xl leading-relaxed">
            Upload a drawing, get a detailed cost breakdown. No manual data entry, no spreadsheets.
          </p>
          <div className="space-y-0">
            {STEPS.map((step, i) => (
              <div key={step.num} className="flex gap-6 group">
                {/* Timeline */}
                <div className="flex flex-col items-center">
                  <div className="w-10 h-10 rounded-full bg-primary-600 text-white flex items-center justify-center flex-shrink-0 shadow-md shadow-primary-600/20">
                    {step.icon}
                  </div>
                  {i < STEPS.length - 1 && (
                    <div className="w-px flex-1 bg-primary-200 my-2" />
                  )}
                </div>
                {/* Content */}
                <div className={`flex-1 pb-10 ${i === STEPS.length - 1 ? "pb-0" : ""}`}>
                  <div className="text-xs font-mono font-semibold text-primary-400 mb-1">{step.num}</div>
                  <h3 className="text-lg font-bold mb-1.5 text-gray-900">{step.title}</h3>
                  <p className="text-gray-500 leading-relaxed text-sm">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* vs manual quoting */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24">
        <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3 text-center">Why Costrich</div>
        <h2 className="text-3xl sm:text-4xl font-extrabold mb-12 tracking-tight text-center">Built differently</h2>
        <div className="grid sm:grid-cols-2 gap-6">
          {/* Before */}
          <div className="border border-red-100 bg-red-50 rounded-2xl p-6">
            <div className="text-sm font-semibold text-red-500 mb-4 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Without Costrich
            </div>
            <ul className="space-y-3 text-sm text-red-700">
              {[
                "2–3 days to get 3 quotes from suppliers",
                "No idea if quotes are fair or inflated",
                "Negotiation based on gut feel",
                "Tribal knowledge leaves when people do",
                "Different engineers use different cost benchmarks",
              ].map((t) => (
                <li key={t} className="flex items-start gap-2">
                  <span className="mt-0.5 text-red-400">✗</span>
                  {t}
                </li>
              ))}
            </ul>
          </div>
          {/* After */}
          <div className="border border-green-200 bg-green-50 rounded-2xl p-6">
            <div className="text-sm font-semibold text-green-600 mb-4 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              With Costrich
            </div>
            <ul className="space-y-3 text-sm text-green-700">
              {[
                "Should-cost in under 60 seconds",
                "Line-by-line breakdown to challenge every rupee",
                "Walk into negotiation knowing the floor price",
                "Every estimate saved — builds institutional memory",
                "Consistent physics-based benchmarks across team",
              ].map((t) => (
                <li key={t} className="flex items-start gap-2">
                  <span className="mt-0.5 text-green-500">✓</span>
                  {t}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-slate-50 border-y border-gray-100 py-16 sm:py-24">
        <div className="max-w-5xl mx-auto px-4 sm:px-8">
          <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">Under the hood</div>
          <h2 className="text-3xl sm:text-4xl font-extrabold mb-12 tracking-tight">
            Not another AI wrapper
          </h2>
          <div className="grid sm:grid-cols-2 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <h3 className="font-bold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Industries / part types */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">Coverage</div>
        <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight">
          Defense · Aerospace · Automobile
        </h2>
        <p className="text-gray-500 mb-8 max-w-lg mx-auto leading-relaxed">
          Built for Indian job shops. Covers the parts your procurement team buys most.
        </p>
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {PARTS.map((tag) => (
            <span key={tag} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium text-gray-700 shadow-sm">
              {tag}
            </span>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-slate-50 border-y border-gray-100 py-16 sm:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-8 text-center">
          <div className="text-xs font-semibold text-primary-600 uppercase tracking-widest mb-3">Pricing</div>
          <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight">Simple. Start free.</h2>
          <p className="text-gray-500 mb-12">No credit card required. No commitment.</p>
          <div className="grid sm:grid-cols-2 gap-6 text-left">
            {/* Free */}
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
              <div className="text-sm font-semibold text-gray-500 mb-1">Free</div>
              <div className="text-4xl font-extrabold text-gray-900 mb-1 font-mono">₹0</div>
              <div className="text-sm text-gray-400 mb-6">Forever free</div>
              <ul className="space-y-3 text-sm text-gray-600 mb-8">
                {[
                  "10 estimates / month",
                  "Mechanical + sheet metal parts",
                  "PDF & image uploads",
                  "Cost breakdown export",
                  "Similarity search (session-scoped)",
                ].map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <span className="text-primary-500">✓</span> {f}
                  </li>
                ))}
              </ul>
              <Link
                href="/login"
                className="block text-center bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                Get started free
              </Link>
            </div>
            {/* Pro */}
            <div className="bg-primary-700 border border-primary-600 rounded-2xl p-8 shadow-xl relative overflow-hidden">
              <div className="absolute top-4 right-4 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-0.5 rounded-full">
                Coming soon
              </div>
              <div className="text-sm font-semibold text-primary-300 mb-1">Pro</div>
              <div className="text-4xl font-extrabold text-white mb-1 font-mono">₹4,999</div>
              <div className="text-sm text-primary-400 mb-6">per user / month</div>
              <ul className="space-y-3 text-sm text-primary-200 mb-8">
                {[
                  "Unlimited estimates",
                  "PCB + cable assembly support",
                  "Persistent similarity index",
                  "Team cost memory",
                  "Export to Excel / PDF",
                  "Priority support",
                ].map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <span className="text-yellow-400">✓</span> {f}
                  </li>
                ))}
              </ul>
              <button
                disabled
                className="block w-full text-center bg-white/10 text-white px-6 py-3 rounded-lg font-semibold cursor-not-allowed border border-white/20"
              >
                Join waitlist
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="max-w-3xl mx-auto px-4 sm:px-8 py-16 sm:py-24 text-center">
        <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight">
          Stop negotiating blind.
        </h2>
        <p className="text-gray-500 mb-8 text-lg leading-relaxed">
          Your first estimate is free. Upload a drawing and see what it should cost in under 60 seconds.
        </p>
        <Link
          href="/login"
          className="inline-flex items-center gap-2 bg-primary-600 text-white px-10 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20"
        >
          Try Costrich free
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Link>
        <p className="text-sm text-gray-400 mt-4">No credit card. No setup. Just upload and go.</p>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-400">
          <span className="font-semibold text-primary-700" style={{ fontFamily: "var(--font-heading)" }}>Costrich</span>
          <p>&copy; 2026 Costrich. Should-cost intelligence for manufacturing.</p>
          <div className="flex gap-4">
            <Link href="/login" className="hover:text-gray-600 transition-colors">Sign in</Link>
            <Link href="/login" className="hover:text-gray-600 transition-colors">Get started</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
