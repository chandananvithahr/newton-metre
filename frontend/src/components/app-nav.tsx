import Link from "next/link";

const NAV_LINKS = [
  { href: "/estimate/new", label: "Should-Cost" },
  { href: "/similar", label: "Similarity" },
  { href: "/mpn", label: "Part Search" },
  { href: "/workflows", label: "Workflows" },
  { href: "/chat", label: "Chat" },
];

interface AppNavProps {
  children?: React.ReactNode;
  active?: string;
}

export function AppNav({ children, active }: AppNavProps) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white border-b border-black/5">
      <div className="flex items-center gap-8">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative w-9 h-9 flex items-center justify-center">
            <div className="absolute inset-0 bg-[var(--color-brand-dark)] rounded-xl" />
            <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
          </div>
          <span className="text-[var(--color-brand-dark)] text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-body)" }}>
            Newton-Metre
          </span>
        </Link>
        <div className="hidden sm:flex items-center gap-1">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`px-3 py-1.5 rounded-lg text-[13px] transition-colors ${
                active === link.href
                  ? "text-[var(--color-brand-dark)] font-semibold bg-[var(--color-surface-hover)]"
                  : "text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-hover)]"
              }`}
              style={{ fontFamily: "var(--font-body)" }}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
      {children}
    </nav>
  );
}
