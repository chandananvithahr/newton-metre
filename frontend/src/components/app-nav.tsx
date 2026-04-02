import Link from "next/link";

interface AppNavProps {
  children?: React.ReactNode;
}

export function AppNav({ children }: AppNavProps) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white border-b border-black/5">
      <Link href="/" className="flex items-center gap-3 group">
        <div className="relative w-9 h-9 flex items-center justify-center">
          <div className="absolute inset-0 bg-[#1a1a1a] rounded-xl" />
          <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
        </div>
        <span className="text-[#1a1a1a] text-xl font-semibold tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>
          Newton-Metre
        </span>
      </Link>
      {children}
    </nav>
  );
}
