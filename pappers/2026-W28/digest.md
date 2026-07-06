# Digest 2026-W28

_Barrido manual — ventana 2026-06-29 → 2026-07-06. Fuentes: `sources.yaml`
(Databricks, SAP, Microsoft/Fabric, dbt, arXiv/research, newsletters)._

> **Tema de la semana:** el *semantic layer* dejó de ser un detalle de modelado
> y se volvió la infraestructura que decide si los agentes de datos dicen la
> verdad. Casi todas las fuentes de la semana convergen ahí.

---

## Idea 1 — El semantic layer: el activo que decide si tus agentes de datos dicen la verdad  ⭐ (top / seed)
- **Formato:** deep-dive
- **Tesis:** El cuello de botella de la BI generativa no es el modelo, es el
  contexto. Sin un semantic layer gobernado, el text-to-SQL falla de la peor
  forma posible: te da un número plausible y equivocado. Con él, cuando no puede
  responder, te lo dice. Esa diferencia es todo para un KPI de directorio.
- **Por qué ahora:** El benchmark 2026 de dbt muestra text-to-SQL en ~64.5% de
  acierto contra ~100% dentro del alcance del semantic layer; Databricks presentó
  Genie Ontology como "capa de contexto viva"; Dremio, Snowflake y otros publican
  la misma tesis la misma semana.
- **Ángulo de Ricardo:** hablar desde la migración SAP–Databricks: por qué el
  esfuerzo de modelar (BW/4HANA, Unity Catalog) es justamente lo que hace
  confiable a un agente, no un lujo previo a la IA.
- **Fuentes:**
  - https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — benchmark 64.5% vs ~100%; "el fallo del SL es un error, el del text-to-SQL es una mentira plausible".
  - https://www.dremio.com/blog/semantic-layer-for-ai-agents-stop-getting-the-numbers-wrong/ — el SL cubre el 80% de errores de alto impacto (tabla/columna/regla de negocio equivocada).
  - https://www.databricks.com/blog/introducing-genie-code — Genie Ontology como capa de contexto que codifica métricas y términos del negocio.

## Idea 2 — SAP Business Data Cloud + Databricks ya es GA: qué cambia para un shop BW/4HANA
- **Formato:** deep-dive
- **Tesis:** Con la GA de SAP Databricks sobre BDC y el conector zero-copy vía
  Delta Sharing + Unity Catalog, la decisión ya no es "¿saco los datos de SAP?"
  sino "¿cómo gobierno un solo plano de datos entre SAP y el lakehouse?".
- **Por qué ahora:** Anuncios de disponibilidad general esta ventana; es el núcleo
  exacto del stack de Ricardo y una decisión de arquitectura que muchos líderes
  SAP están tomando en 2026.
- **Ángulo de Ricardo:** el más "suyo" de todos — puede escribir la guía de
  decisión que le hubiera gustado tener, con los trade-offs reales (costo,
  gobernanza, latencia, Datasphere subsumido en BDC).
- **Fuentes:**
  - https://www.databricks.com/blog/announcing-general-availability-sap-databricks-sap-business-data-cloud — GA de SAP Databricks sobre BDC.
  - https://www.databricks.com/blog/announcing-general-availability-sap-business-data-cloud-connect-databricks — GA del conector BDC↔Databricks (Delta Sharing zero-copy, Unity Catalog).
  - https://adastracorp.com/insights/sap-databricks-in-2026-a-strategic-architecture-decision-for-enterprise-ai/ — lectura de la decisión de arquitectura para líderes de negocio.

## Idea 3 — Agentes de datos en producción: el salto de la demo a la operación gobernada
- **Formato:** opinión
- **Tesis:** 2026 es el año en que los agentes de datos pasan de "demo impresionante"
  a "operación bajo gobierno": identidad propia (service principals), catálogo,
  alertas, MCP. El diferenciador ya no es el modelo, es el control plane.
- **Por qué ahora:** Databricks posiciona el lakehouse como "el plano de control
  agéntico de la empresa" (Bain); Fabric habilita service principals y agentes
  declarativos en M365 Copilot; Genie se embebe en Teams/Excel.
- **Ángulo de Ricardo:** la pregunta incómoda de gobernanza — ¿quién es el agente
  cuando ejecuta una query?, ¿qué ve, con qué permisos, con qué trazabilidad?
- **Fuentes:**
  - https://www.bain.com/insights/databricks-data-ai-summit-the-lakehouse-becomes-the-agentic-enterprise-control-plane/ — el lakehouse como plano de control agéntico.
  - https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Fabric-June-2026-Feature-Summary/ba-p/5190690 — service principals para data agents; agentes declarativos en M365 Copilot.
  - https://www.databricks.com/blog/agent-bricks-dais-2026 — Agent Bricks como runtime de agentes sobre datos gobernados.

## Idea 4 — Semantic layer automático: la promesa (y la trampa) de aprender de tus query logs
- **Formato:** opinión
- **Tesis:** Herramientas como Cortex Sense prometen construir el semantic layer
  observando cómo ya consultas tus datos. Genial contra el cuello de botella del
  modelado manual — pero si tus logs históricos tienen lógica sucia, el sistema
  aprende y propaga esos errores con total confianza.
- **Por qué ahora:** Snowflake presentó Cortex Sense (semantic layer inferido de
  señales existentes) esta ventana; contrasta directo con la tesis "modela a mano"
  de dbt/Dremio. Debate abierto y jugoso.
- **Ángulo de Ricardo:** el trade-off velocidad vs. deuda semántica; por qué el
  human-in-the-loop no es opcional cuando el número va a un board.
- **Fuentes:**
  - https://dev.to/albertomontagnese/text-to-sql-is-still-brittle-snowflakes-cortex-sense-is-a-new-take-2ahj — Cortex Sense infiere el semantic layer de query logs; riesgo de heredar malos hábitos.
  - https://www.snowflake.com/en/blog/engineering/agentic-semantic-model-text-to-sql/ — sistema agéntico que mejora el modelo semántico (+20% acierto) con validación estructurada.
  - https://medium.com/@hello_27440/from-promise-to-reliability-semantic-mapping-and-sql-validation-as-dual-drivers-for-enterprise-1596b893ebe4 — mapeo semántico + validación SQL en 3 capas (sintaxis/lógica/negocio).

## Idea 5 — Antes de que el agente escriba SQL: descubrir y gobernar el esquema
- **Formato:** deep-dive
- **Tesis:** El paso invisible que decide el éxito de NL2SQL no es el prompt: es
  convertir metadata cruda en una capa semántica gobernada (dominios, descripciones
  de columnas, grafos de relación) *antes* de dejar que el agente razone.
- **Por qué ahora:** Oracle publicó su Schema Discovery Agent (pipeline de 11 pasos,
  detección de comunidades + embeddings) el 6-jul; encaja con la ola de "primero el
  contexto, después el SQL".
- **Ángulo de Ricardo:** más técnico; útil como pieza de autoridad de ingeniería.
  Puede contrastar el enfoque automático con el modelado curado que exige un
  entorno SAP.
- **Fuentes:**
  - https://blogs.oracle.com/cloud-infrastructure/schema-discovery-agent-for-nl2sql-ai — pipeline de descubrimiento de esquema como fundación semántica gobernada para NL2SQL.
  - https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — la calidad del modelado importa enormemente para ambos enfoques.

---

### Ranking sugerido
1. **Idea 1** (seed) — máxima afinidad + tesis opinable + permite voz de experiencia.
2. **Idea 2** — la más "de Ricardo" y la más noticiosa (GA esta semana).
3. **Idea 3** — buena para opinión de liderazgo (gobernanza de agentes).
4. Ideas 4 y 5 — reserva / material de autoridad técnica.

_Nota: todas las fuentes se verificaron como publicadas en la ventana o vigentes
esta semana. Ninguna fuente quedó inaccesible durante el barrido._
