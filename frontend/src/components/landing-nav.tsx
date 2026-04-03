"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase";

export function LandingNav() {
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

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

  const navLinks = [
    ["How it works", "#how-it-works"],
    ["Capabilities", "#capabilities"],
    ["Pricing", "#pricing"],
  ] as const;

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

        {/* Desktop nav links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map(([label, href]) => (
            <a
              key={label}
              href={href}
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              {label}
            </a>
          ))}
          {loggedIn ? (
            <button
              onClick={handleLogout}
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              Log out
            </button>
          ) : (
            <Link
              href="/login"
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium"
            >
              Log in
            </Link>
          )}
        </div>

        <div className="flex items-center gap-3">
          {/* Hamburger (mobile only) */}
          <button
            onClick={() => setMenuOpen((v) => !v)}
            className="md:hidden flex flex-col justify-center items-center w-10 h-10 gap-1.5"
            aria-label="Toggle menu"
          >
            <span className={`block w-5 h-0.5 bg-[#1a1a1a] transition-transform ${menuOpen ? "rotate-45 translate-y-1" : ""}`} />
            <span className={`block w-5 h-0.5 bg-[#1a1a1a] transition-opacity ${menuOpen ? "opacity-0" : ""}`} />
            <span className={`block w-5 h-0.5 bg-[#1a1a1a] transition-transform ${menuOpen ? "-rotate-45 -translate-y-1" : ""}`} />
          </button>

          {/* CTA */}
          <Link
            href="/estimate/new"
            className="dark-pill px-5 py-2.5 text-xs font-bold uppercase tracking-widest"
          >
            New Estimate
          </Link>
        </div>
      </div>

      {/* Mobile dropdown */}
      {menuOpen && (
        <div className="md:hidden mt-3 pb-3 border-t border-black/5 pt-3 flex flex-col gap-3">
          {navLinks.map(([label, href]) => (
            <a
              key={label}
              href={href}
              onClick={() => setMenuOpen(false)}
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium px-2"
            >
              {label}
            </a>
          ))}
          {loggedIn ? (
            <button
              onClick={() => { handleLogout(); setMenuOpen(false); }}
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium px-2 text-left"
            >
              Log out
            </button>
          ) : (
            <Link
              href="/login"
              onClick={() => setMenuOpen(false)}
              className="text-base text-[#374151] hover:text-[#1a1a1a] transition-colors font-medium px-2"
            >
              Log in
            </Link>
          )}
        </div>
      )}
    </nav>
  );
}
