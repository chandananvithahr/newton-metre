"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase";

export function LandingNav() {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const supabase = createClient();
    supabase.auth.getUser().then(({ data }) => {
      setLoggedIn(!!data.user);
    });
  }, []);

  async function handleLogout() {
    const supabase = createClient();
    await supabase.auth.signOut();
    setLoggedIn(false);
    router.refresh();
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-black/5 px-4 sm:px-8 py-4">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative w-11 h-11 flex items-center justify-center">
            <div className="absolute inset-0 bg-[#1a1a1a] rounded-xl rotate-3 opacity-10 group-hover:rotate-6 transition-transform" />
            <div className="absolute inset-0 bg-[#1a1a1a] rounded-xl" />
            <span className="relative text-white font-mono font-bold text-base tracking-tighter">N·m</span>
          </div>
          <span className="text-[#1a1a1a] text-2xl font-bold tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>Newton-Metre</span>
        </Link>

        {/* Nav links */}
        <div className="hidden md:flex items-center gap-8">
          {[
            ["How it works", "#how-it-works"],
            ["Capabilities", "#capabilities"],
            ["Pricing", "#pricing"],
          ].map(([label, href]) => (
            <a
              key={label}
              href={href}
              className="text-sm text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              {label}
            </a>
          ))}
          {loggedIn ? (
            <button
              onClick={handleLogout}
              className="text-sm text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              Log out
            </button>
          ) : (
            <Link
              href="/login"
              className="text-sm text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              Log in
            </Link>
          )}
        </div>

        {/* CTA */}
        <Link
          href="/estimate/new"
          className="dark-pill px-5 py-2.5 text-xs font-bold uppercase tracking-widest"
        >
          New Estimate
        </Link>
      </div>
    </nav>
  );
}
