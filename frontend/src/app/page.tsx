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
function Hero() {
  return (
    <section className="pt-40 pb-24 px-4 sm:px-8 warm-gradient-hero">
      <div className="max-w-[720px] mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-5xl lg:text-[64px] font-bold text-[#1a1a1a] leading-[1.08] tracking-tight mb-6">
            Know what it costs.
            <br />
            Before they quote.
          </h1>

          <div className="max-w-[600px] mx-auto mb-10 space-y-3 text-lg text-[#525252] leading-relaxed">
            <p>Should-cost in 30 seconds.</p>
            <p>Every drawing, PO, and spec your company ever created &mdash; searchable.</p>
            <p>Drop one file for instant insight, or upload your entire history.</p>
            <p>AI that surfaces what your team would never find.</p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-10">
            <Link
              href="/estimate/new"
              className="dark-pill inline-flex items-center gap-2 px-8 py-4 text-xs font-bold uppercase tracking-widest"
            >
              Upload a Drawing <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="#capabilities"
              className="text-sm text-[#525252] hover:text-[#1a1a1a] transition-colors inline-flex items-center gap-1.5"
            >
              See how it works <ArrowRight className="w-3.5 h-3.5" />
            </a>
          </div>

          <p className="text-[11px] text-[#525252] uppercase tracking-[0.15em] font-medium mb-4">
            Three products. One platform.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            {[
              { label: "Should-Cost Estimate", href: "/estimate/new" },
              { label: "Similarity Search", href: "/similar" },
              { label: "AI Procurement", href: "/login" },
            ].map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className="px-5 py-2.5 rounded-full border border-black/8 bg-white/80 text-sm text-[#525252] hover:bg-white hover:border-black/15 transition-all"
              >
                {item.label}
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
        </div>

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
              desc: "60% of part numbers in a typical manufacturing database are duplicates. Each redundant part costs $4,500–7,500/year in carrying costs.",
            },
            {
              stat: "70%",
              label: "Spend is off-the-shelf",
              desc: "70% of procurement spend is on bought-out MPN items. Your company\u2019s negotiation history for these is trapped in email threads and spreadsheets.",
            },
          ].map((item, i) => (
            <div
              key={i}
              className="p-8 rounded-2xl bg-white border border-black/5 h-full flex flex-col"
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
    <section id="capabilities" className="py-28 px-4 sm:px-8 warm-gradient-subtle">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid lg:grid-cols-2 gap-20 items-center">
          <div>
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
              finishing, overhead — in 30 seconds. Not days. Companies save
              8–12% on the first quote they challenge.
            </p>
            <Link
              href="/estimate/new"
              className="dark-pill inline-flex items-center gap-2 px-8 py-4 text-xs font-bold uppercase tracking-widest"
            >
              Upload a Drawing <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

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
              desc: "Your supplier quoted ₹48,000. The should-cost is ₹29,400. That\u2019s ₹18,600 back per part.",
            },
            {
              title: "Cost Engineering",
              desc: "Should-cost in minutes, not days. Every line item defensible in an audit.",
            },
            {
              title: "Design Engineering",
              desc: "See the cost impact of every design choice before it reaches procurement.",
            },
            {
              title: "Leadership",
              desc: "See total overpayment across your supply base. Know which suppliers are competitive.",
            },
          ].map((item, i) => (
            <div
              key={i}
              className="p-8 rounded-2xl border border-black/5 bg-[#f9fafb] hover:bg-white hover:border-black/15 transition-all h-full flex flex-col"
            >
              <CheckCircle2 className="w-5 h-5 text-orange-500 mb-5" />
              <div className="text-[11px] font-bold text-[#1a1a1a] uppercase tracking-widest mb-3">
                {item.title}
              </div>
              <p className="text-[15px] text-[#525252] leading-relaxed flex-1">
                {item.desc}
              </p>
            </div>
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
        <div className="text-center max-w-3xl mx-auto mb-20">
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
        </div>

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
            ].map((item, i) => (
              <div
                key={i}
                className="relative pl-8 border-l border-white/10 hover:border-l-orange-500/50 transition-colors"
              >
                <div className="text-[11px] font-bold text-white/30 uppercase tracking-widest mb-2">
                  {item.dept}
                </div>
                <div className="text-xl font-bold mb-3">{item.title}</div>
                <p className="text-white/50 text-[15px] leading-relaxed">
                  {item.desc}
                </p>
              </div>
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
        <div className="text-center mb-16">
          <div className="text-[11px] tracking-widest text-white/20 uppercase font-bold mb-8 font-mono">
            03 / 03 · Coming Soon · Enterprise
          </div>

          <h2 className="text-4xl sm:text-5xl font-bold text-white tracking-tight leading-tight mb-6">
            Better decisions. Faster.
          </h2>

          <p className="text-lg text-white/40 leading-relaxed max-w-[640px] mx-auto">
            Your company&apos;s PO history, vendor master, negotiation
            transcripts, and approval templates &mdash; turned into live
            intelligence. AI reads your data. You make the call.
          </p>
        </div>

        {/* Two columns: off-the-shelf + negotiation intelligence */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {/* Off-the-shelf procurement */}
          <div className="bg-white/5 rounded-2xl p-8 border border-white/5">
            <div className="text-[11px] font-bold text-white/30 uppercase tracking-widest mb-4 font-mono">
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
                  className="border-l-2 border-white/10 pl-5 py-1 text-white/40 text-[15px] leading-relaxed"
                >
                  {line}
                </div>
              ))}
            </div>
          </div>

          {/* Negotiation intelligence */}
          <div className="bg-white/5 rounded-2xl p-8 border border-white/5">
            <div className="text-[11px] font-bold text-white/30 uppercase tracking-widest mb-4 font-mono">
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
                  className="border-l-2 border-white/10 pl-5 py-1 text-white/40 text-[15px] leading-relaxed"
                >
                  {line}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom: compounding moat */}
        <div className="text-center">
          <p className="text-white/30 text-sm mb-8 max-w-lg mx-auto">
            Every interaction makes the system smarter. Alternate approvals,
            negotiation outcomes, vendor performance, price trends &mdash; your
            company&apos;s institutional memory, compounding with every deal.
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
