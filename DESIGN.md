# Costimize Design System

> **For Claude Code:** This file is the ground truth for ALL UI implementation.
> When converting Stitch screens to React/Next.js, treat every value here as a CONSTRAINT, not a suggestion.
> DO NOT rewrite layout logic. DO NOT substitute spacing. DO NOT change colors.
> Match the Stitch screenshot exactly — use it as visual ground truth.

---

## Source

Stitch Project: **Costimize - Should-Cost Intelligence**
Project ID: `4964390080194993667`
Color Mode: `LIGHT`
Last Updated: 2026-03-30

---

## Brand

Professional procurement intelligence tool for manufacturing companies.

- **Primary:** Deep blue `#1E40AF` — trust, precision, engineering
- **Secondary:** Teal `#0F766E` — growth, cost savings
- **Neutral Override:** `#374151`
- **Backgrounds:** Clean white / off-white (`#F8F8F6` for landing page)
- **Borders:** Subtle gray borders
- Data-heavy tables with clear hierarchy
- Industrial/engineering aesthetic — not consumer SaaS

---

## Typography

| Role | Font | Notes |
|------|------|-------|
| Body | Inter | Default body text |
| Headline | Inter | Section headings |
| Label | IBM Plex Sans | UI labels, metadata |
| Monospace | IBM Plex Mono / DM Mono | Costs, IDs, dimensions, timestamps |

**Rules:**
- Use monospace (`font-mono`) for ALL cost values, part numbers, tolerances, measurements
- Numbers and data are prominent
- Professional tone — no playful copy

---

## Colors

```
Primary:           #1E40AF  (deep blue)
Secondary:         #0F766E  (teal)
Neutral:           #374151  (gray-700)
Background (app):  #0F1117  (dark — dashboard, estimate, similarity pages)
Background (landing): #F8F8F6  (off-white/cream)
```

**Confidence Badges:**
- `green` = HIGH confidence
- `yellow` = MEDIUM confidence
- `red` = LOW / INSUFFICIENT confidence

---

## Roundness

`ROUND_EIGHT` — border-radius: 8px (`rounded-lg` in Tailwind)

---

## Components

| Component | Style |
|-----------|-------|
| Cards | Subtle shadows, clean borders, `rounded-lg`, no heavy gradients |
| Tables | Alternating row shading, monospace for cost columns |
| CTAs | Large, clear labels, primary blue fill |
| File upload zones | Dashed borders |
| Loading states | Spinner for AI processing (never blank) |
| Confidence badges | Colored pill badges (green/yellow/red) |

---

## Tone

- Professional, not playful
- Numbers and data are the hero — give them space
- Clear hierarchy: label → value → action
- Never use decorative elements that obscure data

---

## Page-Level Theme Rules

| Page | Theme | Background |
|------|-------|------------|
| `/` (landing) | Light | `#F8F8F6` (off-white) |
| `/login` | Dark Stitch | `#0F1117` |
| `/dashboard` | Dark Stitch | `#0F1117` |
| `/estimate/new` | Dark Stitch | `#0F1117` |
| `/estimate/[id]` | Dark Stitch | `#0F1117` |
| `/similar` | Dark Stitch | `#0F1117` |
| `/rfq/new` | Dark Stitch | `#0F1117` |

---

## How to Use This File When Implementing Stitch Designs

1. **Always pull the screenshot** via `mcp__stitch__get_screen` (use the image as visual ground truth)
2. **Always pull the HTML/CSS** via the screen code tool
3. **Match pixel-for-pixel** — spacing, color hex values, font sizes, border-radius
4. **Reference this file** for any value not explicitly in the screen HTML
5. **Do NOT improvise** layout, spacing tokens, or color substitutions

---

## Stitch MCP Usage Pattern

```
# Step 1: Get screenshot (visual ground truth)
mcp__stitch__get_screen(name="projects/4964390080194993667/screens/<screenId>")

# Step 2: Get HTML/CSS
# Step 3: Implement in React/Next.js matching screenshot exactly
# Step 4: Verify against screenshot — if it diverges, fix it
```
