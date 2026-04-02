# Newton-Metre Design System — "Tactical Elegance"

> **For Claude Code:** This file is the ground truth for ALL UI implementation.
> When converting Stitch screens to React/Next.js, treat every value here as a CONSTRAINT, not a suggestion.
> DO NOT rewrite layout logic. DO NOT substitute spacing. DO NOT change colors.
> Match the Stitch screenshot exactly — use it as visual ground truth.

---

## Brand

- **Name:** Newton-Metre
- **Logo:** `/newton-metre-logo.png` (rounded-lg, 32px in navs, 40px on auth pages)
- **Tagline:** "Know what it costs. Before they quote."
- Professional procurement intelligence tool for manufacturing companies
- Industrial/engineering aesthetic — not consumer SaaS

---

## Typography

| Token | Font | Usage |
|-------|------|-------|
| `--font-headline` | Newsreader (serif) | Page titles, hero text, brand name (always italic) |
| `--font-body` | Space Grotesk (sans) | Body text, descriptions, form inputs |
| `--font-label` | Space Grotesk (sans) | Buttons, nav links, section labels (uppercase tracking-widest) |
| `--font-mono` | DM Mono | Costs, part numbers, tolerances, timestamps, tabular data |
| `--font-code` | IBM Plex Mono | Code blocks (alternative mono) |

**Font Sizes:**
- Hero title: `clamp(28px, 4vw, 42px)`
- Page headings (h1): `text-4xl` (form pages), `text-3xl` (sub-pages)
- Section headings: `text-[28px]` or `text-2xl`
- Body: `text-[15px]` or `text-sm` (14px)
- Labels/caps: `text-[11px]` uppercase tracking-wider font-bold
- Micro: `text-[10px]` for timestamps, metadata

**Rules:**
- Use monospace (`font-mono`) for ALL cost values, part numbers, tolerances, measurements
- Headlines use Newsreader italic
- Numbers and data are prominent — give them space
- Professional tone — no playful copy

---

## Color Palette

### Surfaces (Tonal Layering)

| Token | Hex | Usage |
|-------|-----|-------|
| `surface` | `#faf8ff` | ALL page backgrounds |
| `surface-container-low` | `#f4f3fa` | Hover states, table headers, sidebar bg |
| `surface-container` | `#efedf4` | Inactive/disabled backgrounds |
| `surface-container-high` | `#e9e7ee` | Heavy disabled |
| `surface-container-highest` | `#e3e1e8` | — |
| `surface-lowest` | `#ffffff` | Cards, modals, inputs |

### Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `nm-primary` | `#00288e` | Primary actions, links, brand text, icons, gradient start |
| `nm-primary-container` | `#1e40af` | Secondary blue, hover states, gradient end |
| `nm-tertiary` | `#611e00` | Orange accent (sparingly) |

### Text Colors

| Hex | Tailwind | Usage |
|-----|----------|-------|
| `#1a1b20` | `text-[#1a1b20]` | Primary text (headings, values, body) |
| `#444653` | `text-[#444653]` | Secondary text |
| `#515f74` | `text-[#515f74]` | Descriptive text, subtitles, form labels |
| `#757684` | `text-[#757684]` | Muted text, placeholders, timestamps |
| `#c4c5d5` | `text-[#c4c5d5]` | Disabled text, faint dividers |

### Semantic Colors

- **Success:** emerald-50/500/700 (confidence badges, checkmarks)
- **Warning:** amber-50/600/700 (low confidence, material warnings)
- **Error:** red-50/200/600 (validation errors)

**Confidence Badges:**
- `emerald` = HIGH confidence
- `amber` = MEDIUM confidence
- `red` = LOW / INSUFFICIENT confidence

---

## Roundness

`rounded-xl` for cards and containers, `rounded-lg` for buttons and inputs, `rounded-full` for badges/pills only.

---

## Components

### Cards
```
bg-white rounded-xl ghost-border
```
- `ghost-border`: `border: 1px solid rgba(196, 197, 213, 0.15)`
- Hover: add `hover:ambient-shadow` for interactive cards

### Primary Buttons (CTA)
```
gradient-cta text-white rounded-lg font-bold tracking-widest uppercase text-sm py-3.5
```
- `gradient-cta`: `linear-gradient(135deg, #00288e 0%, #1e40af 100%)`
- Disabled: `opacity-30`
- Style: `fontFamily: var(--font-label)`

### Secondary Buttons
```
border border-[#c4c5d5]/20 rounded-lg hover:bg-[#f4f3fa] text-sm font-medium text-[#515f74]
```

### Inputs (no-line philosophy)
```
border-b border-[#c4c5d5]/30 bg-transparent outline-none text-sm text-[#1a1b20]
placeholder:text-[#c4c5d5] focus:border-[#00288e] transition-colors
```
- Bottom-border only for text inputs
- Selects/number inputs: full border with `rounded-lg bg-[#f4f3fa]`

### Labels
```
text-[11px] font-bold text-[#515f74] uppercase tracking-wider
font-family: var(--font-label)
```

### Tables
```
<thead>: bg-[#f4f3fa] border-b border-[#c4c5d5]/20
<th>: text-xs font-medium text-[#757684] uppercase tracking-wider (font-mono)
<tbody>: divide-y divide-[#c4c5d5]/10
<td>: text-sm, values in font-mono
```

### Navigation
- Fixed top bar (landing): `bg-[#faf8ff]/90 backdrop-blur-md`
- Brand: `<Image>` logo (32px rounded-lg) + italic Newsreader "Newton-Metre" in `#00288e`
- Sidebar (dashboard): `bg-white border-r border-[#c4c5d5]/20` with history items

### Shadows
- `ambient-shadow`: `0 4px 24px rgba(0, 40, 142, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04)`

### File Upload Zones
```
border-2 border-dashed border-[#c4c5d5]/20 rounded-xl p-8 text-center
hover:border-[#00288e]/30 transition-colors cursor-pointer
```

### Loading States
- Spinner: `border-2 border-[#c4c5d5]/20 border-t-[#00288e] rounded-full animate-spin`
- Mission log with step-by-step progress lines

---

## Page-Level Theme Rules

| Page | Background | Notes |
|------|------------|-------|
| `/` (landing) | `#faf8ff` | Fixed nav with backdrop blur |
| `/login` | `#faf8ff` | Centered card with `ghost-border ambient-shadow` |
| `/dashboard` | `#faf8ff` | Sidebar + main content |
| `/estimate/new` | `#faf8ff` | Step progress + form cards |
| `/estimate/[id]` | `#faf8ff` | Detail view with cost tables |
| `/similar` | `#faf8ff` | Multi-file upload |
| `/rfq/new` | `#faf8ff` | RFQ extraction form |

**IMPORTANT:** ALL pages use `#faf8ff` background. Never use `#F8F8F6`, `#0F1117`, `bg-gray-*`, or `bg-slate-*` for page backgrounds.

---

## Spacing

- Page max-width: `max-w-[1400px]` (landing), `max-w-2xl` (forms), `max-w-3xl` (results)
- Page padding: `px-4 sm:px-8 py-8` (inner pages), `py-12` (landing sections)
- Card padding: `p-6` or `p-8`
- Section gap: `mb-4` to `mb-8`

---

## Icons

- SVG stroke icons, `strokeWidth={1.5}` or `{2}`
- Sizes: `w-4 h-4` (inline), `w-5 h-5` (in badges), `w-6 h-6` (in feature cards)
- Icon badges: `w-10 h-10 gradient-cta rounded-lg` or `w-10 h-10 bg-[#1e40af] rounded-lg`

---

## Tone

- Professional, not playful
- Numbers and data are the hero — give them space
- Clear hierarchy: label → value → action
- Never use decorative elements that obscure data

---

## How to Use This File

1. **Read this file first** before implementing any UI
2. **Match pixel-for-pixel** — spacing, color hex values, font sizes, border-radius
3. **Reference this file** for any value not explicitly in the screen HTML
4. **Do NOT improvise** layout, spacing tokens, or color substitutions
5. **Do NOT use** old colors (cyan, slate, gray, `#F8F8F6`, `#0F1117`)
