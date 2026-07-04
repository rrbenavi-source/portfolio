# Weekly Papper Pipeline — Design Spec

**Fecha:** 2026-07-03
**Autor:** Ricardo Benavides (con Claude)
**Estado:** Aprobado para plan de implementación

## 1. Objetivo

Sistema para producir y publicar **un "papper" semanal** alineado al trabajo actual de Ricardo:
Arquitectura Data & Analytics, Generative BI, soluciones de IA, Databricks y automatizaciones
de datos por IA. El sistema cubre el ciclo completo: **fuentes → ideas → borrador → edición →
humanización → revisión → render bilingüe (PDF + web + LinkedIn)**.

Metas de negocio: reforzar posicionamiento como autoridad en Data Engineering & Analytics,
alimentar el portafolio como hub de contenido, y crecer la red de LinkedIn con cadencia constante.

## 2. Decisiones tomadas (brainstorming)

- **Formato:** rotativo entre **deep-dive técnico (4-8 pág)** y **artículo de opinión/insight (2-3 pág)**; Ricardo elige por semana según el tema.
- **Fuentes:** las 4 categorías — vendors/docs, research/arXiv, newsletters/voces, noticias/industria+LinkedIn.
- **Operación:** **semi-automática agendada** (Enfoque A: cron local `launchd` + Claude Code headless).
- **Destino:** **PDF + LinkedIn + web** (los tres).
- **Idioma:** **bilingüe siempre** (ES + EN) en todo el pipeline.
- **Sección web:** todo en `/publicaciones`, ordenado por fecha (junto a los 2 papers flagship).
- **Gate de revisión:** Ricardo **aprueba siempre** el texto final antes de renderizar/publicar.
- **Agentes:** `papper-editor` (rigor técnico/estructura) + `papper-humanizer` (voz natural, anti-IA).

## 3. No-objetivos (YAGNI)

- **No** publicación automatizada en LinkedIn (no hay API fiable de terceros para documentos). El sistema entrega post + PDF listos; la subida es manual.
- **No** infraestructura en la nube (routines/servicios). Todo corre local, reutilizando el stack existente.
- **No** nueva sección web ni rediseño de `/publicaciones`; se reutiliza el renderer actual.
- **No** base de datos ni CMS; el estado vive en archivos versionados en git.

## 4. Arquitectura

Reutiliza la infraestructura ya probada del proyecto: pipeline HTML→PDF con Chrome headless
(igual que los CV), sitio Astro bilingüe con `ArticleBody.astro`, y contenido en `web/src/i18n/{es,en}.ts`.

### 4.1 Estructura de carpetas

```
pappers/
  sources.yaml              # fuentes curadas por las 4 categorías (editable por Ricardo)
  voice-profile.md          # perfil de voz autoral (derivado de papers previos + portfolio)
  _template/
    papper.html             # plantilla whitepaper (tokens: verde SAP, Fraunces+Inter)
    build_pdf.sh            # render Chrome headless (patrón de CV/build_pdf.sh)
  2026-W28/                 # una carpeta por semana ISO
    digest.md               # 3-5 ideas del barrido del lunes
    draft-es.md
    draft-en.md
    edit-notes.md           # salida del agente editor
    papper-es.pdf
    papper-en.pdf
    linkedin-es.md
    linkedin-en.md
```

### 4.2 Piezas nuevas

| Pieza | Tipo | Rol |
|-------|------|-----|
| `pappers/sources.yaml` | config | Lista curada de fuentes por categoría |
| `pappers/voice-profile.md` | doc | Voz autoral de Ricardo para el humanizador |
| `pappers/_template/` | plantilla | HTML + `build_pdf.sh` del whitepaper |
| `/papper-digest` | comando | Fase 1: barrido de fuentes + digest + borrador semilla |
| `/papper` | comando | Fase 2: build colaborativo (draft→editor→humanizer→render) |
| `papper-editor` | agente | Revisión técnica/editorial |
| `papper-humanizer` | agente | Voz natural + anti-tells de IA |
| launchd `.plist` | scheduler | Dispara `/papper-digest` los lunes |

## 5. Flujo — Fase 1 (Lunes, autónoma)

Trigger: `launchd` los lunes (con `StartCalendarInterval`; si la Mac está apagada, corre al próximo arranque via `RunAtLoad` de respaldo). Ejecuta `claude` headless con el comando `/papper-digest`.

1. **Barrido de fuentes:** por cada categoría de `sources.yaml`, busca lo publicado en los últimos 7 días usando Exa (`web_search_exa`) y WebSearch. Prioriza relevancia al stack (Databricks, SAP, GenBI, IA para datos).
2. **Síntesis:** produce `pappers/2026-Www/digest.md` con **3-5 ideas**, cada una con: título tentativo, ángulo/tesis, formato sugerido (deep-dive u opinión), y 2-4 fuentes citadas (URL + por qué importa).
3. **Borrador semilla:** redacta un primer borrador (`draft-es.md`) de la idea mejor rankeada, para que Ricardo no arranque de cero.
4. **Notificación:** deja el output en el repo; Ricardo lo encuentra el lunes en `pappers/2026-Www/`.

## 6. Flujo — Fase 2 (Colaborativa, `/papper`)

1. **Selección:** Ricardo elige la idea del `digest.md` (o pide otra).
2. **Draft completo:** se expande a borrador completo con estructura del formato elegido y citas.
3. **Agente `papper-editor`:** revisa rigor técnico, exactitud de datos y afirmaciones, estructura del argumento, calidad de citas y ausencia de relleno. Escribe `edit-notes.md` y aplica correcciones al draft.
4. **Agente `papper-humanizer`:** reescribe en la voz de `voice-profile.md` — cadencia natural, primera persona basada en experiencia real (HEINEKEN, SAP–Databricks), elimina *tells* de IA (aperturas genéricas tipo "en el mundo actual", listas mecánicas, adjetivos vacíos, simetría artificial).
5. **Traducción EN:** genera `draft-en.md` como contraparte del ES ya editado/humanizado (misma voz, no traducción literal).
6. **Gate de revisión (Ricardo):** se muestra el texto final ES+EN; **Ricardo aprueba** antes de renderizar.
7. **Render bilingüe:**
   - **PDF:** `build_pdf.sh` renderiza `papper-es.pdf` y `papper-en.pdf` desde la plantilla.
   - **Web:** añade la entrada a `web/src/i18n/es.ts` y `en.ts` (`publicaciones.items[]`), renderizada por el `ArticleBody.astro` existente; ordenada por fecha. Deploy vía push a `main` (auto-CI ya configurado).
   - **LinkedIn:** `linkedin-es.md` y `linkedin-en.md` con hook + cuerpo + CTA al PDF/artículo, listos para copiar y subir manualmente.

## 7. Agentes

### 7.1 `papper-editor`
- **Propósito:** editor técnico exigente. Verifica que cada afirmación técnica sea correcta y esté respaldada; endurece la estructura del argumento; marca datos sin fuente; recorta relleno.
- **Entrada:** `draft-es.md` + fuentes del digest.
- **Salida:** `edit-notes.md` (hallazgos por severidad) + draft corregido.
- **Herramientas:** Read, Edit, Grep, WebSearch/Exa (para verificar afirmaciones).

### 7.2 `papper-humanizer`
- **Propósito:** dar voz humana y autoral; eliminar señales de texto generado por IA.
- **Entrada:** draft post-editor + `voice-profile.md`.
- **Salida:** draft reescrito en la voz de Ricardo.
- **Reglas clave:** primera persona con experiencia concreta; frases de longitud variable; sin clichés ni aperturas genéricas; opiniones con postura; términos técnicos precisos, no decorativos.

### 7.3 `voice-profile.md`
Perfil derivado (con la skill `brand-voice`) de los 2 papers previos (`/publicaciones`) y el copy del portafolio: tono práctico, value-driven, orientado a decisiones y ahorros reales; español profesional latinoamericano; equilibrio entre autoridad técnica y claridad para negocio.

## 8. Fuentes (`sources.yaml`)

```yaml
vendors:
  - Databricks blog
  - Microsoft / Azure data & AI
  - SAP (BW/4HANA, Datasphere, BDC)
  - dbt Labs
research:
  - arXiv cs.DB / cs.AI (text-to-SQL, RAG, GenBI, semantic layers)
newsletters:
  - Data Engineering Weekly
  - Seattle Data Guy
  - Modern Data Stack voices
news:
  - VentureBeat AI
  - anuncios de producto / adquisiciones
  - debates relevantes en LinkedIn
```
Editable por Ricardo. El barrido prioriza los últimos 7 días y la afinidad al stack.

## 9. Restricciones y riesgos

- **LinkedIn manual:** sin API; subida a mano del post + PDF.
- **Mac encendida:** `launchd` requiere el equipo activo el lunes; `RunAtLoad` cubre el arranque tardío.
- **Costos/GateGuard:** los hooks de fact-forcing inyectan avisos por herramienta. Correr las sesiones con `ECC_GATEGUARD=off` o hooks deshabilitados para el job headless. Preferir sesiones frescas para el build web.
- **Calidad de fuentes:** el digest cita URLs; el agente editor verifica afirmaciones antes de publicar.

## 10. Criterios de éxito

- Cada lunes existe un `digest.md` con 3-5 ideas accionables y un borrador semilla.
- Un papper terminado pasa por editor + humanizer y por el gate de aprobación de Ricardo.
- Se generan PDF ES+EN, entrada en `/publicaciones` (ES+EN) y posts LinkedIn ES+EN, consistentes con la identidad visual del proyecto.
