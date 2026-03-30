"use client";

// Click-to-copy on cost rows — dns.toys pattern:
// every technical value is clickable, fires a toast to confirm copy.

import { useToast } from "@/components/Toast";

const COST_LINES = [
  { label: "Raw material", detail: "EN8 Steel, 0.38 kg", value: "₹228" },
  { label: "CNC Turning", detail: "8.4 min @ ₹800/hr", value: "₹112" },
  { label: "Drilling", detail: "× 4 holes, 3.2 min", value: "₹32" },
  { label: "Threading", detail: "2.1 min", value: "₹21" },
  { label: "Setup", detail: "amortised over qty 100", value: "₹45" },
  { label: "Tooling", detail: "", value: "₹18" },
  { label: "Labour", detail: "", value: "₹38" },
  { label: "Power", detail: "", value: "₹9" },
  { label: "Overhead", detail: "15%", value: "₹76" },
  { label: "Profit margin", detail: "20%", value: "₹116" },
];

const TOTAL = "₹695";

function CopyCell({ value, onCopy }: { value: string; onCopy: (v: string) => void }) {
  return (
    <td
      onClick={() => onCopy(value)}
      title="Click to copy"
      className="text-right px-4 py-2.5 cursor-pointer select-none tabular-nums font-medium text-slate-700 hover:text-cyan-600 transition-colors"
      style={{ fontFamily: "var(--font-mono)" }}
    >
      {value}
    </td>
  );
}

export function CostBreakdownTable() {
  const toast = useToast();

  function handleCopy(value: string) {
    navigator.clipboard.writeText(value).then(() => {
      toast(`Copied ${value}`, { variant: "success" });
    });
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      {/* Card header */}
      <div className="bg-slate-50 px-4 py-3 border-b border-slate-200 flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold text-slate-800">EN8 Steel Shaft — Ø50×100mm</div>
          <div
            className="text-xs text-slate-400 mt-0.5"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            Qty 100 · CNC Turning + Drilling + Threading
          </div>
        </div>
        <span
          className="bg-emerald-50 text-emerald-700 text-xs font-semibold px-2 py-1 rounded-full border border-emerald-200"
          style={{ fontFamily: "var(--font-mono)" }}
        >
          HIGH
        </span>
      </div>

      {/* Table — semantic HTML, dns.toys pattern */}
      <table className="w-full text-sm">
        <thead className="sr-only">
          <tr>
            <th>Cost item</th>
            <th>Detail</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {COST_LINES.map((line) => (
            <tr key={line.label} className="hover:bg-slate-50 transition-colors">
              <td className="px-4 py-2.5 text-slate-500 w-[40%]">{line.label}</td>
              <td className="px-2 py-2.5 text-slate-400 text-xs" style={{ fontFamily: "var(--font-mono)" }}>
                {line.detail}
              </td>
              <CopyCell value={line.value} onCopy={handleCopy} />
            </tr>
          ))}
        </tbody>
      </table>

      {/* Total row */}
      <div
        onClick={() => handleCopy(TOTAL)}
        title="Click to copy total"
        className="px-4 py-3 flex items-center justify-between cursor-pointer bg-slate-900 text-white hover:bg-slate-700 transition-colors"
      >
        <span className="font-bold text-sm">Should cost / unit</span>
        <span className="text-xl font-bold" style={{ fontFamily: "var(--font-mono)" }}>
          {TOTAL}
        </span>
      </div>

      <p
        className="text-center text-xs text-slate-400 py-2"
        style={{ fontFamily: "var(--font-mono)" }}
      >
        Click any value to copy
      </p>
    </div>
  );
}
