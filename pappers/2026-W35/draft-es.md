# El reloj que no es tuyo

*Te van a vender la migración a Business Data Cloud con una fecha en rojo. Si ya estás en BW/4HANA esa fecha no es la tuya —y el documento que sí deberías leer está publicado, es gratis y casi nadie lo abre.*

**Brújula · Edición 08 · W35**
*Arquitectura de Datos · SAP*

---

Todas las presentaciones empiezan igual. Una línea de tiempo, una fecha en rojo y una
flecha hacia arriba: **31 de diciembre de 2027**, fin del mantenimiento mainstream de SAP
BW NetWeaver 7.5. La fecha es real y el problema es enorme —en Sapphire 2025 el propio
product management de SAP habló de **entre 20,000 y 30,000 clientes** todavía en esa
versión. Para ellos la propuesta es buena: mover el sistema tal como está a **SAP BW,
private cloud edition** dentro de BDC y ganar tres años, hasta fin de 2030, sin proyecto
de conversión.

Si ya estás en **BW/4HANA**, esa no es tu fecha. Y aquí hay que leer con cuidado, porque
el dato circula mal en las dos direcciones.

SAP alineó **la línea de producto** BW/4HANA con la de S/4HANA hasta finales de **2040**,
y ese compromiso cubre el despliegue on-premise. Pero está redactado como promesa de
línea, entregada *"through a sequence of releases"*. Tu **release** tiene su propia fecha:
BW/4HANA **2023** salió a disponibilidad general el **30 de octubre de 2023** y su
mantenimiento mainstream termina el **31 de diciembre de 2030**. No es interpretación: es
lo que dice el Product Availability Matrix, que es la fuente oficial y la única que vale
para esto. Siete años de ciclo, de los que ya van casi tres.

Y si además corres **BPC**, el tren va en pareja. SAP BPC 2021 para BW/4HANA salió en
noviembre de 2021 y BW/4HANA 2023 dos años después, pero **los dos terminan el mismo día:
31 de diciembre de 2030**. Dos productos, un solo reloj.

Cómo llegó ahí explica el mecanismo. En enero de 2023 la tabla de PAM que SAP publicaba en
su propio blog daba a BPC 2021 la fecha de **31.12.2027**, con la promesa de anunciar más
cerca de 2027 qué versión seguiría. Hoy el PAM dice 2030: la promesa se cumplió
**extendiéndole la fecha al release que ya existía**, no sacando uno nuevo. No hay un "BPC
2023". Y eso es exactamente lo que significa un compromiso de línea entregado *"through a
sequence of releases"*: tu fecha es real, y también es revisable por quien la puso.

Ni el pánico de 2027 ni la calma de 2040. **Cuatro años y cuatro meses de pista en lo que
tienes hoy**, y un camino comprometido más allá mediante upgrades sucesivos.

Y ahí está lo que la línea de tiempo en rojo esconde: **un upgrade de BW/4HANA es un
proyecto técnico. Un movimiento a Business Data Cloud es un cambio de contrato, de modelo
de consumo y de régimen del dato.** No están en la misma categoría, y elegir el segundo
por miedo al primero sale caro.

Sin la urgencia prestada quedan tres preguntas que sí valen: **de dónde va a venir tu
dato, qué firmas, y cuánto cuesta de verdad.**

## Lo que sí ganas, dicho sin adorno

Empiezo por ahí porque el resto es incómodo y no quiero que se lea como una postura.

**Conservas el activo.** El movimiento es un *lift* **as-is**: el sistema se levanta y se
deja caer en la nube de SAP tal como está, sin convertir nada. Quince años de lógica de
negocio y de reglas que nadie documentó completas siguen ahí. **Y BPC se mueve junto con
el sistema** —justo la pieza que suele descarrilar estos proyectos, y aquí no lo hace.

**La infraestructura por fin se encoge.** El volumen grande baja al object store
—almacenamiento barato de archivos, fuera de memoria— y la máquina se dimensiona por uso
real. SAP documenta el caso de pasar de 8 TB de memoria a 2 TB.

**Mueves capacidad sin renegociar.** Los servicios de BW dentro de BDC caen bajo el
contrato de BDC y no bajo RISE: achicar BW y reasignar lo liberado a Datasphere, SAC o
Databricks se hace en autoservicio.

**Y la brecha técnica se cierra rápido.** En enero de 2026 el reproche más citado era que
los *data products* —los paquetes de datos curados que BDC publica— viajan en Parquet, un
formato que no carga significado. El 30 de abril salió en disponibilidad general la
sincronización de metadatos semánticos hacia Unity Catalog, el catálogo de gobierno de
Databricks: cuatro meses entre la crítica y el cierre. Cualquier objeción puramente técnica
que escriba hoy tiene fecha de caducidad.

Las que no se han movido en dieciocho meses son las otras dos.

## De dónde viene el dato: la puerta que casi nadie revisa

El contenido premium de BDC son los **data products administrados por SAP** y las
**Intelligent Applications**. Y existen bajo una condición que no aparece en las
portadas: **tu ERP tiene que estar en la nube de SAP.**

El FAQ oficial lo dice sin rodeos. BDC soporta las ediciones cloud de S/4HANA
—private cloud edition y public cloud— y ahí los data products administrados están
*"exclusively available"*. Sobre el resto: *"there are no immediate plans to extend
support to on-premise S/4HANA systems"*. Los sistemas on-premise obtienen, en cambio, una
opción customer-managed: conectan y meten su dato, pero el catálogo administrado no les
aplica.

No es una limitación teórica. Existe la KBA **3786663**: *"S/4HANA on premise system is not
listed in formation"*. Una *formation* es la agrupación de sistemas que se registran juntos
para que BDC los reconozca como un paisaje, y el sistema on-premise simplemente **no
aparece** ahí. Entre las palabras clave de la KBA está *integration not supported*: no es un
problema de configuración, es diseño.

**Y ECC no aparece como fuente de data products administrados en ningún lado.** Aparece en
el roadmap: catalog crawling en Q2-2026, ingesta directa hacia SAP Databricks en 2026. Las
dos, plan.

Lo demás entra por otra tubería. La conectividad de Datasphere sí acepta S/4 on-premise,
ECC, campos Z —los que tu propia gente le agregó a las tablas estándar—, CDS views propios
y fuentes no-SAP: Oracle, SQL Server, Salesforce, object stores, Snowflake, BigQuery. Pero
todo eso aterriza como **data product propio**, en el object store de Datasphere, distinto
del de Foundation Services donde SAP guarda los suyos. Dos mundos que no se cruzan.

El tamaño del catálogo también conviene mirarlo. A principios de 2026 había **259 data
products estándar** en disponibilidad general, **la mayoría de datos maestros**, con **tres
sistemas fuente**: S/4HANA private, S/4HANA public y SuccessFactors. El discurso menciona
además Ariba, Concur y Fieldglass; el inventario, no. Y no hace falta creerle a nadie: SAP
publica el catálogo en el Discovery Center, se consulta sin cotizar, y lo único que hay que
hacer es filtrar por tu sistema fuente **antes** de mirar el total.

### El único reloj que sí es tuyo, y vence este año

Para entender por qué la arquitectura es así hay que mirar la puerta que se cerró antes
—y la que se está cerrando ahora mismo.

ODP —*Operational Data Provisioning*— es el marco por el que, durante más de una década,
cualquier herramienta externa sacó dato de un sistema ABAP: los extractores de ECC, los
DataSources de BW, todo salía por ahí. La nota **3255746** viene desde 2022, cuando SAP
advirtió que esas APIs eran internas y no soportadas. En su versión de febrero de 2024
pasó de advertencia a prohibición —clientes y aplicaciones de terceros **ya no tienen
permitido** usarlas— y dirigió a los clientes a Datasphere para replicar hacia
herramientas de terceros. La nota va hoy en su **versión 11, del 21 de abril de 2026**.

Y en **junio de 2026 la prohibición dejó de ser contractual y pasó a ser técnica**: un
parche de seguridad valida las llamadas entrantes y **bloquea** las que vienen de
aplicaciones no autorizadas contra S/4HANA, BW y ECC. Queda un **opt-out temporal que
permite que esas llamadas sigan funcionando hasta fin de 2026**, y desde el **13 de abril
de 2026** SAP publica una herramienta de autoevaluación —nota **3439624**— que inventaría
todo el uso de ODP-RFC en el paisaje.

Léelo contra el resto del papper. La fecha en rojo que te presentan es 2027 o 2030, y es el
reloj del release de alguien más; **esta lleva tu nombre y vence en diciembre**. El ejercicio
de esta semana no es dibujar un roadmap a 2030: es correr la 3439624 y contar cuántas
tuberías propias dependen hoy de una puerta que ya está cerrada y sostenida con un opt-out.

El camino histórico para sacar dato de ABAP hacia un lago propio se cerró primero; el nuevo
tiene contrato, métrica y precio. Ese orden no es casualidad, y explica todo lo que sigue.

## El documento que nadie abre

Los términos de BDC son públicos y se descargan sin registro del Trust Center. La versión
vigente —la séptima de 2026— tiene párrafos que valen más que cualquier demo. Empiezo por
el que decide arquitectura, la sección 3.3:

> *"Customer may allow Third-Party Connectors to temporarily store or materialize Data
> Products on such Third Party Connectors' systems solely for performance optimization
> purposes. For the avoidance of doubt, Customer may not allow Third-Party Connectors'
> systems to distribute Data Products to systems other than SAP Business Data Cloud."*

En corto: puedes compartir un data product con tu propio Databricks, y ahí puede quedarse
copiado **temporalmente y solo para que las consultas corran más rápido**. Lo que ese
Databricks no puede hacer es **repartirlo hacia adelante**. Power BI, Tableau, un lago
externo, otro tenant: todos quedan del lado equivocado de la frase. Tu lakehouse deja de ser
la capa desde donde todo se sirve y pasa a ser un consumidor autorizado, no un
redistribuidor.

Ojo con la consecuencia para quien ya mueve dato con herramientas propias: **cambiar tu
pipeline por *zero-copy*** —compartir el dato donde ya está, sin moverlo ni duplicarlo— **no
es cambiar de tubo, es cambiar el régimen del dato.** Lo que hoy es tuyo y redistribuyes
libremente, mañana es un objeto licenciado.

El argumento que circula entre consultores para librar la restricción es que un dato
suficientemente transformado ya deja de ser data product. Ojalá. La sección 1.11 define
*Data Product* como *"enriched data or enriched Customer Data, where enrichment is any
type of reorganization, semantics, summarization, reporting or metadata"*. El
enriquecimiento no es lo que te saca de la definición: es lo que te mete en ella. Puede
que SAP acepte esa lectura en tu caso; no está en el texto. Si tu arquitectura depende de
ella, pídela por escrito antes de diseñar.

Tres párrafos más antes del datasheet:

- **3.5.** SAP se declara dueño de la propiedad intelectual de los data products; tú
  tienes licencia de uso.
- **3.6.** Usar un conector de tercero **es consentir** que SAP y ese tercero intercambien
  información de uso, *"including identifying Customer"*. La documentación de Databricks
  —actualizada el 4 de agosto de 2026— es más específica: puede revelar a SAP el volumen
  de datos de BDC y su proporción frente a los no-BDC, y **el precio efectivo que tu
  organización paga por consumo de Databricks**, por workload y sin anonimizar.
- **2.6.4.** Los servicios de BDC Connect están clasificados como **Grupo 2**: si SAP
  deprecia un servicio de Grupo 1 lo sigues usando el resto de tu suscripción; si es de
  Grupo 2, al vencer el aviso de seis meses **pierdes el acceso**. El puente hacia tu
  propio Databricks es, por contrato, la pieza apagable.

## Las capacity units no se guardan

BDC se vende en **capacity units**: fichas reasignables entre Datasphere, SAC, BW en nube
privada y Databricks. Hacia adentro la flexibilidad es real. Hacia afuera, tres reglas.

**Lo que no gastas se pierde.** Una sola frase —*"Unused Capacity Units may not be carried
over into any subsequent month"*— y la aclaración de que tampoco se prorratean por meses
parciales. No es el vencimiento anual de los créditos de BTP: es mensual. Presupuestas por
año y consumes por mes. Esta cláusula la cito del Supplement de **octubre de 2025**, no de
la versión vigente; el documento cambia varias veces al año, así que confírmala en la
versión exacta que te pongan a firmar.

**El contrato trae una errata declarada.** La sección 2.4 aclara que donde el Order Form
dice que la métrica de uso muestra el máximo utilizable en doce meses, *"includes a
drafting error"* y debe leerse **un mes**.

Antes de los números, lo que los hace legibles: **SAP no publica el precio de una capacity
unit.** Lo que sigue no son pesos ni dólares, son fichas —sirven para comparar un producto
contra otro y un tramo contra otro, no para estimar una factura.

**Y SAP Analytics Cloud vuelve a cotizarse por usuario:** **25.60** capacity units por
usuario de BI al mes en el tramo de 25 a 200, bajando a **10.54** arriba de 5,000. Los
números de planeación son otra liga: **72.85** por usuario en planning estándar y
**820.43** en planning profesional. Si tu horizonte incluye mover planeación de BPC a SAC
—que es la dirección declarada de SAP, y que **no es migración sino reimplementación**—
esos son los renglones que deciden el caso. Además BDC Core *"must always be sold in
conjunction with at least one Intelligent Application"*, y la implementación mínima viable
que la propia SAP presenta arranca en **640 capacity units**.

Cruza esa regla con la sección anterior y sale algo incómodo: todas las Intelligent
Applications que SAP publica tienen como aplicación fuente un producto cloud. Un cliente
con ERP on-premise queda obligado a comprar al menos una aplicación inteligente **que su
ERP no puede alimentar**. Es una inferencia mía cruzando dos documentos, no una
declaración de SAP —y es exactamente la pregunta que hay que hacer por escrito.

## Y esto, desde aquí, se ve distinto

Escribo desde Monterrey, y el caso que acabo de describir no es un caso de borde: es el
caso de buena parte del parque instalado de la región. Operaciones grandes de manufactura
y consumo masivo, con ECC todavía en piso, migración a S/4 planeada para 2027 o 2028, y
veinte años de reglas de negocio viviendo dentro de queries de BW —cómo se reconoce una
venta, cómo se prorratea un flete, qué cuenta como devolución.

Para ese perfil, BDC entrega su valor premium **después** de la migración a S/4, no antes.
La arquitectura de referencia está escrita para un paisaje que la mayoría todavía no
tiene. Lo cual convierte a Business Data Cloud, para gran parte del mercado local, en
**una decisión de 2028 disfrazada de urgencia de 2026**.

Eso no significa quedarse quieto. Significa separar los relojes: el de tu release, el de
tu ERP, y el de las herramientas que sí tienen fecha corta. Rara vez es el mismo.

## Lo que hay que pedir antes de firmar

Cuatro cosas que valen más que el descuento:

1. **La lectura de "enriquecido", por escrito.** Si tu arquitectura depende de que un dato
   transformado deje de ser data product, que lo diga el contrato y no una llamada.
2. **Qué obtienes hoy con el ERP que hoy tienes.** Si tu ERP es on-premise, que te listen
   por nombre los data products administrados a los que sí tendrías acceso. Y que expliquen
   qué Intelligent Application vas a comprar y con qué la vas a alimentar.
3. **El costo modelado a 24 meses con la caducidad mensual puesta**, incluyendo la
   población de planeación si BPC va camino a SAC.
4. **Una cláusula de portabilidad de la semántica.** Forrester lo dijo en mayo con más
   crudeza que yo: SAP está construyendo un *control plane* de datos para IA —la capa que
   decide quién puede leer qué y con qué significado— y la ventana para negociar es de doce
   a veinticuatro meses, antes de que los agentes congelen esas decisiones en sistemas de
   trabajo.

Business Data Cloud probablemente sea el destino. La parte que decides tú es el calendario
—con una excepción, la que abrimos a la mitad: el pedazo de calendario que ya no decides es
ODP, y ese vence en diciembre.

*La próxima edición sigue a una query de ventas concreta —de BW a SAC— estación por
estación, con lo que hay que validar en cada una y lo que se pierde en el camino sin que
nadie avise.*

---

## Fuentes

- **SAP.** *Product Availability Matrix — SAP BW/4HANA 2023.* **Fuente oficial y primaria
  de las fechas.** Release to Customer y disponibilidad general el 30-oct-2023; fin de
  mantenimiento mainstream el **31-dic-2030**. Requiere sesión en SAP for Me.
  https://userapps.support.sap.com/sap/support/pam
- **SAP.** *Product Availability Matrix — SAP BPC 2021, for SAP BW/4HANA.* RTC y
  disponibilidad general el 01-nov-2021; fin de mantenimiento mainstream el **31-dic-2030**,
  la misma fecha que BW/4HANA 2023. Contrasta con la tabla de PAM que SAP publicó en enero
  de 2023, que daba 31.12.2027 para ese mismo producto: la extensión se hizo sobre el
  release existente. Requiere sesión en SAP for Me.
  https://userapps.support.sap.com/sap/support/pam
- **SAP.** *SAP BW/4HANA to extend maintenance in alignment with SAP Business Suite and SAP
  S/4HANA.* La **línea de producto** BW/4HANA se mantiene hasta finales de 2040, alineada
  con S/4HANA e incluyendo on-premise, entregada mediante una secuencia de releases. El
  compromiso de 2040 es de línea; la fecha del release está en el PAM, arriba.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-bw-4hana-to-extend-maintenance-in-alignment-with-sap-business-suite-and/ba-p/13457952
- **SAP.** *Maintenance timelines for SAP Business Planning and Consolidation (SAP BPC)*,
  blog oficial. Tabla con fechas de PAM por versión y la explicación del mecanismo de
  releases sucesivos: *"as we approach 2027, we will share which version of SAP BPC for SAP
  BW/4HANA will be available beyond 2027"*.
  https://community.sap.com/t5/financial-management-blog-posts-by-sap/maintenance-timelines-for-sap-business-planning-and-consolidation-sap-bpc/ba-p/13551547
- **SAP.** *SAP Business Planning and Consolidation (SAP BPC) Strategy Update*, 8 de octubre
  de 2025. BPC 10.1 NW y BPC 2021 pueden moverse a la nube privada **junto con** el sistema
  BW; BPC 2021 soporta BW/4HANA 2021 y 2023 con fin de mantenimiento al 31-dic-2030.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-planning-and-consolidation-sap-bpc-strategy-update/ba-p/14237803
- **SAP.** *SAP Business Data Cloud — FAQs*, blog oficial. Ediciones de S/4HANA soportadas y
  la frase *"SAP-managed Data Products are exclusively available"* para private y public
  cloud, con *"no immediate plans to extend support to on-premise S/4HANA systems"*.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-data-cloud-faqs/ba-p/14022781
- **SAP.** KBA **3786663**, *[BDC-FOS] S/4HANA on premise system is not listed in
  formation*. El sistema on-premise no aparece en la lista de formations; palabra clave
  *integration not supported*.
  https://userapps.support.sap.com/sap/support/knowledge/en/3786663
- **SAP.** Nota **3255746**, *Unpermitted usage of ODP*. Prohibición de uso de las APIs de
  ODP por clientes y terceros para acceder a fuentes ABAP, y redirección a Datasphere.
  Versión 11 del 21 de abril de 2026. Requiere sesión en SAP for Me.
  https://me.sap.com/notes/3255746
- **SAP.** Nota **3439624**, herramienta de autoevaluación del uso de ODP-RFC en el paisaje,
  publicada el 13 de abril de 2026. Requiere sesión en SAP for Me.
  https://me.sap.com/notes/3439624
- **SAPinsider.** *SAP Note 3255746: The June 2026 ODP-RFC Deadline Explained.* Publicación
  de industria, no de proveedor: fecha del parche de seguridad de junio de 2026 que bloquea
  las llamadas ODP-RFC no autorizadas contra S/4HANA, BW y ECC; opt-out temporal vigente
  hasta fin de 2026; versión 11 de la nota y referencia a la 3439624. ⚠️ Confirmar el
  alcance exacto del opt-out en la propia nota antes de comprometerlo con un cliente.
  https://sapinsider.org/blogs/sap-note-3255746-odp-rfc-deadline-2026/
- **SAP.** *SAP Business Data Cloud — Supplemental Terms and Conditions*, versión 7-2026,
  documento público. Secciones 1.11, 2.4, 2.6.4, 3.1–3.7 y 6.2.5.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v7-2026.pdf
- **SAP.** *SAP Business Data Cloud Supplement*, versión 10-2025, secciones 3.2.2 y 3.2.4:
  *"Unused Capacity Units may not be carried over into any subsequent month"*.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v10-2025.pdf
- **Raver, B. (SAP).** *Breaking Down the SAP BDC Pricing Model*, 16 de abril de 2026,
  presentación a los SAP user groups. Valores de capacity unit de SAC por tramo, planning
  estándar y profesional, la regla de vender siempre con al menos una Intelligent
  Application y el mínimo de 640 capacity units.
  https://assets.dm.ux.sap.com/sap-user-groups/pdfs/260416_breaking_down_the_sap_bdc_pricing_model.pdf
- **Expertum.** *SAP Business Data Cloud: Reflections After One Year of Data Products*,
  8 de enero de 2026. Conteo de 259 data products estándar, mayoría de datos maestros, y los
  tres sistemas fuente soportados. Dato fechado en enero de 2026 y de un socio de
  implementación, no de SAP: en el texto se cita con su fecha y se remite al catálogo oficial.
  https://expertum.net/sap-bdc-reflections-after-one-year/
- **SAP.** *SAP BDC Catalog*, Discovery Center. Catálogo público de data products, consultable
  sin cotizar y filtrable por sistema fuente. Es la fuente que le permite al lector contar el
  inventario vigente el día que lo necesite, en vez de heredar el conteo de un tercero.
  https://discovery-center.cloud.sap/bdcCatalog
- **Databricks.** *Share data between SAP Business Data Cloud (BDC) and Databricks*,
  documentación oficial, última actualización 4 de agosto de 2026.
  https://docs.databricks.com/aws/en/opensharing/sap-bdc/
- **Databricks.** *Unlocking SAP business context in Databricks with semantic metadata Delta
  Sharing*, 30 de abril de 2026. Fuente de proveedor sobre su propio producto.
  https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
- **SAPinsider.** *Modernizing SAP BW: The Path to Business Data Cloud*, 21 de mayo de 2025.
  Dominik Kurz (SAP) con la cifra de 20,000 a 30,000 clientes en BW 7.5 y el ejemplo de
  reducción de 8 TB a 2 TB.
  https://sapinsider.org/analyst-insights/modernizing-sap-bw-the-path-to-business-data-cloud/
- **Forrester.** *SAP Is Targeting The AI Data Control Plane*, 14 de mayo de 2026.
  https://www.forrester.com/blogs/sap-is-targeting-the-ai-data-control-plane/
