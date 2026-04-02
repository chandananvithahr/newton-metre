# Newton-Metre Design System — "Warm Editorial"

> **For Claude Code:** This file is the ground truth for ALL UI implementation.
> When converting Stitch screens to React/Next.js, treat every value here as a CONSTRAINT, not a suggestion.
> DO NOT rewrite layout logic. DO NOT substitute spacing. DO NOT change colors.
> Match the Stitch screenshot exactly — use it as visual ground truth.

---

## Brand

- **Name:** Newton-Metre
- **Logo:** Dark rounded-xl badge with "N·m" in white mono + italic Newsreader "Newton-Metre"
- **Tagline:** "Know what it should cost. Find where it already exists."
- Manufacturing cost intelligence platform for defense, aerospace, and automobile companies
- Bold editorial aesthetic — warm gradients, big serif headlines, dark pill CTAs

---

## Typography

| Token | Font | Usage |
|-------|------|-------|
| `--font-headline` | Newsreader (serif) | Page titles, hero text, brand name (always italic) |
| `--font-body` | Space Grotesk (sans) | Body text, descriptions, form inputs |
| `--font-label` | Space Grotesk (sans) | Buttons, nav links, section labels (uppercase tracking-widest) |
| `--font-mono` | DM Mono | Costs, part numbers, tolerances, timestamps, tabular data |

**Font Sizes:**
- Hero title: `text-4xl sm:text-5xl lg:text-[64px]`
- Section headings: `text-4xl sm:text-5xl`
- Body: `text-base` (16px) or `text-sm` (14px)
- Labels/caps: `text-[11px]` uppercase tracking-wider font-bold
- Micro: `text-[10px]` for timestamps, metadata, counters

**Rules:**
- Use monospace (`font-mono`) for ALL cost values, part numbers, tolerances, measurements
- Headlines use Newsreader italic
- Numbers and data are prominent — give them space
- Professional tone — no playful copy

---

## Color Palette

### Warm Gradient Backgrounds (Base44-inspired)

| Class | Gradient | Usage |
|-------|----------|-------|
| `warm-gradient-hero` | `linear-gradient(135deg, #B2EBF2 0%, #FFE0B2 50%, #FFCC80 100%)` | Hero, Should-Cost, How It Works, Pricing, Final CTA |
| `warm-gradient-subtle` | `linear-gradient(135deg, #D4F5ED 0%, #FFF0DB 50%, #FFE4BC 100%)` | Problem, Silo Breaker, Built for India |
| `warm-gradient-page` | `linear-gradient(180deg, #D4F5ED 0%, #FFF0DB 30%, #FFE4BC 100%)` | ALL inner pages (login, dashboard, estimate, similar) |
| `warm-gradient-footer` | `linear-gradient(135deg, #FFECD2 0%, #FFD8A8 40%, #F97316 100%)` | Footer |
| `warm-gradient-accent` | `linear-gradient(135deg, #FFF7ED 0%, #FFE4E6 100%)` | Pro pricing card |

### Dark Section

- Background: `#1a1a1a` — used for similarity search section and should-cost preview card
- Subtle glow orbs: `bg-orange-500/10` and `bg-amber-500/5` with blur-3xl

### Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Primary text/buttons | `#1a1a1a` | Dark pill CTAs, headings, primary actions |
| Accent | `orange-500` (`#f97316`) | Highlighted keywords ("should", "already"), hover states |
| Emerald | `emerald-500` | Confidence badges, checkmarks, match percentages |

### Text Colors

| Hex | Tailwind | Usage |
|-----|----------|-------|
| `#1a1a1a` | `text-[#1a1a1a]` | Primary text (headings, values) |
| `#374151` | `text-[#374151]` | Strong body text |
| `#6b7280` | `text-[#6b7280]` | Body copy, descriptions |
| `#9ca3af` | `text-[#9ca3af]` | Muted text, counters, placeholders |

### Semantic Colors

- **Success:** emerald-50/500/700 (confidence badges, checkmarks)
- **Warning:** amber-50/600/700 (low confidence, material warnings)
- **Error:** red-50/200/600 (validation errors)

---

## Roundness

- `rounded-2xl` for section cards and large containers
- `rounded-xl` for inner cards and form containers
- `rounded-lg` for form buttons and inputs
- `rounded-full` for pill CTAs, badges, and prompt bar

---

## Components

### Cards
```
bg-white/80 border border-black/10 rounded-2xl h-full flex flex-col
```
- Equal height in grids with `h-full flex flex-col`
- Hover: `hover:bg-white hover:border-black/20 transition-all`

### Primary Buttons (Dark Pill CTA)
```
dark-pill px-8 py-4 text-xs font-bold uppercase tracking-widest
```
- `dark-pill`: `background-color: #1a1a1a; color: white; border-radius: 9999px;`
- Hover: `background-color: #333`
- Disabled: `opacity-30`

### Form Buttons (not pill-shaped)
```
bg-[#1a1a1a] hover:bg-[#333] text-white py-3.5 rounded-lg font-bold tracking-widest uppercase text-sm
```

### Secondary Buttons
```
border border-black/10 rounded-full bg-white/60 text-sm text-[#374151] hover:bg-white hover:border-black/20
```

### Inputs
```
border-b border-black/30 bg-transparent outline-none text-sm text-[#1a1b20]
placeholder:text-[#c4c5d5] focus:border-[#1a1a1a] transition-colors
```
- Bottom-border only for text inputs
- Selects/number inputs: full border with `rounded-lg bg-[#fafafa]`

### Labels
```
text-[11px] font-bold text-[#515f74] uppercase tracking-wider
font-family: var(--font-label)
```

### Tables
```
<thead>: bg-[#fafafa] border-b border-black/20
<th>: text-xs font-medium text-[#757684] uppercase tracking-wider (font-mono)
<td>: text-sm, values in font-mono
```

### Navigation
- **Landing (fixed):** `bg-white/80 backdrop-blur-md border-b border-black/5`
- **Logo:** Dark rounded-xl badge "N·m" + italic Newsreader "Newton-Metre" in `#1a1a1a`
- **Nav links:** `text-[#6b7280] hover:text-[#1a1a1a]`
- **CTA:** Dark pill "New Estimate"
- **Auth-aware:** Shows "Log out" when signed in, "Log in" when not
- **Inner pages (AppNav):** `bg-white border-b border-black/5`, same logo
- **Dashboard sidebar:** `bg-white/80 backdrop-blur-sm border-r border-black/10`

### File Upload Zones
```
border-2 border-dashed border-black/20 rounded-xl p-8 text-center
hover:border-[#1a1a1a]/30 transition-colors cursor-pointer
```

### Loading States
- Spinner: `border-2 border-black/5 border-t-[#1a1a1a] rounded-full animate-spin`

---

## Page-Level Theme Rules

| Page | Background | Notes |
|------|------------|-------|
| `/` (landing) | Alternating `warm-gradient-hero` and `warm-gradient-subtle` | Fixed nav with backdrop blur |
| `/` similarity section | `bg-[#1a1a1a]` | Dark section with orange glow orbs |
| `/login` | `warm-gradient-page` | Centered card, nav with `bg-white/60 backdrop-blur-sm` |
| `/dashboard` | `warm-gradient-page` | Sidebar `bg-white/80 backdrop-blur-sm` |
| `/estimate/new` | `warm-gradient-page` | Step progress + form cards |
| `/estimate/[id]` | `warm-gradient-page` | Detail view with cost tables |
| `/similar` | `warm-gradient-page` | Multi-file upload |
| `/rfq/new` | `bg-[#0F1117]` | Dark theme (intentionally different) |

**IMPORTANT:** ALL pages (except RFQ) use warm gradient backgrounds. Never use flat `#faf8ff`, `#F8F8F6`, `bg-gray-*`, or `bg-slate-*` for page backgrounds.

---

## Spacing

- Page max-width: `max-w-[1200px]` (landing), `max-w-2xl` (forms), `max-w-3xl` (results)
- Section padding: `py-28 px-4 sm:px-8` (landing sections)
- Page padding: `px-4 sm:px-8 py-8` (inner pages)
- Card padding: `p-6` or `p-8`

---

## Icons

- Lucide React icons (not inline SVGs)
- Stroke width: 1.5
- Sizes: `w-4 h-4` (inline), `w-5 h-5` (in badges), `w-6 h-6` (in feature cards)
- Icon badges: `w-10 h-10 bg-[#1a1a1a] rounded-lg` (dark) or `w-12 h-12 bg-[#fafafa] rounded-xl` (light, inverts on hover)

---

## Tone & Copy Rules

- Professional, confident, editorial — not playful
- Numbers and data are the hero — give them space
- Clear hierarchy: label → value → action
- NEVER say "physics-based", "MRR", formulas, or technical implementation details in user-facing copy
- NEVER show HOW cost lines are calculated (no "Weight × grade price × wastage factor")
- Sell the ANSWER and OUTCOME, not the method
- Position for ALL teams: sourcing, cost engineering, design engineering, manufacturing, quality, leadership
- Similarity search = "company knowledge as a searchable asset"

---

## How to Use This File

1. **Read this file first** before implementing any UI
2. **Match pixel-for-pixel** — spacing, color hex values, font sizes, border-radius
3. **Reference this file** for any value not explicitly in the screen HTML
4. **Do NOT improvise** layout, spacing tokens, or color substitutions
5. **Do NOT use** old colors (`#00288e`, `#1e40af`, `#faf8ff`, cyan, slate, gray, `#F8F8F6`, `#0F1117` except RFQ)
