"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase";

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [country, setCountry] = useState("India");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const countries = [
    "India", "China", "Vietnam", "Thailand", "Taiwan",
    "South Korea", "Japan", "Germany", "USA", "UK", "Other",
  ];

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const supabase = createClient();

    if (isSignUp) {
      const { error: signUpError } = await supabase.auth.signUp({
        email,
        password,
        options: {
          emailRedirectTo: `${window.location.origin}/auth/callback`,
          data: {
            full_name: fullName,
            company,
            sourcing_country: country,
          },
        },
      });
      if (signUpError) {
        setError(signUpError.message);
        setLoading(false);
        return;
      }
      setLoading(false);
      setEmailSent(true);
      return;
    } else {
      const { error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (signInError) {
        setError(signInError.message);
        setLoading(false);
        return;
      }
    }

    router.push("/dashboard");
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#0F1117]">
      {/* Nav */}
      <nav className="flex items-center px-8 py-5 border-b border-[#2A3140]">
        <Link href="/" className="text-xl tracking-tight text-[#22D3EE] py-2" style={{ fontFamily: "var(--font-heading)" }}>
          Costrich
        </Link>
      </nav>

      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-[#161B27] rounded-2xl border border-[#2A3140] p-8">
            {emailSent ? (
              <div className="text-center py-4">
                <div className="w-12 h-12 bg-[#22D3EE]/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-[#22D3EE]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                </div>
                <h1 className="text-2xl mb-2 tracking-tight text-[#E2E8F0]">Check your email</h1>
                <p className="text-[#64748B] text-sm mb-6">
                  We sent a confirmation link to <span className="font-medium text-[#94A3B8]">{email}</span>.
                  Click the link to activate your account, then come back to log in.
                </p>
                <button
                  onClick={() => { setEmailSent(false); setIsSignUp(false); }}
                  className="text-[#22D3EE] hover:text-[#06B6D4] text-sm font-medium transition-colors"
                >
                  Back to log in
                </button>
              </div>
            ) : (
              <>
                <h1 className="text-2xl mb-1 text-center tracking-tight text-[#E2E8F0]">
                  {isSignUp ? "Create your account" : "Welcome back"}
                </h1>
                <p className="text-[#64748B] text-sm text-center mb-8">
                  {isSignUp ? "Start estimating costs in under a minute." : "Log in to continue."}
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                  {isSignUp && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-[#94A3B8] mb-1.5">Full Name</label>
                        <input
                          type="text"
                          value={fullName}
                          onChange={(e) => setFullName(e.target.value)}
                          required
                          className="w-full px-4 py-3 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0] placeholder:text-[#475569]"
                          placeholder="Your full name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-[#94A3B8] mb-1.5">Company</label>
                        <input
                          type="text"
                          value={company}
                          onChange={(e) => setCompany(e.target.value)}
                          required
                          className="w-full px-4 py-3 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0] placeholder:text-[#475569]"
                          placeholder="Company name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-[#94A3B8] mb-1.5">Sourcing Country</label>
                        <select
                          value={country}
                          onChange={(e) => setCountry(e.target.value)}
                          className="w-full px-4 py-3 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0]"
                        >
                          {countries.map((c) => (
                            <option key={c} value={c}>{c}</option>
                          ))}
                        </select>
                      </div>
                    </>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-[#94A3B8] mb-1.5">Email</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full px-4 py-3 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0] placeholder:text-[#475569]"
                      placeholder="you@company.com"
                      autoComplete={isSignUp ? "off" : "email"}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-[#94A3B8] mb-1.5">Password</label>
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength={6}
                      className="w-full px-4 py-3 border border-[#2A3140] rounded-lg bg-[#1C2235] outline-none text-sm text-[#E2E8F0] placeholder:text-[#475569]"
                      placeholder="At least 6 characters"
                      autoComplete={isSignUp ? "new-password" : "current-password"}
                    />
                  </div>

                  {error && (
                    <div role="alert" className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm">
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-[#22D3EE] text-[#0F1117] py-3 rounded-lg font-semibold hover:bg-[#06B6D4] disabled:opacity-50 transition-colors mt-2"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center gap-2">
                        <span className="w-4 h-4 border-2 border-[#0F1117]/30 border-t-[#0F1117] rounded-full animate-spin" />
                        Please wait...
                      </span>
                    ) : isSignUp ? "Create Account" : "Log In"}
                  </button>
                </form>

                <div className="mt-6 text-center">
                  <button
                    onClick={() => { setIsSignUp(!isSignUp); setError(""); }}
                    className="text-[#22D3EE] hover:text-[#06B6D4] text-sm font-medium py-3 px-4 transition-colors"
                  >
                    {isSignUp ? "Already have an account? Log in" : "Need an account? Sign up"}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
