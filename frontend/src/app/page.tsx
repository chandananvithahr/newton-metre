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
            <Image src="/costrich-logo.png" alt="Costrich" width={44} height={44} className="rounded-xl" />
            <span className="font-heading text-2xl text-cyan-600 tracking-tight">Costrich</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            {[["How it works", "#how-it-works"], ["Features", "#features"], ["Pricing", "#pricing"]].map(([l, h]) => (
              <a key={l} href={h} className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">{l}</a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-5">
          <Link href="/login" className="hidden sm:block font-sans text-sm text-slate-500 hover:text-slate-800 transition-colors">
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2 bg-cyan-600 text-white font-sans text-sm font-semibold rounded-md hover:bg-cyan-700 transition-colors">
            Get started free
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ── Hero ── */}
        <section className="relative min-h-[88vh] flex flex-col items-center justify-center px-6 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: "radial-gradient(circle, #94A3B8 1px, transparent 1px)", backgroundSize: "32px 32px" }} />

          <div className="max-w-5xl w-full text-center space-y-7 relative z-10">

            {/* Logo mark */}
            <div className="flex justify-center">
              <Image src="/costrich-logo.png" alt="Costrich" width={88} height={88} className="rounded-2xl shadow-lg" />
            </div>

            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 font-mono text-[11px] text-cyan-700 uppercase tracking-widest">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
              Physics-based · ±5–10% accuracy
            </div>

            <h1 className="font-heading text-[clamp(44px,7vw,84px)] tracking-tight leading-[1.04] text-slate-900">
              Know what it<br />
              <span className="text-cyan-600 italic">should cost.</span>
            </h1>

            <p className="max-w-xl mx-auto font-sans text-lg text-slate-500 leading-relaxed">
              AI-powered should-cost breakdowns for mechanical parts. Line-by-line, physics-based, built for Indian manufacturing economics.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-cyan-600 text-white font-sans text-base font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                Get my first estimate
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 bg-white border border-slate-200 text-slate-700 font-sans text-base font-semibold rounded-md hover:border-cyan-300 transition-colors">
                See a sample breakdown ↓
              </a>
            </div>
          </div>
        </section>

        {/* ── Live Demo ── */}
        <section id="demo" className="pb-24 px-6">
          <div className="max-w-3xl mx-auto">
            <CostBreakdownTable />
          </div>
        </section>

        {/* ── How it works ── */}
        <section id="how-it-works" className="py-20 bg-slate-50 border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">How it works</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4">
              From drawing to negotiation-ready<br className="hidden md:block" /> in under 60 seconds.
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-2xl leading-relaxed">
              Physics-based math, Indian manufacturing rates.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  n: "01",
                  title: "Upload",
                  desc: "Upload your engineering drawing or CAD file. Dimensions, material, and process requirements extracted directly — no conversion, no quality loss.",
                  tags: ["PDF · DXF · DWG · STEP", "Image support"],
                },
                {
                  n: "02",
                  title: "Calculate",
                  desc: "Physics-based cost modelling: cycle times, tool wear, machine rates from real Indian job-shop data. No guesswork.",
                  tags: ["Should-cost modelling", "Indian labour indexing"],
                },
                {
                  n: "03",
                  title: "Negotiate",
                  desc: "Receive a line-by-line cost breakdown — material, machining, overhead, and margin — ready to use in any supplier conversation.",
                  tags: ["Line-by-line breakdown", "Copy any value instantly"],
                },
              ].map((s) => (
                <div key={s.n} className="bg-white border border-slate-200 rounded-xl p-8 hover:border-cyan-300 transition-colors">
                  <div className="font-mono text-3xl text-slate-200 mb-4">{s.n}</div>
                  <h3 className="font-sans text-lg font-semibold text-slate-800 mb-3">{s.title}</h3>
                  <p className="font-sans text-sm text-slate-500 leading-relaxed mb-4">{s.desc}</p>
                  <div className="flex flex-wrap gap-2">
                    {s.tags.map((t) => (
                      <span key={t} className="font-mono text-[10px] px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-full text-slate-500 uppercase tracking-wide">{t}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Features ── */}
        <section id="features" className="py-20">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">Capabilities</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-12">
              Not another <span className="text-cyan-600 italic">AI wrapper.</span>
            </h2>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { title: "Physics engine", desc: "MRR, cutting force, Taylor tool life. Real formulas, not token predictions." },
                { title: "Indian rates", desc: "CNC ₹800/hr, milling ₹1,000/hr, labour ₹250/hr. 15-city index. Not US benchmarks." },
                { title: "Similarity search", desc: "Match to past estimates. Compare paid vs. should-cost. Build institutional memory." },
                { title: "AI validation", desc: "Physics and AI run in parallel. Gap >15% triggers line-by-line arbitration." },
                { title: "Any drawing", desc: "PDF, image, DXF, DWG, STEP. Dimensions extracted directly — no pre-processing, no templates." },
                { title: "4 part types", desc: "Turned, milled, sheet metal, PCB & cable. Defense · Aerospace · Automobile." },
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
                  Make every purchase<br />order count.
                </h2>
                <p className="font-sans text-base text-slate-500 leading-relaxed mb-8">
                  When you know what a part should cost, you negotiate from facts. Costrich gives procurement teams the data to close better deals — every time.
                </p>
                <div className="flex flex-wrap gap-4">
                  <Link href="/login" className="px-6 py-3 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                    Get started free
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
                  <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-3">Live Benchmark</p>
                  <p className="font-sans text-sm font-semibold text-slate-800 mb-1">EN8 Steel Shaft · Ø50×100mm</p>
                  <div className="flex items-center justify-between">
                    <span className="font-sans text-sm text-slate-500">Savings found</span>
                    <span className="font-mono text-sm font-bold text-cyan-600">+22.4%</span>
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
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-12">
              Start free. Scale when ready.
            </h2>

            <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left">
              <div className="bg-white border border-slate-200 rounded-xl p-8">
                <p className="font-mono text-[11px] text-slate-400 uppercase tracking-widest mb-2">Free</p>
                <p className="font-mono text-4xl text-slate-900 mb-1">₹0</p>
                <p className="font-sans text-sm text-slate-400 mb-6">Forever free, no card required</p>
                <div className="space-y-2.5 mb-6">
                  {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Cost breakdown view", "Similarity search"].map((f) => (
                    <div key={f} className="flex items-center gap-2 font-sans text-sm text-slate-600">
                      <span className="text-cyan-500">✓</span> {f}
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center bg-cyan-600 text-white px-6 py-3 rounded-md font-sans font-semibold hover:bg-cyan-700 transition-colors">
                  Get started free
                </Link>
              </div>

              <div className="bg-white border border-cyan-200 rounded-xl p-8 relative">
                <div className="absolute top-4 right-4 bg-amber-50 text-amber-600 font-mono text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider border border-amber-200">Coming soon</div>
                <p className="font-mono text-[11px] text-slate-400 uppercase tracking-widest mb-2">Pro</p>
                <p className="font-mono text-4xl text-slate-900 mb-1">₹4,999</p>
                <p className="font-sans text-sm text-slate-400 mb-6">per user / month</p>
                <div className="space-y-2.5 mb-6">
                  {["Unlimited estimates", "PCB + cable assembly", "Persistent similarity index", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
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
              Your first estimate is free.
            </h2>
            <p className="font-sans text-lg text-slate-500 leading-relaxed mb-8">
              Upload a drawing and get a full should-cost breakdown in under 60 seconds. No credit card, no setup.
            </p>
            <Link href="/login" className="inline-flex items-center justify-center px-8 py-4 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
              Try Costrich free →
            </Link>
            <p className="mt-4 font-sans text-sm text-slate-400">No credit card · No setup · Just upload and go</p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-200 py-12 bg-white">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2.5 mb-3">
                <Image src="/costrich-logo.png" alt="Costrich" width={40} height={40} className="rounded-xl" />
                <span className="font-heading text-xl text-cyan-600">Costrich</span>
              </div>
              <p className="font-sans text-sm text-slate-500 max-w-xs leading-relaxed">
                Engineered for manufacturing procurement teams. Physics-based should-cost intelligence for India.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-x-12 gap-y-2">
              <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-2 col-span-2">Product</p>
              {[["How it works", "#how-it-works"], ["Features", "#features"], ["Pricing", "#pricing"]].map(([l, h]) => (
                <a key={l} href={h} className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">{l}</a>
              ))}
              <p className="font-mono text-[10px] text-slate-400 uppercase tracking-widest mb-2 col-span-2 mt-4">Account</p>
              <Link href="/login" className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">Sign in</Link>
              <Link href="/login" className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">Get started free</Link>
            </div>
          </div>
          <div className="border-t border-slate-200 pt-6 font-mono text-[10px] text-slate-400 uppercase tracking-widest">
            © 2026 Costrich. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
