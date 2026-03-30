"use client";

/**
 * Toast — oat toast pattern ported to React.
 *
 * oat uses a popover + data-variant + data-placement.
 * We replicate the same API surface with a React context.
 *
 * Usage:
 *   import { useToast } from "@/components/Toast";
 *   const toast = useToast();
 *   toast("Copied ₹695", { variant: "success" });
 *   toast("Failed to save", { variant: "danger" });
 */

import { createContext, useCallback, useContext, useRef, useState } from "react";

type Variant = "info" | "success" | "danger" | "warning";

interface ToastItem {
  id: number;
  message: string;
  variant: Variant;
}

interface ToastContextValue {
  toast: (message: string, opts?: { variant?: Variant; duration?: number }) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);
let _nextId = 0;

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const timers = useRef<Map<number, ReturnType<typeof setTimeout>>>(new Map());

  const toast = useCallback(
    (message: string, { variant = "info", duration = 3000 }: { variant?: Variant; duration?: number } = {}) => {
      const id = _nextId++;
      setItems((prev) => [...prev, { id, message, variant }]);

      timers.current.set(
        id,
        setTimeout(() => {
          setItems((prev) => prev.filter((t) => t.id !== id));
          timers.current.delete(id);
        }, duration),
      );
    },
    [],
  );

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      {/* oat: data-placement="top-right" container */}
      <div className="toast-container" data-placement="top-right" aria-live="polite" aria-atomic="false">
        {items.map((item) => (
          <div
            key={item.id}
            className="toast"
            data-variant={item.variant}
            role="status"
            onMouseEnter={() => {
              const t = timers.current.get(item.id);
              if (t) clearTimeout(t);
            }}
            onMouseLeave={() => {
              const t = setTimeout(() => {
                setItems((prev) => prev.filter((i) => i.id !== item.id));
                timers.current.delete(item.id);
              }, 1500);
              timers.current.set(item.id, t);
            }}
          >
            {item.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): (message: string, opts?: { variant?: Variant; duration?: number }) => void {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx.toast;
}
