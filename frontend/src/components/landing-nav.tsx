"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
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
    <nav className="fixed top-0 z-50 w-full bg-[#faf8ff]/90 backdrop-blur-md">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between px-8 py-4">
        <div className="flex items-center gap-12">
          <Link href="/" className="flex items-center gap-3">
            <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={40} height={40} className="rounded-xl" />
            <span className="text-[26px] italic text-[#00288e] font-semibold" style={{ fontFamily: "var(--font-headline)" }}>Newton-Metre</span>
          </Link>
          <div className="hidden md:flex gap-8">
            {[
              ["How it works", "#workflow"],
              ["Capabilities", "#capabilities"],
              ["Pricing", "#pricing"],
            ].map(([label, href]) => (
              <a
                key={label}
                href={href}
                className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                style={{ fontFamily: "var(--font-label)" }}
              >
                {label}
              </a>
            ))}
            {loggedIn ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                  style={{ fontFamily: "var(--font-label)" }}
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                  style={{ fontFamily: "var(--font-label)" }}
                >
                  Log out
                </button>
              </>
            ) : (
              <Link
                href="/login"
                className="text-[14px] font-medium text-[#515f74] hover:text-[#00288e] transition-colors"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Log in
              </Link>
            )}
          </div>
        </div>
        <Link
          href="/estimate/new"
          className="gradient-cta text-white px-6 py-2.5 rounded-lg text-xs font-bold tracking-widest uppercase transition-transform active:scale-95"
          style={{ fontFamily: "var(--font-label)" }}
        >
          New Estimate
        </Link>
      </div>
    </nav>
  );
}
