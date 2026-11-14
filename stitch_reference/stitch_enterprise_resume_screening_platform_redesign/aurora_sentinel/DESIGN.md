---
name: Aurora Sentinel
colors:
  surface: '#10131c'
  surface-dim: '#10131c'
  surface-bright: '#363943'
  surface-container-lowest: '#0b0e17'
  surface-container-low: '#181b25'
  surface-container: '#1c1f29'
  surface-container-high: '#272a34'
  surface-container-highest: '#32343f'
  on-surface: '#e0e2ef'
  on-surface-variant: '#cbc3d7'
  inverse-surface: '#e0e2ef'
  inverse-on-surface: '#2d303a'
  outline: '#958ea0'
  outline-variant: '#494454'
  surface-tint: '#d0bcff'
  primary: '#d0bcff'
  on-primary: '#3c0091'
  primary-container: '#a078ff'
  on-primary-container: '#340080'
  inverse-primary: '#6d3bd7'
  secondary: '#ccbeff'
  on-secondary: '#332664'
  secondary-container: '#4a3d7c'
  on-secondary-container: '#baabf3'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#e7deff'
  secondary-fixed-dim: '#ccbeff'
  on-secondary-fixed: '#1e0e4e'
  on-secondary-fixed-variant: '#4a3d7c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#10131c'
  on-background: '#e0e2ef'
  surface-variant: '#32343f'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-xs:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '400'
    lineHeight: 12px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  gutter-lg: 2rem
  margin: 2rem
  margin-sm: 1rem
  margin-lg: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system defines an enterprise talent screening and evaluation ecosystem. The system communicates precision, cryptographic integrity, forensic calm, and executive-tier clarity. Designed specifically for enterprise security, HR tech compliance, and high-volume candidate evaluation platforms, it rejects frenetic dashboard tropes in favor of an immersive, focused command-center experience.

The design movement balances **Dark-Mode Minimalism** with **Tonal Layering and Cryptographic Restraint**:
- Backgrounds are deep, absorbing charcoal navy that eliminates visual glare during marathon review sessions.
- Interfaces rely on subtle structural luminance rather than aggressive drop shadows or loud decorative graphics.
- Information density is balanced through purposeful whitespace, progressive disclosure, and monospaced cryptographic metrics that evoke trust, verification, and unshakeable accuracy.

## Colors

The palette is engineered around an "Aurora Sentinel" theme: a midnight expanse calibrated with refined violet intelligence and precise forensic telemetry accents.

### Core Architecture
- **Canvas Base (`#090C15`):** Deep charcoal navy; foundational backdrop for entire interface canvas.
- **Layer 1 Surface (`#0F1523`):** Slate graphite for primary panels, nav rails, and side sheets.
- **Layer 2 Card/Container (`#161F33`):** Elevated slate for tables, candidate cards, and dialogs.
- **Layer 3 Interactive/Hover Surface (`#1D2840`):** Elevated hover state, active pill backdrops, and active inputs.
- **Borders & Dividers:** High-precision, low-luminance borders using `rgba(255, 255, 255, 0.08)` for dormant states and `rgba(139, 92, 246, 0.3)` for focused/active states.

### Accents & Semantics
- **Primary Violet (`#8B5CF6`):** Key interactive buttons, selection outlines, and primary system metrics.
- **Primary Violet Hover (`#A78BFA`):** Hover states for high-emphasis buttons and interactive focus rings.
- **Secondary Lavender (`#C4B5FD`):** Metadata tags, candidate attribute indicators, secondary badges, and subtle icons.
- **Success Emerald (`#10B981`):** Verified credentials, passed benchmarks, high confidence indicators.
- **Warning Amber (`#F59E0B`):** Verification anomalies, review required, pending background checks.
- **Forensic Coral (`#F43F5E`):** Identity mismatch, anti-tampering alerts, failed screenings.

## Typography

The typographic hierarchy blends **Inter** for supreme reading legibility in dense enterprise screens with **JetBrains Mono** for forensic verification figures, hashes, matching percentages, timestamps, and candidate IDs.

- **Inter:** Applied across all narrative headers, candidate descriptions, modal prompts, and standard form controls. Maintains crisp, high-contrast readability against dark slate surfaces.
- **JetBrains Mono:** Reserved for structured screening metrics, verification tokens, tamper-check hashes, timestamp logs, match scores, and status flags. It elevates the operational authority of the application.
- **Rules:** Letter-spacing is tightened slightly on display sizes to prevent visual dissipation on dark canvases, while monospaced labels use positive letter-spacing to optimize scannability in technical log tables.

## Layout & Spacing

The layout operates on a strict **8px baseline grid** configured as a fluid-responsive system with safe guttering and deliberate boundaries to support high data density without visual claustrophobia.

### Grid Architecture
- **Desktop (1440px+):** 12-column layout, 2rem (32px) margins, 1.5rem (24px) gutters. Fixed collateral side-nav (260px) paired with fluid multi-column assessment grids.
- **Tablet (768px - 1439px):** 8-column layout, 1.5rem (24px) margins, 1rem (16px) gutters. Collapsible rail navigation.
- **Mobile (Below 768px):** 4-column layout, 1rem (16px) margins, 1rem (16px) gutters. Off-canvas drawer navigation, sequential stacked assessment streams.

### Progressive Disclosure Philosophy
Screening dashboards employ clean primary vistas showing top-level scores and status flags. Deep forensic verification logs, tamper details, and interview transcripts are revealed through sliding side-drawers or contextual expanders rather than cluttered persistent tables.

## Elevation & Depth

This design system avoids heavy drop shadows and instead uses **Tonal Layering** accompanied by **Subtle Linear Boundaries** and **Violet Luminosity**.

- **Level 0 (Canvas Base):** `#090C15` — The deep foundation; zero elevation.
- **Level 1 (Structural Containers):** `#0F1523` — Navigation bars, fixed side rails, master screening panels. Bordered by `1px solid rgba(255, 255, 255, 0.06)`.
- **Level 2 (Interactive Cards & Modules):** `#161F33` — Candidate profiles, test breakdown modules, telemetry cards. Bordered by `1px solid rgba(255, 255, 255, 0.08)`.
- **Level 3 (Floating Overlays & Modals):** `#1D2840` — Candidate drill-down drawers, action sheets, floating filter heads. Elevated with an ambient tint shadow: `0 12px 32px -4px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(139, 92, 246, 0.15)`.
- **Focus & Integrity State Glow:** Active cards or selected profiles receive a faint electric violet outer aura: `0 0 0 1px #8B5CF6, 0 0 16px -2px rgba(139, 92, 246, 0.25)`.

## Shapes

The design system adopts a **Soft (`1`) shape language** with an 0.25rem (4px) base radius for small elements, 0.5rem (8px) for standard containers/cards, and 0.75rem (12px) for primary layout panels and modal frames.

- **Micro Components (Badges, Buttons, Checkboxes):** 4px corner radius. Communicates surgical precision and strict enterprise control.
- **Medium Components (Input Fields, Candidate Row Cards, Action Bars):** 8px corner radius (`rounded-lg`). Softens touch points while maintaining architectural order.
- **Major Containers (Screening Modals, Verification Drawers):** 12px corner radius (`rounded-xl`). Smoothly delineates elevated overlays from base views.

## Components

### Buttons
- **Primary:** Background `#8B5CF6`, text `#FFFFFF`, radius 4px, height 36px/42px. Hover transforms to `#A78BFA`. Active state uses `0 0 0 2px rgba(139, 92, 246, 0.4)`.
- **Secondary / Ghost:** Transparent background with border `1px solid rgba(255, 255, 255, 0.12)`, text `#C4B5FD`. Hover transforms to background `#1D2840` and border `rgba(196, 181, 253, 0.3)`.
- **Destructive / Flag:** Background `rgba(244, 63, 94, 0.12)`, border `1px solid rgba(244, 63, 94, 0.4)`, text `#F43F5E`. Hover shifts to `#F43F5E` with white text.

### Chips & Status Badges
- Rendered using `label-sm` or `label-xs` in **JetBrains Mono**. Height 24px, padding 2px 8px, border radius 4px.
- **Verified / High Match:** Background `rgba(16, 185, 129, 0.1)`, border `1px solid rgba(16, 185, 129, 0.3)`, text `#10B981`.
- **Review Flag:** Background `rgba(245, 158, 11, 0.1)`, border `1px solid rgba(245, 158, 11, 0.3)`, text `#F59E0B`.
- **Integrity Alert:** Background `rgba(244, 63, 94, 0.1)`, border `1px solid rgba(244, 63, 94, 0.3)`, text `#F43F5E`.
- **Attribute Tag:** Background `#1D2840`, border `1px solid rgba(255, 255, 255, 0.08)`, text `#C4B5FD`.

### Input Fields & Selects
- Height 40px, background `#0F1523`, border `1px solid rgba(255, 255, 255, 0.12)`, text `#FFFFFF`, placeholder `rgba(255, 255, 255, 0.35)`.
- **Focus State:** Border color `#8B5CF6`, shadow `0 0 0 2px rgba(139, 92, 246, 0.25)`.
- Accompanied by micro label (`label-xs`) aligned above the field.

### Candidate Cards & Screening Lists
- Surfaces configured at `#161F33` with internal padding of `space-md` (16px).
- Border `1px solid rgba(255, 255, 255, 0.06)`, smoothly shifting to `rgba(139, 92, 246, 0.35)` on hover.
- Split-screen candidate layout: left column displays candidate identity and Inter body metrics; right column displays JetBrains Mono forensic tokens, match index, and anti-tamper telemetry hash.

### Checkboxes & Radios
- Size 16px x 16px, background `#0F1523`, border `1px solid rgba(255, 255, 255, 0.2)`, radius 3px for checkboxes, full circle for radios.
- **Selected State:** Background `#8B5CF6` with crisp white check/dot icon and subtle violet aura.

### Specialized System Component: Telemetry & Hash Inspector
- A dedicated monospaced inspection block for candidate screening audits.
- Background `#090C15`, border `1px solid rgba(139, 92, 246, 0.2)`, padding `space-sm` (8px). Text rendered in `label-sm` with dimmed syntax keys (`rgba(255, 255, 255, 0.4)`) and active values in `#C4B5FD`. Includes a copy-to-clipboard action with instant micro-transition.