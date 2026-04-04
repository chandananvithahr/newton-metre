"use client";

import Link from "next/link";
import { motion } from "motion/react";
import {
  FileText, Search, ArrowRight, CheckCircle2, BarChart3,
  ShieldCheck, Factory, Zap, IndianRupee, Layers,
} from "lucide-react";
import { LandingNav } from "@/components/landing-nav";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Base44-inspired landing
   Alternating white / gradient sections, curved dividers,
   green-to-orange logo, large centered headings
   ───────────────────────────────────────────────────────────── */

/* ── Curved SVG divider ──────────────────────────────────── */
function CurveDivider({ from, to }: { from: string; to: string }) {
  return (
    <div className="relative h-20 -mt-1" style={{ background: from }}>
      <svg
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        className="absolute bottom-0 w-full h-20"
      >
        <path
          d="M0,40 C360,80 1080,0 1440,40 L1440,80 L0,80 Z"
          fill={to}
        />
      </svg>
    </div>
  );
}

/* ── Hero ─────────────────────────────────────────────── */
function Hero() {
  return (
    <section className="pt-36 pb-28 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[900px] mx-auto text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>

          {/* Badge */}
          <div className="inline-flex items-center gap-3 px-5 py-2 rounded-full bg-white/80 text-[var(--color-brand-dark)] text-[11px] font-bold uppercase tracking-widest mb-8 border border-black/8 shadow-sm">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            Say hello to your Superagent
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-[56px] font-medium text-[var(--color-brand-dark)] leading-[1.08] tracking-tight mb-6" style={{ fontFamily: "var(--font-headline)" }}>
            Know what it <em className="text-orange-500">should</em> cost.
            <br />Before they quote.
          </h1>

          <p className="text-lg text-[var(--color-neutral-gray)] leading-relaxed max-w-xl mx-auto mb-10" style={{ fontFamily: "var(--font-body)" }}>
            Upload any manufacturing drawing. Get a line-by-line should-cost breakdown. Find similar parts from your history. Negotiate with data.
          </p>

          {/* Prompt-style input bar */}
          <div className="max-w-xl mx-auto mb-8">
            <div className="bg-white rounded-full shadow-lg shadow-black/5 border border-black/5 p-2 flex items-center gap-3">
              <span className="text-[var(--color-text-disabled)] text-sm pl-5 flex-1 text-left truncate" style={{ fontFamily: "var(--font-body)" }}>Upload a drawing to get a should-cost breakdown...</span>
              <Link
                href="/estimate/new"
                className="w-10 h-10 rounded-full bg-orange-500 hover:bg-orange-600 text-white flex items-center justify-center shrink-0 transition-colors"
              >
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>

          <p className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-[0.15em] font-medium mb-4" style={{ fontFamily: "var(--font-label)" }}>Not sure where to start? Try one of these:</p>
          <div className="flex flex-wrap justify-center gap-3">
            {["Should-Cost Estimate", "Similarity Search"].map((label) => (
              <Link
                key={label}
                href={label === "Similarity Search" ? "/similar" : "/estimate/new"}
                className="px-5 py-2.5 rounded-full border border-black/8 bg-white text-sm text-[var(--color-neutral-gray)] hover:bg-[#f9fafb] hover:border-black/15 transition-all"
                style={{ fontFamily: "var(--font-body)" }}
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
    <section className="py-28 bg-white">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] mb-6 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
            Engineering became precise.<br />
            <em className="text-[var(--color-text-disabled)]">Commercial negotiations never did.</em>
          </h2>
          <p className="text-lg text-[var(--color-neutral-gray)] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            Your engineers design to micron-level tolerances. But when procurement negotiates the price, they rely on PDFs from suppliers, old purchase orders, and gut feeling.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            { stat: "14%", label: "Average Overpayment", desc: "Procurement teams accept supplier quotes with no independent benchmark. On precision parts, the average overspend is 14%." },
            { stat: "40+", label: "Hours per Project", desc: "Engineers cross-reference old POs, call vendors, build spreadsheets. Weeks of work for a number that\u2019s still a guess." },
            { stat: "1", label: "Bad Quote Kills a Bid", desc: "In defense and aerospace, a wrong cost estimate doesn\u2019t just blow the budget \u2014 it loses the contract." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl bg-[#f9fafb] border border-black/5 h-full flex flex-col">
              <div className="text-4xl font-medium text-[var(--color-brand-dark)] mb-3" style={{ fontFamily: "var(--font-mono)" }}>{item.stat}</div>
              <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-label)" }}>{item.label}</div>
              <p className="text-[15px] text-[var(--color-neutral-gray)] leading-relaxed flex-1" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Should-Cost ──────────────────────────────────────── */
function ShouldCost() {
  return (
    <section id="capabilities" className="py-28 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <div className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-widest font-bold mb-6" style={{ fontFamily: "var(--font-mono)" }}>01 / 02 &middot; Should-Cost Engine</div>
            <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
              Upload a drawing.<br />
              <em>Get the real number.</em>
            </h2>
            <p className="text-lg text-[var(--color-neutral-gray)] leading-relaxed mb-10" style={{ fontFamily: "var(--font-body)" }}>
              Your supplier already knows what it costs to make your part. Now you will too. Newton-Metre gives you a line-by-line should-cost — material, machining, finishing, overhead — so you walk into every negotiation with the real number. Companies save 8-12% on the first quote they challenge.
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
            <div className="bg-[var(--color-brand-dark)] rounded-2xl p-6 text-white shadow-2xl">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                <div>
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1" style={{ fontFamily: "var(--font-label)" }}>Analysis: NM-9283</div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-widest" style={{ fontFamily: "var(--font-label)" }}>HIGH confidence</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1" style={{ fontFamily: "var(--font-label)" }}>Should-Cost</div>
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
                    <span className="text-sm text-white/50" style={{ fontFamily: "var(--font-body)" }}>{item.label}</span>
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
            { title: "Sourcing & Procurement", desc: "Your supplier quoted ₹48,000. The should-cost is ₹29,400. That\u2019s ₹18,600 back per part." },
            { title: "Cost Engineering", desc: "Should-cost in minutes, not days. Every line item defensible in an audit." },
            { title: "Design Engineering", desc: "See the cost impact of every design choice before it reaches procurement." },
            { title: "Leadership", desc: "See total overpayment across your supply base. Know which suppliers are competitive." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl border border-black/5 bg-white/80 hover:bg-white hover:border-black/15 transition-all group h-full flex flex-col">
              <CheckCircle2 className="w-6 h-6 text-emerald-500 mb-5" />
              <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest mb-3 group-hover:text-orange-600 transition-colors" style={{ fontFamily: "var(--font-label)" }}>{item.title}</div>
              <p className="text-[15px] text-[var(--color-neutral-gray)] leading-relaxed flex-1" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Similarity Search (dark section) ────────────── */
function SimilaritySearch() {
  return (
    <section className="py-28 bg-[var(--color-brand-dark)] text-white overflow-hidden relative">
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-orange-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-emerald-500/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/3" />

      <div className="max-w-[1200px] mx-auto px-4 sm:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <div className="text-white/40 text-[11px] font-bold uppercase tracking-widest mb-6" style={{ fontFamily: "var(--font-mono)" }}>02 / 02 &middot; Search Engine</div>
          <h2 className="text-4xl sm:text-5xl font-medium mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
            Your company already knows.<br />
            <em className="text-white/60">It just can&apos;t remember.</em>
          </h2>
          <p className="text-lg text-white/60 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
            10,000+ drawings in shared drives. Cost data in spreadsheets. Tribal knowledge in your senior engineer&apos;s head. When they retire, it all walks out the door. Newton-Metre makes your entire company history searchable in seconds.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-10">
            {[
              { dept: "Design & Engineering", title: "She spent 3 days designing a bracket. It already existed.", desc: "Your team has drawn 10,000+ parts. Find the one that\u2019s 90% similar, tweak 10%, and ship \u2014 in hours, not weeks." },
              { dept: "Sourcing & Procurement", title: "You paid ₹32,000 for this part last year. The supplier is quoting ₹48,000.", desc: "Every past PO, supplier contract, and price history \u2014 searchable. Know what you paid and where the leverage sits." },
              { dept: "Quality & Compliance", title: "When Rajesh retired, 20 years of inspection knowledge didn\u2019t leave with him.", desc: "Inspection reports, test results, material certs, failure histories \u2014 indexed and searchable by anyone, forever." },
              { dept: "Cost Engineering", title: "Benchmark every quote against your own data. In minutes.", desc: "Pull up historical should-costs for similar parts. Compare supplier quotes against what you actually paid." },
              { dept: "Manufacturing & Shop Floor", title: "Same geometry, same material. Here\u2019s the setup that worked last time.", desc: "Search past production records to find proven setups, cycle times, and tooling configs." },
            ].map((item, i) => (
              <div key={i} className="relative pl-8 border-l border-white/10 group hover:border-l-orange-400/50 transition-colors">
                <div className="text-[11px] font-bold text-white/40 uppercase tracking-widest mb-2" style={{ fontFamily: "var(--font-label)" }}>{item.dept}</div>
                <div className="text-xl font-bold mb-3" style={{ fontFamily: "var(--font-headline)" }}>{item.title}</div>
                <p className="text-white/60 text-[15px] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
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
                <span className="text-[11px] font-bold uppercase tracking-widest text-white/40" style={{ fontFamily: "var(--font-label)" }}>Search Results</span>
              </div>

              <div className="space-y-2">
                {[
                  { name: "Bracket_Assy_Rev3.pdf", type: "Manufacturing Drawing", match: "94%" },
                  { name: "Inspection_Report_Q3.pdf", type: "QA Certificate", match: "89%" },
                  { name: "PO_Supplier_Tata_2025.pdf", type: "Purchase Order", match: "85%" },
                  { name: "CNC_Setup_Sheet_M12.pdf", type: "Process Record", match: "82%" },
                ].map((item, i) => (
                  <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-all cursor-pointer flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium mb-0.5" style={{ fontFamily: "var(--font-mono)" }}>{item.name}</div>
                      <div className="text-[10px] text-white/30 uppercase tracking-widest" style={{ fontFamily: "var(--font-label)" }}>{item.type}</div>
                    </div>
                    <span className="text-xs font-bold text-emerald-400" style={{ fontFamily: "var(--font-mono)" }}>{item.match}</span>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <Link
                  href="/similar"
                  className="w-full py-4 rounded-full bg-white text-[var(--color-brand-dark)] text-xs font-bold uppercase tracking-widest hover:bg-white/90 transition-colors flex items-center justify-center gap-2"
                  style={{ fontFamily: "var(--font-label)" }}
                >
                  Search Your Company History <ArrowRight className="w-4 h-4" />
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
    <section className="py-28 px-4 sm:px-8 bg-white">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>
            One upload. <em>Five departments get answers.</em>
          </h2>
        </div>
        <p className="text-center text-lg text-[var(--color-neutral-gray)] leading-relaxed max-w-2xl mx-auto mb-20" style={{ fontFamily: "var(--font-body)" }}>
          Manufacturing companies lose 20-30% in revenue to disconnected data. Newton-Metre turns your scattered files into one searchable company brain.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { Icon: Factory, dept: "Engineering", work: "60% of your part numbers already exist. Find the match in seconds instead of designing from scratch." },
            { Icon: IndianRupee, dept: "Procurement", work: "Every past PO, price, and supplier quote — searchable. Walk into negotiations knowing what you paid last time." },
            { Icon: ShieldCheck, dept: "Quality", work: "When your senior QA lead retires, 20 years of inspection reports and material certs stay indexed." },
            { Icon: Layers, dept: "Shop Floor", work: "Same geometry, same material — here\u2019s the proven setup, cycle time, and tooling config from last time." },
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl border border-black/5 bg-[#f9fafb] hover:border-black/15 hover:bg-white transition-all group h-full flex flex-col">
              <div className="w-12 h-12 rounded-xl bg-white border border-black/5 flex items-center justify-center text-[var(--color-brand-dark)] mb-6 group-hover:logo-gradient group-hover:text-white transition-all">
                <item.Icon className="w-6 h-6" />
              </div>
              <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-label)" }}>{item.dept}</div>
              <p className="text-[15px] text-[var(--color-neutral-gray)] leading-relaxed flex-1" style={{ fontFamily: "var(--font-body)" }}>{item.work}</p>
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
    <section id="how-it-works" className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-6">
          <div className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-widest font-bold mb-4" style={{ fontFamily: "var(--font-label)" }}>How it works</div>
          <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>
            Five steps. <em>Drawing to negotiation.</em>
          </h2>
        </div>
        <p className="text-center text-lg text-[var(--color-neutral-gray)] max-w-xl mx-auto mb-20" style={{ fontFamily: "var(--font-body)" }}>
          From upload to cost breakdown in under 60 seconds.
        </p>

        <div className="grid md:grid-cols-5 gap-8">
          {[
            { step: "01", title: "Upload", desc: "Drop a manufacturing drawing \u2014 PDF, DXF, or image." },
            { step: "02", title: "Extract", desc: "AI reads dimensions, tolerances, material, and processes." },
            { step: "03", title: "Calculate", desc: "Line-by-line should-cost: material, machining, finishing, overhead." },
            { step: "04", title: "Validate", desc: "Compared against every similar part your company has ever made." },
            { step: "05", title: "Negotiate", desc: "Walk in with the number. Save 8-12% on the first quote." },
          ].map((item, i) => (
            <div key={i} className="relative group text-center">
              <div className="text-6xl font-bold text-[var(--color-brand-dark)]/10 mb-4 group-hover:text-orange-500/30 transition-colors" style={{ fontFamily: "var(--font-mono)" }}>{item.step}</div>
              <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-label)" }}>{item.title}</div>
              <p className="text-[15px] text-[var(--color-neutral-gray)] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
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
    <section className="py-28 px-4 sm:px-8 bg-white">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div>
            <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] mb-8 tracking-tight leading-tight" style={{ fontFamily: "var(--font-headline)" }}>
              Built for the <br />
              <em>Indian Manufacturing Renaissance.</em>
            </h2>
            <p className="text-lg text-[var(--color-neutral-gray)] leading-relaxed mb-10" style={{ fontFamily: "var(--font-body)" }}>
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
                  <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest mb-1.5" style={{ fontFamily: "var(--font-label)" }}>{item.label}</div>
                  <p className="text-[15px] text-[var(--color-neutral-gray)]" style={{ fontFamily: "var(--font-body)" }}>{item.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#f9fafb] rounded-2xl p-10 border border-black/5">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-12 h-12 rounded-lg logo-gradient flex items-center justify-center text-white">
                <Zap className="w-6 h-6" />
              </div>
              <div className="text-[11px] font-bold text-[var(--color-brand-dark)] uppercase tracking-widest" style={{ fontFamily: "var(--font-label)" }}>Results from Real Users</div>
            </div>
            <div className="space-y-5">
              <div className="p-6 rounded-xl bg-white border border-black/5">
                <div className="text-[11px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-label)" }}>Market Insight</div>
                <div className="text-[15px] text-[var(--color-brand-dark)] leading-relaxed font-medium" style={{ fontFamily: "var(--font-body)" }}>
                  &ldquo;Newton-Metre identified a 12% cost variance in our Pune-based suppliers vs. Bangalore for the same part family.&rdquo;
                </div>
              </div>
              <div className="p-6 rounded-xl bg-white border border-black/5">
                <div className="text-[11px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest mb-3" style={{ fontFamily: "var(--font-label)" }}>Design Reuse</div>
                <div className="text-[15px] text-[var(--color-brand-dark)] leading-relaxed font-medium" style={{ fontFamily: "var(--font-body)" }}>
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

/* ── Pricing ───────────────────────────────────────────── */
function Pricing() {
  return (
    <section id="pricing" className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-3 gap-8 items-stretch">
          {/* Left: heading */}
          <div className="flex flex-col justify-center">
            <h2 className="text-4xl sm:text-5xl font-medium text-[var(--color-brand-dark)] tracking-tight mb-4" style={{ fontFamily: "var(--font-headline)" }}>
              Pricing plans<br />for every need
            </h2>
            <p className="text-[15px] text-[var(--color-neutral-gray)] leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
              One corrected quote pays for a year. Everything after that is pure savings.
            </p>
          </div>

          {/* Free */}
          <div className="p-8 rounded-2xl bg-white border border-black/5 h-full flex flex-col">
            <div className="text-[11px] font-bold uppercase tracking-widest text-[var(--color-brand-dark)] mb-6" style={{ fontFamily: "var(--font-label)" }}>Start for free</div>
            <p className="text-[15px] text-[var(--color-neutral-gray)] mb-6" style={{ fontFamily: "var(--font-body)" }}>Get access to:</p>
            <ul className="space-y-3 mb-8">
              {["10 estimates / month", "Should-cost breakdown", "Similarity search", "PDF & image uploads"].map((f) => (
                <li key={f} className="flex items-center gap-2.5 text-[15px] text-[var(--color-neutral-gray)]" style={{ fontFamily: "var(--font-body)" }}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link href="/login" className="dark-pill block w-full py-3.5 text-xs font-bold uppercase tracking-widest text-center mt-auto" style={{ fontFamily: "var(--font-label)" }}>
              Start building
            </Link>
          </div>

          {/* Pro */}
          <div className="p-8 rounded-2xl warm-gradient-accent border border-black/5 relative overflow-hidden h-full flex flex-col">
            <div className="text-[11px] font-bold uppercase tracking-widest text-[var(--color-brand-dark)] mb-2" style={{ fontFamily: "var(--font-label)" }}>Paid plans from</div>
            <div className="flex items-baseline gap-1 mb-6">
              <span className="text-4xl font-medium text-[var(--color-brand-dark)]" style={{ fontFamily: "var(--font-mono)" }}>₹4,999</span>
              <span className="text-xs text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-body)" }}>/mo</span>
            </div>
            <p className="text-[15px] text-[var(--color-neutral-gray)] mb-6" style={{ fontFamily: "var(--font-body)" }}>Upgrade as you go for more credits, more features, and more support.</p>
            <Link href="/login?waitlist=pro" className="block w-full py-3.5 rounded-full border border-black/8 text-xs font-bold uppercase tracking-widest text-center text-[var(--color-brand-dark)] hover:bg-white/60 transition-colors mt-auto" style={{ fontFamily: "var(--font-label)" }}>
              See all plans
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── CTA Banner ──────────────────────────────────────── */
function CtaBanner() {
  return (
    <section className="py-20 px-4 sm:px-8 warm-gradient-footer relative overflow-hidden">
      <div className="absolute top-0 left-[20%] w-[300px] h-[300px] bg-orange-400/30 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-[20%] w-[400px] h-[400px] bg-orange-500/20 rounded-full blur-3xl" />
      <div className="max-w-[600px] mx-auto text-center relative z-10">
        <div className="bg-[#fefce8]/90 backdrop-blur-sm rounded-2xl px-10 py-10 border border-black/5">
          <h2 className="text-3xl sm:text-4xl font-medium text-[var(--color-brand-dark)] mb-4 tracking-tight" style={{ fontFamily: "var(--font-headline)" }}>
            So, what are we building?
          </h2>
          <Link
            href="/estimate/new"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-white text-xs font-bold uppercase tracking-widest transition-colors"
            style={{ background: "linear-gradient(135deg, #059669, #10b981)" }}
          >
            Get started <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </section>
  );
}

/* ── Footer ───────────────────────────────────────────── */
function Footer() {
  return (
    <footer className="py-16 px-4 sm:px-8 warm-gradient-footer relative overflow-hidden">
      <div className="max-w-[1200px] mx-auto relative z-10">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          <div>
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="relative w-9 h-9 flex items-center justify-center">
                <div className="absolute inset-0 logo-gradient rounded-xl" />
                <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
              </div>
              <span className="text-[var(--color-brand-dark)] text-lg font-semibold" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>Newton-Metre</span>
            </div>
            <p className="text-[15px] text-[var(--color-brand-dark)]/60 leading-relaxed text-center" style={{ fontFamily: "var(--font-body)" }}>
              Know what it costs, before they quote.
            </p>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[var(--color-brand-dark)] mb-4" style={{ fontFamily: "var(--font-label)" }}>Company</div>
            <ul className="space-y-2.5">
              <li><a href="mailto:chand@costimize.dev" className="text-[15px] text-[var(--color-brand-dark)]/60 hover:text-[var(--color-brand-dark)] transition-colors" style={{ fontFamily: "var(--font-body)" }}>Contact Us</a></li>
            </ul>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[var(--color-brand-dark)] mb-4" style={{ fontFamily: "var(--font-label)" }}>Product</div>
            <ul className="space-y-2.5">
              {[
                { label: "Should-Cost", href: "/estimate/new" },
                { label: "Similarity Search", href: "/similar" },
              ].map((item) => (
                <li key={item.label}><Link href={item.href} className="text-[15px] text-[var(--color-brand-dark)]/60 hover:text-[var(--color-brand-dark)] transition-colors" style={{ fontFamily: "var(--font-body)" }}>{item.label}</Link></li>
              ))}
            </ul>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[var(--color-brand-dark)] mb-4" style={{ fontFamily: "var(--font-label)" }}>Legal</div>
            <ul className="space-y-2.5">
              <li><a href="mailto:chand@costimize.dev" className="text-[15px] text-[var(--color-brand-dark)]/60 hover:text-[var(--color-brand-dark)] transition-colors" style={{ fontFamily: "var(--font-body)" }}>Contact</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-[#1a1a1a]/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-[var(--color-brand-dark)]/40" style={{ fontFamily: "var(--font-body)" }}>&copy; 2026 Newton-Metre. Should-cost in minutes, not meetings.</div>
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
        <CurveDivider from="#e2f6ec" to="#ffffff" />
        <Problem />
        <CurveDivider from="#ffffff" to="#e8fdf5" />
        <ShouldCost />
        {/* No curve before dark section — clean edge */}
        <SimilaritySearch />
        {/* No curve after dark section — clean edge */}
        <SiloBreaker />
        <CurveDivider from="#ffffff" to="#dff7ee" />
        <HowItWorks />
        <CurveDivider from="#e8f4ee" to="#ffffff" />
        <BuiltForIndia />
        <CurveDivider from="#ffffff" to="#dff7ee" />
        <Pricing />
        <CtaBanner />
      </main>
      <Footer />
    </div>
  );
}
