# Edit notes — W32 (papper-editor, 2026-08-03)

**Conteo: 0 CRÍTICO / 2 IMPORTANTE / 5 MENOR.** Estructura y formato OK
(tesis clara, desarrollo lógico, cierre accionable, ~1,000 palabras ≈ 2–2.5 pág).
Verificación previa de cifras contra el post de dbt (7-abr-2026) hecha por el
controller antes del despacho; autores Ganz & Perigaud confirmados en esa misma
verificación.

## IMPORTANTE (aplicados por el editor)

1. "un detalle que casi nadie comenta" era falso — los modos de falla son de lo
   más comentado del benchmark. Reescrito a "más revelador que la cifra principal".
   La caracterización en sí (text-to-SQL falla plausible y confiado; semantic
   layer rehúsa con error explícito) SÍ está en el benchmark.
2. URL de Solid tenía slug truncado; reemplazada por la canónica:
   `journey.getsolid.ai/p/text2sql-vs-semantic-layer-the-real`.

## MENOR

1. ✅ (editor) "plausible y incorrecto" → "plausible e incorrecto".
2. ✅ (controller) "un debate que duró tres años" → "un debate de años" (la cifra
   no tenía fuente).
3. ⏳ **Decisión de Ricardo:** VBAK/VBAP/KONV son correctas para ECC, pero en
   S/4HANA KONV → PRCD_ELEMENTS. Para "una operación SAP de veinte años" es
   defendible tal cual; precisar solo si el público incluye shops S/4.
4. ✅ (controller) "devuelve" → "suele devolver" (el benchmark describe el modo
   de falla típico, no universal).
5. ✅ Autores confirmados contra el post (Jason Ganz & Benoit Perigaud, dbt Labs).

## Paso de voz (controller, en lugar del agente humanizer no registrado)

- "Preveo una ola" → "Viene una ola" (más natural hablado).
- Revisión contra `voice-profile.md`: sin aperturas genéricas, sin listas
  mecánicas de 3, primera persona donde hay experiencia real, cierre accionable.

## Extensión v2 (feedback de Ricardo: "parece un resumen de 3 pappers anteriores")

Reescritura completa post-editor con investigación adicional. Secciones nuevas:

1. **"Tres años, mismo examen"** — el linaje del benchmark: Sequeda/Allemang/Jacob
   nov-2023 (GPT-4 crudo 16.7% → con knowledge graph 54.2%, 43 preguntas, mismo
   dataset ACME). Verificado contra arXiv 2311.07509.
2. **"El examen de verdad es más duro"** — Spider 2.0 (arXiv 2411.07763, ICLR
   2025): 632 problemas enterprise reales; mejor modelo ~20% al lanzamiento
   (91.2% en Spider clásico); frontera ~70% en la variante 2026 (Spider
   2.0-AIFunc, arXiv 2607.06229). Verificado contra abstracts y review.
3. **"Los vendors ya votaron"** — convergencia: dbt MetricFlow, Snowflake
   Semantic Views, Databricks Metric Views / Business Semantics (GA inicios
   2026) + Genie Ontology (preview, DAIS 2026). Incluye 1 párrafo en primera
   persona de operación Genie (sin cifras de cliente — solo experiencia pública
   del portfolio).
4. **"SAP también votó"** — BDC data products con semántica preservada + sync de
   metadata semántica a Unity Catalog vía Delta Sharing (GA, alianza
   SAP–Databricks), y el giro propio: la semántica que viaja es la del contenido
   estándar; la custom (Z, extractores, user exits) no viene en el paquete.

**Nota de rigor:** el papper-editor revisó la v1. Las secciones nuevas de la v2
fueron verificadas por el controller contra arXiv y blogs de vendor (URLs en
fuentes), pero NO pasaron por el agente editor. Si Ricardo quiere el pase
completo del editor sobre la v2, correrlo antes del render.
