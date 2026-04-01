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
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={44} height={44} className="rounded-xl" />
            <span className="font-heading text-2xl text-cyan-600 tracking-tight">Newton-Metre</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            {[["How it works", "#how-it-works"], ["Should-Cost", "#should-cost"], ["Similarity", "#similarity"], ["Pricing", "#pricing"]].map(([l, h]) => (
              <a key={l} href={h} className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">{l}</a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-5">
          <Link href="/login" className="hidden sm:block font-sans text-sm text-slate-500 hover:text-slate-800 transition-colors">
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2 bg-cyan-600 text-white font-sans text-sm font-semibold rounded-md hover:bg-cyan-700 transition-colors">
            Upload a drawing
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ── Hero ── */}
        <section className="relative min-h-[90vh] flex flex-col items-center justify-center px-6 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: "radial-gradient(circle, #94A3B8 1px, transparent 1px)", backgroundSize: "32px 32px" }} />

          <div className="max-w-5xl w-full text-center space-y-7 relative z-10">

            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 font-mono text-[11px] text-cyan-700 uppercase tracking-widest">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
              Built for Indian manufacturing
            </div>

            <h1 className="font-heading text-[clamp(40px,7vw,80px)] tracking-tight leading-[1.04] text-slate-900">
              Newton-Metre reads the drawing.<br />
              <span className="text-cyan-600 italic">Hands you the cost.</span>
            </h1>

            <p className="max-w-2xl mx-auto font-sans text-lg text-slate-500 leading-relaxed">
              Newton-Metre extracts dimensions, identifies every process, calculates material + machining + finishing costs,
              and finds similar parts your company has already made. Line by line. In 60 seconds.
              You just upload and negotiate.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-cyan-600 text-white font-sans text-base font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                Upload a drawing
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 bg-white border border-slate-200 text-slate-700 font-sans text-base font-semibold rounded-md hover:border-cyan-300 transition-colors">
                See a sample estimate ↓
              </a>
            </div>

            {/* Trust badges */}
            <div className="flex items-center justify-center gap-6 pt-4 text-slate-400">
              <span className="font-mono text-[10px] uppercase tracking-widest">Physics-based</span>
              <span className="w-1 h-1 rounded-full bg-slate-300" />
              <span className="font-mono text-[10px] uppercase tracking-widest">±5–10% accuracy</span>
              <span className="w-1 h-1 rounded-full bg-slate-300" />
              <span className="font-mono text-[10px] uppercase tracking-widest">No credit card</span>
            </div>
          </div>
        </section>

        {/* ── Before / After ── The Shift ── */}
        <section className="py-20 bg-white border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3 text-center">The problem</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4 text-center">
              Your team is negotiating blind.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-2xl mx-auto text-center leading-relaxed">
              A supplier sends a quote for Rs 2,400 per part. Is that fair? Today, the answer takes weeks. Or gut feel. Or hope.
            </p>

            <div className="grid md:grid-cols-2 gap-6 lg:gap-8">
              {/* Before */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-8">
                <p className="font-mono text-[10px] text-red-500 uppercase tracking-widest mb-6">Without Newton-Metre</p>
                <div className="space-y-5">
                  {[
                    { icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z", text: "Call 3 suppliers, wait 2 weeks for counter-quotes" },
                    { icon: "M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z", text: "Negotiate on gut feel — no cost data to back it up" },
                    { icon: "M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636", text: "No way to challenge a quote line by line" },
                    { icon: "M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0", text: "Tribal knowledge — leaves when people leave" },
                  ].map((item) => (
                    <div key={item.text} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-red-400 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
                      </svg>
                      <span className="font-sans text-sm text-slate-600 leading-relaxed">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* After */}
              <div className="bg-cyan-50/50 border border-cyan-200 rounded-xl p-8">
                <p className="font-mono text-[10px] text-cyan-600 uppercase tracking-widest mb-6">With Newton-Metre</p>
                <div className="space-y-5">
                  {[
                    { icon: "M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z", text: "Newton-Metre reads the drawing and delivers the answer in 60 seconds" },
                    { icon: "M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5", text: "Newton-Metre breaks down every cost: material, machining, finishing, overhead, margin" },
                    { icon: "M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5", text: "Newton-Metre finds similar parts your company has already made — instantly" },
                    { icon: "M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z", text: "You negotiate with data. Suppliers can't hide margins." },
                  ].map((item) => (
                    <div key={item.text} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-cyan-600 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
                      </svg>
                      <span className="font-sans text-sm text-slate-700 leading-relaxed">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Live Demo ── */}
        <section id="demo" className="py-20 px-6">
          <div className="max-w-3xl mx-auto">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3 text-center">Live example</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-3 text-center">
              This is what the answer looks like.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-10 text-center max-w-xl mx-auto leading-relaxed">
              Every cost line. Every assumption. Click any value to copy it straight into your negotiation.
            </p>
            <CostBreakdownTable />
            <p className="text-center mt-6">
              <Link href="/login" className="font-sans text-sm font-semibold text-cyan-600 hover:text-cyan-700 transition-colors">
                Get your own breakdown →
              </Link>
            </p>
          </div>
        </section>

        {/* ── Superpower 1: Should-Cost ── */}
        <section id="should-cost" className="py-20 bg-slate-50 border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
              <div>
                <p className="font-mono text-[10px] text-cyan-600 uppercase tracking-widest mb-3">For procurement</p>
                <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight leading-tight mb-4">
                  The cost analyst<br />
                  <span className="text-cyan-600 italic">your team doesn&apos;t have.</span>
                </h2>
                <p className="font-sans text-base text-slate-500 leading-relaxed mb-6">
                  Newton-Metre reads the drawing. Extracts every dimension. Identifies the manufacturing
                  processes. Calculates material cost, cycle times, surface treatment, heat treatment,
                  overhead, and margin. Hands you a line-by-line breakdown. In seconds.
                </p>
                <p className="font-sans text-base text-slate-500 leading-relaxed mb-8">
                  The supplier quotes Rs 2,400. Newton-Metre says Rs 1,400.
                  You walk in with the number already worked out. Zero spreadsheets. Zero guesswork.
                </p>
                <Link href="/login" className="inline-flex items-center gap-2 px-6 py-3 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                  Upload a drawing
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                  </svg>
                </Link>
              </div>

              <div className="space-y-4">
                <div className="bg-white border border-slate-200 rounded-xl p-6">
                  <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-4">What it calculates</p>
                  <div className="space-y-3">
                    {[
                      { label: "Raw material cost", detail: "Weight × ₹/kg for 9+ materials" },
                      { label: "Machining time", detail: "MRR-based cycle time for 18 processes" },
                      { label: "Surface treatment", detail: "40+ treatments, area-based pricing" },
                      { label: "Heat treatment", detail: "15 processes, weight-based pricing" },
                      { label: "Setup + tooling", detail: "Amortised over your order quantity" },
                      { label: "Overhead + margin", detail: "15% overhead, 20% standard margin" },
                    ].map((item) => (
                      <div key={item.label} className="flex items-center justify-between">
                        <span className="font-sans text-sm font-medium text-slate-700">{item.label}</span>
                        <span className="font-mono text-xs text-slate-400">{item.detail}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { val: "±5–10%", label: "Accuracy" },
                    { val: "<60s", label: "Time to result" },
                    { val: "₹/unit", label: "Line by line" },
                  ].map((s) => (
                    <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-4 text-center">
                      <div className="font-mono text-lg font-bold text-cyan-600 mb-0.5">{s.val}</div>
                      <div className="font-sans text-[11px] text-slate-400">{s.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Superpower 2: Similarity Search — Company Brain ── */}
        <section id="similarity" className="py-24 bg-gradient-to-b from-[#F0FDFA] to-[#F8F8F6]">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">

            {/* Section header — big, bold, center */}
            <div className="text-center mb-16">
              <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">Your company&apos;s brain</p>
              <h2 className="font-heading text-[clamp(32px,5vw,56px)] text-slate-900 tracking-tight leading-tight mb-4">
                Thousands of drawings.<br />
                <span className="text-cyan-600 italic">Searchable in seconds.</span>
              </h2>
              <p className="max-w-2xl mx-auto font-sans text-lg text-slate-500 leading-relaxed">
                Every drawing your company has ever made — designed, costed, manufactured, delivered — sitting in shared drives, inboxes, and filing cabinets. Newton-Metre turns that into a searchable brain that every department can use.
              </p>
            </div>

            {/* The story */}
            <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-start mb-16">
              {/* Left: the problem story */}
              <div>
                <div className="bg-white border border-slate-200 rounded-xl p-8 mb-6">
                  <p className="font-mono text-[10px] text-red-500 uppercase tracking-widest mb-4">The problem no one talks about</p>
                  <p className="font-sans text-base text-slate-600 leading-relaxed mb-4">
                    A designer sits down to design a mounting bracket. Three days later, the design is done.
                  </p>
                  <p className="font-sans text-base text-slate-600 leading-relaxed mb-4">
                    What she didn&apos;t know: a colleague designed a nearly identical bracket 18 months ago.
                    It was tested, approved, manufactured, and delivered. The drawing is buried on a shared drive.
                    Nobody told her. She didn&apos;t know to look.
                  </p>
                  <p className="font-sans text-base text-slate-700 leading-relaxed font-medium">
                    This happens every week in every manufacturing company. The senior engineer who remembered everything retired last year. The knowledge walked out the door with him.
                  </p>
                </div>

                <div className="bg-cyan-50 border border-cyan-200 rounded-xl p-8">
                  <p className="font-mono text-[10px] text-cyan-600 uppercase tracking-widest mb-4">What Newton-Metre does</p>
                  <p className="font-sans text-base text-slate-700 leading-relaxed">
                    Upload any drawing. Newton-Metre searches your entire part library — thousands of drawings —
                    and surfaces matches with cost history, supplier data, and who designed it.
                    <span className="font-semibold"> No more reinventing. No more lost knowledge. No more &ldquo;has someone already done this?&rdquo;</span>
                  </p>
                </div>
              </div>

              {/* Right: mock similarity UI */}
              <div>
                <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                  <div className="bg-slate-50 px-5 py-3 border-b border-slate-200 flex items-center justify-between">
                    <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest">Similarity results</p>
                    <span className="font-mono text-[10px] text-cyan-600">3 matches found</span>
                  </div>
                  <div className="p-5 space-y-3">
                    {[
                      { name: "Bracket-A4521.pdf", match: 92, person: "Rajesh K. · Design", date: "Oct 2024", cost: "₹1,180/unit" },
                      { name: "Mount-B2290.pdf", match: 78, person: "Priya S. · Procurement", date: "Jul 2024", cost: "₹1,340/unit" },
                      { name: "Flange-C0087.pdf", match: 65, person: "Amit P. · Quality", date: "Mar 2024", cost: "₹890/unit" },
                    ].map((item) => {
                      const barColor = item.match >= 80 ? "bg-emerald-500" : item.match >= 60 ? "bg-amber-500" : "bg-slate-300";
                      return (
                        <div key={item.name} className="bg-slate-50 rounded-lg px-4 py-3">
                          <div className="flex items-center justify-between mb-1">
                            <p className="font-sans text-sm font-medium text-slate-800">{item.name}</p>
                            <div className="flex items-center gap-2">
                              <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                                <div className={`h-full ${barColor} rounded-full`} style={{ width: `${item.match}%` }} />
                              </div>
                              <span className="font-mono text-xs font-semibold text-slate-700 w-10 text-right" style={{ fontVariantNumeric: "tabular-nums" }}>{item.match}%</span>
                            </div>
                          </div>
                          <p className="font-mono text-[10px] text-slate-400">{item.person} · {item.date} · {item.cost}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-3 mt-4">
                  {[
                    { val: "1000s", label: "Drawings searchable" },
                    { val: "<5s", label: "Search time" },
                    { val: "92%", label: "Match accuracy" },
                  ].map((s) => (
                    <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-4 text-center">
                      <div className="font-mono text-lg font-bold text-cyan-600 mb-0.5">{s.val}</div>
                      <div className="font-sans text-[11px] text-slate-400">{s.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Department grid — who uses it */}
            <div className="mb-12">
              <h3 className="font-heading text-2xl text-slate-900 tracking-tight text-center mb-8">
                Every department. One brain.
              </h3>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {[
                  {
                    dept: "Design",
                    icon: "M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42",
                    headline: "Stop reinventing parts",
                    desc: "Find existing designs before starting from scratch. Reuse what's tested and approved.",
                  },
                  {
                    dept: "Procurement",
                    icon: "M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z",
                    headline: "Know what you paid last time",
                    desc: "Find historical costs for similar parts instantly. Never negotiate from zero again.",
                  },
                  {
                    dept: "Sales & Marketing",
                    icon: "M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z",
                    headline: "Quote faster, win more",
                    desc: "Pull cost data from similar past parts to build accurate quotes in minutes, not days.",
                  },
                  {
                    dept: "Quality",
                    icon: "M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z",
                    headline: "Trace back to what worked",
                    desc: "Find similar approved parts. Trace quality history. Avoid repeating past failures.",
                  },
                ].map((d) => (
                  <div key={d.dept} className="bg-white border border-slate-200 rounded-xl p-6 hover:border-cyan-300 transition-colors">
                    <div className="flex items-center gap-2.5 mb-3">
                      <div className="w-8 h-8 bg-cyan-50 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d={d.icon} />
                        </svg>
                      </div>
                      <span className="font-mono text-[10px] text-cyan-600 uppercase tracking-widest">{d.dept}</span>
                    </div>
                    <h4 className="font-sans text-sm font-semibold text-slate-800 mb-2">{d.headline}</h4>
                    <p className="font-sans text-sm text-slate-500 leading-relaxed">{d.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="text-center">
              <Link href="/login" className="inline-flex items-center gap-2 px-8 py-3.5 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                Try similarity search free
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
              </Link>
            </div>
          </div>
        </section>

        {/* ── How it works ── */}
        <section id="how-it-works" className="py-20 bg-white border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3 text-center">How it works</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4 text-center">
              Upload. Wait 60 seconds. Negotiate.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-2xl mx-auto text-center leading-relaxed">
              No configuration. No learning curve. No prompting. The tool reads the drawing and does the math.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  n: "01",
                  title: "Upload your drawing",
                  desc: "Drop in a PDF, DXF, DWG, STEP, or even a photo. Newton-Metre extracts dimensions, material, tolerances, and process requirements directly from the file.",
                  mono: "PDF · DXF · DWG · STEP · PNG",
                },
                {
                  n: "02",
                  title: "Newton-Metre does the work",
                  desc: "Newton-Metre calculates material cost, machining time, surface treatment, heat treatment, tooling, setup, overhead, and margin. Finds similar parts your company has already made. Validates with AI cross-check.",
                  mono: "18 processes · 40+ treatments · similarity search",
                },
                {
                  n: "03",
                  title: "You negotiate with data",
                  desc: "Newton-Metre hands you a line-by-line breakdown. Copy any value. Walk into the supplier meeting already knowing what the part should cost. Zero spreadsheets.",
                  mono: "Line-by-line · Copy to clipboard",
                },
              ].map((s) => (
                <div key={s.n} className="bg-[#F8F8F6] border border-slate-200 rounded-xl p-8 hover:border-cyan-300 transition-colors">
                  <div className="font-mono text-3xl text-slate-200 mb-4">{s.n}</div>
                  <h3 className="font-sans text-lg font-semibold text-slate-800 mb-3">{s.title}</h3>
                  <p className="font-sans text-sm text-slate-500 leading-relaxed mb-4">{s.desc}</p>
                  <span className="font-mono text-[10px] px-2.5 py-1 bg-white border border-slate-200 rounded-full text-slate-500 uppercase tracking-wide">{s.mono}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Technical Capabilities ── */}
        <section className="py-20">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3 text-center">Under the hood</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4 text-center">
              Physics, not guesswork.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-2xl mx-auto text-center leading-relaxed">
              Built on real manufacturing data — Sandvik cutting parameters, Machinery&apos;s Handbook formulas,
              and Indian job-shop rates from 15 cities.
            </p>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {[
                { title: "Calculates cycle times", desc: "Newton-Metre computes MRR-based machining time for turning, milling, drilling — from real Sandvik cutting parameters." },
                { title: "Knows Indian rates", desc: "Newton-Metre uses Indian job-shop rates: CNC ₹800/hr, milling ₹1,000/hr, labour ₹250/hr. 15-city cost index." },
                { title: "Costs 40+ treatments", desc: "Newton-Metre prices electroplating, anodizing, PVD/CVD, paint, powder coat — area-based with mil-spec references." },
                { title: "Validates with AI", desc: "Newton-Metre runs physics + AI in parallel. Discrepancies >7% trigger automatic line-by-line arbitration." },
                { title: "Reads any format", desc: "Newton-Metre extracts dimensions from PDF, DXF, DWG, STEP, PNG, JPG — no manual input, no templates." },
                { title: "Remembers every part", desc: "Newton-Metre searches thousands of drawings to find similar parts — your company's brain, searchable in seconds." },
              ].map((f) => (
                <div key={f.title} className="bg-white border border-slate-200 rounded-xl p-6 hover:border-cyan-300 transition-colors">
                  <h3 className="font-sans text-sm font-semibold text-slate-800 mb-2">{f.title}</h3>
                  <p className="font-sans text-sm text-slate-500 leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Social proof / stats ── */}
        <section className="py-20 bg-slate-50 border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight leading-tight mb-4">
                  Every overpaid part<br /> compounds.
                </h2>
                <p className="font-sans text-base text-slate-500 leading-relaxed mb-4">
                  200 parts a month. If you&apos;re overpaying 20% on half of them — that&apos;s lakhs per year walking
                  out the door. Not because your team is bad at their job, but because they don&apos;t have the data.
                </p>
                <p className="font-sans text-base text-slate-500 leading-relaxed mb-8">
                  Newton-Metre does the homework. Reads the drawing. Calculates every cost line. Finds similar parts
                  from your history. Hands you the answer. Your team just negotiates.
                </p>
                <div className="flex flex-wrap gap-4">
                  <Link href="/login" className="px-6 py-3 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                    Upload a drawing
                  </Link>
                  <a href="#demo" className="px-6 py-3 bg-white border border-slate-200 text-slate-700 font-sans font-semibold rounded-md hover:border-cyan-300 transition-colors">
                    See the math
                  </a>
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { val: "164+", label: "Estimates run" },
                    { val: "±5–10%", label: "Accuracy" },
                    { val: "<60s", label: "Time to result" },
                  ].map((s) => (
                    <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-5 text-center">
                      <div className="font-mono text-xl font-bold text-cyan-600 mb-1">{s.val}</div>
                      <div className="font-sans text-xs text-slate-500">{s.label}</div>
                    </div>
                  ))}
                </div>

                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-3">Live benchmark</p>
                  <p className="font-sans text-sm font-semibold text-slate-800 mb-1">EN8 Steel Shaft — Ø50×100mm</p>
                  <div className="flex items-center justify-between">
                    <span className="font-sans text-sm text-slate-500">Supplier quoted ₹2,400 — should-cost: ₹1,400</span>
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-emerald-600">42% savings found</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing" className="py-20">
          <div className="max-w-4xl mx-auto px-6 lg:px-10 text-center">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">Pricing</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-3">
              Start free. Pay when it pays for itself.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-xl mx-auto leading-relaxed">
              Newton-Metre does the work for free. One estimate that catches a 20% overpayment pays for a year of Pro.
            </p>

            <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left">
              <div className="bg-white border border-slate-200 rounded-xl p-8">
                <p className="font-mono text-[11px] text-slate-400 uppercase tracking-widest mb-2">Free</p>
                <p className="font-mono text-4xl text-slate-900 mb-1">₹0</p>
                <p className="font-sans text-sm text-slate-400 mb-6">Forever free, no card required</p>
                <div className="space-y-2.5 mb-6">
                  {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Line-by-line breakdown", "Similarity search"].map((f) => (
                    <div key={f} className="flex items-center gap-2 font-sans text-sm text-slate-600">
                      <span className="text-cyan-500">✓</span> {f}
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center bg-cyan-600 text-white px-6 py-3 rounded-md font-sans font-semibold hover:bg-cyan-700 transition-colors">
                  Upload a drawing
                </Link>
              </div>

              <div className="bg-white border border-cyan-200 rounded-xl p-8 relative">
                <div className="absolute top-4 right-4 bg-amber-50 text-amber-600 font-mono text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider border border-amber-200">Coming soon</div>
                <p className="font-mono text-[11px] text-slate-400 uppercase tracking-widest mb-2">Pro</p>
                <p className="font-mono text-4xl text-slate-900 mb-1">₹4,999</p>
                <p className="font-sans text-sm text-slate-400 mb-6">per user / month</p>
                <div className="space-y-2.5 mb-6">
                  {["Unlimited estimates", "PCB + cable assembly", "Persistent part library", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2 font-sans text-sm text-slate-600">
                      <span className="text-cyan-500">✓</span> {f}
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-slate-100 text-slate-400 px-6 py-3 rounded-md font-sans font-semibold cursor-not-allowed">
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="py-20 bg-slate-50 border-t border-slate-200">
          <div className="max-w-3xl mx-auto px-6 lg:px-10 text-center">
            <h2 className="font-heading text-[clamp(32px,5vw,56px)] text-slate-900 tracking-tight leading-tight mb-4">
              Newton-Metre does the work.<br />
              <span className="text-cyan-600 italic">You negotiate.</span>
            </h2>
            <p className="font-sans text-lg text-slate-500 leading-relaxed mb-8">
              Upload a drawing. Newton-Metre reads it, calculates every cost line, finds similar parts
              from your history, and hands you the answer. Your company&apos;s brain — searchable in seconds.
            </p>
            <Link href="/login" className="inline-flex items-center justify-center px-8 py-4 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
              Upload your first drawing →
            </Link>
            <p className="mt-4 font-sans text-sm text-slate-400">No credit card · No setup · Results in 60 seconds</p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-200 py-12 bg-white">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2.5 mb-3">
                <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={40} height={40} className="rounded-xl" />
                <span className="font-heading text-xl text-cyan-600">Newton-Metre</span>
              </div>
              <p className="font-sans text-sm text-slate-500 max-w-xs leading-relaxed">
                Newton-Metre reads the drawing, calculates every cost line, and remembers every part your company has ever made. Your company&apos;s brain.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-x-12 gap-y-2">
              <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-2 col-span-2">Product</p>
              {[["How it works", "#how-it-works"], ["Should-Cost", "#should-cost"], ["Similarity", "#similarity"], ["Pricing", "#pricing"]].map(([l, h]) => (
                <a key={l} href={h} className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">{l}</a>
              ))}
              <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-2 col-span-2 mt-4">Account</p>
              <Link href="/login" className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">Sign in</Link>
              <Link href="/login" className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">Upload a drawing</Link>
            </div>
          </div>
          <div className="border-t border-slate-200 pt-6 font-mono text-[10px] text-slate-400 uppercase tracking-widest">
            © 2026 Newton-Metre. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
