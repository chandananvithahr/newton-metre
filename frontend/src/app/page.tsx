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
            {["How it works", "Features", "Pricing"].map((l) => (
              <a key={l} href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="font-sans text-sm text-slate-500 hover:text-cyan-600 transition-colors">
                {l}
              </a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-5">
          <Link href="/login" className="hidden sm:block font-sans text-sm text-slate-500 hover:text-slate-800 transition-colors">
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2 bg-cyan-600 text-white font-sans text-sm font-semibold rounded-md hover:bg-cyan-700 transition-colors">
            Get started
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ── Hero ── */}
        <section className="relative min-h-[85vh] flex flex-col items-center justify-center px-6 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: "radial-gradient(circle, #94A3B8 1px, transparent 1px)", backgroundSize: "32px 32px" }} />

          <div className="max-w-5xl w-full text-center space-y-6 relative z-10">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 font-mono text-[11px] text-cyan-700 uppercase tracking-widest">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
              Live product · Not a waitlist
            </div>

            <h1 className="font-heading text-[clamp(40px,7vw,80px)] tracking-tight leading-[1.05] text-slate-900">
              Know what it<br />
              <span className="text-cyan-600 italic">should cost.</span>
            </h1>

            <p className="max-w-xl mx-auto font-sans text-lg text-slate-500 leading-relaxed">
              Upload a drawing. Get a line-by-line should-cost breakdown in 60 seconds. Walk into the negotiation with facts.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-cyan-600 text-white font-sans text-base font-semibold rounded-md hover:bg-cyan-700 transition-colors">
                Upload a drawing free
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 bg-white border border-slate-200 text-slate-700 font-sans text-base font-semibold rounded-md hover:border-cyan-300 transition-colors">
                See a live breakdown ↓
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
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-12">
              Three steps. Every cost line exposed.
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  n: "01",
                  title: "Upload any drawing",
                  desc: "PDF, image, any CAD output. AI extracts dimensions, material, tolerances, and processes automatically.",
                },
                {
                  n: "02",
                  title: "Physics runs the numbers",
                  desc: "Real cutting parameters, Indian machine rates, Taylor tool wear. 18 processes calculated from first principles.",
                },
                {
                  n: "03",
                  title: "Negotiate with facts",
                  desc: "Line-by-line breakdown: material, machining, setup, tooling, overhead, margin. Click any value to copy.",
                },
              ].map((s) => (
                <div key={s.n} className="bg-white border border-slate-200 rounded-xl p-8 hover:border-cyan-300 transition-colors">
                  <div className="font-mono text-3xl text-slate-200 mb-4">{s.n}</div>
                  <h3 className="font-sans text-lg font-semibold text-slate-800 mb-3">{s.title}</h3>
                  <p className="font-sans text-sm text-slate-500 leading-relaxed">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Features ── */}
        <section id="features" className="py-20">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">Capabilities</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-4">
              Not another <span className="text-cyan-600 italic">AI wrapper.</span>
            </h2>
            <p className="font-sans text-base text-slate-500 mb-12 max-w-2xl leading-relaxed">
              Built on Sandvik cutting data, Machinery&apos;s Handbook, and Indian MSME machine hour rates.
            </p>

            <div className="grid sm:grid-cols-2 gap-6">
              {[
                { title: "Should-Cost Engine", desc: "Physics-based cycle times, Indian machine rates, Taylor tool wear. Not guesswork." },
                { title: "AI Validation", desc: "Physics engine and AI run in parallel. Four confidence tiers. Self-correcting." },
                { title: "4 Part Types", desc: "Turned, milled, sheet metal, PCB & cable. 40+ surface treatments. 15 heat treatments." },
                { title: "Cost Memory", desc: "Every estimate saved. Compare new quotes against historical baselines. Knowledge that doesn't retire." },
              ].map((f) => (
                <div key={f.title} className="bg-white border border-slate-200 rounded-xl p-6 hover:border-cyan-300 transition-colors">
                  <h3 className="font-sans text-sm font-semibold text-slate-800 mb-2">{f.title}</h3>
                  <p className="font-sans text-sm text-slate-500 leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>

            <div className="mt-10 pt-5 border-t border-slate-200">
              <p className="text-center font-mono text-[10px] text-slate-400 uppercase tracking-widest">
                Sandvik Coromant · Kennametal · Machinery&apos;s Handbook · CMTI Machine Hour Rates
              </p>
            </div>
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing" className="py-20 bg-slate-50 border-y border-slate-200">
          <div className="max-w-4xl mx-auto px-6 lg:px-10 text-center">
            <p className="font-mono text-[11px] text-cyan-600 uppercase tracking-widest mb-3">Pricing</p>
            <h2 className="font-heading text-[clamp(28px,4vw,44px)] text-slate-900 tracking-tight mb-12">
              Start free. Scale when ready.
            </h2>

            <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left">
              <div className="bg-white border border-slate-200 rounded-xl p-8">
                <p className="font-mono text-[11px] text-slate-400 uppercase tracking-widest mb-2">Free</p>
                <p className="font-mono text-4xl text-slate-900 mb-1">₹0</p>
                <p className="font-sans text-sm text-slate-400 mb-6">No credit card required</p>
                <div className="space-y-2.5 mb-6">
                  {["10 estimates / month", "Mechanical + sheet metal", "Full line-by-line breakdown"].map((f) => (
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
                  {["Unlimited estimates", "PCB + cable assembly", "Team cost baselines", "Excel / PDF export"].map((f) => (
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
        <section className="py-20">
          <div className="max-w-3xl mx-auto px-6 lg:px-10 text-center">
            <h2 className="font-heading text-[clamp(32px,5vw,56px)] text-slate-900 tracking-tight leading-tight mb-4">
              Your supplier quoted <span className="font-mono">₹850</span>.<br />
              The physics says <span className="text-cyan-600 italic font-mono">₹695.</span>
            </h2>
            <p className="font-sans text-lg text-slate-500 leading-relaxed mb-8">
              Upload a drawing. Get the breakdown. Negotiate with data.
            </p>
            <Link href="/login" className="inline-flex items-center justify-center px-8 py-4 bg-cyan-600 text-white font-sans font-semibold rounded-md hover:bg-cyan-700 transition-colors">
              Try Costrich free →
            </Link>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-200 py-12 bg-slate-50">
        <div className="max-w-5xl mx-auto px-6 lg:px-10 flex flex-col md:flex-row justify-between items-start gap-8">
          <div className="flex items-center gap-2">
            <Image src="/costrich-logo.png" alt="Costrich" width={36} height={36} className="rounded-lg" />
            <span className="font-heading text-xl text-cyan-600">Costrich</span>
          </div>
          <div className="flex gap-8 font-sans text-sm text-slate-500">
            {["How it works", "Features", "Pricing"].map((l) => (
              <a key={l} href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="hover:text-cyan-600 transition-colors">{l}</a>
            ))}
            <Link href="/login" className="hover:text-cyan-600 transition-colors">Sign in</Link>
          </div>
        </div>
        <div className="max-w-5xl mx-auto px-6 lg:px-10 mt-8 pt-6 border-t border-slate-200 font-mono text-[10px] text-slate-400 uppercase tracking-widest">
          © 2026 Costrich. Built for Indian manufacturing.
        </div>
      </footer>
    </div>
  );
}
