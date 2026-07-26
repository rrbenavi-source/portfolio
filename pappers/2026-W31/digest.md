# Digest 2026-W31

_Barrido dirigido — ventana 2026-07-20 → 2026-07-26, más evergreen 2025-2026.
Tema pedido por Ricardo: **migrar reportes SAP (estándar y Z) y modelos BW a
lakehouses (Databricks/Snowflake) — actualidad y mejores prácticas**, anclado en
el POC real IEPS/RTDs (ECC → Databricks). Fuentes: SAP Notes/Community,
Databricks/Snowflake oficial, SAPinsider, CIO.com, BARC, Protiviti + exploración
del repo del POC._

> **Confidencialidad (regla de la casa):** el caso se cuenta anónimo — sin
> cliente, sociedad, marcas, RFCs, UUIDs, importes exactos ni nombres de
> objetos Z. Publicable sin problema: tablas SAP estándar (BKPF/BSEG/BSET,
> VBRK/VBRP, KONV, MVKE…), transacciones, el objeto de archivado `FI_DOCUMNT`,
> tasas de IEPS (son ley), el marco legal (LIEPS Art. 4, Art. 22 CFF) y todas
> las trampas técnicas. Referirse a "un report Z de ~3,000 líneas", "una tabla Z
> de parametrización", "un saldo a favor de nueve cifras en MXN".

> **Tema de la semana:** 2026 es el año en que "sacar el dato de SAP" dejó de
> ser un problema de plomería y se volvió una decisión de arquitectura con
> fecha límite. En junio SAP desplegó el parche que **bloquea técnicamente** las
> llamadas ODP-RFC de aplicaciones no-SAP (Note 3255746, opt-out solo hasta
> **2026-12-31**); en mayo compró **Dremio** para volver BDC un lakehouse
> Iceberg nativo; y las vías "oficiales" zero-copy hacia Databricks (GA
> oct-2025) y Snowflake (GA may-2026) ya están en producción. Mientras el
> mercado discute *cómo extraer*, casi nadie escribe sobre lo que pasa
> *después*: reconstruir la semántica, replicar lógica ABAP de 20 años y
> cuadrar al centavo contra el documento fiscal. Ahí es exactamente donde vive
> el POC de Ricardo — y donde hay hueco editorial real.

---

## Idea 1 — Migrar un reporte Z no es traducir ABAP: es una autopsia  ⭐⭐ (seed recomendado)
- **Formato:** deep-dive / autoridad con caso real (estilo W29/W30)
- **Tesis:** El error de manual al llevar reportes SAP al lakehouse es tratarlo
  como traducción: ABAP entra, PySpark sale. En la práctica es una **autopsia**:
  abres un report Z productivo de ~3,000 líneas y descubres que (a) media docena
  de FORMs existen solo para esquivar limitaciones que el lakehouse no tiene —
  en el caso real, 4 flujos de lectura (archivado/vivo × facturación/no)
  **colapsan a 1**; (b) la mitad de la lógica no está en el código sino en
  **filas de una tabla Z de parametrización** (cuentas, tasas válidas,
  tolerancias) que nadie replicó al lake; (c) hay function modules cuyo código
  fuente **ya no se puede obtener** y toca decidir un fallback documentado; y
  (d) a veces el código no hace lo que aparenta — la navegación de la cadena de
  compensación resultó no ejecutarse nunca en productivo (`AUGBL` vacío), y la
  decisión correcta fue **replicar el comportamiento real, no la intención del
  código**. La postura opinable: el entregable de una migración de reporte no
  es "el mismo reporte en Delta"; es la **decisión explícita y documentada de
  qué lógica vive, qué lógica muere y qué lógica nunca estuvo viva**. Quien
  promete "migración automática de reportes Z" no ha abierto uno.
- **Por qué ahora:** BW 7.5 sale de mantenimiento mainstream a **fines de 2027**
  (extendido 2030) y Protiviti (abr-2026) pone número al replatforming a
  plataforma no-SAP: **"3–4 veces más esfuerzo"** que las rutas SAP — el
  esfuerzo está justo en preservar lógica de negocio compleja. Con la puerta
  ODP-RFC cerrándose el 31-dic-2026 (ver Idea 3), miles de shops SAP están
  decidiendo *este año* qué migra y qué muere.
- **Ángulo de Ricardo:** primera mano total. El catálogo de hallazgos del POC es
  oro publicable: rangos SIGN/OPTION/LOW/HIGH sin equivalente Spark, el patrón
  `CP` `'131*4'` → `LIKE '131%4'`, `AUTHORITY-CHECK` que se vuelve Unity
  Catalog + row-level security, `OPEN DATASET` que se vuelve write a Volume, y
  el método serio: spec source-to-target de 33 columnas + **TDD con golden case**
  (un número esperado fijo como no-regresión) antes de tocar producción.
  Mensaje de liderazgo: la migración se gana en la especificación (eco directo
  de W29 "el diseño es la migración" — esto es la secuela natural).
- **Fuentes:**
  - https://tcblog.protiviti.com/2026/04/21/moving-beyond-sap-bw-the-real-options-analytics-leaders-are-weighing-in-2026/ — (21-abr-2026, verificada) las 5 rutas de salida de BW; replatforming no-SAP = 3-4× esfuerzo; el obstáculo #1 es la lógica de negocio compleja.
  - https://barc.com/end-of-maintenance-sap-bw/ — (analista neutral, evergreen) fechas EoM: BW 7.5 fin de 2027 / extendido 2030; BW/4HANA hasta 2040. _(URL de listado de búsqueda; verificar link directo antes de citar en el draft.)_
  - https://community.sap.com/t5/technology-blog-posts-by-members/the-sap-bw-migration-decision-your-real-options-in-2026/ba-p/14359306 — (SAP Community, 2026) el debate de opciones dentro de la propia comunidad. _(no abierta; verificar antes de citar)_
  - Caso propio (anónimo): report Z FI de evidencias de archivado ~3,000 líneas → tabla Delta + Power BI; spec de emulación de 33 columnas; hallazgos de la autopsia listados arriba.

## Idea 2 — El cuadre contra el CFDI no es el paso final de la migración: es la migración
- **Formato:** opinión / autoridad con caso (el más "fiscal" de los cinco)
- **Tesis:** Un cálculo fiscal replicado en el lakehouse no es válido porque el
  job corrió en verde; es válido cuando **cuadra al centavo contra el documento
  legal**. Y el árbitro no es SAP: es el CFDI timbrado — porque el SAT ya opera
  su propia analítica sobre la base nacional de CFDIs y cruza lo facturado
  contra lo declarado. Tu lakehouse tiene que cuadrar contra el de ellos, no al
  revés. La postura opinable: en dominio fiscal, la reconciliación de tres vías
  (réplica ↔ contabilidad SAP ↔ comprobante fiscal) **es el proyecto**; la
  extracción y el cómputo son el andamio. Un match del "99.9%" no es un éxito
  de migración, es un hallazgo de auditoría.
- **Por qué ahora:** evergreen con percha de caso: en el POC, la validación
  por UUID contra CFDIs reales dio 3 documentos exactos **al centavo** (valida
  el pipeline end-to-end), 6 parciales explicables por diseño, y 6
  inconsistencias reales — IEPS causado que el CFDI nunca trasladó,
  concentrado en un mismo receptor (problema sistémico de configuración, no
  errores dispersos). El cuadre no confirmó el cálculo: **encontró el
  hallazgo de negocio que justificaba todo el POC**.
- **Ángulo de Ricardo:** la mejor historia del caso es un fallo instructivo: una
  consulta con grano por documento (material representativo vía `min(MATNR)` +
  filtro de grupo de material) dejaba fuera facturas multi-SKU completas —
  **~57% del importe real invisible sin ser un error de cálculo**: la lógica era
  correcta, la *unidad de análisis* estaba mal. Solo se detectó exportando
  BKPF/BSEG/BSET de un documento real y sumando a mano. Lección value-driven:
  control totals por documento contra BSET (`HWSTE`/`HWBAS`) antes de agregar
  nada, y reglas determinísticas + Delta time travel como cadena de evidencia
  auditable (decisión explícita del POC: nada de ML donde el SAT puede
  preguntar "¿por qué este peso?").
- **Fuentes:**
  - https://help.sap.com/docs/ABAP_PLATFORM_NEW/f1afe2b5ff9d4b5d82d2c58051ffefc5/4a12e8f576df1b42e10000000a42189c.html — (SAP Help oficial, evergreen) Data Reconciliation: el estándar BW de comparar totales del target contra lectura directa del source. _(URL de listado; verificar antes de citar)_
  - https://www.edifact.com.mx/blog/conciliacion-de-cfdi-nueva-herramienta-del-sat-para-fortalecer-la-transparencia-fiscal/ — (mercado MX) el SAT concilia CFDIs vs declaraciones con su propia analítica. _(evidencia de mercado, no autoridad; verificar)_
  - https://www.vertexinc.com/solutions/products/vertex-vat-compliance — (vendor, solo como evidencia de mercado) los tax engines ya asumen matching automático e-invoice ↔ GL ↔ declaración.
  - Marco legal citable: LIEPS Art. 4 fr. IV (acreditamiento por misma clase de bien), Art. 22 CFF (5 años de prescripción).
  - Caso propio (anónimo): validación por UUID contra CFDIs timbrados; categorías A/B/C; el error de grano del 57%.

## Idea 3 — SAP ya te cerró la puerta trasera: te quedan 5 meses para decidir arquitectura
- **Formato:** actualidad / servicio ("qué hacer antes del 31 de diciembre")
- **Tesis:** La Note 3255746 dejó de ser letra chica: desde el parche de
  **junio 2026**, las llamadas ODP-RFC de aplicaciones no-SAP se **bloquean
  técnicamente** (check de subscriber type en cada llamada), con opt-out
  temporal solo hasta el **2026-12-31**. Años de pipelines third-party
  (Fivetran/Theobald/ADF vía ODP-RFC) se volvieron deuda con fecha de
  caducidad. La postura opinable: no lo trates como un problema de conectores
  ("¿qué herramienta sigue funcionando?") sino de arquitectura: la vía
  soportada ya no es *replicar más duro*, es decidir entre **compartir sin
  copiar** (BDC Connect zero-copy) o extraer por las rutas compliant asumiendo
  su costo (ODP OData es más lento — lo admite el propio Databricks;
  Replication Flows de Datasphere cuesta licencia). Quien llegue a diciembre
  sin haber corrido el auto-diagnóstico (Note 3439624) va a decidir en pánico.
- **Por qué ahora:** es lo más fresco y accionable de la ventana: SAPinsider
  publicó la guía de la deadline el **2026-07-02**; el parche está ligado a un
  CVE de 2026; y la herramienta de auto-diagnóstico está disponible desde
  abril. Al publicar el 28-jul quedan exactamente 5 meses de opt-out.
- **Ángulo de Ricardo:** checklist de arquitecto, no de vendor: (1) audita tu
  uso real de ODP-RFC con la Note 3439624; (2) clasifica pipelines por vía de
  extracción (el bloqueo es a ODP-RFC, no al RFC como protocolo — table CDC,
  CDS views y BW cubes por otras vías siguen compliant); (3) decide replicar
  vs compartir por workload, no por inercia. Conecta con el caso: el POC usó
  extractores ODP *dentro* del stack SAP (BW como conducto) — exactamente el
  uso que sigue permitido; el punto es saber cuál eres tú.
- **Fuentes:**
  - https://sapinsider.org/blogs/sap-note-3255746-odp-rfc-deadline-2026/ — (2-jul-2026, verificada, en ventana editorial) cronología completa: v4 feb-2024 "unpermitted", parche jun-2026, opt-out 31-dic-2026, Note 3439624.
  - https://community.databricks.com/t5/technical-blog/navigating-the-sap-data-ocean-demystifying-sap-data-extraction/ba-p/94617 — (oficial Databricks Community, oct-2024, verificada) Databricks mismo recomienda Replication Flow y admite el trade-off compliance vs eficiencia de ODP OData.
  - https://community.sap.com/t5/technology-blog-posts-by-members/sap-s-new-api-policy-is-quietly-rewriting-the-bw-roadmap/ba-p/14441607 — (SAP Community; existe pero tras login) "SAP's New API Policy Is Quietly Rewriting the BW Roadmap" — señal de debate interno.
  - https://theobald-software.com/en/blog/sap-note-3255746 — (vendor, solo evidencia de mercado) qué rutas third-party siguen compliant. _(no abierta; verificar)_

## Idea 4 — Zero-copy no es zero-lock-in: solo cambió de lugar el candado
- **Formato:** opinión estratégica / anti-hype
- **Tesis:** La secuencia 2025-2026 es elegante: SAP cierra ODP-RFC, abre BDC
  Connect zero-copy hacia Databricks (GA oct-2025) y Snowflake (GA may-2026)…
  y en mayo **compra Dremio** para volver BDC un lakehouse Iceberg nativo,
  quedándose con la capa semántica y el formato. El zero-copy es real y
  técnicamente superior a las copias CSV que reemplaza — pero la neutralidad es
  narrativa: **el dato ya no se copia; la dependencia sí**. Databricks y
  Snowflake quedan posicionados como backend computacional mientras la
  semántica (lo que de verdad cuesta reconstruir) vive en BDC, que es SaaS con
  su licencia. La postura opinable: "¿replico o comparto?" es en realidad
  "¿de quién quiero depender y en qué capa?" — y la respuesta correcta se
  decide por workload, no por keynote.
- **Por qué ahora:** el mercado sigue digiriendo Dremio (comprada 2026-05-04,
  el mismo día de la GA de Snowflake+BDC); los analistas ya dijeron la parte
  incómoda: hacia H1-2027 "SAP dirigirá las nuevas cargas AI hacia BDC
  independientemente de lo que digan los comunicados de partnership"
  (Constellation/CIO); BARC lee a Databricks acotado a "ML workbench" en
  estates SAP-céntricos. Continuación natural de la Idea 2 del digest W30
  (SAP Databricks vs Enterprise Databricks) con la pieza que faltaba.
- **Ángulo de Ricardo:** el arquitecto que opera *ambos* mundos: qué preserva
  el zero-copy (bytes, tags de gobierno, algo de metadata semántica vía Delta
  Sharing/CSN) y qué **no** te da nadie: la lógica de determinación fiscal,
  las conversiones, el cuadre. Ecos de W30 (data gravity, el último
  kilómetro). Anti-humo puro: ni "SAP te encierra" ni "el lakehouse te
  libera" — factura y contrato en la mano.
- **Fuentes:**
  - https://www.cio.com/article/4166881/sap-to-acquire-data-lakehouse-vendor-dremio.html — (4-may-2026, verificada, medio neutral) compra de Dremio; BDC como lakehouse Iceberg; quote de analista sobre H1-2027.
  - https://www.databricks.com/blog/announcing-general-availability-sap-business-data-cloud-connect-databricks — (6-oct-2025, verificada, oficial) GA de BDC Connect for Databricks: zero-copy bidireccional vía Delta Sharing.
  - https://docs.snowflake.com/en/release-notes/2026/other/2026-05-04-Snowflake-SAP-zerocopy-integration — (4-may-2026, verificada, doc oficial Snowflake) GA: data products SAP como databases catalog-linked; Semantic Views desde SAP CSN.
  - https://barc.com/perspective-on-saps-dual-acquisition-of-prior-labs-and-dremio/ — (BARC, analista neutral) la lectura de mercado post-Dremio. _(URL de listado; verificar antes de citar)_
  - https://news.sap.com/2025/11/sap-snowflake-new-data-fabric-innovations-sap-bdc-sap-hana-cloud/ — (oficial SAP, nov-2025) anuncio del partnership Snowflake. _(verificar link directo)_

## Idea 5 — El lakehouse no tiene tu historia: lo que nadie cuenta de los datos archivados
- **Formato:** deep-dive técnico / trinchera
- **Tesis:** Toda réplica SAP → lakehouse nace con un hueco que ningún conector
  menciona: **los datos archivados no están**. Si SARA ya corrió (en el caso:
  `FI_DOCUMNT` sobre los ejercicios 2021-2022), esos documentos no existen en
  la réplica — pero la ley sí los exige (Art. 22 CFF: 5 años). La ironía
  publicable: para llenar el lakehouse **hubo que escribir ABAP nuevo** — tres
  extractores genéricos expuestos por ODP que entregan la unión de online +
  archivado, reutilizando el mismo patrón de lectura del archivo que los
  reportes Z productivos ya usaban. Y las trampas de ahí abajo no las cuenta
  ningún whitepaper: índices secundarios (BSID/BSAD) que no se replican y hay
  que reconstruir desde BSEG; la **ventana de extracción por fecha contable vs
  la ventana de negocio por fecha de compensación** (documentos contabilizados
  antes del corte y cobrados después simplemente no están — no es un bug, es
  una dimensión distinta); fechas de compensación corruptas en el archivo que
  resultaron ser documentos aún vivos en ECC; y la solución final: un query
  híbrido que **cose la réplica viva con la archivada** del mismo sistema en
  distinto estado de ciclo de vida.
- **Por qué ahora:** evergreen, pero pega con la ola de decomisos: cada
  migración BW→lakehouse y cada brownfield a S/4 deja atrás un archivo SARA, y
  la retención legal no migra sola. Nadie está escribiendo esto desde la
  trinchera; es hueco editorial verificado (el barrido no encontró ni una
  guía oficial Databricks/Snowflake sobre archived data de SAP).
- **Ángulo de Ricardo:** el catálogo de fricciones reales del POC: `NOT IN` con
  NULLs que descarta todas las filas, formato de `BUKRS` inconsistente entre
  réplicas ('083' vs '0083'), `MATNR` con ceros a la izquierda rompiendo
  joins, listas hardcodeadas de cuentas que cambian por ejercicio, el divisor
  de `KBETR` (265.0 = 26.5%), y BSEG guardando solo la última compensación
  (adiós historial de parcialidades → decisión de grano documentada). Mensaje:
  la calidad de la réplica no se hereda, se verifica — "paso 0 de sanidad"
  antes de cualquier cálculo.
- **Fuentes:**
  - Doc oficial SAP de archivado FI (`FI_DOCUMNT`, SARA) y Data Reconciliation (Idea 2) como marco.
  - https://community.databricks.com/t5/technical-blog/navigating-the-sap-data-ocean-demystifying-sap-data-extraction/ba-p/94617 — (verificada) el mapa oficial de vías de extracción, donde el archivo brilla por su ausencia.
  - Caso propio (anónimo): extractores Z ODP para archivo + réplica; consultas de diagnóstico de embudo; query híbrido vivo+archivado.
  - _Nota honesta para el draft:_ la recuperación completa del histórico seguía en diagnóstico al corte del POC — no prometer resultados no medidos (regla de W30).

---

## Recomendación de seed

**Idea 1** (⭐⭐, la autopsia del reporte Z) como cuerpo principal: es la
respuesta directa al tema pedido, es 100% de primera mano, es la secuela
natural de W29 ("el diseño es la migración") y no existe nada igual publicado.
**Percha de actualidad:** abrir o cerrar con la deadline de la Idea 3 (ODP-RFC,
opt-out expira 31-dic-2026, pieza de SAPinsider del 2-jul) para que el artículo
tenga "por qué esta semana". Las Ideas 2 y 5 son spin-offs fuertes para
semanas futuras (W32+) — el caso da para una mini-serie de migración SAP →
lakehouse. La Idea 4 es el backup estratégico si se prefiere opinión pura sin
caso.

## Notas de verificación de fuentes

Las URLs marcadas "verificada" fueron abiertas y confirmadas (contenido +
fecha) durante el barrido. Las marcadas "_(verificar)_" aparecieron en
resultados de búsqueda con título/resumen consistente pero **no se abrieron**
— confirmar el link directo antes de citarlas en el draft (regla W30: no
inventar links). La pieza de SAP Community sobre la API policy existe pero
está tras login wall.
