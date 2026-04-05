"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "motion/react";
import {
  ArrowRight,
  CheckCircle2,
  Search,
  Upload,
  Zap,
  ShieldCheck,
  BarChart3,
  Package,
  AlertTriangle,
  TrendingDown,
} from "lucide-react";
import { LandingNav } from "@/components/landing-nav";

/* ─────────────────────────────────────────────────────────────
   NEWTON-METRE — Landing Page
   Narrative: Problem → Vision → Products (Door Opener → Platform → Engine)
   "The Price Integrity Layer for Global Manufacturing"
   ───────────────────────────────────────────────────────────── */

/* ── ₹ Currency — same height as adjacent number ─────── */
function R({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <span className={`font-mono inline-flex items-baseline whitespace-nowrap ${className}`}>
      <span className="font-sans text-[0.95em] leading-none mr-[0.04em]" style={{ verticalAlign: "baseline" }}>₹</span>
      {children}
    </span>
  );
}

/* ── Page ──────────────────────────────────────────────── */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <LandingNav />
      <main>
        <Hero />
        <Proof />
        <Vision />
        <ShouldCost />
        <SimilaritySearch />
        <AIEngine />
        <SeventyPercentGuardrail />
        <ROICalculator />
        <Pricing />
      </main>
      <Footer />
    </div>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 1: HERO — THE PROBLEM
   "You're sitting on 20 years of procurement data.
    It's in PDFs, spreadsheets, and people's heads."
   ══════════════════════════════════════════════════════════ */
function Hero() {
  return (
    <section className="pt-36 pb-20 px-4 sm:px-8 warm-gradient-hero overflow-hidden">
      <div className="max-w-[1000px] mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-600 text-[14px] font-bold uppercase tracking-widest mb-8">
            <Zap className="w-3 h-3" /> Built for Defense, Aerospace &amp; Automotive
          </div>

          {/* Headline — the problem */}
          <h1
            className="text-5xl sm:text-6xl lg:text-[80px] font-semibold leading-[1] tracking-tight mb-8"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>20 years of data.</em>
            <br />
            <span className="text-[#A3A3A3] not-italic">Zero intelligence.</span>
          </h1>

          <div className="max-w-2xl mx-auto mb-12 space-y-4">
            <p className="text-xl text-[#525252] leading-relaxed text-justify">
              Your company has 20 years of data — stuck in PDFs,
              messy spreadsheets, and an ERP that&apos;s really just an accounting tool.
              Great at storing data. Terrible at making sense of it.
            </p>
            <p className="text-xl text-[#525252] leading-relaxed text-justify">
              When your senior people leave, 20 years of design knowledge,
              machining experience, assembly process know-how, vendor relationships,
              and negotiation intuition walks out the door.
            </p>
          </div>

          {/* Drop Zone */}
          <Link href="/estimate/new" className="block max-w-xl mx-auto group">
            <div className="border-2 border-dashed border-black/15 rounded-2xl bg-white/60 backdrop-blur-sm p-10 hover:border-[#1a1a1a]/30 hover:bg-white/80 hover:shadow-xl hover:shadow-black/5 transition-all duration-300 cursor-pointer">
              <div className="w-14 h-14 mx-auto mb-4 rounded-xl bg-[#1a1a1a]/5 flex items-center justify-center group-hover:bg-[#1a1a1a]/10 transition-colors">
                <Upload className="w-6 h-6 text-[#525252]" />
              </div>
              <div className="text-[17px] font-bold text-[#1a1a1a] mb-1.5">
                Drop a 2D drawing or supplier quote
              </div>
              <div className="text-[15px] text-[#A3A3A3]">
                DWG, STEP, DXF, PDF — or click to browse
              </div>
            </div>
          </Link>

          {/* On-prem badge */}
          <div className="flex items-center justify-center gap-2 mt-6 text-[14px] font-bold uppercase tracking-widest text-[#A3A3A3]">
            <ShieldCheck className="w-3.5 h-3.5" /> 100% On-Premise for Defense
          </div>
        </motion.div>
      </div>

      {/* Product Preview Card */}
      <motion.div
        className="max-w-[1000px] mx-auto mt-16 px-4"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <div className="bg-white rounded-3xl border border-black/8 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.08)] p-6 sm:p-10 overflow-hidden">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between border-b border-black/5 pb-6 mb-6 gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-emerald-600" />
              </div>
              <div>
                <div className="text-[12px] uppercase tracking-widest font-bold text-[#A3A3A3]">
                  Analysis: BRKT-928-AL
                </div>
                <div className="text-lg font-bold text-[#1a1a1a]">
                  Should-Cost Breakdown
                </div>
              </div>
            </div>
            <div className="flex items-center gap-8">
              <div className="text-right">
                <div className="text-[12px] uppercase tracking-widest font-bold text-[#A3A3A3]">
                  Supplier Quote
                </div>
                <div className="text-xl font-bold text-[#A3A3A3] line-through font-mono">
                  <R>48,200</R>
                </div>
              </div>
              <div className="text-right">
                <div className="text-[12px] uppercase tracking-widest font-bold text-orange-500">
                  True Cost
                </div>
                <div className="text-3xl font-bold text-[#1a1a1a] font-mono tracking-tighter">
                  <R>32,450</R>
                </div>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="col-span-2 space-y-4">
              {[
                { label: "Material: Aluminum 6061-T6 (2.4 kg)", cost: "4,820", pct: 15 },
                { label: "CNC Machining (3-Axis Milling)", cost: "18,400", pct: 56 },
                { label: "Surface: Clear Anodize", cost: "3,200", pct: 10 },
                { label: "Overhead & Standard Margin", cost: "6,030", pct: 19 },
              ].map((row, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-4 rounded-xl bg-[#fafafa] border border-black/[0.03]"
                >
                  <span className="text-sm font-medium text-[#525252]">{row.label}</span>
                  <div className="flex items-center gap-4">
                    <div className="w-24 h-1.5 bg-black/5 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${row.pct}%` }}
                        transition={{ duration: 1, delay: 0.5 + i * 0.1 }}
                        className="h-full bg-orange-500/70 rounded-full"
                      />
                    </div>
                    <span className="text-sm font-bold font-mono text-[#1a1a1a] w-16 text-right">
                      <R>{row.cost}</R>
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <div className="bg-orange-50 rounded-2xl p-6 border border-orange-100 flex flex-col justify-center">
              <div className="text-orange-600 font-bold text-sm mb-3">Hidden Margin</div>
              <div className="text-4xl font-bold tracking-tight text-[#1a1a1a] font-mono mb-2">
                <R>15,750</R>
              </div>
              <div className="text-sm text-orange-700/70 leading-snug">
                That&apos;s how much extra you&apos;re paying. Per unit. Now go back to the table with proof.
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 2: PROOF — REAL RESULT
   ══════════════════════════════════════════════════════════ */
function Proof() {
  return (
    <section className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1100px] mx-auto">
        {/* Big quote */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-[14px] font-bold uppercase tracking-widest text-orange-500 mb-6 font-mono">
            Real result &middot; Defense sub-assembly
          </div>
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-[#1a1a1a] tracking-tight leading-tight mb-8"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>&ldquo;The deal they were celebrating?</em>
            <br />
            <span className="text-orange-500">They&apos;d left ₹6 crore on the table.&rdquo;</span>
          </h2>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Story */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-[17px] text-[#525252] leading-relaxed mb-6 text-justify">
              Vendor quoted <R className="font-bold text-[#1a1a1a]">43L</R>. After negotiations, it came down to{" "}
              <R className="font-bold text-[#1a1a1a]">37L</R> — team celebrated.
              Newton-Metre ran the numbers: mechanical cost{" "}
              <R className="font-bold text-[#1a1a1a]">8L</R>, purchased components{" "}
              <R className="font-bold text-[#1a1a1a]">12L</R>, with margin: should-cost{" "}
              <R className="font-bold text-[#1a1a1a]">25L</R>.
            </p>
            <p className="text-[17px] text-[#525252] leading-relaxed mb-8 text-justify">
              Armed with a line-by-line breakdown, the team pushed again. Vendor settled at{" "}
              <R className="font-bold text-[#1a1a1a]">28L</R>.
            </p>
            {/* Evidence bullets — bigger */}
            <div className="space-y-4">
              <motion.div
                className="flex items-center gap-4 p-4 rounded-xl bg-white border border-black/5"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.2 }}
              >
                <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />
                <span className="text-[16px] text-[#1a1a1a] font-medium">Line-by-line breakdown revealed 14% margin padding</span>
              </motion.div>
              <motion.div
                className="flex items-center gap-4 p-4 rounded-xl bg-white border border-black/5"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.3 }}
              >
                <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />
                <span className="text-[16px] text-[#1a1a1a] font-medium">Same part bought at <R>31K</R> last year — now quoted at <R>48K</R></span>
              </motion.div>
            </div>
          </motion.div>

          {/* Numbers */}
          <motion.div
            className="grid grid-cols-2 gap-4"
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            {[
              { stat: "43L", label: "Vendor's opening quote", muted: true },
              { stat: "37L", label: "What management celebrated", muted: true },
              { stat: "25L", label: "Should-cost (Newton-Metre)", highlight: true },
              { stat: "28L", label: "Final negotiated price", highlight: true },
            ].map((item, i) => (
              <motion.div
                key={i}
                className={`p-6 rounded-2xl border ${item.highlight ? "bg-[#1a1a1a] border-[#1a1a1a]" : "bg-white border-black/8"}`}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                whileHover={{ scale: 1.03 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.2 + i * 0.1 }}
              >
                <div className={`text-4xl font-bold font-mono mb-2 ${item.highlight ? "text-white" : "text-[#1a1a1a]"}`}>
                  <R className={item.highlight ? "text-white" : "text-[#1a1a1a]"}>{item.stat}</R>
                </div>
                <div className={`text-[12px] uppercase tracking-widest font-bold ${item.highlight ? "text-white/60" : "text-[#A3A3A3]"}`}>
                  {item.label}
                </div>
              </motion.div>
            ))}
            <motion.div
              className="col-span-2 p-8 rounded-2xl bg-orange-50 border border-orange-200"
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.5 }}
            >
              <div className="text-5xl font-bold font-mono text-orange-600 mb-2">
                <R>10.05 Cr</R>
              </div>
              <div className="text-[14px] uppercase tracking-widest font-bold text-orange-500">
                Total saved &middot; 67 units &times; ₹15L per unit
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 3: THE VISION — PRICE INTELLIGENCE
   "We turn your history into your company's price intelligence."
   ══════════════════════════════════════════════════════════ */
function Vision() {
  return (
    <section className="py-28 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8">
        <motion.div
          className="text-center max-w-3xl mx-auto mb-20"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-orange-500 text-[14px] font-bold uppercase tracking-widest mb-6 font-mono">
            The Vision
          </div>
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-[#1a1a1a] mb-6 tracking-tight leading-tight"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>We turn your history into</em>
            <br />
            <span className="text-[#A3A3A3] not-italic">price intelligence.</span>
          </h2>
          <p className="text-lg text-[#525252] leading-relaxed text-justify">
            Drawing archive, PO records, vendor negotiations, tribal knowledge —
            all of it in one searchable system. Every past deal makes the next one sharper.
            That&apos;s not a tool. That&apos;s your company&apos;s memory. And it only gets smarter.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              stat: "14%",
              label: "Information Asymmetry",
              desc: "Your supplier knows exactly what it costs to make your part. Your buyer doesn't. On precision parts, the average overspend is 14%. Every year. Every order.",
            },
            {
              stat: "60%",
              label: "Parts already exist",
              desc: "60% of the parts in your system are duplicates or variants of something you already made. One search catches them. Every redundant part is costing you ₹3.5–6 lakh a year to maintain.",
            },
            {
              stat: "70%",
              label: "Spend is off-the-shelf",
              desc: "70% of what you buy is catalog items — bearings, connectors, motors. Better prices, alternate vendors, volume deals — all sitting in your own purchase history. If only it was searchable.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="p-8 rounded-2xl bg-white border border-black/5 h-full flex flex-col hover:shadow-lg hover:shadow-black/5 transition-all duration-300 cursor-default"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              whileHover={{ y: -4, scale: 1.02 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.5, delay: i * 0.15 }}
            >
              <div className="text-4xl font-bold text-[#1a1a1a] mb-3 font-mono">
                {item.stat}
              </div>
              <div className="text-[14px] font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">
                {item.label}
              </div>
              <p className="text-[16px] text-[#525252] leading-relaxed flex-1 text-justify">
                {item.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 4: SHOULD-COST — THE DOOR OPENER
   "Upload a drawing. See the real number. Negotiate with data."
   ══════════════════════════════════════════════════════════ */
function ShouldCost() {
  return (
    <section id="capabilities" className="py-32 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-orange-500 text-[15px] sm:text-[18px] uppercase tracking-widest font-bold mb-6 font-mono">
            01 / 03 &middot; The Door Opener
          </div>
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-[#1a1a1a] tracking-tight leading-tight"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>Upload a drawing.</em>
            <br />
            <span className="text-[#A3A3A3] not-italic">Get the real number.</span>
          </h2>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16 items-start">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-white rounded-2xl border border-black/8 p-8 sm:p-10 shadow-sm mb-8">
              <p className="text-[17px] text-[#525252] leading-[1.8] mb-6 text-justify">
                Your supplier knows what it costs to make your part.
                You don&apos;t. That ends now.
              </p>
              <p className="text-[17px] text-[#525252] leading-[1.8] mb-6 text-justify">
                Upload a drawing. Get the full breakdown — material, machining, finishing,
                overhead — in <span className="font-bold text-[#1a1a1a]">30 seconds</span>.
                Not days. Every line item you can defend. Every number you can trace.
              </p>
              <p className="text-[17px] text-[#525252] leading-[1.8] text-justify">
                Companies save{" "}
                <span className="font-bold text-[#1a1a1a]">8–12%</span> on the
                very first quote they challenge. First quote. First day.
              </p>
            </div>
            <Link
              href="/estimate/new"
              className="dark-pill inline-flex items-center gap-2 px-10 py-5 text-xs font-bold uppercase tracking-widest"
            >
              Start a 30-second audit <ArrowRight className="w-4 h-4" />
            </Link>
          </motion.div>

          {/* Cost breakdown card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="bg-[#1a1a1a] rounded-2xl p-6 text-white shadow-2xl">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                <div>
                  <div className="text-[12px] font-bold text-white/40 uppercase tracking-widest mb-1">
                    Analysis: NM-9283
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-[14px] font-bold text-emerald-400 uppercase tracking-widest">
                      HIGH confidence
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[12px] font-bold text-white/40 uppercase tracking-widest mb-1">
                    Should-Cost
                  </div>
                  <div className="text-2xl font-bold tracking-tighter font-mono">
                    <R className="text-white">14,820</R>
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
                        <R className="text-white/80">{item.value}</R>
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
              desc: "Supplier says ₹48,000. Should-cost says ₹29,400. You paid ₹31,000 last year for the same part. Now walk in and ask them why.",
            },
            {
              title: "Cost Engineering",
              desc: "Get should-cost in minutes, not days. Every line item holds up. Cross-check against your own past estimates instantly.",
            },
            {
              title: "Design Engineering",
              desc: "Know the cost impact before it reaches procurement. That part? It probably already exists in your history. Search first, design second.",
            },
            {
              title: "Leadership",
              desc: "How much are you overpaying across the entire supply base? Which vendors are sharp, which are milking you — visible in one click.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="p-8 rounded-2xl border border-black/5 bg-white/80 hover:bg-white hover:border-black/15 hover:shadow-md hover:-translate-y-1 transition-all duration-300 h-full flex flex-col"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
            >
              <CheckCircle2 className="w-5 h-5 text-orange-500 mb-5" />
              <div className="text-[14px] font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">
                {item.title}
              </div>
              <p className="text-[16px] text-[#525252] leading-relaxed flex-1 text-justify">
                {item.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 5: INSTITUTIONAL MEMORY — THE PLATFORM
   "Once 100,000 drawings are indexed, they never leave."
   ══════════════════════════════════════════════════════════ */
function SimilaritySearch() {
  return (
    <section className="py-32 bg-[#1a1a1a] overflow-hidden relative">
      {/* Glow orbs — animated */}
      <motion.div
        className="absolute top-20 left-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl pointer-events-none"
        animate={{ x: [0, 30, 0], y: [0, -20, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-20 right-1/4 w-80 h-80 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"
        animate={{ x: [0, -20, 0], y: [0, 30, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8 relative z-10">
        <motion.div
          className="text-center max-w-3xl mx-auto mb-20"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-orange-500 text-[15px] sm:text-[18px] font-bold uppercase tracking-widest mb-6 font-mono">
            02 / 03 &middot; The Platform
          </div>
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold mb-8 tracking-tight leading-tight text-white"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>Your company already knows.</em>
            <br />
            <span className="text-white/40 not-italic">It just can&apos;t remember.</span>
          </h2>
          <p className="text-lg text-white/75 leading-relaxed text-justify">
            10,000+ drawings sitting in shared drives. Cost data buried in
            spreadsheets. 20 years of knowledge locked in one person&apos;s head.
            Index it once in Newton-Metre — now it&apos;s permanent, searchable, and gets
            sharper with every decision. Once 100,000 drawings are in, nobody leaves.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-10">
            {[
              {
                dept: "Design Engineering",
                title: "3 days designing a part that already existed.",
                desc: "70–80% of new designs are variants of something you already made. Find the match in seconds, tweak 10%, ship in hours. Every avoided redesign saves ₹12–15 lakh.",
              },
              {
                dept: "Procurement",
                title: "Paid ₹32,000 last year. Now they want ₹48,000.",
                desc: "Every past PO, every negotiation outcome, every discount pattern — searchable. What you paid, when, to whom. One click.",
              },
              {
                dept: "Quality",
                title: "Same defect. Third time this year. All preventable.",
                desc: "Defect shows up? Pull every past NCR for similar parts instantly. Inspection reports, FAI docs, failure patterns — all indexed. Forever.",
              },
              {
                dept: "Sales",
                title: "Customer on the phone. Quote sent in 10 minutes. Competitor took 3 days.",
                desc: "Upload the sketch, find 5 similar parts from history, give a price — while they&apos;re still on the call. Speed wins orders.",
              },
              {
                dept: "Finance",
                title: "₹3.2 crore on turned parts last year. Nobody even knew.",
                desc: "Spend by part family, material, supplier. Budget vs actual on every category. Where the money actually goes — finally visible.",
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                className="relative pl-8 border-l-2 border-white/10 hover:border-orange-500/60 transition-colors"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
              >
                <div className="text-[14px] font-bold text-orange-500 uppercase tracking-widest mb-2">
                  {item.dept}
                </div>
                <div className="text-xl font-bold mb-3 text-white">{item.title}</div>
                <p className="text-white/70 text-[16px] leading-relaxed text-justify">
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
            <div className="bg-white/5 rounded-2xl p-8 border border-white/10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                  <Search className="w-4 h-4 text-white/60" />
                </div>
                <span className="text-[14px] font-bold uppercase tracking-widest text-white/40">
                  Search Results
                </span>
              </div>

              <div className="space-y-2">
                {[
                  { name: "Bracket_Assy_Rev3.pdf", type: "Manufacturing Drawing", match: "94%" },
                  { name: "Inspection_Report_Q3.pdf", type: "QA Certificate", match: "89%" },
                  { name: "PO_Supplier_Tata_2025.pdf", type: "Purchase Order", match: "85%" },
                  { name: "CNC_Setup_Sheet_M12.pdf", type: "Process Record", match: "82%" },
                ].map((item, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 hover:bg-white/8 transition-all cursor-pointer flex items-center justify-between"
                  >
                    <div>
                      <div className="text-sm font-medium mb-0.5 font-mono text-white">
                        {item.name}
                      </div>
                      <div className="text-[12px] text-white/40 uppercase tracking-widest">
                        {item.type}
                      </div>
                    </div>
                    <span className="text-xs font-bold text-orange-500 font-mono">
                      {item.match}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <Link
                  href="/similar"
                  className="w-full py-4 rounded-full bg-white text-[#1a1a1a] text-xs font-bold uppercase tracking-widest hover:bg-white/90 transition-colors flex items-center justify-center gap-2"
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

/* ══════════════════════════════════════════════════════════
   SECTION 6: AI PROCUREMENT ENGINE — THE REVENUE
   "From tactical buying to strategic sourcing."
   ══════════════════════════════════════════════════════════ */
function AIEngine() {
  return (
    <section className="py-32 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[900px] mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-orange-500 text-[15px] sm:text-[18px] tracking-widest uppercase font-bold mb-6 font-mono">
            03 / 03 &middot; The Revenue Engine
          </div>

          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-[#1a1a1a] tracking-tight leading-tight mb-6"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>From tactical buying</em>
            <br />
            <span className="text-[#A3A3A3] not-italic">to strategic sourcing.</span>
          </h2>

          <p className="text-lg text-[#525252] leading-relaxed max-w-[640px] mx-auto text-justify">
            PO history, vendor master, negotiation transcripts, approval
            templates — all turned into live intelligence. AI reads your data, audits every quote,
            gets sharper with every deal. You make the call.
          </p>
        </motion.div>

        {/* Two-column breakdown */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <motion.div
            className="bg-white rounded-2xl p-8 border border-black/6"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.5 }}
          >
            <div className="text-[14px] font-bold text-orange-500 uppercase tracking-widest mb-5 font-mono">
              70% of your spend &middot; Off-the-shelf items
            </div>
            <div className="space-y-4">
              {[
                "Quote arrives — AI instantly checks your PO history for this exact MPN",
                "Finds alternate parts with similar functionality and quality",
                "Builds a supplier matrix: qty tiers, volume history, discount patterns",
                "Sends alternates to design for verification — accept/reject saved forever",
              ].map((line, i) => (
                <div key={i} className="border-l-2 border-black/8 pl-5 py-0.5 text-[#525252] text-[15px] leading-relaxed">
                  {line}
                </div>
              ))}
            </div>
          </motion.div>
          <motion.div
            className="bg-white rounded-2xl p-8 border border-black/6"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <div className="text-[14px] font-bold text-orange-500 uppercase tracking-widest mb-5 font-mono">
              Live negotiation intelligence
            </div>
            <div className="space-y-4">
              {[
                "Before the meeting — AI reads every past negotiation with this vendor",
                "Gives exact % targets: \"This supplier typically gives 14% on this volume\"",
                "Shows what arguments worked last time and where they gave in",
                "Every outcome saved — next negotiation is sharper than the last",
              ].map((line, i) => (
                <div key={i} className="border-l-2 border-black/8 pl-5 py-0.5 text-[#525252] text-[15px] leading-relaxed">
                  {line}
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Department scenario cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
          {[
            {
              dept: "Procurement",
              headline: "They quoted ₹48,000. You paid ₹32,000 last year.",
              desc: "AI surfaces your exact PO history, discount patterns, and negotiation wins before the meeting. Walk in knowing the number.",
            },
            {
              dept: "Design Engineering",
              headline: "Part went end-of-life. 3 verified alternates found in 40 seconds.",
              desc: "AI checks your approved parts list against supplier catalogs. Design reviews, approvals saved forever — no more email chains.",
            },
            {
              dept: "Finance",
              headline: "₹2.4 crore off-contract spend. Caught before the audit.",
              desc: "Every purchase checked against approved vendor rates. Rogue spend flagged in real time. Budget vs actual on every category.",
            },
            {
              dept: "Quality",
              headline: "Supplier defect rate: 4.2%. You kept giving them more orders.",
              desc: "Scorecards built from every NCR, FAI, incoming inspection. Updated with every delivery. No spreadsheet maintenance needed.",
            },
            {
              dept: "Supply Planning",
              headline: "Lead time jumped from 6 to 14 weeks. AI flagged it 90 days ago.",
              desc: "PO history feeds a forecasting engine. It spots disruptions before they hit your production line. Reorder points calculated, not guessed.",
            },
            {
              dept: "Leadership",
              headline: "₹50 crore procurement spend. Understood in 3 minutes flat.",
              desc: "Spend by category, supplier, department. Every saving identified, every risk visible. The brief your team never had time to prepare.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="bg-white rounded-2xl p-7 border border-black/6 hover:shadow-lg hover:shadow-black/5 hover:-translate-y-1 transition-all duration-300 flex flex-col"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.07 }}
            >
              <div className="text-[12px] font-bold text-orange-500 uppercase tracking-widest mb-3 font-mono">
                {item.dept}
              </div>
              <div className="text-[16px] font-bold text-[#1a1a1a] leading-snug mb-3 flex-1">
                {item.headline}
              </div>
              <p className="text-[15px] text-[#525252] leading-relaxed text-justify">
                {item.desc}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Bottom: compounding moat */}
        <div className="text-center">
          <p className="text-[#525252] text-[16px] leading-relaxed mb-8 max-w-lg mx-auto text-justify">
            Every interaction compounds the memory. Alternate approvals,
            negotiation outcomes, vendor performance, price trends — all
            searchable, all growing. This is the system of record your suppliers
            hope you never build.
          </p>
          <Link
            href="/waitlist"
            className="inline-flex items-center gap-2 bg-[#1a1a1a] text-white text-xs font-bold uppercase tracking-widest rounded-full px-8 py-4 hover:bg-[#333] transition-colors"
          >
            Join the waitlist <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 7: THE 70% GUARDRAIL
   "Beyond the Drawing — the spend nobody audits."
   ══════════════════════════════════════════════════════════ */
function SeventyPercentGuardrail() {
  const mpnItems = [
    {
      icon: <Package className="w-6 h-6" />,
      label: "Bearings & bushings",
      problem: "Your vendor charges 62% above market price.",
      solution: "Same spec, same grade — AI flags it before the PO goes out.",
    },
    {
      icon: <AlertTriangle className="w-6 h-6" />,
      label: "Motors & actuators",
      problem: "Same MPN, three distributors — prices vary 40%.",
      solution: "AI compares all sources and picks the best one in seconds.",
    },
    {
      icon: <TrendingDown className="w-6 h-6" />,
      label: "Connectors & harnesses",
      problem: "Your vendor charges 2.5x what the market pays.",
      solution: "Flagged automatically. Alternate source suggested with pricing.",
    },
    {
      icon: <Search className="w-6 h-6" />,
      label: "Sensors & switches",
      problem: "Vendor substituted a higher-margin equivalent.",
      solution: "Your spec says standard part. AI catches the swap before approval.",
    },
  ];

  return (
    <section className="py-40 px-4 sm:px-8 bg-[#1a1a1a] text-white relative overflow-hidden">
      <motion.div
        className="absolute top-0 left-1/4 w-[500px] h-[500px] rounded-full bg-orange-500/8 blur-[120px] pointer-events-none"
        animate={{ x: [0, 40, 0], y: [0, -30, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-0 right-1/4 w-[400px] h-[400px] rounded-full bg-blue-500/5 blur-[120px] pointer-events-none"
        animate={{ x: [0, -30, 0], y: [0, 40, 0] }}
        transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
      />

      <div className="max-w-[1200px] mx-auto relative z-10">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-orange-500/15 border border-orange-500/25 text-orange-400 text-[14px] sm:text-[16px] font-bold uppercase tracking-widest mb-8">
            The 70% nobody audits
          </div>
          <h2
            className="text-4xl sm:text-5xl lg:text-7xl font-semibold tracking-tight mb-8"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>Not just drawings.</em>
            <br />
            <span className="text-white/40 not-italic">Your entire spend.</span>
          </h2>
          <p className="text-xl text-white/70 max-w-3xl mx-auto leading-relaxed text-justify">
            Most cost tools only handle custom machined parts — that&apos;s 30% of your spend.
            The other{" "}
            <span className="text-white font-bold">
              70% is off-the-shelf
            </span>{" "}
            — bearings, motors, connectors, sensors. Catalog items that nobody audits.
            You overpay on them every single time. Newton-Metre audits everything.
          </p>
        </motion.div>

        {/* Visual split — 70/30 bar */}
        <motion.div
          className="mb-20 max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex gap-2 mb-4">
            <motion.div
              className="h-5 rounded-full bg-orange-500"
              initial={{ width: 0 }}
              whileInView={{ width: "70%" }}
              viewport={{ once: true }}
              transition={{ duration: 1.2, ease: "easeOut" }}
            />
            <motion.div
              className="h-5 rounded-full bg-white/20"
              initial={{ width: 0 }}
              whileInView={{ width: "30%" }}
              viewport={{ once: true }}
              transition={{ duration: 1.2, ease: "easeOut", delay: 0.3 }}
            />
          </div>
          <div className="flex justify-between text-[14px]">
            <span className="text-white font-bold">70% Off-the-shelf MPN items — <span className="text-orange-400">unaudited</span></span>
            <span className="text-white/50">30% Made-to-drawing</span>
          </div>
        </motion.div>

        {/* MPN examples — bigger cards with problem/solution split */}
        <div className="grid sm:grid-cols-2 gap-6 mb-16">
          {mpnItems.map((item, i) => (
            <motion.div
              key={i}
              className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-8 hover:border-orange-500/30 transition-all duration-300"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              whileHover={{ y: -4 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.1 }}
            >
              <div className="flex items-center gap-4 mb-5">
                <div className="w-12 h-12 rounded-xl bg-orange-500/15 flex items-center justify-center text-orange-400">
                  {item.icon}
                </div>
                <div className="text-[16px] font-bold text-white">{item.label}</div>
              </div>
              <p className="text-[16px] text-white/80 leading-relaxed mb-3">
                <span className="text-orange-400 font-semibold">Problem:</span> {item.problem}
              </p>
              <p className="text-[16px] text-white/80 leading-relaxed">
                <span className="text-emerald-400 font-semibold">Fix:</span> {item.solution}
              </p>
            </motion.div>
          ))}
        </div>

        <motion.div
          className="text-center"
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-white/80 text-lg max-w-2xl mx-auto mb-8 text-justify">
            <span className="text-white font-bold">One platform.</span>{" "}
            Drawings and MPNs. Custom parts and catalog items.
            The full procurement stack — not just the pretty half.
          </p>
        </motion.div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 8: ROI CALCULATOR
   "How much value is leaking?"
   ══════════════════════════════════════════════════════════ */
function ROICalculator() {
  const [spend, setSpend] = useState(5);
  const [saving, setSaving] = useState(8);

  const spendInr = spend * 1_00_00_000;
  const savingsInr = spendInr * (saving / 100);
  const annualCost = 4_999 * 12;
  const roi = Math.round(savingsInr / annualCost);
  const fmt = (n: number) =>
    n >= 1_00_00_000
      ? `${(n / 1_00_00_000).toFixed(1)} Cr`
      : n >= 1_00_000
        ? `${(n / 1_00_000).toFixed(0)}L`
        : n.toLocaleString("en-IN");

  return (
    <section className="py-32 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-20">
          <div className="text-[14px] font-bold uppercase tracking-widest text-orange-500 mb-6 font-mono">
            ROI calculator
          </div>
          <h2
            className="text-5xl sm:text-6xl font-semibold tracking-tight mb-6 text-[#1a1a1a]"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>How much value is leaking?</em>
          </h2>
          <p className="text-xl text-[#525252] max-w-2xl mx-auto leading-relaxed text-justify">
            Manufacturing companies overpay suppliers by 8–14% on average.
            One corrected quote pays for a full year of Newton-Metre.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-16 items-center max-w-5xl mx-auto">
          {/* Sliders */}
          <div className="space-y-10">
            <div>
              <div className="flex justify-between items-baseline mb-4">
                <label className="text-[12px] font-bold uppercase tracking-widest text-[#6b7280] font-mono">
                  Annual procurement spend
                </label>
                <span className="text-2xl font-bold font-mono text-[#1a1a1a]">
                  <R>{spend} Cr</R>
                </span>
              </div>
              <input
                type="range"
                min={1}
                max={100}
                step={1}
                value={spend}
                onChange={(e) => setSpend(Number(e.target.value))}
                className="w-full h-2 bg-black/10 rounded-full appearance-none cursor-pointer accent-orange-500"
              />
              <div className="flex justify-between text-[14px] text-[#9ca3af] font-mono mt-2">
                <span>₹1 Cr</span>
                <span>₹100 Cr</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-baseline mb-4">
                <label className="text-[12px] font-bold uppercase tracking-widest text-[#6b7280] font-mono">
                  Negotiation improvement
                </label>
                <span className="text-2xl font-bold font-mono text-[#1a1a1a]">
                  {saving}%
                </span>
              </div>
              <input
                type="range"
                min={2}
                max={20}
                step={1}
                value={saving}
                onChange={(e) => setSaving(Number(e.target.value))}
                className="w-full h-2 bg-black/10 rounded-full appearance-none cursor-pointer accent-orange-500"
              />
              <div className="flex justify-between text-[14px] text-[#9ca3af] font-mono mt-2">
                <span>2% (conservative)</span>
                <span>20% (aggressive)</span>
              </div>
            </div>
          </div>

          {/* Result card */}
          <div className="bg-[#1a1a1a] rounded-2xl p-10 shadow-2xl">
            <div className="space-y-6">
              <div className="flex justify-between items-center pb-5 border-b border-white/10">
                <span className="text-sm text-white/40">Procurement spend</span>
                <span className="font-mono font-bold text-white text-lg">
                  <R className="text-white">{fmt(spendInr)}</R>/yr
                </span>
              </div>
              <div className="flex justify-between items-center pb-5 border-b border-white/10">
                <span className="text-sm text-white/40">
                  Savings at {saving}%
                </span>
                <span className="font-mono font-bold text-emerald-400 text-2xl">
                  <R className="text-emerald-400">{fmt(savingsInr)}</R>/yr
                </span>
              </div>
              <div className="flex justify-between items-center pb-5 border-b border-white/10">
                <span className="text-sm text-white/40">Newton-Metre Pro</span>
                <span className="font-mono text-white/60"><R className="text-white/60">59,988</R>/yr</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-base font-bold text-white">
                  Return on investment
                </span>
                <span className="font-mono font-bold text-orange-400 text-4xl">
                  {roi}x
                </span>
              </div>
            </div>
            <Link
              href="/login"
              className="block w-full mt-10 py-4 rounded-full bg-white text-[#1a1a1a] text-xs font-bold uppercase tracking-widest text-center hover:bg-white/90 transition-colors"
            >
              Start saving — free
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   SECTION 9: PRICING
   ══════════════════════════════════════════════════════════ */
function Pricing() {
  return (
    <section id="pricing" className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-16">
          <h2
            className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-[#1a1a1a] tracking-tight mb-4"
            style={{ fontFamily: "var(--font-headline)" }}
          >
            <em>Simple pricing.</em>
          </h2>
          <p className="text-lg text-[#525252]">
            One corrected quote pays for the entire year.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-[800px] mx-auto">
          {/* Free */}
          <div className="p-8 rounded-2xl bg-white/80 border border-black/6 flex flex-col">
            <div className="text-[14px] font-bold uppercase tracking-widest text-[#A3A3A3] mb-3 font-mono">
              Free
            </div>
            <div className="text-5xl font-bold text-[#1a1a1a] font-mono mb-1">
              <R>0</R>
            </div>
            <p className="text-[15px] text-[#A3A3A3] mb-8">No credit card required</p>
            <ul className="space-y-3 mb-8 flex-1">
              {[
                "10 estimates / month",
                "Should-cost breakdown",
                "Company brain search",
                "MPN part number lookup",
                "DWG, STEP, DXF, PDF & image uploads",
              ].map((f) => (
                <li key={f} className="flex items-center gap-2.5 text-[14px] text-[#525252]">
                  <CheckCircle2 className="w-4 h-4 text-orange-500 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/login"
              className="block w-full py-3.5 rounded-full border border-black/15 text-xs font-bold uppercase tracking-widest text-center text-[#1a1a1a] hover:bg-white transition-colors"
            >
              Get started free
            </Link>
          </div>

          {/* Pro */}
          <div className="p-8 rounded-2xl bg-[#1a1a1a] flex flex-col relative overflow-hidden">
            <div className="absolute top-5 right-5">
              <span className="text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30">
                Most popular
              </span>
            </div>
            <div className="text-[14px] font-bold uppercase tracking-widest text-white/40 mb-3 font-mono">
              Pro
            </div>
            <div className="flex items-baseline gap-1 mb-1">
              <span className="text-5xl font-bold text-white font-mono">
                <R className="text-white">4,999</R>
              </span>
              <span className="text-sm text-white/40">/mo</span>
            </div>
            <p className="text-[14px] text-white/40 mb-8">One corrected quote covers it</p>
            <ul className="space-y-3 mb-8 flex-1">
              {[
                "Unlimited estimates",
                "MPN lookup — market price before you negotiate",
                "AI procurement engine — RFQ, compare, negotiate",
                "Full drawing library with similarity search",
                "Priority support",
                "Team features",
              ].map((f) => (
                <li key={f} className="flex items-center gap-2.5 text-[15px] text-white/80">
                  <CheckCircle2 className="w-4 h-4 text-orange-400 shrink-0" />
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/waitlist"
              className="block w-full py-3.5 rounded-full bg-white text-[#1a1a1a] text-xs font-bold uppercase tracking-widest text-center hover:bg-white/90 transition-colors"
            >
              Join the waitlist
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ══════════════════════════════════════════════════════════
   FOOTER
   ══════════════════════════════════════════════════════════ */
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
            <p className="text-[16px] text-[#1a1a1a]/60 leading-relaxed">
              The price integrity layer for global manufacturing.
            </p>
          </div>

          <div>
            <div className="text-[14px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Company
            </div>
            <ul className="space-y-2.5">
              <li>
                <a
                  href="mailto:chand@costimize.dev"
                  className="text-[16px] text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors"
                >
                  Contact Us
                </a>
              </li>
            </ul>
          </div>

          <div>
            <div className="text-[14px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Product
            </div>
            <ul className="space-y-2.5">
              {[
                { label: "Should-Cost", href: "/estimate/new" },
                { label: "Company Brain", href: "/similar" },
                { label: "AI Procurement", href: "/waitlist" },
              ].map((item) => (
                <li key={item.label}>
                  <Link
                    href={item.href}
                    className="text-[16px] text-[#1a1a1a]/60 hover:text-[#1a1a1a] transition-colors"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="text-[14px] font-bold uppercase tracking-widest text-[#1a1a1a] mb-4">
              Enterprise
            </div>
            <ul className="space-y-2.5">
              {["On-Premise Hosting", "Defense & Aerospace", "Custom Integration"].map((item) => (
                <li key={item}>
                  <span className="text-[16px] text-[#1a1a1a]/60">
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-[#1a1a1a]/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-[#1a1a1a]/40">
            &copy; 2026 Newton-Metre. Price integrity for global manufacturing. Made in India.
          </div>
        </div>
      </div>
    </footer>
  );
}
