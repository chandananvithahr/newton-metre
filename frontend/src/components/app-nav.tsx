import Link from "next/link";
import Image from "next/image";

interface AppNavProps {
  children?: React.ReactNode;
}

export function AppNav({ children }: AppNavProps) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white border-b border-slate-200">
      <Link href="/" className="flex items-center gap-2.5">
        <Image src="/newton-metre-logo.png" alt="Newton-Metre" width={40} height={40} className="rounded-xl" />
        <span className="text-[22px] tracking-tight text-[#00288e] italic py-2" style={{ fontFamily: "var(--font-headline)" }}>
          Newton-Metre
        </span>
      </Link>
      {children}
    </nav>
  );
}
