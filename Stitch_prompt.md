# Stitch — Yven Personal Portfolio (Cyberpunk) Prototype Prompt

Use this prompt with **Stitch** to generate **wireframe-level or high-fidelity UI prototypes** (screens / flows). **Do not include real photos**: no portrait photography, no stock imagery, no brand logos in raster form. Use **abstract placeholders** only (e.g., empty circle avatar frame, geometric silhouette, icon slot, or labeled “Avatar” box).

---

## Style anchor (reference)

Overall aesthetic should align with the **“Cyberpunk” (Dark)** design vocabulary catalogued on **[Design Prompts](https://www.designprompts.dev/)** (dark canvas, neon accent hierarchy, futuristic UI cues, controlled “glitch” as typography/detail—not chaotic noise). Pair that with a **“High Tech, Low Life”** mood: impressive tech feel, but **clean layouts** and **negative space** to avoid visual fatigue.

---

## Design goals

- **Strong futuristic / tech impact** without overcrowding the UI.
- **Readable hierarchy**: one primary action per section; restrained decoration.
- **Glassmorphism-lite**: translucent panels with **1px neon borders**; subtle inner glow on focus states.

---

## Color & materials

- **Background**: deep night black or blue-violet near **`#050510`**. Optional subtle **grid** or **sparse starfield** texture at low contrast (decorative only).
- **Primary neon**: **cyan** around **`#00F3FF`**.
- **Secondary neon**: **electric purple** around **`#BC13FE`**.
- **Accent (sparingly)**: **warning yellow** or **laser red** for hover states, critical labels, or primary CTA emphasis.
- **Text**: off-white / cool gray; **key headings** may include **soft outer glow** (not full rainbow chromatic aberration).
- **Typography**: modern **sans** and/or **monospace** for titles and UI chrome; optional **mild glitch** treatment on hero title only (subtle slices / offset, 1–2 steps max).

---

## Global chrome

- **Navigation**: fixed **top-right**, **minimal line style**. On hover, labels get a **neon flicker / pulse** micro-animation.
- **Nav items** (exact labels): `Home` · `About` · `Work` · `Contact`.
- **Page transitions**: **no hard cuts** between sections—use **fade** or **gentle horizontal slide** between views.

---

## Page-by-page content (placeholders OK)

### 1) Home

- **Logo / mark**: a large **“Y”** with a **holographic / projected** feel (gradient sheen + subtle scanband—not a photo).
- **Hero type**: centered **typewriter animation** concept for the line: **`Hello! Welcome to Yven's web`** (prototype may show **static text + caret** if animation not supported).
- **Primary CTA** below: **`Contact me`** as a **chamfered / angled tech button** with **flowing light (sheen sweep)** on hover.

### 2) About

- **Two-column layout**:
  - **Left**: hologram-style **bio block** (short paragraphs, small meta chips like “Role / Stack / Location” as text-only).
  - **Right**: **decorative data viz** or **pseudo-code snippet panel** (abstract charts, bars, hex metrics—no real user data required).

### 3) Work (Portfolio)

- **Responsive card grid**.
- Each card feels like a **“data chip”**: compact title, 1–2 lines description, tags as pills.
- **Hover**: card **lifts slightly**, **border brightens**, reveal **extra detail** (expand secondary line or a small “Details” row—keep it lightweight).

### 4) Contact

- **Center**: circular **avatar placeholder** (empty ring frame) **or** hexagon frame—**optionally** with a **slow rotating halo ring** around it (no face image).
- Below: social row with **linear / outline cyber icons** (placeholder icons OK) for:
  - **WeChat**
  - **GitHub**
  - **Xiaohongshu (RED)**
- **Click / tap feedback**: brief **electric pulse** along borders or icon stroke (micro-interaction).

---

## Motion & loading (prototype notes)

- **Initial load**: suggest a **CRT boot sequence**—brief **flicker**, **scanlines opening**, then **content fades in**. Keep duration **short** (avoid seizure-risk strobing; no extreme flashing).
- **Micro-interactions**: hovers should **invert contrast slightly** or **intensify glow** consistently across clickable elements.

---

## Deliverables to generate

1. **Desktop** layouts for **Home, About, Work, Contact** (at least one key state each: default + one hover example on Work card + one hover on nav).
2. **Mobile** variant for **Home + Contact** (stacked, thumb-friendly targets).
3. **Component sheet** (optional but helpful): nav item, chip card, glass panel, chamfer CTA button, icon button.

---

## Non-goals / constraints

- **No photography**, **no illustrated portraits**, **no raster avatars**.
- Avoid **excessive** glitch layers, **heavy film grain**, or **neon everywhere**—keep accents purposeful.
- Avoid dense “hacker movie” cliché clutter; **legibility first**.

---

## One-line creative direction (copy-paste friendly)

**“Dark cyberpunk personal portfolio for ‘Yven’: neon cyan + purple on `#050510`, glass panels with 1px neon strokes, subtle grid/star texture, monospace/sans typography with mild hero glitch, CRT-inspired short boot then soft fades, floating top-right nav with hover flicker, giant holographic ‘Y’, typewriter hero line, chamfer CTA, about split with abstract metrics/code decor, ‘data chip’ project cards, contact with empty geometric avatar frame + rotating halo and outline social icons with electric tap feedback—no photos or real faces, placeholders only; strong impact, clean spacing, high-tech low-life tone; style anchored to Design Prompts Cyberpunk dark UI language.”**
