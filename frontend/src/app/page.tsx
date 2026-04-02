"use client";

import Link from "next/link";
import { motion } from "motion/react";
import {
  FileText, Search, ArrowRight, CheckCircle2, BarChart3,
  ShieldCheck, Factory, Zap, IndianRupee, Layers,
} from "lucide-react";
import { LandingNav } from "@/components/landing-nav";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Base44-inspired warm redesign
   Warm gradients, big serif headlines, dark pill CTAs,
   generous whitespace, confident editorial tone
   ───────────────────────────────────────────────────────────── */

/* ── Hero ─────────────────────────────────────────────── */
function Hero() {
  return (
    <section className="pt-36 pb-24 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <div className="inline-flex items-center gap-3 px-6 py-2.5 rounded-full bg-white/70 backdrop-blur-sm text-[#1a1a1a] text-sm font-bold uppercase tracking-widest mb-10 border border-black/10 shadow-sm">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            Precision Sourcing Intelligence
          </div>

          <div className="max-w-3xl mx-auto mb-12 space-y-8">
            <div>
              <h1 className="text-4xl sm:text-5xl lg:text-[64px] font-medium text-[#1a1a1a] leading-[1.1] tracking-tight mb-4" style={{ fontFamily: "var(--font-headline)" }}>
                Know what it <em className="text-orange-500">should</em> cost.
              </h1>
              <p className="text-[#374151] text-lg leading-relaxed">
                Upload any manufacturing drawing. Get a line-by-line breakdown of material, machining, and finishing costs. Negotiate with the real number.
              </p>
            </div>
            <div>
              <h1 className="text-4xl sm:text-5xl lg:text-[64px] font-medium text-[#1a1a1a] leading-[1.1] tracking-tight mb-4" style={{ fontFamily: "var(--font-headline)" }}>
                Find where it <em className="text-orange-500">already</em> exists.
              </h1>
              <p className="text-[#374151] text-lg leading-relaxed">
                Search your company&apos;s entire history — find similar parts, specs, and contracts in seconds. Stop reinventing the wheel.
              </p>
            </div>
          </div>

          {/* Prompt-style input bar (Base44 inspired) */}
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-white rounded-full shadow-lg shadow-black/5 border border-black/5 p-2 flex items-center gap-3">
              <span className="text-[#9ca3af] text-sm pl-5 flex-1 text-left truncate">Upload a drawing to get a should-cost breakdown...</span>
              <Link
                href="/estimate/new"
                className="dark-pill px-6 py-3 text-xs font-bold uppercase tracking-widest flex items-center gap-2 shrink-0"
              >
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>

          <div className="text-[11px] text-[#374151] uppercase tracking-widest font-bold mb-4">Not sure where to start? Try one of these:</div>
          <div className="flex flex-wrap justify-center gap-3">
            {["Should-Cost Estimate", "Similarity Search"].map((label) => (
              <Link
                key={label}
                href={label === "Similarity Search" ? "/similar" : "/estimate/new"}
                className="px-5 py-2.5 rounded-full border border-black/10 bg-white/60 text-sm text-[#374151] hover:bg-white hover:border-black/20 transition-all"
              >
                {label}
              </Link>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/* ── Problem ──────────────────────────────────────────── */
function Problem() {
  return (
    <section className="py-28 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8">
        <div className="max-w-2xl mb-20">
          <h2 className="text-4xl sm:text-5xl font-medium text-[#1a1a1a] mb-6 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
            Engineering became precise.<br />
            <em className="text-[#9ca3af]">Commercial negotiations never did.</em>
          </h2>
          <p className="text-[#374151] text-lg leading-relaxed">
            Your engineers design to micron-level tolerances. But when procurement negotiates the price, they rely on PDFs from suppliers, old purchase orders, and gut feeling.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            { stat: "14%", label: "Average Overpayment", desc: "Procurement teams accept supplier quotes with no independent benchmark. On precision parts, the average overspend is 14%." },
            { stat: "40+", label: "Hours per Project", desc: "Engineers cross-reference old POs, call vendors, build spreadsheets. Weeks of work for a number that\u2019s still a guess." },
            { stat: "1", label: "Bad Quote Kills a Bid", desc: "In defense and aerospace, a wrong cost estimate doesn\u2019t just blow the budget \u2014 it loses the contract." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl bg-white/80 border border-black/10 h-full flex flex-col">
              <div className="text-4xl font-medium text-[#1a1a1a] mb-3" style={{ fontFamily: "var(--font-mono)" }}>{item.stat}</div>
              <div className="text-xs font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">{item.label}</div>
              <p className="text-sm text-[#374151] leading-relaxed flex-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Should-Cost (with step counter) ──────────────────── */
function ShouldCost() {
  return (
    <section id="capabilities" className="py-28 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <div className="text-sm text-[#1a1a1a]/60 uppercase tracking-widest font-bold mb-6" style={{ fontFamily: "var(--font-mono)" }}>01 / 02 &middot; Should-Cost Intelligence</div>
            <h2 className="text-4xl sm:text-5xl font-medium text-[#1a1a1a] mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
              Upload a drawing.<br />
              <em>Get the real number.</em>
            </h2>
            <p className="text-[#1a1a1a] text-lg leading-relaxed mb-10 font-medium">
              Newton-Metre gives you a complete should-cost breakdown — material, machining, finishing, setup, overhead, and margin — line by line. No spreadsheets. No guessing. One number your entire team can act on.
            </p>
            <Link href="/estimate/new" className="dark-pill inline-flex items-center gap-2 px-8 py-4 text-xs font-bold uppercase tracking-widest">
              Upload a Drawing <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Preview card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-[#1a1a1a] rounded-2xl p-6 text-white shadow-2xl">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                <div>
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1">Analysis: NM-9283</div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-widest">HIGH confidence</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1">Should-Cost</div>
                  <div className="text-2xl font-medium tracking-tighter" style={{ fontFamily: "var(--font-mono)" }}>₹ 14,820</div>
                </div>
              </div>

              <div className="space-y-4">
                {[
                  { label: "Material (Al 6061-T6)", value: "2,340", pct: 28 },
                  { label: "CNC Turning", value: "4,180", pct: 50 },
                  { label: "CNC Milling", value: "3,260", pct: 39 },
                  { label: "Setup & Tooling", value: "1,840", pct: 22 },
                  { label: "Overhead + Margin", value: "3,200", pct: 38 },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="text-sm text-white/50">{item.label}</span>
                    <div className="flex items-center gap-3">
                      <div className="w-24 h-1 bg-white/10 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          whileInView={{ width: `${item.pct}%` }}
                          viewport={{ once: true }}
                          transition={{ duration: 1, delay: 0.3 + i * 0.1 }}
                          className="h-full bg-orange-400/60 rounded-full"
                        />
                      </div>
                      <span className="text-sm text-white/80 w-16 text-right" style={{ fontFamily: "var(--font-mono)" }}>₹ {item.value}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Audience cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-20">
          {[
            { title: "Sourcing & Procurement", desc: "Challenge inflated quotes with a defensible, line-by-line breakdown." },
            { title: "Cost Engineering", desc: "Generate should-cost estimates in minutes, not days." },
            { title: "Design Engineering", desc: "See the cost impact of design choices before they reach procurement." },
            { title: "Leadership", desc: "Visibility into what you pay vs. what you should pay." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-xl border border-black/10 bg-white/80 hover:bg-white hover:border-black/20 transition-all group h-full flex flex-col">
              <CheckCircle2 className="w-6 h-6 text-emerald-500 mb-5" />
              <div className="text-sm font-bold text-[#1a1a1a] uppercase tracking-widest mb-3 group-hover:text-orange-600 transition-colors">{item.title}</div>
              <p className="text-base text-[#374151] leading-relaxed flex-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Similarity Search (warm dark section) ────────────── */
function SimilaritySearch() {
  return (
    <section className="py-28 bg-[#1a1a1a] text-white overflow-hidden relative">
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-orange-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-amber-500/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/3" />

      <div className="max-w-[1200px] mx-auto px-4 sm:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <div className="text-white/50 text-sm font-bold uppercase tracking-widest mb-6" style={{ fontFamily: "var(--font-mono)" }}>02 / 02 &middot; Universal Intelligence</div>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-medium mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
            One Search. <br />
            <em className="text-white/60">The Entire Company Database.</em>
          </h2>
          <p className="text-lg text-white/70 leading-relaxed">
            Every department creates knowledge. Most of it gets buried in folders, lost when people leave, or duplicated across teams. Newton-Metre indexes everything and makes it searchable in seconds.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-10">
            {[
              { dept: "Design & Engineering", title: "Stop redesigning what already exists", desc: "Your team has drawn 10,000+ parts over the years. Find the one that\u2019s 90% similar, tweak 10%, and ship \u2014 in hours, not weeks." },
              { dept: "Sourcing & Procurement", title: "Never negotiate blind again", desc: "Search across supplier contracts, POs, and price histories. Know what you paid last time, what the market rate is, and where the leverage sits." },
              { dept: "Quality & Compliance", title: "Institutional memory that never retires", desc: "When a senior QA lead leaves, their 20 years of inspection reports, test results, and material certs stay indexed and searchable." },
              { dept: "Cost Engineering", title: "Benchmark every quote in minutes", desc: "Pull up historical should-costs for similar parts. Compare supplier quotes against your own data instead of gut feeling." },
              { dept: "Manufacturing & Shop Floor", title: "Right process, right machine, first time", desc: "Search past production records to find proven setups, cycle times, and tooling configs for similar geometries." },
            ].map((item, i) => (
              <div key={i} className="relative pl-8 border-l border-white/10 group hover:border-l-orange-400/50 transition-colors">
                <div className="text-sm font-bold text-white/50 uppercase tracking-widest mb-2">{item.dept}</div>
                <div className="text-xl font-bold mb-3">{item.title}</div>
                <p className="text-white/70 text-base leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                  <Search className="w-4 h-4 text-white/60" />
                </div>
                <span className="text-xs font-bold uppercase tracking-widest text-white/40">Search Results</span>
              </div>

              <div className="space-y-2">
                {[
                  { name: "Shaft_Assy_Rev3.pdf", type: "Technical Drawing", match: "94%" },
                  { name: "Stress_Test_2025.pdf", type: "QA Report", match: "89%" },
                  { name: "Master_SLA_v4.docx", type: "Supplier Contract", match: "85%" },
                  { name: "Cost_Analysis_Q3.xlsx", type: "Finance Report", match: "82%" },
                ].map((item, i) => (
                  <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-all cursor-pointer flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium mb-0.5" style={{ fontFamily: "var(--font-mono)" }}>{item.name}</div>
                      <div className="text-[10px] text-white/30 uppercase tracking-widest">{item.type}</div>
                    </div>
                    <span className="text-xs font-bold text-emerald-400">{item.match}</span>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <Link
                  href="/similar"
                  className="w-full py-4 rounded-full bg-white text-[#1a1a1a] text-xs font-bold uppercase tracking-widest hover:bg-white/90 transition-colors flex items-center justify-center gap-2"
                >
                  Search Your Company Brain <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

/* ── Silo Breaker ─────────────────────────────────────── */
function SiloBreaker() {
  return (
    <section className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-20">
          <h2 className="text-4xl sm:text-5xl font-medium text-[#1a1a1a] tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>
            One Brain. <em>Every Department.</em>
          </h2>
        </div>

        <div className="grid md:grid-cols-4 gap-6">
          {[
            { Icon: Factory, dept: "Engineering", work: "Reuse 90% of existing designs. Stop reinventing the bracket." },
            { Icon: BarChart3, dept: "Marketing", work: "Extract insights from past campaigns and market strategy docs." },
            { Icon: IndianRupee, dept: "Sales", work: "Quote with confidence using historical cost and sales data." },
            { Icon: ShieldCheck, dept: "Quality", work: "Access every testing report and QA doc ever produced." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl border border-black/10 bg-white/80 hover:border-black/20 hover:bg-white transition-all group h-full flex flex-col">
              <div className="w-12 h-12 rounded-xl bg-[#fafafa] border border-black/5 flex items-center justify-center text-[#1a1a1a] mb-6 group-hover:bg-[#1a1a1a] group-hover:text-white transition-all">
                <item.Icon className="w-6 h-6" />
              </div>
              <div className="text-sm font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">{item.dept}</div>
              <p className="text-base text-[#374151] leading-relaxed flex-1">{item.work}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── How It Works ─────────────────────────────────────── */
function HowItWorks() {
  return (
    <section id="how-it-works" className="py-28 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-20">
          <h2 className="text-4xl sm:text-5xl font-medium text-[#1a1a1a] tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>
            Five steps. <em>Drawing to negotiation.</em>
          </h2>
        </div>

        <div className="grid md:grid-cols-5 gap-8">
          {[
            { step: "01", title: "Upload", desc: "Drop any file \u2014 Drawing, PDF, Contract, or Report." },
            { step: "02", title: "Extract", desc: "AI reads dimensions, terms, specs, and context." },
            { step: "03", title: "Calculate", desc: "Every cost and insight computed independently." },
            { step: "04", title: "Validate", desc: "Cross-checked against history and AI benchmarks." },
            { step: "05", title: "Negotiate", desc: "Hand the data-backed breakdown to stakeholders." },
          ].map((item, i) => (
            <div key={i} className="relative group text-center">
              <div className="text-6xl font-bold text-[#1a1a1a]/20 mb-4 group-hover:text-orange-500/40 transition-colors" style={{ fontFamily: "var(--font-mono)" }}>{item.step}</div>
              <div className="text-sm font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">{item.title}</div>
              <p className="text-base text-[#374151] leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Built for India ──────────────────────────────────── */
function BuiltForIndia() {
  return (
    <section className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <h2 className="text-4xl sm:text-5xl font-medium text-[#1a1a1a] mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
              Built for the <br />
              <em>Indian Manufacturing Renaissance.</em>
            </h2>
            <p className="text-[#1a1a1a] text-lg leading-relaxed mb-10 font-medium">
              Western tools use Western approximations. Newton-Metre is built on the ground truth of Indian economics — MSME labour rates, regional machine hour rates, BIS standards, and INR material pricing.
            </p>
            <div className="grid grid-cols-2 gap-8">
              {[
                { label: "BIS Standards", desc: "Native support for Indian steel grades." },
                { label: "Regional Rates", desc: "15+ Indian industrial hubs calibrated." },
                { label: "INR Native", desc: "Material pricing in Indian Rupees." },
                { label: "MSME Ready", desc: "Built for Indian workshop economics." },
              ].map((item, i) => (
                <div key={i}>
                  <div className="text-sm font-bold text-[#1a1a1a] uppercase tracking-widest mb-1.5">{item.label}</div>
                  <p className="text-base text-[#374151]">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white/80 rounded-2xl p-10 border border-black/10">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-12 h-12 rounded-lg bg-[#1a1a1a] flex items-center justify-center text-white">
                <Zap className="w-6 h-6" />
              </div>
              <div className="text-sm font-bold text-[#1a1a1a] uppercase tracking-widest">Strategic Intelligence</div>
            </div>
            <div className="space-y-5">
              <div className="p-6 rounded-xl bg-white border border-black/5">
                <div className="text-xs font-bold text-[#1a1a1a]/50 uppercase tracking-widest mb-3">Market Insight</div>
                <div className="text-base text-[#1a1a1a] leading-relaxed font-medium">
                  &ldquo;Newton-Metre identified a 12% cost variance in our Pune-based suppliers vs. Bangalore for the same part family.&rdquo;
                </div>
              </div>
              <div className="p-6 rounded-xl bg-white border border-black/5">
                <div className="text-xs font-bold text-[#1a1a1a]/50 uppercase tracking-widest mb-3">Design Reuse</div>
                <div className="text-base text-[#1a1a1a] leading-relaxed font-medium">
                  &ldquo;By indexing our 10-year drawing history, we reduced new part design time by 85% in the first quarter.&rdquo;
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Pricing (Base44 style) ───────────────────────────── */
function Pricing() {
  return (
    <section id="pricing" className="py-28 px-4 sm:px-8 warm-gradient-hero border-t border-black/5">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-3 gap-8 items-end">
          {/* Left: heading */}
          <div>
            <h2 className="text-4xl font-medium text-[#1a1a1a] tracking-tight mb-4" style={{ fontFamily: "var(--font-headline)" }}>
              Pricing plans<br />for every need
            </h2>
            <p className="text-base text-[#374151] leading-relaxed">
              Scale as you go with plans designed to match your growth.
            </p>
          </div>

          {/* Free */}
          <div className="p-8 rounded-2xl bg-white/80 border border-black/10 h-full flex flex-col">
            <div className="text-sm font-bold uppercase tracking-widest text-[#1a1a1a] mb-6">Start for free</div>
            <p className="text-sm text-[#374151] mb-6">Get access to:</p>
            <ul className="space-y-3 mb-8">
              {["10 estimates / month", "Should-cost breakdown", "Similarity search", "PDF & image uploads"].map((f) => (
                <li key={f} className="flex items-center gap-2.5 text-sm text-[#374151]">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link href="/login" className="dark-pill block w-full py-3.5 text-xs font-bold uppercase tracking-widest text-center">
              Start building
            </Link>
          </div>

          {/* Pro */}
          <div className="p-8 rounded-2xl warm-gradient-accent border border-black/10 relative overflow-hidden h-full flex flex-col">
            <div className="text-sm font-bold uppercase tracking-widest text-[#1a1a1a] mb-2">Paid plans from</div>
            <div className="flex items-baseline gap-1 mb-6">
              <span className="text-4xl font-medium text-[#1a1a1a]" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</span>
              <span className="text-xs text-[#6b7280]">/mo</span>
            </div>
            <p className="text-sm text-[#374151] mb-6">Upgrade as you go for more credits, more features, and more support.</p>
            <Link href="/login?waitlist=pro" className="block w-full py-3.5 rounded-full border border-black/10 text-xs font-bold uppercase tracking-widest text-center text-[#1a1a1a] hover:bg-white/60 transition-colors">
              See all plans
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Footer (warm gradient) ───────────────────────────── */
function Footer() {
  return (
    <footer className="py-16 px-4 sm:px-8 warm-gradient-footer relative overflow-hidden">
      <div className="max-w-[1200px] mx-auto relative z-10">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="relative w-9 h-9 flex items-center justify-center">
                <div className="absolute inset-0 bg-[#1a1a1a] rounded-xl" />
                <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
              </div>
              <span className="text-[#1a1a1a] text-lg font-semibold" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>Newton-Metre</span>
            </div>
            <p className="text-sm text-[#1a1a1a]/60 leading-relaxed">
              Precision Sourcing Intelligence for manufacturing. Know what it costs, before they quote.
            </p>
          </div>

          <div>
            <div className="text-xs font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">Company</div>
            <ul className="space-y-2.5">
              {["About Us", "Careers"].map((item) => (
                <li key={item}><a href="#" className="text-sm text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors">{item}</a></li>
              ))}
            </ul>
          </div>

          <div>
            <div className="text-xs font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">Product</div>
            <ul className="space-y-2.5">
              {[
                { label: "Should-Cost", href: "/estimate/new" },
                { label: "Similarity Search", href: "/similar" },
              ].map((item) => (
                <li key={item.label}><Link href={item.href} className="text-sm text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors">{item.label}</Link></li>
              ))}
            </ul>
          </div>

          <div>
            <div className="text-xs font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">Legal</div>
            <ul className="space-y-2.5">
              {["Privacy Policy", "Terms of Service"].map((item) => (
                <li key={item}><a href="#" className="text-sm text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors">{item}</a></li>
              ))}
              <li><a href="mailto:chand@costimize.dev" className="text-sm text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-[#1a1a1a]/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-xs text-[#1a1a1a]/40">&copy; 2026 Newton-Metre. Precision Sourcing Intelligence.</div>
        </div>
      </div>
    </footer>
  );
}

/* ── Page ──────────────────────────────────────────────── */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <LandingNav />
      <main>
        <Hero />
        <Problem />
        <ShouldCost />
        <SimilaritySearch />
        <SiloBreaker />
        <HowItWorks />
        <BuiltForIndia />
        <Pricing />
      </main>
      <Footer />
    </div>
  );
}
