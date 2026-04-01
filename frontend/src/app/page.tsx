import Link from "next/link";
import Image from "next/image";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#F8F8F6] text-slate-900">

      {/* ── Nav ── */}
      <nav className="bg-[#F8F8F6]/90 backdrop-blur-md flex justify-between items-center w-full px-6 lg:px-10 h-16 lg:h-20 fixed top-0 z-50 border-b border-slate-200">
        <div className="flex items-center gap-10">
          <Link href="/" className="flex items-center gap-2.5">
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={40} height={40} className="rounded-xl" />
            <span style={{ fontFamily: "var(--font-heading)" }} className="text-[22px] text-cyan-600 tracking-tight">Newton-Metre</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            {[["How it works", "#how-it-works"], ["Pricing", "#pricing"]].map(([l, h]) => (
              <a key={l} href={h} className="text-[13px] text-slate-500 hover:text-slate-800 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login" className="hidden sm:block text-[13px] text-slate-500 hover:text-slate-800 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2.5 bg-cyan-600 text-white text-[13px] font-semibold rounded-lg hover:bg-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
            Upload a drawing
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ════════════════════════════════════════════════════════════
            HERO — "Newton-Metre does the work. You negotiate."
            ════════════════════════════════════════════════════════════ */}
        <section className="relative py-24 lg:py-32 flex flex-col items-center px-6 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.025]" style={{ backgroundImage: "radial-gradient(circle, #94A3B8 1px, transparent 1px)", backgroundSize: "28px 28px" }} />

          <div className="max-w-4xl w-full text-center relative z-10">
            {/* Eyebrow */}
            <p className="mb-6 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
              Should-cost intelligence + Similarity search
            </p>

            <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(36px,6vw,72px)] tracking-tight leading-[1.06] text-slate-900 mb-6">
              Newton-Metre does the work.<br />
              <span className="text-cyan-600 italic">You negotiate.</span>
            </h1>

            <p className="max-w-xl mx-auto text-[17px] text-slate-500 leading-[1.7] mb-10" style={{ fontFamily: "var(--font-sans)" }}>
              Upload a drawing. Newton-Metre reads it, calculates every cost line, and finds
              similar parts your company has already made. 60 seconds. Line by line.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-cyan-600 text-white text-[15px] font-semibold rounded-lg hover:bg-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                Upload a drawing — free
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 bg-white border border-slate-200 text-slate-600 text-[15px] font-semibold rounded-lg hover:border-slate-300 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                See a live estimate ↓
              </a>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            TWO SUPERPOWERS — side by side, immediately visible
            ════════════════════════════════════════════════════════════ */}
        <section className="py-20 lg:py-24 bg-white border-y border-slate-200">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <p className="text-center mb-4 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
              Two superpowers
            </p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4vw,48px)] text-slate-900 tracking-tight leading-tight mb-5">
              Know what it costs. Find what you&apos;ve made.
            </h2>
            <p className="text-center max-w-2xl mx-auto text-[16px] text-slate-500 leading-[1.7] mb-14" style={{ fontFamily: "var(--font-sans)" }}>
              Newton-Metre isn&apos;t a dashboard you stare at. It reads the drawing, runs the numbers, searches your history, and hands you the answer.
            </p>

            <div className="grid lg:grid-cols-2 gap-8">

              {/* ── Superpower 1: Should-Cost ── */}
              <div className="bg-[#F8F8F6] border border-slate-200 rounded-2xl p-8 lg:p-10">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-cyan-50 rounded-xl flex items-center justify-center">
                    <svg className="w-5 h-5 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-[10px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Superpower 1</p>
                    <h3 className="text-[18px] font-semibold text-slate-900 tracking-tight" style={{ fontFamily: "var(--font-sans)" }}>Should-Cost Breakdown</h3>
                  </div>
                </div>

                <p className="text-[15px] text-slate-600 leading-[1.7] mb-6" style={{ fontFamily: "var(--font-sans)" }}>
                  Newton-Metre reads the drawing, extracts every dimension, identifies manufacturing processes,
                  and calculates what the part <span className="font-semibold text-slate-800">should</span> cost — material, machining, finishing, overhead, margin.
                </p>

                {/* Mini cost preview */}
                <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
                  <div className="divide-y divide-slate-100">
                    {[
                      ["Raw material", "EN8, 0.38 kg", "₹228"],
                      ["CNC Turning", "8.4 min", "₹112"],
                      ["Drilling", "× 4 holes", "₹32"],
                      ["Setup + tooling", "qty 100", "₹63"],
                      ["Overhead + margin", "15% + 20%", "₹192"],
                    ].map(([label, detail, cost]) => (
                      <div key={label} className="flex items-center justify-between px-5 py-2.5">
                        <div className="flex items-center gap-3">
                          <span className="text-[13px] text-slate-600" style={{ fontFamily: "var(--font-sans)" }}>{label}</span>
                          <span className="text-[11px] text-slate-400" style={{ fontFamily: "var(--font-mono)" }}>{detail}</span>
                        </div>
                        <span className="text-[13px] font-semibold text-slate-700 tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>{cost}</span>
                      </div>
                    ))}
                  </div>
                  <div className="bg-slate-900 text-white px-5 py-3 flex items-center justify-between">
                    <span className="text-[13px] font-semibold" style={{ fontFamily: "var(--font-sans)" }}>Should-cost / unit</span>
                    <span className="text-[18px] font-bold tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>₹695</span>
                  </div>
                </div>

                <div className="mt-5 flex items-center gap-5">
                  {[["±5–10%", "Accuracy"], ["<60s", "Result"], ["₹/unit", "Line by line"]].map(([val, label]) => (
                    <div key={label} className="flex items-center gap-2">
                      <span className="text-[13px] font-bold text-cyan-600" style={{ fontFamily: "var(--font-mono)" }}>{val}</span>
                      <span className="text-[11px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>{label}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* ── Superpower 2: Similarity Search ── */}
              <div className="bg-gradient-to-b from-[#F0FDFA] to-[#F7FDFB] border border-cyan-200 rounded-2xl p-8 lg:p-10">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-cyan-50 rounded-xl flex items-center justify-center">
                    <svg className="w-5 h-5 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-[10px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Superpower 2</p>
                    <h3 className="text-[18px] font-semibold text-slate-900 tracking-tight" style={{ fontFamily: "var(--font-sans)" }}>Similarity Search</h3>
                  </div>
                </div>

                <p className="text-[15px] text-slate-600 leading-[1.7] mb-6" style={{ fontFamily: "var(--font-sans)" }}>
                  Newton-Metre searches thousands of drawings and finds every similar part your company has already
                  designed, costed, and manufactured. <span className="font-semibold text-slate-800">Your company&apos;s brain — searchable in seconds.</span>
                </p>

                {/* Mini similarity preview */}
                <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
                  <div className="px-5 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                    <span className="text-[10px] text-slate-400 uppercase tracking-[0.15em]" style={{ fontFamily: "var(--font-mono)" }}>Matches found</span>
                    <span className="text-[10px] text-cyan-600 font-medium" style={{ fontFamily: "var(--font-mono)" }}>3 results</span>
                  </div>
                  <div className="divide-y divide-slate-100">
                    {[
                      { name: "Bracket-A4521", dept: "Design · Rajesh K.", match: 92, cost: "₹1,180" },
                      { name: "Mount-B2290", dept: "Procurement · Priya S.", match: 78, cost: "₹1,340" },
                      { name: "Flange-C0087", dept: "Quality · Amit P.", match: 65, cost: "₹890" },
                    ].map((item) => {
                      const color = item.match >= 80 ? "bg-emerald-500" : item.match >= 60 ? "bg-amber-500" : "bg-slate-300";
                      return (
                        <div key={item.name} className="px-5 py-3 flex items-center justify-between">
                          <div>
                            <p className="text-[13px] font-medium text-slate-800" style={{ fontFamily: "var(--font-sans)" }}>{item.name}</p>
                            <p className="text-[10px] text-slate-400 mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>{item.dept} · {item.cost}</p>
                          </div>
                          <div className="flex items-center gap-2.5">
                            <div className="w-14 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                              <div className={`h-full ${color} rounded-full`} style={{ width: `${item.match}%` }} />
                            </div>
                            <span className="text-[12px] font-semibold text-slate-700 w-9 text-right tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>{item.match}%</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Department tags */}
                <div className="mt-5 flex flex-wrap gap-2">
                  {["Design", "Procurement", "Sales", "Quality"].map((dept) => (
                    <span key={dept} className="text-[10px] px-3 py-1.5 bg-white border border-cyan-200 rounded-full text-cyan-700 uppercase tracking-[0.15em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
                      {dept}
                    </span>
                  ))}
                  <span className="text-[10px] px-3 py-1.5 text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>
                    Every department. One brain.
                  </span>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            LIVE DEMO — Interactive cost breakdown
            ════════════════════════════════════════════════════════════ */}
        <section id="demo" className="py-20 lg:py-24 px-6">
          <div className="max-w-3xl mx-auto">
            <p className="text-center mb-4 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Live example</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-3">
              This is what the answer looks like.
            </h2>
            <p className="text-center max-w-lg mx-auto text-[15px] text-slate-500 leading-[1.7] mb-10" style={{ fontFamily: "var(--font-sans)" }}>
              Every cost line. Every assumption visible. Click any value to copy.
            </p>
            <CostBreakdownTable />
            <p className="text-center mt-8">
              <Link href="/login" className="text-[14px] font-semibold text-cyan-600 hover:text-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                Get your own breakdown →
              </Link>
            </p>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            HOW IT WORKS — 3 steps
            ════════════════════════════════════════════════════════════ */}
        <section id="how-it-works" className="py-20 lg:py-24 bg-white border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="text-center mb-4 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>How it works</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4">
              Upload. Newton-Metre does the rest.
            </h2>
            <p className="text-center max-w-xl mx-auto text-[15px] text-slate-500 leading-[1.7] mb-14" style={{ fontFamily: "var(--font-sans)" }}>
              No configuration. No prompting. No learning curve. One upload, two superpowers.
            </p>

            <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
              {[
                {
                  n: "01",
                  title: "You upload a drawing",
                  desc: "PDF, DXF, DWG, STEP, or even a photo. Newton-Metre extracts dimensions, material, tolerances, and processes directly.",
                },
                {
                  n: "02",
                  title: "Newton-Metre does the work",
                  desc: "Calculates every cost line — material, machining, finishing, overhead. Searches your history for similar parts. Validates with AI cross-check.",
                },
                {
                  n: "03",
                  title: "You negotiate with data",
                  desc: "Line-by-line breakdown ready to use. Similar parts from your past. Zero spreadsheets. The supplier can't hide margins.",
                },
              ].map((s) => (
                <div key={s.n} className="relative bg-[#F8F8F6] border border-slate-200 rounded-2xl p-8 hover:border-cyan-300 transition-colors">
                  <span className="text-[40px] font-bold text-slate-100 absolute top-6 right-8 select-none" style={{ fontFamily: "var(--font-mono)" }}>{s.n}</span>
                  <h3 className="text-[16px] font-semibold text-slate-900 mb-3 relative" style={{ fontFamily: "var(--font-sans)" }}>{s.title}</h3>
                  <p className="text-[14px] text-slate-500 leading-[1.7] relative" style={{ fontFamily: "var(--font-sans)" }}>{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            BEFORE / AFTER — The shift
            ════════════════════════════════════════════════════════════ */}
        <section className="py-20 lg:py-24">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="text-center mb-4 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>The shift</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-14">
              Your team is negotiating blind.
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Before */}
              <div className="bg-white border border-slate-200 rounded-2xl p-8">
                <p className="text-[10px] text-red-500 uppercase tracking-[0.2em] font-medium mb-6" style={{ fontFamily: "var(--font-mono)" }}>Without Newton-Metre</p>
                <div className="space-y-4">
                  {[
                    "Call 3 suppliers, wait 2 weeks for counter-quotes",
                    "Negotiate on gut feel — no cost data to challenge with",
                    "\"We made something like this once...\" but nobody can find it",
                    "Senior engineer retires — knowledge walks out the door",
                  ].map((text) => (
                    <div key={text} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-red-300 mt-2 shrink-0" />
                      <span className="text-[14px] text-slate-600 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* After */}
              <div className="bg-cyan-50/60 border border-cyan-200 rounded-2xl p-8">
                <p className="text-[10px] text-cyan-600 uppercase tracking-[0.2em] font-medium mb-6" style={{ fontFamily: "var(--font-mono)" }}>With Newton-Metre</p>
                <div className="space-y-4">
                  {[
                    "Newton-Metre reads the drawing, delivers the answer in 60 seconds",
                    "Newton-Metre breaks down every cost: material, machining, finishing, margin",
                    "Newton-Metre finds similar parts from your entire history — instantly",
                    "Knowledge stays in the system — searchable by every department, forever",
                  ].map((text) => (
                    <div key={text} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 mt-2 shrink-0" />
                      <span className="text-[14px] text-slate-700 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            STATS — Social proof
            ════════════════════════════════════════════════════════════ */}
        <section className="py-20 lg:py-24 bg-slate-50 border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <div className="grid lg:grid-cols-2 gap-14 items-center">
              <div>
                <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight leading-tight mb-5">
                  Every overpaid part compounds.
                </h2>
                <p className="text-[15px] text-slate-500 leading-[1.7] mb-5" style={{ fontFamily: "var(--font-sans)" }}>
                  200 parts a month. Overpaying 20% on half of them? That&apos;s lakhs per year.
                  Not because your team is bad — because they don&apos;t have the data.
                </p>
                <p className="text-[15px] text-slate-500 leading-[1.7] mb-8" style={{ fontFamily: "var(--font-sans)" }}>
                  Newton-Metre does the homework. Reads the drawing. Calculates every cost line.
                  Finds similar parts from your history. Hands you the answer.
                </p>
                <Link href="/login" className="inline-flex px-7 py-3.5 bg-cyan-600 text-white text-[14px] font-semibold rounded-lg hover:bg-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                  Upload a drawing — free
                </Link>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { val: "164+", label: "Estimates run" },
                    { val: "±5–10%", label: "Accuracy" },
                    { val: "<60s", label: "Time to result" },
                  ].map((s) => (
                    <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-5 text-center">
                      <div className="text-[20px] font-bold text-cyan-600 mb-1" style={{ fontFamily: "var(--font-mono)" }}>{s.val}</div>
                      <div className="text-[11px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>{s.label}</div>
                    </div>
                  ))}
                </div>
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <p className="text-[10px] text-slate-400 uppercase tracking-[0.15em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Live benchmark</p>
                  <p className="text-[14px] font-semibold text-slate-800 mb-2" style={{ fontFamily: "var(--font-sans)" }}>EN8 Steel Shaft — Ø50×100mm</p>
                  <p className="text-[13px] text-slate-500 mb-2" style={{ fontFamily: "var(--font-sans)" }}>Supplier quoted ₹2,400 — should-cost: ₹1,400</p>
                  <span className="text-[14px] font-bold text-emerald-600" style={{ fontFamily: "var(--font-mono)" }}>42% savings found</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            PRICING
            ════════════════════════════════════════════════════════════ */}
        <section id="pricing" className="py-20 lg:py-24">
          <div className="max-w-4xl mx-auto px-6 lg:px-10 text-center">
            <p className="mb-4 text-[11px] text-cyan-600 uppercase tracking-[0.2em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Pricing</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-3">
              Start free. Pay when it pays for itself.
            </h2>
            <p className="max-w-lg mx-auto text-[15px] text-slate-500 leading-[1.7] mb-14" style={{ fontFamily: "var(--font-sans)" }}>
              One estimate that catches a 20% overpayment pays for a year of Pro.
            </p>

            <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left">
              {/* Free */}
              <div className="bg-white border border-slate-200 rounded-2xl p-8">
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] mb-2" style={{ fontFamily: "var(--font-mono)" }}>Free</p>
                <p className="text-[36px] text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹0</p>
                <p className="text-[13px] text-slate-400 mb-6" style={{ fontFamily: "var(--font-sans)" }}>Forever free, no card required</p>
                <div className="space-y-3 mb-8">
                  {["10 estimates / month", "Should-cost breakdown", "Similarity search", "PDF & image uploads", "All part types"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5">
                      <svg className="w-4 h-4 text-cyan-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                      <span className="text-[13px] text-slate-600" style={{ fontFamily: "var(--font-sans)" }}>{f}</span>
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center bg-cyan-600 text-white px-6 py-3.5 rounded-lg font-semibold hover:bg-cyan-700 transition-colors text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>
                  Upload a drawing
                </Link>
              </div>

              {/* Pro */}
              <div className="bg-white border border-cyan-200 rounded-2xl p-8 relative">
                <div className="absolute top-4 right-4 bg-amber-50 text-amber-600 text-[10px] px-2.5 py-1 rounded-full uppercase tracking-[0.15em] border border-amber-200 font-medium" style={{ fontFamily: "var(--font-mono)" }}>Coming soon</div>
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] mb-2" style={{ fontFamily: "var(--font-mono)" }}>Pro</p>
                <p className="text-[36px] text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</p>
                <p className="text-[13px] text-slate-400 mb-6" style={{ fontFamily: "var(--font-sans)" }}>per user / month</p>
                <div className="space-y-3 mb-8">
                  {["Unlimited estimates", "Persistent part library", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5">
                      <svg className="w-4 h-4 text-cyan-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                      <span className="text-[13px] text-slate-600" style={{ fontFamily: "var(--font-sans)" }}>{f}</span>
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-slate-100 text-slate-400 px-6 py-3.5 rounded-lg font-semibold cursor-not-allowed text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            FINAL CTA
            ════════════════════════════════════════════════════════════ */}
        <section className="py-20 lg:py-24 bg-slate-50 border-t border-slate-200">
          <div className="max-w-3xl mx-auto px-6 lg:px-10 text-center">
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(32px,5vw,56px)] text-slate-900 tracking-tight leading-tight mb-5">
              Newton-Metre does the work.<br />
              <span className="text-cyan-600 italic">You negotiate.</span>
            </h2>
            <p className="text-[17px] text-slate-500 leading-[1.7] mb-10" style={{ fontFamily: "var(--font-sans)" }}>
              Upload a drawing. Newton-Metre reads it, calculates every cost line, finds similar parts
              from your history, and hands you the answer. Your company&apos;s brain — searchable in seconds.
            </p>
            <Link href="/login" className="inline-flex items-center px-9 py-4 bg-cyan-600 text-white text-[15px] font-semibold rounded-lg hover:bg-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
              Upload your first drawing →
            </Link>
            <p className="mt-5 text-[12px] text-slate-400" style={{ fontFamily: "var(--font-sans)" }}>No credit card · No setup · Results in 60 seconds</p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-200 py-12 bg-white">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="flex flex-col md:flex-row justify-between items-start gap-10 mb-10">
            <div>
              <div className="flex items-center gap-2.5 mb-3">
                <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={36} height={36} className="rounded-xl" />
                <span style={{ fontFamily: "var(--font-heading)" }} className="text-[20px] text-cyan-600">Newton-Metre</span>
              </div>
              <p className="text-[13px] text-slate-500 max-w-xs leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>
                Should-cost intelligence + similarity search. Your company&apos;s brain for manufactured parts.
              </p>
            </div>
            <div className="flex gap-16">
              <div>
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Product</p>
                <div className="space-y-2">
                  {[["How it works", "#how-it-works"], ["Pricing", "#pricing"]].map(([l, h]) => (
                    <a key={l} href={h} className="block text-[13px] text-slate-500 hover:text-slate-800 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.2em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Account</p>
                <div className="space-y-2">
                  <Link href="/login" className="block text-[13px] text-slate-500 hover:text-slate-800 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Sign in</Link>
                  <Link href="/login" className="block text-[13px] text-slate-500 hover:text-slate-800 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Upload a drawing</Link>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-slate-200 pt-6 text-[10px] text-slate-400 uppercase tracking-[0.15em]" style={{ fontFamily: "var(--font-mono)" }}>
            © 2026 Newton-Metre. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
