import Link from "next/link";
import Image from "next/image";
import { ScrollReveal, StaggerReveal, StaggerItem } from "@/components/ScrollReveal";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Tactical Elegance design system
   Newsreader (headline) + Space Grotesk (body/UI)
   Deep blue #00288e · Tonal surface layering · Ambient shadows
   ───────────────────────────────────────────────────────────── */

const WORKFLOW_STEPS = [
  { num: "1", title: "CAD Ingestion", desc: "Upload your drawing — PDF, DXF, STEP, or image. Securely processed." },
  { num: "2", title: "Geometric Scan", desc: "AI identifies features, tolerances, and surface finishes automatically." },
  { num: "3", title: "Material Grade", desc: "Automated substantiation of alloy requirements against market indices." },
  { num: "4", title: "Cost Benchmark", desc: "Physics-based should-cost model using real Indian manufacturing rates." },
  { num: "5", title: "Export & Negotiate", desc: "Download line-by-line breakdowns for immediate supplier negotiation." },
];

const CAPABILITIES = [
  { tag: "Feature Detection" },
  { tag: "Tool-Path Mapping" },
  { tag: "Tolerance Impact" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#faf8ff] text-[#1a1b20]">

      {/* ── Nav ───────────────────────────────────────────────── */}
      <nav className="fixed top-0 z-50 w-full bg-[#faf8ff]/90 backdrop-blur-md">
        <div className="max-w-[1400px] mx-auto flex items-center justify-between px-8 py-4">
          <div className="flex items-center gap-12">
            <Link href="/" className="text-2xl italic text-[#00288e]" style={{ fontFamily: "var(--font-headline)" }}>
              Newton-Metre
            </Link>
            <div className="hidden md:flex gap-8">
              {[
                ["How it works", "#workflow"],
                ["Capabilities", "#capabilities"],
                ["Pricing", "#pricing"],
              ].map(([label, href]) => (
                <a
                  key={label}
                  href={href}
                  className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                  style={{ fontFamily: "var(--font-label)" }}
                >
                  {label}
                </a>
              ))}
              <Link
                href="/login"
                className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Sign in
              </Link>
            </div>
          </div>
          <Link
            href="/login"
            className="gradient-cta text-white px-6 py-2.5 rounded-lg text-xs font-bold tracking-widest uppercase transition-transform active:scale-95"
            style={{ fontFamily: "var(--font-label)" }}
          >
            New Estimate
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ════════════════════════════════════════════════════════
            HERO — Asymmetric layout with dashboard preview
            ════════════════════════════════════════════════════════ */}
        <section className="pt-12 pb-20 px-8 max-w-[1400px] mx-auto overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-7">
              <ScrollReveal>
                <h1
                  className="hero-title text-[clamp(48px,7vw,72px)] font-extrabold text-[#00288e] mb-8 max-w-2xl"
                  style={{ fontFamily: "var(--font-headline)" }}
                >
                  KNOW WHAT IT SHOULD COST
                </h1>
              </ScrollReveal>
              <ScrollReveal>
                <p className="text-[#515f74] text-lg max-w-xl mb-10 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                  Precision engineering meets sourcing intelligence. Leverage our physics-based engines and Proprietary Geometric Complexity Index to substantiate material grades and manufacturing costs instantly.
                </p>
              </ScrollReveal>
              <ScrollReveal>
                <div className="flex items-center gap-6">
                  <Link
                    href="/login"
                    className="gradient-cta text-white px-8 py-4 rounded-lg font-bold tracking-widest uppercase text-sm transition-transform active:scale-95"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    Start Your Analysis
                  </Link>
                  <a href="#workflow" className="flex items-center gap-2 text-[#00288e] font-bold tracking-tight text-xs uppercase" style={{ fontFamily: "var(--font-label)" }}>
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                    Watch Process
                  </a>
                </div>
              </ScrollReveal>
            </div>

            {/* Hero Dashboard Preview */}
            <div className="lg:col-span-5 relative">
              <ScrollReveal direction="right">
                <div className="bg-white ambient-shadow p-6 rounded-xl border border-[#c4c5d5]/20 relative z-10">
                  <div className="flex justify-between items-center mb-8">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-[#1e40af] rounded flex items-center justify-center">
                        <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={24} height={24} className="invert" />
                      </div>
                      <span className="italic font-bold" style={{ fontFamily: "var(--font-headline)" }}>Analysis: NM-9283</span>
                    </div>
                    <span className="bg-green-100 text-green-800 text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wider">Verified</span>
                  </div>
                  <div className="space-y-6">
                    <div className="bg-[#f4f3fa] p-4 rounded-lg">
                      <div className="flex justify-between text-xs text-[#515f74] uppercase mb-2" style={{ fontFamily: "var(--font-label)" }}>
                        <span>Estimated Manufacturing Cost</span>
                        <span className="font-bold text-[#00288e]">Target Value</span>
                      </div>
                      <div className="text-3xl font-bold text-[#00288e] tabular" style={{ fontFamily: "var(--font-body)" }}>₹ 14,820.45</div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 border-l-2 border-[#1e40af] bg-[#f4f3fa]/50">
                        <div className="text-[10px] text-[#515f74] uppercase font-bold mb-1">Geometric Complexity</div>
                        <div className="text-xl tabular" style={{ fontFamily: "var(--font-body)" }}>0.842 <span className="text-xs text-[#515f74]">Index</span></div>
                      </div>
                      <div className="p-4 border-l-2 border-[#1e40af] bg-[#f4f3fa]/50">
                        <div className="text-[10px] text-[#515f74] uppercase font-bold mb-1">Material Substantiation</div>
                        <div className="text-xl tabular text-blue-600" style={{ fontFamily: "var(--font-body)" }}>Al 6061-T6</div>
                      </div>
                    </div>
                    <div className="pt-4">
                      <div className="flex justify-between text-[10px] font-bold uppercase text-[#515f74] mb-3">
                        <span>Risk Assessment</span>
                        <span>Low Volatility</span>
                      </div>
                      <div className="w-full h-1.5 bg-[#e3e1e8] rounded-full overflow-hidden">
                        <div className="h-full bg-[#00288e] w-4/5 rounded-full" />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="absolute -top-10 -right-10 w-64 h-64 bg-[#1e40af]/5 rounded-full blur-3xl -z-0" />
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            THE PRECISION GAP — Problem statement
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 bg-[#f4f3fa]">
          <div className="max-w-[1400px] mx-auto px-8">
            <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
              <ScrollReveal className="max-w-2xl">
                <span className="text-[#00288e] font-bold tracking-widest text-xs uppercase block mb-4" style={{ fontFamily: "var(--font-label)" }}>The Precision Gap</span>
                <h2 className="text-[clamp(32px,5vw,48px)] font-bold leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
                  Costing is no longer an art form. It&apos;s a science.
                </h2>
              </ScrollReveal>
              <ScrollReveal className="max-w-xs">
                <p className="text-[#515f74] text-sm" style={{ fontFamily: "var(--font-body)" }}>
                  Traditional sourcing relies on &ldquo;gut feeling&rdquo; and historical averages. We replace ambiguity with automated material grade substantiation.
                </p>
              </ScrollReveal>
            </div>

            <StaggerReveal className="grid grid-cols-1 md:grid-cols-3 gap-px bg-[#c4c5d5]/10" delayStep={100}>
              {[
                { icon: "⚠", title: "Opaque Quotations", desc: "Lack of transparency in supplier pricing models leads to an average 14% overspend on precision parts." },
                { icon: "📊", title: "Manual Analysis", desc: "Engineering teams waste 40+ hours per project verifying material grades and geometric difficulties manually." },
                { icon: "🔺", title: "Risk Exposure", desc: "Inaccurate cost estimates lead to budget overruns and missed delivery windows in high-stakes manufacturing." },
              ].map((item) => (
                <StaggerItem key={item.title}>
                  <div className="bg-[#faf8ff] p-12 hover:bg-white transition-colors group">
                    <span className="text-[#00288e] text-4xl mb-8 group-hover:scale-110 transition-transform block">{item.icon}</span>
                    <h3 className="text-2xl font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>{item.title}</h3>
                    <p className="text-[#515f74] text-sm leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
                  </div>
                </StaggerItem>
              ))}
            </StaggerReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            WORKFLOW — 5 steps with large background numbers
            ════════════════════════════════════════════════════════ */}
        <section id="workflow" className="py-24 max-w-[1400px] mx-auto px-8">
          <ScrollReveal className="text-center mb-20">
            <h2 className="text-[clamp(32px,5vw,48px)] font-bold mb-6" style={{ fontFamily: "var(--font-headline)" }}>
              The Newton-Metre Workflow
            </h2>
            <p className="text-[#515f74] max-w-xl mx-auto text-base" style={{ fontFamily: "var(--font-body)" }}>
              Five steps from raw drawing data to a definitive, defensible cost breakdown.
            </p>
          </ScrollReveal>

          <StaggerReveal className="grid grid-cols-1 md:grid-cols-5 gap-8" delayStep={80}>
            {WORKFLOW_STEPS.map((step) => (
              <StaggerItem key={step.num}>
                <div className="relative text-center">
                  <div
                    className="text-[#00288e]/10 text-[120px] font-bold select-none leading-none"
                    style={{ fontFamily: "var(--font-headline)" }}
                  >
                    {step.num}
                  </div>
                  <div className="relative z-10 -mt-8">
                    <h4 className="font-bold text-xs uppercase tracking-widest text-[#00288e] mb-3" style={{ fontFamily: "var(--font-label)" }}>
                      {step.title}
                    </h4>
                    <p className="text-sm text-[#515f74] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                      {step.desc}
                    </p>
                  </div>
                </div>
              </StaggerItem>
            ))}
          </StaggerReveal>
        </section>

        {/* ════════════════════════════════════════════════════════
            CAPABILITIES — Bento grid
            ════════════════════════════════════════════════════════ */}
        <section id="capabilities" className="py-24 bg-[#faf8ff]">
          <div className="max-w-[1400px] mx-auto px-8">
            <ScrollReveal>
              <h2 className="text-[clamp(32px,5vw,48px)] font-bold mb-16 text-center" style={{ fontFamily: "var(--font-headline)" }}>
                Engineering Capabilities
              </h2>
            </ScrollReveal>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
              {/* Large card — Geometric Complexity Index */}
              <ScrollReveal className="md:col-span-8">
                <div className="bg-[#f4f3fa] rounded-xl p-10 flex flex-col justify-between min-h-[280px] relative overflow-hidden group">
                  <div className="max-w-md relative z-10">
                    <h3 className="text-3xl font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>
                      Proprietary Geometric Complexity Index
                    </h3>
                    <p className="text-[#515f74] text-sm" style={{ fontFamily: "var(--font-body)" }}>
                      Quantify manufacturing difficulty with an algorithm that maps geometric variables to machining time and machine hourly rates.
                    </p>
                  </div>
                  <div className="mt-12 relative z-10 flex gap-4 flex-wrap">
                    {CAPABILITIES.map((c) => (
                      <span key={c.tag} className="bg-[#00288e]/5 text-[#00288e] text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded">
                        {c.tag}
                      </span>
                    ))}
                  </div>
                </div>
              </ScrollReveal>

              {/* Small card — Integrations */}
              <ScrollReveal className="md:col-span-4">
                <div className="bg-[#1e40af] text-white rounded-xl p-10 flex flex-col justify-center text-center min-h-[280px]">
                  <div className="mb-6 text-6xl opacity-50">⚙</div>
                  <h3 className="text-2xl font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>Unified Integrations</h3>
                  <p className="text-white/70 text-sm leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                    Direct synchronization with SolidWorks, SAP, and Oracle for seamless procurement lifecycles.
                  </p>
                </div>
              </ScrollReveal>

              {/* Small card — Material Grade */}
              <ScrollReveal className="md:col-span-4">
                <div className="bg-[#e3e1e8] rounded-xl p-10 flex flex-col justify-center min-h-[250px]">
                  <h3 className="text-2xl font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>Automated Material Grade</h3>
                  <p className="text-[#515f74] text-sm" style={{ fontFamily: "var(--font-body)" }}>
                    Verify compliance and market pricing for over 12,000 specific metal alloys and industrial polymers.
                  </p>
                </div>
              </ScrollReveal>

              {/* Medium card — Rupee Benchmarking */}
              <ScrollReveal className="md:col-span-8">
                <div className="bg-[#f4f3fa] rounded-xl p-10 flex items-center gap-12 overflow-hidden min-h-[250px]">
                  <div className="flex-1">
                    <h3 className="text-3xl font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>
                      Real-Time Rupee (₹) Benchmarking
                    </h3>
                    <p className="text-[#515f74] text-sm" style={{ fontFamily: "var(--font-body)" }}>
                      We track thousands of live transactions across India&apos;s manufacturing hubs to ensure your should-cost is hyper-accurate to local market conditions.
                    </p>
                  </div>
                  <div className="hidden lg:flex w-48 h-48 bg-white/50 rounded-full items-center justify-center border border-[#c4c5d5]/30">
                    <span className="text-5xl font-bold text-[#00288e]" style={{ fontFamily: "var(--font-body)" }}>₹</span>
                  </div>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            PRICING
            ════════════════════════════════════════════════════════ */}
        <section id="pricing" className="py-24 bg-[#f4f3fa]">
          <div className="max-w-4xl mx-auto px-8 text-center">
            <ScrollReveal>
              <span className="text-[#00288e] font-bold tracking-widest text-xs uppercase block mb-4" style={{ fontFamily: "var(--font-label)" }}>Pricing</span>
              <h2 className="text-[clamp(28px,4.5vw,48px)] font-bold mb-4" style={{ fontFamily: "var(--font-headline)" }}>
                Start free. Pay when it pays for itself.
              </h2>
              <p className="max-w-md mx-auto text-[16px] text-[#515f74] leading-[1.7] mb-16" style={{ fontFamily: "var(--font-body)" }}>
                One estimate that catches a 20% overpayment pays for a year of Pro.
              </p>
            </ScrollReveal>

            <StaggerReveal className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left" delayStep={120}>
              <StaggerItem>
                <div className="bg-white ghost-border rounded-xl p-8 hover:ambient-shadow transition-shadow">
                  <p className="text-[12px] text-[#515f74] uppercase tracking-[0.25em] mb-3 font-bold" style={{ fontFamily: "var(--font-label)" }}>Free</p>
                  <p className="text-[36px] text-[#00288e] tracking-tight mb-1 font-bold" style={{ fontFamily: "var(--font-headline)" }}>₹0</p>
                  <p className="text-[14px] text-[#757684] mb-8" style={{ fontFamily: "var(--font-body)" }}>No card required</p>
                  <div className="space-y-3 mb-8">
                    {["10 estimates / month", "Should-cost breakdown", "Similarity search", "PDF & image uploads", "All part types"].map((f) => (
                      <div key={f} className="flex items-center gap-2.5">
                        <svg className="w-3.5 h-3.5 text-[#00288e] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>
                        <span className="text-[14px] text-[#444653]" style={{ fontFamily: "var(--font-body)" }}>{f}</span>
                      </div>
                    ))}
                  </div>
                  <Link href="/login" className="block text-center gradient-cta text-white px-6 py-3.5 rounded-lg font-bold text-[14px] tracking-widest uppercase" style={{ fontFamily: "var(--font-label)" }}>
                    Upload a drawing
                  </Link>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="bg-white ghost-border rounded-xl p-8 relative hover:ambient-shadow transition-shadow border-2 border-[#00288e]/20">
                  <p className="text-[12px] text-[#515f74] uppercase tracking-[0.25em] mb-3 font-bold" style={{ fontFamily: "var(--font-label)" }}>Pro</p>
                  <p className="text-[36px] text-[#00288e] tracking-tight mb-1 font-bold" style={{ fontFamily: "var(--font-headline)" }}>₹4,999</p>
                  <p className="text-[14px] text-[#757684] mb-8" style={{ fontFamily: "var(--font-body)" }}>per user / month</p>
                  <div className="space-y-3 mb-8">
                    {["Unlimited estimates", "Persistent part library", "Team cost memory", "Excel / PDF export", "Priority support"].map((f) => (
                      <div key={f} className="flex items-center gap-2.5">
                        <svg className="w-3.5 h-3.5 text-[#00288e] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>
                        <span className="text-[14px] text-[#444653]" style={{ fontFamily: "var(--font-body)" }}>{f}</span>
                      </div>
                    ))}
                  </div>
                  <Link href="/login?waitlist=pro" className="block text-center gradient-cta text-white px-6 py-3.5 rounded-lg font-bold text-[14px] tracking-widest uppercase" style={{ fontFamily: "var(--font-label)" }}>
                    Join waitlist
                  </Link>
                </div>
              </StaggerItem>
            </StaggerReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            FINAL CTA
            ════════════════════════════════════════════════════════ */}
        <section className="py-32 relative overflow-hidden">
          <ScrollReveal className="max-w-[1200px] mx-auto px-8 text-center relative z-10">
            <h2
              className="text-[clamp(36px,6vw,64px)] font-bold mb-10 max-w-4xl mx-auto leading-tight"
              style={{ fontFamily: "var(--font-headline)" }}
            >
              Stop guessing. Start calculating with engineering precision.
            </h2>
            <div className="flex flex-col md:flex-row gap-6 justify-center items-center">
              <Link
                href="/login"
                className="gradient-cta text-white px-10 py-5 rounded-lg text-sm font-bold tracking-widest uppercase shadow-xl shadow-[#00288e]/20 transition-transform active:scale-95"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Get Your First Estimate
              </Link>
              <a
                href="mailto:chand@costimize.dev"
                className="ghost-border text-[#00288e] px-10 py-5 rounded-lg text-sm font-bold tracking-widest uppercase hover:bg-[#efedf4] transition-colors"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Contact Engineering
              </a>
            </div>
          </ScrollReveal>
          <div className="absolute inset-0 bg-[#f4f3fa] -z-0 opacity-50" />
          <div className="absolute -bottom-24 -left-24 w-[500px] h-[500px] bg-[#00288e]/5 rounded-full blur-3xl" />
        </section>

      </main>

      {/* ── Footer ────────────────────────────────────────────── */}
      <footer className="bg-slate-50 py-12">
        <div className="flex flex-col md:flex-row justify-between items-center px-8 max-w-[1400px] mx-auto w-full">
          <div className="mb-8 md:mb-0">
            <span className="text-lg text-[#1a1b20] block mb-2 italic" style={{ fontFamily: "var(--font-headline)" }}>Newton-Metre</span>
            <p className="text-[12px] text-[#757684]" style={{ fontFamily: "var(--font-body)" }}>© 2026 Newton-Metre. Precision Sourcing Intelligence.</p>
          </div>
          <div className="flex gap-8">
            {["Privacy Policy", "Terms of Service"].map((link) => (
              <a key={link} href="#" className="text-[#757684] text-[12px] hover:underline decoration-[#00288e]/30 transition-all" style={{ fontFamily: "var(--font-body)" }}>
                {link}
              </a>
            ))}
            <a href="mailto:chand@costimize.dev" className="text-[#757684] text-[12px] hover:underline decoration-[#00288e]/30 transition-all" style={{ fontFamily: "var(--font-body)" }}>
              Contact Engineering
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
