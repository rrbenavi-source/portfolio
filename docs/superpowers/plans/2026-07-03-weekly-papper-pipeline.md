# Weekly Papper Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir un sistema local para producir un "papper" semanal (fuentes → digest → borrador → edición → humanización → revisión → render bilingüe PDF+web+LinkedIn), agendado los lunes 9:30 AM.

**Architecture:** Pipeline de dos fases. Fase 1 (autónoma, launchd → `claude` headless → `/papper-digest`) barre fuentes y deja digest + borrador semilla. Fase 2 (colaborativa, `/papper`) orquesta draft → agente `papper-editor` → agente `papper-humanizer` → contraparte EN → gate de aprobación → render. Reutiliza el patrón Chrome-headless-PDF de `CV/build_pdf.sh` y la integración web de `web/src/i18n/{es,en}.ts` + `ArticleBody.astro`.

**Tech Stack:** Bash + macOS `launchd`, Google Chrome `--headless=new --print-to-pdf`, Astro (Node), Claude Code commands (`.claude/commands/*.md`) y agents (`.claude/agents/*.md`), YAML/Markdown como estado versionado en git.

## Global Constraints

- **Idioma:** bilingüe siempre — cada papper produce ES + EN en PDF, web y LinkedIn.
- **Formato:** rotativo deep-dive técnico (4-8 pág) u opinión/insight (2-3 pág); lo elige Ricardo por semana.
- **Sección web:** todo en `/publicaciones` (`publicaciones.items[]`), ordenado por fecha; NO crear sección nueva.
- **Gate humano:** Ricardo aprueba el texto final ES+EN ANTES de renderizar/publicar. Ningún render ocurre sin su OK.
- **LinkedIn:** entrega de post + PDF para subida manual; NO automatizar la publicación.
- **Tokens visuales (verbatim):** acento verde SAP `#0f7a5a` (claro) / `#2bbd8f` (oscuro); oro `#b9893f`; tipografías `Fraunces` (display serif) + `Inter` (body) vía Google Fonts. A4.
- **Cron:** lunes 9:30 AM (`Weekday=1, Hour=9, Minute=30`) con `RunAtLoad` de respaldo.
- **Costos:** el job headless corre con `ECC_GATEGUARD=off` para evitar los hooks de fact-forcing.
- **Fuentes de contenido web canónicas:** el contenido web vive en `web/src/i18n/es.ts` y `web/src/i18n/en.ts`; nunca hardcodear texto en los `.astro`.
- **Deploy web:** push a `main` (auto-CI ya configurado); no tocar `gh-pages`.

---

### Task 1: Scaffold de `pappers/` — estructura, `.gitignore`, `sources.yaml`, `voice-profile.md`

**Files:**
- Modify: `.gitignore`
- Create: `pappers/sources.yaml`
- Create: `pappers/voice-profile.md`
- Create: `pappers/README.md`

**Interfaces:**
- Produces: `pappers/sources.yaml` (categorías `vendors|research|newsletters|news`, cada una lista de `{name, url, why}`); `pappers/voice-profile.md` (perfil de voz para el agente humanizer); convención de carpeta semanal `pappers/AAAA-Www/`.

- [ ] **Step 1: Excluir los PDFs fuente pesados del root de `pappers/`**

Añadir a `.gitignore` (los PDFs deliverables viven en subcarpetas `pappers/AAAA-Www/` y SÍ se versionan; solo se excluyen los PDFs sueltos en el root):

```gitignore
# PDFs fuente sueltos en la raíz de pappers/ (material de referencia, no deliverables)
pappers/*.pdf
```

- [ ] **Step 2: Crear `pappers/sources.yaml`**

```yaml
# Fuentes curadas para el barrido semanal de ideas. Editable por Ricardo.
# El barrido prioriza publicaciones de los últimos 7 días y la afinidad al stack
# (Databricks, SAP, Generative BI, IA para datos, automatización de datos).

vendors:
  - name: Databricks Blog
    url: https://www.databricks.com/blog
    why: Releases, AI/BI Genie, patrones de data products y lakehouse.
  - name: Microsoft Azure — Data & AI Blog
    url: https://azure.microsoft.com/en-us/blog/
    why: Fabric, Synapse, Copilot para datos; complementa el stack cloud.
  - name: SAP News & Community (BW/4HANA, Datasphere, BDC)
    url: https://news.sap.com/
    why: Núcleo del stack de Ricardo; evolución analítica SAP.
  - name: dbt Labs Blog
    url: https://www.getdbt.com/blog
    why: Semantic layer, transformación y prácticas de modern data stack.

research:
  - name: arXiv cs.DB
    url: https://arxiv.org/list/cs.DB/recent
    why: Text-to-SQL, semantic layers, sistemas analíticos.
  - name: arXiv cs.AI / cs.CL
    url: https://arxiv.org/list/cs.CL/recent
    why: LLMs, RAG y Generative BI aplicados a datos.

newsletters:
  - name: Data Engineering Weekly
    url: https://www.dataengineeringweekly.com/
    why: Pulso semanal de tendencias en data engineering.
  - name: Seattle Data Guy
    url: https://seattledataguy.substack.com/
    why: Perspectiva práctica de arquitectura y carrera en datos.
  - name: Modern Data Stack voices (Benn Stancil / dbt / MDS)
    url: https://benn.substack.com/
    why: Opinión de fondo para artículos de tesis.

news:
  - name: VentureBeat AI
    url: https://venturebeat.com/category/ai/
    why: Anuncios de producto, adquisiciones y debates de IA/datos.
  - name: LinkedIn — debates de líderes Data/Analytics
    url: https://www.linkedin.com/feed/
    why: Temas "de la semana" con gancho de actualidad y red de Ricardo.
```

- [ ] **Step 3: Crear `pappers/voice-profile.md`**

```markdown
# Perfil de voz autoral — Ricardo Benavides

Voz para el agente `papper-humanizer`. Derivada de sus 2 publicaciones previas
(/publicaciones) y del copy del portafolio.

## Quién habla
Líder de Data Engineering SAP y Arquitecto de Datos (HEINEKEN México · D&C Solutions),
+20 años, integración SAP–Databricks. Escribe desde la experiencia real, no desde la teoría.

## Tono
- Práctico y value-driven: conecta cada idea técnica con decisiones y ahorros reales.
- Autoridad tranquila: afirma con postura, sin grandilocuencia ni hype.
- Claridad para negocio + precisión técnica; traduce lo complejo sin diluirlo.
- Español profesional latinoamericano (México). El EN mantiene la misma voz, no es traducción literal.

## Firmas de estilo
- Primera persona cuando hay experiencia concreta ("cuando migramos 300+ reportes…").
- Frases de longitud variable; ritmo natural, no simétrico.
- Analogías concretas ("un producto de datos sin propósito es un GPS sin destino").
- Cierra con una idea accionable, no con un resumen genérico.

## Anti-patrones (tells de IA a eliminar)
- Aperturas tipo "En el mundo actual/digital…", "En la era de…".
- Listas mecánicas de 3 con adjetivos vacíos ("robusto, escalable, eficiente").
- Simetría artificial y conectores de relleno ("Además, cabe destacar que…").
- Afirmaciones sin fuente ni experiencia detrás.
- Conclusiones que solo reformulan la introducción.
```

- [ ] **Step 4: Crear `pappers/README.md`**

```markdown
# Pappers — pipeline semanal

Sistema de producción de un papper semanal. Ver spec:
`docs/superpowers/specs/2026-07-03-weekly-papper-pipeline-design.md`.

## Uso
- **Fase 1 (lunes 9:30, automática):** launchd corre `/papper-digest` → `pappers/AAAA-Www/digest.md` + borrador semilla.
- **Fase 2 (cuando estés listo):** corre `/papper` → elige idea → editor → humanizer → EN → apruebas → render PDF+web+LinkedIn.

## Estructura semanal
`pappers/AAAA-Www/`: `digest.md`, `draft-es.md`, `draft-en.md`, `edit-notes.md`,
`papper-es.pdf`, `papper-en.pdf`, `linkedin-es.md`, `linkedin-en.md`.

## Config
- `sources.yaml` — fuentes por categoría (edítalo cuando quieras).
- `voice-profile.md` — tu voz autoral para el humanizer.
```

- [ ] **Step 5: Verificar y commit**

Run: `cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB" && python3 -c "import yaml,sys; yaml.safe_load(open('pappers/sources.yaml')); print('yaml OK')" && git check-ignore pappers/1763569092495.pdf`
Expected: imprime `yaml OK` y `pappers/1763569092495.pdf` (confirmando que el PDF pesado queda ignorado). Si `yaml` no está instalado, validar con `python3 -c "import pappers" ` NO aplica; usar en su lugar `ruby -ryaml -e "YAML.load_file('pappers/sources.yaml'); puts 'yaml OK'"` o revisar a ojo la indentación.

```bash
git add .gitignore pappers/sources.yaml pappers/voice-profile.md pappers/README.md
git commit -m "feat(pappers): scaffold — sources, voice profile, gitignore, readme"
```

---

### Task 2: Plantilla PDF whitepaper + `build_pdf.sh`

**Files:**
- Create: `pappers/_template/papper.html`
- Create: `pappers/_template/build_pdf.sh`
- Create (fixture temporal): `pappers/2026-W99/draft-es.md`, `pappers/2026-W99/draft-en.md`

**Interfaces:**
- Consumes: convención `pappers/AAAA-Www/draft-{es,en}.md` (markdown del papper con front-matter `title`, `subtitle`, `format`, `date`).
- Produces: `pappers/_template/build_pdf.sh <week_dir>` → renderiza `<week_dir>/papper-es.pdf` y `<week_dir>/papper-en.pdf`. Reutiliza el patrón `data-theme` sed-swap de `CV/build_pdf.sh`.

- [ ] **Step 1: Crear la plantilla `pappers/_template/papper.html`**

Plantilla autocontenida con tokens verbatim. Usa marcadores `{{TITLE}}`, `{{SUBTITLE}}`, `{{META}}`, `{{BODY_HTML}}`, `{{SOURCES_HTML}}` que `build_pdf.sh` sustituye. `data-theme="light"` por defecto (swappeable a `dark`).

```html
<!doctype html>
<html lang="es" data-theme="light">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
<style>
  :root {
    --accent: #0f7a5a; --gold: #b9893f;
    --bg: #ffffff; --surface: #f6f5f2; --text: #1a1a1a; --dim: #5b5b57; --line: #e3e1dc;
  }
  [data-theme="dark"] {
    --accent: #2bbd8f; --gold: #cda25a;
    --bg: #14161a; --surface: #1c1f25; --text: #eceae4; --dim: #a2a6ad; --line: #2c3038;
  }
  * { box-sizing: border-box; }
  @page { size: A4; margin: 18mm 16mm; }
  body { font-family: Inter, system-ui, sans-serif; color: var(--text); background: var(--bg);
         margin: 0; font-size: 10.5pt; line-height: 1.55; }
  .eyebrow { color: var(--accent); font-weight: 600; letter-spacing: .08em;
             text-transform: uppercase; font-size: 8.5pt; }
  h1 { font-family: Fraunces, Georgia, serif; font-weight: 600; font-size: 26pt;
       line-height: 1.1; margin: .3rem 0 .2rem; }
  .subtitle { color: var(--dim); font-size: 12pt; margin: 0 0 .2rem; }
  .meta { color: var(--dim); font-size: 8.5pt; border-top: 1px solid var(--line);
          padding-top: .5rem; margin-top: .6rem; }
  h2 { font-family: Fraunces, Georgia, serif; font-weight: 600; font-size: 15pt;
       margin: 1.4rem 0 .4rem; break-after: avoid; }
  p { margin: 0 0 .7rem; }
  blockquote { border-left: 3px solid var(--accent); margin: 1rem 0; padding: .2rem 0 .2rem 1rem;
               font-family: Fraunces, Georgia, serif; font-size: 13pt; color: var(--text); }
  ul, ol { margin: 0 0 .8rem 1.1rem; } li { margin: 0 0 .3rem; }
  strong { color: var(--accent); }
  .sources { margin-top: 1.6rem; border-top: 1px solid var(--line); padding-top: .8rem; }
  .sources h2 { font-size: 11pt; } .sources li { font-size: 8.5pt; color: var(--dim); }
  .sources a { color: var(--accent); text-decoration: none; word-break: break-all; }
</style>
</head>
<body>
  <header>
    <p class="eyebrow">{{EYEBROW}}</p>
    <h1>{{TITLE}}</h1>
    <p class="subtitle">{{SUBTITLE}}</p>
    <p class="meta">{{META}}</p>
  </header>
  <main>
    {{BODY_HTML}}
    <section class="sources">
      <h2>Fuentes</h2>
      <ul>{{SOURCES_HTML}}</ul>
    </section>
  </main>
</body>
</html>
```

- [ ] **Step 2: Crear `pappers/_template/build_pdf.sh`**

Convierte `draft-{es,en}.md` a PDF vía pandoc si está disponible, o (fallback) inyecta el markdown pre-convertido. Para mantener cero dependencias nuevas como el resto del proyecto, el script asume que `/papper` ya escribió el HTML del cuerpo en `<week_dir>/body-{es,en}.html` y las fuentes en `<week_dir>/sources-{es,en}.html`. Renderiza ambos idiomas.

```bash
#!/usr/bin/env bash
# Renderiza los pappers a PDF vía Chrome headless. Uso: bash build_pdf.sh <week_dir>
# Espera en <week_dir>: meta-es.txt / meta-en.txt (líneas: eyebrow|title|subtitle|meta)
# y body-es.html / body-en.html y sources-es.html / sources-en.html
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WEEK="${1:?Uso: build_pdf.sh <week_dir>}"
WEEK="$(cd "$WEEK" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
[ -x "$CHROME" ] || { echo "✗ Chrome no encontrado: $CHROME" >&2; exit 1; }

render() { # <lang> <theme> <out>
  local lang="$1" theme="$2" out="$3"
  local meta body sources html
  IFS='|' read -r eyebrow title subtitle metaline < "$WEEK/meta-$lang.txt"
  body="$(cat "$WEEK/body-$lang.html")"
  sources="$(cat "$WEEK/sources-$lang.html")"
  html="$TMP/papper-$lang-$theme.html"
  sed -e "s/data-theme=\"light\"/data-theme=\"$theme\"/" \
      -e "s|{{EYEBROW}}|$eyebrow|" -e "s|{{TITLE}}|$title|" \
      -e "s|{{SUBTITLE}}|$subtitle|" -e "s|{{META}}|$metaline|" \
      "$DIR/papper.html" > "$html.stage"
  # inyectar bloques HTML multilínea con awk (evita problemas de sed con saltos)
  awk -v b="$body" '{gsub(/\{\{BODY_HTML\}\}/,b)}1' "$html.stage" > "$html.stage2"
  awk -v s="$sources" '{gsub(/\{\{SOURCES_HTML\}\}/,s)}1' "$html.stage2" > "$html"
  echo "→ $out (tema: $theme)"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$WEEK/$out" "file://$html" 2>/dev/null
  echo "  ✓ $(du -h "$WEEK/$out" | cut -f1)"
}

render es light "papper-es.pdf"
render en light "papper-en.pdf"
echo "Listo. PDFs en: $WEEK"
```

- [ ] **Step 3: Crear un fixture mínimo para probar el render**

Crear `pappers/2026-W99/meta-es.txt`:
```text
Papper · Insight|Prueba de render|Subtítulo de prueba|Ricardo Benavides · 2026 · borrador de prueba
```
Crear `pappers/2026-W99/body-es.html`:
```html
<h2>Sección de prueba</h2><p>Este es un <strong>párrafo</strong> de prueba para validar el render.</p><blockquote>Una cita de ejemplo.</blockquote>
```
Crear `pappers/2026-W99/sources-es.html`:
```html
<li><a href="https://example.com">Fuente de ejemplo</a> — por qué importa.</li>
```
Duplicar los tres como `meta-en.txt`, `body-en.html`, `sources-en.html` (mismo contenido, EN).

- [ ] **Step 4: Ejecutar el render y verificar**

Run: `cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB" && bash pappers/_template/build_pdf.sh pappers/2026-W99 && ls -la pappers/2026-W99/*.pdf`
Expected: se generan `papper-es.pdf` y `papper-en.pdf` (>10 KB cada uno). Abrir `papper-es.pdf` y confirmar tipografías Fraunces/Inter y acento verde.

- [ ] **Step 5: Limpiar fixture y commit**

```bash
cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB"
rm -rf pappers/2026-W99
chmod +x pappers/_template/build_pdf.sh
git add pappers/_template/papper.html pappers/_template/build_pdf.sh
git commit -m "feat(pappers): plantilla whitepaper PDF + build_pdf.sh (Chrome headless)"
```

---

### Task 3: Agente `papper-editor`

**Files:**
- Create: `.claude/agents/papper-editor.md`

**Interfaces:**
- Consumes: `pappers/AAAA-Www/draft-es.md` + fuentes del `digest.md`.
- Produces: `pappers/AAAA-Www/edit-notes.md` (hallazgos por severidad) y aplica correcciones al `draft-es.md`.

- [ ] **Step 1: Crear el agente**

```markdown
---
name: papper-editor
description: Editor técnico exigente para los pappers. Verifica rigor técnico, exactitud de datos, estructura del argumento y calidad de citas; recorta relleno. Usar en la Fase 2 tras el draft completo.
tools: Read, Edit, Grep, Glob, WebSearch
---

Eres un editor técnico exigente para artículos de Data & Analytics, Generative BI,
Databricks e IA para datos. Recibes un borrador (`draft-es.md`) y sus fuentes.

## Tu trabajo
1. **Exactitud técnica:** verifica cada afirmación técnica. Si algo es dudoso o
   desactualizado, márcalo; usa WebSearch para confirmar hechos clave (versiones,
   nombres de producto, capacidades).
2. **Citas:** toda afirmación de datos/estadística debe tener fuente. Marca las que no.
3. **Estructura del argumento:** tesis clara al inicio, desarrollo lógico, cierre accionable.
   Señala saltos lógicos o secciones que no aportan.
4. **Relleno:** recorta párrafos genéricos, redundancias y adjetivos vacíos.
5. **Formato correcto:** confirma que respeta el formato elegido (deep-dive 4-8 pág u opinión 2-3 pág).

## Salida
- Escribe `edit-notes.md` en la misma carpeta con hallazgos clasificados:
  `CRÍTICO` (error factual / afirmación sin sustento), `IMPORTANTE` (estructura/argumento),
  `MENOR` (estilo/claridad). Cada hallazgo con ubicación y corrección sugerida.
- Aplica directamente al `draft-es.md` las correcciones CRÍTICAS e IMPORTANTES que sean
  inequívocas. Deja las que requieran criterio de Ricardo anotadas en `edit-notes.md`.
- NO reescribas la voz ni el estilo — eso es trabajo del `papper-humanizer`. Enfócate en
  corrección y estructura.
```

- [ ] **Step 2: Verificar (dry run)**

Crear un borrador de prueba `pappers/2026-W99/draft-es.md` con una afirmación falsa deliberada (p.ej. "Databricks fue fundada en 2020") y una estadística sin fuente. Dispatch al agente `papper-editor` sobre esa carpeta.
Expected: `edit-notes.md` marca la fecha como `CRÍTICO` y la estadística sin fuente. Borrar `pappers/2026-W99` tras verificar.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/papper-editor.md
git commit -m "feat(pappers): agente papper-editor (rigor técnico y estructura)"
```

---

### Task 4: Agente `papper-humanizer`

**Files:**
- Create: `.claude/agents/papper-humanizer.md`

**Interfaces:**
- Consumes: `draft-es.md` (post-editor) + `pappers/voice-profile.md`.
- Produces: `draft-es.md` reescrito en la voz de Ricardo (in-place).

- [ ] **Step 1: Crear el agente**

```markdown
---
name: papper-humanizer
description: Reescribe el papper en la voz autoral de Ricardo y elimina señales de texto generado por IA. Usar en la Fase 2 tras el papper-editor, antes del gate de aprobación.
tools: Read, Edit
---

Reescribes el borrador para que suene a Ricardo Benavides, no a una IA.

## Antes de empezar
Lee SIEMPRE `pappers/voice-profile.md` y aplica su tono, firmas de estilo y anti-patrones.

## Reglas
1. **Voz:** primera persona cuando hay experiencia real (SAP–Databricks, HEINEKEN, migraciones,
   liderazgo de ~15 personas). Autoridad tranquila, value-driven.
2. **Ritmo:** frases de longitud variable. Rompe la simetría. Nada de listas mecánicas de 3.
3. **Elimina tells de IA:** aperturas "En el mundo actual…", conectores de relleno, adjetivos
   vacíos ("robusto, escalable"), conclusiones que reformulan la intro.
4. **Concreción:** cambia lo abstracto por ejemplos concretos y analogías del oficio.
5. **Cierre accionable:** termina con una idea que el lector pueda aplicar, no un resumen.
6. **Preserva los hechos y las citas** que dejó el editor. No inventes datos nuevos.

## Salida
Reescribe `draft-es.md` in-place. No toques `edit-notes.md`. No cambies afirmaciones técnicas
ni fuentes; solo voz, ritmo y naturalidad.
```

- [ ] **Step 2: Verificar (dry run)**

Crear `pappers/2026-W99/draft-es.md` con un párrafo lleno de tells de IA ("En el mundo digital actual, las soluciones robustas, escalables y eficientes…"). Dispatch al `papper-humanizer`.
Expected: el párrafo queda reescrito sin la apertura genérica ni la lista de adjetivos, en primera persona con concreción. Borrar `pappers/2026-W99` tras verificar.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/papper-humanizer.md
git commit -m "feat(pappers): agente papper-humanizer (voz natural, anti-IA)"
```

---

### Task 5: Comando `/papper-digest` (Fase 1 — barrido + digest + semilla)

**Files:**
- Create: `.claude/commands/papper-digest.md`

**Interfaces:**
- Consumes: `pappers/sources.yaml`.
- Produces: `pappers/AAAA-Www/digest.md` (3-5 ideas) + `pappers/AAAA-Www/draft-es.md` (borrador semilla de la idea top).

- [ ] **Step 1: Crear el comando**

```markdown
---
description: Fase 1 del pipeline de pappers — barre las fuentes de la última semana y deja un digest de 3-5 ideas + un borrador semilla.
---

Ejecuta el barrido semanal de ideas para el papper.

## Pasos
1. Calcula la semana ISO actual (formato `AAAA-Www`, p.ej. `2026-W28`) y crea la carpeta
   `pappers/AAAA-Www/` si no existe.
2. Lee `pappers/sources.yaml`. Para cada categoría (`vendors`, `research`, `newsletters`, `news`),
   busca lo publicado en los **últimos 7 días** usando WebSearch (y Exa `web_search_exa` si está
   disponible). Prioriza relevancia al stack: Databricks, SAP (BW/4HANA, Datasphere, BDC),
   Generative BI, IA para datos, automatización de datos.
3. Sintetiza **3-5 ideas** de papper. Para cada una: título tentativo, tesis/ángulo, formato
   sugerido (`deep-dive` u `opinión`), y 2-4 fuentes (URL + por qué importa).
4. Escribe `pappers/AAAA-Www/digest.md` con este esquema:

   ```markdown
   # Digest AAAA-Www

   ## Idea 1 — <título>
   - **Formato:** deep-dive | opinión
   - **Tesis:** <una frase>
   - **Por qué ahora:** <gancho de actualidad>
   - **Fuentes:**
     - <URL> — <por qué importa>
   ...
   ```
5. Redacta un **borrador semilla** de la idea mejor rankeada en `pappers/AAAA-Www/draft-es.md`
   con front-matter:

   ```markdown
   ---
   title: <título>
   subtitle: <subtítulo>
   format: deep-dive | opinión
   date: AAAA-MM-DD
   ---
   ```
   Seguido de un primer desarrollo (no final) con las fuentes citadas. Es una semilla para que
   Ricardo no arranque de cero, NO el papper terminado.
6. Termina imprimiendo un resumen de las ideas y la ruta del digest.

## Notas
- Este comando NO renderiza PDF ni publica; solo investiga y siembra.
- Si una fuente no es accesible, anótalo en el digest y continúa (no falles el barrido completo).
```

- [ ] **Step 2: Verificar**

Run (en sesión interactiva): invocar `/papper-digest`.
Expected: se crea `pappers/<semana-actual>/digest.md` con 3-5 ideas bien formadas y `draft-es.md` con front-matter y un desarrollo inicial. Revisar que las fuentes citadas sean reales y recientes.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/papper-digest.md
git commit -m "feat(pappers): comando /papper-digest (Fase 1 — barrido + digest + semilla)"
```

---

### Task 6: Comando `/papper` (Fase 2 — draft → editor → humanizer → EN → gate → render)

**Files:**
- Create: `.claude/commands/papper.md`

**Interfaces:**
- Consumes: `pappers/AAAA-Www/digest.md` + `draft-es.md`; agentes `papper-editor`, `papper-humanizer`; `pappers/_template/build_pdf.sh`.
- Produces: `draft-en.md`, `body-{es,en}.html`, `sources-{es,en}.html`, `meta-{es,en}.txt`, `papper-{es,en}.pdf`, `linkedin-{es,en}.md`, y la integración web (Task 7 la define en detalle).

- [ ] **Step 1: Crear el comando**

```markdown
---
description: Fase 2 del pipeline de pappers — construye el papper elegido (editor + humanizer + EN), pide aprobación y renderiza PDF + web + LinkedIn.
argument-hint: "[semana AAAA-Www, opcional; por defecto la más reciente]"
---

Construye el papper de la semana. Argumento opcional: la carpeta de semana; si se omite, usa
la más reciente en `pappers/`.

## Flujo
1. **Selección:** muestra las ideas de `digest.md`. Pregunta a Ricardo cuál desarrollar
   (o si ya editó `draft-es.md`, confírmalo).
2. **Draft completo:** expande `draft-es.md` al formato elegido (deep-dive 4-8 pág u opinión
   2-3 pág), con estructura clara y citas a las fuentes del digest.
3. **Editor:** dispatch al agente `papper-editor` sobre la carpeta. Espera `edit-notes.md`.
   Resume a Ricardo los hallazgos CRÍTICOS/IMPORTANTES.
4. **Humanizer:** dispatch al agente `papper-humanizer`. Reescribe `draft-es.md` en su voz.
5. **Contraparte EN:** genera `draft-en.md` con la misma voz (no traducción literal), preservando
   hechos y fuentes.
6. **GATE DE APROBACIÓN (obligatorio):** presenta a Ricardo el texto final ES + EN. NO continúes
   sin su "OK". Si pide cambios, edítalos y vuelve a presentar.
7. **Preparar artefactos de render** (tras el OK):
   - Convierte el cuerpo de cada idioma a HTML de bloques (`<h2>`, `<p>`, `<blockquote>`,
     `<ul>/<ol>`, `<strong>`) y escríbelo en `body-es.html` / `body-en.html`.
   - Escribe las fuentes como `<li>` en `sources-es.html` / `sources-en.html`.
   - Escribe `meta-es.txt` / `meta-en.txt` con una línea `eyebrow|title|subtitle|meta`
     (meta = "Ricardo Benavides · <mes año> · <formato>").
8. **Render PDF:** ejecuta `bash pappers/_template/build_pdf.sh pappers/AAAA-Www`.
   Verifica que se crearon `papper-es.pdf` y `papper-en.pdf`.
9. **LinkedIn:** escribe `linkedin-es.md` y `linkedin-en.md`, cada uno con: hook (1-2 líneas),
   cuerpo (150-220 palabras adaptado a LinkedIn, no el papper completo), y CTA al PDF/artículo.
   Indica a Ricardo que la subida es manual.
10. **Web:** integra el papper en `/publicaciones` siguiendo el procedimiento de la Task 7 del plan
    (añadir item a `web/src/i18n/es.ts` y `en.ts`), corre `cd web && npm run build` para validar,
    y recuérdale a Ricardo hacer `git push origin main` para desplegar.
11. **Cierre:** resume qué se generó y las rutas.

## Reglas
- NUNCA renderices ni publiques antes del gate de aprobación del paso 6.
- Preserva los tokens visuales y el patrón de la plantilla; no inventes estilos nuevos.
```

- [ ] **Step 2: Verificar (dry run hasta el gate)**

Con una carpeta de semana que tenga `digest.md` + `draft-es.md`, invocar `/papper`. Confirmar que:
Expected: pide selección de idea, corre editor y humanizer (se crean `edit-notes.md` y se reescribe `draft-es.md`), genera `draft-en.md`, y **se detiene en el gate de aprobación** sin renderizar.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/papper.md
git commit -m "feat(pappers): comando /papper (Fase 2 — build, gate de aprobación, render)"
```

---

### Task 7: Integración web en `/publicaciones` (procedimiento + validación)

**Files:**
- Modify: `web/src/i18n/es.ts` (`publicaciones.items[]`)
- Modify: `web/src/i18n/en.ts` (`publicaciones.items[]`)
- Create: `pappers/_template/web-item-example.md` (guía de referencia para `/papper`)

**Interfaces:**
- Consumes: papper aprobado (ES + EN) y sus fuentes.
- Produces: un nuevo objeto en `publicaciones.items[]` en ambos idiomas; la ruta `/publicaciones/<slug>` (+ `/en/`) se genera sola vía el `getStaticPaths` existente.

- [ ] **Step 1: Documentar el shape del item como referencia**

Crear `pappers/_template/web-item-example.md` (lo consulta `/papper` al integrar; el `body` usa los
bloques que ya soporta `ArticleBody.astro`: `prose`, `quote`, `list`, `steps`, `domains`):

```markdown
# Item de publicación (referencia para /papper)

Añadir al inicio del array `publicaciones.items` en `web/src/i18n/es.ts` (y su gemelo en `en.ts`),
para que el más reciente aparezca primero. `idx` = número correlativo con cero a la izquierda.

```ts
{
  idx: '03',                         // siguiente correlativo
  slug: 'kebab-del-titulo',          // único; genera /publicaciones/<slug>
  subtitle: 'Etiqueta corta',        // aparece como "Publicación · <subtitle>"
  title: 'Título del papper',
  role: 'Autor: Ricardo Benavides',  // sin editora salvo colaboración
  meta: '2026',
  lead: 'Frase gancho.',
  summary: 'Resumen 1-2 frases (usado en card y <meta description>).',
  tags: ['Databricks', 'Generative BI'],
  body: [
    { type: 'prose', heading: 'Sección', body: ['Párrafo con <strong>énfasis</strong>.'] },
    { type: 'quote', text: 'Una cita.' },
    { type: 'list', heading: 'Puntos', items: ['Uno', 'Dos'] },
  ],
},
```

En `en.ts` usar el MISMO `slug` y `idx`, con el contenido en inglés.
```

- [ ] **Step 2: Integrar un papper de prueba en ambos idiomas**

Añadir manualmente un item de prueba (slug `papper-smoke-test`) al inicio de `publicaciones.items`
en `web/src/i18n/es.ts` y `web/src/i18n/en.ts`, siguiendo el shape anterior con 2 bloques `prose`.

- [ ] **Step 3: Validar el build de Astro**

Run: `cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB/web" && npm run build`
Expected: build exitoso; en la salida aparecen las rutas `/publicaciones/papper-smoke-test` y
`/en/publicaciones/papper-smoke-test`.

- [ ] **Step 4: Revertir el item de prueba y commit de la guía**

```bash
cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB"
git checkout web/src/i18n/es.ts web/src/i18n/en.ts   # quita el item de prueba
git add pappers/_template/web-item-example.md
git commit -m "docs(pappers): guía de integración web en /publicaciones"
```

---

### Task 8: Scheduler `launchd` (lunes 9:30 AM)

**Files:**
- Create: `pappers/_template/run-digest.sh`
- Create: `pappers/_template/com.ricardo.papper-digest.plist`
- Modify: `.claude/settings.local.json` (allowlist de herramientas para el job headless)

**Interfaces:**
- Consumes: el comando `/papper-digest`.
- Produces: un job `launchd` que corre `run-digest.sh` los lunes 9:30 AM; log en `pappers/_template/digest.log`.

- [ ] **Step 1: Crear el wrapper `pappers/_template/run-digest.sh`**

```bash
#!/usr/bin/env bash
# Ejecuta el barrido semanal de pappers en modo headless. Lo dispara launchd los lunes 9:30.
set -euo pipefail
PROJECT="/Users/ricardobenavides/Documents/ Claude Files/CV RB"
LOG="$PROJECT/pappers/_template/digest.log"
cd "$PROJECT"
{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') — inicio /papper-digest ====="
  ECC_GATEGUARD=off claude -p "/papper-digest" --permission-mode acceptEdits
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') — fin ====="
} >> "$LOG" 2>&1
```

Nota: `claude` debe estar en el PATH del entorno de launchd; si no, sustituir por la ruta absoluta
(`which claude` para obtenerla) en la línea de ejecución.

- [ ] **Step 2: Crear el plist `pappers/_template/com.ricardo.papper-digest.plist`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.ricardo.papper-digest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/ricardobenavides/Documents/ Claude Files/CV RB/pappers/_template/run-digest.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>1</integer>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>30</integer>
  </dict>
  <key>StandardOutPath</key><string>/Users/ricardobenavides/Documents/ Claude Files/CV RB/pappers/_template/launchd.out.log</string>
  <key>StandardErrorPath</key><string>/Users/ricardobenavides/Documents/ Claude Files/CV RB/pappers/_template/launchd.err.log</string>
</dict>
</plist>
```

Nota sobre `RunAtLoad`: NO se activa por defecto para no disparar un barrido en cada login. Si
Ricardo prefiere que un lunes perdido se recupere al encender, añadir `<key>RunAtLoad</key><true/>`
— pero entonces conviene que `/papper-digest` sea idempotente por semana (ya crea la carpeta
`AAAA-Www` si no existe y puede sobreescribir el digest de la semana en curso).

- [ ] **Step 3: Allowlist de herramientas para el job headless**

En `.claude/settings.local.json`, asegurar permisos para que el job no se bloquee. Leer el archivo
actual y añadir (fusionando con lo existente) un bloque `permissions.allow` con las herramientas del
barrido:

```json
{
  "permissions": {
    "allow": ["WebSearch", "Bash(git add:*)", "Bash(git commit:*)", "Write", "Edit", "Read"]
  }
}
```

(Ajustar el merge para no pisar claves existentes del archivo.)

- [ ] **Step 4: Instalar y probar el job manualmente**

```bash
cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB"
chmod +x pappers/_template/run-digest.sh
cp pappers/_template/com.ricardo.papper-digest.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.ricardo.papper-digest.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.ricardo.papper-digest.plist
launchctl list | grep papper-digest
```
Expected: `launchctl list` muestra `com.ricardo.papper-digest`. Luego probar la ejecución:
`launchctl start com.ricardo.papper-digest` y revisar `pappers/_template/digest.log` — debe registrar
inicio/fin y haberse creado la carpeta de la semana con `digest.md`.

- [ ] **Step 5: Añadir logs al gitignore y commit**

```bash
cd "/Users/ricardobenavides/Documents/ Claude Files/CV RB"
printf '\n# logs del scheduler de pappers\npappers/_template/*.log\n' >> .gitignore
git add .gitignore pappers/_template/run-digest.sh pappers/_template/com.ricardo.papper-digest.plist .claude/settings.local.json
git commit -m "feat(pappers): scheduler launchd (lunes 9:30) + wrapper headless + allowlist"
```

---

## Notas de ejecución transversales

- **Orden recomendado:** Task 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Las tasks 3 y 4 (agentes) son
  independientes entre sí; 6 depende de 2,3,4,5; 8 depende de 5.
- **Costos:** ejecutar las sesiones de build con `ECC_GATEGUARD=off` para evitar los hooks de
  fact-forcing (ver spec §9).
- **Deploy web:** cada papper publicado en web requiere `git push origin main` (auto-CI). No tocar
  `gh-pages`.

## Self-Review (cobertura del spec)

- Fuentes (spec §8) → Task 1 (`sources.yaml`). ✅
- Fase 1 autónoma (§5) → Task 5 (`/papper-digest`) + Task 8 (launchd lunes 9:30). ✅
- Fase 2 colaborativa (§6) → Task 6 (`/papper`), con editor (Task 3) y humanizer (Task 4). ✅
- Gate de aprobación (§2, §6.6) → Task 6 paso 6, regla explícita. ✅
- Render bilingüe PDF (§6.7) → Task 2 (plantilla + build_pdf.sh) + Task 6. ✅
- Web en /publicaciones bilingüe (§4, §6) → Task 7. ✅
- LinkedIn manual (§6, §9) → Task 6 paso 9. ✅
- Voz autoral (§7.3) → Task 1 (`voice-profile.md`) + Task 4. ✅
- Restricciones costos/Mac/LinkedIn (§9) → notas transversales + Task 8. ✅
```
