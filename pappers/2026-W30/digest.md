# Digest 2026-W30

_Barrido manual — ventana 2026-07-13 → 2026-07-20. Fuentes: `sources.yaml`
(Databricks, SAP News/Community, Microsoft/Fabric, dbt, arXiv/research,
Data Engineering Weekly, Benn Stancil, Seattle Data Guy, VentureBeat)._

> **Tema de la semana:** pasó el eval y aun así rompió con el cliente. W28
> preguntó si el agente *dice la verdad* (contexto/semantic layer); W29 mostró
> que el agente pasó de *responder* a *ejecutar* (determinismo, costo,
> gobernanza). Esta ventana el hilo se movió a la **medición**: VentureBeat
> publicó un clúster de encuestas (15–16 jul) demoledor — la mitad de las
> empresas ya desplegó un agente que **pasó sus evals internos y luego falló
> frente a un cliente**, casi nadie confía en sus evals automáticos, y aun así
> dos tercios están quitando al humano del gate de deployment. El debate dejó de
> ser "¿es cierto?" y "¿cuánto cuesta?" para volverse **"¿cómo sabes que
> funciona — y por qué estás removiendo al humano justo ahora?"**.

---

## Idea 1 — El eval verde es el nuevo "200 OK": medir éxito no es medir correctitud  ⭐ (top / seed)
- **Formato:** opinión / autoridad
- **Tesis:** Un eval en verde no es un agente que funciona, igual que un HTTP 200
  con respuesta vacía no es un job que corrió bien. La industria está cometiendo
  un error de medición de manual: confunde *pasó la prueba* con *hizo lo
  correcto*, y encima está removiendo al humano del deployment justo cuando menos
  confía en la prueba. La postura opinable: la confiabilidad de un agente no se
  certifica con un pass/fail al final, se *instrumenta* — monitoreo de
  **correctitud en producción** (no de uptime), trazas como capa de evidencia, y
  un human-in-the-loop obligatorio donde la salida toca una decisión de negocio.
  Quitar el gate humano antes de que el eval refleje la realidad no es madurez,
  es automatizar la falsa confianza.
- **Por qué ahora:** El clúster Pulse de VentureBeat de esta ventana es el gancho:
  50% ya desplegó un agente que pasó sus evals y falló con un cliente (25% más de
  una vez); solo 5% confía plenamente en sus evals automáticos; el defecto más
  citado es "mala alineación con resultados reales" (29%); y 51% monitorea solo si
  el agente *funciona*, mientras solo 23% monitorea si sus respuestas son
  *correctas*. Aun así, 66% ya permite —o está construyendo hacia— deployment sin
  humano en el loop. Lo refuerzan Databend ("Trace is Evals", el trace como capa
  de evidencia, no de debug) y philliant ("un árbol de git limpio no es un estado
  known-good; lee el diff, no el resumen del agente").
- **Ángulo de Ricardo:** desde la disciplina SAP. En un entorno serio no publicas
  un reporte financiero porque el job terminó en verde: lo publicas cuando *cuadra*
  — reconciliación, control de totales, un dueño que firma. Ese gate de
  correctitud (no de éxito) es exactamente lo que la ingeniería de datos madura ya
  sabía hacer antes de que existieran los agentes. El mensaje de liderazgo y
  anti-humo: automatizar el deployment es fácil; automatizar la *confianza* es el
  error caro. Value-driven: el human-in-the-loop no frena la escala, es lo que
  permite decir "sí" a producción sin apostar la operación.
- **Fuentes:**
  - https://venturebeat.com/ai/the-agent-evaluation-gap-enterprise-ai-organizations-have-a-reality-alignment-problem-not-a-coverage-problem-and-most-are-shipping-to-production-anyway — (16-jul, en ventana) el "evaluation gap": 50% pasó eval y falló con cliente; 5% confía; 51% mira uptime vs 23% correctitud; 66% hacia zero-human deployment.
  - https://medium.com/@databend/trace-is-evals-data-engineering-for-agent-trace-analysis-and-attribution-9c173e8ce657 — (2-jul, vigente) "Trace is Evals": el pass/fail final no basta; el trace completo es la capa de evidencia para evaluar, atribuir y reproducir.
  - https://philliant.com/writings/ai-assisted-data-engineering/02-the-danger-of-trusting-the-agent/ — (8-jul, reciente) automation bias; "clean tree ≠ known-good state"; lee el diff y el output real, no el resumen del agente; ownership como estándar.
  - https://venturebeat.com/orchestration/wall-street-is-debating-the-ai-buildout-enterprises-just-answered-86-say-their-gpus-run-at-half-capacity-or-less — (10-jul, actualizado 14-jul en ventana) solo 23% corre chequeos de calidad en vivo; "instrumenta calidad de respuesta, no solo uptime".

## Idea 2 — SAP Databricks vs Enterprise Databricks: la decisión de arquitectura que muchos líderes SAP cierran en 2026
- **Formato:** deep-dive / decisión
- **Tesis:** Para un shop BW/4HANA la pregunta de 2026 no es "¿migro a la nube?",
  es "¿qué Databricks?". Y la respuesta no se decide por potencia sino por
  encaje: SAP Databricks (gestionado por SAP, embebido en BDC) preserva el
  business context y la gobernanza SAP; Enterprise Databricks (nativo) da el
  lakehouse amplio cross-SAP/no-SAP. La tesis opinable: para la mayoría de los
  shops SAP el ganador no es uno u otro sino el **híbrido con BDC Connect** —
  zero-copy Delta Sharing como columna vertebral, BDC como fundación semántica
  gobernada, Enterprise Databricks para ingeniería y AI a escala — y el momento
  de la verdad está en el "shift" con el Data Product Generator: si arrastras
  Queries-as-InfoProvider con semántica sucia, heredas deuda al lakehouse; si
  modelas con intención, el "lift" deja de ser un estacionamiento caro y se
  vuelve palanca.
- **Por qué ahora:** La ventana concentra material de decisión: la guía ejecutiva
  de SAP Insider "SAP Databricks vs Enterprise Databricks" (8-jul) que compara
  roles y costo; conectividad privada a BDC vía AWS PrivateLink en las release
  notes de Databricks (9-jul); y en SAP Community aparece por fin —tras semanas
  como enlace relacionado— el post "Accessing BW Data Products in the Query Layer
  of SAP BW/4HANA PCE in BDC" (~17-jul) más un "Architecture Deep-Dive:
  Transforming SAP BW with SAP BDC" (~19-jul). Es el núcleo exacto del stack de
  Ricardo y una decisión que se está cerrando este año con el end-of-maintenance
  2027 de BW 7.5 de fondo.
- **Ángulo de Ricardo:** el más "suyo" y de arquitecto. Guía de decisión anónima
  desde la trinchera SAP–Databricks: cuándo SAP Databricks paga su costo y cuándo
  BDC Connect + Enterprise Databricks es más barato y más flexible; por qué el
  zero-copy con semantic metadata sync a Unity Catalog cambia el cálculo; y dónde
  está la trampa del DPG (carga física a HDLFS, merge tasks, delta) para no
  vender un "zero-copy" que en realidad materializa. Anclar en marcos SAP
  reconocidos (lift-shift-innovate, clean core) y no nombrar cliente ni sociedad.
- **Fuentes:**
  - https://sapinsider.org/expert-insights/sap-databricks-vs-enterprise-databricks-guide/ — (8-jul) comparación ejecutiva de roles, costo y el modelo híbrido; BDC Connect como habilitador zero-copy para Snowflake/Fabric/Databricks.
  - https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing — (30-abr, GA vigente) sync automático de semantic metadata y tags de gobernanza SAP BDC → Unity Catalog; SAP sigue siendo source of truth.
  - https://community.sap.com/t5/technology-blog-posts-by-sap/bw-modernisation-with-the-sap-bw-data-product-generator/ba-p/14336399 — (feb, vigente) DPG: exponer ADSOs/CompositeProviders/Queries como local tables (file) y data products; base técnica del "shift".
  - https://community.sap.com/t5/technology-blog-posts-by-sap/blog-2-accelerating-sap-bw-modernization-hands-on-experiences-with-the-bdc/ba-p/14333206 — (feb, vigente) experiencia real de piloto BW→BDC: carga física a HDLFS, subscriptions, merge tasks, association handling; matices del "zero-copy".
  - _(sin cita directa)_ SAP Community: "Accessing BW Data Products in the Query Layer of SAP BW/4HANA PCE in BDC" y "Architecture Deep-Dive: Transforming SAP BW with SAP BDC" aparecen en los listados de la ventana (~17–19 jul) pero **no verifiqué sus URLs directas**; no los cito para no inventar el link.

## Idea 3 — La mayoría de tus "agentes" son chatbots con nombre bonito (y el label decide la factura)
- **Formato:** opinión anti-hype
- **Tesis:** El 71% de las empresas admite que un cuarto o menos de sus "agentes"
  son de verdad workflows multi-step; el resto son chatbots de un solo prompt con
  un nombre de producto encima. Y esto no es semántica: el label decide el riesgo
  y la factura. Un chatbot con un humano leyendo cada respuesta no necesita
  identity, eval ni cost controls; un agente que ejecuta multi-step los necesita
  todos. La postura opinable: antes de "ponerle un agente a todo", clasifica
  honestamente qué tienes, porque el discurso de "somos AI-native" está
  inflando expectativas de tablero y presionando a los líderes técnicos a
  moverse más rápido de lo que su control real permite.
- **Por qué ahora:** VentureBeat "agentic orchestration" (15-jul) pone el número —
  71% ≤25% de agentes reales, 27% no puede detener un agente descontrolado en
  tiempo real— y titula justo "most are calling chatbots agents". Benn Stancil lo
  ataca por el otro lado: "get out of the token path" (el reflejo de meterle un
  chatbot a todo) y "be a winner, or join one?" (10-jul) sobre wrappers
  derivativos. Seattle Data Guy (jun, vigente) aterriza el anti-humo: "comprar una
  suscripción a Claude no te hace AI-native; los fundamentos de datos importan
  más que nunca".
- **Ángulo de Ricardo:** liderazgo técnico y anti-humo. La pregunta de team lead:
  "¿esto es un agente o un chatbot con disfraz, y qué controles exige de
  verdad?". Desde la experiencia: los fundamentos aburridos —modelado, contratos,
  reprocesabilidad— son los que separan un agente desplegable de una demo.
  Value-driven: nombrar bien lo que tienes es lo que evita comprar (y gobernar)
  controles que no necesitas, o peor, no comprar los que sí.
- **Fuentes:**
  - https://venturebeat.com/ai/agentic-orchestration-enterprise-ai-organizations-have-a-deployment-problem-not-a-platform-problem-and-most-are-calling-chatbots-agents — (15-jul, en ventana) 71% ≤25% de "agentes" son multi-step reales; 27% sin control fiscal en tiempo real; el label decide qué controles hacen falta.
  - https://benn.substack.com/p/get-out-of-the-token-path — (5-jun, vigente) "Your agent will be your undoing": la crítica de fondo al reflejo de meter IA/chatbot a todo producto.
  - https://benn.substack.com/p/be-a-winner-or-join-one — (10-jul, en ventana) los "smaller companies" como wrappers derivativos frente a los labs; ¿construyes tu agente o te subes al de otro?
  - https://seattledataguy.substack.com/p/in-2026-the-data-fundamentals-matter — (13-jun, vigente) los fundamentos de datos siguen siendo el cuello de botella real; "AI-native" no se compra con una suscripción.

## Idea 4 — El 69% comparte credenciales entre agentes: extiende tu cultura SAP de SoD al plano agéntico
- **Formato:** deep-dive / gobernanza
- **Tesis:** La pieza más incompleta de la seguridad de agentes no es el modelo,
  es la **identidad**. 54% de las empresas ya tuvo un incidente o near-miss de
  seguridad agéntica, solo 32% le da a cada agente una identidad propia con scope,
  y 69% comparte credenciales en algún punto del fleet — lo que significa que un
  solo agente sobre-permisado tiene un blast radius enorme y, tras el incidente,
  el forensics no puede decir qué agente hizo qué. La tesis opinable: no hay que
  inventar una disciplina nueva. La cultura de non-human identity, service
  principals, autorizaciones y segregation of duties (SoD) que SAP lleva 20 años
  operando es precisamente el modelo que falta — el trabajo es *extenderla* al
  plano agéntico, con scoped identity por agente, sandbox para los de alto riesgo
  y enforcement en runtime, no post-hoc.
- **Por qué ahora:** VentureBeat "agent security gap" (16-jul) trae los números
  duros. Del lado vendor, Databricks respondió justo en la temporada con Unity AI
  Gateway y Contextual Service Policies (governar *qué hace* un agente en runtime,
  no solo a qué accede) y Secrets en Unity Catalog (release notes de 20-jul). El
  hueco de gobernanza tiene ahora tanto la evidencia del problema como el
  andamiaje de la solución.
- **Ángulo de Ricardo:** gobernanza y liderazgo, desde SAP. El paralelo es
  directo: SoD, roles, service principals y trazabilidad ya existen en un entorno
  SAP maduro; la falla de las empresas es tratar al agente como una excepción sin
  dueño en vez de como una identidad más que gobernar. Continúa el hilo de W29
  (dueño y límites) pero en un plano distinto —identidad e isolation, no costo y
  accountability—, así que no repite: aterriza el "quién es el agente" en
  credenciales y blast radius.
- **Fuentes:**
  - https://venturebeat.com/ai/the-agent-security-gap-54-of-enterprises-have-already-had-an-ai-agent-incident-and-most-still-let-agents-share-credentials — (16-jul, en ventana) 54% incidente/near-miss; 32% scoped identity; 69% comparte credenciales; 30% aísla los de alto riesgo.
  - https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026 — (16-jun, vigente) Unity AI Gateway: governar modelos, agentes, MCPs y tools en runtime; Contextual Service Policies (allow/deny/require-approval); guardrails contra PII y prompt injection.
  - https://docs.databricks.com/aws/en/release-notes/product/2026/july — (20-jul, en ventana) Secrets en Unity Catalog (Public Preview) como securable object con namespace de tres niveles y privilegios UC.

## Idea 5 — La capa de contexto gobernada es la precondición, no el adorno: Genie Ontology y el "confident wrong answer"
- **Formato:** deep-dive técnico
- **Tesis:** 57% de las empresas rastreó al menos una respuesta *confiada y
  equivocada* de un agente a contexto de negocio ausente o inconsistente —
  métricas mal, definiciones stale, documentos faltantes. El diferenciador
  defendible de un agente de datos no es el modelo, es el **contexto de negocio
  gobernado** que lee antes de responder. La tesis opinable: el semantic layer
  dejó de ser una opción de BI y se volvió infraestructura de correctitud para
  IA; y el eje del debate se está moviendo de *definición en runtime* a
  *resolución compilada/gobernada* (semantic execution layer), porque un agente
  que adivina el join y la métrica en el momento es exactamente donde nace la
  alucinación.
- **Por qué ahora:** Databricks publicó en ventana "Unified context: the missing
  layer for enterprise AI coworkers" (16-jul) con Genie One + Genie Ontology como
  capa de contexto viva sobre Unity Catalog. Jaehyeon Kim publicó un PoC
  end-to-end de analítica agéntica con semantic layer sobre Iceberg (18-jul) que
  aísla la alucinación por diseño. Colrows (actualizado 11-jul) empuja el
  "semantic execution layer" (RBAC/ABAC/join-proofs en compile time). De fondo,
  el benchmark de dbt (abr) que mostró accuracy saltando a ~100% con semantic
  layer gobernado.
- **Ángulo de Ricardo:** autoridad técnica, pieza de arquitectura. El puente
  natural con SAP: el semantic metadata sync de SAP BDC a Unity Catalog es
  exactamente "contexto gobernado zero-copy" — el agente ve display names,
  descripciones y relaciones PK/FK, no identificadores SAP crudos. Riesgo: roza
  el tema de W28 (contexto/semantic layer), por eso va al final salvo que se
  enfoque puro en el giro nuevo: **runtime → compile-time** y el semantic layer
  como capa de *correctitud*, no de consistencia de BI.
- **Fuentes:**
  - https://www.databricks.com/blog/unified-context-missing-layer-enterprise-ai-coworkers — (16-jul, en ventana) Genie One + Genie Ontology: capa de contexto gobernada sobre Unity Catalog para "AI coworkers".
  - https://jaehyeon.me/blog/2026-07-18-agentic-analytics-system/ — (18-jul, en ventana) PoC open-source: semantic layer (WrenAI) entre el modelo y el lakehouse; generación y ejecución separadas; harness de golden tests contra alucinación.
  - https://colrows.com/blogs/semantic-layer-vs-semantic-execution-layer/ — (1-jul, actualizado 11-jul en ventana) semantic layer (runtime) vs semantic execution layer (compile-time): RBAC/ABAC/join-proofs antes de que la query toque el warehouse.
  - https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — (abr, foundational) benchmark: con semantic layer gobernado la accuracy sube a ~98–100%; el fallo se vuelve un error, no un número plausible equivocado.

## Idea 6 — El near real time que el lakehouse no te iba a dar (CASO REAL)  ⭐⭐ (seed recomendado)
- **Formato:** opinión / autoridad · **Borrador semilla:** `draft-es-nrt.md`
- **Tesis:** Cuando el dato transaccional y su lógica de negocio ya viven
  gobernados en SAP, el camino más corto para monitoreo operativo near-real-time
  es **traer la query a donde vive la verdad, no mover la verdad para
  alcanzarla**. No es que un lakehouse no haga streaming (sí puede); es que
  meterlo en medio de un reporte operativo sobre datos SAP compra latencia y
  re-implementación de semántica, no capacidad. El tiempo real no lo pone el
  destino (Power BI / SAC), lo pone el **extractor**.
- **Por qué ahora:** caso propio con evidencia de primera persona y a punto de
  liberarse a producción — la tensión real es que la dirección proponía
  **Databricks + Power BI**, mientras que el requisito de NRT (dashboard móvil,
  refresh 30 min, acción táctica durante el día) solo era viable con
  **BW/4HANA + SAC Live**. Encaja con el tema de la ventana W30 (elegir la
  arquitectura que el caso pide, no la más "moderna") y con la Idea 2.
- **Ángulo de Ricardo:** el más "suyo" y el que mejor cumple la regla editorial
  (caso real anónimo como *evidencia* de una tesis general de mejores prácticas).
  AS-IS potente: reporte manual, 3 cortes/día, 15 h-persona/semana, legado en
  Power BI. Principio de autoridad: *no muevas el dato para alcanzarlo.* Matiz
  honesto anti-overclaim: el lake sí paga en data science / cross-SAP / ML — el
  error es no **separar** el reporte operativo NRT de la plataforma de analítica.
- **Fuentes / evidencia (interna, anonimizada):** FFD "Sales Order Follow Up"
  (requerimiento + AS-IS); Definición Funcional de Indicadores (KPIs AY/LY, Meta,
  Cobertura vs Visit list, fusión SAP + interfaz externa); baraja/SLA de
  arquitectura (rama BW/4HANA+SAC streaming 15–30 min vs rama lake 2 cargas/día;
  `2LIS_11_VAITM`/ODP/ADSO `/IMO/D_SD11`/Streaming Process Chains; SAC Live vía
  InA). **Refuerzo externo (verificable, ya integrado en `draft-es-nrt.md`):**
  MIT CISR — real-time businesses del cuartil superior con **+50% ingresos y
  margen**; **data gravity** (McCrory; TechTarget 9-jul-2026; AtScale) — acerca el
  cómputo al dato, la performance se degrada al replicar; **SAP oficial** — SAC
  Live = sin replicación / near-real-time / seguridad heredada vs Import = copia +
  re-crear jerarquías; **Coalesce** (migración SAP→lake) — reconciliar/semántica
  cuesta más que la ingesta; **"Beyond Zero Copy"** (jun-2026) — el workload que
  sirve a usuarios vía SAC "debe quedarse compartido, real-time, sin duplicación";
  **Business Model Analyst** — define latencia por necesidad, no sobre-construir;
  además benchmark dbt semantic layer + "cost-per-task" (ver Ideas 1 y 5).

---

### Ranking sugerido
0. **Idea 6** (seed recomendado ⭐⭐) — es la más fuerte de la serie: evidencia
   real de primera persona, tesis de arquitecto + líder de opinión, y a punto de
   producción. Supera a la Idea 1 como semilla porque no depende solo de fuentes
   de terceros: el caso *es* el argumento. Anonimizar con rigor.
1. **Idea 1** — el ángulo más nuevo respecto a W28/W29 y el más opinable;
   encaja con el posicionamiento de líder de opinión y el ancla de experiencia
   SAP (gate de reconciliación) es de las más fuertes de la serie. Buen candidato
   a **segunda mitad** de un papper que abra con la Idea 6.
2. **Idea 2** — la más "de Ricardo" y de decisión real de arquitectura
   (SAP Databricks vs Enterprise Databricks / BW→BDC); noticiosa en la ventana y
   con marcos SAP reconocidos para anclar la tesis.
3. **Idea 3** — opinión anti-hype filosa (chatbots vs agentes); números duros de
   VentureBeat + voz de Benn Stancil; combina bien como sección dentro de la
   Idea 1 si se busca un solo papper.
4. **Idea 4** — gobernanza de identidad agéntica; excelente para pieza de
   liderazgo con paralelo SAP (SoD); distinta del hilo de gobernanza de W29
   (costo/dueño) porque ataca identidad e isolation.
5. **Idea 5** — reserva / autoridad técnica; riesgo de rozar el tema de contexto
   de W28, por eso va al final salvo que se enfoque puro en runtime → compile-time.

_Nota de verificación de fuentes: todas las URLs citadas provienen de resultados
de búsqueda web reales de esta sesión, con fecha de publicación visible.
**Publicadas en la ventana estricta (13–20 jul):** las tres de VentureBeat
(evaluation gap 16-jul, orchestration 15-jul, security gap 16-jul), Databricks
"Unified context" (16-jul), las release notes de Databricks July 2026 (20-jul,
incluye Secrets en UC y conectividad privada a BDC del 9-jul), Jaehyeon Kim
(18-jul), Benn Stancil "Be a winner" (10-jul, actualizado en ventana) y Colrows
(actualizado 11-jul). **Vigentes/recientes pero fuera de la ventana estricta:**
SAP Insider "SAP Databricks vs Enterprise Databricks" (8-jul), philliant
(8-jul), Databend "Trace is Evals" (2-jul), VentureBeat GPUs (10-jul, act.
14-jul), Unity Catalog DAIS (16-jun), semantic metadata sync SAP (30-abr), DPG
blogs de SAP (feb), benchmark dbt (abr), Benn Stancil "token path" (5-jun),
Seattle Data Guy (13-jun). **No verificado / no citado con URL:** los posts de
SAP Community "Accessing BW Data Products in the Query Layer of SAP BW/4HANA PCE
in BDC" y "Architecture Deep-Dive: Transforming SAP BW with SAP BDC" aparecen en
los listados de la ventana (~17–19 jul) pero no pude confirmar sus URLs directas,
así que NO las cité para no inventar el link (mismo criterio que W29 con este
mismo post)._
