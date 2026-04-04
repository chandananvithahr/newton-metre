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
    ["Capabilities", "#capabilities"],
    ["Pricing", "#pricing"],
  ] as const;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-4 sm:px-8 pt-3">
      <div className="max-w-[1200px] mx-auto">
        <div className="bg-white/90 backdrop-blur-md border border-black/8 rounded-full px-5 py-2.5 flex items-center justify-between shadow-sm">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative w-9 h-9 flex items-center justify-center">
              <div className="absolute inset-0 bg-[var(--color-brand-dark)] rounded-xl shadow-sm" />
              <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
            </div>
            <span className="hidden sm:inline text-[var(--color-brand-dark)] text-xl font-bold tracking-tight">Newton-Metre</span>
          </Link>

          {/* Desktop nav links */}
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map(([label, href]) => (
              <a
                key={label}
                href={href}
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium"

              >
                {label}
              </a>
            ))}
            {loggedIn ? (
              <button
                onClick={handleLogout}
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium"

              >
                Log out
              </button>
            ) : (
              <Link
                href="/login"
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium"

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
              <span className={`block w-5 h-0.5 bg-[var(--color-brand-dark)] transition-transform ${menuOpen ? "rotate-45 translate-y-1" : ""}`} />
              <span className={`block w-5 h-0.5 bg-[var(--color-brand-dark)] transition-opacity ${menuOpen ? "opacity-0" : ""}`} />
              <span className={`block w-5 h-0.5 bg-[var(--color-brand-dark)] transition-transform ${menuOpen ? "-rotate-45 -translate-y-1" : ""}`} />
            </button>

            {/* CTA — bolder green */}
            <Link
              href="/estimate/new"
              className="dark-pill px-5 py-2 text-xs font-bold uppercase tracking-widest"
            >
              Upload a Drawing
            </Link>
          </div>
        </div>

        {/* Mobile dropdown */}
        {menuOpen && (
          <div className="md:hidden mt-2 bg-white/95 backdrop-blur-md rounded-2xl border border-black/8 shadow-lg px-5 py-4 flex flex-col gap-3">
            {navLinks.map(([label, href]) => (
              <a
                key={label}
                href={href}
                onClick={() => setMenuOpen(false)}
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium py-1"

              >
                {label}
              </a>
            ))}
            {loggedIn ? (
              <button
                onClick={() => { handleLogout(); setMenuOpen(false); }}
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium py-1 text-left"

              >
                Log out
              </button>
            ) : (
              <Link
                href="/login"
                onClick={() => setMenuOpen(false)}
                className="text-sm text-[var(--color-neutral-gray)] hover:text-[var(--color-brand-dark)] transition-colors font-medium py-1"

              >
                Log in
              </Link>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
