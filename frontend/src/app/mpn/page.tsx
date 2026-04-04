"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { track } from "@vercel/analytics";
import { lookupMPN } from "@/lib/api";
import { AppNav } from "@/components/app-nav";

interface SupplierOption {
  name: string;
  unit_price_inr: number | null;
  in_stock: boolean;
  source: "live" | "estimate";
}

interface MPNResult {
  mpn: string;
  quantity: number;
  description: string;
  category: string;
  key_specs: string[];
  unit_price_inr: number | null;
  unit_price_inr_low: number | null;
  unit_price_inr_high: number | null;
  order_cost_inr: number | null;
  negotiation_headroom_pct: number;
  lead_time_weeks: number | null;
  notes: string;
  supplier_options: SupplierOption[];
}

const CATEGORY_LABELS: Record<string, string> = {
  connector: "Connector",
  fastener: "Fastener",
  bearing: "Bearing",
  capacitor: "Capacitor",
  resistor: "Resistor",
  IC: "IC / Chip",
  sensor: "Sensor",
  relay: "Relay",
  switch: "Switch",
  cable: "Cable",
  motor: "Motor",
  pneumatic: "Pneumatic",
  hydraulic: "Hydraulic",
  other: "Component",
};

function fmt(n: number | null | undefined) {
  if (n == null) return "—";
  return `₹${n.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
}

export default function MPNSearchPage() {
  const router = useRouter();
  const [mpn, setMpn] = useState("");
  const [qty, setQty] = useState("1");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MPNResult | null>(null);
  const [error, setError] = useState("");

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!mpn.trim()) return;
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await lookupMPN(mpn.trim(), parseInt(qty) || 1);
      setResult(data);
      track("mpn_lookup", { mpn: mpn.trim().toUpperCase(), qty: parseInt(qty) || 1, category: data.category });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lookup failed");
    }
    setLoading(false);
  }

  const savings = result
    ? Math.round(
        ((result.unit_price_inr || 0) *
          (result.negotiation_headroom_pct / 100) *
          result.quantity) *
          100
      ) / 100
    : 0;

  return (
    <div className="min-h-screen warm-gradient-page">
      <AppNav active="/mpn" />
      <div className="max-w-3xl mx-auto px-4 sm:px-8 py-12">

        {/* Header */}
        <h1
          style={{ fontFamily: "var(--font-headline)" }}
          className="text-[32px] tracking-tight text-[var(--color-text-primary)] mb-2"
        >
          Part Number Search
        </h1>
        <p
          className="text-[var(--color-text-muted)] mb-8 text-[14px]"
          style={{ fontFamily: "var(--font-body)" }}
        >
          Look up any MPN — connectors, fasteners, bearings, ICs. Get market
          price, supplier options, and negotiation intelligence.
        </p>

        {/* Search form */}
        <form
          onSubmit={handleSearch}
          className="bg-white rounded-2xl border border-black/10 p-6 mb-6"
        >
          <div className="flex gap-3">
            <div className="flex-1">
              <label
                className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-1.5 block"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Part Number (MPN)
              </label>
              <input
                type="text"
                value={mpn}
                onChange={(e) => setMpn(e.target.value)}
                placeholder="e.g. GX16-4, 6204-2RS, MCP23017"
                className="w-full px-4 py-3 rounded-xl border border-black/10 text-[14px] text-[var(--color-text-primary)] placeholder-[var(--color-text-disabled)] focus:outline-none focus:ring-2 focus:ring-[var(--color-nm-primary)]/20 focus:border-[var(--color-nm-primary)]/30"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>
            <div className="w-28">
              <label
                className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-1.5 block"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Quantity
              </label>
              <input
                type="number"
                min="1"
                value={qty}
                onChange={(e) => setQty(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-black/10 text-[14px] text-[var(--color-text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-nm-primary)]/20 focus:border-[var(--color-nm-primary)]/30"
                style={{ fontFamily: "var(--font-mono)" }}
              />
            </div>
          </div>

          {error && (
            <div className="mt-3 bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-red-600 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !mpn.trim()}
            className="mt-4 w-full bg-[var(--color-brand-dark)] text-white py-3.5 rounded-full font-medium hover:bg-[var(--color-brand-dark-hover)] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 text-[14px]"
            style={{ fontFamily: "var(--font-body)" }}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Looking up {mpn.toUpperCase()}...
              </span>
            ) : (
              "Get Price Intelligence"
            )}
          </button>
        </form>

        {/* Results */}
        {result && (
          <div className="space-y-4">

            {/* Part summary card */}
            <div className="bg-white rounded-xl border border-black/10 p-6">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className="text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[var(--color-surface-container-low)] text-[var(--color-text-muted)]"
                      style={{ fontFamily: "var(--font-label)" }}
                    >
                      {CATEGORY_LABELS[result.category] ?? result.category}
                    </span>
                  </div>
                  <h2
                    className="text-[20px] font-bold text-[var(--color-text-primary)]"
                    style={{ fontFamily: "var(--font-headline)" }}
                  >
                    {result.mpn}
                  </h2>
                  <p
                    className="text-[14px] text-[var(--color-text-description)] mt-1"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {result.description}
                  </p>
                </div>

                {/* Price summary */}
                <div className="text-right shrink-0">
                  <p
                    className="text-[28px] font-bold text-[var(--color-text-primary)]"
                    style={{
                      fontFamily: "var(--font-headline)",
                      fontVariantNumeric: "tabular-nums",
                    }}
                  >
                    {fmt(result.unit_price_inr)}
                  </p>
                  <p
                    className="text-[11px] text-[var(--color-text-muted)]"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    per unit
                  </p>
                  {result.unit_price_inr_low != null &&
                    result.unit_price_inr_high != null && (
                      <p
                        className="text-[11px] text-[var(--color-text-muted)] mt-0.5"
                        style={{ fontFamily: "var(--font-mono)" }}
                      >
                        {fmt(result.unit_price_inr_low)} –{" "}
                        {fmt(result.unit_price_inr_high)}
                      </p>
                    )}
                </div>
              </div>

              {/* Key specs */}
              {result.key_specs.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {result.key_specs.map((spec) => (
                    <span
                      key={spec}
                      className="text-[12px] px-2.5 py-1 rounded-full bg-[var(--color-surface-container-low)] text-[var(--color-text-secondary)]"
                      style={{ fontFamily: "var(--font-mono)" }}
                    >
                      {spec}
                    </span>
                  ))}
                </div>
              )}

              {/* Stats row */}
              <div className="grid grid-cols-3 gap-4 pt-4 border-t border-black/5">
                <div>
                  <p
                    className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    Order Cost ({result.quantity} pcs)
                  </p>
                  <p
                    className="text-[15px] font-bold text-[var(--color-text-primary)]"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    {fmt(result.order_cost_inr)}
                  </p>
                </div>
                <div>
                  <p
                    className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    Negotiation room
                  </p>
                  <p
                    className="text-[15px] font-bold text-emerald-600"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    ~{result.negotiation_headroom_pct}%
                  </p>
                </div>
                <div>
                  <p
                    className="text-[11px] text-[var(--color-text-muted)] uppercase tracking-wider mb-1"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    Lead time
                  </p>
                  <p
                    className="text-[15px] font-bold text-[var(--color-text-primary)]"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    {result.lead_time_weeks != null
                      ? `${result.lead_time_weeks}w`
                      : "—"}
                  </p>
                </div>
              </div>
            </div>

            {/* Supplier options */}
            {result.supplier_options.length > 0 && (
              <div className="bg-white rounded-xl border border-black/10 overflow-hidden">
                <div className="px-6 py-4 border-b border-black/5">
                  <h3
                    className="text-[13px] font-bold text-[var(--color-text-primary)] uppercase tracking-wider"
                    style={{ fontFamily: "var(--font-label)" }}
                  >
                    Supplier Options
                  </h3>
                </div>
                <table className="w-full">
                  <thead>
                    <tr className="bg-[var(--color-surface-container-low)]">
                      <th
                        className="text-left px-6 py-3 text-[11px] font-bold text-[var(--color-text-muted)] uppercase tracking-wider"
                        style={{ fontFamily: "var(--font-label)" }}
                      >
                        Supplier
                      </th>
                      <th
                        className="text-right px-6 py-3 text-[11px] font-bold text-[var(--color-text-muted)] uppercase tracking-wider"
                        style={{ fontFamily: "var(--font-label)" }}
                      >
                        Unit Price
                      </th>
                      <th
                        className="text-right px-6 py-3 text-[11px] font-bold text-[var(--color-text-muted)] uppercase tracking-wider"
                        style={{ fontFamily: "var(--font-label)" }}
                      >
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-black/5">
                    {result.supplier_options.map((s, i) => (
                      <tr
                        key={i}
                        className="hover:bg-[var(--color-surface-hover)] transition-colors"
                      >
                        <td className="px-6 py-3.5">
                          <div className="flex items-center gap-2">
                            <span
                              className="text-[14px] font-medium text-[var(--color-text-primary)]"
                              style={{ fontFamily: "var(--font-body)" }}
                            >
                              {s.name}
                            </span>
                            {s.source === "live" && (
                              <span
                                className="text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-700"
                                style={{ fontFamily: "var(--font-label)" }}
                              >
                                Live
                              </span>
                            )}
                          </div>
                        </td>
                        <td
                          className="px-6 py-3.5 text-right text-[14px] font-semibold text-[var(--color-text-primary)]"
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontVariantNumeric: "tabular-nums",
                          }}
                        >
                          {s.unit_price_inr != null
                            ? fmt(s.unit_price_inr)
                            : "Request quote"}
                        </td>
                        <td className="px-6 py-3.5 text-right">
                          <span
                            className={`text-[12px] font-medium ${s.in_stock ? "text-emerald-600" : "text-amber-600"}`}
                            style={{ fontFamily: "var(--font-body)" }}
                          >
                            {s.in_stock ? "In stock" : "Lead time"}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Potential savings banner */}
            {savings > 0 && (
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p
                      className="text-[13px] font-bold text-emerald-800 mb-0.5"
                      style={{ fontFamily: "var(--font-body)" }}
                    >
                      Potential savings on this order
                    </p>
                    <p
                      className="text-[12px] text-emerald-700"
                      style={{ fontFamily: "var(--font-body)" }}
                    >
                      ~{result.negotiation_headroom_pct}% negotiation headroom
                      based on market data
                    </p>
                  </div>
                  <p
                    className="text-[24px] font-bold text-emerald-700 shrink-0"
                    style={{
                      fontFamily: "var(--font-headline)",
                      fontVariantNumeric: "tabular-nums",
                    }}
                  >
                    {fmt(savings)}
                  </p>
                </div>
              </div>
            )}

            {/* Notes */}
            {result.notes && (
              <p
                className="text-[12px] text-[var(--color-text-muted)] px-1"
                style={{ fontFamily: "var(--font-body)" }}
              >
                {result.notes}
              </p>
            )}

            {/* CTA */}
            <div className="bg-white ghost-border rounded-xl p-5">
              <h2
                className="text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] mb-3"
                style={{ fontFamily: "var(--font-label)" }}
              >
                Next steps
              </h2>
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={() =>
                    router.push(
                      `/workflows/new?type=negotiate&mpn=${encodeURIComponent(result.mpn)}`
                    )
                  }
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full text-white text-[13px] font-medium transition-colors"
                  style={{
                    fontFamily: "var(--font-body)",
                    background: "var(--color-brand-dark)",
                  }}
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
                    />
                  </svg>
                  Negotiate with AI
                </button>
                <button
                  onClick={() =>
                    router.push(
                      `/workflows/new?type=rfq&mpn=${encodeURIComponent(result.mpn)}`
                    )
                  }
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
                    />
                  </svg>
                  Send RFQ
                </button>
                <button
                  onClick={() => {
                    setResult(null);
                    setMpn("");
                  }}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full border border-black/10 text-[13px] font-medium text-[var(--color-text-secondary)] hover:border-[var(--color-brand-dark)] hover:text-[var(--color-brand-dark)] transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  Search another part
                </button>
              </div>
            </div>

          </div>
        )}

        {/* Empty state — no search yet */}
        {!result && !loading && (
          <div className="text-center py-6">
            <p
              className="text-[12px] text-[var(--color-text-muted)]"
              style={{ fontFamily: "var(--font-body)" }}
            >
              Try: <button onClick={() => setMpn("GX16-4")} className="underline hover:text-[var(--color-text-secondary)]">GX16-4</button>
              {" · "}
              <button onClick={() => setMpn("6204-2RS")} className="underline hover:text-[var(--color-text-secondary)]">6204-2RS</button>
              {" · "}
              <button onClick={() => setMpn("MCP23017")} className="underline hover:text-[var(--color-text-secondary)]">MCP23017</button>
              {" · "}
              <button onClick={() => setMpn("M8x25-ISO4762")} className="underline hover:text-[var(--color-text-secondary)]">M8x25-ISO4762</button>
            </p>
          </div>
        )}

      </div>
    </div>
  );
}
