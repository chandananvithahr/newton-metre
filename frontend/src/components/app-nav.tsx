import Link from "next/link";

interface AppNavProps {
  children?: React.ReactNode;
}

export function AppNav({ children }: AppNavProps) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-[#161B27] border-b border-[#2A3140]">
      <Link href="/dashboard" className="text-xl tracking-tight text-[#22D3EE] py-2" style={{ fontFamily: "var(--font-heading)" }}>
        Costrich
      </Link>
      {children}
    </nav>
  );
}
