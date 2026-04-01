"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
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
    <div className="min-h-screen flex flex-col bg-[#F8F8F6]">
      {/* Nav */}
      <nav className="flex items-center px-8 py-5 border-b border-slate-200 bg-white">
        <Link href="/" className="flex items-center gap-2.5">
          <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={36} height={36} className="rounded-xl" />
          <span className="text-xl tracking-tight text-cyan-600 py-2" style={{ fontFamily: "var(--font-heading)" }}>
            Newton-Metre
          </span>
        </Link>
      </nav>

      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">
            {emailSent ? (
              <div className="text-center py-4">
                <div className="w-12 h-12 bg-cyan-50 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                </div>
                <h1 className="text-2xl mb-2 tracking-tight text-slate-900">Check your email</h1>
                <p className="text-slate-500 text-sm mb-6">
                  We sent a confirmation link to <span className="font-medium text-slate-700">{email}</span>.
                  Click the link to activate your account, then come back to log in.
                </p>
                <button
                  onClick={() => { setEmailSent(false); setIsSignUp(false); }}
                  className="text-cyan-600 hover:text-cyan-700 text-sm font-medium transition-colors"
                >
                  Back to log in
                </button>
              </div>
            ) : (
              <>
                <h1 className="text-2xl mb-1 text-center tracking-tight text-slate-900">
                  {isSignUp ? "Create your account" : "Welcome back"}
                </h1>
                <p className="text-slate-500 text-sm text-center mb-8">
                  {isSignUp ? "Start estimating costs in under a minute." : "Log in to continue."}
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                  {isSignUp && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1.5">Full Name</label>
                        <input
                          type="text"
                          value={fullName}
                          onChange={(e) => setFullName(e.target.value)}
                          required
                          className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-white outline-none text-sm text-slate-900 placeholder:text-slate-400"
                          placeholder="Your full name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1.5">Company</label>
                        <input
                          type="text"
                          value={company}
                          onChange={(e) => setCompany(e.target.value)}
                          required
                          className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-white outline-none text-sm text-slate-900 placeholder:text-slate-400"
                          placeholder="Company name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1.5">Sourcing Country</label>
                        <select
                          value={country}
                          onChange={(e) => setCountry(e.target.value)}
                          className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-white outline-none text-sm text-slate-900"
                        >
                          {countries.map((c) => (
                            <option key={c} value={c}>{c}</option>
                          ))}
                        </select>
                      </div>
                    </>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1.5">Email</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-white outline-none text-sm text-slate-900 placeholder:text-slate-400"
                      placeholder="your@email.com"
                      autoComplete={isSignUp ? "off" : "email"}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength={6}
                      className="w-full px-4 py-3 border border-slate-200 rounded-lg bg-white outline-none text-sm text-slate-900 placeholder:text-slate-400"
                      placeholder="At least 6 characters"
                      autoComplete={isSignUp ? "new-password" : "current-password"}
                    />
                  </div>

                  {error && (
                    <div role="alert" className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm">
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-cyan-600 text-white py-3 rounded-lg font-semibold hover:bg-cyan-700 disabled:opacity-50 transition-colors mt-2"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center gap-2">
                        <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Please wait...
                      </span>
                    ) : isSignUp ? "Create Account" : "Log In"}
                  </button>
                </form>

                <div className="mt-6 text-center">
                  <button
                    onClick={() => { setIsSignUp(!isSignUp); setError(""); }}
                    className="text-cyan-600 hover:text-cyan-700 text-sm font-medium py-3 px-4 transition-colors"
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
