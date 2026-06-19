# Portfolio Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an elaborate, high-end, bilingual (ES/EN) multi-page Astro portfolio for Ricardo Benavides and deploy it to GitHub Pages.

**Architecture:** Astro static site in `web/`. Language-agnostic `.astro` page templates render typed ES/EN content dictionaries; shared `BaseLayout` + components own nav/footer/head. Dark-luxury visual language carried over from the existing `github-page/index.html`, refined. Progressive-enhancement motion only.

**Tech Stack:** Astro (latest), zero UI-framework runtime, plain CSS with design tokens, TypeScript content dictionaries, GitHub Actions → GitHub Pages.

## Global Constraints

- Spanish at root (`/`), English under `/en/`. `defaultLocale: "es"`, `prefixDefaultLocale: false`.
- **No invented facts.** Content only from the design spec §6 / existing CV / `github-page/index.html`.
- Palette/type tokens copied from existing `index.html` (oklch dark, accent teal `oklch(82% 0.15 168)`, gold `oklch(83% 0.12 85)`, Space Grotesk + Inter).
- Animate only `transform` / `opacity` / `clip-path`; everything respects `prefers-reduced-motion`.
- Targets: Lighthouse Perf ≥95, A11y ≥95; responsive 320/375/768/1024/1440/1920, no overflow.
- Files focused (<400 lines typical); organize by feature/surface.
- Each task ends green: `npm run build` succeeds AND a quick visual check via the running dev server.
- Historical strings unchanged: cert "SAP NetWeaver 2004s — Business Intelligence", role "Líder Técnico BI/BPC".
- Verification = build + visual screenshot (not unit tests; this is a static content site).

---

### Task 1: Scaffold Astro project, tokens, BaseLayout, i18n infra

**Files:**
- Create: `web/package.json`, `web/astro.config.mjs`, `web/tsconfig.json`
- Create: `web/src/styles/tokens.css`, `web/src/styles/typography.css`, `web/src/styles/global.css`, `web/src/styles/motion.css`
- Create: `web/src/i18n/ui.ts` (helpers), `web/src/i18n/es.ts`, `web/src/i18n/en.ts` (stubs with shared meta strings)
- Create: `web/src/layouts/BaseLayout.astro`
- Create: `web/src/pages/index.astro` (temporary "hello" to verify build)

**Interfaces:**
- Produces: `getLangFromUrl(url): 'es'|'en'`, `useTranslations(lang)`, `getAlternatePath(path, lang)` in `ui.ts`.
- Produces: `BaseLayout` props `{ lang: 'es'|'en', title: string, description: string, path: string }`, default `<slot/>`.
- Produces: token CSS variables (copy verbatim from `github-page/index.html` `:root`).

- [ ] **Step 1:** `cd web` create project: `npm create astro@latest . -- --template minimal --no-install --no-git --skip-houston` then `npm install`. Set `astro.config.mjs` with `site`/`base` placeholders (TODO-resolved in Task 9) and `i18n: { defaultLocale: 'es', locales: ['es','en'], routing: { prefixDefaultLocale: false } }`.
- [ ] **Step 2:** Write `tokens.css` copying the `:root` block from `github-page/index.html` (palette, fluid type, spacing, easing). `typography.css` = font-face/import + base type rules. `global.css` = reset, body, `.wrap`, atmospheric `body::before/::after` layers (copy from existing). `motion.css` = `.reveal` rules + reduced-motion guard.
- [ ] **Step 3:** Write `ui.ts` helpers (lang detection from URL prefix, dictionary selector, alternate-path mapper that toggles `/en/` prefix). Write `es.ts`/`en.ts` exporting a typed `dict` with at least `{ meta: { homeTitle, homeDesc }, nav: {...} }`.
- [ ] **Step 4:** Write `BaseLayout.astro`: `<html lang>`, head (charset, viewport, title, description, OG, preconnect+fonts, `hreflang` alternate, all four styles imported), body with atmospheric layers, `<slot/>`. Temporary `index.astro` renders BaseLayout + an `<h1>`.
- [ ] **Step 5:** Run `npm run build` (expect success) and `npm run dev`, screenshot `/` — expect dark background with heading. Commit: `git add web && git commit -m "feat: scaffold astro portfolio with tokens, layout, i18n infra"`.

---

### Task 2: Nav, LangToggle, Footer

**Files:**
- Create: `web/src/components/nav/Nav.astro`, `web/src/components/nav/LangToggle.astro`, `web/src/components/footer/Footer.astro`
- Modify: `web/src/layouts/BaseLayout.astro` (mount Nav + Footer around slot)
- Modify: `web/src/i18n/es.ts`, `en.ts` (nav labels, footer strings)

**Interfaces:**
- Consumes: `BaseLayout` `{ lang, path }`; `useTranslations`, `getAlternatePath` from Task 1.
- Produces: `Nav` props `{ lang, path }`; `LangToggle` props `{ lang, path }`; `Footer` props `{ lang }`.

- [ ] **Step 1:** Write `Nav.astro` — sticky blurred header (copy `.nav` styles), localized links (Inicio/Casos/Trayectoria/Contacto), active state by `path`, LinkedIn CTA, `<LangToggle>`. Mobile: hide link list <760px (matches existing).
- [ ] **Step 2:** Write `LangToggle.astro` — renders link to `getAlternatePath(path, otherLang)`, shows "EN"/"ES" with accessible label.
- [ ] **Step 3:** Write `Footer.astro` — copy `.foot-inner`, dynamic year, localized role line "Data Architect & Data Engineering SAP Leader", location.
- [ ] **Step 4:** Wire into `BaseLayout` (Nav above slot, Footer below). Add nav/footer strings to dictionaries.
- [ ] **Step 5:** `npm run build` + dev screenshot at `/` and `/en/` (toggle works). Commit: `feat: shared nav, language toggle, footer`.

---

### Task 3: Home page components (Hero, MetricBand, ExpertiseGrid, ClientMarquee)

**Files:**
- Create: `web/src/components/hero/Hero.astro`, `web/src/components/metrics/MetricBand.astro`, `web/src/components/expertise/ExpertiseGrid.astro`, `web/src/components/clients/ClientMarquee.astro`
- Create: `web/src/scripts/motion.ts`
- Modify: `web/src/pages/index.astro`, `web/src/i18n/es.ts`, `en.ts`

**Interfaces:**
- Consumes: dictionaries from Task 1.
- Produces: `Hero{lang}`, `MetricBand{metrics: {value:number|string, suffix:string, label:string, gold?:boolean}[]}`, `ExpertiseGrid{groups: {idx:string,title:string,chips:string[]}[]}`, `ClientMarquee{clients:string[]}`, and `initMotion()` in `motion.ts` (reveal + count-up, reduced-motion aware).

- [ ] **Step 1:** Add home content to dictionaries (spec §6): hero (eyebrow, name, role, sub, tags, CTAs), metrics array (20+ años, €1.5M gold, 12, 50%), expertise 3 groups with chips (incl. Databricks AI/BI Genie, Productos de datos, IA generativa & NLP), clients array.
- [ ] **Step 2:** Write `Hero.astro` (copy `.hero` styles, use dict), `MetricBand.astro` (copy `.metrics`, `data-count`), `ExpertiseGrid.astro` (copy `.grid-3`/`.card`/`.chip`), `ClientMarquee.astro` (copy `.clients`).
- [ ] **Step 3:** Write `motion.ts` (port reveal IntersectionObserver + count-up from existing `<script>`), import once in `BaseLayout` with `is:inline` guard or as a module script.
- [ ] **Step 4:** Assemble `index.astro` (ES): Hero, MetricBand, a "Perfil" section, ExpertiseGrid, condensed trayectoria teaser + link, ClientMarquee, contact CTA band.
- [ ] **Step 5:** `npm run build` + screenshots 1440 & 375 of `/`. Verify count-up + reveals, no overflow. Commit: `feat: home page (es) with hero, metrics, expertise, clients`.

---

### Task 4: Trayectoria page (Timeline + Education/Cert)

**Files:**
- Create: `web/src/components/timeline/Timeline.astro`, `web/src/components/timeline/TimelineItem.astro`
- Create: `web/src/pages/trayectoria.astro`
- Modify: `web/src/i18n/es.ts`, `en.ts`

**Interfaces:**
- Produces: `Timeline{items}`, `TimelineItem{role,company,dates,bullets:string[]}`. `items` source = dictionary `experience` array.

- [ ] **Step 1:** Add `experience` array (5 roles, spec §6, HEINEKEN bullets reordered-by-impact as in current page), `education`, `certification`, `languages` to dictionaries. Keep historical strings verbatim.
- [ ] **Step 2:** Write `Timeline.astro`/`TimelineItem.astro` (copy `.timeline`/`.tl-*` styles).
- [ ] **Step 3:** Write `trayectoria.astro`: section head, Timeline, then `.grid-2` Education + Certification cards.
- [ ] **Step 4:** `npm run build` + screenshot `/trayectoria/`. Commit: `feat: trayectoria page with timeline and credentials`.

---

### Task 5: Casos index + two case-study detail pages

**Files:**
- Create: `web/src/components/cases/CaseCard.astro`, `web/src/components/cases/CaseHeader.astro`, `web/src/components/cases/StatRow.astro`
- Create: `web/src/pages/casos/index.astro`, `web/src/pages/casos/heineken-genie.astro`, `web/src/pages/casos/dcsol.astro`
- Modify: `web/src/i18n/es.ts`, `en.ts`

**Interfaces:**
- Produces: `CaseCard{slug,title,summary,tag}`, `CaseHeader{eyebrow,title,lead}`, `StatRow{stats:{v:string,k:string}[]}`. Case content from dictionary `cases.{heineken,dcsol}`.

- [ ] **Step 1:** Add `cases` content to dictionaries — for each: eyebrow, title, lead, problem, approach (bullets), results (stats array). HEINEKEN: Genie Sales Assistant + SAP ECC→Databricks data product, −50% licensing, 300+ reports, 12-person team. D&C: €1.5M / €1.4M direct / €100k avoided / €0 infra, multi-plant supply-contract unification. **Only spec §6 facts.**
- [ ] **Step 2:** Write `CaseCard`, `CaseHeader`, `StatRow` (reuse `.case`/`.case-stat` styles + new card styles).
- [ ] **Step 3:** Write `casos/index.astro` (two CaseCards), `heineken-genie.astro` and `dcsol.astro` (CaseHeader + problem/approach/results sections using StatRow).
- [ ] **Step 4:** `npm run build` + screenshots of index + both case pages. Verify internal links. Commit: `feat: case studies index and detail pages`.

---

### Task 6: Contacto page

**Files:**
- Create: `web/src/pages/contacto.astro`
- Modify: `web/src/i18n/es.ts`, `en.ts`

- [ ] **Step 1:** Add contact strings (heading, lead, emails, LinkedIn) to dictionaries.
- [ ] **Step 2:** Write `contacto.astro` (copy `.contact`/`.contact-links` styles): primary email `rbenavides@dcsol.com.mx`, secondary `rrbenavi@gmail.com`, LinkedIn `in/rrbenavi`.
- [ ] **Step 3:** `npm run build` + screenshot `/contacto/`. Commit: `feat: contact page`.

---

### Task 7: English mirror — all pages under `/en/`

**Files:**
- Create: `web/src/pages/en/index.astro`, `web/src/pages/en/trayectoria.astro`, `web/src/pages/en/contacto.astro`, `web/src/pages/en/casos/index.astro`, `web/src/pages/en/casos/heineken-genie.astro`, `web/src/pages/en/casos/dcsol.astro`
- Modify: `web/src/i18n/en.ts` (complete all English copy)

**Interfaces:**
- Consumes: every component from Tasks 2–6 (all are `{lang}`-driven). EN pages = same templates, `lang="en"`.

- [ ] **Step 1:** Complete `en.ts` with full English translations of every key used so far (meta, nav, hero, metrics labels, expertise, experience, cases, education/cert, contact, footer). Keep proper nouns/cert name unchanged.
- [ ] **Step 2:** Create the six `/en/` page files, each importing the same sections as its ES twin but passing `lang="en"` and `path` set to the `/en/...` route.
- [ ] **Step 3:** `npm run build`; verify each ES route has an EN counterpart and LangToggle round-trips on every page. Screenshot `/en/` and `/en/casos/heineken-genie/`.
- [ ] **Step 4:** Commit: `feat: complete english locale for all pages`.

---

### Task 8: Premium polish + accessibility + responsive pass

**Files:**
- Modify: `web/src/styles/motion.css`, `global.css`, component styles as needed
- Modify: `web/src/scripts/motion.ts`

- [ ] **Step 1:** Add refined premium layer: staggered reveals, subtle card 3D tilt on hover (transform only, disabled under reduced-motion), directional glow/grain, magnetic primary button (optional, reduced-motion safe). Keep within token system.
- [ ] **Step 2:** A11y pass: landmarks (`header/main/footer/nav[aria-label]`), heading order, focus-visible states on all interactive elements, color-contrast check, `aria` on LangToggle. Test full keyboard nav.
- [ ] **Step 3:** Responsive pass: screenshot 320/768/1024/1920 on home + a case page (ES+EN); fix any overflow/spacing.
- [ ] **Step 4:** `npm run build`; run Lighthouse (or equivalent) on home + a case page; confirm Perf ≥95, A11y ≥95. Record results in commit body. Commit: `feat: premium motion, a11y and responsive polish`.

---

### Task 9: Deploy to GitHub Pages

**Files:**
- Create: `.github/workflows/deploy.yml` (repo root)
- Modify: `web/astro.config.mjs` (`site`/`base` resolved to real Pages URL)
- Create/Modify: `README.md` (deploy notes)

**Interfaces:**
- Consumes: built `web/dist`. Produces: live Pages site.

- [ ] **Step 1:** Confirm GitHub username + repo name with user; determine project-page base (`/<repo>/`) vs custom domain. Set `site`/`base` in `astro.config.mjs` accordingly.
- [ ] **Step 2:** Write `.github/workflows/deploy.yml` using `withastro/action` (or `actions/setup-node` + build) with `working-directory: web`, then `actions/upload-pages-artifact` (`web/dist`) + `actions/deploy-pages`. Trigger on push to `main`.
- [ ] **Step 3:** User creates the GitHub repo and authenticates (`gh auth login` / login when prompted — assistant never enters credentials). Push `main`.
- [ ] **Step 4:** In repo Settings → Pages, set source = GitHub Actions. Verify the Action run succeeds and the live URL renders ES + EN. Update `README.md`. Commit: `ci: github pages deploy via actions`.

---

## Self-Review

**Spec coverage:** §2 visual → Tasks 1,3,8. §3 IA (6 ES + 6 EN routes) → Tasks 3–7. §4 tech/i18n → Tasks 1,2,7. §5 component contracts → Tasks 2–6. §6 content (no fabrication) → Tasks 3,4,5,6 dictionaries. §7 deploy → Task 9. §8 testing → per-task build+visual, Task 8 Lighthouse/a11y/responsive. All covered.

**Placeholders:** `site`/`base` intentionally deferred to Task 9 (needs real repo name) — explicitly called out, not a silent TODO. No other placeholders.

**Type consistency:** `{lang, path}` prop shape consistent across BaseLayout/Nav/LangToggle/pages. `metrics`/`groups`/`items`/`cases` dictionary shapes defined in their producing task and consumed unchanged. `initMotion()`/`getAlternatePath()` names stable across tasks.
