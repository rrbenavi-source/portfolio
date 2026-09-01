# Lo que se omite en silencio

*El viaje de una query de ventas de BW a Business Data Cloud, estación por estación —y qué validar en cada una antes de que lo descubra un director en una junta.*

**Brújula · Edición 09 · W36**
*Arquitectura de Datos · SAP*

---

La edición pasada terminó en la decisión: qué firmas cuando te mueves a Business Data
Cloud, de dónde puede venir tu dato y cuánto cuesta de verdad. Esta empieza donde aquella
acaba. Supongamos que la decisión ya se tomó. **¿Qué le pasa a tu reporte?**

Los diagramas de tres cajas —*lift*, *shift*, *innovate*— no contestan eso. Así que
tomemos algo concreto y absolutamente típico: una **query de ventas** sobre un
**CompositeProvider** —el objeto de BW que junta varias fuentes en una sola vista para
reportar—, con jerarquía comercial, un par de *restricted key figures* —ventas del
año anterior, mismo periodo—, una fórmula de variación, variables de periodo y sociedad, y
autorizaciones por organización de ventas. Se consume de dos maneras: una historia en SAC
para la dirección comercial, y Analysis for Office en Excel para los controllers que
reconcilian.

Ese objeto, o uno casi idéntico, existe en prácticamente todos los BW de manufactura y
consumo masivo del país. Vamos a llevarlo estación por estación.

## Estación 1 — El lift: no pasa nada, y ese es el punto

El sistema se mueve *as-is*. La query sigue siendo la misma query, la conexión live de SAC
sigue apuntando al mismo sistema, Analysis for Office sigue funcionando. Nada se rompe
porque nada cambió: cambió el datacenter y el contrato.

**Qué validar:** que la versión califica —BW/4HANA 2021 SP4 o superior, o 2023 SP0 o
superior—. Que la limpieza se hizo **antes**: el lift se lleva todo, incluido lo que no
querías llevarte, y un BW con quince años de objetos muertos lifteado tal cual es el mismo
BW, ahora rentado por capacity unit. Y algo que casi nunca aparece en la propuesta: **la
extracción desde tu ERP ahora cruza la red.** Si tu origen se queda on-premise, las
ventanas de carga diarias que hoy corren dentro del datacenter pasan a viajar hacia la
nube de SAP. Hay que dimensionar el enlace y re-medir los tiempos con volumen real, no con
una muestra.

## Estación 2 — La query se vuelve modelo analítico

Aquí está la noticia. En el Architecture Center de SAP, el **Query Template Generator**
—la herramienta que convierte queries de BW en modelos analíticos de Datasphere— aparecía
marcado como *(planned)*. El **30 de julio de 2026** SAP publicó el curso que lo documenta
con transacción, autorizaciones y pasos de configuración. Las dos páginas oficiales se
contradicen; gana la más reciente.

Funciona en dos pasos. Creas un **query template** desde la query existente —en las BW
Modeling Tools 1.27 PL3, o en SAP GUI con `RSDWCTG_ADMIN`— y eliges el **espacio HANA** de
Datasphere donde nacerán los objetos. Luego generas: el sistema lee la definición completa
de la query, **fórmulas y variables incluidas**, y crea **dimensiones** por cada InfoObject
con textos o jerarquías —reutilizando las compatibles que ya existan—, una **fact view**
sobre el CompositeProvider limitada a los campos que la query referencia, y un **analytic
model** que espeja la estructura de la query.

Dos detalles importantes: lee desde **BW private cloud edition dentro de BDC**, o sea que
exige haber hecho la estación 1; y no usa el object store sino un espacio HANA, un camino
distinto al del Data Product Generator —los *targets* de las dos herramientas ni siquiera
se ven entre sí.

Si todavía no quieres mover el sistema, existe desde hace años el camino equivalente
on-premise: liberas la query con `RSDWC_QUERY` y la importas desde el Semantic Onboarding
de Datasphere con **BW/4HANA Model Transfer**. Un caso documentado por SAP muestra lo que
produce: una sola query generó **63 objetos** entre dimensiones, textos, jerarquías, fact
view y modelo analítico.

### Y aquí está el documento que decide tu proyecto

La nota SAP **2932647** —versión 18, del 18 de diciembre de 2025— lista, para el Model
Transfer desde BW/4HANA y desde BW bridge, qué features de una query se soportan y cuáles
no. La regla general está escrita así:

> *"If not indicated otherwise, unsupported features do not prevent the BW analytic query
> from being transferrable from SAP BW/4HANA to SAP Datasphere, but are simply skipped and
> removed from the transferred object during the process."*

Hay dos formas de perder, y solo una avisa.

**La que avisa.** Cuatro situaciones en las que el modelo **no se transfiere**: si la query
no está construida sobre un **CompositeProvider (HCPR)** —en escenarios BW/4HANA es el
único InfoProvider admitido—, o si ese CompositeProvider trae un **temporal join**, un
**ambiguous join** o **input parameters de vistas HANA**. Molesto, pero honesto: te enteras
el primer día.

**La que no avisa.** Todo lo demás se transfiere, y el feature no soportado desaparece del
objeto. La lista no tiene nada de exótica. Se pierden:

- **Cualquier fórmula que exceda `+ - * /`.** La nota enumera lo que no viaja y ahí está,
  prácticamente entero, el lenguaje de fórmulas de BW: `IF`, `AND`, `OR`, los comparadores,
  `%`, `%A`, `%GT`, `%CT`, `SUMCT`, `SUMGT`, `NODIM`, `NOERR`, `NDIV`, `COUNT`, `DELTA`,
  `LEAF`, `FRAC` y todas las funciones matemáticas.
- **Las queries de dos estructuras** — el diseño clásico de un reporte comercial.
- **El default filter**: solo sobrevive el global filter.
- **Las variables de exit, de replacement path y de autorización.**
- **La conversión de unidades**, los **key figures no acumulables**, los de **cobertura de
  inventario**, la **eliminación de volumen de negocio** y los **display attributes**.

Vuelve al ejemplo del principio. Esa query tenía una fórmula de variación —y una variación
protegida contra división entre cero se escribe con `NOERR` o `NDIV`—, variables de periodo
que en la práctica casi siempre son de exit, y autorizaciones apoyadas en variables de
autorización. Tres de sus piezas están en la lista. **No inventé un caso difícil: inventé
el caso típico.**

Y dos comportamientos que reordenan el roadmap completo. El primero: *"By design, any
transferred model is disconnected from any changes applied in SAP BW/4HANA after the model
was transferred."* El transfer **no es un puente vivo: es una foto de los metadatos.** Cada
cambio en la query original obliga a correr el proceso otra vez. El segundo: las
**jerarquías se aplanan y se materializan** hasta sus valores hoja, y las actualizaciones
en BW **no se reflejan** en modelos ya transferidos. Tu jerarquía comercial queda congelada
el día que la transferiste; una reorganización de zonas no llega sola.

**Qué validar, y es lo más importante de este papper:** no es que el objeto exista. Es que
**el número cuadre**, celda por celda, contra la query original, con las mismas variables y
el mismo día. Un modelo al que le quitaron media fórmula se ve perfectamente sano.

Y hay una pregunta que hoy no tiene respuesta pública. La nota 2932647 cubre el **Model
Transfer** y el **BW bridge**. Para el **Query Template Generator** no existe una lista
equivalente publicada. Puede que sea mejor, porque SAP dice que lee la definición completa
*"including formulas and variables"*. Puede que herede los mismos límites, porque el
destino es el mismo analytic model y varias de las pérdidas son del modelo de destino, no
del transporte. Nadie debería firmar un roadmap de miles de queries sin esa lista.
**Pídela por su nombre.**

Y una advertencia que la nota se hace a sí misma: es "desarrollo en curso, liberado en
múltiples oleadas", va en la versión 18 y se actualiza con frecuencia. La lista de hoy no
va a ser la de tu proyecto.

## Estación 3 — Dónde vive el número ahora

Cambió el motor. Con Model Transfer, BW queda como fuente remota y **el cálculo lo hacen
los motores de HANA de Datasphere**. Con el Query Template Generator, los objetos viven en
un espacio HANA de Datasphere. En los dos casos, el plan de ejecución que llevabas años
afinando —agregados, particiones, caché de OLAP— ya no es el que corre.

**Qué validar:** tiempos de respuesta con volumen productivo y con la jerarquía completa
desplegada. Conversión de moneda contra el mismo tipo de cambio y la misma fecha de
referencia. Fiscal year variant. Textos en los idiomas que realmente usas. Y si tienes
inventarios, recuerda que los no acumulables ni siquiera llegan: hay que rehacerlos, y son
el lugar clásico donde el total anual deja de ser la suma de los meses.

## Estación 4 — Dónde se consume el reporte

La historia de SAC es la parte fácil: creas una **conexión live de SAC hacia Datasphere** y
ahí puedes construir de nuevo o **sustituir la fuente BW en las historias y modelos que ya
existen**. Es trabajo, no es drama.

**El problema son los controllers.** Según la KBA **3297935** y la matriz de conexiones de
Analysis for Office, la herramienta alcanza **vistas y perspectivas** de Datasphere, pero
**no los modelos analíticos** —justo el objeto que producen las dos herramientas de la
estación 2—. El camino soportado para llevar un modelo analítico a Excel es el **add-in de
SAP Analytics Cloud para Microsoft Excel**: otro producto, que sí consume modelos de
Datasphere, queries de BW y de S/4HANA, hace planeación en vivo, y **requiere licencia de
BI o de planning de SAC** — es decir, capacity units por usuario al mes.

Ahí es donde el roadmap técnico choca con la estrategia de costos. Si tu ahorro en
licenciamiento de analytics vino de mover consumo hacia Analysis for Office —una jugada
común y correcta—, la migración de la query empuja a esa gente de regreso a la familia SAC.
Nadie va a poner las dos cosas en la misma diapositiva por ti.

**¿Y Power BI?** Hay tres caminos y no son equivalentes:

- **OData** —un protocolo de consulta sobre HTTP, con conector nativo en Power BI— es el
  único de los tres que alcanza **modelos analíticos** y no solo vistas, y el único que
  respeta las dos cosas que hacen valioso a ese modelo. Su **agregación**: el modelo no solo
  suma, también define excepciones —inventario que se toma como el último valor del periodo,
  headcount que se cuenta sin acumular— y por OData el motor de Datasphere aplica esa regla
  antes de mandarte el número. Y sus **asociaciones**: los joins ya definidos hacia las
  dimensiones, que traen el texto y la jerarquía pegados a la llave. El precio está en la
  autenticación: **OAuth de tres patas** —usuario, aplicación cliente y servidor de
  autorización—, donde la persona autoriza a Power BI a leer en su nombre. Bueno para la
  seguridad, porque el token carga su identidad y los Data Access Controls aplican por
  persona; incómodo para la operación, porque los tokens expiran y el refresh programado
  depende de que alguien se vuelva a autenticar.
- **ODBC/JDBC** vía Open SQL schema es más simple, pero SQL devuelve resultados
  bidimensionales: contra un modelo analítico **se pierden asociaciones y jerarquías, y el
  dato llega des-agregado**, así que Power BI lo vuelve a sumar con la regla equivocada —el
  inventario anual sale como la suma de doce meses en vez del saldo de diciembre—. Para el
  mundo OLAP que traes de BW, te devuelve al inicio.
- **Premium Outbound Integration** es la salida masiva con precio explícito: bloques de
  20 GB con tarifa escalonada. El detalle que hunde presupuestos es que se cobra el volumen
  de salida, no el de la tabla; mediciones públicas sobre tablas tipo BSEG dieron un
  **factor cercano a 30** contra el tamaño original.

Y encima está la frontera contractual, que tiene dos puertas con dos reglas distintas.
Conviene no confundirlas, porque la gente cita la que le conviene.

**Sacar datos de Datasphere** hacia una herramienta de terceros se rige por los términos de
esa capacidad: las APIs de SAP no pueden usarse para extraer hacia aplicaciones de
terceros, con la frase *"Use of OData APIs for data extraction is prohibited"* y un tope de
2,000 llamadas OData por GB de memoria de cómputo por tenant al mes.

**Sacar datos del BW** que ahora corre en la nube de SAP se rige por la sección 6 del
Supplement vigente, la de los *BW Capacity Services*, y ahí la redacción es más dura. El
§6.2.5 —dentro del apartado que gobierna la HANA runtime edition sobre la que se apoya tu
sistema— dice *"Customer is expressly prohibited from performing the mass extraction of any
data"*, salvo mediante herramientas SAP licenciadas y **únicamente hacia seis destinos
enumerados**: HANA enterprise edition, HANA standard edition, el servicio HANA de SAP Cloud
Platform, HANA Cloud, HANA EE Cloud y las capacidades de Datasphere. Los seis son SAP. Un
lakehouse de terceros no está en la lista.

La línea práctica, en las dos puertas, está entre **consumir** —reportar en vivo, dentro de
los topes— y **extraer**. Los topes son, de hecho, el gobernador: te dejan reportar, no
vaciar.

Si tu destino corporativo de reporting es Power BI, la vía que SAP y Microsoft están
construyendo se llama **BDC Connect for Microsoft Fabric**: compartición bidireccional
zero-copy hacia OneLake. Su disponibilidad general está planeada para el **tercer
trimestre de 2026** —el que está corriendo y cierra en septiembre—, así que al momento de
escribir esto sigue siendo una promesa con calendario, no algo que puedas probar.
Pregúntala por nombre y pide la fecha por escrito.

## Estación 5 — Las autorizaciones no viajan solas

Tu query filtra por organización de ventas mediante analysis authorizations, y ya vimos que
las **variables de autorización no sobreviven al transfer**. Datasphere tampoco tiene
analysis authorizations: tiene **Data Access Controls**. Hay puente: la transacción
`RSDWC_DAC_RSEC_GEN` exporta tus autorizaciones a la tabla `RSDWC_RSEC_DAC`, que se importa
a Datasphere y genera una cláusula de filtro donde el usuario de BW se sustituye por el de
Datasphere —por correo, con un BAdI si tu lógica es otra—, más una vista de permisos y el
DAC.

**Qué validar:** los **comodines**. En BW se usan a manos llenas y los Data Access Controls
no los soportan; toda autorización basada en patrones hay que resolverla en valores. La
granularidad: dentro de un mismo espacio no puedes restringir un modelo analítico a un
grupo de usuarios, así que la separación se hace **por espacio**, y eso reordena tu diseño.
Y la prueba que nadie hace: entrar con el usuario de un gerente regional y confirmar que ve
exactamente lo mismo que veía, ni una fila más.

## Estación 6 — ¿Y BPC?

Buena noticia primero: **BPC se mueve con el BW**, en el mismo movimiento. SAP lo dice
explícitamente —*"along with moving your SAP BW 7.50 or SAP BW/4HANA to a private cloud
environment (PCE) in Business Data Cloud, you can also move your SAP BPC 10.1 NW or SAP BPC
2021 at the same time"*—. Eso es justo lo que suele descarrilar estos proyectos, y aquí no
lo hace. Y existe una arquitectura híbrida que ya funciona: una aplicación de planeación en
SAC apoyada en **BPC Live Connection** contra el BW en nube privada; el usuario oprime
guardar en SAC y el dato queda disponible en Datasphere, sin duplicar.

Lo incómodo viene después. La dirección estratégica de SAP no es BPC: es **SAC para
planeación** y **Group Reporting para consolidación estatutaria**. Y de BPC a SAC no hay
migración, hay **reimplementación** —modelos, script logic y reportes se rehacen—. Con lo
cual la planeación queda partida entre dos programas: la consolidación viaja con el
proyecto de S/4, la planeación con el de analytics, y **la licencia de BPC sigue haciendo
falta mientras BPC exista**. Durante la transición se paga dos veces.

**Qué validar:** si sigues desarrollando en BPC, usa **estructuras aDSO modernas
compatibles con el Data Product Generator** —es gratis hacerlo bien ahora y caro
descubrirlo después—. Y algo de contrato que casi nadie revisa y que aquí pesa.

El Supplement separa dos figuras con definiciones propias. Un **Add-on** agrega
funcionalidad nueva e independiente *sin modificar* la funcionalidad SAP existente (§1.1).
Una **Modification** es un cambio al código o los metadatos entregados, o cualquier
desarrollo que personalice o altere funcionalidad existente (§1.9). El script logic, los
BAdIs, los exits y buena parte de los desarrollos Z que rodean a BPC caen del lado de la
Modification.

La distinción no es académica. El §6.7.2 enumera los servicios en los que el cliente tiene
derecho a desarrollar y usar Modifications, y son las cuatro variantes de S/4HANA Cloud
private edition; los *BW Capacity Services* no están en esa lista. Para BW, lo que el
§6.7.1 concede es el derecho a desarrollar y usar **Customer ABAP Add-ons**. Puede ser una
imprecisión de redacción —el documento usa el término *BW Capacity Services* de forma
elástica— o puede ser exactamente lo que dice. La pregunta hay que hacerla por escrito
antes de firmar: **¿mis desarrollos actuales alrededor de BPC siguen siendo admisibles
dentro del BW en la nube de SAP, y bajo qué figura?**

Lo que sí está escrito sin ambigüedad son las consecuencias. El SLA y el Support Schedule
**no aplican** a los Customer ABAP Add-ons, y tú respondes por su instalación, soporte,
compatibilidad y vulnerabilidades (§6.7.2). Los checks de simplificación e incompatibilidad
en cada upgrade **los ejecutas tú** (§6.10.2). Y la propiedad intelectual de toda
Modification queda del lado de SAP (§6.7.4).

## Estación 7 — Y hasta entonces, el dato para IA

Solo aquí entra el **Data Product Generator**, que es otra herramienta y sirve para otra
cosa: publica InfoProviders —InfoObjects, aDSOs, CompositeProviders, MultiProviders,
InfoCubes y queries usadas como InfoProvider— hacia tablas de solo lectura en el object
store, con una tarea de consolidación que mantiene la consistencia contra el origen y
deltas para CompositeProviders y MultiProviders. De ahí sale, por delta share, el dato para
Databricks — con todas las restricciones de contrato que revisamos la edición pasada.

Y una que no revisamos, porque vive en la sección de desarrollos: el §6.7.2 le reserva a
SAP el derecho de restringir o exigir la remoción de cualquier Add-on o Modification que
*"enable the extraction of Data Products to non-SAP applications through any means not
authorized via SAP"*. El código que escribas dentro de ese BW también queda sujeto a la
frontera del dato.

## Lo que se lleva de aquí quien firma

Tres números, y ninguno es el del servidor:

1. **Cuántas de tus queries usan features que se van a omitir en silencio.** No cuántas
   tienes: cuántas están en la lista. Ese es el proyecto.
2. **Cuántos de tus usuarios de Excel tocan objetos que van a terminar siendo modelos
   analíticos**, y qué cuesta esa población en capacity units.
3. **Con qué frecuencia cambian tus queries y tus jerarquías.** Porque cada cambio obliga a
   volver a transferir, y ese trabajo recurrente no aparece en ninguna propuesta.

Y una exigencia: **la lista de features no soportados del Query Template Generator**, que
hoy no está publicada. Sin ella, el roadmap de la estación 2 es una casilla en blanco.

Nada de esto dice que no te muevas. Dice que el número que llega al dashboard después del
movimiento tiene que ser el mismo que llegaba antes —y que demostrarlo es trabajo, no un
supuesto.

---

## Fuentes

- **SAP.** Nota **2932647**, *Supported and unsupported features with SAP BW/4HANA / SAP BW
  Bridge Model Transfer in SAP Datasphere*, **versión 18, 18 de diciembre de 2025**. Fuente
  primaria de la estación 2: regla de omisión silenciosa, bloqueantes duros, listas por
  nivel, desconexión por diseño del modelo transferido y aplanamiento de jerarquías. La
  propia nota advierte que la lista cambia con el tiempo. Relacionada: nota **3478268**,
  sobre el soporte de jerarquías. https://me.sap.com/notes/2932647
- **SAP Learning.** *Outlining the Capabilities of the Query Template Generator* y
  *Outlining the Configuration of the Query Template Generator*, publicados el **30 de julio
  de 2026**. Proceso de dos pasos, objetos generados, transacción `RSDWCTG_ADMIN`, BW
  Modeling Tools 1.27 PL3 y objeto de autorización S_ADT_RES.
  https://learning.sap.com/courses/transforming-sap-bw-with-sap-business-data-cloud/outlining-the-capabilities-of-the-query-template-generator_a2bfd608-4246-4255-8ea9-2d250e90de91
- **SAP Architecture Center.** *Modernizing SAP BW with SAP Business Data Cloud*
  (ref-arch 6550e4). Prerrequisitos por release, detalle del Data Product Generator y la
  marca *(planned)* del Query Template Generator, que la fuente anterior supera.
  https://architecture.learning.sap.com/docs/ref-arch/6550e4
- **SAP Learning.** *Introducing Model Transfer*. Transacción `RSDWC_QUERY`, BW como fuente
  remota con cálculo en los motores de HANA de Datasphere, traspaso de analysis
  authorizations vía `RSDWC_DAC_RSEC_GEN` y la tabla `RSDWC_RSEC_DAC`, y sustitución de
  fuentes BW en historias existentes de SAC.
  https://learning.sap.com/learning-journeys/modernizing-your-data-warehouse-landscape-from-sap-bw-to-sap-datasphere/introducing-the-hybrid-approach
- **SAP / comunidad SAP.** *Part 2 – Import SAP BW/4HANA Queries into SAP Datasphere using
  SAP BW/4HANA Model Transfer.* Caso documentado: una sola query genera 63 objetos.
  https://community.sap.com/t5/technology-blog-posts-by-sap/part-2-import-sap-bw-4hana-queries-into-sap-datasphere-using-sap-bw-4hana/ba-p/13759521
- **SAP.** KBA **3297935**, *SAP Datasphere Analytic Models and some Views are not shown in
  AO*, y KBA **2436382**, matriz de conexiones de Analysis for Office. Alcance sobre
  Datasphere: vistas y perspectivas sí, modelos analíticos no.
  https://userapps.support.sap.com/sap/support/knowledge/en/3297935
- **SAP Help Portal.** *Consuming Data Exposed by SAP Datasphere*. Los tres caminos hacia
  Power BI y otros clientes: OData, ODBC/JDBC vía Open SQL schema, y sus límites.
  https://help.sap.com/docs/SAP_DATASPHERE
- **SAP.** *SAP Business Data Cloud — Supplemental Terms and Conditions*, **versión 7-2026**.
  Documento público, sin registro, leído completo para esta edición. Definiciones de Add-on
  (§1.1), Customer ABAP Add-on (§1.7) y Modification (§1.9); prohibición de extracción
  masiva y lista cerrada de seis destinos permitidos (§6.2.5); derechos y responsabilidades
  sobre Add-ons y Modifications, incluida la cláusula de remoción por extracción de Data
  Products hacia aplicaciones no-SAP (§6.7.1–§6.7.5); checks de simplificación e
  incompatibilidad a cargo del cliente (§6.10.2). Las citas de *"Use of OData APIs for data
  extraction is prohibited"* y del tope de 2,000 llamadas por GB corresponden a la **versión
  10-2025** (secciones 2.5 y 5.5), que gobierna el consumo de Datasphere; la numeración de
  secciones no es la misma entre versiones y aquí se citan por separado a propósito.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v7-2026.pdf
- **SAP y Microsoft.** *SAP Business Data Cloud Connect for Microsoft Fabric*, anunciado en
  noviembre de 2025, con disponibilidad general planeada para Q3 2026. Compartición
  bidireccional zero-copy hacia OneLake.
  https://news.sap.com/2025/11/sap-bdc-connect-for-microsoft-fabric-business-insights-ai-innovation/
- **SAP.** *SAP Business Planning and Consolidation (SAP BPC) Strategy Update*, 8 de octubre
  de 2025. BPC se mueve a la nube privada junto con el sistema BW.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-planning-and-consolidation-sap-bpc-strategy-update/ba-p/14237803
- **Comunidad SAP.** *Planning Modernization*, 31 de mayo de 2025. Arquitectura híbrida de
  SAC sobre BPC Live Connection contra BW en nube privada, y la recomendación de usar
  estructuras aDSO compatibles con el Data Product Generator. Contribución de miembro.
  https://community.sap.com/t5/technology-blog-posts-by-members/planning-modernization/ba-p/14115243
- **Comunidad SAP.** *Working with BW Authorizations in Datasphere on Enterprise Level.* Los
  Data Access Controls no soportan comodines y la separación por espacio. Contribución de
  miembro; validar contra el estado actual del producto.
  https://community.sap.com/t5/technology-blog-posts-by-members/working-with-bw-authorizations-in-datasphere-on-enterprise-level/ba-p/14302361
- **Expertum.** *Premium Outbound Integration in SAP Datasphere.* Bloques de 20 GB y el
  factor de inflación medido sobre tablas grandes. Medición de partner, de 2024: sirve el
  orden de magnitud, no el número exacto.
  https://expertum.net/premium-outbound-integration-in-sap-datasphere/
