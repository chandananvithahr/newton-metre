import Link from "next/link";
import Image from "next/image";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#F8F8F6] text-slate-900">

      {/* ── Nav ── */}
      <nav className="bg-[#F8F8F6]/90 backdrop-blur-md flex justify-between items-center w-full px-6 lg:px-10 h-16 lg:h-20 fixed top-0 z-50 border-b border-slate-200/80">
        <div className="flex items-center gap-10">
          <Link href="/" className="flex items-center gap-2.5">
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={36} height={36} className="rounded-xl" />
            <span style={{ fontFamily: "var(--font-heading)" }} className="text-[20px] text-cyan-600 tracking-tight">Newton-Metre</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            {[["How it works", "#how-it-works"], ["Pricing", "#pricing"]].map(([l, h]) => (
              <a key={l} href={h} className="text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login" className="hidden sm:block text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2 bg-slate-900 text-white text-[13px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200 hover:shadow-lg" style={{ fontFamily: "var(--font-sans)" }}>
            Get started
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ════════════════════════════════════════════════════════════
            HERO
            ════════════════════════════════════════════════════════════ */}
        <section className="py-28 lg:py-40 flex flex-col items-center px-6">
          <div className="max-w-3xl w-full text-center">
            <p className="mb-8 text-[11px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
              Should-cost intelligence + Company memory
            </p>

            <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(40px,7vw,80px)] tracking-[-0.03em] leading-[1.05] text-slate-900 mb-8">
              Know what it costs.<br />
              <span className="text-cyan-600 italic">Find what you&apos;ve made.</span>
            </h1>

            <p className="max-w-lg mx-auto text-[18px] text-slate-400 leading-[1.7] mb-12" style={{ fontFamily: "var(--font-sans)" }}>
              Upload a drawing. Get a line-by-line should-cost breakdown.
              Search thousands of drawings, POs, and contracts to find similar parts — instantly.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-slate-900 text-white text-[15px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200 hover:shadow-lg hover:scale-[1.02]" style={{ fontFamily: "var(--font-sans)" }}>
                Upload a drawing — free
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 text-slate-400 text-[15px] font-medium hover:text-slate-600 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                See a live estimate ↓
              </a>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            TRUST BAR — credibility signal below hero
            ════════════════════════════════════════════════════════════ */}
        <section className="py-10 border-y border-slate-200/60">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <p className="text-[11px] text-slate-300 uppercase tracking-[0.25em] mb-6" style={{ fontFamily: "var(--font-mono)" }}>
              Built for Indian manufacturing procurement
            </p>
            <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-4">
              {[
                { val: "18", label: "Machining processes" },
                { val: "40+", label: "Surface treatments" },
                { val: "164", label: "Physics tests passing" },
                { val: "4", label: "Part types supported" },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-2">
                  <span className="text-[15px] font-bold text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{item.val}</span>
                  <span className="text-[11px] text-slate-300" style={{ fontFamily: "var(--font-sans)" }}>{item.label}</span>
                </div>
              ))}
            </div>
            <div className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
              {["Defense", "Aerospace", "Automobile"].map((industry) => (
                <span key={industry} className="text-[10px] text-slate-400 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>
                  {industry}
                </span>
              ))}
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            TWO SUPERPOWERS — side by side
            ════════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <div className="grid lg:grid-cols-2 gap-6 lg:gap-8">

              {/* ── Superpower 1: Should-Cost ── */}
              <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8 lg:p-10">
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.25em] font-medium mb-5" style={{ fontFamily: "var(--font-mono)" }}>
                  Should-Cost Breakdown
                </p>

                <h3 style={{ fontFamily: "var(--font-heading)" }} className="text-[28px] lg:text-[32px] tracking-[-0.02em] text-slate-900 leading-tight mb-4">
                  Every cost line.<br />Before any supplier quotes.
                </h3>

                <p className="text-[15px] text-slate-400 leading-[1.7] mb-8" style={{ fontFamily: "var(--font-sans)" }}>
                  Material, machining, finishing, overhead, margin — calculated from the drawing. Not a guess. A breakdown.
                </p>

                {/* Mini cost preview */}
                <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden">
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
                          <span className="text-[11px] text-slate-300" style={{ fontFamily: "var(--font-mono)" }}>{detail}</span>
                        </div>
                        <span className="text-[13px] font-semibold text-slate-700 tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>{cost}</span>
                      </div>
                    ))}
                  </div>
                  <div className="bg-slate-900 text-white px-5 py-3 flex items-center justify-between">
                    <span className="text-[13px] font-medium" style={{ fontFamily: "var(--font-sans)" }}>Should-cost / unit</span>
                    <span className="text-[18px] font-bold tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>₹695</span>
                  </div>
                </div>

                <div className="mt-6 flex items-center gap-6">
                  {[["±5–10%", "Accuracy"], ["<60s", "Result"], ["₹/unit", "Line by line"]].map(([val, label]) => (
                    <div key={label} className="flex items-center gap-2">
                      <span className="text-[13px] font-bold text-cyan-600" style={{ fontFamily: "var(--font-mono)" }}>{val}</span>
                      <span className="text-[11px] text-slate-300" style={{ fontFamily: "var(--font-sans)" }}>{label}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* ── Superpower 2: Similarity Search — Your Company's Brain ── */}
              <div className="bg-[#F7FBFA] border border-cyan-200/60 rounded-2xl p-8 lg:p-10">
                <p className="text-[10px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-5" style={{ fontFamily: "var(--font-mono)" }}>
                  Your Company&apos;s Brain
                </p>

                <h3 style={{ fontFamily: "var(--font-heading)" }} className="text-[28px] lg:text-[32px] tracking-[-0.02em] text-slate-900 leading-tight mb-4">
                  Thousands of drawings.<br />Searchable in seconds.
                </h3>

                <p className="text-[15px] text-slate-400 leading-[1.7] mb-8" style={{ fontFamily: "var(--font-sans)" }}>
                  Drawings, POs, contracts, QA reports, supplier records — buried across shared drives and inboxes. Newton-Metre turns them into one searchable brain.
                </p>

                {/* Mini similarity preview */}
                <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden">
                  <div className="px-5 py-2.5 border-b border-slate-100 flex items-center justify-between">
                    <span className="text-[10px] text-slate-300 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>Matches found</span>
                    <span className="text-[10px] text-cyan-600 font-medium" style={{ fontFamily: "var(--font-mono)" }}>3 results</span>
                  </div>
                  <div className="divide-y divide-slate-100">
                    {[
                      { name: "Bracket-A4521", dept: "Design · Rajesh K.", match: 92, cost: "₹1,180" },
                      { name: "Mount-B2290", dept: "Procurement · Priya S.", match: 78, cost: "₹1,340" },
                      { name: "Flange-C0087", dept: "Quality · Amit P.", match: 65, cost: "₹890" },
                    ].map((item) => {
                      const color = item.match >= 80 ? "text-emerald-600" : item.match >= 60 ? "text-amber-600" : "text-slate-400";
                      return (
                        <div key={item.name} className="px-5 py-3 flex items-center justify-between">
                          <div>
                            <p className="text-[13px] font-medium text-slate-700" style={{ fontFamily: "var(--font-sans)" }}>{item.name}</p>
                            <p className="text-[10px] text-slate-300 mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>{item.dept} · {item.cost}</p>
                          </div>
                          <span className={`text-[13px] font-bold tabular-nums ${color}`} style={{ fontFamily: "var(--font-mono)" }}>{item.match}%</span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Department tags */}
                <div className="mt-6 flex flex-wrap gap-2">
                  {["Design", "Procurement", "Sales", "Quality"].map((dept) => (
                    <span key={dept} className="text-[10px] px-3 py-1.5 bg-white border border-cyan-200/60 rounded-full text-cyan-700 uppercase tracking-[0.15em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
                      {dept}
                    </span>
                  ))}
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            EVERY DEPARTMENT — Similarity search expanded
            One line per department. Verb + outcome.
            ════════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="text-center mb-5 text-[11px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
              One brain. Every department.
            </p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] leading-tight mb-6">
              Stop reinventing what already exists.
            </h2>
            <p className="text-center max-w-xl mx-auto text-[16px] text-slate-400 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
              Your company has already designed, costed, and manufactured thousands of parts.
              Newton-Metre makes that history searchable — for everyone.
            </p>

            <div className="grid sm:grid-cols-2 gap-5">
              {[
                {
                  dept: "Design",
                  line: "Find if the part already exists. Skip three days of reinvention.",
                  detail: "Search every drawing your company has ever made. Reuse tested, approved designs instead of starting from scratch.",
                },
                {
                  dept: "Procurement",
                  line: "Find what you paid last time. Never negotiate from zero.",
                  detail: "Pull cost history for similar parts — material, supplier, price, quantity. Walk into negotiations with data.",
                },
                {
                  dept: "Quality",
                  line: "Find supplier rejection history. Avoid repeat failures.",
                  detail: "Trace similar parts back to tested designs. See which suppliers had first-article rejections. Spot patterns before they cost you.",
                },
                {
                  dept: "Sales",
                  line: "Find previous contracts. Quote with historical advantage.",
                  detail: "Pull pricing from past orders for similar parts. Quote faster, more accurately, with margins you can defend.",
                },
              ].map((item) => (
                <div key={item.dept} className="bg-white border border-slate-200/80 rounded-2xl p-8 hover:border-cyan-200 transition-colors">
                  <p className="text-[10px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-4" style={{ fontFamily: "var(--font-mono)" }}>
                    {item.dept}
                  </p>
                  <p className="text-[17px] font-semibold text-slate-900 leading-snug mb-3" style={{ fontFamily: "var(--font-sans)" }}>
                    {item.line}
                  </p>
                  <p className="text-[14px] text-slate-400 leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>
                    {item.detail}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            LIVE DEMO — Interactive cost breakdown
            ════════════════════════════════════════════════════════════ */}
        <section id="demo" className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-3xl mx-auto px-6">
            <p className="text-center mb-5 text-[11px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Live example</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-4">
              This is the answer.
            </h2>
            <p className="text-center max-w-md mx-auto text-[15px] text-slate-400 leading-[1.7] mb-12" style={{ fontFamily: "var(--font-sans)" }}>
              Every cost line. Every assumption visible. Click any value to copy.
            </p>
            <CostBreakdownTable />
            <p className="text-center mt-10">
              <Link href="/login" className="text-[14px] font-medium text-cyan-600 hover:text-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                Get your own breakdown →
              </Link>
            </p>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            HOW IT WORKS — 3 steps
            ════════════════════════════════════════════════════════════ */}
        <section id="how-it-works" className="py-24 lg:py-32">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="text-center mb-5 text-[11px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>How it works</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-16">
              Upload. Newton-Metre does the rest.
            </h2>

            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  n: "01",
                  title: "You upload a drawing",
                  desc: "PDF, DXF, DWG, STEP, or a photo. Newton-Metre extracts dimensions, material, tolerances, and processes.",
                },
                {
                  n: "02",
                  title: "Newton-Metre does the work",
                  desc: "Calculates every cost line. Searches your history for similar parts. Validates with AI cross-check.",
                },
                {
                  n: "03",
                  title: "You negotiate with data",
                  desc: "Line-by-line breakdown. Similar parts from your past. The supplier can't hide margins.",
                },
              ].map((s) => (
                <div key={s.n} className="relative bg-white border border-slate-200/80 rounded-2xl p-8">
                  <span className="text-[48px] font-bold text-slate-100 absolute top-6 right-8 select-none" style={{ fontFamily: "var(--font-mono)" }}>{s.n}</span>
                  <h3 className="text-[16px] font-semibold text-slate-900 mb-3 relative" style={{ fontFamily: "var(--font-sans)" }}>{s.title}</h3>
                  <p className="text-[14px] text-slate-400 leading-[1.7] relative" style={{ fontFamily: "var(--font-sans)" }}>{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            BEFORE / AFTER
            ════════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-16">
              Your team is negotiating blind.
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Before */}
              <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8">
                <p className="text-[10px] text-red-400 uppercase tracking-[0.25em] font-medium mb-8" style={{ fontFamily: "var(--font-mono)" }}>Without Newton-Metre</p>
                <div className="space-y-5">
                  {[
                    "Call 3 suppliers. Wait 2 weeks.",
                    "Negotiate on gut feel — no cost data.",
                    "\"We made something like this once...\" — nobody can find it.",
                    "Engineer retires. Knowledge walks out the door.",
                  ].map((text) => (
                    <div key={text} className="flex items-start gap-3">
                      <span className="w-1 h-1 rounded-full bg-red-300 mt-[9px] shrink-0" />
                      <span className="text-[14px] text-slate-500 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* After */}
              <div className="bg-[#F7FBFA] border border-cyan-200/60 rounded-2xl p-8">
                <p className="text-[10px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-8" style={{ fontFamily: "var(--font-mono)" }}>With Newton-Metre</p>
                <div className="space-y-5">
                  {[
                    "Upload a drawing. Answer in 60 seconds.",
                    "Every cost line: material, machining, finishing, margin.",
                    "Newton-Metre finds similar parts from your entire history.",
                    "Knowledge stays in the system. Searchable forever.",
                  ].map((text) => (
                    <div key={text} className="flex items-start gap-3">
                      <span className="w-1 h-1 rounded-full bg-cyan-500 mt-[9px] shrink-0" />
                      <span className="text-[14px] text-slate-600 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            STATS
            ════════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32">
          <div className="max-w-4xl mx-auto px-6 lg:px-10 text-center">
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] leading-tight mb-6">
              Every overpaid part compounds.
            </h2>
            <p className="max-w-lg mx-auto text-[16px] text-slate-400 leading-[1.7] mb-14" style={{ fontFamily: "var(--font-sans)" }}>
              200 parts a month. Overpaying 20% on half of them. That&apos;s lakhs per year — not because your team is bad, because they don&apos;t have the data.
            </p>

            <div className="grid grid-cols-3 gap-4 max-w-xl mx-auto mb-8">
              {[
                { val: "164+", label: "Estimates run" },
                { val: "±5–10%", label: "Accuracy" },
                { val: "<60s", label: "Time to result" },
              ].map((s) => (
                <div key={s.label} className="bg-white border border-slate-200/80 rounded-xl p-6">
                  <div className="text-[22px] font-bold text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>{s.val}</div>
                  <div className="text-[11px] text-slate-300 uppercase tracking-[0.15em]" style={{ fontFamily: "var(--font-mono)" }}>{s.label}</div>
                </div>
              ))}
            </div>

            <div className="bg-white border border-slate-200/80 rounded-xl p-6 max-w-sm mx-auto">
              <p className="text-[14px] text-slate-600 mb-1" style={{ fontFamily: "var(--font-sans)" }}>EN8 Steel Shaft — Ø50×100mm</p>
              <p className="text-[13px] text-slate-400 mb-2" style={{ fontFamily: "var(--font-sans)" }}>Supplier quoted ₹2,400 — should-cost ₹1,400</p>
              <span className="text-[15px] font-bold text-emerald-600" style={{ fontFamily: "var(--font-mono)" }}>42% savings identified</span>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            PRICING
            ════════════════════════════════════════════════════════════ */}
        <section id="pricing" className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-4xl mx-auto px-6 lg:px-10 text-center">
            <p className="mb-5 text-[11px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Pricing</p>
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-4">
              Start free. Pay when it pays for itself.
            </h2>
            <p className="max-w-md mx-auto text-[15px] text-slate-400 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
              One estimate that catches a 20% overpayment pays for a year of Pro.
            </p>

            <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left">
              {/* Free */}
              <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8">
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Free</p>
                <p className="text-[36px] text-slate-900 tracking-tight mb-1" style={{ fontFamily: "var(--font-heading)" }}>₹0</p>
                <p className="text-[13px] text-slate-300 mb-8" style={{ fontFamily: "var(--font-sans)" }}>No card required</p>
                <div className="space-y-3 mb-8">
                  {["10 estimates / month", "Should-cost breakdown", "Similarity search", "PDF & image uploads", "All part types"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5">
                      <svg className="w-3.5 h-3.5 text-cyan-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                      <span className="text-[13px] text-slate-500" style={{ fontFamily: "var(--font-sans)" }}>{f}</span>
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center bg-slate-900 text-white px-6 py-3.5 rounded-full font-medium hover:bg-slate-800 transition-colors text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>
                  Upload a drawing
                </Link>
              </div>

              {/* Pro */}
              <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8 relative">
                <div className="absolute top-4 right-4 bg-amber-50 text-amber-600 text-[9px] px-2.5 py-1 rounded-full uppercase tracking-[0.2em] border border-amber-200 font-medium" style={{ fontFamily: "var(--font-mono)" }}>Coming soon</div>
                <p className="text-[10px] text-slate-400 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Pro</p>
                <p className="text-[36px] text-slate-900 tracking-tight mb-1" style={{ fontFamily: "var(--font-heading)" }}>₹4,999</p>
                <p className="text-[13px] text-slate-300 mb-8" style={{ fontFamily: "var(--font-sans)" }}>per user / month</p>
                <div className="space-y-3 mb-8">
                  {["Unlimited estimates", "Persistent part library", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5">
                      <svg className="w-3.5 h-3.5 text-cyan-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                      <span className="text-[13px] text-slate-500" style={{ fontFamily: "var(--font-sans)" }}>{f}</span>
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-slate-200 text-slate-400 px-6 py-3.5 rounded-lg font-medium cursor-not-allowed text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════════
            FINAL CTA
            ════════════════════════════════════════════════════════════ */}
        <section className="py-28 lg:py-40">
          <div className="max-w-3xl mx-auto px-6 text-center">
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(36px,6vw,64px)] text-slate-900 tracking-[-0.03em] leading-[1.05] mb-8">
              Newton-Metre does the work.<br />
              <span className="text-cyan-600 italic">You negotiate.</span>
            </h2>
            <p className="max-w-md mx-auto text-[17px] text-slate-400 leading-[1.7] mb-12" style={{ fontFamily: "var(--font-sans)" }}>
              Upload a drawing. Get a should-cost breakdown + similar parts from your history. Your company&apos;s brain — searchable in seconds.
            </p>
            <Link href="/login" className="inline-flex px-9 py-4 bg-slate-900 text-white text-[15px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200 hover:shadow-lg" style={{ fontFamily: "var(--font-sans)" }}>
              Upload your first drawing →
            </Link>
            <p className="mt-6 text-[12px] text-slate-300" style={{ fontFamily: "var(--font-mono)" }}>No credit card · No setup · Results in 60 seconds</p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-200/80 py-12 bg-white">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="flex flex-col md:flex-row justify-between items-start gap-10 mb-10">
            <div>
              <div className="flex items-center gap-2.5 mb-3">
                <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={32} height={32} className="rounded-xl" />
                <span style={{ fontFamily: "var(--font-heading)" }} className="text-[18px] text-cyan-600">Newton-Metre</span>
              </div>
              <p className="text-[13px] text-slate-400 max-w-xs leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>
                Should-cost intelligence + company memory for manufactured parts.
              </p>
            </div>
            <div className="flex gap-16">
              <div>
                <p className="text-[10px] text-slate-300 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Product</p>
                <div className="space-y-2">
                  {[["How it works", "#how-it-works"], ["Pricing", "#pricing"]].map(([l, h]) => (
                    <a key={l} href={h} className="block text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] text-slate-300 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Account</p>
                <div className="space-y-2">
                  <Link href="/login" className="block text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Sign in</Link>
                  <Link href="/login" className="block text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Get started</Link>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-slate-100 pt-6 text-[10px] text-slate-300 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>
            © 2026 Newton-Metre
          </div>
        </div>
      </footer>
    </div>
  );
}
