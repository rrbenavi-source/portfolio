# Brújula — Edición 04 (2026-W31) · Material copy-paste

_Publica: martes 2026-07-28, 9:00 AM CDMX. Todo lo de abajo está listo para
pegar; las marcas `[ Sube la figura: … ]` indican dónde insertar cada imagen en
el editor de LinkedIn._

---

## Título del artículo

Migrar un reporte Z no es traducir ABAP: es una autopsia

## Subtítulo

Lo que un report de casi 3,000 líneas me enseñó sobre llevar SAP al lakehouse

## Portada

[ Sube la portada: `brujula-cover-04.png` (1920×1080) ]

---
---

## CUERPO DEL ARTÍCULO (pegar completo)

Hay una promesa que se repite en cada propuesta de modernización: "migramos tus reportes SAP al lakehouse". Suena a traducción — ABAP entra, SQL o PySpark sale, y el número que el negocio ya conoce aparece ahora en un dashboard.

Este año la decisión dejó de ser opcional para muchos: SAP BW 7.5 sale de mantenimiento mainstream a fines de 2027, y desde junio de 2026 SAP bloquea técnicamente la extracción ODP-RFC de aplicaciones no-SAP, con un opt-out que expira el 31 de diciembre. Miles de organizaciones están decidiendo este año qué se lleva al lakehouse y por dónde.

Yo acabo de pasar por eso con un reporte concreto: un report Z de FI, productivo desde hace años, de casi tres mil líneas de ABAP. El destino: una tabla Delta en Databricks, consumida desde Power BI. Y no se quedó en piloto: el modelo ya está generado y hoy cuadra los ejercicios 2025 y 2026 contra el sistema origen.

La lección más honesta que puedo compartir: migrar ese reporte no fue traducirlo. Fue hacerle una autopsia. El entregable de una migración de reporte no es "el mismo reporte en otra plataforma" — es la decisión explícita, documentada, de qué lógica vive, qué lógica muere y qué lógica nunca estuvo viva.

**Dead code walking**

Lo primero que apareció al abrir el reporte: cuatro flujos de lectura distintos (documentos archivados contra vivos, cruzados con facturación contra no-facturación). ¿Por qué existen? Porque en el sistema origen los datos archivados y los vivos se leen por mecanismos diferentes. En el lakehouse esa limitación no existe: la unión es un UNION y los cuatro flujos colapsan en uno. Media docena de FORMs desaparecieron, no porque los optimizamos, sino porque el problema que resolvían ya no existe.

Y no fueron los únicos funerales: el AUTHORITY-CHECK se vuelve Unity Catalog y row-level security; el OPEN DATASET se vuelve un write a un Volume; la tabla Z de log se vuelve el logging del job. Nada de eso se migra: se deja morir con dignidad, y se levanta el acta de defunción.

Primer hallazgo de método: separa la lógica de negocio de la lógica de compensación — el código que solo existe para esquivar limitaciones de la plataforma vieja. Quien cotiza la migración por líneas de código está cotizando la mudanza de muebles que van directo a la basura.

**La lógica que no está en el código**

La sorpresa opuesta fue más incómoda: una parte central del comportamiento del reporte no estaba en el ABAP. Estaba en filas — una tabla Z de configuración (cuentas, tasas válidas, tolerancias) que la réplica hacia el lakehouse no incluía. El programa podía traducirse completo y aun así no calcular nada correcto, porque su cerebro estaba en otra parte.

Peor todavía: un function module cuyo código fuente ya no se pudo obtener. No hay traducción posible de un programa que nadie puede leer — solo un fallback documentado, con el hueco marcado y visible.

Segundo hallazgo: el inventario de un reporte no es su código; es su código más su configuración más sus dependencias. El código te lo da un extractor; el inventario completo solo te lo da la autopsia.

**Replicar el comportamiento, no la intención**

El reporte incluye lógica para navegar la cadena de compensación de un documento — en Spark, self-joins recursivos: caros y delicados. Y entonces miramos los datos productivos: el campo que encadena la navegación llegaba siempre vacío. Esa lógica —correcta, bien escrita, probada— nunca se había ejecutado.

¿Replicas lo que el código intenta hacer, o lo que el sistema realmente hace? Nosotros elegimos replicar el comportamiento real y dejar la divergencia asentada por escrito. Migrar la intención habría sido pagar y mantener una pieza de complejidad que producción jamás usó.

[ Sube la figura: `fig-autopsia.png` — La autopsia: qué muere, qué vive fuera del código y qué nunca estuvo vivo ]

**La spec es el contrato, el golden case es el seguro**

Para este reporte, el diseño tomó la forma de una especificación source-to-target de 33 columnas, decidida antes de escribir el pipeline. Y la implementación se protegió con desarrollo guiado por pruebas y un golden case: un caso real verificado a mano contra el sistema origen, fijado como prueba de no-regresión. En dominio fiscal esto no es perfeccionismo: es la diferencia entre "el job corrió en verde" y "el número es defendible frente a una auditoría".

Protiviti estimó este año que salir de BW hacia una plataforma no-SAP demanda 3–4 veces más esfuerzo que las rutas SAP. Mi experiencia dice que es creíble, con un matiz: el esfuerzo no se va en traducir lógica. Se va en descubrir cuál lógica es de negocio, cuál es compensación de plataforma y cuál está en configuración — la autopsia. La traducción, con la spec cerrada, es la parte rápida.

Y por si piensas que exagero: la guía oficial no existe. Databricks, Snowflake, Microsoft, AWS y Google documentan la capa de datos (extracción, CDC, zero-copy), pero ninguno publica cómo traducir la lógica de un reporte Z. El único que documenta migración de lógica ABAP es SAP mismo — solo rutinas BW, y solo hacia su propio Business Data Cloud. Si vas a un lakehouse de terceros, el método lo pones tú.

**IEPS por material: cuando la granularidad decide la verdad**

El mismo proyecto incluía un reto mayor que migrar lo existente: construir un desglose que SAP no daba de fábrica — el IEPS por material. La verdad fiscal del IEPS vive en BSET (importe y base por línea de impuesto), pero BSET no lleva material. Y llegar al material no era un lujo: el IEPS no es una tasa única — en bebidas alcohólicas la tasa cambia con la graduación (26.5%, 30% o 53%), así que una factura mixta puede mezclar varias tasas en un mismo documento. Sin el nivel de detalle por material no hay forma de atribuir a cada línea su tasa y su base correctas. El detalle por SKU se reconstruye desde las posiciones y se cuadra de vuelta contra BSET. Cuando lo probamos contra un documento real, la reconstrucción cuadró al centavo: base idéntica y una diferencia de un centavo por redondeo.

Y ahí está la palabra clave: la granularidad. La primera versión de la consulta trabajaba a granularidad de documento, con un "material representativo" por factura (min(MATNR) + filtro de grupo). Las facturas mixtas, con treinta o cuarenta materiales, se caían completas del universo. Resultado: cerca del 57% del importe real era invisible — sin un solo error de cálculo. La lógica era correcta; la unidad de análisis estaba mal elegida.

El error se detectó de la manera aburrida: exportar BKPF, BSEG y BSET de un documento real y sumar a mano. Las dos prácticas que me llevo: control totals por documento contra la fuente fiscal antes de agregar nada, y la granularidad como decisión de diseño explícita en la spec. Un desglose fiscal que cuadra "casi" no es un éxito: en este dominio se cuadra al centavo, o no se cuadró.

**El mejor reporte que migras es el que matas**

Si un solo report Z exigió este nivel de análisis, ¿qué haces con los cientos que acumula cualquier instalación con veinte años de historia? La respuesta seria: medir uso antes de tocar nada, enterrar sin culpa lo huérfano, y migrar lo que sí migra como data product, no como reporte. Cada reporte que matas es una autopsia que no pagas.

Con la puerta ODP-RFC cerrándose en diciembre, la tentación es correr a mover todo lo que hay. Es la decisión exactamente equivocada: la fecha límite es para decidir la arquitectura de extracción, no para congelar veinte años de reportes en una plataforma nueva. La deuda técnica no se paga mudándola de casa.

[ Sube la figura: `fig-deadline-odp.png` — Cronología de la Note 3255746: la extracción de SAP ya tiene fecha límite ]

Un reporte legacy no es un requerimiento, es un testigo: testifica lo que el negocio necesitó alguna vez, con las limitaciones de la plataforma donde nació. El trabajo del arquitecto no es traducir al testigo palabra por palabra. Es interrogarlo, quedarse con la verdad, y dejar que el resto descanse en paz.

—

📍 La versión completa, con las fuentes verificadas (SAPinsider, Protiviti, BARC, Databricks, SAP Community), está en mi portfolio — link en el primer comentario.

---
---

## POST DE LANZAMIENTO (feed, publicar el martes al salir la edición)

"Migramos tus reportes SAP al lakehouse."

Suena a traducción: ABAP entra, PySpark sale.

Acabo de migrar un report Z de casi 3,000 líneas a Databricks y no fue una traducción. Fue una autopsia:

🪦 4 flujos de lectura colapsaron en 1 — existían solo por limitaciones de la plataforma vieja.

📋 Parte de la lógica no estaba en el código: vivía en una tabla Z de configuración que nadie había replicado.

👻 La pieza más compleja del reporte —la navegación de la cadena de compensación— nunca se había ejecutado en productivo. Años corriendo, y el campo que la encadena siempre llegó vacío.

📊 Y al reconstruir el cálculo de IEPS por material (obligado: el IEPS maneja tasas distintas por graduación — 26.5%, 30%, 53%), la primera consulta dejaba invisible ~57% del importe real — sin un solo error de cálculo. El nivel de detalle estaba mal elegido: las facturas multi-SKU se caían completas del universo.

El entregable de una migración de reporte no es "el mismo reporte en otra plataforma". Es la decisión documentada de qué lógica vive, qué lógica muere y qué lógica nunca estuvo viva.

Y el contexto de 2026 no perdona: desde junio SAP bloquea técnicamente la extracción ODP-RFC de aplicaciones no-SAP, y el opt-out expira el 31 de diciembre. La pregunta ya no es cómo sacar el dato — es qué merece vivir del otro lado.

En la Edición 04 de Brújula: la autopsia completa, el método (spec source-to-target + golden case) y por qué el mejor reporte que migras es el que matas.

¿Tú qué harías primero: medir el uso de tus reportes, o empezar a migrarlos?

#DataEngineering #SAP #Databricks #Lakehouse #ABAP #Arquitectura

---
---

## PRIMER COMENTARIO (pegar inmediatamente después de publicar el post)

La versión completa, con fuentes verificadas y las dos figuras, está aquí 👇

📄 Artículo: https://rrbenavi-source.github.io/portfolio/publicaciones/autopsia-reporte-z

🇬🇧 English version: https://rrbenavi-source.github.io/portfolio/en/publicaciones/autopsia-reporte-z
