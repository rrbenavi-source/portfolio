# Brújula · Edición 12 — material listo para copiar y pegar

**Publicación: martes 22 de septiembre de 2026, 9:00 AM CDMX.**
Artículo en el portfolio: https://rrbenavi-source.github.io/portfolio/publicaciones/quitamos-bw-el-motor-se-quedo

Sigue la línea SAP de las ediciones 08–11, pero baja un piso: de la puerta de salida del dato a lo que pasa cuando decides quedarte adentro y reportear directo desde el ERP. Es la primera edición con código CDS en tres de las cuatro figuras.

---

## Checklist

1. Crear la edición nueva en el editor de newsletter de LinkedIn.
2. Pegar **título** y **subtítulo** (abajo).
3. Subir la **portada**: `brujula-cover-12.png` (1920×1080).
4. Pegar el **cuerpo** entre los separadores, respetando las cuatro marcas `[ Sube la figura N: … ]`.
5. Los tres bloques de código van como texto plano (LinkedIn no tiene formato de código); la figura 2 los muestra con formato, así que si se ven mal, borrarlos y dejar la figura.
6. Subir las **cuatro figuras** en su posición, con el **alt text** que viene más abajo.
7. Llenar los campos de **SEO** (título y descripción).
8. Publicar, y de inmediato hacer el **post de lanzamiento** en el feed.
9. Poner el **primer comentario** con los links. LinkedIn penaliza los links externos en el cuerpo del post.

---

## Título

Quitamos BW. El motor se quedó.

## Subtítulo

Un cliente apagó BW y BusinessObjects al migrar a S/4HANA y hoy reporta directo a SAP Analytics Cloud. Funciona. Pero cada query la sigue corriendo el motor analítico de BW, ahora dentro del ERP. Y el trabajo que hacía el universo de BO no desapareció: hay que volverlo a escribir en vistas CDS, con anotaciones, y probarlo en RSRT antes de que nadie abra un dashboard.

## SEO — título

Quitamos BW: reportear de S/4HANA a SAC con CDS, sin perder el motor

## SEO — descripción

Un cliente apagó BW y BusinessObjects y reporta directo a SAC. Cada query la sigue corriendo el motor de BW, embebido en S/4HANA. Tres capas, ocho anotaciones y RSRT como puerta de calidad.

---

## Alt text de las imágenes

**Figura 1 — fig-motor.png:** Dos cadenas lado a lado: antes, reporte de Web Intelligence, query BEx, motor OLAP de BW, InfoProviders y extractores desde ECC, con todo apagado menos el motor; hoy, story de SAC, transient query 2C, analytic engine embebido, cubo CDS y tablas de S/4HANA, con el motor marcado como el mismo.

**Figura 2 — fig-tres-capas.png:** Tres tarjetas con código CDS: la dimensión con @Analytics.dataCategory #DIMENSION y representativeKey, el cubo con #CUBE, asociación a la dimensión, moneda y agregación por defecto, y la query con @Analytics.query true y las anotaciones de AnalyticsDetails; el nombre 2CZCSALESQ marcado como el que se busca en RSRT.

**Figura 3 — fig-anotaciones.png:** Lista de ocho anotaciones CDS para reportear en SAC, con la columna de qué se rompe cuando falta cada una: dataCategory, query, representativeKey, text, currencyCode y unitOfMeasure, DefaultAggregation, AnalyticsDetails.query y authorizationCheck.

**Figura 4 — fig-universo.png:** El semantic layer que vivía en el universo de BO y la query de BEx tiene dos destinos: la vista CDS, una vez, o cada story, cada vez. Debajo, los cuatro hallazgos del cuadre BO contra SAC: filtros no identificados, redondeo, el año histórico y la lógica en la story.

---

## CUERPO — copiar de aquí

Un cliente con el que trabajamos venía de la foto más común de la industria de aquí, de Nuevo León, y de media república: ECC como ERP, BW 7.3 como data warehouse y BusinessObjects como capa de reportes. Tres sistemas, y en cada uno un lugar distinto donde una cifra podía cambiar de significado. BW 7.3 lleva fuera de mantenimiento desde finales de 2020 y BusinessObjects 4.3 termina el suyo el 31 de diciembre de este año, así que la migración a S/4HANA era también el momento de decidir qué hacer con los otros dos.

Decidieron algo que cada vez veo más seguido por acá: quitar los dos. Sin BW, sin BO. S/4HANA expone el dato a través de vistas CDS y SAP Analytics Cloud (SAC) lo consume, la mayoría de las veces con conexión live, unas pocas por import. Un solo sistema de origen y el ERP como única verdad.

Es una decisión que se defiende sola, y la volvería a firmar. Pero hay dos cosas que conviene decir en voz alta antes de firmarla, porque ninguna sale en la presentación del vendedor. La primera es que el motor de BW no se fue a ningún lado. La segunda es que el universo de BusinessObjects tampoco: se quedó, nomás que en forma de deuda.

Lo que pasa cuando marcas una vista

En S/4HANA, una vista CDS se vuelve consumible desde SAC en el momento en que le pones una anotación: @Analytics.query: true. La documentación de SAC lo dice derecho: solo las vistas que llevan esa anotación aparecen en la conexión live. Lo que no dice tan fuerte es lo que pasa atrás.

Al activar la vista, el sistema genera una transient query, una query analítica que no diseñaste en ningún editor y que vive con el nombre 2C más el nombre SQL de tu vista. Esa query no la ejecuta HANA directamente. La ejecuta el analytic engine que viene embebido en cualquier S/4HANA: el mismo motor OLAP que corre las queries de BEx en un BW. SAC le habla por el protocolo InA, el mismo que ya usaban Design Studio y las herramientas de BusinessObjects para consultar HANA y BW. Y la transacción para probarla es RSRT, la misma que cualquier consultor de BW ha abierto diez mil veces.

Por eso digo que quitamos BW y el motor se quedó. No es una metáfora. Es la arquitectura. Lo que se fue es la persistencia (los InfoProviders, las cargas nocturnas, el sistema aparte) y el lenguaje (BEx Query Designer). Lo que llegó en su lugar es un lenguaje nuevo, las anotaciones CDS, para hablarle al mismo motor.

Esto tiene una consecuencia práctica que vale más que cualquier diagrama, y me la he topado a la mera hora de validar: si ejecutas una vista analítica con F8 desde Eclipse, el resultado no es el que va a ver SAC. F8 le pregunta a HANA; SAC le pregunta al motor. Las agregaciones de excepción, las fórmulas de la query, los textos y las jerarquías de las características se resuelven en el motor. Si la prueba no pasa por RSRT, no probaste lo que el usuario va a ver. Probaste otra cosa.

[ Sube la figura 1: fig-motor.png ]

Tres capas

El error más caro que he visto en estos proyectos es escribir una vista gigante, con todos los joins, todos los cálculos y la anotación de query encima, y llamarla "el reporte". Sale a la primera. A la segunda, cuando alguien pide un campo más, la vista se rompe o se duplica.

SAP organiza sus propias vistas en un Virtual Data Model de tres capas, y la práctica que aplicamos con este cliente fue respetarlas también en el desarrollo propio. Las nombro con el prefijo que usamos (ZI_ para interfaz, ZC_ para consumo) porque el prefijo es parte de la disciplina.

Capa 1: básicas y dimensiones. Una vista por entidad de negocio, sin lógica de reporte. Las dimensiones llevan @Analytics.dataCategory: #DIMENSION y declaran cuál es su llave y cuál su texto. Es la capa que hace que SAC muestre "Cliente 1000 · Comercial del Norte" en vez de un número suelto.

@AbapCatalog.sqlViewName: 'ZICUSTOMER'
@VDM.viewType: #BASIC
@Analytics.dataCategory: #DIMENSION
@ObjectModel.representativeKey: 'Customer'
@EndUserText.label: 'Cliente (dimensión)'
define view ZI_Customer as select from kna1
{
  key kunnr as Customer,
  @Semantics.text: true
      name1 as CustomerName,
      land1 as Country
}

Capa 2: el cubo. Aquí viven los hechos: la partida de factura, el movimiento de material, el documento de transporte. Se anota como #CUBE, que SAP define como datos factuales que sí pueden tener redundancia, y por eso es el lugar correcto para las asociaciones a las dimensiones. Cada importe declara su moneda y cada cantidad su unidad, y cada medida dice cómo se agrega. Sin eso, SAC suma como puede.

@AbapCatalog.sqlViewName: 'ZISALESCUBE'
@VDM.viewType: #COMPOSITE
@Analytics.dataCategory: #CUBE
@EndUserText.label: 'Ventas (cubo)'
define view ZI_SalesCube as select from ZI_BillingItem as Item
  association [0..1] to ZI_Customer as _Customer
    on $projection.Customer = _Customer.Customer
{
  key Item.BillingDocument,
  key Item.BillingDocumentItem,
      Item.BillingDate,
      @ObjectModel.foreignKey.association: '_Customer'
      Item.Customer,
      Item.DistributionChannel,
      @Semantics.amount.currencyCode: 'TransactionCurrency'
      @DefaultAggregation: #SUM
      Item.NetAmount,
      @Semantics.currencyCode: true
      Item.TransactionCurrency,
      @Semantics.quantity.unitOfMeasure: 'BaseUnit'
      @DefaultAggregation: #SUM
      Item.BillingQuantity,
      @Semantics.unitOfMeasure: true
      Item.BaseUnit,
      _Customer
}

Capa 3: la query. Es la vista que SAC ve. No trae joins nuevos ni lógica de negocio: trae decisiones de presentación. Qué va en filas por defecto, qué va en columnas, qué fórmulas calcula el motor, qué variables pide al abrir. Y la única anotación que la vuelve visible.

@AbapCatalog.sqlViewName: 'ZCSALESQ'
@VDM.viewType: #CONSUMPTION
@Analytics.query: true
@EndUserText.label: 'Ventas por cliente (query)'
define view ZC_SalesQuery as select from ZI_SalesCube
{
  @AnalyticsDetails.query.axis: #ROWS
  @AnalyticsDetails.query.display: #KEY_TEXT
  Customer,
  @AnalyticsDetails.query.axis: #FREE
  DistributionChannel,
  @AnalyticsDetails.query.axis: #COLUMNS
  NetAmount,
  BillingQuantity,
  @AnalyticsDetails.query.formula: 'NetAmount / BillingQuantity'
  @EndUserText.label: 'Precio promedio'
  0 as AveragePrice
}

Tres vistas, tres responsabilidades. Si mañana Ventas pide el precio por tonelada en vez de por pieza, se toca la query. Si Finanzas pide la moneda local, se toca el cubo. Si Maestros cambia el nombre del cliente, no se toca nada.

Un detalle que suena menor y no lo es: la anotación @AbapCatalog.sqlViewName de la query es la que define el nombre con el que existe en el motor. En el ejemplo, la transient query se llama 2CZCSALESQ, y el cubo debajo es el proveedor 2CZISALESCUBE. En RSRT se buscan juntos, 2CZISALESCUBE/2CZCSALESQ, y el nombre de la query es el que aparece en SAC al crear el modelo.

[ Sube la figura 2: fig-tres-capas.png ]

Las anotaciones que sí importan

Hay cientos de anotaciones CDS. Para reportear en SAC, la lista corta, la que de plano no puede faltar, es esta.

1. @Analytics.dataCategory con #DIMENSION en maestros y #CUBE en hechos. Es la que le dice al motor qué es estrella y qué es centro.
2. @Analytics.query: true, solo en la capa de consumo. Es la puerta a SAC.
3. @ObjectModel.representativeKey en cada dimensión, para que el motor sepa cuál campo es la llave cuando la vista tiene varios.
4. @Semantics.text: true en el campo de descripción y @ObjectModel.text.association cuando el texto vive en otra vista. Sin esto, SAC te muestra puros códigos.
5. @Semantics.amount.currencyCode y @Semantics.quantity.unitOfMeasure en cada medida, con su pareja @Semantics.currencyCode: true o @Semantics.unitOfMeasure: true. Es lo que evita que se sumen pesos con dólares, o piezas con toneladas.
6. @DefaultAggregation en cada medida (#SUM, #MAX, #NONE). Sin ella, cada cifra hereda un comportamiento por defecto que nadie eligió.
7. @AnalyticsDetails.query.axis, .display, .totals y .formula en la query. Son el equivalente de lo que antes se configuraba en BEx: layout inicial, texto o llave, totales, fórmulas calculadas en el motor.
8. @AccessControl.authorizationCheck: #CHECK con su DCL. En BW la seguridad la ponía el analysis authorization; aquí la pones tú, vista por vista, y el motor la aplica en cada petición de SAC.

Hay una novena que no es para SAC pero conviene conocer: @Analytics.dataExtraction.enabled: true. Marca la vista como apta para replicación por ODP hacia un warehouse o un lago. Es otra puerta, con otras reglas y otro contrato, y de esa hablé en la edición pasada.

[ Sube la figura 3: fig-anotaciones.png ]

RSRT antes que SAC

En este cliente, la prueba unitaria de una vista analítica no se hace en SAC. Se hace en RSRT, con el nombre 2C de la query, y con tres validaciones concretas: que las características libres sean las esperadas, que los textos salgan junto a las llaves, y que los atributos derivados de una dimensión (por ejemplo, región, línea y canal que cuelgan de una oficina de ventas) lleguen con el valor correcto para cada llave.

La razón es la de arriba: SAC es un cliente delgado, pide y muestra, no calcula ni persiste. Si el número está mal en SAC, el número está mal en la query, y la query se depura en RSRT, donde puedes ver el plan, activar y desactivar la caché, mirar las estadísticas y comparar contra el resultado de una transacción estándar. Cuando una story se pone lenta, casi siempre la causa está en el cubo (demasiados joins) o en la query (demasiadas fórmulas en el motor), no en SAC. SAC nomás entrega lo que le dan.

Y hay una cifra de SAP que conviene tener a la mano. El Quick Sizer de embedded analytics asume que una query tarda como máximo 10 segundos. Si una vista tarda 60, el problema no es solo que el usuario espere: el dimensionamiento del sistema asumía seis veces menos recurso para esa consulta. Reportear encima del ERP significa que cada query mal hecha se la cobras al ERP, y el ERP se la cobra a todos los demás.

El universo escondido

Cuando este cliente empezó a comparar los reportes nuevos de SAC contra los viejos de BusinessObjects, página por página, aparecieron tres tipos de diferencia. Ninguna era falla de SAC.

La primera: filtros que el reporte de BO aplicaba y que nadie tenía escritos. Cifras que cuadraban en años recientes y no en otros, tablas donde SAC traía más de lo que traía BO, y una frase que resume el problema entero, escrita por quien validaba: "hay filtros que no identificamos para aplicarlos en la query de SAC". Esos filtros vivían en el universo de BO o en el propio reporte, no en el dato. Al apagar BO, se apagaron con él.

La segunda: el redondeo. BO redondeaba a entero en varias tablas; SAC mostraba los decimales que traía la CDS. Eran el mismo número. Parecían dos.

La tercera: el año histórico completo que no cuadraba. Todos los años posteriores coincidían; el más antiguo, no. La explicación más probable no es un filtro perdido: son datos que existían en BW porque BW los cargó en su momento, y que en S/4HANA ya no están igual. Ese es el caso que SAP describe cuando explica para qué no sirve el embedded analytics: snapshots, historización de maestros, retención larga. Un data warehouse guarda la foto; un ERP guarda el estado.

Y hubo una cuarta que no salió del comparativo sino de leer las stories: en una de ellas, la etiqueta del centro de distribución se resolvía con una cadena de "si el puesto de planificación es 01 entonces Norte, si es 06 entonces Centro". Lógica de negocio escrita en el front. Funciona, y funciona bien. Pero la próxima story que necesite el mismo mapeo lo va a volver a escribir, y en algún momento las dos versiones van a divergir.

La tesis es esta: el semantic layer no desaparece cuando apagas la herramienta que lo tenía. En BusinessObjects vivía en el universo; en BW, en la query de BEx y en los InfoObjects. Al quitar los dos, ese significado tiene exactamente dos lugares donde caer: la vista CDS, una vez, con anotaciones que todo el mundo consume; o cada story, cada vez, a mano. Lo que no anotes en la capa 2 o la capa 3, lo vas a encontrar reescrito en el front, a la mera hora y por triplicado.

Por eso la disciplina de las tres capas no es una preferencia de arquitecto. Es la única forma de que el universo escondido tenga un lugar visible donde vivir.

[ Sube la figura 4: fig-universo.png ]

Live o import

Una última decisión que conviene entender antes de firmar, porque cambia qué objetos vas a construir.

La conexión live es la que consume las queries analíticas. SAC pide, el motor responde, nada se copia. Es la que respeta la seguridad del ERP, la que no tiene desfase y la que le pega al ERP con cada clic.

La conexión import no consume vistas CDS. La documentación de SAC lo dice literal: consume servicios OData. Eso significa que para importar necesitas otra anotación (@OData.publish: true), otro objeto activado en Gateway, y aceptar que las relaciones uno a muchos no se siguen. A cambio, el dato queda en SAC, se puede mezclar con otras fuentes y no le pega al ERP en cada consulta.

Con este cliente la regla quedó simple: live por defecto, import solo cuando el reporte necesita mezclarse con algo que no está en S/4HANA (un presupuesto que viene de otro lado, por ejemplo) o cuando el volumen y la frecuencia de uso no justifican pegarle al ERP en cada apertura. Y una advertencia documentada por SAP que sorprende a más de uno: el blending entre un modelo live de S/4HANA y otro no estaba disponible en el modo optimizado de las stories en las versiones que la nota de soporte describe, y SAP lo ha ido habilitando por partes en versiones posteriores. Si el diseño depende de mezclar, hay que probarlo en la versión que tienes antes de prometerlo.

El norte

Volvería a firmar la arquitectura de este cliente. Un ERP, un front, vistas CDS como contrato y ninguna copia intermedia que mantener. Para una empresa de su tamaño, con reportes operativos y un horizonte de análisis de dos o tres años, es la decisión correcta, sin darle más vueltas.

Lo que le pediría a cualquiera que esté por tomar la misma decisión son tres cosas, y ninguna es una licencia.

Presupuesta la reconstrucción del semantic layer como un entregable, no como una consecuencia. Los filtros, las reglas de redondeo, los mapeos y las jerarquías que hoy viven en universos de BO y queries de BEx tienen que inventariarse antes de apagar nada, y tienen que aterrizar en las capas 2 y 3, con anotaciones. Si el plan solo dice "migrar reportes", ese trabajo va a aparecer igual, pero en la fase de validación, con el reloj corriendo.

Haz de RSRT la puerta de calidad. Ninguna query llega a SAC sin pasar por ahí. Es barato, el motor la entiende, y ahí se ven los problemas de rendimiento antes de que los vea un director.

No retires al equipo de BW: reconviértelo. El motor, el protocolo y la transacción siguen ahí. Lo que cambió es el lenguaje. Un consultor que entiende cómo agrega el motor, cómo se comportan las excepciones y qué es una característica libre tiene la mayor parte del camino hecho; lo que le falta es sintaxis de anotaciones, y eso se aprende en semanas, no en años.

Quitamos BW. El motor se quedó. Hay que tratarlo como lo que es: el mismo motor, con otro nombre en la puerta.

Fuentes

SAP Help Portal — Live Data Connections to SAP S/4HANA (SAP Analytics Cloud): "Only CDS Views containing the @Analytics.query: true annotation will appear in SAP Analytics Cloud"; transient query con nombre 2C<sqlViewName>; conexión Direct con CORS, Tunnel más lenta; remite a las notas SAP 2595552 y 2715030. https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/00f68c2e08b941f081002fd3691d86a7/d2a1edf7cda74315a2c5052de8a3a4eb.html

SAP Help Portal — Import Data Connection to SAP S/4HANA (SAP Analytics Cloud): "SAP Analytics Cloud does not consume CDS views from SAP S/4HANA, it consumes OData services only"; limitaciones de navegación uno a muchos y de tipos complejos. https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/00f68c2e08b941f081002fd3691d86a7/63140f17362947fe8bcd9c6960db23bc.html

SAP Help Portal — Analytics Annotations (SAP NetWeaver 7.5): definiciones de Analytics.dataCategory (#DIMENSION, #FACT, #CUBE, #AGGREGATIONLEVEL), Analytics.query, Analytics.dataExtraction.enabled, Analytics.hidden, Analytics.planning.enabled. https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/c2/dd92fb83784c4a87e16e66abeeacbd/content.htm

SAP Community, Enterprise Architecture Knowledge Base — Peter Schmidt (SAP), When to use SAP S/4HANA Embedded Analytics?, 17-oct-2022: "First choice should be SAP S/4HANA embedded analytics specifically for light-weight real-time data models"; criterios de snapshots, historización, retención, harmonización y cross-system. https://community.sap.com/t5/enterprise-architecture-knowledge-base/when-to-use-sap-s-4hana-embedded-analytics/ta-p/5154

SAP Community — Masaaki Ishii (SAP), Analytics in S/4HANA: real shape of embedded analytics and beyond embedded analytics, 2019, actualizado 2023: la conexión InA para SAC, la expectativa de 10 segundos del Quick Sizer y el impacto en recursos de una vista de 60 segundos. https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/analytics-in-s-4hana-real-shape-of-embedded-analytics-and-beyond-embedded/ba-p/13403536

SAP Community — Pavan Kumar Reddy, Step 2: Define the Analytical Query CDS View, 26-feb-2017: prueba de la query en RSRT con prefijo 2C y la advertencia de que la ejecución con F8 no refleja el resultado del analytic engine. https://community.sap.com/t5/technology-blog-posts-by-sap/step-2-define-the-analytical-query-cds-view/ba-p/13349493

SAP KBA 2591655 — Performance analysis when using SAP HANA Live Data Connections in SAP Analytics Cloud: endpoint InA y método de aislamiento de modelos complejos. https://userapps.support.sap.com/sap/support/knowledge/E/2591655

SAP KBA 3466290 — Data blending for S/4HANA or BW models is not available in optimized mode of story in SAP Analytics Cloud. https://userapps.support.sap.com/sap/support/knowledge/en/3466290

SAP KBA 3507024 — Ability to create blended chart in the optimized story experience for SAP Business Warehouse (BW) data models in SAP Analytics Cloud. https://userapps.support.sap.com/sap/support/knowledge/en/3507024

SAP KBA 3763590 — SAP BI Platform 4.3: End of Mainstream Maintenance 31 December 2026. https://userapps.support.sap.com/sap/support/knowledge/en/3763590

SAP Community — SAP NetWeaver 7.5 Maintenance Strategy: fin de mantenimiento mainstream de SAP NetWeaver 7.3, 7.31 y 7.4 a finales de 2020. https://pages.community.sap.com/topics/abap/netweaver-maintenance-strategy

## CUERPO — copiar hasta aquí

---

## POST DE LANZAMIENTO (feed) — copiar de aquí

Un cliente apagó BW y BusinessObjects al migrar a S/4HANA. Hoy reporta directo a SAP Analytics Cloud, casi todo por conexión live.

Funciona. Y lo volvería a firmar.

Pero hay algo que no sale en la presentación del vendedor: el motor de BW no se fue a ningún lado.

Cuando anotas una vista CDS con @Analytics.query: true, S/4HANA genera una transient query (la 2C…) y la ejecuta el analytic engine embebido en el ERP. El mismo motor OLAP que corría las queries de BEx. SAC le habla por InA, el mismo protocolo de siempre. Y se prueba en RSRT, la misma transacción de siempre.

Se fueron la persistencia y BEx. El motor se quedó. Lo que cambió es el lenguaje: ahora se le habla con anotaciones.

Eso tiene tres consecuencias prácticas que desarrollo en la edición de esta semana:

Una vista analítica ejecutada con F8 no te dice lo que va a ver SAC. F8 le pregunta a HANA; SAC le pregunta al motor. Si la prueba no pasa por RSRT, probaste otra cosa.

La vista de consumo se construye en tres capas (dimensión, cubo, query) y hay ocho anotaciones que de plano no pueden faltar. Van con código en las figuras.

Y la que le duele al CIO: el semantic layer del universo de BO no desaparece cuando lo apagas. Al cuadrar BO contra SAC aparecieron filtros que nadie tenía escritos, redondeos distintos, un año histórico que no cuadraba y un mapeo de negocio escrito a mano dentro de una story. Lo que no anotes en CDS, lo vas a encontrar reescrito en el front, a la mera hora y por triplicado.

Link en el primer comentario.

#SAP #S4HANA #SAPAnalyticsCloud #CDS #EmbeddedAnalytics #DataEngineering #ArquitecturaDeDatos

---

## PRIMER COMENTARIO (poner de inmediato)

Edición 12 completa, con el código de las tres capas, las ocho anotaciones y el cuadre BO contra SAC:
https://rrbenavi-source.github.io/portfolio/publicaciones/quitamos-bw-el-motor-se-quedo

Y la edición anterior, la otra decisión del mismo tipo de proyecto: qué pasa cuando en vez de quedarte adentro decides sacar el dato de SAP hacia otra plataforma:
https://rrbenavi-source.github.io/portfolio/publicaciones/la-aduana

---

## VERSIÓN CORTA (para repostear en unos días)

RSRT antes que SAC.

Si reporteas de S/4HANA a SAP Analytics Cloud por conexión live, la query que SAC ejecuta no es tu vista CDS: es la transient query 2C que S/4HANA generó a partir de ella, y la corre el analytic engine embebido en el ERP.

Por eso ejecutar la vista con F8 no sirve como prueba. F8 le pregunta a HANA. SAC le pregunta al motor. Las agregaciones de excepción, las fórmulas, los textos y las jerarquías se resuelven en el motor.

En el cliente de la edición 12 la regla quedó simple: ninguna query llega a SAC sin pasar por RSRT. Ahí se validan las características libres, los textos junto a las llaves y los atributos derivados. Y ahí se ven los problemas de rendimiento antes de que los vea un director.

Es barato, el motor la entiende, y cualquier consultor de BW ya sabe usarla. Quitamos BW. El motor se quedó.
