# Notas de edición — 2026-W28 · draft-es.md

_Producidas por el agente `papper-editor` (Fase 2). Resolución anotada por el orquestador._

## CRÍTICO
- **C1 — Fuente Genie fabricada.** Se citaba "Introducing Genie Code" + URL inválida.
  → **RESUELTO:** sustituida por "Introducing Genie One, Genie Ontology, and Genie Agents"
  (`https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents`).
- **C2 — Atribución falsa de la baseline 21-25%.** Se decía "mediciones internas de Snowflake
  y Anthropic" enlazando solo un análisis de terceros (dev.to / Cortex Sense).
  → **RESUELTO:** reencuadrado como "distintas mediciones citadas ubican la línea base…",
  sin atribuir a publicaciones internas; se conserva la fuente real (dev.to).

## IMPORTANTE
- **I1 — 32.7%→64.5% "set completo" no corroborado por el editor.**
  → **MANTENIDO con precisión.** La recuperación primaria (Exa sobre el blog de dbt) cita
  textual "Text-to-SQL accuracy nearly doubled, from 32.7% to 64.5% on the full question set".
  Se explicitan denominadores: 64.5% = set completo; ~100% = dentro del alcance del semantic layer.
- **I2 — Dremio "80%" cambio de denominador.**
  → **MANTENIDO.** La fuente primaria de Dremio dice literal "These errors affect 80% of business
  queries". El draft es fiel; el digest lo parafraseó distinto.
- **I3 — Bloque SAP con cifra de experiencia no verificada.**
  → **PENDIENTE (gate).** El cuerpo visible es cualitativo; Ricardo debe confirmar o añadir
  cifras reales antes de publicar. Se conserva la NOTA.
- **I4 — Fuente del claim zero-copy.**
  → **RESUELTO:** añadido el blog del conector "SAP Business Data Cloud Connect to Databricks".

## MENOR
- **M1** — muletillas de énfasis y triple repetición de "cómo falla > cuánto falla". → recortado.
- **M2** — cadencia "No es X. Es Y." repetida. → variada.
- **M3** — título de sección "Los números que deberían cerrar el debate" sobrepromete. → suavizado.

## Estructura (global)
Tesis clara y sostenida; sin saltos lógicos graves; cierre accionable; extensión de deep-dive
adecuada. Claims de SAP Databricks GA (Delta Sharing zero-copy, Unity Catalog) verificados correctos.
