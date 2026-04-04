# Newton-Metre Design System v2

## Brand Identity
Newton-Metre is a manufacturing intelligence platform. "Know what it costs. Before they quote." The design must feel like a precision instrument — clean, confident, data-rich. Enterprise voice, individual entry point.

## Colors

### Core Palette
- **Brand Dark (Primary):** `#1a1a1a` — headlines, logo, primary CTAs, dark sections
- **Text Primary:** `#1a1a1a` — headings, bold labels
- **Text Secondary:** `#525252` — body text, descriptions
- **Text Muted:** `#A3A3A3` — helper text, timestamps, disabled states
- **Accent (Orange-500):** `#F97316` — used SPARINGLY. Badges, check icons, hover accents on dark sections. ONE accent color only.
- **Surface White:** `#FFFFFF` — primary background for light sections
- **Surface Hover:** `#f5f5f5` — hover states on light backgrounds
- **Dark Section:** `#09090B` — Similarity Search section and AI Worker trailer

### Warm Gradients (Background only)
- **Hero:** `linear-gradient(135deg, #faf8ef 0%, #f0ece0 25%, #f5f0e8 50%, #eef0e8 75%, #f0f4ef 100%)`
- **Subtle:** `linear-gradient(135deg, #f8f6f0 0%, #f5f2ec 50%, #f0f2ed 100%)`
- **Page:** `linear-gradient(180deg, #faf8f2 0%, #f5f3ed 100%)` — for app pages
- **Footer:** `linear-gradient(135deg, #f0ece0 0%, #e8e4d8 50%, #f0ece0 100%)`

### CSS Variables
```css
--color-brand-dark: #1a1a1a;
--color-text-primary: #1a1a1a;
--color-text-secondary: #3a3a3a;
--color-text-description: #525252;
--color-text-muted: #8a8a8a;
--color-surface-hover: #f5f5f5;
--color-neutral-gray: #6b6b6b;
```

## Typography

### Font Stack
- **Headlines & Body:** Space Grotesk (weights 300-700), `--font-body` / `--font-headline`
- **Monospace/Code:** DM Mono (weights 400-500), `--font-mono`
- **NO Newsreader. NO IBM Plex Mono. NO italic logos.**

### Scale
| Element | Size | Weight | Line-height | Tracking |
|---------|------|--------|-------------|----------|
| Hero headline | 56-64px | 700 | 1.08 | -0.03em |
| Section headline | 36-48px | 700 | tight | tight |
| Card title | 17px | 700 | - | - |
| Body | 14-15px | 400 | 1.6-1.7 | - |
| Label/Badge | 10-11px | 700 | - | 0.2em, uppercase |
| Mono numbers | DM Mono | 400 | - | - |

### Max Widths
- Hero text: 720px centered
- Hero cards grid: 1100px
- Content sections: 1200px
- Body text columns: 640px max

## Layout & Spacing

### Section Padding
- Vertical: 96-128px (`py-24` to `py-32`)
- Between hero headline and cards: 56px (`mb-14`)
- Between section header and content: 80px (`mb-20`)

### Spacing Scale (Tailwind)
4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128

### Grid
- 3-column for product cards, stat cards
- 2-column for feature sections (text + visual)
- Gap: 20-24px between cards

## Components

### Cards
- Background: `white/80` with `backdrop-blur-sm`
- Border: `border-black/6` (barely visible)
- Radius: `rounded-2xl` (16px)
- Padding: `p-8 sm:p-10`
- Hover: `bg-white`, `shadow-xl shadow-black/5`, `border-black/10`, translate-y -4 to -6px
- Icon container: 48x48px, `logo-gradient` background, `rounded-xl`

### Dark Cards
- Background: `#09090B`
- Text: white with opacity (50-70% body, 30-40% labels)
- Border: `border-white/10`
- Inner items: `bg-white/5` hover `bg-white/10`

### Buttons
- **Primary (dark-pill):** `#1a1a1a` bg, white text, `rounded-full`, 11-12px uppercase tracking-widest
- **Secondary (outlined):** transparent bg, `border-white/20` on dark, white text
- **Ghost:** no bg, text only with hover underline
- Arrow icon slides right on hover (gap transition)

### Badges
- "Coming Soon": `bg-orange-50 text-orange-600 border-orange-200/60`, `rounded-full`
- Confidence: green (high), amber (medium), red (low)
- Size: 9px uppercase tracking-widest

### Navigation
- **Landing:** Floating pill (`rounded-full`), `white/90 backdrop-blur-md`, max-width 1200px
- **App:** Full-width white bar, `border-b border-black/5`
- Logo: N·m icon (brand dark `rounded-xl`) + "Newton-Metre" (Space Grotesk bold, NOT italic)

## Motion & Interaction
- **Card entrance:** staggered fade-up (opacity 0→1, y 30→0) with 0.15s delays
- **Scroll reveal:** sections fade up (y 24→0) when entering viewport, once only
- **Hover lift:** cards translate-y -4 to -6px with shadow increase
- **Icon scale:** logo icons scale to 110% on card hover
- **Arrow slide:** CTA arrows increase gap on hover
- Easing: ease-out for entrances, 0.25-0.3s duration for hovers
- `viewport: { once: true }` — never re-animate on scroll

## Data Display
- Costs always in DM Mono
- Currency: ₹ (INR) formatted with Indian locale (`en-IN`)
- Confidence tiers: HIGH (green), MEDIUM (amber), LOW (red), INSUFFICIENT (gray)
- Process breakdown: left-aligned labels, right-aligned costs

## Voice & Messaging
- Enterprise voice, individual entry point
- AI helps decisions, surfaces insights, gives speed — NEVER implies replacement
- Sell outcome, never method (no "physics-based", no formulas)
- Human is always the hero, AI is the tool
- Similarity search mentioned everywhere

## Do's
- Use warm gradient backgrounds (Base44-inspired warmth)
- Keep sections clean-edged (no curve dividers)
- Use monospace for all numbers and costs
- Keep bullet points short (5-7 words)
- Add subtle hover states to everything interactive

## Don'ts
- Don't use italic for the logo or brand name
- Don't use more than 2 fonts (Space Grotesk + DM Mono)
- Don't use emerald/green as an accent — orange only
- Don't use curve SVG dividers between sections
- Don't show formulas or say "physics-based" in UI copy
- Don't use pure black (#000000) for text — use #1a1a1a
