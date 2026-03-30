import Link from "next/link";
import Image from "next/image";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-surface-bg text-[#E2E8F0]">

      {/* ── Nav ── */}
      <nav className="bg-surface-bg/90 backdrop-blur-md flex justify-between items-center w-full px-6 lg:px-10 h-16 lg:h-20 fixed top-0 z-50 border-b border-surface-border">
        <div className="flex items-center gap-10">
          <Link href="/" className="flex items-center gap-2.5">
            <Image src="/costrich-logo.png" alt="Costrich" width={32} height={32} className="rounded-lg" />
            <span className="font-heading text-xl text-accent tracking-tight">Costrich</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            {["Problem", "How it works", "Features", "Pricing"].map((l) => (
              <a key={l} href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="font-sans text-sm text-[#94A3B8] hover:text-accent transition-colors">
                {l}
              </a>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-5">
          <Link href="/login" className="hidden sm:block font-sans text-sm text-[#94A3B8] hover:text-[#E2E8F0] transition-colors">
            Sign in
          </Link>
          <Link href="/login" className="px-5 py-2 bg-accent text-surface-bg font-sans text-sm font-semibold rounded-md hover:bg-accent-dark transition-colors">
            Get started
          </Link>
        </div>
      </nav>

      <main className="pt-20">

        {/* ── Hero ── */}
        <section className="relative min-h-[90vh] flex flex-col items-center justify-center px-6 overflow-hidden">
          {/* Subtle grid */}
          <div className="absolute inset-0 opacity-[0.04]" style={{ backgroundImage: "radial-gradient(circle, #94A3B8 1px, transparent 1px)", backgroundSize: "32px 32px" }} />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-surface-bg pointer-events-none" />

          <div className="max-w-6xl w-full text-center space-y-8 relative z-10">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-md bg-surface-card border border-surface-border font-mono text-[11px] text-accent uppercase tracking-widest">
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
              Live product · Not a waitlist
            </div>

            <div className="flex justify-center">
              <Image src="/costrich-logo.png" alt="Costrich" width={72} height={72} className="rounded-2xl" />
            </div>

            <h1 className="font-heading text-[clamp(40px,7vw,88px)] tracking-tight leading-[1.05]">
              Know what it<br />
              <span className="text-accent italic">should cost.</span>
            </h1>

            <p className="max-w-2xl mx-auto font-sans text-lg text-[#94A3B8] leading-relaxed">
              From drawing to negotiation brief in 60 seconds.
              Line-by-line cost intelligence for Indian manufacturing procurement.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/login" className="w-full sm:w-auto px-8 py-3.5 bg-accent text-surface-bg font-sans text-base font-semibold rounded-md hover:bg-accent-dark transition-colors">
                Upload a drawing free
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-3.5 bg-surface-card border border-surface-border text-[#E2E8F0] font-sans text-base font-semibold rounded-md hover:border-accent/40 transition-colors">
                See a live breakdown
              </a>
            </div>

            {/* Dashboard preview */}
            <div id="demo" className="mt-16 relative mx-auto max-w-5xl rounded-xl border border-surface-border bg-surface-card shadow-2xl overflow-hidden">
              <div className="h-8 bg-surface-panel border-b border-surface-border flex items-center px-4 gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
                <div className="w-2.5 h-2.5 rounded-full bg-amber-500/60" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
                <div className="flex-1 mx-3 bg-surface-bg rounded px-3 py-0.5 font-mono text-xs text-[#64748B] border border-surface-border">
                  costrich.ai/estimate/en8-shaft-100qty
                </div>
              </div>
              <div className="p-4 bg-surface-bg">
                <div className="grid grid-cols-12 gap-4">
                  <div className="col-span-12 md:col-span-3 space-y-4">
                    <div className="h-32 bg-surface-card border border-surface-border rounded-lg p-4 flex flex-col justify-between">
                      <span className="font-mono text-[10px] text-[#64748B] uppercase tracking-widest">Should Cost</span>
                      <span className="font-mono text-2xl font-medium text-accent">₹695</span>
                      <div className="h-1 bg-surface-panel rounded overflow-hidden">
                        <div className="h-full w-3/4 rounded bg-accent" />
                      </div>
                    </div>
                    <div className="h-32 bg-surface-card border border-surface-border rounded-lg p-4 flex flex-col justify-between">
                      <span className="font-mono text-[10px] text-[#64748B] uppercase tracking-widest">Supplier Markup</span>
                      <span className="font-mono text-2xl font-medium text-red-400">22.4%</span>
                      <div className="h-1 bg-surface-panel rounded overflow-hidden">
                        <div className="h-full bg-red-500 w-1/2 rounded" />
                      </div>
                    </div>
                  </div>
                  <div className="col-span-12 md:col-span-9">
                    <CostBreakdownTable />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Who it's for ── */}
        <section className="py-20 border-y border-surface-border">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-accent uppercase tracking-widest mb-6">
              Built for both sides of the table
            </p>
            <div className="grid md:grid-cols-2 gap-0 border border-surface-border rounded-xl overflow-hidden">
              {[
                {
                  persona: "BUYER", title: "You send drawings",
                  desc: "OEM or mid-tier. You issue RFQs, negotiate, and need to know if the quoted price is fair — before you sign.",
                  points: ["Should-cost before negotiation", "Line-by-line markup exposure", "Historical cost comparison"],
                },
                {
                  persona: "SUPPLIER", title: "You receive drawings",
                  desc: "Tier 2 or 3 shop. You quote on drawings and win jobs on speed and accuracy. Costrich structures your cost model in minutes.",
                  points: ["Instant cost model from drawing", "Structured quote in minutes", "Win on speed, not guesswork"],
                },
              ].map((p, i) => (
                <div key={p.persona} className={`p-10 bg-surface-card hover:bg-surface-panel transition-colors ${i === 0 ? "border-b md:border-b-0 md:border-r border-surface-border" : ""}`}>
                  <div className="font-mono text-2xl text-surface-border mb-4">{p.persona}</div>
                  <h3 className="font-heading text-xl text-[#E2E8F0] mb-3">{p.title}</h3>
                  <p className="font-sans text-sm text-[#94A3B8] leading-relaxed mb-6">{p.desc}</p>
                  <ul className="space-y-2.5">
                    {p.points.map((pt) => (
                      <li key={pt} className="flex items-center gap-2.5 font-mono text-[11px] text-accent uppercase tracking-widest">
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {pt}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Problem ── */}
        <section id="problem" className="py-24">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <div className="mb-16 max-w-3xl">
              <p className="font-mono text-[11px] text-accent uppercase tracking-widest mb-4">
                Section 01 · The problem
              </p>
              <h2 className="font-heading text-[clamp(32px,4vw,52px)] text-[#E2E8F0] tracking-tight leading-tight mb-6">
                Three things that break every procurement cycle.
              </h2>
              <p className="font-sans text-lg text-[#94A3B8] leading-relaxed">
                Every procurement team has the same three problems. All three are still managed manually — by experienced engineers, in spreadsheets, on instinct. Costrich solves all three with physics.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-px bg-surface-border rounded-xl overflow-hidden mb-16">
              {[
                { n: "01", title: "You don\u2019t know what it should cost", desc: "The supplier quotes \u20B9850. Is that fair? Your senior engineer says \u2018seems high.\u2019 That\u2019s not a negotiation \u2014 that\u2019s a guess. Costrich gives you the physics-based answer: \u20B9695. Line by line." },
                { n: "02", title: "Every quote comparison is manual", desc: "Three suppliers. Three formats. Someone rebuilds it into a spreadsheet every time \u2014 missing the line where one supplier buried a 40% markup on surface treatment." },
                { n: "03", title: "Knowledge walks out the door", desc: "Your best cost estimator has 25 years of experience. When they retire, that knowledge is gone. No record of what past parts cost, why, or what they should have cost." },
              ].map((s) => (
                <div key={s.n} className="bg-surface-card p-10 hover:bg-surface-panel transition-colors">
                  <div className="font-mono text-3xl text-surface-border mb-6">{s.n}</div>
                  <h3 className="font-sans text-lg font-semibold text-[#E2E8F0] mb-4 leading-snug">{s.title}</h3>
                  <p className="font-sans text-sm text-[#94A3B8] leading-relaxed">{s.desc}</p>
                </div>
              ))}
            </div>

            {/* Stats strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-surface-border rounded-xl overflow-hidden">
              {[
                { value: "22%", label: "Average supplier markup we expose on first estimate" },
                { value: "<60s", label: "Drawing to full cost breakdown \u2014 no templates, no setup" },
                { value: "10", label: "Line items per estimate \u2014 material, machining, overhead, margin" },
                { value: "\u00B15-10%", label: "Physics-based accuracy \u2014 not token predictions" },
              ].map((s) => (
                <div key={s.label} className="bg-surface-card p-8 text-center">
                  <div className="font-mono text-3xl text-accent mb-2">{s.value}</div>
                  <div className="font-sans text-xs text-[#64748B] leading-relaxed">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── How it works ── */}
        <section id="how-it-works" className="py-24 border-y border-surface-border">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <div className="mb-16 max-w-3xl">
              <p className="font-mono text-[11px] text-accent uppercase tracking-widest mb-4">
                Section 02 · Process
              </p>
              <h2 className="font-heading text-[clamp(32px,4vw,52px)] text-[#E2E8F0] tracking-tight leading-tight mb-6">
                Three steps. Every cost line exposed.
              </h2>
              <p className="font-sans text-lg text-[#94A3B8] leading-relaxed">
                Every step that currently requires a senior engineer and a spreadsheet — Costrich replaces with physics. From the drawing on your desk to a negotiation-ready cost brief.
              </p>
            </div>

            <div className="space-y-0 border border-surface-border rounded-xl overflow-hidden">
              {[
                {
                  n: "01", title: "Drawing Intelligence",
                  before: "Engineer studies the drawing for an hour. Emails supplier for clarifications. Waits.",
                  after: "AI reads the drawing in seconds. Dimensions, material, tolerances, processes \u2014 extracted automatically.",
                  tags: ["PDF & image support", "Any CAD output", "GD&T extraction"],
                },
                {
                  n: "02", title: "Physics-Based Costing",
                  before: "Senior estimator guesses based on experience. Or asks the supplier what it costs \u2014 and trusts the answer.",
                  after: "Real cutting parameters. Real Indian machine rates. Real cycle times. Every cost line calculated from first principles.",
                  tags: ["Cycle time from MRR", "Indian job-shop rates", "Material + tooling + overhead"],
                },
                {
                  n: "03", title: "Negotiation Brief",
                  before: "You negotiate on total price. Supplier says \u2018that\u2019s the best we can do.\u2019 You have no data to push back.",
                  after: "Line-by-line breakdown shows exactly where the markup is. Material \u20B9228, machining \u20B9165, supplier quoted \u20B9850. Push back with facts.",
                  tags: ["Line-by-line breakdown", "Markup exposure", "Click to copy any value"],
                },
              ].map((s, i) => (
                <div key={s.n} className={`p-10 bg-surface-card hover:bg-surface-panel transition-colors ${i < 2 ? "border-b border-surface-border" : ""}`}>
                  <div className="flex flex-col md:flex-row md:items-start gap-8">
                    <div className="font-mono text-4xl text-surface-border shrink-0">{s.n}</div>
                    <div className="flex-1">
                      <h3 className="font-sans text-xl font-semibold text-[#E2E8F0] mb-6">{s.title}</h3>
                      <div className="grid md:grid-cols-2 gap-4 mb-6">
                        <div className="bg-red-500/5 border border-red-500/15 rounded-lg p-5">
                          <div className="font-mono text-[10px] text-red-400 uppercase tracking-widest mb-2">Before</div>
                          <p className="font-sans text-sm text-red-300/70 leading-relaxed">{s.before}</p>
                        </div>
                        <div className="bg-emerald-500/5 border border-emerald-500/15 rounded-lg p-5">
                          <div className="font-mono text-[10px] text-emerald-400 uppercase tracking-widest mb-2">After</div>
                          <p className="font-sans text-sm text-emerald-300/70 leading-relaxed">{s.after}</p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {s.tags.map((tag) => (
                          <span key={tag} className="font-mono text-[10px] uppercase tracking-widest px-3 py-1 rounded-md border border-surface-border text-[#64748B]">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Features ── */}
        <section id="features" className="py-24">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <p className="font-mono text-[11px] text-accent uppercase tracking-widest mb-4">
              Section 03 · Capabilities
            </p>
            <h2 className="font-heading text-[clamp(32px,4vw,52px)] text-[#E2E8F0] tracking-tight mb-4">
              Not another <span className="text-accent italic">AI wrapper.</span>
            </h2>
            <p className="font-sans text-lg text-[#94A3B8] mb-16 max-w-2xl leading-relaxed">
              Built on Sandvik cutting data, Machinery&apos;s Handbook, Kennametal power constants, and Indian MSME machine hour rates. Physics, not prompt engineering.
            </p>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-px bg-surface-border rounded-xl overflow-hidden">
              {[
                { title: "Drawing Intelligence", desc: "Upload any engineering drawing \u2014 PDF, image, any CAD output. AI extracts dimensions, material, tolerances, and processes automatically. No templates. No pre-processing." },
                { title: "Should-Cost Engine", desc: "Physics-based: cycle times from real cutting parameters, Indian machine rates (\u20B9600-1500/hr), Taylor tool wear. 18 manufacturing processes. Not guesswork." },
                { title: "Negotiation Briefs", desc: "Every estimate is a line-by-line cost breakdown \u2014 material, machining, setup, tooling, labour, overhead, margin. Click any value to copy. Walk in with facts." },
                { title: "AI Validation", desc: "Physics engine and AI run in parallel. If they disagree by more than 15%, an AI arbitrator investigates line by line. Four confidence tiers. Self-correcting." },
                { title: "Cost Baseline Memory", desc: "Every estimate saved. Compare new quotes against historical baselines. Match similar parts across your library. Build institutional cost knowledge that doesn\u2019t retire." },
                { title: "4 Part Types", desc: "Turned parts. Milled parts. Sheet metal. PCB and cable assemblies. 40+ surface treatments. 15 heat treatments. Defense, aerospace, automobile." },
              ].map((f) => (
                <div key={f.title} className="bg-surface-card p-8 hover:bg-surface-panel transition-colors">
                  <h3 className="font-mono text-[11px] text-accent uppercase tracking-widest mb-3">{f.title}</h3>
                  <p className="font-sans text-sm text-[#94A3B8] leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>

            <div className="mt-12 pt-6 border-t border-surface-border">
              <p className="text-center font-mono text-[10px] text-[#475569] uppercase tracking-widest">
                Powered by Sandvik Coromant · Kennametal · Machinery&apos;s Handbook · CMTI Machine Hour Rates · BIS Standards
              </p>
            </div>
          </div>
        </section>

        {/* ── Pricing ── */}
        <section id="pricing" className="py-24 border-t border-surface-border">
          <div className="max-w-5xl mx-auto px-6 lg:px-10 text-center">
            <p className="font-mono text-[11px] text-accent uppercase tracking-widest mb-4">
              Section 04 · Pricing
            </p>
            <h2 className="font-heading text-[clamp(32px,4vw,52px)] text-[#E2E8F0] tracking-tight mb-16">
              Start free. Scale when ready.
            </h2>

            <div className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto text-left">
              <div className="bg-surface-card border border-surface-border rounded-xl p-8">
                <p className="font-mono text-[11px] text-[#64748B] uppercase tracking-widest mb-2">Free</p>
                <p className="font-mono text-4xl text-[#E2E8F0] mb-1">₹0</p>
                <p className="font-sans text-sm text-[#64748B] mb-8">No credit card. No setup. Just upload.</p>
                <div className="space-y-3 mb-8">
                  {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Full line-by-line breakdown", "Similarity search"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 font-sans text-sm text-[#94A3B8]">
                      <span className="text-accent">✓</span> {f}
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center bg-accent text-surface-bg px-6 py-3 rounded-md font-sans font-semibold hover:bg-accent-dark transition-colors">
                  Get started free
                </Link>
              </div>

              <div className="bg-surface-panel border border-accent/20 rounded-xl p-8 relative overflow-hidden">
                <div className="absolute top-4 right-4 bg-amber-500/20 text-amber-400 font-mono text-[10px] px-2.5 py-0.5 rounded-md uppercase tracking-wider">Coming soon</div>
                <p className="font-mono text-[11px] text-[#64748B] uppercase tracking-widest mb-2">Pro</p>
                <p className="font-mono text-4xl text-[#E2E8F0] mb-1">₹4,999</p>
                <p className="font-sans text-sm text-[#64748B] mb-8">per user / month</p>
                <div className="space-y-3 mb-8">
                  {["Unlimited estimates", "PCB + cable assembly", "Persistent cost memory", "Team cost baselines", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 font-sans text-sm text-[#94A3B8]">
                      <span className="text-accent">✓</span> {f}
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-surface-border/50 text-[#64748B] px-6 py-3 rounded-md font-sans font-semibold cursor-not-allowed">
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="py-24 lg:py-32 border-t border-surface-border bg-surface-card">
          <div className="max-w-3xl mx-auto px-6 lg:px-10 text-center">
            <h2 className="font-heading text-[clamp(36px,5vw,64px)] text-[#E2E8F0] tracking-tight leading-tight mb-6">
              Your supplier quoted ₹850.<br />
              The physics says <span className="text-accent italic">₹695.</span>
            </h2>
            <p className="font-sans text-lg text-[#94A3B8] leading-relaxed mb-10">
              Upload a drawing. Get the full should-cost breakdown in 60 seconds. Walk into the negotiation knowing exactly where to push back.
            </p>
            <Link href="/login" className="inline-flex items-center justify-center px-8 py-4 bg-accent text-surface-bg font-sans font-semibold rounded-md hover:bg-accent-dark transition-colors">
              Try Costrich free
              <svg className="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <p className="mt-8 font-mono text-[10px] text-[#475569] uppercase tracking-widest">
              No credit card · No setup · Upload and go
            </p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-surface-border py-16">
        <div className="max-w-6xl mx-auto px-6 lg:px-10 grid grid-cols-2 md:grid-cols-4 gap-12">
          <div className="col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <Image src="/costrich-logo.png" alt="Costrich" width={24} height={24} className="rounded-md" />
              <span className="font-heading text-lg text-accent">Costrich</span>
            </div>
            <p className="font-sans text-sm text-[#64748B] max-w-sm leading-relaxed">
              The cost intelligence engine for Indian manufacturing procurement. Physics-based. Line-by-line. Built for negotiation.
            </p>
          </div>
          <div className="space-y-4">
            <h4 className="font-mono text-[10px] text-accent uppercase tracking-widest">Product</h4>
            <ul className="space-y-2 font-sans text-sm text-[#64748B]">
              {["Problem", "How it works", "Features", "Pricing"].map((l) => (
                <li key={l}><a href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="hover:text-accent transition-colors">{l}</a></li>
              ))}
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="font-mono text-[10px] text-accent uppercase tracking-widest">Account</h4>
            <ul className="space-y-2 font-sans text-sm text-[#64748B]">
              <li><Link href="/login" className="hover:text-accent transition-colors">Sign in</Link></li>
              <li><Link href="/login" className="hover:text-accent transition-colors">Get started free</Link></li>
            </ul>
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-6 lg:px-10 mt-12 pt-8 border-t border-surface-border flex justify-between items-center font-mono text-[10px] text-[#475569] uppercase tracking-widest">
          <span>&copy; 2026 Costrich. Built for Indian manufacturing.</span>
          <div className="flex gap-4">
            <a href="#" className="hover:text-accent transition-colors">Privacy</a>
            <a href="#" className="hover:text-accent transition-colors">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
