"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { createClient } from "@/lib/supabase";

function friendlyAuthError(message: string): string {
  const lower = message.toLowerCase();
  if (lower.includes("invalid login credentials"))
    return "Incorrect email or password. Please try again.";
  if (lower.includes("email not confirmed"))
    return "Please confirm your email before logging in. Check your inbox (and spam folder).";
  if (lower.includes("user already registered"))
    return "This email is already registered. Try logging in instead.";
  if (lower.includes("password") && lower.includes("characters"))
    return "Password must be at least 6 characters.";
  if (lower.includes("rate limit") || lower.includes("too many"))
    return "Too many attempts. Please wait a moment and try again.";
  if (lower.includes("network") || lower.includes("fetch"))
    return "Connection error. Please check your internet and try again.";
  return message;
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginContent />
    </Suspense>
  );
}

function LoginContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isSignUp, setIsSignUp] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [country, setCountry] = useState("India");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [resendSuccess, setResendSuccess] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const redirectTo = searchParams.get("redirect");

  useEffect(() => {
    const callbackError = searchParams.get("error");
    if (callbackError) {
      setError(callbackError);
      setIsSignUp(false);
    }
    // If redirected from a protected page, show login form (not signup)
    if (searchParams.get("redirect")) {
      setIsSignUp(false);
    }
  }, [searchParams]);

  const countries = [
    "India", "China", "Vietnam", "Thailand", "Taiwan",
    "South Korea", "Japan", "Germany", "USA", "UK", "Other",
  ];

  async function handleResendConfirmation() {
    setResending(true);
    setError("");
    setResendSuccess(false);
    try {
      const supabase = createClient();
      const { error: resendError } = await supabase.auth.resend({
        type: "signup",
        email,
        options: {
          emailRedirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (resendError) {
        setError(friendlyAuthError(resendError.message));
      } else {
        setError("");
        setResendSuccess(true);
        setTimeout(() => setResendSuccess(false), 5000);
      }
    } catch {
      setError("Failed to resend. Please try again in a moment.");
    } finally {
      setResending(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const supabase = createClient();

      if (isSignUp) {
        const { data, error: signUpError } = await supabase.auth.signUp({
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
          setError(friendlyAuthError(signUpError.message));
          setLoading(false);
          return;
        }
        if (data.user && data.user.identities && data.user.identities.length === 0) {
          setError("This email is already registered. Try logging in instead, or check your inbox for a confirmation link.");
          setIsSignUp(false);
          setLoading(false);
          return;
        }
        setLoading(false);
        setEmailSent(true);
        return;
      }

      const { error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (signInError) {
        setError(friendlyAuthError(signInError.message));
        setLoading(false);
        return;
      }

      router.push(redirectTo || "/dashboard");
    } catch {
      setError("Something went wrong. Please check your connection and try again.");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col warm-gradient-page">
      {/* Nav */}
      <nav className="flex items-center px-8 py-5 border-b border-black/5 bg-white/60 backdrop-blur-sm">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative w-9 h-9 flex items-center justify-center">
            <div className="absolute inset-0 bg-[#1a1a1a] rounded-xl" />
            <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
          </div>
          <span className="text-[#1a1a1a] text-xl font-semibold tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>
            Newton-Metre
          </span>
        </Link>
      </nav>

      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-xl ghost-border ambient-shadow p-8">
            {emailSent ? (
              <div className="text-center py-4">
                <div className="w-12 h-12 bg-[#1a1a1a]/5 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-[#1a1a1a]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                </div>
                <h1 className="text-2xl mb-2 tracking-tight text-[#1a1b20]" style={{ fontFamily: "var(--font-headline)" }}>Check your email</h1>
                <p className="text-[#515f74] text-sm mb-2" style={{ fontFamily: "var(--font-body)" }}>
                  We sent a confirmation link to <span className="font-medium text-[#1a1b20]">{email}</span>.
                  Click the link to activate your account, then come back to log in.
                </p>
                <p className="text-[#757684] text-xs mb-6" style={{ fontFamily: "var(--font-body)" }}>
                  Don&apos;t see it? Check your spam/junk folder.
                </p>
                <div className="flex flex-col items-center gap-3">
                  <button
                    onClick={handleResendConfirmation}
                    disabled={resending}
                    className="text-[#1a1a1a] hover:text-[#374151] text-sm font-medium transition-colors disabled:opacity-50"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {resending ? "Sending..." : "Resend confirmation email"}
                  </button>
                  <button
                    onClick={() => { setEmailSent(false); setIsSignUp(false); setError(""); }}
                    className="text-[#757684] hover:text-[#1a1b20] text-sm transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    Back to log in
                  </button>
                </div>
                {resendSuccess && (
                  <div className="mt-4 bg-green-50 border border-green-200 rounded-lg px-4 py-3 text-green-700 text-sm">
                    Confirmation email resent. Check your inbox.
                  </div>
                )}
                {error && (
                  <div role="alert" className="mt-4 bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm">
                    {error}
                  </div>
                )}
              </div>
            ) : (
              <>
                <h1 className="text-2xl mb-1 text-center tracking-tight text-[#1a1b20] font-bold" style={{ fontFamily: "var(--font-headline)" }}>
                  {isSignUp ? "Create your account" : "Welcome back"}
                </h1>
                <p className="text-[#515f74] text-sm text-center mb-8" style={{ fontFamily: "var(--font-body)" }}>
                  {isSignUp ? "Start estimating costs in under a minute." : "Log in to continue."}
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                  {isSignUp && (
                    <>
                      <div>
                        <label className="block text-[11px] font-bold text-[#515f74] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-label)" }}>Full Name</label>
                        <input
                          type="text"
                          value={fullName}
                          onChange={(e) => setFullName(e.target.value)}
                          required
                          className="w-full px-4 py-3 border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20] placeholder:text-[#c4c5d5] focus:border-[#1a1a1a] transition-colors"
                          style={{ fontFamily: "var(--font-body)" }}
                          placeholder="Your full name"
                        />
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-[#515f74] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-label)" }}>Company</label>
                        <input
                          type="text"
                          value={company}
                          onChange={(e) => setCompany(e.target.value)}
                          required
                          className="w-full px-4 py-3 border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20] placeholder:text-[#c4c5d5] focus:border-[#1a1a1a] transition-colors"
                          style={{ fontFamily: "var(--font-body)" }}
                          placeholder="Company name"
                        />
                      </div>
                      <div>
                        <label className="block text-[11px] font-bold text-[#515f74] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-label)" }}>Country</label>
                        <select
                          value={country}
                          onChange={(e) => setCountry(e.target.value)}
                          className="w-full px-4 py-3 border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20] focus:border-[#1a1a1a] transition-colors"
                          style={{ fontFamily: "var(--font-body)" }}
                        >
                          {countries.map((c) => (
                            <option key={c} value={c}>{c}</option>
                          ))}
                        </select>
                      </div>
                    </>
                  )}

                  <div>
                    <label className="block text-[11px] font-bold text-[#515f74] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-label)" }}>Email</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full px-4 py-3 border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20] placeholder:text-[#c4c5d5] focus:border-[#1a1a1a] transition-colors"
                      style={{ fontFamily: "var(--font-body)" }}
                      placeholder="your@email.com"
                      autoComplete={isSignUp ? "off" : "email"}
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-[#515f74] uppercase tracking-wider mb-1.5" style={{ fontFamily: "var(--font-label)" }}>Password</label>
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength={6}
                      className="w-full px-4 py-3 border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20] placeholder:text-[#c4c5d5] focus:border-[#1a1a1a] transition-colors"
                      style={{ fontFamily: "var(--font-body)" }}
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
                    className="w-full bg-[#1a1a1a] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm disabled:opacity-30 transition-all duration-200 mt-2 hover:bg-[#333]"
                    style={{ fontFamily: "var(--font-label)" }}
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
                    className="text-[#1a1a1a] hover:text-[#374151] text-sm font-medium py-3 px-4 transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
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
