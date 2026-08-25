# Digest 2026-W35

Barrido: viernes 21-ago-2026. **Barrido dirigido, no general**: Ricardo fijó el eje antes de
investigar (lección de W33 y W34, donde el barrido genérico se tiró completo dos veces).
Edición objetivo: **08** del newsletter Brújula, martes **25-ago-2026**.

**Tema pedido:** la evolución de **SAP BW/4HANA a SAP Business Data Cloud (BDC)** — ventajas,
desventajas y un **roadmap** pensado desde una arquitectura real y vigente.

> Notas del barrido:
> - Se abrieron fuentes primarias, no resúmenes: SAP Architecture Center (ref-arch 6550e4),
>   learning.sap.com, el FAQ oficial de BDC, la documentación de Databricks para el conector
>   BDC (actualizada el **04-ago-2026**), el PDF de precios presentado a los user groups y el
>   reporte de benchmark de SAPinsider (Q1-2026).
> - **La regla de confidencialidad manda** ([[feedback-papper-editorial]]): la arquitectura de
>   referencia se describe de forma **anónima** — "una operación de consumo masivo con
>   BW/4HANA 2023 on-premise, SAC, Analysis for Office, BPC y un Databricks propio en Azure".
>   Nunca el nombre del cliente ni de la sociedad.
> - **Registro de audiencia** ([[feedback-papper-audiencia]]): el eje pedido —pros, contras y
>   roadmap— es literalmente una conversación de presupuesto y de contrato. Esta edición se
>   escribe para quien firma, no para quien configura.
> - Hallazgo que reordena todo el tema y que **no está en ningún blog de partner**: el reloj de
>   2027 que se usa para vender BDC **no es el reloj de un cliente BW/4HANA**. Ver Idea 1.

---

## Idea 1 — El reloj de 2027 no es tu reloj ⭐

- **Formato:** opinión / autoridad (2–3 páginas), con sección de roadmap.
- **Tesis:** casi todo el material de venta de BDC —de SAP y de sus partners— se apoya en una
  fecha: **el 31-dic-2027**, fin del mantenimiento mainstream de **SAP BW NetWeaver 7.5**. Es
  una urgencia real y enorme: en Sapphire 2025, el propio product management de SAP habló de
  **entre 20,000 y 30,000 clientes** todavía corriendo BW 7.5. Para ellos, mover el sistema a
  **SAP BW, private cloud edition** dentro de BDC compra tres años (mantenimiento hasta
  **2030**) sin proyecto de conversión.

  Pero si ya estás en **BW/4HANA**, esa fecha no te aplica. SAP alineó el mantenimiento de
  BW/4HANA con el de S/4HANA: **hasta finales de 2040**, y ese compromiso cubre el despliegue
  **on-premise**, no solo la private cloud edition. Es decir: **catorce años de pista**. La
  decisión de moverse a BDC deja de ser una respuesta a un vencimiento y pasa a ser lo que
  siempre debió ser — una decisión de arquitectura y de contrato, tomada con calma.

  El giro que hace propia la pieza: cuando quitas la urgencia artificial, las tres preguntas
  que quedan no son técnicas. **(1)** ¿Qué gano yo, hoy, que no pueda conseguir con lo que ya
  pagué? **(2)** ¿Qué le entrego a SAP que hoy es mío —el control del modelo comercial y la
  libertad de mover mis propios datos? **(3)** ¿En qué orden lo hago para no quedar a medio río?
  El papper contesta las tres, en ese orden, y cierra con el roadmap.
- **Por qué ahora:** julio de 2026, SAP consolidó **BTP + BDC + Business Transformation
  Management** bajo una marca nueva, **SAP Business AI Platform (BAIP)**, anunciada en Sapphire
  2026. La plataforma a la que te pedirían migrar **se reorganizó y se renombró hace un mes**.
  Ese solo hecho justifica el consejo central: mover el calendario a tu favor.
- **Riesgo a vigilar:** que se lea como "no te muevas". No es eso. La tesis es **"muévete por
  arquitectura, no por miedo"**, y el papper debe traer un roadmap concreto de tres fases —si
  no, es una columna de opinión sin entregable. Segundo riesgo: sonar anti-SAP con 19 años de
  carrera en SAP encima. Se resuelve con la Idea 3, que documenta lo que SAP **sí** cerró.
- **Fuentes:**
  - https://community.sap.com/t5/technology-blog-posts-by-sap/sap-bw-4hana-to-extend-maintenance-in-alignment-with-sap-business-suite-and/ba-p/13457952
    — **anuncio oficial de SAP**: BW/4HANA se alinea con S/4HANA y se mantiene **hasta 2040**.
  - https://userapps.support.sap.com/sap/support/knowledge/en/2934895 — **KBA 2934895,
    "Maintenance for SAP BW/4HANA"**. ⚠️ **Abrir y citar de aquí las fechas exactas por release**
    antes de escribir; el PAM es la fuente oficial y una nota de mantenimiento mal citada tumba
    la pieza entera.
  - https://architecture.learning.sap.com/docs/ref-arch/6550e4 — SAP Architecture Center,
    "Modernizing SAP BW with SAP Business Data Cloud". Fuente SAP oficial y accesible. De aquí
    salen: BW NetWeaver → private cloud edition con soporte **hasta fin de 2030**; BW/4HANA →
    private cloud edition **hasta 2040**; y el modelo de tres pasos Lift / Shift / Innovate.
  - https://sapinsider.org/analyst-insights/modernizing-sap-bw-the-path-to-business-data-cloud/
    — SAPinsider, 21-may-2025. Dominik Kurz (Senior Director Product Management, BW/4HANA y BW
    Bridge) citado con la cifra de **20,000–30,000 clientes en BW 7.5**. Es la mejor evidencia
    de que el discurso de urgencia existe y de a quién está dirigido.
  - https://sapinsider.org/blogs/sap-sapphire-2026-how-sap-business-ai-platform-consolidates-sap-btp-sap-business-data-cloud-and-sap-business-ai/
    — consolidación BTP + BDC + BTM en SAP Business AI Platform (Sapphire 2026). SAP declara
    que no hay migración forzada y que las inversiones en BTP se conservan.

## Idea 2 — La letra chica del zero-copy ⭐ (núcleo técnico de la pieza)

- **Formato:** sección central del papper, no pieza aparte.
- **Tesis:** *zero-copy* —compartir el dato sin copiarlo— es el argumento estrella de BDC, y
  técnicamente **funciona**: el protocolo **Delta Sharing** expone los *data products* de BDC
  directamente en Databricks, en ambos sentidos, sin pipelines. El problema no es el protocolo.
  Es el contrato.

  La versión de **febrero de 2026** del Supplement de BDC introdujo **BDC Connect** como métrica
  de uso y fijó condiciones para los "Third-Party Connectors": los data products **solo pueden
  usarse dentro de BDC** o en el sistema conectado vía BDC Connect; el conector puede
  materializar (guardar) el data product **solo temporalmente y solo por performance**; **no**
  puede distribuirlo a sistemas posteriores; y **SAP se declara dueño de la propiedad
  intelectual** del data product, licenciando únicamente su uso. La posición declarada de SAP
  —que un dato **enriquecido o transformado** deja de ser data product y ya puede quedarse— es
  justamente la que **no aparece en el texto contractual**.

  Para una casa que ya tiene su propio Databricks, ese párrafo decide la arquitectura entera.
  El lakehouse deja de poder ser lo que hoy es —la capa donde todo aterriza y desde donde todo
  se sirve— y pasa a ser un **consumidor autorizado y no redistribuidor**. Power BI, Tableau o
  cualquier data lake externo quedan del lado equivocado de la frase.

  Y hay un detalle que casi nadie ha leído, y está en la documentación pública de Databricks,
  actualizada el 4 de agosto de 2026: Databricks **puede revelar a SAP** información de uso de
  los workloads que tocan datos compartidos por el conector — volumen de datos de BDC y su
  proporción frente a los no-BDC, fecha y hora, y **el precio efectivo que tu organización paga
  por consumo de Databricks** — "por workload, sin agregar ni anonimizar", para fines de
  facturación y administración. Ahí ya no estamos hablando de arquitectura: estamos hablando de
  quién ve tu estructura de costos con el otro proveedor.
- **Por qué ahora:** el conector es GA, la documentación se actualizó **este mes**, y las
  integraciones brownfield siguen llegando (Snowflake GA en mayo-2026, BigQuery H1-2026,
  Microsoft Fabric H2-2026, Amazon Athena planeada H2-2026). Es exactamente el momento en que
  un arquitecto firma o no firma.
- **Riesgo a vigilar:** **alto, es el punto más delicado del papper.** Se está citando el
  contenido de un contrato a partir de lecturas de terceros. **Regla dura:** escribir "según la
  lectura del Supplement de febrero de 2026 que publican X e Y", nunca "el contrato dice". Y
  cerrar con el consejo que los propios analistas dan: **pídelo por escrito a tu account
  executive antes de diseñar sobre esa premisa.**
- **Fuentes:**
  - https://docs.databricks.com/aws/en/opensharing/sap-bdc/ — **documentación oficial de
    Databricks, última actualización 04-ago-2026.** De aquí salen la mecánica de OpenSharing /
    Delta Sharing (mTLS, OIDC, zero-copy bidireccional) **y** la cláusula de divulgación de
    información de uso a SAP. Fuente de primera parte y verificable con búsqueda de texto.
  - https://medium.com/@mario.defelipe/sap-limits-3rd-party-connectors-for-its-data-platform-bdc-updated-usage-terms-and-conditions-e751709fd0ef
    — Mario Defelipe, 22-feb-2026. Desglose cláusula por cláusula del Supplement v2. ⚠️ Análisis
    individual, no documento oficial; el propio autor recomienda pedir confirmación por escrito.
  - https://expertum.net/sap-bdc-delta-share/ — Expertum, 17-feb-2026. Confirma de forma
    independiente lo mismo, y añade el detalle práctico: para compartir hacia un Databricks
    externo hay que **mover físicamente el dato curado a un espacio HANA Data Lake Files** en
    Datasphere primero; y advierte que violar los términos puede derivar en terminación de
    contrato o penalidades.
  - https://learning.sap.com/courses/mastering-sap-data-architecture/integrating-sap-business-data-cloud-with-databricks
    — SAP Learning (oficial): **BDC Connect for Enterprise Databricks** existe explícitamente
    para "salvaguardar la inversión existente en Databricks". Es el reconocimiento de SAP de que
    este escenario es el común, no la excepción.
  - https://architecture.learning.sap.com/docs/ref-arch/12d55f — SAP Architecture Center, "SAP
    Databricks in SAP BDC": diferencia entre el Databricks **embebido (OEM)** y el **propio**;
    en el propio, cada data product debe compartirse **explícitamente** desde el catálogo.
  - ⚠️ **Pendiente antes de publicar:** localizar el **Supplement / Usage Guidelines oficial de
    BDC** en sap.com y citar de ahí. Si no aparece público, decirlo en el texto — "el documento
    que gobierna esto no es de acceso abierto" es, en sí mismo, un dato del papper.

## Idea 3 — Lo que SAP sí cerró en doce meses (contrapeso honesto)

- **Formato:** sección de "ventajas reales", con arco temporal.
- **Tesis:** la crítica fácil a BDC envejece rápido, y hay que decirlo. En **enero de 2026**, el
  reproche técnico más citado era que los data products viajan en **Parquet**, un formato que
  no lleva semántica: al consumirlos fuera de BDC quedaban nombres técnicos de campo y se perdía
  el contexto de negocio. **Cuatro meses después, el 30-abr-2026**, se anunció la disponibilidad
  general de la **sincronización de metadatos semánticos** entre BDC y Unity Catalog: nombres de
  despliegue, descripciones, llaves primarias y foráneas, y las etiquetas de gobierno del
  namespace `PersonalData` que habilitan control de acceso fino por atributos. BDC sigue siendo
  la fuente única de verdad de esa semántica, y los cambios se reflejan del otro lado.

  Ese es el patrón honesto del papper: **la brecha de producto se está cerrando mes con mes**
  (BDC entrega releases mensuales), mientras que **la brecha contractual y de costo no se ha
  movido**. Y esa asimetría es exactamente la razón por la que la decisión debe ser gradual y
  reversible, no de una sola firma.
- **Otras ventajas verificadas, sin humo:**
  - **Se conserva el activo.** El *lift* es *as-is*: los objetos BW no se tocan. Años de lógica
    de negocio, KPIs y jerarquías sobreviven al movimiento — el argumento del "gold mine" que
    SAP usa, y que en este caso es cierto.
  - **Elasticidad real de infraestructura.** SAP documenta el caso de bajar un sistema de 8 TB
    de memoria a 2 TB cuando el uso ya no lo justifica, y el volumen grande se descarga al object
    store (HANA Data Lake Files). Para quien ya hizo un proyecto serio de **Data Volume
    Management**, esto no es teoría: es la continuación natural de ese trabajo.
  - **Reasignación sin renegociar.** Los servicios BW dentro de BDC caen bajo el contrato de BDC
    y no bajo RISE. En capacity units, achicar BW y **reasignar la capacidad liberada** a SAC,
    Datasphere o Databricks se hace en autoservicio, sin reabrir el contrato. Es la única parte
    del modelo comercial que **juega a favor** del cliente, y hay que reconocerla.
  - **El camino de AI/ML deja de ser un proyecto de extracción.** Con el dato de BW publicado
    como data product y compartido por delta share, entrenar un modelo sobre datos de BW deja de
    empezar con "primero sacamos el dato".
- **Fuentes:**
  - https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
    — Databricks, 30-abr-2026, anuncio de GA del sync de metadatos semánticos. Es fuente de
    vendor y se cita **como declaración del vendor sobre su propio producto**, respaldada por la
    documentación técnica de la Idea 2.
  - https://expertum.net/sap-bdc-reflections-after-one-year/ — Expertum, 08-ene-2026. El
    reproche del Parquet sin semántica, el conteo de **259 standard data products** (mayoría
    master data, solo tres sistemas fuente soportados) y el modelo de costo de los data products.
    ⚠️ **Enero: el conteo casi seguro ya cambió. Re-verificar antes de citar la cifra o quitarla.**
  - https://learning.sap.com/courses/transforming-sap-bw-with-sap-business-data-cloud/moving-an-sap-bw-system-to-sap-bw-private-cloud-edition-in-sap-business-data-cloud
    — SAP Learning (oficial): movimiento *as-is*, ahorro por object store, capacity units fuera
    de RISE y reasignación en autoservicio.
  - https://community.sap.com/t5/data-professionals-knowledge-base/sap-business-data-cloud-release-update-highlights/ta-p/14419067
    — release highlights mensuales de BDC (junio-2026: object stores como fuente en replication
    flows, Snowflake como fuente, acceso directo a delta shares en transformation flows).

## Idea 4 — El roadmap: dónde el diagrama de SAP dice "planned"

- **Formato:** sección de cierre del papper — el entregable que pidió Ricardo.
- **Tesis:** SAP publica un roadmap de tres pasos, **Lift → Shift → Innovate**, y está bien
  planteado. Lo que el diagrama no dice con la misma letra es **qué pieza ya existe y cuál está
  marcada como planeada**. Un roadmap propio se construye poniendo esa distinción encima.

  **Lo que ya existe y funciona hoy:**
  - **El lift.** Prerrequisitos publicados: BW/4HANA **2021 SP4 o superior**, o **2023 SP0 o
    superior**; BW/4HANA 1.0 y 2.0 exigen subir a 2023 con el último SP; BW NetWeaver 7.5 debe
    estar **sobre base de datos HANA** (SPS 24+). Los partners estiman el lift en **2 a 3 meses**
    según el tamaño del landscape. ⚠️ Estimación de partner, no compromiso de SAP: citarla como
    tal, o no citarla.
  - **El Data Product Generator.** Publica InfoProviders —InfoObject, aDSO, CompositeProvider,
    MultiProvider, InfoCube y Query as InfoProvider— como *Local Tables (File)* en un espacio
    **BW Inbound** de Datasphere. Los objetos ahí son de solo lectura, una *merge task* mantiene
    la consistencia contra el origen, y hay **delta para CompositeProviders y MultiProviders**.
    Se opera desde el BW/4HANA Cockpit. Ese es el puente real entre el mundo viejo y el nuevo.
  - **La compartición hacia Databricks**, con las restricciones de la Idea 2.

  **Lo que está marcado como planeado o en camino (2026):** el **Query Template Generator**
  —convertir queries BW en analytic models— aparece explícitamente como *planned* en el
  Architecture Center; el **BW Migration Assistant**, que traduce data flows de BW a artefactos
  de Datasphere con ayuda de IA; el **Data Product Studio** (Q2-2026) y la absorción del Data
  Product Generator dentro de él; **Deep Copy** para Intelligent Applications (Q3-2026); y las
  mejoras del generador —soporte de jerarquías, delta mejorado, nombres técnicos propios.

  El párrafo que hay que escribir, y que casi nadie escribe: **las queries son el activo más
  grande y el último en tener herramienta.** En un BW maduro hay miles de queries con lógica de
  negocio, restricciones y variables. El generador mueve **datos con su semántica de modelo**;
  la herramienta que mueve **queries** todavía dice *planned*. Cualquier roadmap que planee
  apagar BW antes de que esa pieza sea real está planeando sobre una casilla vacía.
- **Riesgo a vigilar:** este es el terreno donde es fácil escribir un how-to. **No es un how-to:**
  la tesis es que un roadmap se ordena por **lo que ya existe**, y que la fase 3 se planea pero
  no se compromete. Y hay que decir la incomodidad completa: **lo que se lleva bien en el lift
  es también lo que no querías llevarte.** Un BW con quince años de objetos muertos lifteado
  as-is es el mismo BW, ahora rentado. La limpieza es prerrequisito, no consecuencia.
- **Fuentes:**
  - https://architecture.learning.sap.com/docs/ref-arch/6550e4 — SAP Architecture Center. De
    aquí salen prerrequisitos por release, el detalle del Data Product Generator, el "(planned)"
    del Query Template Generator y el BW Migration Assistant.
  - https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/cca4744c85b14788babe7cb6b77c9973.html
    — SAP Help Portal, documentación del data product generator. **Fuente primaria para el
    detalle operativo.**
  - https://assets.dm.ux.sap.com/sap-user-groups/pdfs/260129_discover_sap_business_data_cloud_in_2026.pdf
    — "Discover SAP Business Data Cloud in 2026", presentación de SAP a los user groups (Sauer,
    ene-2026). De aquí salen las fechas de Data Product Studio (Q2-2026), Deep Copy (Q3-2026),
    BDC Connect brownfield para BigQuery/Snowflake/Fabric y las mejoras del generador.
  - https://www.element61.be/en/resource/beyond-bw-building-scalable-modernisation-strategy-sap-business-data-cloud
    y https://www.interdobs.nl/dwc/sap-bw-7-5-pce-in-business-data-cloud-the-legacy-objects-dilemma/
    — partners, sobre el dilema de arrastrar objetos legacy y sobre la coordinación con la
    transformación a S/4HANA. ⚠️ Fuentes de consultoría: usar como voz de campo, no como dato.

## Idea 5 — El costo que no cabe en la calculadora (contras duras)

- **Formato:** sección de desventajas del papper.
- **Tesis:** las tres desventajas de BDC que importan a quien firma no son técnicas.
  1. **El modelo comercial es opaco por diseño.** BDC se vende en **capacity units (CU)**, fichas
     reasignables entre Datasphere, SAC, BW private cloud edition y Databricks. Suena flexible, y
     lo es hacia adentro. Hacia afuera: BDC Core **debe venderse siempre junto con al menos una
     Intelligent Application**; la implementación mínima viable arranca en **640 CU** (un tenant
     de SAC con 25 usuarios BI); los **standard data products** se licencian por línea de negocio
     según los **FUEs del sistema fuente** y **no aparecen en la calculadora de CU**; y los
     **custom data products** cuestan **1,500 CU/mes**, de los cuales 1,000 son reutilizables
     —un incremento neto de ~500 CU/mes. El grupo de usuarios alemán, **DSAG**, presentó en marzo
     de 2026 una lista de contradicciones de este esquema y lo rebautizó, medio en broma,
     **"Business Data Complexity"**; su conclusión fue que, con las reglas actuales, **es casi
     imposible estimar el costo de licencia por adelantado**. ⚠️ El dato más filoso de esa
     presentación —que las capacity units **caducan mensualmente**, no anualmente como los
     créditos de BTP— llega vía prensa (E3) sobre una presentación de DSAG. **Verificar contra
     el service description de BDC antes de escribirlo, o atribuirlo explícitamente a DSAG.**
  2. **SAC vuelve a cotizarse por usuario.** Dentro de BDC Core, SAP Analytics Cloud se mide en
     **usuarios por mes** convertidos a CU, con escalones: de **25.60 CU** por usuario BI en el
     tramo de 25–200 usuarios hasta **10.54** arriba de 5,000; planning estándar arranca en
     **72.85** y planning profesional en **820.43**. Para cualquier organización que haya
     optimizado su licenciamiento de SAC moviendo consumo a **Analysis for Office**, entrar a BDC
     significa volver a poner exactamente ese eje sobre la mesa. Es la ventaja competitiva más
     clara de Ricardo en esta pieza: **él hizo ese ejercicio y le funcionó**, y puede decir en qué
     orden se debe negociar. (Anonimizado: "una operación donde dirigí esa optimización".)
  3. **La gravedad arquitectónica es el producto, no un efecto secundario.** Forrester lo dijo sin
     rodeos en mayo de 2026: con Dremio y Prior Labs, SAP está posicionando BDC como el **"AI data
     control plane"** —el plano de control de datos para IA—, y el intercambio es acelerar la
     ejecución a cambio de que **semántica, linaje y control de acceso vivan cada vez más adentro
     de la plataforma de SAP**, con la palanca de precios que eso da. Su recomendación es la que
     el papper debe adoptar: **diseñar para portabilidad** y decidir explícitamente dónde vive la
     autoridad del significado, con una ventana de 12 a 24 meses antes de que la IA agéntica
     congele esas decisiones. Aquí engancha directo con el arco semántico de las ediciones 01,
     04, 05 y 07 — **"¿con la semántica de quién?"** vuelve, ahora con precio.
- **Fuentes:**
  - https://assets.dm.ux.sap.com/sap-user-groups/pdfs/260416_breaking_down_the_sap_bdc_pricing_model.pdf
    — "Breaking Down the SAP BDC Pricing Model" (Raver, 16-abr-2026), material presentado a los
    SAP user groups. De aquí salen los valores de CU por usuario de SAC, el mínimo de 640 CU, la
    regla de "al menos una Intelligent Application" y el roadmap comercial. **Abrir y verificar
    los tramos exactos antes de escribir cualquier número.**
  - https://e3mag.com/en/sap-bdc-the-new-business-data-complexity/ — E3 Magazine, **19-mar-2026**,
    sobre la presentación de Michael Bloch (Head of Licenses, Contracts and Support, DSAG) en los
    DSAG Technology Days de Hamburgo. ⚠️ Prensa especializada reportando una presentación; el
    apodo "Business Data Complexity" y la caducidad mensual de los CU vienen de ahí.
  - https://www.forrester.com/blogs/sap-is-targeting-the-ai-data-control-plane/ — Forrester,
    14-may-2026. Analista independiente. La tesis del control plane, el riesgo de lock-in y las
    recomendaciones de portabilidad.
  - https://www.forrester.com/blogs/saps-reltio-acquisition-choice-cios/ — Forrester, 31-mar-2026,
    sobre Reltio y el master data como punto de control. Complemento, no eje.
  - https://expertum.net/sap-bdc-reflections-after-one-year/ — modelo de costo de standard vs.
    custom data products (FUEs, 1,500 CU/mes).
  - https://barc.com/research/sap-business-data-cloud/ — BARC, 21-abr-2026. Research note
    independiente sobre los límites prácticos del zero-copy y las implicaciones de costo. De pago;
    útil como respaldo de que **un analista neutral considera el tema digno de nota**, aunque no se
    cite su contenido.

---

## También pasó (contexto de mercado, sin idea propia)

- **Adopción, con la advertencia puesta.** El benchmark de **SAPinsider (Q1-2026)** reporta
  **45%** de organizaciones evaluando BDC, **4%** con adopción amplia, **26%** sin planes y
  **38%** sin resultados medibles todavía; solo **3%** dice tener una capa de datos unificada y
  gobernada; las barreras principales son **presupuesto (44%)**, complejidad del landscape
  **(34%)** y **roadmap poco claro (32%)**; **29%** tiene la migración de BW/BW4 en alcance y
  **69%** ancla BDC a S/4HANA. ⚠️ **Es un reporte "research partner sponsored"** y la muestra se
  inclina a Software/Tecnología (34%) e Industrial/Manufactura (28%). Si se usa, **decir que es
  patrocinado en la misma oración** ([[feedback-papper-sourcing]]).
- **Sapphire 2026 (mayo):** HANA Cloud pasa a componente nativo de BDC; **SAP Master Data
  Governance y Reltio** entran a BDC; **BDC Connect para Amazon Athena** con GA planeada H2-2026.
- **Mayo 2026:** **SAP Snowflake** disponible en general como solution extension, con
  compartición bidireccional vía BDC Connect.
- **Junio 2026:** replication flows aceptan object stores como fuente (HANA Data Lake Files, S3,
  ADLS, GCS, OneLake); acceso directo a tablas de delta share en transformation flows.
- **Julio 2026:** consolidación en **SAP Business AI Platform**.

---

## Ranking sugerido

Este barrido fue dirigido, así que las ideas **no compiten: se ensamblan**. El orden es el orden
del papper.

1. **Idea 1 — El reloj de 2027 no es tu reloj.** Es la tesis. Un hallazgo verificable contra
   fuente oficial de SAP que reencuadra todo el tema y que ningún blog de partner tiene incentivo
   para escribir.
2. **Idea 2 — La letra chica del zero-copy.** El núcleo técnico y el mayor diferenciador: casi
   nadie ha leído la cláusula de divulgación de la documentación de Databricks.
3. **Idea 5 — El costo que no cabe en la calculadora.** Las desventajas, en el registro de quien
   firma presupuesto.
4. **Idea 3 — Lo que SAP sí cerró.** El contrapeso que hace creíble todo lo anterior.
5. **Idea 4 — El roadmap.** El entregable de cierre.

## Estructura propuesta para el papper (edición 08)

**Título de trabajo:** *El reloj que no es tuyo* — con subtítulo del tipo "Qué decidir de verdad
cuando te proponen mover BW/4HANA a Business Data Cloud".

1. **Apertura (Idea 1).** El calendario de 2027 y a quién le aplica realmente. 2040 como el dato
   que cambia la conversación.
2. **Qué ganas de verdad (Idea 3).** Ventajas verificadas, incluido el arco de doce meses en el
   que SAP cerró la brecha de semántica. Sin humo y sin sarcasmo.
3. **Qué entregas (Ideas 2 y 5).** La letra chica del zero-copy, el modelo de capacity units y la
   gravedad arquitectónica. Aquí va el párrafo de SAC / Analysis for Office con la experiencia
   propia, anonimizada.
4. **El roadmap (Idea 4).** Tres fases ordenadas por lo que existe hoy, con la limpieza previa
   como fase cero y las queries como el riesgo declarado.
5. **Cierre para quien firma.** Tres o cuatro exigencias concretas para la mesa de negociación:
   confirmación **por escrito** del alcance de materialización y redistribución; costo de las
   capacity units modelado a 24 meses con el supuesto de caducidad puesto sobre la mesa; una
   cláusula de portabilidad de la semántica; y la fecha comprometida —no planeada— de la
   herramienta de queries. Ancla regional: en el noreste, la operación de manufactura y consumo
   masivo lleva veinte años acumulando lógica de negocio dentro de BW; esa lógica es el activo que
   se está negociando, aunque el contrato hable de capacidad.

## Antes de escribir — verificaciones obligatorias

1. **KBA 2934895 / PAM** — fechas exactas de mantenimiento de BW/4HANA 2021 y 2023. Es la
   columna vertebral de la tesis. Abrir la fuente, no el resumen.
2. **PDF de precios de BDC** — confirmar tramos de CU de SAC, mínimo de 640 CU y la regla de la
   Intelligent Application.
3. **Caducidad mensual de las capacity units** — buscar el service description oficial. Si no
   aparece, atribuir explícitamente a DSAG vía E3 y decir que SAP no lo publica abierto.
4. **Supplement / Usage Guidelines de BDC** — intentar la fuente oficial de sap.com. Si no es
   pública, decirlo en el texto.
5. **Conteo de standard data products** — el 259 es de enero de 2026. Re-verificar o quitar.
6. **Longitud objetivo fijada ANTES de escribir**: ~2,000 palabras, como la edición 07
   ([[feedback-cost-aware-execution]]).

## Corrección posterior al barrido (24-ago-2026)

⚠️ **El Query Template Generator ya no es *planned*.** El Architecture Center (página de
2025) lo marca así, pero el **30-jul-2026** SAP publicó en SAP Learning el curso que lo
documenta con transacción (`RSDWCTG_ADMIN`), objetos generados, autorizaciones y pasos de
configuración. Las dos páginas oficiales de SAP se contradicen; la más reciente gana. El
draft ya está corregido y el hallazgo pasó de riesgo a noticia.

También se incorporaron al draft, verificados después del barrido: el camino alterno
**BW/4HANA Model Transfer** desde on-premise (`RSDWC_QUERY`), la regla de la **nota SAP
2932647** —los features no soportados no bloquean la transferencia, se omiten y se quitan
del objeto—, el traspaso de analysis authorizations vía `RSDWC_DAC_RSEC_GEN`, y el límite
de **Analysis for Office**, que alcanza vistas y perspectivas de Datasphere pero no
modelos analíticos.

## Nota de alcance

No se generó `draft-es.md` en esta fase. El tema tiene mucha superficie factual y **seis
verificaciones abiertas** que conviene cerrar antes de redactar; escribir el borrador semilla
ahora significaría reescribirlo después. Recomendación: cerrar las verificaciones 1 a 4 y
arrancar el draft en esa misma sesión.
