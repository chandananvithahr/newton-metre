import Link from "next/link";
import Image from "next/image";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";
import { ScrollReveal, StaggerReveal, StaggerItem } from "@/components/ScrollReveal";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Emil Kowalski design engineering applied
   Custom easings · scroll reveals · stagger · hover-lift
   clip-path image reveals · button press · reduced-motion
   ───────────────────────────────────────────────────────────── */

const PROCESS_STEPS = [
  {
    img: "/assets/image_1.png",
    title: "CNC Turning",
    sub: "Material + Machining",
    cost: "₹340",
    desc: "Steel billet clamped in a 3-jaw chuck. Chips curl, coolant catches light. Time and material — calculated.",
  },
  {
    img: "/assets/image_2.png",
    title: "CNC Milling",
    sub: "Milling",
    cost: "₹190",
    desc: "End mill plunging into a polished shaft. Keyway slot cut with micron precision on a 3-axis VMC.",
  },
  {
    img: "/assets/image_3.png",
    title: "Sequential Drilling",
    sub: "Drilling",
    cost: "₹32",
    desc: "Four M6 holes in sequence. Twist drill penetrating steel flange, chips spiraling upward.",
  },
  {
    img: "/assets/image_4.png",
    title: "Surface Treatment",
    sub: "Chrome Plating",
    cost: "₹120",
    desc: "Finished shaft lowered into a chrome plating bath. Bubbles rising. Scientific precision.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#F8F8F6] text-slate-900">

      {/* ── Nav ───────────────────────────────────────────────── */}
      <nav className="fixed top-0 z-50 w-full bg-[#F8F8F6]/90 backdrop-blur-md border-b border-slate-200/80">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 lg:px-10 h-16 lg:h-20">
          <Link href="/" className="flex items-center gap-3">
            <Image src="/newton-metre-logo.png" alt="Costrich" width={40} height={40} className="rounded-xl" />
            <span style={{ fontFamily: "var(--font-heading)" }} className="text-[22px] text-cyan-600 tracking-tight">Costrich</span>
          </Link>
          <div className="flex items-center gap-8">
            <div className="hidden md:flex items-center gap-8">
              {[["Process", "#process"], ["Pricing", "#pricing"]].map(([l, h]) => (
                <a key={l} href={h} className="link-reveal text-[14px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
              ))}
            </div>
            <Link href="/login" className="hidden sm:block link-reveal text-[14px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
              Sign in
            </Link>
            <Link href="/login" className="px-5 py-2.5 bg-slate-900 text-white text-[14px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200" style={{ fontFamily: "var(--font-sans)" }}>
              Get started
            </Link>
          </div>
        </div>
      </nav>

      <main className="pt-20">

        {/* ════════════════════════════════════════════════════════
            HERO — Staggered text entrance
            ════════════════════════════════════════════════════════ */}
        <section className="relative overflow-hidden bg-slate-900">
          <div className="absolute inset-0">
            <Image src="/assets/image_0.png" alt="" fill className="object-cover object-center opacity-70" priority />
            <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-transparent" />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-transparent to-slate-900/30" />
          </div>

          <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-10 py-32 lg:py-44">
            <div className="max-w-2xl">
              <p className="mb-6 text-[14px] text-cyan-400 uppercase tracking-[0.25em] font-medium animate-fade-in-up" style={{ fontFamily: "var(--font-mono)" }}>
                Your AI cost analyst. Works 24/7. Never wrong.
              </p>

              <h1 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(40px,7vw,76px)] tracking-[-0.03em] leading-[1.05] text-white mb-6 animate-fade-in-up animate-fade-in-up-delay-1">
                Know what it costs.<br />
                <span className="text-cyan-400 italic">Before they quote.</span>
              </h1>

              <div className="max-w-lg space-y-3 mb-10 animate-fade-in-up animate-fade-in-up-delay-2">
                <p className="text-[20px] text-white/70 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>
                  Costrich reads your drawing, breaks down every cost line — material, machining, finishing, margin — like a senior cost analyst would.
                </p>
                <p className="text-[20px] text-white/70 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>
                  Then searches your company&apos;s entire history for similar parts. Instantly.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-start gap-4 animate-fade-in-up animate-fade-in-up-delay-3">
                <Link href="/login" className="px-8 py-4 bg-white text-slate-900 text-[15px] font-medium rounded-full hover:bg-slate-100 transition-all duration-200 hover:shadow-lg" style={{ fontFamily: "var(--font-sans)" }}>
                  Upload a drawing — free
                </Link>
                <a href="#process" className="px-8 py-4 text-white/50 text-[15px] font-medium hover:text-white/80 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                  See the process ↓
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            TRUST BAR — fade in on scroll
            ════════════════════════════════════════════════════════ */}
        <section className="py-10 border-b border-slate-200/60">
          <ScrollReveal direction="none">
            <div className="max-w-5xl mx-auto px-6">
              <div className="flex flex-wrap items-center justify-center gap-x-12 gap-y-4">
                {[
                  { val: "18", label: "Machining processes" },
                  { val: "40+", label: "Surface treatments" },
                  { val: "164", label: "Physics tests passing" },
                  { val: "4", label: "Part types supported" },
                ].map((item) => (
                  <div key={item.label} className="flex items-center gap-2.5">
                    <span className="text-[15px] font-bold text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>{item.val}</span>
                    <span className="text-[13px] text-slate-300" style={{ fontFamily: "var(--font-sans)" }}>{item.label}</span>
                  </div>
                ))}
              </div>
              <div className="mt-5 flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
                {["Defense", "Aerospace", "Automobile"].map((industry) => (
                  <span key={industry} className="text-[12px] text-slate-400 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>{industry}</span>
                ))}
              </div>
            </div>
          </ScrollReveal>
        </section>

        {/* ════════════════════════════════════════════════════════
            THE PROCESS — Staggered card reveals + hover lift
            ════════════════════════════════════════════════════════ */}
        <section id="process" className="py-24 lg:py-32">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <ScrollReveal>
              <p className="text-center mb-4 text-[13px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
                The Process
              </p>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,5vw,52px)] text-slate-900 tracking-[-0.02em] leading-tight mb-5">
                Every rupee, explained.
              </h2>
              <p className="text-center max-w-lg mx-auto text-[16px] text-slate-400 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
                From raw billet to finished part. Costrich calculates every process, every cost line, every margin.
              </p>
            </ScrollReveal>

            <StaggerReveal className="grid md:grid-cols-2 gap-6">
              {PROCESS_STEPS.map((step, i) => (
                <StaggerItem key={step.title}>
                  <div className="group bg-white border border-slate-200/80 rounded-2xl overflow-hidden hover-lift hover:border-slate-300">
                    {/* Image with clip-path reveal */}
                    <div className="relative h-56 overflow-hidden">
                      <Image src={step.img} alt={step.title} fill className="object-cover hover-zoom" />
                      <div className="absolute inset-0 bg-gradient-to-t from-white via-transparent to-transparent" />
                      <div className="absolute top-4 left-4 w-8 h-8 bg-white/90 backdrop-blur-sm border border-slate-200 rounded-full flex items-center justify-center">
                        <span className="text-[13px] font-bold text-slate-900" style={{ fontFamily: "var(--font-mono)" }}>
                          {String(i + 1).padStart(2, "0")}
                        </span>
                      </div>
                      <div className="absolute top-4 right-4 bg-slate-900/90 backdrop-blur-sm rounded-full px-3 py-1.5">
                        <span className="text-[13px] font-bold text-white tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>
                          {step.cost}
                        </span>
                      </div>
                    </div>
                    <div className="p-6">
                      <p className="text-[12px] text-cyan-600 uppercase tracking-[0.25em] mb-2" style={{ fontFamily: "var(--font-mono)" }}>
                        {step.sub}
                      </p>
                      <h3 className="text-[18px] font-semibold text-slate-900 mb-2" style={{ fontFamily: "var(--font-sans)" }}>
                        {step.title}
                      </h3>
                      <p className="text-[14px] text-slate-400 leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>
                        {step.desc}
                      </p>
                    </div>
                  </div>
                </StaggerItem>
              ))}
            </StaggerReveal>

            {/* Total cost bar */}
            <ScrollReveal className="mt-8">
              <div className="bg-slate-900 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                  <span className="text-[14px] text-white/60" style={{ fontFamily: "var(--font-sans)" }}>
                    Total should-cost per unit (qty 100)
                  </span>
                </div>
                <div className="flex items-center gap-6">
                  <span className="text-[32px] font-bold text-white tabular-nums" style={{ fontFamily: "var(--font-mono)" }}>₹695</span>
                  <Link href="/login" className="px-6 py-2.5 bg-white text-slate-900 text-[13px] font-medium rounded-full hover:bg-slate-100 transition-all duration-200" style={{ fontFamily: "var(--font-sans)" }}>
                    Get your breakdown →
                  </Link>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            THE REVEAL — Clip-path cinematic image entrance
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32 bg-slate-900">
          <div className="max-w-5xl mx-auto px-6 lg:px-10 text-center">
            <ScrollReveal>
              <p className="mb-4 text-[13px] text-cyan-400 uppercase tracking-[0.3em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
                The Result
              </p>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(36px,6vw,64px)] text-white tracking-[-0.03em] leading-[1.05] mb-4">
                The Master Part.
              </h2>
              <p className="max-w-md mx-auto text-[17px] text-white/40 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
                Immaculate chrome finish. Precise geometry. Assembled, measured, and verified.
              </p>
            </ScrollReveal>

            <ScrollReveal>
              <div className="relative max-w-2xl mx-auto">
                <Image src="/assets/image_5.png" alt="Finished precision-machined shaft" width={1200} height={600} className="w-full h-auto rounded-2xl" />
              </div>
            </ScrollReveal>

            <ScrollReveal>
              <div className="mt-12 flex flex-wrap items-center justify-center gap-8">
                {[
                  ["Material", "EN8 Steel"],
                  ["Finish", "Hard Chrome"],
                  ["Tolerance", "±0.05mm"],
                  ["Processes", "Turn · Mill · Drill · Plate"],
                ].map(([label, val]) => (
                  <div key={label} className="text-center">
                    <p className="text-[12px] text-white/20 uppercase tracking-[0.2em] mb-1" style={{ fontFamily: "var(--font-mono)" }}>{label}</p>
                    <p className="text-[14px] text-white/60 font-medium" style={{ fontFamily: "var(--font-sans)" }}>{val}</p>
                  </div>
                ))}
              </div>
            </ScrollReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            COMPANY BRAIN — Image slides in from left
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <div className="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">

              <ScrollReveal direction="left">
                <div className="rounded-2xl overflow-hidden border border-slate-200/80 shadow-lg">
                  <Image src="/assets/image_6.png" alt="Engineer finding similar parts with Costrich" width={800} height={600} className="w-full h-auto" />
                </div>
              </ScrollReveal>

              <ScrollReveal direction="right">
                <div>
                  <p className="text-[13px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-4" style={{ fontFamily: "var(--font-mono)" }}>
                    Your Company&apos;s Brain
                  </p>

                  <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4vw,48px)] text-slate-900 tracking-[-0.02em] leading-tight mb-6">
                    Stop designing<br />from scratch.
                  </h2>

                  <p className="text-[16px] text-slate-400 leading-[1.8] mb-8" style={{ fontFamily: "var(--font-sans)" }}>
                    Thousands of drawings, POs, contracts, QA reports — buried across shared drives and inboxes.
                    Costrich turns them into one searchable brain. Upload a drawing,
                    find every similar part your company has ever made.
                  </p>

                  {/* Match preview */}
                  <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden mb-8">
                    <div className="px-5 py-2.5 border-b border-slate-100 flex items-center justify-between">
                      <span className="text-[12px] text-slate-300 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>Matches found</span>
                      <span className="text-[12px] text-cyan-600 font-medium" style={{ fontFamily: "var(--font-mono)" }}>3 results</span>
                    </div>
                    {[
                      { name: "Bracket-A4521", dept: "Design · Rajesh K.", match: 92, cost: "₹1,180" },
                      { name: "Mount-B2290", dept: "Procurement · Priya S.", match: 78, cost: "₹1,340" },
                      { name: "Flange-C0087", dept: "Quality · Amit P.", match: 65, cost: "₹890" },
                    ].map((item) => {
                      const color = item.match >= 80 ? "text-emerald-600" : item.match >= 60 ? "text-amber-600" : "text-slate-400";
                      return (
                        <div key={item.name} className="px-5 py-3 border-b border-slate-100 last:border-0 flex items-center justify-between">
                          <div>
                            <p className="text-[13px] font-medium text-slate-700" style={{ fontFamily: "var(--font-sans)" }}>{item.name}</p>
                            <p className="text-[12px] text-slate-300 mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>{item.dept} · {item.cost}</p>
                          </div>
                          <span className={`text-[13px] font-bold tabular-nums ${color}`} style={{ fontFamily: "var(--font-mono)" }}>{item.match}%</span>
                        </div>
                      );
                    })}
                  </div>

                  <Link href="/login" className="inline-flex px-7 py-3.5 bg-slate-900 text-white text-[14px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200" style={{ fontFamily: "var(--font-sans)" }}>
                    Search your drawings →
                  </Link>
                </div>
              </ScrollReveal>
            </div>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            EVERY DEPARTMENT — Staggered card entrance + hover lift
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <ScrollReveal>
              <p className="text-center mb-4 text-[13px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>
                One brain. Every department.
              </p>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] leading-tight mb-5">
                Stop reinventing what already exists.
              </h2>
              <p className="text-center max-w-xl mx-auto text-[16px] text-slate-400 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
                Your company has already designed, costed, and manufactured thousands of parts.
                Costrich makes that history searchable — for everyone.
              </p>
            </ScrollReveal>

            <StaggerReveal className="grid sm:grid-cols-2 gap-5" delayStep={80}>
              {[
                { dept: "Design", line: "Find if the part already exists. Skip three days of reinvention.", detail: "Search every drawing your company has ever made. Reuse tested, approved designs." },
                { dept: "Procurement", line: "Find what you paid last time. Never negotiate from zero.", detail: "Pull cost history for similar parts — material, supplier, price. Walk into negotiations with data." },
                { dept: "Quality", line: "Find supplier rejection history. Avoid repeat failures.", detail: "Trace similar parts back to tested designs. See which suppliers had first-article rejections." },
                { dept: "Sales", line: "Find previous contracts. Quote with historical advantage.", detail: "Pull pricing from past orders for similar parts. Quote faster, with margins you can defend." },
              ].map((item) => (
                <StaggerItem key={item.dept}>
                  <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8 hover-lift hover:border-cyan-200">
                    <p className="text-[12px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-4" style={{ fontFamily: "var(--font-mono)" }}>{item.dept}</p>
                    <p className="text-[17px] font-semibold text-slate-900 leading-snug mb-3" style={{ fontFamily: "var(--font-sans)" }}>{item.line}</p>
                    <p className="text-[14px] text-slate-400 leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>{item.detail}</p>
                  </div>
                </StaggerItem>
              ))}
            </StaggerReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            LIVE DEMO
            ════════════════════════════════════════════════════════ */}
        <section id="demo" className="py-24 lg:py-32">
          <div className="max-w-3xl mx-auto px-6">
            <ScrollReveal>
              <p className="text-center mb-4 text-[13px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Live example</p>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-4">
                This is the answer.
              </h2>
              <p className="text-center max-w-md mx-auto text-[15px] text-slate-400 leading-[1.7] mb-12" style={{ fontFamily: "var(--font-sans)" }}>
                Every cost line. Every assumption visible. Click any value to copy.
              </p>
            </ScrollReveal>
            <ScrollReveal>
              <CostBreakdownTable />
            </ScrollReveal>
            <p className="text-center mt-10">
              <Link href="/login" className="link-reveal text-[14px] font-medium text-cyan-600 hover:text-cyan-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>
                Get your own breakdown →
              </Link>
            </p>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            BEFORE / AFTER
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <ScrollReveal>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-center text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-16">
                Your team is negotiating blind.
              </h2>
            </ScrollReveal>
            <StaggerReveal className="grid md:grid-cols-2 gap-6" delayStep={100}>
              <StaggerItem>
                <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8">
                  <p className="text-[12px] text-red-400 uppercase tracking-[0.25em] font-medium mb-8" style={{ fontFamily: "var(--font-mono)" }}>Without Costrich</p>
                  <div className="space-y-5">
                    {["Call 3 suppliers. Wait 2 weeks.", "Negotiate on gut feel — no cost data.", "\"We made something like this once...\" — nobody can find it.", "Engineer retires. Knowledge walks out the door."].map((text) => (
                      <div key={text} className="flex items-start gap-3">
                        <span className="w-1 h-1 rounded-full bg-red-300 mt-[9px] shrink-0" />
                        <span className="text-[14px] text-slate-500 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </StaggerItem>
              <StaggerItem>
                <div className="bg-[#F7FBFA] border border-cyan-200/60 rounded-2xl p-8">
                  <p className="text-[12px] text-cyan-600 uppercase tracking-[0.25em] font-medium mb-8" style={{ fontFamily: "var(--font-mono)" }}>With Costrich</p>
                  <div className="space-y-5">
                    {["Upload a drawing. Answer in 60 seconds.", "Every cost line: material, machining, finishing, margin.", "Costrich finds similar parts from your entire history.", "Knowledge stays in the system. Searchable forever."].map((text) => (
                      <div key={text} className="flex items-start gap-3">
                        <span className="w-1 h-1 rounded-full bg-cyan-500 mt-[9px] shrink-0" />
                        <span className="text-[14px] text-slate-600 leading-[1.6]" style={{ fontFamily: "var(--font-sans)" }}>{text}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </StaggerItem>
            </StaggerReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            STATS
            ════════════════════════════════════════════════════════ */}
        <section className="py-24 lg:py-32">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <ScrollReveal>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] leading-tight mb-6">
                Every overpaid part compounds.
              </h2>
              <p className="max-w-lg mx-auto text-[16px] text-slate-400 leading-[1.7] mb-14" style={{ fontFamily: "var(--font-sans)" }}>
                200 parts a month. Overpaying 20% on half of them. That&apos;s lakhs per year — not because your team is bad, because they don&apos;t have the data.
              </p>
            </ScrollReveal>

            <StaggerReveal className="grid grid-cols-3 gap-4 max-w-xl mx-auto mb-8" delayStep={80}>
              {[
                { val: "164+", label: "Estimates run" },
                { val: "±5–10%", label: "Accuracy" },
                { val: "<60s", label: "Time to result" },
              ].map((s) => (
                <StaggerItem key={s.label}>
                  <div className="bg-white border border-slate-200/80 rounded-xl p-6 hover-lift">
                    <div className="text-[22px] font-bold text-slate-900 mb-1" style={{ fontFamily: "var(--font-mono)" }}>{s.val}</div>
                    <div className="text-[13px] text-slate-300 uppercase tracking-[0.15em]" style={{ fontFamily: "var(--font-mono)" }}>{s.label}</div>
                  </div>
                </StaggerItem>
              ))}
            </StaggerReveal>

            <ScrollReveal>
              <div className="bg-white border border-slate-200/80 rounded-xl p-6 max-w-sm mx-auto">
                <p className="text-[14px] text-slate-600 mb-1" style={{ fontFamily: "var(--font-sans)" }}>EN8 Steel Shaft — Ø50×100mm</p>
                <p className="text-[13px] text-slate-400 mb-2" style={{ fontFamily: "var(--font-sans)" }}>Supplier quoted ₹2,400 — should-cost ₹1,400</p>
                <span className="text-[15px] font-bold text-emerald-600" style={{ fontFamily: "var(--font-mono)" }}>42% savings identified</span>
              </div>
            </ScrollReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            PRICING
            ════════════════════════════════════════════════════════ */}
        <section id="pricing" className="py-24 lg:py-32 bg-white border-y border-slate-200/80">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <ScrollReveal>
              <p className="mb-4 text-[13px] text-cyan-600 uppercase tracking-[0.25em] font-medium" style={{ fontFamily: "var(--font-mono)" }}>Pricing</p>
              <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(28px,4.5vw,48px)] text-slate-900 tracking-[-0.02em] mb-4">
                Start free. Pay when it pays for itself.
              </h2>
              <p className="max-w-md mx-auto text-[15px] text-slate-400 leading-[1.7] mb-16" style={{ fontFamily: "var(--font-sans)" }}>
                One estimate that catches a 20% overpayment pays for a year of Pro.
              </p>
            </ScrollReveal>

            <StaggerReveal className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto text-left" delayStep={120}>
              <StaggerItem>
                <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8 hover-lift">
                  <p className="text-[12px] text-slate-400 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Free</p>
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
              </StaggerItem>

              <StaggerItem>
                <div className="bg-[#F8F8F6] border border-slate-200/80 rounded-2xl p-8 relative hover-lift">
                  <div className="absolute top-4 right-4 bg-amber-50 text-amber-600 text-[12px] px-2.5 py-1 rounded-full uppercase tracking-[0.2em] border border-amber-200 font-medium" style={{ fontFamily: "var(--font-mono)" }}>Coming soon</div>
                  <p className="text-[12px] text-slate-400 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Pro</p>
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
                  <button disabled className="block w-full text-center bg-slate-200 text-slate-400 px-6 py-3.5 rounded-full font-medium cursor-not-allowed text-[14px]" style={{ fontFamily: "var(--font-sans)" }}>
                    Join waitlist
                  </button>
                </div>
              </StaggerItem>
            </StaggerReveal>
          </div>
        </section>

        {/* ════════════════════════════════════════════════════════
            FINAL CTA
            ════════════════════════════════════════════════════════ */}
        <section className="py-28 lg:py-40">
          <ScrollReveal className="max-w-3xl mx-auto px-6 text-center">
            <h2 style={{ fontFamily: "var(--font-heading)" }} className="text-[clamp(36px,6vw,64px)] text-slate-900 tracking-[-0.03em] leading-[1.05] mb-8">
              Your AI cost analyst.<br />
              <span className="text-cyan-600 italic">Works while you negotiate.</span>
            </h2>
            <p className="max-w-md mx-auto text-[17px] text-slate-400 leading-[1.7] mb-12" style={{ fontFamily: "var(--font-sans)" }}>
              Costrich reads drawings like a senior analyst — breaks down every cost, searches your company&apos;s history, and gives you the answer in 60 seconds.
            </p>
            <Link href="/login" className="inline-flex px-9 py-4 bg-slate-900 text-white text-[15px] font-medium rounded-full hover:bg-slate-800 transition-all duration-200 hover:shadow-lg" style={{ fontFamily: "var(--font-sans)" }}>
              Upload your first drawing →
            </Link>
            <p className="mt-6 text-[12px] text-slate-300" style={{ fontFamily: "var(--font-mono)" }}>No credit card · No setup · Results in 60 seconds</p>
          </ScrollReveal>
        </section>

      </main>

      {/* ── Footer ────────────────────────────────────────────── */}
      <footer className="border-t border-slate-200/80 py-12 bg-white">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="flex flex-col md:flex-row justify-between items-start gap-10 mb-10">
            <div>
              <div className="flex items-center gap-2.5 mb-3">
                <Image src="/newton-metre-logo.png" alt="Costrich" width={32} height={32} className="rounded-xl" />
                <span style={{ fontFamily: "var(--font-heading)" }} className="text-[20px] text-cyan-600">Costrich</span>
              </div>
              <p className="text-[13px] text-slate-400 max-w-xs leading-[1.7]" style={{ fontFamily: "var(--font-sans)" }}>
                AI cost analyst + company memory for manufactured parts.
              </p>
            </div>
            <div className="flex gap-16">
              <div>
                <p className="text-[12px] text-slate-300 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Product</p>
                <div className="space-y-2">
                  {[["Process", "#process"], ["Pricing", "#pricing"]].map(([l, h]) => (
                    <a key={l} href={h} className="block link-reveal text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>{l}</a>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[12px] text-slate-300 uppercase tracking-[0.25em] mb-3" style={{ fontFamily: "var(--font-mono)" }}>Account</p>
                <div className="space-y-2">
                  <Link href="/login" className="block link-reveal text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Sign in</Link>
                  <Link href="/login" className="block link-reveal text-[13px] text-slate-400 hover:text-slate-700 transition-colors" style={{ fontFamily: "var(--font-sans)" }}>Get started</Link>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-slate-100 pt-6 text-[12px] text-slate-300 uppercase tracking-[0.2em]" style={{ fontFamily: "var(--font-mono)" }}>
            © 2026 Costrich
          </div>
        </div>
      </footer>
    </div>
  );
}
