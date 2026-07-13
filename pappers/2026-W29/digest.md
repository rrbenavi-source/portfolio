# Digest 2026-W29

_Barrido manual — ventana 2026-07-03 → 2026-07-10. Fuentes: `sources.yaml`
(Databricks, SAP, Microsoft/Fabric, dbt, arXiv/research, Data Engineering Weekly,
Benn Stancil, VentureBeat)._

> **Tema de la semana:** el agente de datos pasó de *responder* a *ejecutar* — y
> la factura ya llegó. La edición pasada (W28) discutió si el agente dice la
> verdad (contexto/semantic layer). Esta ventana el hilo se movió: casi todo lo
> publicado habla de **qué se rompe cuando metes un agente que actúa dentro de tu
> pipeline** (determinismo, idempotencia, costo, gobernanza) y de la reacción
> correctiva — capas deterministas, dueños claros, límites duros. VentureBeat lo
> pone en número: ~79% de las empresas ya sufrió un fallo real de control por
> agentes autónomos. El debate dejó de ser "¿es cierto?" y pasó a ser
> "¿es operable y cuánto cuesta?".

---

## Idea 1 — Tus DAGs asumían determinismo. El agente lo rompió.  ⭐ (top / seed)
- **Formato:** deep-dive
- **Tesis:** Un pipeline clásico es confiable porque *hereda* tres garantías de
  su forma: determinismo, costo acotado e idempotencia. Una llamada a un LLM las
  viola las tres a la vez. La conclusión práctica no es "no uses agentes", es que
  la confiabilidad ya no se hereda: hay que *ingenierarla* explícitamente —
  idempotency keys antes de cada acción con efecto, costo-por-corrida como métrica
  de primera clase, y observabilidad de *correctitud*, no de *éxito* (un 200 con
  respuesta vacía se ve idéntico a un job que funcionó).
- **Por qué ahora:** Tres fuentes independientes convergen en la misma ventana:
  el ensayo de Towards Data Engineering (4-jul) que enumera exactamente qué
  supuestos se rompen; Simon Späti (7-jul) proponiendo una "correctness layer"; y
  Data Engineering Weekly #277 (6-jul) recogiendo el patrón de "loop engineering"
  de Addy Osmani. No es hype de vendor: es el gremio de data engineering
  reescribiendo sus reglas.
- **Ángulo de Ricardo:** desde la trinchera SAP–Databricks. Un job que corre dos
  veces contra S/4HANA y duplica un asiento contable no es un "bug del modelo": es
  un fallo de diseño que la disciplina SAP (idempotencia, reprocesos controlados,
  claves de negocio) ya sabía resolver hace 20 años. El mensaje anti-hype: los
  fundamentos aburridos de data engineering son justamente lo que hace desplegable
  a un agente. Reprocesabilidad primero, agente después.
- **Fuentes:**
  - https://medium.com/towards-data-engineering/data-engineering-for-ai-agents-what-actually-changes-in-your-pipeline-design-682858705cc9 — (4-jul) los 3 supuestos que se rompen y los 4 arreglos concretos: idempotency keys, costo por stage, semantic cache, observabilidad de correctitud.
  - https://www.ssp.sh/blog/where-agents-belong-in-de/ — (7-jul) la "correctness layer": agente probabilístico arriba, núcleo determinista abajo; el agente nunca decide equivalencia de queries, la *prueba*.
  - https://www.dataengineeringweekly.com/p/data-engineering-weekly-277 — (6-jul) "loop engineering": worktrees aislados, SKILL.md, sub-agentes maker/checker y estado en disco que sobrevive cada corrida.

## Idea 2 — El control gap: 79% ya se quemó. Ponle dueño al agente antes de escalarlo.
- **Formato:** opinión
- **Tesis:** El cuello de botella de los agentes en producción no es técnico, es de
  *propiedad*. Nadie es accountable end-to-end, así que la gobernanza sigue siendo
  manual (revisión humana), y la factura llega por vías tontas: shadow AI en
  tarjetas corporativas y el "infinite loop bill". La tesis opinable: antes de
  escalar un agente, define el dueño y pon límites *deterministas* (throttling,
  budget caps a nivel de infraestructura). El gobierno por buena voluntad no
  escala; el gobierno por cuota sí.
- **Por qué ahora:** El Pulse Research de VentureBeat (1-jul) es demoledor: solo
  10% tiene monitoreo y alerta activos, 49% cita shadow AI como su peor fallo, 25%
  ya comió un infinite-loop bill, y 32% dice que el mayor bloqueo es "no hay un
  solo dueño". Lo refuerza la charla de Red Hat (7-jul) sobre disciplina de costo
  y buy-in de los expertos de dominio.
- **Ángulo de Ricardo:** el ángulo de *liderazgo* (team lead). La pregunta
  incómoda: "¿quién es el agente cuando ejecuta, y quién responde por su factura?".
  En un entorno SAP la respuesta *parcial* ya existe — service principals,
  autorizaciones, segregación de funciones — y el trabajo es extender esa cultura
  de accountability al plano agéntico, no reinventarla. Value-driven: la gobernanza
  no es freno, es lo que permite decir "sí" a producción.
- **Fuentes:**
  - https://venturebeat.com/resources/the-control-gap-enterprise-ai-organizations-have-an-ownership-problem-not-a-technology-problem-and-most-are-governing-it-by-hand — (1-jul) los números del "control gap": ownership, detección manual, shadow AI, infinite-loop bill.
  - https://venturebeat.com/security/the-real-cost-security-and-culture-problems-behind-enterprise-ai-agents — (7-jul) Red Hat: costo como tema de directorio, y por qué el buy-in del experto de dominio decide si el agente escala.

## Idea 3 — El query layer de BW/4HANA PCE en BDC: el "lift" deja de ser estacionamiento
- **Formato:** deep-dive
- **Tesis:** El "lift & shift" de BW a Business Data Cloud dejaba una duda legítima:
  ¿mover BW a la nube es solo estacionarlo con un costo nuevo? La evolución de BDC
  esta temporada cambia el cálculo: HANA Cloud ahora es componente nativo de BDC, el
  Data Product Generator ya trae onboarding semántico de asociaciones, y el consumo
  vía SQL-on-file en el object store hace que los BW Data Products sean gobernados y
  consumibles zero-copy en Datasphere/SAC y Databricks. La tesis opinable: para un
  shop BW/4HANA, la migración deja de ser defensa (end of maintenance 2027) y se
  vuelve palanca — *si* modelas el "shift" con intención y no arrastras lógica sucia
  de queries legacy.
- **Por qué ahora:** SAP publicó en la ventana el caso de People Analytics sobre BDC
  (7-jul) y "What's New in SAP HANA Cloud – July 2026"; los release highlights de BDC
  (jun) confirman HANA Cloud nativo, object-store sources en replication flows y
  acceso directo a delta shares en transformation flows. Es el núcleo exacto del
  stack de Ricardo y una decisión de arquitectura que muchos líderes SAP están
  cerrando en 2026.
- **Ángulo de Ricardo:** el más "suyo". Guía de decisión BW-modernization desde la
  experiencia real: qué se gana con el DPG y el object store, dónde está la trampa
  (queries-as-InfoProvider que obligan a re-implementar semántica), y por qué el
  esfuerzo de modelar en el "shift" es lo que evita heredar deuda al lakehouse.
- **Fuentes:**
  - https://news.sap.com/2026/07/how-sap-is-reinventing-people-analytics/ — (7-jul) caso de negocio de analítica gobernada sobre BDC, en la ventana.
  - https://community.sap.com/t5/data-professionals-knowledge-base/sap-business-data-cloud-release-update-highlights/ta-p/14419067 — (jun, actualización continua) HANA Cloud nativo en BDC, object-store sources, acceso directo a delta shares sin copia intermedia.
  - https://community.sap.com/t5/technology-blog-posts-by-sap/need-to-know-beyond-sap-analytics-cloud-ai-and-using-sap-databricks-in-sap/ba-p/14416821 — (11-jun) walkthrough end-to-end BDC↔SAP Databricks vía Delta Sharing zero-copy, y vuelta del resultado como derived Data Product.
  - https://community.sap.com/t5/technology-blog-posts-by-sap/bw-modernisation-with-the-sap-bw-data-product-generator/ba-p/14336399 — (feb, vigente) DPG: exponer ADSOs/CompositeProviders/Queries como local tables y data products; base técnica del "shift".

## Idea 4 — Cost-per-task, no cost-per-token: la economía real (y anti-hype) de los agentes de datos
- **Formato:** opinión
- **Tesis:** La métrica que todos miran — costo por token — es la equivocada,
  porque el propio medidor se mueve con cada release de modelo. Lo que hay que
  optimizar es *costo por tarea*. Y el mayor ahorro no es un modelo más barato: es
  *no llamar al modelo* para lo que una función determinista resuelve en
  submilisegundos (parsear, validar, transpilar, comparar equivalencia). El
  "tokenmaxxing" (tener un agente corriendo todo el día) es lujo, no rigor.
- **Por qué ahora:** Späti (7-jul) articula "correctness over confidence" y cita el
  argumento de "The Great Token Heist of '26" (cost-per-token es el número
  equivocado). VentureBeat (1 y 7-jul) pone el costo agéntico como tema de
  directorio y documenta el infinite-loop bill. Benn Stancil (jun) empuja la tesis
  de fondo — casi todo el mundo quiere "meterse en el token path" — que es
  justamente el hype que conviene desinflar.
- **Ángulo de Ricardo:** value-driven y anti-humo. Desde HEINEKEN, el costo de un
  pipeline es una línea de presupuesto real, no una demo. El encuadre: el agente
  que ahorra tokens porque delega en tooling determinista no es "menos IA", es
  ingeniería adulta. Contraste con el discurso de "ponle un agente a todo".
- **Fuentes:**
  - https://www.ssp.sh/blog/where-agents-belong-in-de/ — (7-jul) cost-per-task vs cost-per-token; funciones deterministas que evitan quemar tokens; "token lean".
  - https://venturebeat.com/resources/the-control-gap-enterprise-ai-organizations-have-an-ownership-problem-not-a-technology-problem-and-most-are-governing-it-by-hand — (1-jul) el costo del descontrol: infinite-loop bill, shadow AI.
  - https://benn.substack.com/p/get-out-of-the-token-path — (jun, vigente) "Your agent will be your undoing": la crítica de fondo al reflejo de "vender tokens / meter IA a todo".

## Idea 5 — Del agente que responde al agente que opera: ZeroOps y el "agentic data engineering"
- **Formato:** deep-dive
- **Tesis:** El salto de 2026 no es que el agente *escriba* SQL, es que *opere* el
  pipeline: detecta el fallo, hace root-cause con lineage y logs, propone el fix y
  lo valida en un sandbox gobernado — con human-in-the-loop. Databricks empuja este
  runtime (Lakeflow, Genie ZeroOps, feature views auto-mantenidas, upgrades
  automáticos de tablas). La postura opinable: la promesa es real, pero el
  diferenciador defendible no es el modelo — es el human-in-the-loop y que las
  trazas del agente vivan gobernadas en el lakehouse, auditables, no en un silo de
  vendor.
- **Por qué ahora:** En la ventana, Databricks publicó "Automatic Upgrades" para
  tablas del lakehouse (6-jul) e "Introducing Feature Views" (10-jul), extensiones
  concretas del stack agéntico presentado en DAIS (Lakeflow/ZeroOps). Encadena con
  las Ideas 1–2: el agente que opera es exactamente el que rompe supuestos y hay que
  gobernar.
- **Ángulo de Ricardo:** más técnico, pieza de autoridad. Puede contrastar el
  "ZeroOps" automático con la realidad de un entorno SAP: qué operación
  delegarías a un agente y cuál exige aún firma humana, y por qué la trazabilidad
  gobernada (Unity Catalog) es la precondición, no el adorno.
- **Fuentes:**
  - https://www.databricks.com/blog/lakeflow-new-era-agentic-data-engineering — (DAIS, vigente) Genie ZeroOps: detección de fallos, RCA, fix propuesto validado en sandbox, human-in-the-loop.
  - https://www.databricks.com/blog/automatic-upgrades-best-practice-features-your-lakehouse-tables — (6-jul) mantenimiento automático de tablas del lakehouse.
  - https://www.databricks.com/blog/introducing-feature-views — (10-jul) feature views gobernadas en Unity Catalog.
  - https://venturebeat.com/data/databricks-says-it-solved-the-decades-old-data-pipeline-problem-thats-been-slowing-ai-agents — (16-jun, vigente) LTAP + Lakehouse//RT: colapsar la infraestructura porque "un stack simple es el santo grial para los agentes".

---

### Ranking sugerido
1. **Idea 1** (seed) — máxima afinidad práctica + tesis opinable + voz de
   experiencia (idempotencia SAP). Es el ángulo más nuevo respecto a W28 y el que
   mejor sostiene un deep-dive con autoridad de ingeniería.
2. **Idea 3** — la más "de Ricardo" y de decisión real de arquitectura (BW/4HANA →
   BDC). Alto valor para su audiencia SAP; noticiosa en la ventana.
3. **Idea 2** — excelente para opinión de liderazgo (gobernanza y factura de
   agentes); números duros de VentureBeat le dan gancho.
4. **Idea 4** — opinión anti-hype filosa (cost-per-task); combina bien como
   sección dentro de la Idea 1 o 2 si se busca un solo papper.
5. **Idea 5** — reserva / autoridad técnica; riesgo de rozar la Idea 3 de W28
   (gobernanza de agentes), por eso va al final salvo que se enfoque puro en
   "operación autónoma del pipeline".

_Nota de verificación de fuentes: todas las URLs provienen de resultados de
búsqueda web reales de esta sesión, con fecha de publicación visible. Verifiqué
como **publicadas en la ventana** (3–10 jul): las tres de VentureBeat, DEW #277,
ssp.sh, el Medium de Towards Data Engineering, los dos posts de Databricks
(Automatic Upgrades, Feature Views) y la nota de SAP News de People Analytics.
Vigentes/recientes pero fuera de la ventana estricta: Lakeflow y LTAP de
Databricks (DAIS/16-jun), release highlights de BDC (jun), "Beyond SAC AI /
SAP Databricks" (11-jun), Benn Stancil (jun) y el DPG blog de SAP (feb).
**No verificado / no incluido:** el post de SAP "Accessing BW Data Products in
the Query Layer of SAP BW/4HANA PCE in BDC" aparece como enlace relacionado
("a week ago", ~3-jul) pero no pude confirmar su URL directa, así que NO lo cité
para no inventar el link. Para research, TOFFEE (arXiv 2607.06233, jul-2026)
sobre síntesis de trayectorias de data agents queda como material de respaldo si
se quiere una pieza más académica; su URL html no la verifiqué accesible._
