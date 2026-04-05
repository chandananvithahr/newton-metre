"use client";

import { usePathname } from "next/navigation";
import { ChatPanel } from "@/components/chat-widget";

const FULL_WIDTH_PATHS = ["/", "/login", "/chat"];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const showChat = !FULL_WIDTH_PATHS.includes(pathname);

  // Extract estimate ID from /estimate/[id] routes so chat has context
  const estimateMatch = pathname.match(/^\/estimate\/([^/]+)$/);
  const estimateId = estimateMatch ? estimateMatch[1] : null;

  if (!showChat) {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <main className="flex-1 min-w-0 overflow-y-auto">
        {children}
      </main>
      <ChatPanel estimateId={estimateId} />
    </div>
  );
}
