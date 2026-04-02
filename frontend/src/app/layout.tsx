import type { Metadata } from "next";
import { Instrument_Serif, Source_Sans_3, DM_Mono, IBM_Plex_Mono, Inter, Geist } from "next/font/google";
import { Analytics } from "@vercel/analytics/react";
import { ToastProvider } from "@/components/Toast";
import "./globals.css";
import { cn } from "@/lib/utils";

const instrumentSerif = Instrument_Serif({
  subsets: ["latin"],
  weight: ["400"],
  style: ["normal", "italic"],
  variable: "--font-heading",
  display: "swap",
});

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

const dmMono = DM_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-inter",
  display: "swap",
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-code",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Newton-Metre — Should-Cost Intelligence",
  description: "Know what it costs. Before they quote. Newton-Metre reads your drawing, breaks down every cost line — material, machining, finishing, margin — like a senior cost analyst. Then searches your company's history for similar parts.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={cn(instrumentSerif.variable, dmMono.variable, ibmPlexMono.variable, inter.variable, "font-sans", geist.variable)}
    >
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className="min-h-screen antialiased">
        <ToastProvider>
          {children}
        </ToastProvider>
        <Analytics />
      </body>
    </html>
  );
}
