# El reloj que no es tuyo

*Te van a vender la migración de BW a Business Data Cloud con una fecha y un diagrama de tres cajas. Aquí está el viaje real de una query de ventas —de BW a SAC— con lo que hay que validar en cada estación.*

**Brújula · Edición 08 · W35**
*Arquitectura de Datos · SAP*

---

Todas las presentaciones empiezan igual. Una línea de tiempo, una fecha en rojo y una
flecha que apunta hacia arriba: **31 de diciembre de 2027**, fin del mantenimiento
mainstream de SAP BW NetWeaver 7.5. Es una fecha real y el problema que representa es
enorme —en Sapphire 2025, el propio product management de SAP habló de **entre 20,000 y
30,000 clientes** todavía corriendo esa versión.

Si eres uno de ellos, la propuesta es buena: mover el sistema tal como está a **SAP BW,
private cloud edition** dentro de Business Data Cloud —dejar que SAP lo opere en su nube
sin convertir ni reescribir nada— y ganar tres años, hasta **fin de 2030**.

Pero si ya estás en **BW/4HANA**, esa fecha no es la tuya. Y aquí hay que leer con
cuidado, porque el dato circula mal en las dos direcciones. SAP alineó **la línea de
producto** BW/4HANA con la de S/4HANA hasta finales de **2040**, y ese compromiso cubre el
despliegue on-premise. Pero está redactado como una promesa de línea, entregada *"through
a sequence of releases"*: tu **release** tiene su propia fecha. BW/4HANA **2023** está en
mantenimiento mainstream hasta el **31 de diciembre de 2030**.

O sea: ni el pánico de 2027 ni la calma de 2040. Cuatro años y medio de pista en lo que
tienes hoy, y un camino comprometido a 2040 mediante upgrades sucesivos. Si además corres
**BPC**, ese tren va en pareja: BPC 2021 —que soporta BW/4HANA 2021 y 2023— vence la misma
fecha, el 31 de diciembre de 2030, y la continuidad hasta 2040 depende de releases de BPC
que SAP se compromete a entregar pero que todavía no tienen nombre.

Y ahí está el punto que la línea de tiempo en rojo esconde: **un upgrade de BW/4HANA es un
proyecto técnico. Un movimiento a Business Data Cloud es un cambio de contrato, de modelo
de consumo y de régimen del dato.** No están en la misma categoría, y elegir el segundo
por miedo al primero sale caro.

Sin la urgencia prestada, quedan dos preguntas que sí valen: **qué firmas** y **cómo se ve
tu reporte del otro lado**. Este papper contesta las dos, en ese orden.

## Lo que sí ganas, dicho sin adorno

Empiezo por ahí porque el resto es incómodo y no quiero que se lea como una postura.

**Conservas el activo.** El *lift* es *as-is*: los objetos de BW no se tocan. Quince años
de lógica de negocio y reglas que nadie documentó completas siguen ahí después del
movimiento.

**La infraestructura por fin se encoge.** El volumen grande baja al object store
—almacenamiento barato de archivos, fuera de memoria— y la máquina se dimensiona por uso
real. SAP documenta el caso de pasar de 8 TB de memoria a 2 TB. Si ya hiciste *data
volume management*, esto es el siguiente capítulo del mismo trabajo.

**Mueves capacidad sin renegociar.** Los servicios de BW dentro de BDC caen bajo el
contrato de BDC y no bajo RISE: achicar BW y reasignar lo liberado a Datasphere, SAC o
Databricks se hace en autoservicio.

**Y la brecha técnica se cierra rápido.** En enero, el reproche más citado era que los
*data products* —los paquetes de datos curados que BDC publica— viajan en Parquet, un
formato que no carga significado. El 30 de abril de 2026 salió en disponibilidad general
la sincronización de metadatos semánticos hacia Unity Catalog, el catálogo de gobierno de
Databricks: descripciones, llaves y etiquetas de datos personales. Cuatro meses entre la
crítica y el cierre. Cualquier objeción puramente técnica que escriba hoy tiene fecha de
caducidad.

La que no se ha movido en dieciocho meses es la otra.

## El documento que nadie abre

Los términos de Business Data Cloud son públicos, se descargan sin registro del Trust
Center de SAP, y la versión vigente —la séptima de 2026— tiene párrafos que valen más que
cualquier demo. Empiezo por el que decide arquitectura, la sección 3.3:

> *"Customer may allow Third-Party Connectors to temporarily store or materialize Data
> Products on such Third Party Connectors' systems solely for performance optimization
> purposes. For the avoidance of doubt, Customer may not allow Third-Party Connectors'
> systems to distribute Data Products to systems other than SAP Business Data Cloud."*

En corto: puedes compartir un data product con tu propio Databricks, y ahí puede quedarse
copiado **temporalmente y solo para que las consultas corran más rápido**. Lo que ese
Databricks no puede hacer es **repartirlo hacia adelante**. Power BI, Tableau, un data
lake externo, otro tenant: todos quedan del lado equivocado de esa frase. Tu lakehouse
deja de poder ser la capa desde donde todo se sirve y pasa a ser un consumidor autorizado
y no redistribuidor.

El argumento que circula entre consultores para librar la restricción es que un dato
suficientemente transformado ya deja de ser un data product. Ojalá. La sección 1.11 define
*Data Product* como *"enriched data or enriched Customer Data, where enrichment is any type
of reorganization, semantics, summarization, reporting or metadata"*. El enriquecimiento no
es lo que te saca de la definición: es lo que te mete en ella. Puede que SAP acepte esa
lectura en tu caso; no está en el texto. Si tu arquitectura depende de ella, pídela por
escrito antes de diseñar.

Tres párrafos más antes del datasheet:

- **3.5.** SAP se declara dueño de la propiedad intelectual de los data products; tú tienes
  licencia de uso.
- **3.6.** Usar un conector de tercero **es consentir** que SAP y ese tercero intercambien
  información de uso, *"including identifying Customer"*. La documentación de Databricks
  —actualizada el 4 de agosto de 2026— es más específica: puede revelar a SAP el volumen de
  datos de BDC y su proporción frente a los no-BDC, y **el precio efectivo que tu
  organización paga por consumo de Databricks**, por workload y sin anonimizar.
- **2.6.4.** Los servicios de BDC Connect están clasificados como **Grupo 2**: si SAP
  deprecia un servicio de Grupo 1 lo sigues usando el resto de tu suscripción; si es de
  Grupo 2, al vencer el aviso de seis meses **pierdes el acceso**. El puente hacia tu propio
  Databricks es, por contrato, la pieza apagable.

Y sobre el BW ya en la nube privada: la sección 6.2.5 prohíbe la extracción masiva salvo
con herramientas SAP licenciadas, y enumera los destinos permitidos —las ediciones de HANA
y **SAP Datasphere**—. Databricks no aparece en esa lista.

## Las capacity units no se guardan

BDC se vende en **capacity units**: fichas que reasignas entre Datasphere, SAC, BW en nube
privada y Databricks. Hacia adentro la flexibilidad es real. Hacia afuera, tres reglas que
conviene modelar antes de firmar.

**Lo que no gastas se pierde.** El Supplement de octubre de 2025 lo dice en una línea
—*"Unused Capacity Units may not be carried over into any subsequent month"*— y agrega que
no se prorratean por meses parciales. No es el vencimiento anual de los créditos de BTP:
es mensual. Presupuestas por año y consumes por mes.

**El contrato trae una errata declarada.** La sección 2.4 aclara que donde el Order Form
dice que la métrica de uso muestra el máximo utilizable en doce meses, *"includes a
drafting error"* y debe leerse **un mes**.

**Y SAP Analytics Cloud vuelve a cotizarse por usuario:** **25.60** capacity units por
usuario de BI al mes en el tramo de 25 a 200, bajando a **10.54** arriba de 5,000; planning
estándar desde **72.85**; planning profesional en **820.43**. Además BDC Core *"must always
be sold in conjunction with at least one Intelligent Application"*, y la implementación
mínima viable que la propia SAP presenta arranca en **640 capacity units**.

Ese último punto lo escribo con historia personal. En la plataforma que dirijo —BW/4HANA
2023, SAC, Analysis for Office y un Databricks propio en Azure— el proyecto que más ahorro
directo produjo dos años seguidos no fue técnico: fue mover consumo de SAC hacia Analysis
for Office y recortar a la mitad el licenciamiento de analytics. Guarda ese dato. Reaparece
en la estación 4 del roadmap, y no de la forma que esperas.

## El viaje de una query de ventas

Aquí es donde los diagramas de tres cajas dejan de servir. Tomemos algo concreto y
absolutamente típico: una **query de ventas** sobre un CompositeProvider, con jerarquía
comercial, conversión a moneda de grupo, un par de *restricted key figures* —ventas del año
anterior, ventas del mismo periodo— una fórmula de variación, variables de periodo y
sociedad, y autorizaciones por organización de ventas. Se consume de dos maneras: una
historia en SAC para la dirección comercial, y Analysis for Office en Excel para los
controllers que reconcilian.

Ese objeto, o uno igualito, existe en todos los BW de manufactura y consumo masivo del
país. Vamos a llevarlo a BDC estación por estación.

### Estación 1 — El lift: no pasa nada, y eso es el punto

El sistema se mueve *as-is* a BW private cloud edition. La query sigue siendo la misma
query, la conexión live de SAC sigue apuntando al mismo sistema, Analysis for Office sigue
funcionando. Nada se rompe porque nada cambió: cambió el datacenter y el contrato.

**Qué validar aquí:** que la versión califica —BW/4HANA **2021 SP4** o superior, o **2023
SP0** o superior; 1.0 y 2.0 exigen subir a 2023 primero—. Que la limpieza se hizo **antes**:
el lift se lleva todo, incluido lo que no querías llevarte, y un BW con quince años de
objetos muertos lifteado tal cual es el mismo BW, ahora rentado por capacity unit. Y que
mediste la latencia de red desde donde se consume: tus usuarios de Excel dejaron de estar
en el mismo datacenter que el sistema.

### Estación 2 — La query se vuelve modelo analítico

Aquí está la noticia que cambia el roadmap. En el Architecture Center de SAP, el **Query
Template Generator** —la herramienta que convierte queries de BW en modelos analíticos de
Datasphere— aparecía como *(planned)*. El **30 de julio de 2026** SAP publicó el curso que
lo documenta con transacción, autorizaciones y pasos de configuración. Las dos páginas de
SAP se contradicen; la más reciente gana.

Funciona en dos pasos. Creas un **query template** desde la query existente —en las BW
Modeling Tools, versión 1.27 PL3, o en SAP GUI con la transacción `RSDWCTG_ADMIN`— y ahí
eliges el **espacio HANA** de Datasphere donde van a nacer los objetos. Luego generas: el
sistema lee la definición completa de la query, **fórmulas y variables incluidas**, y crea
tres cosas. **Dimensiones** por cada InfoObject que tenga textos o jerarquías —y si ya
existe una dimensión compatible en el espacio, la reutiliza en vez de duplicarla—. Una
**fact view** sobre el CompositeProvider, limitada a los campos que la query referencia. Y
un **analytic model** que espeja la estructura de la query: sus key figures se vuelven
measures, sus características se vuelven asociaciones a dimensiones.

Dos cosas importantes. La primera: esto lee desde **BW private cloud edition dentro de
BDC**. Es decir, exige haber hecho la estación 1. La segunda: no usa el object store, usa
un espacio HANA —o sea, no es el mismo camino que el Data Product Generator, y los
*targets* de las dos herramientas ni siquiera se ven entre sí.

Si todavía no quieres mover el sistema, existe desde hace años el camino equivalente
on-premise: liberas la query con la transacción `RSDWC_QUERY` y la importas desde el
Semantic Onboarding de Datasphere con **BW/4HANA Model Transfer**. Un caso documentado por
SAP muestra lo que eso produce en la práctica: una sola query generó **63 objetos** entre
dimensiones, vistas de texto, jerarquías, fact view y modelo analítico. Los restricted key
figures llegaron como restricted measures, la exception aggregation se conservó con sus
características de referencia, y el filtro por nodo de jerarquía se convirtió en una lista
explícita de sus hijos.

**Y aquí está el documento que decide tu proyecto.** La nota SAP **2932647** —versión 18,
del 18 de diciembre de 2025— lista, para el Model Transfer desde BW/4HANA y desde BW bridge,
qué features de una query se soportan y cuáles no. La regla general está escrita así:

> *"If not indicated otherwise, unsupported features do not prevent the BW analytic query
> from being transferrable from SAP BW/4HANA to SAP Datasphere, but are simply skipped and
> removed from the transferred object during the process."*

Traducido a consecuencias: hay dos formas de perder, y solo una avisa.

**La que avisa.** Cuatro situaciones en las que el modelo **no se transfiere**: si la query
no está construida sobre un **CompositeProvider (HCPR)** —en escenarios BW/4HANA es el único
InfoProvider admitido—, o si ese CompositeProvider trae un **temporal join**, un **ambiguous
join** o **input parameters de vistas HANA**. Molesto, pero honesto: te enteras el primer día.

**La que no avisa.** Todo lo demás se transfiere, y el feature no soportado desaparece del
objeto. La lista importa porque no tiene nada de exótica. Se pierden:

- **Cualquier fórmula que exceda `+ - * /`.** La nota enumera lo que no viaja y ahí está,
  prácticamente entero, el lenguaje de fórmulas de BW: `IF`, `AND`, `OR`, los comparadores,
  `%`, `%A`, `%GT`, `%CT`, `SUMCT`, `SUMGT`, `NODIM`, `NOERR`, `NDIV`, `COUNT`, `DELTA`,
  `LEAF`, `FRAC` y todas las funciones matemáticas.
- **Las queries de dos estructuras** — el diseño clásico de un reporte comercial.
- **El default filter**: solo sobrevive el global filter.
- **Las variables de exit, de replacement path y de autorización.**
- **La conversión de unidades**, los **key figures no acumulables**, los de **cobertura de
  inventario**, la **eliminación de volumen de negocio** y los **display attributes**.

Vuelve al ejemplo del principio. Esa query de ventas tenía una fórmula de variación —y una
variación protegida contra división entre cero se escribe con `NOERR` o `NDIV`—, variables de
periodo que en la práctica casi siempre son de exit, y autorizaciones por organización de
ventas apoyadas en variables de autorización. Tres de sus piezas están en la lista. **No
inventé un caso difícil: inventé el caso típico.**

**Y dos comportamientos que reordenan el roadmap completo.**

El primero: *"By design, any transferred model is disconnected from any changes applied in
SAP BW/4HANA after the model was transferred."* El transfer **no es un puente vivo: es una
foto de los metadatos.** Cada cambio en la query original obliga a correr el proceso otra
vez. Si tu operación toca queries seguido —y toda operación comercial las toca—, acabas de
heredar un trabajo recurrente que nadie presupuestó.

El segundo: las **jerarquías se aplanan y se materializan** hasta sus valores hoja, y
*"updates to the hierarchy data in SAP BW/4HANA are not reflected in any models that have
already been transferred"*. Tu jerarquía comercial queda congelada el día que la
transferiste; una reorganización de zonas no llega sola. Además los nodos deben ser únicos,
los link nodes no se soportan, las jerarquías dependientes de versión tampoco —se concatenan
versión y nombre para fabricar un identificador único— y las de estructura dependiente del
tiempo se leen siempre con la fecha de hoy.

**Qué validar aquí, y es lo más importante del papper:** no es que el objeto exista. Es que
**el número cuadre**, celda por celda, contra la query original, con las mismas variables y
el mismo día. Un modelo al que le quitaron media fórmula se ve perfectamente sano.

Y hay una pregunta que hoy no tiene respuesta pública. La nota 2932647 cubre el **Model
Transfer** y el **BW bridge**. Para el **Query Template Generator** —la herramienta nueva, la
de BDC— **no existe una lista equivalente publicada**. Puede que sea mejor, porque SAP dice
que lee la definición completa de la query "including formulas and variables". Puede que
herede los mismos límites, porque el destino es el mismo analytic model y varias de las
pérdidas son del modelo de destino, no del transporte. Nadie debería firmar un roadmap de
miles de queries sin esa lista en la mano. **Pídela por su nombre.**

Y una advertencia que la nota se hace a sí misma: es "desarrollo en curso, liberado en
múltiples oleadas", va en la versión 18 y se actualiza con frecuencia. La lista de hoy no
va a ser la de tu proyecto. Vuelve a leerla antes de estimar.

### Estación 3 — Dónde vive el número ahora

Cambió el motor. Con Model Transfer, BW queda como fuente remota y **el cálculo lo hacen
los motores de HANA de Datasphere**. Con el Query Template Generator, los objetos viven en
un espacio HANA de Datasphere. En los dos casos, el plan de ejecución que llevabas años
afinando —agregados, particiones, caché de OLAP— ya no es el que corre.

**Qué validar:** tiempos de respuesta con volumen productivo y con la jerarquía completa
desplegada, no con una muestra. Conversión de moneda contra el mismo tipo de cambio y la
misma fecha de referencia. Fiscal year variant. Textos en los idiomas que realmente usas.
Y si tienes inventarios, ten presente que los key figures no acumulables ni siquiera
llegan: hay que rehacerlos, y son el lugar clásico donde el total anual deja de ser la suma
de los meses.

### Estación 4 — El reporte, y la trampa de Excel

La historia de SAC es la parte fácil. Creas una **conexión live de SAC hacia Datasphere** y
ahí tienes dos opciones: construir de nuevo, o **sustituir la fuente BW en las historias y
modelos que ya existen** por el nuevo objeto de Datasphere. Es trabajo, no es drama.

El problema son los controllers. Según la KBA **3297935** y la matriz de conexiones de
Analysis for Office, la herramienta alcanza **vistas y perspectivas** de Datasphere, pero
**no los modelos analíticos** —justo el objeto que producen las dos herramientas de la
estación 2—. El camino soportado para llevar un modelo analítico a Excel es el **add-in de
SAP Analytics Cloud para Microsoft Excel**, que es otro producto, con otra licencia.

Ahí es donde la historia personal de hace tres párrafos se cierra sola. Si tu estrategia de
costos fue mover consumo de SAC hacia Analysis for Office, la migración de la query te
empuja de regreso a la familia SAC —y en BDC, SAC se cotiza por usuario al mes en capacity
units. La optimización de licencias y el roadmap técnico se estorban, y nadie va a ponerlo
en la misma diapositiva por ti.

**Qué validar:** cuántos de tus usuarios de Excel tocan objetos que van a terminar siendo
modelos analíticos, contra tu versión y SP exactos de Analysis for Office; y qué cuesta
esa población en el modelo de capacity units. Ese número, y no el del servidor, es el que
decide si el caso de negocio cierra.

### Estación 5 — Las autorizaciones no viajan solas

Tu query filtra por organización de ventas mediante analysis authorizations, y ya vimos que
las **variables de autorización no sobreviven al transfer**. Datasphere tampoco tiene
analysis authorizations: tiene **Data Access Controls**. Hay puente: la transacción
`RSDWC_DAC_RSEC_GEN` exporta tus autorizaciones a una tabla de permisos, `RSDWC_RSEC_DAC`,
que se importa a Datasphere y genera una cláusula de filtro donde el usuario de BW se
sustituye por el de Datasphere —por correo electrónico, con un BAdI si tu lógica es otra—,
más una vista de permisos y el DAC.

**Qué validar:** los **comodines**. En BW se usan a manos llenas y los Data Access Controls
no los soportan; toda autorización basada en patrones hay que resolverla en valores. La
granularidad por objeto: dentro de un mismo espacio no puedes restringir un modelo
analítico a un grupo de usuarios, así que la separación se hace **por espacio** y eso
reordena tu diseño. Y la prueba que nadie hace: entrar con el usuario de un gerente
regional y confirmar que ve exactamente lo mismo que veía —ni una fila más.

### Estación 6 — Y hasta entonces, el dato para IA

Solo aquí entra el **Data Product Generator**, que es otra cosa y sirve para otra cosa:
publica InfoProviders —InfoObjects, aDSOs, CompositeProviders, MultiProviders, InfoCubes y
queries usadas como InfoProvider— hacia tablas de solo lectura en el object store, con una
tarea de consolidación que mantiene la consistencia contra el origen y deltas para
CompositeProviders y MultiProviders. De ahí sale, por delta share, el dato para
Databricks. **Qué validar:** todo lo de la sección del contrato. Este es el punto donde
aplica.

## Lo que hay que pedir antes de firmar

Cuatro cosas que valen más que el descuento:

1. **La lectura de "enriquecido", por escrito.** Si tu arquitectura depende de que un dato
   transformado deje de ser data product, que lo diga el contrato y no una llamada.
2. **El costo modelado a 24 meses con la caducidad mensual puesta** —y con la población de
   Excel de la estación 4 dentro del modelo, no fuera.
3. **Una cláusula de portabilidad de la semántica.** Forrester lo dijo en mayo con más
   crudeza que yo: SAP está construyendo un *control plane* de datos para IA, y la ventana
   para negociar es de doce a veinticuatro meses, antes de que los agentes congelen esas
   decisiones.
4. **La lista de la nota 2932647, en su versión vigente, cruzada contra tus queries
   reales** —no cuántas tienes: cuántas usan features que se van a omitir en silencio—, y
   **la lista equivalente para el Query Template Generator**, que hoy no está publicada. Ese
   par de números es tu proyecto.

Aquí en el noreste esto no es abstracto. Las operaciones de manufactura y consumo masivo de
la región llevan veinte años metiendo reglas dentro de queries de BW: cómo se reconoce una
venta, cómo se prorratea un flete, qué cuenta como devolución. Ese acervo es lo que se está
negociando, aunque el contrato hable de capacidad y el diagrama hable de fases.

Business Data Cloud probablemente sea el destino. La parte que decides tú es el calendario
—y con BW/4HANA, el calendario lo tienes tú.

---

## Fuentes

- **SAP.** *SAP BW/4HANA to extend maintenance in alignment with SAP Business Suite and SAP
  S/4HANA.* Anuncio oficial: la **línea de producto** BW/4HANA se mantiene hasta finales de
  2040, alineada con S/4HANA e incluyendo on-premise, entregada mediante una secuencia de
  releases. ⚠️ **Distinción crítica:** el compromiso de 2040 es de línea, no de release. El
  release **BW/4HANA 2023** tiene mantenimiento mainstream hasta el **31-dic-2030**. Las
  fechas por release están en la KBA 2934895 (*Maintenance for SAP BW/4HANA*, cubre 1.0,
  2.0, 2021 y 2023) y en el Product Availability Matrix; el texto completo requiere sesión
  en SAP for Me. **Confirmar ambas fechas en el PAM antes de publicar.**
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-bw-4hana-to-extend-maintenance-in-alignment-with-sap-business-suite-and/ba-p/13457952
- **SAP.** *SAP Business Planning and Consolidation (SAP BPC) Strategy Update*, blog oficial,
  8 de octubre de 2025. BPC 10.1 NW y BPC 2021 pueden moverse a la nube privada **junto con**
  el sistema BW; BPC 2021 soporta BW/4HANA 2021 y 2023 con fin de mantenimiento al
  **31-dic-2030**; y el compromiso hasta 2040 se formula como *"there will always be a
  corresponding SAP BPC/4HANA product version which supports the latest SAP BW/4HANA
  release. The corresponding release name will be communicated in a timely manner."*
  ⚠️ Pendiente: verificar si existe un release **BPC 2023** posterior a este blog y su fecha
  propia en el PAM.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-planning-and-consolidation-sap-bpc-strategy-update/ba-p/14237803
- **SAP Architecture Center.** *Modernizing SAP BW with SAP Business Data Cloud*
  (ref-arch 6550e4). Prerrequisitos por release, detalle del Data Product Generator y sus
  InfoProviders soportados, y la marca *(planned)* del Query Template Generator.
  https://architecture.learning.sap.com/docs/ref-arch/6550e4
- **SAP Learning.** *Outlining the Capabilities of the Query Template Generator* y
  *Outlining the Configuration of the Query Template Generator*, curso *Transforming SAP BW
  with SAP Business Data Cloud*, publicados el **30 de julio de 2026**. Proceso de dos pasos,
  objetos generados (dimensiones, fact view, analytic model), transacción `RSDWCTG_ADMIN`,
  BW Modeling Tools 1.27 PL3, objeto de autorización S_ADT_RES, y la lectura completa de la
  definición de la query incluyendo fórmulas y variables.
  https://learning.sap.com/courses/transforming-sap-bw-with-sap-business-data-cloud/outlining-the-capabilities-of-the-query-template-generator_a2bfd608-4246-4255-8ea9-2d250e90de91
- **SAP.** *SAP Business Data Cloud — Supplemental Terms and Conditions*, versión 7-2026,
  documento público. Secciones 1.11, 2.4, 2.6.4, 3.1–3.7 y 6.2.5.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v7-2026.pdf
- **SAP.** *SAP Business Data Cloud Supplement*, versión 10-2025, secciones 3.2.2 y 3.2.4:
  *"Unused Capacity Units may not be carried over into any subsequent month"* y la no
  prorrateabilidad en meses parciales.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v10-2025.pdf
- **Raver, B. (SAP).** *Breaking Down the SAP BDC Pricing Model*, 16 de abril de 2026,
  presentación a los SAP user groups. Valores de capacity unit de SAC por tramo, la regla de
  vender siempre con al menos una Intelligent Application y el mínimo de 640 capacity units.
  https://assets.dm.ux.sap.com/sap-user-groups/pdfs/260416_breaking_down_the_sap_bdc_pricing_model.pdf
- **SAP.** Nota **2932647**, *Supported and unsupported features with SAP BW/4HANA / SAP BW
  Bridge Model Transfer in SAP Datasphere*, **versión 18, 18 de diciembre de 2025**
  (componente DS-BB). **Fuente primaria de la estación 2.** De aquí salen la regla general de
  omisión silenciosa, los cuatro bloqueantes duros, las listas de features soportados y no
  soportados por nivel —query, CompositeProvider e InfoObject—, la desconexión por diseño del
  modelo transferido y el aplanamiento y congelamiento de jerarquías. La propia nota advierte
  que la funcionalidad se libera en oleadas y que la lista cambia con el tiempo: verificar la
  versión vigente antes de estimar. Requiere sesión en SAP for Me.
  https://me.sap.com/notes/2932647
  Relacionada: nota **3478268**, *Releasing The Hierarchy Functionality For The Export Of
  Metadata To Datasphere*, que habilita el soporte de jerarquías descrito arriba.
- **SAP / comunidad SAP.** *Part 2 – Import SAP BW/4HANA Queries into SAP Datasphere using
  SAP BW/4HANA Model Transfer.* Caso documentado de referencia: una sola query genera 63
  objetos entre dimensiones, textos, jerarquías, fact view y modelo analítico.
  https://community.sap.com/t5/technology-blog-posts-by-sap/part-2-import-sap-bw-4hana-queries-into-sap-datasphere-using-sap-bw-4hana/ba-p/13759521
- **SAP Learning.** *Introducing Model Transfer* (learning journey *Modernizing your data
  warehouse landscape from SAP BW to SAP Datasphere*). Transacción `RSDWC_QUERY`, el rol de
  BW como fuente remota con cálculo en los motores de HANA de Datasphere, el traspaso de
  analysis authorizations vía `RSDWC_DAC_RSEC_GEN` y la tabla `RSDWC_RSEC_DAC`, y la
  sustitución de fuentes BW por objetos de Datasphere en historias existentes de SAC.
  https://learning.sap.com/learning-journeys/modernizing-your-data-warehouse-landscape-from-sap-bw-to-sap-datasphere/introducing-the-hybrid-approach
- **SAP.** KBA **3297935**, *SAP Datasphere Analytic Models and some Views are not shown in
  AO*, y KBA **2436382**, *Analysis for Office connections (BW – BW/4HANA – HANA – BIP – SAC
  – Datasphere)*. Alcance de Analysis for Office sobre Datasphere: vistas y perspectivas sí,
  modelos analíticos no; el camino soportado para modelos analíticos en Excel es el add-in de
  SAP Analytics Cloud. ⚠️ Verificar contra la versión y SP en uso antes de decidir.
  https://userapps.support.sap.com/sap/support/knowledge/en/3297935
- **Comunidad SAP.** *Working with BW Authorizations in Datasphere on Enterprise Level* y
  *BW-Like Authorizations in Datasphere*. Los Data Access Controls no soportan comodines, y
  dentro de un mismo espacio no se puede restringir un modelo analítico por grupo de
  usuarios: la separación se hace por espacio. Contribuciones de miembros, no documentación
  oficial; validar contra el estado actual del producto.
  https://community.sap.com/t5/technology-blog-posts-by-members/working-with-bw-authorizations-in-datasphere-on-enterprise-level/ba-p/14302361
- **Databricks.** *Share data between SAP Business Data Cloud (BDC) and Databricks*,
  documentación oficial, última actualización 4 de agosto de 2026. Delta Sharing y la
  cláusula de divulgación de información de uso a SAP por workload.
  https://docs.databricks.com/aws/en/opensharing/sap-bdc/
- **Databricks.** *Unlocking SAP business context in Databricks with semantic metadata Delta
  Sharing*, 30 de abril de 2026. Disponibilidad general del sync de metadatos semánticos
  hacia Unity Catalog. Fuente de proveedor sobre su propio producto.
  https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
- **SAPinsider.** *Modernizing SAP BW: The Path to Business Data Cloud*, 21 de mayo de 2025.
  Dominik Kurz (SAP) citado con la cifra de 20,000 a 30,000 clientes en BW 7.5 y el ejemplo
  de reducción de 8 TB a 2 TB.
  https://sapinsider.org/analyst-insights/modernizing-sap-bw-the-path-to-business-data-cloud/
- **Forrester.** *SAP Is Targeting The AI Data Control Plane*, 14 de mayo de 2026. El
  posicionamiento de BDC como plano de control de datos para IA y la ventana de 12 a 24
  meses para decidir.
  https://www.forrester.com/blogs/sap-is-targeting-the-ai-data-control-plane/
