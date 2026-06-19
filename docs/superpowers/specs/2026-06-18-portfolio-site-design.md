# Portfolio Site — Design Spec

**Date:** 2026-06-18
**Owner:** Ricardo Benavides (Data Engineering SAP Leader / Data Architect)
**Goal:** Replace the single-page `github-page/index.html` with an elaborate, high-end, multi-page bilingual portfolio site, deployed live on GitHub Pages.

---

## 1. Objective & Success Criteria

Build a portfolio that reads as the work of a senior data professional — distinctive, polished, fast, and bilingual (ES/EN).

**Success criteria:**
- Multi-page site with shared navigation/footer, no markup duplication.
- Bilingual: Spanish at root, English under `/en/`, with a visible language toggle that preserves the current page.
- Lighthouse: Performance ≥ 95, Accessibility ≥ 95, near-zero CLS. Landing JS (gzipped) well under 150 kb (Astro ships ~0 framework JS).
- Fully responsive at 320 / 375 / 768 / 1024 / 1440 / 1920; no horizontal overflow.
- Respects `prefers-reduced-motion`.
- Deployed automatically to GitHub Pages on push to `main`.
- **No invented facts.** Content derives only from the existing CV / current page; case-study pages expand on known facts without adding new metrics or claims.

**Non-goals (YAGNI):** CMS, blog, contact-form backend, analytics, dark/light toggle (dark only), professional photo (reserved placeholder only).

---

## 2. Visual Direction — "Dark luxury / data editorial"

Carry over the current design language (it is already strong) and refine it.

**Design tokens (reuse from current `index.html`, centralized in `tokens.css`):**
- Palette: oklch dark surfaces (`--bg` 15%, surfaces 18–25%), accent teal `oklch(82% 0.15 168)`, gold `oklch(83% 0.12 85)`, text tiers (text / dim / faint).
- Type: `Space Grotesk` (display/headings/mono-ish) + `Inter` (body). `font-display: swap`, preload only critical weights.
- Fluid scale via `clamp()` (hero, h2, metric, section spacing) — reuse existing variables.
- Atmospheric layers: fixed radial glows + faint masked grid (from current page).

**Premium layer (new, subtle):**
- Scroll reveals (IntersectionObserver, opacity/transform only).
- Count-up metrics (reuse current logic).
- Card hover: subtle lift + border/accent shift; optional light 3D tilt (transform only), disabled under reduced-motion.
- Directional glow / grain texture for depth.
- Refined editorial rhythm: intentional non-uniform spacing, scale contrast for hierarchy.

Satisfies design-quality bar: hierarchy via scale contrast, intentional rhythm, depth/layering, typography pairing, semantic color (teal = accent, gold = economic value), designed hover/focus states.

---

## 3. Information Architecture

Spanish (default, at root) mirrored in English under `/en/`.

| Route (ES) | Route (EN) | Purpose |
|---|---|---|
| `/` | `/en/` | Home: hero, metric band, perfil, expertise, condensed trayectoria, clientes, contact CTA |
| `/casos/` | `/en/casos/` | Case-study index (cards linking to the two studies) |
| `/casos/heineken-genie/` | `/en/casos/heineken-genie/` | HEINEKEN: Genie Sales Assistant + SAP ECC→Databricks data product |
| `/casos/dcsol/` | `/en/casos/dcsol/` | D&C Solutions: €1.5M manufacturing data tool |
| `/trayectoria/` | `/en/trayectoria/` | Full timeline + education + certification + languages |
| `/contacto/` | `/en/contacto/` | Contact (emails, LinkedIn) |

Nav links: Inicio · Casos · Trayectoria · Contacto + LinkedIn CTA + language toggle.

---

## 4. Tech Architecture

**Framework:** Astro (static output). No UI framework runtime; components are `.astro`.

**Project location:** new `web/` directory at repo root (keeps existing `CV/`, `linkedin/`, old `github-page/` intact as reference). GitHub Action builds from `web/`.

**Directory layout (by feature/surface, per coding-style rules):**
```
web/
├── astro.config.mjs        # site, base, i18n (es default, en), Pages output
├── package.json
├── public/                 # favicon, og image, (reserved photo slot)
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro # <head>, fonts, nav, footer, meta/OG, hreflang
│   ├── components/
│   │   ├── nav/Nav.astro, LangToggle.astro
│   │   ├── hero/Hero.astro
│   │   ├── metrics/MetricBand.astro
│   │   ├── expertise/ExpertiseGrid.astro
│   │   ├── timeline/Timeline.astro, TimelineItem.astro
│   │   ├── cases/CaseCard.astro, CaseHeader.astro, StatRow.astro
│   │   ├── clients/ClientMarquee.astro
│   │   └── footer/Footer.astro
│   ├── i18n/
│   │   ├── es.ts, en.ts     # content dictionaries (strings + structured data)
│   │   └── ui.ts            # helper: getLang(url), t(key), localized routes
│   ├── styles/
│   │   ├── tokens.css, typography.css, global.css
│   │   └── motion.css
│   ├── scripts/
│   │   └── motion.ts        # reveal + count-up, reduced-motion aware
│   └── pages/
│       ├── index.astro
│       ├── casos/index.astro, heineken-genie.astro, dcsol.astro
│       ├── trayectoria.astro, contacto.astro
│       └── en/ (mirror of the above)
└── .github/workflows/deploy.yml  # (or repo-root workflow)
```

**i18n approach:** Astro i18n routing, `defaultLocale: "es"`, `locales: ["es","en"]`, `prefixDefaultLocale: false`. Content lives in `es.ts` / `en.ts` dictionaries (typed) so pages are language-agnostic templates that receive the right dictionary by locale. LangToggle maps the current path to its counterpart. `hreflang` alternate tags + per-locale `<title>`/description in `BaseLayout`.

**Content model:** structured TS objects for repeated data (experience items, expertise groups, clients, case studies, metrics). Each has ES and EN variants. Single source → rendered by shared components.

---

## 5. Component Contracts (isolation)

- **BaseLayout** — props: `{ lang, title, description, path }`. Owns `<head>`, fonts, atmospheric layers, Nav, Footer, hreflang. Slots page body.
- **Nav** — props: `{ lang, path }`. Renders localized links, active state, LinkedIn CTA, LangToggle. No data deps beyond i18n dict.
- **LangToggle** — props: `{ lang, path }`. Computes the alternate-locale URL for the current page.
- **Hero** — props: `{ lang }`. Name, role, sub-paragraph, tag chips, CTAs.
- **MetricBand** — props: `{ metrics }` (array of `{ value, suffix, label, gold? }`). Count-up via `data-count`.
- **Timeline / TimelineItem** — props: `{ items }` / `{ role, company, dates, bullets }`.
- **CaseCard / CaseHeader / StatRow** — case index cards + case detail header + stat list.
- **ClientMarquee** — props: `{ clients }`.
- **motion.ts** — pure progressive enhancement: adds reveals + count-up; no-ops under reduced-motion. Page works fully without it.

Each component: single purpose, props-only inputs, no hidden globals → independently understandable and testable.

---

## 6. Content Source (no fabrication)

Derived strictly from existing CV / current page:
- **Positioning:** "Data Architect & Data Engineering SAP Leader". Hero sub = approved text ("…integración de SAP & Databricks … más de 20 años…").
- **Metrics:** 20+ años · €1.5M valor económico · 12 profesionales · −50% licenciamiento SAC.
- **HEINEKEN case:** Genie Sales Assistant (Databricks AI/BI Genie), sales data product (SAP ECC → Databricks), −50% licensing, 300+ reports to SAC, 12-person team, BW/4HANA 2023 & Data Intelligence migrations.
- **D&C Solutions case:** €1.5M (€1.4M direct savings, €100k avoided), €0 extra infra, manufacturing multi-plant supply-contract unification.
- **Trayectoria:** HEINEKEN, Grupo AlEn, Pueblo Bonito (Líder Técnico BI/BPC — historical, unchanged), Fibra Inn, CEMEX.
- **Clients:** CEMEX, NEMAK, VITRO, Grupo AlEn, Fibra Inn, Pueblo Bonito, Papel San Francisco, SADM, Mega Alimentos, Peñafiel, HEINEKEN, Minera México.
- **Education/cert:** Lic. Ciencias Computacionales (UANL, 2002–2006); SAP NetWeaver 2004s — Business Intelligence (cert name unchanged); Español nativo, Inglés intermedio.
- **Contact:** rbenavides@dcsol.com.mx (primary), rrbenavi@gmail.com (secondary), LinkedIn `in/rrbenavi`.

Case detail pages expand narrative/structure around these facts only.

---

## 7. Deployment

- GitHub repo created (no git repo exists yet — initialize during implementation). Need: GitHub username + interactive login when required (user performs auth; assistant never enters credentials).
- `astro.config.mjs`: `site` + `base` set to match the Pages URL (project page `/<repo>/` vs user/custom domain — confirm at deploy time).
- `.github/workflows/deploy.yml`: official Astro + `actions/deploy-pages` flow, build from `web/`, deploy on push to `main`.
- Pages source = GitHub Actions.

---

## 8. Testing / Verification

Per web testing rules:
1. **Visual regression / review** — screenshot 320/768/1024/1440 for home + one case page, ES and EN.
2. **Accessibility** — semantic landmarks, keyboard nav, focus states, contrast, reduced-motion; automated check.
3. **Performance** — Lighthouse on home + a case page; meet §1 targets.
4. **i18n** — every ES page has an EN counterpart; toggle preserves page; hreflang present.
5. **Build** — `astro build` clean; links valid.

---

## 9. Risks / Open Questions (resolved defaults)

- **Pages base path:** depends on repo name vs custom domain — confirm at deploy step; default assume project page `/<repo>/`.
- **English translation quality:** assistant drafts; user (inglés intermedio) reviews before publish.
- **Photo:** reserved elegant placeholder; swap-in later.
- **Old `github-page/index.html`:** kept as reference, not deleted, until new site approved.
