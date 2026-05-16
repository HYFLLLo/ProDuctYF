---
name: Yven Portfolio System
colors:
  surface: '#11131e'
  surface-dim: '#11131e'
  surface-bright: '#373845'
  surface-container-lowest: '#0c0d19'
  surface-container-low: '#191b27'
  surface-container: '#1d1f2b'
  surface-container-high: '#282936'
  surface-container-highest: '#333441'
  on-surface: '#e2e1f2'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e2e1f2'
  inverse-on-surface: '#2e2f3c'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dce6'
  primary: '#e3fdff'
  on-primary: '#00373a'
  primary-container: '#00f3ff'
  on-primary-container: '#006b71'
  inverse-primary: '#00696f'
  secondary: '#ebb2ff'
  on-secondary: '#520072'
  secondary-container: '#b600f8'
  on-secondary-container: '#fff6fc'
  tertiary: '#fbf7ff'
  on-tertiary: '#2f2f3d'
  tertiary-container: '#dddaec'
  on-tertiary-container: '#605f6e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ff6ff'
  primary-fixed-dim: '#00dce6'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#f8d8ff'
  secondary-fixed-dim: '#ebb2ff'
  on-secondary-fixed: '#320047'
  on-secondary-fixed-variant: '#74009f'
  tertiary-fixed: '#e3e0f3'
  tertiary-fixed-dim: '#c7c4d6'
  on-tertiary-fixed: '#1a1a27'
  on-tertiary-fixed-variant: '#464554'
  background: '#11131e'
  on-background: '#e2e1f2'
  surface-variant: '#333441'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  label-mono:
    fontFamily: Space Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1'
    letterSpacing: 0.1em
  label-glitch:
    fontFamily: Space Mono
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.05em
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 80px
  container-max: 1440px
---

## Brand & Style

The design system is a "High Tech, Low Life" digital environment designed for a personal portfolio. It balances the aggressive aesthetics of cyberpunk culture with the precision of high-end UI/UX. The personality is tech-forward, slightly clandestine, and highly polished. It evokes a sense of entering a secure terminal or a high-end neural interface.

The design style is a hybrid of **Minimalist Cyberpunk** and **Glassmorphism-lite**. It rejects the cluttered chaos of traditional "retro-cyber" in favor of expansive negative space, razor-thin neon strokes, and sophisticated transparency. Key traits include:
- **Atmospheric Depth:** Deep charcoal and pitch blacks provide a void-like backdrop that makes neon elements pop.
- **Controlled Glitch:** Subtle, intentional horizontal shifts or chromatic aberrations on hover states to suggest a live, slightly unstable connection.
- **Luminous UI:** UI elements appear self-illuminated rather than lit by external sources, using soft glows and vibrant strokes.

## Colors

The palette is rooted in the contrast between the absolute dark of the "Night Black" and the radioactive vibrance of the neon accents.

- **Background:** `#050510` (Night Black). A deep, cold black with a hint of blue to prevent visual "deadness" on OLED screens.
- **Primary:** `#00F3FF` (Neon Cyan). Used for critical actions, active states, and primary data points. It carries a default 0 0 8px outer glow.
- **Secondary:** `#BC13FE` (Neon Purple). Used for secondary highlights, decorative strokes, and "danger" or "alert" states in a subverted way.
- **Surfaces:** Semi-transparent variations of the background (e.g., `rgba(255, 255, 255, 0.03)`) are used for glass panels.
- **Typography:** Pure white for high-readability body text; muted gray-blue for metadata and labels.

## Typography

Typography in the design system serves two purposes: technical data delivery and stylistic impact.

- **Headlines:** Use **Space Grotesk**. For large display sizes, apply a `text-shadow: 0 0 15px rgba(0, 243, 255, 0.4)` to create the signature neon hum.
- **Body:** **Hanken Grotesk** provides a clean, neutral balance to the more aggressive display faces, ensuring long-form case studies remain readable.
- **UI Chrome:** **Space Mono** is used for all "system" information—timestamps, coordinates, button labels, and small metadata. This reinforces the "terminal" aesthetic.
- **Styling:** Headings should predominantly be sentence case or all-caps depending on the hierarchy, but never title case.

## Layout & Spacing

The layout philosophy is a **12-column Fixed Grid** with high internal margins to emphasize the "clean/minimal" aspect of the cyberpunk theme.

- **Negative Space:** Use generous vertical padding between sections (160px+) to allow the glowing elements room to breathe without clashing.
- **Alignment:** Elements should adhere strictly to the grid, but decorative "glitch" elements (like small floating coordinates or scan lines) can break the grid to create visual interest.
- **Desktop:** 80px side margins, 24px gutters.
- **Mobile:** 20px side margins. Layouts should collapse into a single column, maintaining the glassmorphism panels but reducing the neon stroke intensity to prevent screen fatigue.

## Elevation & Depth

In this design system, depth is not created through shadows, but through **light and opacity**.

- **Z-Axis Hierarchy:** Higher-level elements (modals, tooltips) use a stronger backdrop-blur (20px+) and a brighter 1px neon stroke.
- **Glassmorphism-lite:** Surface containers use a subtle dark fill `rgba(5, 5, 16, 0.7)` with a `backdrop-filter: blur(10px)`.
- **The "Stroke" Rule:** Every card or container must have a 1px solid border. Use `#00F3FF` at 20% opacity for default states, and 100% opacity for active or hover states.
- **Glows:** Avoid heavy drop shadows. Use `box-shadow: 0 0 20px rgba(0, 243, 255, 0.15)` for elevated panels to simulate light casting onto the background.

## Shapes

The shape language is **strictly geometric and sharp**. 

- **Corners:** Use 0px border-radius for all primary UI elements. Sharp corners convey a sense of precision and industrial manufacturing.
- **Angled Accents:** For buttons or decorative containers, use a CSS `clip-path` to create "dog-ear" corners (45-degree cuts) on the top-right or bottom-left to evoke military-grade hardware interfaces.
- **Interactive Elements:** Buttons maintain a rectangular profile, using inner borders or scan-line patterns rather than rounded corners for distinction.

## Components

### Buttons
- **Primary:** No fill, 1px `#00F3FF` border, text in Space Mono. On hover, the button fills with Cyan and text flips to Night Black.
- **Ghost:** No border, text in Purple. On hover, a subtle 1px bottom border slides in.

### Cards
- Background: `rgba(255, 255, 255, 0.03)`.
- Border: 1px Cyan at 20% opacity.
- Feature: A small "ID tag" in the top-left corner using Space Mono (e.g., "REF_001").

### Input Fields
- Underline-only style. A simple 1px gray-blue line that glows Cyan and expands when focused. Labels should be small, all-caps Mono text floating above the line.

### Chips/Tags
- Small rectangular boxes with a "Secondary" Purple 1px border. No background fill. Text is 10px Space Mono.

### Lists
- Use custom bullets: small 4x4px Cyan squares. On hover, the list item background gains a faint horizontal scan-line texture.

### Additional Components
- **The "Terminal" Header:** A thin bar at the top of the screen showing "System Status: Online" and the current UTC time in monospace, reinforcing the immersive world-building.
- **Scan-line Overlay:** A global, low-opacity fixed overlay of horizontal lines (1px height, 4px gap) to give the entire UI a subtle CRT/Digital-Lens texture.