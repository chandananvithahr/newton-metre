"use client";

import { useEffect, useRef, useLayoutEffect } from "react";
import Link from "next/link";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { CostBreakdownTable } from "@/components/landing/CostBreakdownTable";
import {
  ArrowRight,
  FileUp,
  Calculator,
  Handshake,
  Search,
  ShieldCheck,
  Layers,
} from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const PRIMARY = "#1E40AF";
const ACCENT = "#2F5EF7";

/* ─────────────────────────────────────────────
   CountUp — animates a number from 0 on scroll
   ───────────────────────────────────────────── */
function CountUp({
  end,
  suffix = "",
  prefix = "",
}: {
  end: number;
  suffix?: string;
  prefix?: string;
}) {
  const ref = useRef<HTMLSpanElement>(null);
  const animated = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const trigger = ScrollTrigger.create({
      trigger: el,
      start: "top 85%",
      onEnter: () => {
        if (animated.current) return;
        animated.current = true;
        const obj = { v: 0 };
        gsap.to(obj, {
          v: end,
          duration: 2,
          ease: "power2.out",
          onUpdate: () => {
            if (ref.current)
              ref.current.textContent = `${prefix}${Math.round(obj.v)}${suffix}`;
          },
        });
      },
    });
    return () => trigger.kill();
  }, [end, prefix, suffix]);

  return (
    <span ref={ref}>
      {prefix}0{suffix}
    </span>
  );
}

/* ─────────────────────────────────────────────
   Main Landing Page
   ───────────────────────────────────────────── */
export default function LandingPage() {
  /* refs for GSAP pinned sections */
  const heroRef = useRef<HTMLDivElement>(null);
  const heroContentRef = useRef<HTMLDivElement>(null);
  const costRef = useRef<HTMLDivElement>(null);
  const costLeftRef = useRef<HTMLDivElement>(null);
  const costCardRef = useRef<HTMLDivElement>(null);
  const uploadRef = useRef<HTMLDivElement>(null);
  const uploadLeftRef = useRef<HTMLDivElement>(null);
  const uploadRightRef = useRef<HTMLDivElement>(null);
  const negotiateRef = useRef<HTMLDivElement>(null);
  const negotiateLeftRef = useRef<HTMLDivElement>(null);
  const negotiateRightRef = useRef<HTMLDivElement>(null);

  /* Hero entrance animation */
  useEffect(() => {
    const ctx = gsap.context(() => {
      // Set initial hidden state via GSAP (not CSS) so SSR renders visible content
      gsap.set(".hero-anim", { opacity: 0 });
      const tl = gsap.timeline({ defaults: { ease: "power3.out" }, delay: 0.1 });
      tl.to(".hero-pill", { opacity: 1, y: 0, duration: 0.4 }, 0);
      tl.fromTo(".hero-h1-1", { y: 40 }, { opacity: 1, y: 0, duration: 0.5 }, 0.15);
      tl.fromTo(".hero-h1-2", { y: 40 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      tl.fromTo(".hero-sub", { y: 18 }, { opacity: 1, y: 0, duration: 0.4 }, 0.55);
      tl.fromTo(".hero-cta", { scale: 0.96 }, { opacity: 1, scale: 1, duration: 0.3 }, 0.75);
    }, heroRef);
    return () => ctx.revert();
  }, []);

  /* Scroll-driven pinned sections */
  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      /* ── Hero pin + exit ── */
      const heroTl = gsap.timeline({
        scrollTrigger: { trigger: heroRef.current, start: "top top", end: "+=120%", pin: true, scrub: 0.6 },
      });
      heroTl.fromTo(heroContentRef.current, { opacity: 1, y: 0 }, { opacity: 0, y: "-8vh", ease: "power2.in" }, 0.7);

      /* ── Cost Breakdown pin ── */
      const costTl = gsap.timeline({
        scrollTrigger: { trigger: costRef.current, start: "top top", end: "+=130%", pin: true, scrub: 0.6 },
      });
      costTl.fromTo(costLeftRef.current, { x: "-40vw", opacity: 0 }, { x: 0, opacity: 1, ease: "none" }, 0);
      costTl.fromTo(costCardRef.current, { x: "50vw", opacity: 0, scale: 0.98 }, { x: 0, opacity: 1, scale: 1, ease: "none" }, 0);
      costTl.fromTo(costLeftRef.current, { x: 0, opacity: 1 }, { x: "-10vw", opacity: 0, ease: "power2.in" }, 0.7);
      costTl.fromTo(costCardRef.current, { x: 0, opacity: 1 }, { x: "-18vw", opacity: 0, ease: "power2.in" }, 0.7);

      /* ── Upload pin ── */
      const uploadTl = gsap.timeline({
        scrollTrigger: { trigger: uploadRef.current, start: "top top", end: "+=130%", pin: true, scrub: 0.6 },
      });
      uploadTl.fromTo(uploadLeftRef.current, { x: "-40vw", opacity: 0 }, { x: 0, opacity: 1, ease: "none" }, 0);
      uploadTl.fromTo(uploadRightRef.current, { x: "50vw", opacity: 0, scale: 1.04 }, { x: 0, opacity: 1, scale: 1, ease: "none" }, 0);
      uploadTl.fromTo(uploadLeftRef.current, { x: 0, opacity: 1 }, { x: "-10vw", opacity: 0, ease: "power2.in" }, 0.7);
      uploadTl.fromTo(uploadRightRef.current, { x: 0, opacity: 1 }, { x: "-10vw", opacity: 0, ease: "power2.in" }, 0.7);

      /* ── Negotiate pin ── */
      const negTl = gsap.timeline({
        scrollTrigger: { trigger: negotiateRef.current, start: "top top", end: "+=130%", pin: true, scrub: 0.6 },
      });
      negTl.fromTo(negotiateLeftRef.current, { x: "-40vw", opacity: 0 }, { x: 0, opacity: 1, ease: "none" }, 0);
      negTl.fromTo(negotiateRightRef.current, { x: "50vw", opacity: 0, scale: 1.04 }, { x: 0, opacity: 1, scale: 1, ease: "none" }, 0);
      negTl.fromTo(negotiateLeftRef.current, { x: 0, opacity: 1 }, { x: "-10vw", opacity: 0, ease: "power2.in" }, 0.7);
      negTl.fromTo(negotiateRightRef.current, { x: 0, opacity: 1 }, { x: "-10vw", opacity: 0, ease: "power2.in" }, 0.7);

      /* ── Flowing sections: scroll-reveal ── */
      gsap.utils.toArray<HTMLElement>(".reveal-up").forEach((el) => {
        gsap.fromTo(el, { y: 30, opacity: 0 }, {
          y: 0, opacity: 1, duration: 0.6,
          scrollTrigger: { trigger: el, start: "top 85%", toggleActions: "play none none reverse" },
        });
      });

      gsap.utils.toArray<HTMLElement>(".stagger-card").forEach((el, i) => {
        gsap.fromTo(el, { y: 40, opacity: 0 }, {
          y: 0, opacity: 1, duration: 0.6, delay: (i % 3) * 0.12,
          scrollTrigger: { trigger: el, start: "top 88%", toggleActions: "play none none reverse" },
        });
      });
    });

    return () => ctx.revert();
  }, []);

  return (
    <div className="relative bg-[#F6F7F9] text-slate-900 antialiased" style={{ fontFamily: "var(--font-inter), 'Inter', sans-serif" }}>

      {/* Grain overlay */}
      <div className="fixed inset-0 pointer-events-none z-[9999] opacity-[0.03] mix-blend-multiply" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
      }} />

      {/* ── Nav ── */}
      <nav className="fixed top-0 left-0 right-0 z-[100] bg-[#F6F7F9]/90 backdrop-blur-md border-b border-slate-900/8">
        <div className="flex justify-between items-center w-full px-6 lg:px-10 h-16 lg:h-20">
          <div className="flex items-center gap-10">
            <Link href="/" className="text-2xl font-black tracking-tighter" style={{ color: PRIMARY }}>
              Costrich
            </Link>
            <div className="hidden lg:flex items-center gap-8">
              {["Problem", "How it works", "Features", "Pricing"].map((l) => (
                <a key={l} href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                  {l}
                </a>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/login" className="hidden sm:block text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors">
              Sign in
            </Link>
            <Link href="/login" className="inline-flex items-center px-5 py-2.5 text-white text-xs font-bold uppercase tracking-wider rounded-full hover:-translate-y-0.5 transition-all" style={{ backgroundColor: ACCENT }}>
              Get started
            </Link>
          </div>
        </div>
      </nav>

      <main className="relative">

        {/* ═══════════════════════════════════════
           PINNED SECTION 1: HERO
           ═══════════════════════════════════════ */}
        <section ref={heroRef} className="relative w-screen h-screen overflow-hidden flex items-center justify-center">
          <div ref={heroContentRef} className="w-[90vw] max-w-6xl text-center space-y-8">
            <div className="hero-anim hero-pill inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-white text-[10px] font-bold uppercase tracking-[0.2em]" style={{ backgroundColor: ACCENT }}>
              <span className="w-1.5 h-1.5 rounded-full bg-white/80 animate-pulse" />
              Live product · Not a waitlist
            </div>

            <h1 className="font-black tracking-tighter leading-[0.95]">
              <div className="hero-anim hero-h1-1 text-[clamp(36px,6vw,80px)] text-slate-900 uppercase">
                Know what it
              </div>
              <div className="hero-anim hero-h1-2 text-[clamp(36px,6vw,80px)] uppercase" style={{ color: PRIMARY }}>
                should cost.
              </div>
            </h1>

            <p className="hero-anim hero-sub max-w-2xl mx-auto text-xl text-slate-500 font-medium">
              From drawing to negotiation brief in 60 seconds.
              Line-by-line cost intelligence for Indian manufacturing procurement.
            </p>

            <div className="hero-anim hero-cta flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/login" className="group inline-flex items-center px-8 py-4 text-white font-black text-lg uppercase tracking-tighter rounded-full shadow-xl hover:-translate-y-0.5 transition-all" style={{ backgroundColor: ACCENT }}>
                Upload a drawing free
                <ArrowRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
              </Link>
              <a href="#cost-breakdown" className="px-8 py-4 bg-white border border-slate-200 text-slate-900 font-black text-lg uppercase tracking-tighter rounded-full hover:bg-slate-50 transition-colors shadow-sm">
                See a live breakdown
              </a>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           PINNED SECTION 2: COST BREAKDOWN
           ═══════════════════════════════════════ */}
        <section id="cost-breakdown" ref={costRef} className="relative w-screen h-screen overflow-hidden flex items-center bg-[#F6F7F9]">
          {/* Left text */}
          <div ref={costLeftRef} className="absolute left-[6vw] top-[18vh] w-[38vw] max-w-[480px]">
            <p className="text-[10px] font-bold uppercase tracking-[0.25em] mb-4" style={{ color: ACCENT }}>
              This is what cost clarity looks like
            </p>
            <h2 className="font-black text-[clamp(28px,3.5vw,48px)] leading-[1.1] tracking-tight text-slate-900 mb-6">
              LINE BY LINE.<br />
              <span style={{ color: PRIMARY }}>PROCESS BY PROCESS.</span>
            </h2>
            <p className="text-slate-500 text-base leading-relaxed mb-6">
              A live breakdown — material, machining, overhead, margin — indexed to real Indian job-shop rates. Click any value to copy it into your negotiation.
            </p>
            <Link href="/login" className="inline-flex items-center text-sm font-medium hover:underline group" style={{ color: ACCENT }}>
              Try with your own drawing
              <ArrowRight className="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" />
            </Link>
          </div>

          {/* Right card */}
          <div ref={costCardRef} className="absolute right-[4vw] top-[10vh] w-[48vw] max-w-[600px] hidden lg:block">
            <div className="bg-white rounded-2xl overflow-hidden" style={{ boxShadow: "0 18px 40px rgba(0,0,0,0.08)" }}>
              <div className="p-5 border-b border-slate-100 flex items-center justify-between">
                <div>
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Should Cost</div>
                  <div className="text-3xl font-black font-mono mt-1" style={{ color: PRIMARY }}>₹695</div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-bold text-red-400 uppercase tracking-widest">Supplier Markup</div>
                  <div className="text-2xl font-black font-mono text-red-500 mt-1">22.4%</div>
                </div>
              </div>
              <CostBreakdownTable />
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           PINNED SECTION 3: UPLOAD (Drawing Intelligence)
           ═══════════════════════════════════════ */}
        <section ref={uploadRef} className="relative w-screen h-screen overflow-hidden flex items-center bg-[#F6F7F9]">
          <div ref={uploadLeftRef} className="absolute left-[6vw] top-[20vh] w-[40vw] max-w-[500px]">
            <p className="text-[10px] font-bold uppercase tracking-[0.25em] mb-4" style={{ color: ACCENT }}>
              Step 01 · Drawing Intelligence
            </p>
            <h2 className="font-black text-[clamp(28px,3.5vw,48px)] leading-[1.1] tracking-tight text-slate-900 mb-6">
              UPLOAD A DRAWING.<br />
              <span style={{ color: PRIMARY }}>GET A NUMBER.</span>
            </h2>
            <p className="text-slate-500 text-base leading-relaxed mb-4">
              PDF, image, any CAD output. Our AI extracts dimensions, material, tolerances, and process requirements — then builds a line-by-line estimate.
            </p>
            <div className="flex flex-wrap gap-2 mb-6">
              {["PDF & images", "Any CAD output", "GD&T extraction", "Under 60 seconds"].map((t) => (
                <span key={t} className="text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-slate-200 text-slate-500">{t}</span>
              ))}
            </div>
          </div>

          <div ref={uploadRightRef} className="absolute right-[6vw] top-[16vh] w-[40vw] max-w-[520px] hidden lg:block">
            <div className="bg-white rounded-2xl p-8 flex flex-col items-center justify-center aspect-[4/3]" style={{ boxShadow: "0 18px 40px rgba(0,0,0,0.08)" }}>
              <FileUp className="w-16 h-16 mb-6" style={{ color: ACCENT }} strokeWidth={1.5} />
              <p className="text-lg font-black text-slate-900 mb-2">Drop your drawing here</p>
              <p className="text-sm text-slate-400 mb-6">PDF, PNG, JPG, STEP, DXF</p>
              <div className="px-6 py-3 rounded-full text-white text-sm font-bold uppercase tracking-wider" style={{ backgroundColor: ACCENT }}>
                Browse files
              </div>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           PINNED SECTION 4: NEGOTIATE
           ═══════════════════════════════════════ */}
        <section ref={negotiateRef} className="relative w-screen h-screen overflow-hidden flex items-center bg-[#F6F7F9]">
          <div ref={negotiateLeftRef} className="absolute left-[6vw] top-[20vh] w-[40vw] max-w-[500px]">
            <p className="text-[10px] font-bold uppercase tracking-[0.25em] mb-4" style={{ color: ACCENT }}>
              Step 02 · Negotiation Brief
            </p>
            <h2 className="font-black text-[clamp(28px,3.5vw,48px)] leading-[1.1] tracking-tight text-slate-900 mb-6">
              NEGOTIATE WITH<br />
              <span style={{ color: PRIMARY }}>DATA,</span> NOT GUESSES.
            </h2>
            <p className="text-slate-500 text-base leading-relaxed mb-6">
              Your supplier quoted ₹850. The physics says ₹695. The breakdown shows the markup is in surface treatment and overhead. Now you know exactly where to push back.
            </p>
            <div className="space-y-3">
              {[
                { before: "You negotiate on total price", after: "You negotiate per cost line" },
                { before: "Supplier says 'best we can do'", after: "You show where they're 40% over" },
                { before: "Senior engineer's gut feel", after: "Physics-based evidence" },
              ].map((r) => (
                <div key={r.before} className="flex gap-3 text-sm">
                  <span className="text-red-400 line-through flex-shrink-0">{r.before}</span>
                  <span className="font-medium" style={{ color: ACCENT }}>{r.after}</span>
                </div>
              ))}
            </div>
          </div>

          <div ref={negotiateRightRef} className="absolute right-[6vw] top-[16vh] w-[40vw] max-w-[520px] hidden lg:block">
            <div className="bg-white rounded-2xl p-8 aspect-[4/3]" style={{ boxShadow: "0 18px 40px rgba(0,0,0,0.08)" }}>
              <div className="text-[10px] font-bold uppercase tracking-widest mb-4" style={{ color: ACCENT }}>Negotiation Brief</div>
              <div className="space-y-3">
                {[
                  { item: "CNC Turning", should: "₹112", quoted: "₹165", delta: "+47%" },
                  { item: "Surface Treatment", should: "₹45", quoted: "₹120", delta: "+167%" },
                  { item: "Overhead", should: "₹76", quoted: "₹95", delta: "+25%" },
                  { item: "Profit Margin", should: "₹116", quoted: "₹180", delta: "+55%" },
                ].map((row) => (
                  <div key={row.item} className="flex items-center justify-between py-2.5 border-b border-slate-100">
                    <span className="text-sm text-slate-600 w-[35%]">{row.item}</span>
                    <span className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{row.should}</span>
                    <span className="text-sm font-mono text-slate-400">{row.quoted}</span>
                    <span className="text-xs font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded-full">{row.delta}</span>
                  </div>
                ))}
              </div>
              <div className="mt-6 flex items-center justify-between px-4 py-3 bg-slate-900 rounded-lg">
                <span className="text-sm text-white/80">Total overcharge</span>
                <span className="text-lg font-black text-red-400 font-mono">+₹155 / unit</span>
              </div>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           FLOWING: Problem Section
           ═══════════════════════════════════════ */}
        <section id="problem" className="relative w-full py-24 bg-[#F6F7F9]">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <div className="reveal-up mb-16 max-w-3xl">
              <p className="text-[10px] font-bold uppercase tracking-[0.25em] mb-4" style={{ color: ACCENT }}>
                The problem
              </p>
              <h2 className="text-[clamp(32px,4vw,52px)] font-black tracking-tight text-slate-900 leading-tight mb-6">
                Three things that break every procurement cycle.
              </h2>
              <p className="text-slate-500 text-lg">
                Every procurement team has the same three problems. All three are still managed manually — by experienced engineers, in spreadsheets, on instinct.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-px bg-slate-200 rounded-2xl overflow-hidden mb-16">
              {[
                { n: "01", title: "You don't know what it should cost", desc: "The supplier quotes ₹850. Is that fair? Your senior engineer says 'seems high.' That's not a negotiation — that's a guess." },
                { n: "02", title: "Every quote comparison is manual", desc: "Three suppliers. Three formats. Someone rebuilds it into a spreadsheet every time — missing the line where one buried a 40% markup." },
                { n: "03", title: "Knowledge walks out the door", desc: "Your best cost estimator has 25 years of experience. When they retire, that knowledge is gone. No record of what past parts should have cost." },
              ].map((s) => (
                <div key={s.n} className="stagger-card bg-white p-10 hover:bg-slate-50 transition-colors">
                  <div className="text-4xl font-black text-slate-200 mb-6 font-mono">{s.n}</div>
                  <h3 className="text-lg font-black mb-4 text-slate-900 leading-snug">{s.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed">{s.desc}</p>
                </div>
              ))}
            </div>

            {/* Stats strip with CountUp */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-slate-200 rounded-2xl overflow-hidden">
              {[
                { value: 22, suffix: "%", label: "Average supplier markup exposed" },
                { value: 60, prefix: "<", suffix: "s", label: "Drawing to full breakdown" },
                { value: 10, suffix: "", label: "Line items per estimate" },
                { value: 164, suffix: "+", label: "Tests validating the engine" },
              ].map((s) => (
                <div key={s.label} className="stagger-card bg-white p-8 text-center">
                  <div className="text-3xl font-black font-mono mb-2" style={{ color: ACCENT }}>
                    <CountUp end={s.value} suffix={s.suffix} prefix={s.prefix || ""} />
                  </div>
                  <div className="text-xs text-slate-500 leading-relaxed">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           FLOWING: Who it's for
           ═══════════════════════════════════════ */}
        <section className="relative w-full py-20 bg-white border-y border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <p className="reveal-up text-[10px] font-bold uppercase tracking-[0.25em] mb-6" style={{ color: ACCENT }}>
              Built for both sides of the table
            </p>
            <div className="grid md:grid-cols-2 gap-0 border border-slate-200 rounded-2xl overflow-hidden">
              {[
                {
                  persona: "BUYER",
                  title: "You send drawings",
                  desc: "OEM or mid-tier. You issue RFQs, negotiate, and need to know if the quoted price is fair — before you sign.",
                  points: ["Should-cost before negotiation", "Line-by-line markup exposure", "Historical cost comparison"],
                },
                {
                  persona: "SUPPLIER",
                  title: "You receive drawings",
                  desc: "Tier 2 or 3 shop. You quote on drawings and win jobs on speed and accuracy. Costrich structures your cost model in minutes.",
                  points: ["Instant cost model from drawing", "Structured quote in minutes", "Win on speed, not guesswork"],
                },
              ].map((p, i) => (
                <div key={p.persona} className={`stagger-card p-10 hover:bg-slate-50 transition-colors ${i === 0 ? "border-b md:border-b-0 md:border-r border-slate-200" : ""}`}>
                  <div className="text-3xl font-black text-slate-200 mb-4 font-mono">{p.persona}</div>
                  <h3 className="text-xl font-black uppercase tracking-tight text-slate-900 mb-3">{p.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed mb-6">{p.desc}</p>
                  <ul className="space-y-2">
                    {p.points.map((pt) => (
                      <li key={pt} className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest" style={{ color: ACCENT }}>
                        <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
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

        {/* ═══════════════════════════════════════
           FLOWING: Features (Not another AI wrapper)
           ═══════════════════════════════════════ */}
        <section id="features" className="relative w-full py-24 bg-[#F6F7F9]">
          <div className="max-w-6xl mx-auto px-6 lg:px-10">
            <h2 className="reveal-up text-[clamp(32px,4vw,52px)] font-black tracking-tight text-slate-900 mb-4">
              Not another <span style={{ color: PRIMARY }}>AI wrapper.</span>
            </h2>
            <p className="reveal-up text-slate-500 text-lg mb-16 max-w-2xl">
              Built on Sandvik cutting data, Machinery&apos;s Handbook, Kennametal power constants, and Indian MSME machine hour rates. Physics, not prompt engineering.
            </p>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-px bg-slate-200 rounded-2xl overflow-hidden">
              {[
                { Icon: FileUp, title: "Drawing Intelligence", desc: "Upload any engineering drawing — PDF, image, any CAD output. AI extracts dimensions, material, tolerances, and processes automatically." },
                { Icon: Calculator, title: "Should-Cost Engine", desc: "Physics-based: cycle times from real cutting parameters, Indian machine rates (₹600-1500/hr), Taylor tool wear. 18 manufacturing processes." },
                { Icon: Handshake, title: "Negotiation Briefs", desc: "Every estimate is a line-by-line breakdown — material, machining, setup, tooling, labour, overhead, margin. Walk in with facts." },
                { Icon: ShieldCheck, title: "AI Validation", desc: "Physics engine and AI run in parallel. >15% gap triggers AI arbitration. Four confidence tiers. Self-correcting." },
                { Icon: Search, title: "Cost Baseline Memory", desc: "Every estimate saved. Compare new quotes against historical baselines. Match similar parts. Knowledge that doesn't retire." },
                { Icon: Layers, title: "4 Part Types", desc: "Turned, milled, sheet metal, PCB, cable. 40+ surface treatments. 15 heat treatments. Defense, aerospace, automobile." },
              ].map((f) => (
                <div key={f.title} className="stagger-card bg-white p-8 hover:bg-slate-50 transition-colors group">
                  <div className="w-10 h-10 rounded-full flex items-center justify-center mb-5 transition-colors" style={{ backgroundColor: `${ACCENT}15` }}>
                    <f.Icon className="w-5 h-5" style={{ color: ACCENT }} />
                  </div>
                  <h3 className="font-black text-sm uppercase tracking-widest mb-3" style={{ color: ACCENT }}>{f.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>

            <div className="mt-12 py-6 border-t border-slate-200">
              <p className="text-center text-xs text-slate-400 uppercase tracking-widest">
                Powered by Sandvik Coromant · Kennametal · Machinery&apos;s Handbook · CMTI Machine Hour Rates · BIS Standards
              </p>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           FLOWING: Pricing
           ═══════════════════════════════════════ */}
        <section id="pricing" className="relative w-full py-24 bg-white border-t border-slate-200">
          <div className="max-w-5xl mx-auto px-6 lg:px-10 text-center">
            <h2 className="reveal-up text-[clamp(32px,4vw,52px)] font-black tracking-tight text-slate-900 mb-16">
              Start free. Scale when ready.
            </h2>

            <div className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto text-left">
              <div className="stagger-card bg-[#F6F7F9] border border-slate-200 rounded-2xl p-8">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 font-mono">Free</p>
                <p className="text-4xl font-black text-slate-900 font-mono mb-1">₹0</p>
                <p className="text-sm text-slate-400 mb-8">No credit card. No setup. Just upload.</p>
                <div className="space-y-3 mb-8">
                  {["10 estimates / month", "Mechanical + sheet metal", "PDF & image uploads", "Full line-by-line breakdown", "Similarity search"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 text-sm text-slate-600">
                      <span className="font-black" style={{ color: ACCENT }}>✓</span> {f}
                    </div>
                  ))}
                </div>
                <Link href="/login" className="block text-center text-white px-6 py-3 rounded-full font-bold uppercase tracking-tight hover:opacity-90 transition-opacity" style={{ backgroundColor: ACCENT }}>
                  Get started free
                </Link>
              </div>

              <div className="stagger-card rounded-2xl p-8 relative overflow-hidden text-white" style={{ backgroundColor: ACCENT }}>
                <div className="absolute top-4 right-4 bg-amber-400 text-amber-900 text-xs font-black px-2 py-0.5 rounded-full uppercase">Coming soon</div>
                <p className="text-xs font-bold text-white/60 uppercase tracking-widest mb-1 font-mono">Pro</p>
                <p className="text-4xl font-black text-white font-mono mb-1">₹4,999</p>
                <p className="text-sm text-white/60 mb-8">per user / month</p>
                <div className="space-y-3 mb-8">
                  {["Unlimited estimates", "PCB + cable assembly", "Persistent cost memory", "Team cost baselines", "Excel / PDF export", "Priority support"].map((f) => (
                    <div key={f} className="flex items-center gap-2.5 text-sm text-white/90">
                      <span className="text-white font-black">✓</span> {f}
                    </div>
                  ))}
                </div>
                <button disabled className="block w-full text-center bg-white/10 text-white/40 px-6 py-3 rounded-full font-bold uppercase tracking-tight cursor-not-allowed">
                  Join waitlist
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════
           FLOWING: Final CTA
           ═══════════════════════════════════════ */}
        <section className="relative w-full py-24 lg:py-32 bg-[#0B0D10]">
          <div className="max-w-3xl mx-auto px-6 lg:px-10 text-center">
            <h2 className="reveal-up text-[clamp(36px,5vw,64px)] font-black tracking-tight text-white leading-tight mb-6">
              Your supplier quoted ₹850.<br />
              The physics says <span style={{ color: ACCENT }}>₹695.</span>
            </h2>
            <p className="reveal-up text-lg text-white/50 leading-relaxed mb-10">
              Upload a drawing. Get the full should-cost breakdown in 60 seconds. Walk into the negotiation knowing exactly where to push back.
            </p>
            <Link href="/login" className="reveal-up inline-flex items-center justify-center px-8 py-4 bg-white text-slate-900 font-bold rounded-full hover:-translate-y-0.5 transition-all group" style={{ boxShadow: "0 8px 32px rgba(255,255,255,0.15)" }}>
              Try Costrich free
              <ArrowRight className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
            </Link>
            <p className="mt-8 text-xs text-white/30 uppercase tracking-widest font-mono">
              No credit card · No setup · Upload and go
            </p>
          </div>
        </section>

      </main>

      {/* ── Footer ── */}
      <footer className="w-full bg-[#F6F7F9] border-t border-slate-200 py-16">
        <div className="max-w-6xl mx-auto px-6 lg:px-10 grid grid-cols-2 md:grid-cols-4 gap-12">
          <div className="col-span-2 space-y-4">
            <span className="text-xl font-black tracking-tighter" style={{ color: PRIMARY }}>Costrich</span>
            <p className="text-slate-500 text-sm max-w-sm">
              The cost intelligence engine for Indian manufacturing procurement. Physics-based. Line-by-line. Built for negotiation.
            </p>
          </div>
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-widest" style={{ color: ACCENT }}>Product</h4>
            <ul className="space-y-2 text-sm text-slate-500">
              {["Problem", "How it works", "Features", "Pricing"].map((l) => (
                <li key={l}><a href={`#${l.toLowerCase().replace(/ /g, "-")}`} className="hover:text-slate-800 transition-colors">{l}</a></li>
              ))}
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-widest" style={{ color: ACCENT }}>Account</h4>
            <ul className="space-y-2 text-sm text-slate-500">
              <li><Link href="/login" className="hover:text-slate-800 transition-colors">Sign in</Link></li>
              <li><Link href="/login" className="hover:text-slate-800 transition-colors">Get started free</Link></li>
            </ul>
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-6 lg:px-10 mt-12 pt-8 border-t border-slate-200 flex justify-between items-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">
          <span>&copy; 2026 Costrich. Built for Indian manufacturing.</span>
          <div className="flex gap-4">
            <a href="#" className="hover:text-slate-600 transition-colors">Privacy</a>
            <a href="#" className="hover:text-slate-600 transition-colors">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
