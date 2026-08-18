# Digest 2026-W34

Barrido: domingo 16-ago-2026 (ventana 09-ago → 16-ago, con arrastre de julio donde el
hilo lo pedía).
Edición objetivo: **07** del newsletter Brújula, martes **18-ago-2026**.

> Notas del barrido:
> - LinkedIn feed (fuente `news`) sigue sin ser accesible desde aquí — omitido.
> - Semana **fuerte** en anuncios, al revés que W33. Hay tres movimientos grandes y
>   verificables contra fuente primaria: Databricks activó su ontología por defecto,
>   SAP cerró la compra de Dremio, y el estándar abierto de capa semántica entró a la
>   Apache Software Foundation.
> - **Verificación hecha en este barrido, no heredada:** leí directo el
>   `core-spec/spec.md` de `apache/ossie` (v0.2.0.dev0) y las release notes oficiales de
>   Databricks de agosto. Los dos hallazgos centrales de la Idea 1 están sostenidos en
>   fuente de primera parte, no en blogs de analistas.
> - Queda **resuelto** el pendiente que marcó el digest W33 sobre el AI Act: ya no es
>   propuesta, es reglamento publicado (ver Idea 5).

---

## Idea 1 — Estandarizaron el diccionario, no la autoridad ⭐

- **Formato:** opinión
- **Tesis:** en un mismo tramo de semanas, cuatro actores que compiten entre sí
  declararon exactamente lo mismo: **la capa de significado es el producto.**
  - **10-jul-2026:** Open Semantic Interchange entra al Apache Incubator y se renombra
    **Apache Ossie** — el formato neutral, en JSON/YAML, para intercambiar métricas,
    dimensiones y relaciones entre herramientas. De 17 socios iniciales a **más de 50
    organizaciones**, entre ellas Snowflake **y** Databricks a la vez.
  - **06-ago-2026:** Databricks **activa la Genie Ontology por defecto** para todos.
  - **12-ago-2026:** Databricks publica **Pages**, que da a cada término de negocio,
    acrónimo y KPI "una sola definición gobernada" y que sus propias notas describen
    como *"the human-modeled layer of the Genie Ontology"* — la capa modelada por
    humanos.
  - **06-jul-2026 (confirmado el 14-ago por analista):** SAP **cierra la compra de
    Dremio** y planea usar su Open Catalog —construido sobre Apache Polaris y el
    Iceberg REST Catalog API— como la capa de descubrimiento **y semántica** de
    Business Data Cloud, y como base del SAP Knowledge Graph.
  - Y Microsoft ya tenía **Fabric IQ** en disponibilidad general desde junio, con
    semantic models más ontologías.

  El giro que lo hace nuestro está en lo que **el estándar no tiene**. Leí el core spec
  de Ossie completo. Estandariza `datasets`, `fields`, `relationships`, `metrics`, un
  `ai_context` de texto libre para el modelo y un `custom_extensions` para lo que no
  cupo. No existe —en ningún objeto, en ninguna versión del borrador— campo para
  **linaje, procedencia, frescura, confianza, ni quién aprobó la definición y contra
  qué la verificó**. La definición viaja entre herramientas; la responsabilidad de
  haberla firmado, no.

  Y del otro lado, los vendors sí prometen resolver la confianza, pero **por
  inferencia**: el blog de Databricks de junio explica que la Genie Ontology decide qué
  definición manda con "un enfoque similar a PageRank" —de dónde vino, qué tan
  autoritativo es el autor, cuánta gente la usa, qué tan fresca es— y remata que así
  resuelve el problema de contexto *"without asking your teams to hand-curate it"*, sin
  pedirle a tus equipos que la curen a mano. Seis semanas después, la misma empresa
  publicó la capa curada a mano. Las dos cosas pueden ser ciertas al mismo tiempo; lo
  que no se sostiene es venderlas como si la segunda no hiciera falta.

  Aterrizaje: la pregunta de la edición 05 —**¿con la semántica de quién?**— acaba de
  recibir su respuesta de la industria. Con la de quien la escribió primero, la
  escribió más seguido, o la escribió con más rango. Ninguno de esos tres es lo mismo
  que "la correcta", y ningún formato de intercambio guarda cuál fue.
- **Por qué ahora:** gancho de calendario **muy fuerte y verificable al día**: los tres
  hitos caen entre el 6 y el 14 de agosto, y el cuarto (Ossie) es de hace cinco
  semanas. Nadie ha escrito todavía la lectura conjunta, y menos con el spec abierto en
  la mano.
- **Riesgo a vigilar:** es la **cuarta pieza** del arco semántico (02 → 04 → 05 → 06).
  Se resuelve si el papper **no** vuelve a explicar qué es un semantic layer —eso ya se
  hizo en la 05— y se va directo a lo nuevo: la gobernanza de la definición como
  artefacto que se exporta. Segundo riesgo: sonar anti-Databricks. No lo es; el
  hallazgo es que **el propio vendor** entregó la capa humana, que es exactamente lo
  que veníamos diciendo. Hay que decirlo así, sin sarcasmo.
- **Fuentes:**
  - https://github.com/apache/ossie/blob/main/core-spec/spec.md — **core spec de Apache
    Ossie v0.2.0.dev0 (DRAFT). Fuente primaria, neutral (ASF), leída completa en este
    barrido.** De aquí sale la afirmación de los campos ausentes; es verificable con
    una búsqueda de texto en el spec.
  - https://ossie.apache.org/updates/ossie-enters-apache-incubator/ — anuncio de la
    incubación, gobernanza y lista de contribuyentes (Snowflake, Dremio, Salesforce,
    Databricks, dbt Labs, RelationalAI, GoodData, Honeydew; 17 → 50+ organizaciones).
    ⚠️ **Discrepancia menor a resolver:** el blog de Snowflake que replica el anuncio
    está fechado **08-jul-2026** y un análisis secundario da **10-jul-2026** como fecha
    de entrada al incubator. Usar "julio de 2026" o confirmar en el sitio de la ASF.
  - https://docs.databricks.com/aws/en/release-notes/product/2026/august — **release
    notes oficiales de Databricks, agosto 2026.** De aquí salen las fechas y el texto
    literal de *Pages* (12-ago) y de la ontología activada por defecto (06-ago). Las
    notas de AI/BI añaden *ontology snippets* para todos los clientes el 13-ago.
  - https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents
    — blog de Databricks, 16-jun-2026. De aquí salen el mecanismo tipo PageRank y la
    frase "without asking your teams to hand-curate it". Es fuente de vendor y se cita
    **como declaración del vendor sobre sí mismo**, que es el único uso legítimo aquí.
  - https://news.sap.com/2026/07/sap-completes-dremio-acquisition/ — **nota oficial
    SAP**, cierre de la adquisición el 06-jul-2026.
  - https://www.arcweb.com/blog/sap-completes-dremio-acquisition-expand-business-data-cloud-agentic-ai
    — ARC Advisory Group (analista, 14-ago-2026): el rol de Open Catalog / Apache
    Polaris como capa semántica y de linaje dentro de BDC, y su aporte al SAP Knowledge
    Graph. ⚠️ Es lectura de analista sobre planes anunciados; escribir "SAP plantea",
    no "SAP ya tiene".
  - https://docs.getdbt.com/docs/build/ossie-semantic-models — dbt Developer Hub,
    30-jul-2026. dbt Core 1.12+ lee documentos Ossie, pero **solo acepta las versiones
    0.1.0 y 0.1.1** del spec —cualquier otra cadena de versión provoca error de
    parseo— mientras el spec va en 0.2.0.dev0; y los constructos no soportados se
    **descartan con una advertencia** y el parseo continúa. Dato durísimo y primario:
    el consumidor más importante del estándar y el estándar ya divergieron.

## Idea 2 — SAP compró el catálogo, no el motor

- **Formato:** deep-dive
- **Tesis:** la lectura fácil de SAP–Dremio es "SAP compró un lakehouse abierto". La
  lectura que importa para quien hoy vive de BW es otra: lo que SAP integra como pieza
  estructural es el **Open Catalog** (Apache Polaris + Iceberg REST Catalog API) para
  que motores SAP y no-SAP compartan significado de negocio, relaciones, permisos y
  linaje, alimentando el Knowledge Graph. Es decir, SAP está resolviendo por compra el
  mismo problema que el Data Product Generator dejaba abierto: mover objetos no mueve
  la semántica. Y confirma la dirección del embudo: Datasphere, SAC, HANA Cloud,
  Databricks, Snowflake y ahora Dremio, todos dentro de BDC.
- **Por qué ahora:** el cierre es del 06-jul y la lectura de analista independiente es
  del **14-ago**, o sea de esta semana. Es el tema donde Ricardo tiene la ventaja más
  grande sobre cualquiera que escriba de esto.
- **Riesgo a vigilar:** exige verificar qué está **anunciado** contra qué está
  **disponible**. Casi todo lo de Dremio dentro de BDC es plan, no GA. Un deep-dive
  aquí obliga a un párrafo explícito de "esto todavía no existe en tu tenant".
- **Fuentes:**
  - https://news.sap.com/2026/07/sap-completes-dremio-acquisition/ — nota oficial SAP.
  - https://news.sap.com/2026/05/sap-to-acquire-dremio-unify-sap-and-non-sap-data-power-agentic-ai/
    — anuncio original de mayo, con el racional declarado.
  - https://www.arcweb.com/blog/sap-completes-dremio-acquisition-expand-business-data-cloud-agentic-ai
    — ARC Advisory, 14-ago-2026.
  - https://architecture.learning.sap.com/docs/ref-arch/6550e4 — SAP Architecture
    Center: modernización de BW con BDC, Data Product Generator, Query Template
    Generator (planeado) y BW Migration Assistant. Fuente SAP oficial y accesible
    (a diferencia de SAP Community, que sigue devolviendo 403).

## Idea 3 — El agente que sabe decir "no sé"

- **Formato:** opinión
- **Tesis:** un preprint de agosto propone lo que llevamos tres ediciones rondando:
  dejar de calificar a los agentes analíticos por **exactitud de SQL** y calificarlos
  por **verdad de negocio**. Su benchmark, WarehouseReliabilityBench, tiene 400 tareas
  congeladas en las que **aproximadamente la mitad de las respuestas correctas no son
  un número, sino una aclaración, una abstención o un rechazo** —porque la pregunta
  tenía dos lecturas válidas, el warehouse no podía contestarla, o la columna quedó
  obsoleta tras un cambio de esquema. El agente propuesto no es más grande: es un
  modelo de 7B con reglas derivadas del semantic layer y verificación determinista
  después de ejecutar. Contra un modelo de 32B con prompt directo, la tasa de "éxito
  falso" —queries que corren, devuelven un número creíble y están mal— cae de 0.754 a
  0.351 de las respuestas entregadas.
- **Por qué ahora:** es de agosto de 2026 y nombra con precisión el modo de falla caro:
  el número plausible y equivocado que llega al dashboard sin que nada avise.
- **Por qué NO como papper principal esta semana:** el sustento es **débil por diseño y
  el propio autor lo dice**: investigador independiente, sin revisión por pares,
  warehouses sintéticos, split de prueba de 80 tareas evaluado una sola vez, y al
  remuestrear familias de plantillas los intervalos de confianza incluyen cero. Además
  el componente aprendido de confianza no transfirió y no se hizo ablación por
  componente. Citar sus cifras como si fueran evidencia dura contradiría
  [[feedback-papper-sourcing]]. **Uso recomendado: un párrafo dentro de la Idea 1**,
  citado como formulación del problema y no como medición.
- **Fuentes:**
  - https://arxiv.org/abs/2608.09254 — *Business Truth, not SQL Accuracy: A Rule-Gated
    7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline*. Morris Lee
    (investigador independiente), ago-2026. Preprint.

## Idea 4 — Cada agente con su propia base de datos

- **Formato:** opinión
- **Tesis:** el martes 11-ago Databricks anunció la compra de Electric (PGlite, un
  Postgres completo compilado a WebAssembly, y su motor de sincronización). El equipo
  se suma a Neon. El dato que sostiene la compra, publicado por la propia Databricks:
  en Lakebase **los agentes crean alrededor de cuatro veces más bases de datos que los
  usuarios humanos**, el proyecto promedio carga unos 10 branches de base, y en cierto
  tipo de aplicaciones el cómputo promedio de una base **vive menos de diez segundos**.
  El ángulo de arquitectura: la gobernanza que dimos por resuelta es la del warehouse
  central; el estado que vive dentro del sandbox de un agente —qué dato se materializó
  ahí, quién lo puede ver, cuándo se destruye, cómo se audita— no está resuelto en
  ningún lado. Varios analistas citados en la cobertura dicen exactamente eso.
- **Por qué ahora:** anuncio de esta semana, con cobertura independiente.
- **Por qué NO esta semana:** desplaza el foco de la audiencia de Brújula (decisión y
  arquitectura de datos) hacia infraestructura de aplicaciones. Es mejor idea para una
  semana sin noticia semántica, o como pieza de continuidad si la Idea 1 abre el tema
  de gobernanza del contexto.
- **Fuentes:**
  - https://thenewstack.io/databricks-electric-wasm-agentic-postgres/ — The New Stack,
    11-ago-2026.
  - https://www.infoworld.com/article/4209184/databricks-acquires-electric-to-bring-local-postgres-databases-to-agentic-apps.html
    — InfoWorld, 13-ago-2026, con las advertencias de gobernanza de analistas externos.

## Idea 5 — El AI Act ya no es propuesta (cierra un pendiente de W33)

- **Formato:** nota de seguimiento, no papper
- **Qué cambió:** el digest de W33 dejó marcado como "por verificar" el estatus del
  Digital Omnibus. Ya se resolvió: el reglamento se publicó en el Diario Oficial el
  **24-jul-2026** y entró en vigor el **27-jul-2026**. El diferimiento de las
  obligaciones de alto riesgo del Anexo III al **02-dic-2027** —y del Anexo I al
  **02-ago-2028**— es derecho vigente, no propuesta.
- **Uso recomendado:** un solo párrafo de cierre si hace falta, exactamente como
  proponía W33. No da para papper propio: sigue siendo tema regulatorio y el papper se
  vuelve pieza de compliance.
- ⚠️ **Antes de citar:** confirmar la referencia exacta del reglamento en EUR-Lex. Las
  fuentes disponibles en este barrido son despachos legales (Lewis Silkin, K&L Gates,
  Gibson Dunn, Cooley) y una nota de la Cloud Security Alliance, todas secundarias.
  Coinciden en fechas, pero la cita debe ir al Diario Oficial.

---

## También pasó (registro, sin idea propia)

- **10-ago:** Progress Software acuerda comprar los activos de la plataforma de AI y
  data products de **Domo** por 400 millones de dólares (cierre esperado antes del
  30-nov-2026).
- **13-ago:** **Dynatrace** acuerda comprar **Arize** por 915 millones de dólares —
  evaluación y observabilidad de agentes de IA. Tercera compra del año de Dynatrace en
  esa dirección; Cisco compró Galileo en abril. La categoría "medir si tu agente sirve"
  se está consolidando por adquisición.
- **~01-ago:** **Apache Iceberg 2.0** — predicate indexes, deletes seguros para
  streaming y APIs de compactación/retención.
- **05-ago (beta):** **Lakehouse Real-Time** de Databricks, SQL serverless de baja
  latencia y alta concurrencia. Continuidad con la edición 03; guardar.

---

## Ranking sugerido

1. **Idea 1 — Estandarizaron el diccionario, no la autoridad.** La mejor por mucho.
   Gancho de calendario de esta semana, evidencia primaria y verificable —el spec
   abierto y las release notes del propio vendor—, y cierra con nombre y apellido la
   pregunta que dejó abierta la edición 05. Es además el tipo de hallazgo que nadie
   consigue sin abrir el archivo: la ausencia de cuatro campos en un estándar.
2. **Idea 2 — SAP compró el catálogo.** Máxima autoridad propia y gancho decente, pero
   pide deep-dive y una separación disciplinada entre anunciado y disponible. Guardarla
   para cuando haya tiempo de escribirla bien.
3. **Idea 4 — Cada agente con su propia base de datos.** Fresca y bien sostenida, pero
   fuera del centro editorial de Brújula.
4. **Idea 3 — El agente que sabe decir "no sé".** No como papper: como párrafo.
5. **Idea 5 — AI Act.** Nota de seguimiento.

## Combinación recomendada

Idea 1 como papper, con **un párrafo de la Idea 3** para nombrar el modo de falla —el
número plausible y equivocado que nadie detecta— citando el preprint como formulación
del problema, con su limitación dicha en la misma oración. Y **una sola línea de la
Idea 5** al cerrar: a partir de diciembre de 2027 alguien te va a pedir demostrar de
dónde salió cada número, y el formato con el que hoy exportas tus definiciones no
guarda esa información.

El borrador semilla de esta combinación está en `draft-es.md`.
