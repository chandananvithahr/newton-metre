import Link from "next/link";

interface AppNavProps {
  children?: React.ReactNode;
}

export function AppNav({ children }: AppNavProps) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white border-b border-gray-100 shadow-sm">
      <Link href="/dashboard" className="text-xl font-bold tracking-tight text-primary-700 py-2">
        Costrich
      </Link>
      {children}
    </nav>
  );
}
