"use client";

// Reusable click-to-copy — dns.toys pattern.
// Wraps any inline value. Fires a toast on copy.

import { useToast } from "@/components/Toast";

interface CopyValueProps {
  value: string;
  className?: string;
  as?: "span" | "td";
  children?: React.ReactNode;
}

export function CopyValue({ value, className = "", as: Tag = "span", children }: CopyValueProps) {
  const toast = useToast();

  function handleCopy() {
    navigator.clipboard.writeText(value).then(() => {
      toast(`Copied ${value}`, { variant: "success" });
    });
  }

  return (
    <Tag
      onClick={handleCopy}
      title="Click to copy"
      className={`cursor-pointer select-none ${className}`}
    >
      {children ?? value}
    </Tag>
  );
}
