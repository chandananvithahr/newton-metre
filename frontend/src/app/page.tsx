"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { ArrowRight, CheckCircle2, Search } from "lucide-react";
import { LandingNav } from "@/components/landing-nav";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Landing page
   Clean sections, white/gray/dark palette, Space Grotesk only
   ───────────────────────────────────────────────────────────── */

/* ── Hero ─────────────────────────────────────────────── */
function HeroCard({
  children,
  delay,
}: {
  children: React.ReactNode;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
      whileHover={{ y: -6, transition: { duration: 0.25 } }}
    >
      {children}
    </motion.div>
  );
}

function Hero() {
  return (
    <section className="pt-36 pb-28 px-4 sm:px-8 warm-gradient-hero">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="max-w-[720px] mx-auto text-center mb-14">
          <h1 className="text-5xl lg:text-[64px] font-bold text-[#1a1a1a] leading-[1.08] tracking-tight">
            Know what it costs.
            <br />
            Before they quote.
          </h1>
        </div>
      </motion.div>

      {/* Three product cards — staggered entrance */}
      <div className="grid sm:grid-cols-3 gap-6 max-w-[1100px] mx-auto text-left">

        {/* Should-Cost */}
        <HeroCard delay={0.3}>
          <Link
            href="/estimate/new"
            className="group flex flex-col h-full bg-white/80 backdrop-blur-sm border border-black/6 rounded-2xl p-8 sm:p-10 hover:bg-white hover:shadow-xl hover:shadow-black/5 hover:border-black/10 transition-all duration-300"
          >
            <div className="w-12 h-12 logo-gradient rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
            </div>
            <div className="text-[17px] font-bold text-[#1a1a1a] mb-1.5">Should-Cost</div>
            <p className="text-[13px] font-medium text-[#525252] mb-5">Instant cost breakdown from any drawing</p>
            <ul className="space-y-3 mb-6 flex-1">
              {[
                "Upload DWG, DXF, STEP, or PDF",
                "Every manufacturing process breakdown",
                "Negotiation-ready in 30 seconds",
                "Save 15–20% on every item",
              ].map((point) => (
                <li key={point} className="flex items-start gap-2.5 text-[14px] text-[#525252]">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#1a1a1a]/25 shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
            <span className="text-[11px] text-[#1a1a1a] font-bold uppercase tracking-widest group-hover:underline inline-flex items-center gap-1.5 group-hover:gap-2.5 transition-all">
              Upload a drawing <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </Link>
        </HeroCard>

        {/* Similarity Search */}
        <HeroCard delay={0.45}>
          <Link
            href="/similar"
            className="group flex flex-col h-full bg-white/80 backdrop-blur-sm border border-black/6 rounded-2xl p-8 sm:p-10 hover:bg-white hover:shadow-xl hover:shadow-black/5 hover:border-black/10 transition-all duration-300"
          >
            <div className="w-12 h-12 logo-gradient rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
              </svg>
            </div>
            <div className="text-[17px] font-bold text-[#1a1a1a] mb-1.5">Similarity Search</div>
            <p className="text-[13px] font-medium text-[#525252] mb-5">Your company&apos;s brain. A genie for insights.</p>
            <ul className="space-y-3 mb-6 flex-1">
              {[
                "Dump all your company data in",
                "Get detailed insights instantly",
                "An analyst for every manufacturer",
                "Answers that will surprise you",
              ].map((point) => (
                <li key={point} className="flex items-start gap-2.5 text-[14px] text-[#525252]">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#1a1a1a]/25 shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
            <span className="text-[11px] text-[#1a1a1a] font-bold uppercase tracking-widest group-hover:underline inline-flex items-center gap-1.5 group-hover:gap-2.5 transition-all">
              Search your history <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </Link>
        </HeroCard>

        {/* AI Procurement */}
        <HeroCard delay={0.6}>
          <div
            className="group flex flex-col h-full bg-white/80 backdrop-blur-sm border border-black/6 rounded-2xl p-8 sm:p-10 relative overflow-hidden hover:bg-white hover:shadow-xl hover:shadow-black/5 hover:border-black/10 transition-all duration-300"
          >
            <div className="absolute top-4 right-4">
              <span className="text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-orange-50 text-orange-600 border border-orange-200/60">Coming Soon</span>
            </div>
            <div className="w-12 h-12 logo-gradient rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
            </div>
            <div className="text-[17px] font-bold text-[#1a1a1a] mb-1.5">AI Procurement</div>
            <p className="text-[13px] font-medium text-[#525252] mb-5">AI does the groundwork. You make the call.</p>
            <ul className="space-y-3 mb-6 flex-1">
              {[
                "Reads your entire PO history",
                "Builds supplier comparison matrix",
                "Surfaces negotiation patterns",
                "Save 15–20% on every purchase",
              ].map((point) => (
                <li key={point} className="flex items-start gap-2.5 text-[14px] text-[#525252]">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#1a1a1a]/25 shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
            <Link href="/login?waitlist=enterprise" className="text-[11px] text-[#1a1a1a] font-bold uppercase tracking-widest group-hover:underline inline-flex items-center gap-1.5 group-hover:gap-2.5 transition-all">
              Join waitlist <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </HeroCard>
      </div>
    </section>
  );
}

/* ── Problem ──────────────────────────────────────────── */
function Problem() {
  return (
    <section className="py-28 bg-white">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8">
        <motion.div
          className="text-center max-w-3xl mx-auto mb-20"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl sm:text-5xl font-bold text-[#1a1a1a] mb-6 tracking-tight leading-tight">
            You engineer to microns.
            <br />
            <span className="text-[#A3A3A3]">You negotiate blind.</span>
          </h2>
          <p className="text-lg text-[#525252] leading-relaxed">
            Your engineers design to micron-level tolerances. But when
            procurement negotiates price, they rely on supplier PDFs, stale POs,
            and gut feeling. That gap costs you 8–14% on every part.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              stat: "14%",
              label: "Average overpayment",
              desc: "Procurement teams accept supplier quotes with no independent baseline. On precision parts, the average overspend is 14%.",
            },
            {
              stat: "60%",
              label: "Parts already exist",
              desc: "60% of part numbers in a typical manufacturing database are duplicates or variants. A single search across your drawing history would catch them. Each redundant part costs $4,500–7,500/year.",
            },
            {
              stat: "70%",
              label: "Spend is off-the-shelf",
              desc: "70% of procurement spend is on bought-out MPN items. Alternate parts, better vendors, volume discounts \u2014 all discoverable if your past POs were searchable. They\u2019re not.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="p-8 rounded-2xl bg-white border border-black/5 h-full flex flex-col hover:shadow-lg hover:shadow-black/5 hover:-translate-y-1 transition-all duration-300"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.5, delay: i * 0.15 }}
            >
              <div className="text-4xl font-bold text-[#1a1a1a] mb-3 font-mono">
                {item.stat}
              </div>
              <div className="text-[11px] font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">
                {item.label}
              </div>
              <p className="text-[15px] text-[#525252] leading-relaxed flex-1">
                {item.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Should-Cost ──────────────────────────────────────── */
function ShouldCost() {
  return (
    <section id="capabilities" className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
          >
            <div className="text-[11px] text-[#A3A3A3] uppercase tracking-widest font-bold mb-6 font-mono">
              01 / 03 · Should-Cost Estimation
            </div>
            <h2 className="text-4xl sm:text-5xl font-bold text-[#1a1a1a] mb-8 tracking-tight leading-tight">
              Upload a drawing.
              <br />
              <span className="text-[#A3A3A3]">Get the real number.</span>
            </h2>
            <p className="text-lg text-[#525252] leading-relaxed mb-10">
              Your supplier already knows what it costs to make your part. Now
              you will too. Line-by-line should-cost — material, machining,
              finishing, overhead — in 30 seconds. Not days. Plus, instantly
              find similar parts from your history with what you paid before.
              Companies save 8–12% on the first quote they challenge.
            </p>
            <Link
              href="/estimate/new"
              className="dark-pill inline-flex items-center gap-2 px-8 py-4 text-xs font-bold uppercase tracking-widest"
            >
              Upload a Drawing <ArrowRight className="w-4 h-4" />
            </Link>
          </motion.div>

          {/* Cost breakdown card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-[#09090B] rounded-2xl p-6 text-white shadow-2xl">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                <div>
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1">
                    Analysis: NM-9283
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-widest">
                      HIGH confidence
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-1">
                    Should-Cost
                  </div>
                  <div className="text-2xl font-bold tracking-tighter font-mono">
                    ₹ 14,820
                  </div>
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
                          className="h-full bg-orange-500/60 rounded-full"
                        />
                      </div>
                      <span className="text-sm text-white/80 w-16 text-right font-mono">
                        ₹ {item.value}
                      </span>
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
            {
              title: "Sourcing & Procurement",
              desc: "Supplier quoted ₹48,000. Should-cost says ₹29,400. Search finds you paid ₹31,000 last year for the same part. Walk in with data.",
            },
            {
              title: "Cost Engineering",
              desc: "Should-cost in minutes, not days. Every line item defensible. Search your history for similar estimates to cross-check.",
            },
            {
              title: "Design Engineering",
              desc: "See cost impact before it reaches procurement. Search 10 years of drawings — that bracket probably already exists.",
            },
            {
              title: "Leadership",
              desc: "See total overpayment across your supply base. Know which suppliers are competitive.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="p-8 rounded-2xl border border-black/5 bg-[#f9fafb] hover:bg-white hover:border-black/15 hover:shadow-md hover:-translate-y-1 transition-all duration-300 h-full flex flex-col"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
            >
              <CheckCircle2 className="w-5 h-5 text-orange-500 mb-5" />
              <div className="text-[11px] font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">
                {item.title}
              </div>
              <p className="text-[15px] text-[#525252] leading-relaxed flex-1">
                {item.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ── Similarity Search ────────────────────────────────── */
function SimilaritySearch() {
  return (
    <section className="py-28 bg-[#09090B] text-white overflow-hidden">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8">
        <motion.div
          className="text-center max-w-3xl mx-auto mb-20"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-white/30 text-[11px] font-bold uppercase tracking-widest mb-6 font-mono">
            02 / 03 · Company Knowledge Engine
          </div>
          <h2 className="text-4xl sm:text-5xl font-bold mb-8 tracking-tight leading-tight">
            Your company already knows.
            <br />
            <span className="text-white/40">It just can&apos;t remember.</span>
          </h2>
          <p className="text-lg text-white/50 leading-relaxed">
            10,000+ drawings in shared drives. Cost data in spreadsheets. 20
            years of tribal knowledge in your senior engineer&apos;s head. When
            they retire, it walks out the door. Newton-Metre turns scattered
            files into one searchable company brain.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-10">
            {[
              {
                dept: "Design Engineering",
                title:
                  "She spent 3 days designing a bracket. It already existed.",
                desc: "70–80% of new designs are variants of existing parts. Find the match in seconds, tweak 10%, ship in hours. Each avoided new part saves $15,000.",
              },
              {
                dept: "Procurement",
                title:
                  "You paid ₹32,000 last year. They\u2019re quoting ₹48,000.",
                desc: "Every past PO, negotiation outcome, and discount pattern — searchable. Know what you paid, when, and from whom.",
              },
              {
                dept: "Quality",
                title:
                  "25% of your quality issues are repeat failures. Preventable.",
                desc: "When a defect appears, instantly find every past NCR for similar parts. Inspection reports, FAI docs, failure histories — indexed forever.",
              },
              {
                dept: "Sales",
                title:
                  "Customer called. You quoted in 10 minutes. Competitor took 3 days.",
                desc: "Upload a sketch, find 5 similar parts from history, give a ballpark price — while the customer is still on the phone.",
              },
              {
                dept: "Import / Export",
                title:
                  "11,000 HS codes. You classified it wrong. Again.",
                desc: "Find the 5 most similar past imports, surface their HS codes and FTA routes. Indian manufacturers leave 70% of FTA benefits on the table.",
              },
              {
                dept: "Finance",
                title:
                  "\u20B93.2 crore on turned parts last year. You had no idea.",
                desc: "Spend analysis by part family, material, supplier. Budget vs. actual on every category. Visibility into where the money actually goes.",
              },
              {
                dept: "Supply Planning",
                title:
                  "AI predicted demand 3 months out. You ordered before the rush.",
                desc: "Your PO history feeds a forecasting engine that predicts demand by part family, spots seasonal patterns, and calculates reorder points.",
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                className="relative pl-8 border-l border-white/10 hover:border-l-orange-500/50 transition-colors"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
              >
                <div className="text-[11px] font-bold text-white/30 uppercase tracking-widest mb-2">
                  {item.dept}
                </div>
                <div className="text-xl font-bold mb-3">{item.title}</div>
                <p className="text-white/50 text-[15px] leading-relaxed">
                  {item.desc}
                </p>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                  <Search className="w-4 h-4 text-white/60" />
                </div>
                <span className="text-[11px] font-bold uppercase tracking-widest text-white/30">
                  Search Results
                </span>
              </div>

              <div className="space-y-2">
                {[
                  {
                    name: "Bracket_Assy_Rev3.pdf",
                    type: "Manufacturing Drawing",
                    match: "94%",
                  },
                  {
                    name: "Inspection_Report_Q3.pdf",
                    type: "QA Certificate",
                    match: "89%",
                  },
                  {
                    name: "PO_Supplier_Tata_2025.pdf",
                    type: "Purchase Order",
                    match: "85%",
                  },
                  {
                    name: "CNC_Setup_Sheet_M12.pdf",
                    type: "Process Record",
                    match: "82%",
                  },
                ].map((item, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-all cursor-pointer flex items-center justify-between"
                  >
                    <div>
                      <div className="text-sm font-medium mb-0.5 font-mono">
                        {item.name}
                      </div>
                      <div className="text-[10px] text-white/30 uppercase tracking-widest">
                        {item.type}
                      </div>
                    </div>
                    <span className="text-xs font-bold text-emerald-400 font-mono">
                      {item.match}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <Link
                  href="/similar"
                  className="w-full py-4 rounded-full bg-white text-[#09090B] text-xs font-bold uppercase tracking-widest hover:bg-white/90 transition-colors flex items-center justify-center gap-2"
                >
                  Search Your Company History{" "}
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

/* ── AI Worker Trailer ────────────────────────────────── */
function AIWorkerTrailer() {
  return (
    <section className="py-32 px-4 sm:px-8 bg-[#09090B] border-t border-white/5">
      <div className="max-w-[900px] mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-[11px] tracking-widest text-white/50 uppercase font-bold mb-8 font-mono">
            03 / 03 · Coming Soon · Enterprise
          </div>

          <h2 className="text-4xl sm:text-5xl font-bold text-white tracking-tight leading-tight mb-6">
            Better decisions. Faster.
          </h2>

          <p className="text-lg text-white/70 leading-relaxed max-w-[640px] mx-auto">
            Your company&apos;s PO history, vendor master, negotiation
            transcripts, and approval templates &mdash; turned into live
            intelligence. AI reads your data. You make the call.
          </p>
        </motion.div>

        {/* Two columns: off-the-shelf + negotiation intelligence */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {/* Off-the-shelf procurement */}
          <motion.div
            className="bg-white/5 rounded-2xl p-8 border border-white/5 hover:bg-white/8 transition-colors duration-300"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.5 }}
          >
            <div className="text-[11px] font-bold text-white/60 uppercase tracking-widest mb-4 font-mono">
              70% of your spend · Off-the-shelf items
            </div>
            <div className="space-y-4">
              {[
                "Quote comes in — AI checks your PO history for this exact MPN",
                "Finds alternate parts with similar functionality and quality",
                "Builds a supplier matrix: qty tiers, volume history, discount patterns",
                "Sends alternates to design for verification — accept/reject saved forever",
              ].map((line, i) => (
                <div
                  key={i}
                  className="border-l-2 border-white/20 pl-5 py-1 text-white/70 text-[15px] leading-relaxed"
                >
                  {line}
                </div>
              ))}
            </div>
          </motion.div>

          {/* Negotiation intelligence */}
          <motion.div
            className="bg-white/5 rounded-2xl p-8 border border-white/5 hover:bg-white/8 transition-colors duration-300"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.5, delay: 0.15 }}
          >
            <div className="text-[11px] font-bold text-white/60 uppercase tracking-widest mb-4 font-mono">
              Live negotiation intelligence
            </div>
            <div className="space-y-4">
              {[
                "Before the meeting — AI reads every past negotiation with this vendor",
                "Gives exact % targets: \"This supplier typically gives 14% on this volume\"",
                "Surfaces what arguments worked before and where they cave",
                "Every outcome saved — next negotiation is sharper than the last",
              ].map((line, i) => (
                <div
                  key={i}
                  className="border-l-2 border-white/20 pl-5 py-1 text-white/70 text-[15px] leading-relaxed"
                >
                  {line}
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Bottom: compounding moat */}
        <div className="text-center">
          <p className="text-white/60 text-sm mb-8 max-w-lg mx-auto">
            Every interaction makes the system smarter. Alternate approvals,
            negotiation outcomes, vendor performance, price trends &mdash; all
            searchable, all compounding. Your company&apos;s institutional
            memory grows with every deal, every search, every decision.
          </p>
          <Link
            href="/login?waitlist=enterprise"
            className="inline-flex items-center gap-2 border border-white/20 text-white text-xs font-bold uppercase tracking-widest rounded-full px-8 py-4 hover:border-white/40 transition-colors"
          >
            Join the waitlist <ArrowRight className="w-4 h-4" />
          </Link>
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
        <div className="text-center mb-16">
          <h2 className="text-4xl sm:text-5xl font-bold text-[#1a1a1a] tracking-tight mb-4">
            Simple pricing
          </h2>
          <p className="text-lg text-[#525252]">
            One corrected quote pays for a year.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-[800px] mx-auto">
          {/* Free */}
          <div className="p-8 rounded-2xl bg-white border border-black/5 flex flex-col">
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-2">
              Free
            </div>
            <div className="text-4xl font-bold text-[#1a1a1a] font-mono mb-6">
              ₹0
            </div>
            <ul className="space-y-3 mb-8 flex-1">
              {[
                "10 estimates / month",
                "Should-cost breakdown",
                "Similarity search",
                "PDF, DXF & image uploads",
              ].map((f) => (
                <li
                  key={f}
                  className="flex items-center gap-2.5 text-[15px] text-[#525252]"
                >
                  <CheckCircle2 className="w-4 h-4 text-orange-500 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/login"
              className="dark-pill block w-full py-3.5 text-xs font-bold uppercase tracking-widest text-center"
            >
              Get started
            </Link>
          </div>

          {/* Pro */}
          <div className="p-8 rounded-2xl bg-white border border-black/5 flex flex-col">
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-2">
              Pro
            </div>
            <div className="flex items-baseline gap-1 mb-6">
              <span className="text-4xl font-bold text-[#1a1a1a] font-mono">
                ₹4,999
              </span>
              <span className="text-sm text-[#A3A3A3]">/mo</span>
            </div>
            <ul className="space-y-3 mb-8 flex-1">
              {[
                "Unlimited estimates",
                "AI procurement (when available)",
                "Priority support",
                "Team features",
              ].map((f) => (
                <li
                  key={f}
                  className="flex items-center gap-2.5 text-[15px] text-[#525252]"
                >
                  <CheckCircle2 className="w-4 h-4 text-orange-500 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/login?waitlist=pro"
              className="block w-full py-3.5 rounded-full border border-black/10 text-xs font-bold uppercase tracking-widest text-center text-[#1a1a1a] hover:bg-[#f9fafb] transition-colors"
            >
              Join waitlist
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Footer ───────────────────────────────────────────── */
function Footer() {
  return (
    <footer className="py-16 px-4 sm:px-8 warm-gradient-footer relative overflow-hidden">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="relative w-9 h-9 flex items-center justify-center">
                <div className="absolute inset-0 logo-gradient rounded-xl" />
                <span className="relative text-white font-mono font-bold text-sm tracking-tighter">
                  N·m
                </span>
              </div>
              <span className="text-[#1a1a1a] text-lg font-bold tracking-tight">
                Newton-Metre
              </span>
            </div>
            <p className="text-[15px] text-[#1a1a1a]/60 leading-relaxed">
              Know what it costs, before they quote.
            </p>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Company
            </div>
            <ul className="space-y-2.5">
              <li>
                <a
                  href="mailto:chand@costimize.dev"
                  className="text-[15px] text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors"
                >
                  Contact Us
                </a>
              </li>
            </ul>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Product
            </div>
            <ul className="space-y-2.5">
              {[
                { label: "Should-Cost", href: "/estimate/new" },
                { label: "Similarity Search", href: "/similar" },
                { label: "AI Procurement", href: "/login" },
              ].map((item) => (
                <li key={item.label}>
                  <Link
                    href={item.href}
                    className="text-[15px] text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Legal
            </div>
            <ul className="space-y-2.5">
              <li>
                <a
                  href="mailto:chand@costimize.dev"
                  className="text-[15px] text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors"
                >
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-[#1a1a1a]/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-[#1a1a1a]/40">
            &copy; 2026 Newton-Metre. Manufacturing intelligence.
          </div>
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
        <AIWorkerTrailer />
        <Pricing />
      </main>
      <Footer />
    </div>
  );
}
