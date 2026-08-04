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

---

# Edit notes — W32 segunda pasada (papper-editor sobre v2, 2026-08-03)

**Conteo: 0 CRÍTICO / 3 IMPORTANTE (aplicados) / 4 MENOR (2 aplicados en
fuentes, 2 a criterio de Ricardo).** Verificación con WebSearch de las cuatro
secciones nuevas.

## Verificado como correcto (sin cambios)

- **Sequeda/Allemang/Jacob (arXiv 2311.07509, nov-2023):** GPT-4 zero-shot
  16.7% vs 54.2% con knowledge graph, esquema enterprise de seguros, 43
  preguntas. Confirmado contra el abstract del paper.
- **Relación entre benchmarks:** el benchmark 2026 de dbt corre sobre el ACME
  Insurance dataset con 11 preguntas × 20 corridas por configuración
  (confirmado contra el post de dbt y el repo dbt-labs/dbt-llm-sl-bench).
  Cifras 2026 confirmadas: crudo 84.1% (GPT-5.3-Codex) y 90.0% (Claude Sonnet
  4.6) → semantic layer 100% y 98.2%.
- **Spider 2.0 (arXiv 2411.07763, ICLR 2025 Oral):** 632 problemas enterprise
  reales, bases con 1,000+ columnas, BigQuery/Snowflake. Al lanzamiento, el
  agente basado en o1-preview resolvió 21.3% ("alrededor del 20%" en el draft,
  OK) vs 91.2% del mismo modelo en Spider 1.0. Confirmado.
- **Genie Ontology:** en preview desde DAIS 2026 (jun-2026). Confirmado.
- **SAP BDC → Unity Catalog:** sync de metadata semántica (display names,
  descripciones, relaciones PK/FK, tags de gobernanza) vía Delta Sharing en GA
  desde el 30-abr-2026. Confirmado contra el blog de Databricks y docs.

## IMPORTANTE (aplicados por el editor)

1. **El ~70% no es del examen original de Spider 2.0** — viene de Spider
   2.0-AIFunc (arXiv 2607.06229): 465 instancias sobre 125 bases en Snowflake
   con AI functions; los mejores propietarios se agrupan en 67–70.3% (Claude
   Opus 4.6 = 70.3%). El draft lo atribuía a "su variante más reciente" sin
   nombrarla y la fuente lo colgaba de 2411.07763. Aplicado: el texto ahora
   nombra Spider 2.0-AIFunc y aclara que es "otro conjunto de tareas, no el
   examen original"; fuentes separadas en dos entradas. También se eliminó
   "año y medio después" (nov-2024 → jul-2026 son ~20 meses, la cifra no
   aguantaba).
2. **"Business Semantics en GA desde inicios de este año"** — Metric Views /
   Business Semantics llegaron a GA en **abril de 2026**, no "inicios".
   Aplicado: "desde abril de este año". (Glossary y Domains siguen en preview;
   el draft no los menciona, así que no hay más que corregir.)
3. **Fuente Spider 2.0 precisada** — la entrada de fuentes ahora dice 21.3%
   (o1-preview) vs 91.2% en Spider 1.0, en lugar del ambiguo "~20%… ~70%".

## MENOR

1. ⏳ **Decisión de Ricardo — cifra 64.5%:** dbt reporta además que el
   text-to-SQL crudo pasó de 32.7% (2023) a 64.5% (2026) *sobre el set
   completo de preguntas*. El 84–90% del draft es correcto (modelos de
   frontera sobre las 11 preguntas), pero si alguien contrasta con el post de
   dbt verá el 64.5%. Opcional: una frase tipo "sobre el set completo la cifra
   agregada es menor" blindaría el argumento. No aplicado por ser criterio
   editorial.
2. ⏳ **Comparación 2023 vs 2026 mezcla harnesses:** 16.7%/54.2% son de
   Sequeda (43 preguntas, GPT-4, knowledge graph); 84–90%/98–100% son de dbt
   (11 preguntas, semantic layer MetricFlow). El draft ya divulga el
   subconjunto, así que es defendible, pero el bullet "2023 → 2026" los
   presenta como el "mismo examen". Riesgo bajo; a criterio de Ricardo si
   quiere suavizar a "mismo dataset, harness distinto".
3. ✅ (aplicado dentro del IMPORTANTE 1) "año y medio después" eliminado.
4. ✅ Dato de dbt "3 de 11 preguntas requieren joins que el semantic layer no
   expresa sin modelos adicionales" — el draft no lo usa y no lo necesita;
   solo se registra aquí por si el humanizer quiere matizar el "98–100%".

## Estructura v2 y recorte (recomendación, no aplicado)

El arco 2023 → operación → Spider → letra chica → vendors → SAP → error de
compra → prueba **fluye sin saltos lógicos**; cada sección empuja la tesis.
Pero está en ~1,483 palabras (~3.5 pág), arriba del formato opinión (2–3 pág).
Recorte sugerido (~180–250 palabras) donde hay redundancia real:

- **"La letra chica" ↔ "SAP también votó":** ambos usan el mismo trío
  (extractores + rutinas + reporte Z con decisión no documentada). Sugerencia:
  en "letra chica" dejar solo VBAK/VBAP y la ventana de contexto, y mover el
  ejemplo de "decisión de 2019 sobre devoluciones" a una sola aparición — hoy
  compite con el "ajuste de hace siete años" de "El error de compra" (tres
  variantes de la misma anécdota).
- **"Las dos lecturas importan"** (sección Spider): puede comprimirse a la
  segunda lectura; la primera repite lo que el lector ya concluyó del 20%.
- El párrafo final de "Los vendors ya votaron" ("Esto lo veo operando…") es
  valioso (primera persona) — no recortar ahí.

**Nota operativa de costo:** el hook de la sesión volvió a marcar costo alto
(USD $50.39 acumulado) durante esta pasada; el coordinador indicó continuar
con conocimiento de Ricardo. Queda registrado.
