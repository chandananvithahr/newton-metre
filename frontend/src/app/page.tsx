import Link from "next/link";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

// Primary blue from Stitch design
const PRIMARY = "#1E40AF";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 antialiased" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

      {/* ── Nav ── */}
      <nav className="bg-slate-50 flex justify-between items-center w-full px-6 py-3 h-16 fixed top-0 z-50 border-b border-slate-200 shadow-sm text-sm font-semibold tracking-tight">
        <div className="flex items-center gap-8">
          <Link href="/" className="text-2xl font-black tracking-tighter" style={{ color: PRIMARY }}>
            Costrich
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <a href="#how-it-works" className="text-slate-600 hover:text-blue-800 transition-colors">How it works</a>
            <a href="#features" className="text-slate-600 hover:text-blue-800 transition-colors">Features</a>
            <a href="#pricing" className="text-slate-600 hover:text-blue-800 transition-colors">Pricing</a>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login" className="hidden sm:block text-slate-500 hover:text-slate-800 text-sm font-medium transition-colors">
            Sign in
          </Link>
          <Link
            href="/login"
            className="text-white px-4 py-2 rounded font-bold hover:opacity-90 active:scale-95 transition-all text-xs uppercase tracking-wider"
            style={{ backgroundColor: PRIMARY }}
          >
            Launch Terminal
          </Link>
        </div>
      </nav>

      <main className="pt-16">

        {/* ── Hero ── */}
        <section
          className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden"
          style={{
            backgroundImage: "radial-gradient(circle, #e2e8f0 1px, transparent 1px)",
            backgroundSize: "32px 32px",
          }}
        >
          {/* Bottom fade */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-50 pointer-events-none" />

          <div className="max-w-6xl w-full text-center space-y-8 relative z-10">
            <div
              className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-white text-[10px] font-black uppercase tracking-[0.2em]"
              style={{ backgroundColor: PRIMARY }}
            >
              <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
              Live Intelligence Active
            </div>

            <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-slate-900 leading-none uppercase">
              Kill the markup.<br />
              <span style={{ color: PRIMARY }}>Own the margin.</span>
            </h1>

            <p className="max-w-2xl mx-auto text-xl text-slate-600 font-medium">
              AI-powered should-cost intelligence that strips away supplier hidden costs.
              Stop asking for a price — know it.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-4 pt-4">
              <Link
                href="/login"
                className="w-full md:w-auto px-8 py-4 text-white font-black text-lg uppercase tracking-tighter rounded-lg shadow-xl hover:-translate-y-0.5 transition-transform"
                style={{ backgroundColor: PRIMARY }}
              >
                Start your first estimate
              </Link>
              <a
                href="#demo"
                className="w-full md:w-auto px-8 py-4 bg-white border-2 border-slate-200 text-slate-900 font-black text-lg uppercase tracking-tighter rounded-lg hover:bg-slate-50 transition-colors"
              >
                View sample output
              </a>
            </div>

            {/* Dashboard preview */}
            <div id="demo" className="mt-16 relative mx-auto max-w-5xl rounded-t-xl border-x border-t border-slate-200 bg-white shadow-2xl overflow-hidden">
              <div className="h-8 bg-slate-100 border-b border-slate-200 flex items-center px-4 gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-400" />
                <div className="w-2.5 h-2.5 rounded-full bg-amber-400" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
                <div className="flex-1 mx-3 bg-white rounded px-3 py-0.5 text-xs text-slate-400 font-mono border border-slate-200">
                  costrich.ai/estimate/en8-shaft-100qty
                </div>
              </div>
              <div className="p-4 bg-slate-50">
                <div className="grid grid-cols-12 gap-4">
                  <div className="col-span-3 space-y-4">
                    <div className="h-32 bg-white border border-slate-200 rounded-lg p-4 flex flex-col justify-between">
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Should Cost</span>
                      <span className="text-2xl font-mono font-black" style={{ color: PRIMARY }}>₹695</span>
                      <div className="h-1 bg-slate-100 rounded overflow-hidden">
                        <div className="h-full w-3/4 rounded" style={{ backgroundColor: PRIMARY }} />
                      </div>
                    </div>
                    <div className="h-32 bg-white border border-slate-200 rounded-lg p-4 flex flex-col justify-between">
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Supplier Markup</span>
                      <span className="text-2xl font-mono font-black text-red-600">22.4%</span>
                      <div className="h-1 bg-slate-100 rounded overflow-hidden">
                        <div className="h-full bg-red-500 w-1/2 rounded" />
                      </div>
                    </div>
                  </div>
                  <div className="col-span-9">
                    <CostBreakdownTable />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── How it works ── */}
        <section id="how-it-works" className="py-24 bg-slate-50">
          <div className="max-w-6xl mx-auto px-6">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
              <div className="space-y-4">
                <h2 className="text-5xl font-black tracking-tighter uppercase italic" style={{ color: PRIMARY }}>
                  Zero Hidden Margins
                </h2>
                <div className="h-1 w-24 rounded" style={{ backgroundColor: PRIMARY }} />
              </div>
              <p className="max-w-md text-slate-600">
                The era of asymmetrical information is over. We provide physics-based evidence to dismantle supplier quotes.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-0 border border-slate-200 bg-white rounded-xl overflow-hidden">
              {[
                {
                  n: "01",
                  title: "Interrogation",
                  desc: "Upload your drawing, BOM, or historical quote. Our AI reads every technical specification to understand the component.",
                  points: ["PDF & image support", "Any CAD format"],
                },
                {
                  n: "02",
                  title: "Deep Dissection",
                  desc: "Physics-based math applied to manufacturing. Cycle times, tool wear, machine rates from real Indian job-shop data.",
                  points: ["Should-cost modelling", "Indian labour indexing"],
                },
                {
                  n: "03",
                  title: "Execution",
                  desc: "Take the data to the negotiation table. Know exactly where margin is hidden — material, machining, overhead, profit.",
                  points: ["Line-by-line breakdown", "Copy any value instantly"],
                },
              ].map((s, i) => (
                <div
                  key={s.n}
                  className={`p-10 group hover:bg-slate-50 transition-colors ${i < 2 ? "border-b md:border-b-0 md:border-r border-slate-200" : ""}`}
                >
                  <div
                    className="text-4xl font-black text-slate-200 group-hover:transition-colors mb-8 font-mono"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    {s.n}
                  </div>
                  <h3 className="text-2xl font-black mb-4 uppercase tracking-tight text-slate-900">{s.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed mb-6">{s.desc}</p>
                  <ul className="space-y-2">
                    {s.points.map((p) => (
                      <li key={p} className="flex items-center gap-2 text-xs font-black uppercase tracking-widest" style={{ color: PRIMARY }}>
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {p}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Features ── */}
        <section id="features" className="py-24 bg-white border-y border-slate-200">
          <div className="max-w-6xl mx-auto px-6">
            <div className="mb-14">
              <h2 className="text-5xl font-black tracking-tighter uppercase text-slate-900 mb-3">
                Not another <span style={{ color: PRIMARY }}>AI wrapper.</span>
              </h2>
              <div className="h-1 w-24 rounded" style={{ backgroundColor: PRIMARY }} />
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-px bg-slate-200">
              {[
                { title: "Physics engine", desc: "MRR, Sandvik kc1 cutting force, Taylor tool life. Real formulas, not token predictions." },
                { title: "Indian rates", desc: "CNC ₹800/hr, milling ₹1,000/hr, labour ₹250/hr. 15-city index. Not US benchmarks." },
                { title: "Similarity search", desc: "Match to past estimates. Compare paid vs. should-cost. Build institutional memory." },
                { title: "AI validation", desc: "Physics + Gemini in parallel. >15% gap triggers line-by-line AI arbitration." },
                { title: "Any drawing", desc: "PDF, image, any CAD output. GPT-4o vision. No pre-processing, no templates." },
                { title: "4 part types", desc: "Turned, milled, sheet metal, PCB, cable. Defense · Aerospace · Automobile." },
              ].map((f) => (
                <div key={f.title} className="bg-white p-8 hover:bg-slate-50 transition-colors">
                  <h3 className="font-black text-sm uppercase tracking-widest mb-3" style={{ color: PRIMARY }}>{f.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── CTA with image ── */}
        <section className="py-24 px-6 bg-slate-50">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row gap-12 items-center">
            <div className="flex-1 space-y-6">
              <h2 className="text-4xl font-black tracking-tight text-slate-900 leading-tight uppercase">
                Stop overpaying for<br />
                <span className="pl-4" style={{ color: PRIMARY, borderLeft: `4px solid ${PRIMARY}` }}>
                  industrial inertia.
                </span>
              </h2>
              <p className="text-lg text-slate-600">
                Suppliers rely on your lack of data. Costrich gives you the tactical advantage
                to recapture up to 18% margin on every purchase order.
              </p>
              <div className="flex gap-4 pt-2">
                <Link
                  href="/login"
                  className="px-8 py-3 text-white font-black rounded-lg uppercase tracking-tight shadow-lg"
                  style={{ backgroundColor: PRIMARY, boxShadow: `0 8px 24px ${PRIMARY}33` }}
                >
                  Get started free
                </Link>
                <a href="#how-it-works" className="px-8 py-3 bg-white text-slate-900 font-black rounded-lg uppercase tracking-tight border border-slate-200 hover:bg-slate-100 transition-colors">
                  See the math
                </a>
              </div>
            </div>

            <div className="flex-1 w-full">
              <div className="relative rounded-xl overflow-hidden shadow-2xl border border-slate-200">
                {/* Manufacturing floor placeholder */}
                <div className="w-full aspect-video bg-gradient-to-br from-slate-800 to-slate-950 flex items-center justify-center">
                  <div className="grid grid-cols-3 gap-4 p-8 w-full">
                    {[
                      { label: "Estimates run", value: "164+" },
                      { label: "Accuracy", value: "±5–10%" },
                      { label: "Time saved", value: "<60s" },
                    ].map((s) => (
                      <div key={s.label} className="text-center">
                        <div className="text-2xl font-black font-mono text-white mb-1">{s.value}</div>
                        <div className="text-xs text-slate-400 uppercase tracking-widest">{s.label}</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="absolute bottom-6 left-6 right-6 p-4 bg-white/95 backdrop-blur rounded border border-slate-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-[10px] font-black uppercase tracking-[0.2em]" style={{ color: PRIMARY }}>Live Benchmark</div>
                      <div className="text-sm font-mono font-bold text-slate-900">EN8 Steel Shaft · Ø50×100mm</div>
                    </div>
                    <div className="text-right">
                      <div className="text-[10px] font-black text-emerald-600 uppercase tracking-[0.2em]">Savings found</div>
                      <div className="text-sm font-mono font-bold text-emerald-600">+22.4%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing" className="py-24 bg-white border-t border-slate-200">
          <div className="max-w-5xl mx-auto px-6 text-center">
            <h2 className="text-5xl font-black tracking-tighter uppercase text-slate-900 mb-3">
              Pricing
            </h2>
            <div className="h-1 w-16 rounded mx-auto mb-14" style={{ backgroundColor: PRIMARY }} />

            <div className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto text-left">
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-8">
                <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Free</p>
                <p className="text-4xl font-black text-slate-900 font-mono mb-1">₹0</p>
                <p className="text-sm text-slate-400 mb-8">Forever free, no card required</p>
                <div className="space-y-3 mb-8">
                  {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Cost breakdown view", "Similarity search"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 text-sm text-slate-600">
                      <span className="font-black" style={{ color: PRIMARY }}>✓</span> {f}
                    </div>
                  ))}
                </div>
                <Link
                  href="/login"
                  className="block text-center text-white px-6 py-3 rounded-lg font-black uppercase tracking-tight hover:opacity-90 transition-opacity"
                  style={{ backgroundColor: PRIMARY }}
                >
                  Get started free
                </Link>
              </div>

              <div className="rounded-xl p-8 relative overflow-hidden text-white" style={{ backgroundColor: "#0f172a" }}>
                <div className="absolute top-4 right-4 bg-amber-400 text-amber-900 text-xs font-black px-2 py-0.5 rounded-full uppercase">
                  Coming soon
                </div>
                <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Pro</p>
                <p className="text-4xl font-black text-white font-mono mb-1">₹4,999</p>
                <p className="text-sm text-slate-400 mb-8">per user / month</p>
                <div className="space-y-3 mb-8">
                  {["Unlimited estimates", "PCB + cable assembly", "Persistent similarity index", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 text-sm text-slate-300">
                      <span className="text-blue-400 font-black">✓</span> {f}
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-white/10 text-white/40 px-6 py-3 rounded-lg font-black uppercase tracking-tight cursor-not-allowed">
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="py-24 px-6" style={{ backgroundColor: PRIMARY }}>
          <div className="max-w-3xl mx-auto text-center text-white">
            <h2 className="text-5xl font-black tracking-tighter uppercase leading-tight mb-5">
              Stop negotiating blind.
            </h2>
            <p className="text-blue-200 mb-10 text-lg">
              Your first estimate is free. Upload a drawing and see what it should cost in under 60 seconds.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 bg-white text-slate-900 px-10 py-4 rounded-lg text-base font-black uppercase tracking-tight hover:bg-blue-50 transition-colors"
            >
              Try Costrich free
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <p className="text-blue-300 text-xs mt-5 uppercase tracking-widest">
              No credit card · No setup · Just upload and go
            </p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="bg-slate-950 border-t border-white/5 py-12">
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-12">
          <div className="col-span-2 space-y-4">
            <span className="text-xl font-black tracking-tighter text-blue-400">Costrich</span>
            <p className="text-slate-500 text-sm max-w-sm">
              Engineered for manufacturing procurement teams. Physics-based should-cost intelligence for India.
            </p>
          </div>
          <div className="space-y-4">
            <h4 className="font-black text-xs uppercase tracking-widest text-blue-400">Product</h4>
            <ul className="space-y-2 text-sm text-slate-500">
              <li><a href="#how-it-works" className="hover:text-blue-400 transition-colors">How it works</a></li>
              <li><a href="#features" className="hover:text-blue-400 transition-colors">Features</a></li>
              <li><a href="#pricing" className="hover:text-blue-400 transition-colors">Pricing</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="font-black text-xs uppercase tracking-widest text-blue-400">Account</h4>
            <ul className="space-y-2 text-sm text-slate-500">
              <li><Link href="/login" className="hover:text-blue-400 transition-colors">Sign in</Link></li>
              <li><Link href="/login" className="hover:text-blue-400 transition-colors">Get started free</Link></li>
            </ul>
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-6 mt-12 pt-8 border-t border-white/5 flex justify-between items-center text-[10px] font-bold text-slate-600 uppercase tracking-widest">
          <span>© 2026 Costrich. All rights reserved.</span>
          <div className="flex gap-4">
            <a href="#" className="hover:text-blue-400 transition-colors">Privacy</a>
            <a href="#" className="hover:text-blue-400 transition-colors">Terms</a>
          </div>
        </div>
      </footer>

    </div>
  );
}
