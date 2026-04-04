"use client";

import { useState } from "react";
import Link from "next/link";
import { createClient } from "@/lib/supabase";

export default function WaitlistPage() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");

  const roles = [
    "Procurement / Sourcing",
    "Design Engineering",
    "Finance",
    "Quality",
    "Supply Planning",
    "Leadership / Management",
    "Other",
  ];

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const supabase = createClient();
      const { error: err } = await supabase.from("waitlist").insert({
        email,
        full_name: fullName,
        company,
        role,
        product: "procurement-brain",
      });
      if (err) throw err;
      setDone(true);
    } catch {
      // Fallback: try storing via auth metadata if table doesn't exist yet
      try {
        const supabase = createClient();
        await supabase.auth.signUp({
          email,
          password: Math.random().toString(36).slice(-12) + "Nm1!",
          options: {
            emailRedirectTo: `${window.location.origin}/auth/callback`,
            data: {
              full_name: fullName,
              company,
              role,
              waitlist_product: "procurement-brain",
              waitlist_only: true,
            },
          },
        });
        setDone(true);
      } catch {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col warm-gradient-page">
      {/* Nav */}
      <nav className="flex items-center px-8 py-5 border-b border-black/5 bg-white/60 backdrop-blur-sm">
        <Link href="/" className="flex items-center gap-3">
          <div className="relative w-9 h-9 flex items-center justify-center">
            <div className="absolute inset-0 bg-[var(--color-brand-dark)] rounded-xl" />
            <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
          </div>
          <span className="text-[var(--color-brand-dark)] text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-body)" }}>
            Newton-Metre
          </span>
        </Link>
      </nav>

      <div className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="w-full max-w-lg">
          {done ? (
            <div className="bg-white rounded-2xl border border-black/6 p-10 text-center">
              <div className="w-14 h-14 bg-orange-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-7 h-7 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold text-[#1a1a1a] mb-3 tracking-tight" style={{ fontFamily: "var(--font-body)" }}>
                You&apos;re on the list.
              </h1>
              <p className="text-[#525252] text-sm leading-relaxed mb-2" style={{ fontFamily: "var(--font-body)" }}>
                We&apos;ll reach out to <span className="font-medium text-[#1a1a1a]">{email}</span> when Procurement Intel goes live.
              </p>
              <p className="text-[#A3A3A3] text-xs mb-8" style={{ fontFamily: "var(--font-body)" }}>
                We'll reach out when it's ready for you.
              </p>
              <Link
                href="/"
                className="inline-flex items-center gap-2 text-sm font-medium text-[#1a1a1a] hover:text-[#525252] transition-colors"
                style={{ fontFamily: "var(--font-body)" }}
              >
                ← Back to Newton-Metre
              </Link>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-black/6 p-10">
              {/* Header */}
              <div className="mb-8">
                <span className="inline-block text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60 mb-4">
                  Live · Free to try
                </span>
                <h1 className="text-[28px] font-bold text-[#1a1a1a] leading-tight tracking-tight mb-2" style={{ fontFamily: "var(--font-body)" }}>
                  Procurement Intel
                </h1>
                <p className="text-[#525252] text-sm leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                  Know the market price before the supplier emails you. Live MPN lookup, negotiation headroom, supplier options — so you walk in with numbers, not assumptions.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label className="block text-[11px] font-bold text-[#525252] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-body)" }}>
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    placeholder="Your full name"
                    className="w-full px-4 py-3 border-b border-black/20 bg-transparent outline-none text-sm text-[#1a1a1a] placeholder:text-[#A3A3A3] focus:border-[#1a1a1a] transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#525252] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-body)" }}>
                    Work Email
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="your@company.com"
                    className="w-full px-4 py-3 border-b border-black/20 bg-transparent outline-none text-sm text-[#1a1a1a] placeholder:text-[#A3A3A3] focus:border-[#1a1a1a] transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#525252] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-body)" }}>
                    Company
                  </label>
                  <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    required
                    placeholder="Company name"
                    className="w-full px-4 py-3 border-b border-black/20 bg-transparent outline-none text-sm text-[#1a1a1a] placeholder:text-[#A3A3A3] focus:border-[#1a1a1a] transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-[#525252] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-body)" }}>
                    Your Role
                  </label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    required
                    className="w-full px-4 py-3 border-b border-black/20 bg-transparent outline-none text-sm text-[#1a1a1a] focus:border-[#1a1a1a] transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    <option value="" disabled>Select your role</option>
                    {roles.map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>

                {error && (
                  <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-[#1a1a1a] text-white py-4 rounded-full font-bold tracking-widest uppercase text-xs disabled:opacity-30 transition-all duration-200 mt-2 hover:bg-[#333]"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Requesting access...
                    </span>
                  ) : "Get early access"}
                </button>
              </form>

              <p className="text-[10px] text-[#A3A3A3] text-center mt-5" style={{ fontFamily: "var(--font-body)" }}>
                No spam. We&apos;ll only contact you when it&apos;s ready.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
