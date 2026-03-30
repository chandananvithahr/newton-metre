# UI/UX Skills — Kailash Nadh / Zerodha Tech Patterns

Extracted from **9 open-source repos** by Kailash Nadh (CTO, Zerodha). All zips in project root.

| Repo | What to study |
|---|---|
| `dns.toys` | Table-first layout, click-to-copy, minimal nav |
| `listmonk` | Public form CSS, button states, subtle shadows |
| `oat` | **Complete design system** — CSS variables, spacing scale, component patterns |
| `dont.build` | Feature decision tool, range inputs, weighted scoring UX |
| `tinytabs` | Zero-dep tabs with anchor routing, ARIA roles |
| `tinyprogressbar` | Minimal progress bar (no deps) |
| `tinytooltip` | Tooltip via data attributes, no JS framework |
| `dragmove.js` | Drag interaction, pointer events |
| `floatype.js` | Floating label pattern |

Use this as a checklist before shipping any new page, component, or UI section.

---

## 1. Tables beat card grids for tabular data

**Pattern:** Use `<table>` with `<thead>` / `<tbody>` / `<tr>` for anything that has rows of structured information. Cards are for isolated items that don't relate to each other.

**dns.toys does this:** Every service is a table row (`Service | Usage`). Not 24 separate cards.

**When to use:**
- Feature lists with name + description → table
- Before/After comparisons → comparison table (2 columns)
- Step-by-step flows → numbered table (`# | Action | What happens`)
- Pricing feature lists → simple single-column table rows

**When to use cards:** Pricing tiers, testimonials, team members — things that stand alone.

```tsx
// ✓ Kailash pattern — feature table
<table className="w-full text-sm border border-[#2A3140] rounded-xl overflow-hidden">
  <thead>
    <tr className="bg-[#1C2235] border-b border-[#2A3140]">
      <th className="text-left px-5 py-3 text-[#94A3B8] font-medium w-64">Feature</th>
      <th className="text-left px-5 py-3 text-[#94A3B8] font-medium">What it means</th>
    </tr>
  </thead>
  <tbody className="divide-y divide-[#2A3140]">
    {FEATURES.map((f) => (
      <tr key={f.name} className="hover:bg-[#1C2235] transition-colors">
        <td className="px-5 py-4 font-semibold text-[#E2E8F0] align-top">{f.name}</td>
        <td className="px-5 py-4 text-[#64748B] leading-relaxed">{f.desc}</td>
      </tr>
    ))}
  </tbody>
</table>
```

---

## 2. Click-to-copy for all technical values

**Pattern:** Any `<code>`, price, number, or technical value that a user might want to paste elsewhere should be clickable. Flash yellow/amber on click to confirm copy.

**dns.toys does this:** Every `dig` command is a `<code>` that copies on click, flashes `#ffbe2e`.

**Implementation (React `'use client'` component):**

```tsx
"use client";
function CopyCell({ value }: { value: string }) {
  const [flash, setFlash] = useState(false);
  function handleCopy() {
    navigator.clipboard.writeText(value).then(() => {
      setFlash(true);
      setTimeout(() => setFlash(false), 500);
    });
  }
  return (
    <td
      onClick={handleCopy}
      title="Click to copy"
      className="cursor-pointer tabular-nums font-medium transition-colors"
      style={{ backgroundColor: flash ? "#ca8a04" : undefined, color: flash ? "#0F1117" : undefined }}
    >
      {value}
    </td>
  );
}
```

**Apply to:** cost breakdowns, API keys, part numbers, machine rates, CLI commands, total prices.

**Never make non-technical prose clickable.** Only values someone would paste.

---

## 3. Typography rhythm

**Pattern:** Let typography do the design work. Don't rely on gradients or decorations.

| Property | dns.toys | listmonk | Costrich |
|---|---|---|---|
| Base font | Inter | Inter | Source Sans 3 |
| Base size | 17px | 16px | 16px |
| Line height | 26px (1.53×) | 26px | Use `leading-relaxed` (1.625) |
| Heading weight | normal (400) | 400 | 400 (Instrument Serif) |
| Mono | system monospace | system | DM Mono |

**Rules:**
- `font-weight: 400` for headings — bold headings feel heavy, not sharp
- 1.5–1.625× line-height for body text — never 1.25× for paragraph content
- Monospace for: numbers, prices, codes, IDs, timestamps, CLI commands, percentages

---

## 4. Single accent colour, used sparingly

**Pattern:** One action colour. Used only for: links, primary CTA buttons, and the most important data value on the page. Everything else is grey.

| Repo | Accent |
|---|---|
| dns.toys | `#166ab9` (blue) |
| listmonk | `#0055d4` (blue) |
| Costrich | `#22D3EE` (cyan) |

**Rules:**
- Don't use accent for decorative purposes (backgrounds, gradients, borders on cards)
- Do use accent for: CTA buttons, active nav links, key numeric values, focus rings
- Use `text-[#64748B]` for secondary text, `text-[#475569]` for tertiary, `text-[#94A3B8]` for medium

---

## 5. Subtle shadows, minimal decoration

**Pattern:** `box-shadow: 2px 2px 0 #f3f3f3` (listmonk) or `2px 2px 2px #eee` (dns.toys).
Two pixels, one shade lighter than background. Not `0 20px 60px rgba(0,0,0,0.5)`.

**For dark theme (Costrich):**
- Borders: `1px solid #2A3140` — not thick, not coloured
- Cards: `bg-[#161B27]` + `border border-[#2A3140]` — no glow, no shadow
- Hover state: `hover:bg-[#1C2235]` — subtle, not dramatic

**Never:**
- `bg-gradient-to-br` as decorative layering inside sections
- Coloured shadows (`shadow-cyan-500/20`)
- Multiple layered box-shadows
- Glassmorphism (`backdrop-blur` on cards)

---

## 6. Zero animation for content sections

**Pattern:** Neither dns.toys nor listmonk use CSS animations on page load. No `fade-in-up`, no staggered delays.

**Why:** Animations delay the user from reading the content. They signal "look how polished I am" at the cost of utility. Technical users find them annoying.

**Exception:** Micro-interactions only:
- Click feedback (flash on copy)
- Hover state (`transition-colors`)
- Button press (`scale(0.98)` on `:active`)
- Form focus rings

**Remove:** `animate-fade-in-up`, `animate-fade-in-up-delay-1/2/3` from hero and hero CTA. These were removed in the Costrich landing page update.

---

## 7. Comparison tables beat two-card layouts

**Pattern:** Before/After is always better as one table than two side-by-side cards.

```
| Metric          | Without       | With Costrich         |
|-----------------|---------------|-----------------------|
| Time            | 2–3 days      | Under 60 seconds      |
| Accuracy        | Unknown       | ±5–10% physics-based  |
```

**Why:** One table:
- Easier to scan horizontally (same topic, different values)
- No visual imbalance if one column has more text
- Naturally handles mobile (one column stack)
- More honest — puts both sides on equal footing

---

## 8. Function-first copy

**Pattern:** Kailash's copy is blunt and direct. No "Transform your workflow" or "Supercharge your productivity."

**dns.toys headline:** `"Useful utilities and services over DNS"` — literally what it is.
**listmonk tagline:** `"High performance, self-hosted newsletter and mailing list manager."` — exactly what it does.

**Rules for Costrich:**
- Lead with what the user gets, not what the product is
- Use second person ("you", "your") not product-centric ("Costrich gives you")
- Specific > vague: "₹800/hr CNC turning rate" not "competitive rates"
- Numbers when you have them: "±5–10%" not "accurate"

---

## 9. Semantic HTML first

**Pattern:** Use the right element. `<table>` for tabular data. `<nav>` for navigation. `<code>` for code/commands. `<section>` with `id` for anchor links.

**dns.toys** uses raw HTML5 with zero JS framework and it's perfect.

**For React/Next.js:**
- `<table>` for comparisons, feature lists, breakdowns — not `<div className="divide-y">`
- `<code>` for CLI commands, part numbers, machine parameters
- `<section id="how-it-works">` for anchor nav links
- `aria-label` on icon-only buttons
- `title="Click to copy"` on copyable elements

---

## 10. Information density over visual whitespace inflation

**Pattern:** Kailash packs in information efficiently. dns.toys has 25 services on one page and it's not overwhelming. Each row is 2 lines: name + description.

**Anti-pattern to avoid:** Big hero section → 3-item "how it works" with large icons → 4 feature cards that each say one sentence → pricing. That's 12 visual elements communicating 8 actual facts.

**Costrich pattern:**
- Stats bar: 4 numbers, one line each
- How it works: table with 3 rows, each row has full detail
- Features: table, scannable in 20 seconds
- Comparison: table, no duplicate layout code

---

## 11. Form design (listmonk patterns)

For any form in the app (login, signup, settings):

```css
/* listmonk form input pattern */
input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 3px;
  box-shadow: 2px 2px 0 #f3f3f3;  /* subtle, not heavy */
  font-size: 1em;
}
input:focus {
  border-color: accent;
  /* no glow, just border change */
}
```

```css
/* Costrich equivalent */
input:focus {
  border-color: #22D3EE;
  box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.15);
}
```

- Labels: always visible, not placeholder-as-label
- Buttons: one primary (filled), one secondary (outline) — never three CTAs on one form
- Error state: red text below the input, not a toast

---

---

## 12. `aria-busy="true"` for loading states (from oat)

**Pattern:** Don't build custom spinner divs. Set `aria-busy="true"` on the container — oat injects the spinner via CSS `::before`. Semantic AND visual.

```tsx
// ✗ Current Costrich pattern — custom div
<div className="w-8 h-8 border-2 border-t-[#22D3EE] rounded-full animate-spin" />

// ✓ oat pattern — HTML attribute drives spinner
<div aria-busy="true" data-spinner="large">
  Loading...
</div>
```

**In Tailwind (Costrich adaptation):**
```tsx
// Container shows spinner automatically when loading
<div
  aria-busy={loading}
  className={loading ? "relative pointer-events-none" : ""}
>
  {/* content */}
</div>
```

The key insight: **loading state is a semantic state, not a visual component**. Use the attribute, not the div.

---

## 13. `data-variant` for component variants (from oat)

**Pattern:** Instead of a `confidenceColor()` function returning different className strings, use a `data-variant` attribute. CSS handles the styling. Logic stays out of components.

**oat badge:**
```html
<span class="badge success">HIGH</span>
<span class="badge warning">MEDIUM</span>
<span class="badge danger">LOW</span>
```

**Costrich currently:**
```tsx
// ✗ Function returning hardcoded className strings
const confidenceColor = (tier) => {
  if (tier === "high") return "bg-emerald-950/60 text-emerald-400 border-emerald-800";
  ...
}
```

**Better pattern (map → class suffix):**
```tsx
const TIER_CLASS: Record<string, string> = {
  high:   "badge-high",
  medium: "badge-medium",
  low:    "badge-low",
};
// In globals.css: .badge-high { @apply bg-emerald-950/60 text-emerald-400 border-emerald-800 ... }
```

---

## 14. `[role="alert"]` for error/success messages (from oat)

**Pattern:** Use `role="alert"` on status messages so screen readers announce them automatically. No extra ARIA needed.

```tsx
// ✗ Current Costrich pattern
<div className="bg-red-950/50 border border-red-900/50 rounded-lg px-4 py-3 text-red-400 text-sm">
  {error}
</div>

// ✓ oat pattern — semantic + auto-announced
<div role="alert" data-variant="error" className="...">
  {error}
</div>
```

Always include `role="alert"` on inline error messages. It costs nothing and makes the app accessible.

---

## 15. Button press = `translate(1px, 1px)` not `scale(0.98)` (from oat)

**Pattern:** oat uses `transform: translate(1px, 1px)` on `:active` instead of `scale(0.98)`. This simulates a real physical press (the button "sinks" diagonally into its shadow).

```css
/* oat */
button:active:not(:disabled) {
  transform: translate(1px, 1px);
}

/* Combined with oat's asymmetric border shadow: */
border-width: 1px 3px 3px 1px;  /* dont.build pattern */
box-shadow: 3px 3px 0px var(--secondary);
```

The diagonal movement only makes sense when paired with an offset shadow. For Costrich's flat buttons (no shadow), `scale(0.98)` is fine. **Use `translate(1px, 1px)` only when there's a visible offset shadow to "sink into".**

---

## 16. CSS spacing scale (from oat)

**Pattern:** oat defines `--space-1` through `--space-18` (0.25rem increments). Every padding, margin, gap uses this scale. Never raw pixel values.

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
```

**Tailwind equivalent already in Costrich** — use Tailwind's spacing scale (`p-4`, `gap-6`, `py-8`) consistently instead of arbitrary values (`py-2.5`, `px-5`, `gap-3.5`). The existing code already does this well.

---

## 17. `color-mix()` for hover/variant states (from oat)

**Pattern:** oat computes hover colors with CSS `color-mix()` — no hardcoded hex variants.

```css
/* oat button hover */
--_hov: color-mix(in srgb, var(--primary), white 25%);

/* oat alert backgrounds */
background-color: color-mix(in srgb, var(--danger) 8%, transparent);
```

**Applied to Costrich:** Instead of hardcoding `#06B6D4` as the hover state of `#22D3EE`, use:
```css
--accent-hover: color-mix(in srgb, #22D3EE, black 15%);
```

This is future-proof — if the accent color changes, hover adjusts automatically.

---

## 18. Weighted feature scoring (from dont.build)

**Pattern:** dont.build is a feature prioritisation tool built in 80 lines of JS. The scoring model:

```js
const params = [
  { weight: 0.10, negative: false, name: 'p-users' },          // % users affected
  { weight: 0.20, negative: false, name: 'p-user-value' },     // importance to those users
  { weight: 0.20, negative: false, name: 'p-feature-value' },  // true user value
  { weight: 0.15, negative: true,  name: 'p-effort' },         // build effort (negative)
  { weight: 0.20, negative: true,  name: 'p-negative-impact'}, // technical risk (negative)
  { weight: 0.15, negative: true,  name: 'p-operational-complexity' }, // ops complexity (negative)
]
```

**For Costrich product decisions:** Run any proposed feature through this model before building. The weights reflect Zerodha's priorities: user value (40% combined) > risk avoidance (35%) > reach (10%).

**Also applies to the confidence tier display:** Costrich's 4 confidence tiers (HIGH/MEDIUM/LOW/INSUFFICIENT) follow the same idea — weighted signals produce a single score, score maps to a tier, tier drives UI (badge color, CTA shown).

---

## 19. Zero-dep tab pattern (from tinytabs)

**Pattern:** tinytabs builds accessible tabs in ~100 lines with no framework. Key patterns:
- `role="tablist"` on the nav container
- `role="tab"` on each tab link
- Anchor-based routing (`#tab-id`) so tabs are deep-linkable
- `data-default` attribute to set the default tab
- `data-name` attribute on section for the tab label

**Applied to Costrich:** If adding tabs to the estimate page (e.g. Mechanical / Sheet Metal / PCB), use this pattern:
```tsx
// Section with id = tab ID, data-name = tab label
<div className="tab-section" id="mechanical" data-name="Mechanical" data-default>
  ...
</div>
<div className="tab-section" id="sheet-metal" data-name="Sheet Metal">
  ...
</div>
```

**Rule:** Tabs should update the URL hash. Procurement teams share links — if someone selects the Sheet Metal tab, the URL should reflect that.

---

## Sources

| Repo | Key file(s) | Primary pattern |
|---|---|---|
| `dns.toys` | `docs/index.html`, `docs/static/style.css` | Table layout, click-to-copy |
| `listmonk` | `static/public/static/style.css` | Form patterns, subtle shadows |
| `oat` | `src/css/00-base.css`, `01-theme.css`, `button.css`, `table.css`, `form.css` | Full design system |
| `dont.build` | `index.html`, `style.css` | Weighted scoring, offset shadows |
| `tinytabs` | `tinytabs.js` | Accessible tab pattern |
| `tinyprogressbar` | source | Minimal progress |
| `tinytooltip` | source | Data-attribute tooltips |
| `dragmove.js` | source | Pointer event drag |
| `floatype.js` | source | Floating label |

---

*Compiled March 2026 from 9 repos by Kailash Nadh (github.com/knadh). All available in `knadh-repos/` in the project root.*
