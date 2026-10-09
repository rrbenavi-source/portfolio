# Brújula · Edición 14 — material listo para copiar y pegar

**Publicada: viernes 9 de octubre de 2026.**
Artículo en el portfolio: https://rrbenavi-source.github.io/portfolio/publicaciones/de-la-sabana-al-agente

Sin caso propio: solo patrón de industria y documentación pública de los fabricantes.

---

## Checklist

1. Crear la edición nueva en el editor de newsletter de LinkedIn.
2. Pegar el **título** y el **subtítulo** (abajo).
3. Subir la **portada**: `brujula-cover-14.png` (1920×1080).
4. Pegar el **cuerpo** que está entre los separadores, respetando las tres marcas `[ Sube la figura N: … ]`.
5. LinkedIn no tiene tablas, así que la de «Qué comprar según la pregunta» va renglón por renglón con flechas. La figura 3 no la sustituye: muestra la escalera de generaciones, no la tabla.
6. Subir las **tres figuras** en su posición, con el **alt text** que viene más abajo.
7. Llenar los campos de **SEO** (título y descripción).
8. Publicar e inmediatamente hacer el **post de lanzamiento** en el feed.
9. Poner el **primer comentario** con los links. LinkedIn penaliza los links externos en el cuerpo del post.

---

## Título

De la sábana al agente

## Subtítulo

En febrero de 2027 Microsoft apaga Power BI Q&A, la función con la que en 2013 prometió que cualquiera podría preguntarle a sus datos en lenguaje natural. Tableau ya retiró Ask Data y SAP, Search to Insight. Esta edición recorre ocho generaciones de reporting, producto por producto: qué permitía cada una, qué no y qué tipo de análisis estamos comprando hoy.

## SEO — título

De la sábana al agente: ocho generaciones de reporting, de Crystal a GenBI

## SEO — descripción

Power BI Q&A se retira en febrero de 2027. Ocho generaciones de reporting, producto por producto, y la tarea que ninguna eliminó: decidir qué significa cada palabra del negocio.

---

## Alt text de las imágenes

**Figura 1 — fig-nlq-retirada.png:** Línea de tiempo de 2013 a 2027 con tres funciones de pregunta en lenguaje natural: Power BI Q&A (septiembre de 2013 a febrero de 2027, reemplazo Copilot), Tableau Ask Data (2019 a febrero de 2024, reemplazo Tableau Pulse) y SAC Search to Insight (retirado en Q4 2024, reemplazo Just Ask y Joule). Abajo, la tabla de migración de Microsoft: Q&A Setup pasa a Prep data for AI.

**Figura 2 — fig-misma-pregunta.png:** La misma pregunta, venta del trimestre contra el mismo trimestre del año pasado por región, escrita en cuatro lenguajes: SQL, MDX con PARALLELPERIOD, una medida DAX con SAMEPERIODLASTYEAR y una verified query de Snowflake con el campo verified_by resaltado.

**Figura 3 — fig-escalera.png:** Escalera de ocho generaciones de reporting, de la sábana al agente, con productos de ejemplo, el análisis que permite cada una y lo que no permite.

---

## CUERPO — copiar de aquí

En febrero de 2027, los reportes de Power BI que todavía tengan un visual de Q&A van a mostrar un error donde antes había una respuesta. Microsoft anunció el retiro en diciembre de 2025 para finales de 2026 y en septiembre lo movió a febrero. El reemplazo oficial es Copilot.

Q&A llegó en septiembre de 2013 al preview de Power BI for Office 365: escribías «ventas por región en 2013» y aparecía una gráfica. Tableau lanzó Ask Data en 2019 y lo retiró en 2024; SAP sustituyó Search to Insight por Just Ask a finales de ese mismo año. Entre 2024 y 2027, los tres fabricantes retiran su primera forma de preguntarle a los datos en lenguaje natural.

[ Sube la figura 1: fig-nlq-retirada.png ]

Llevo más de veinte años construyendo reportes en casi todas las generaciones que siguen, y el patrón se repite: cada producto nuevo cambia qué tipo de pregunta puede hacer el negocio sin pedirle nada a TI. Ninguno ha cambiado quién decide qué significa el número.

Primera generación: la sábana

En los equipos de finanzas y operaciones de México le decimos sábana al reporte tabular largo: cientos o miles de renglones, impresos o exportados, con todas las columnas que alguien pidió alguna vez. Es el listado en COBOL o RPG de los mainframes, el reporte ALV de SAP y, desde los noventa, Crystal Reports.

Qué análisis permite: operativo. Listar, filtrar, ordenar, subtotalizar: «dame las facturas abiertas de la sucursal 12 con más de 60 días». Es la generación más vieja y la que menos ha muerto: con ella se cuadra un cierre, porque cada renglón se rastrea hasta un documento.

Qué no permite: hacer una pregunta nueva; cada variación es un requerimiento a sistemas. A mediados de los setenta, IBM creó los information centers para atender la fila de solicitudes (el backlog) que sistemas no alcanzaba a resolver. El backlog de reportes es más viejo que la PC.

Segunda generación: la hoja de cálculo

VisiCalc (1979, Apple II) suele citarse como la aplicación que convirtió a la computadora personal en herramienta de negocio. Después vinieron Lotus 1-2-3 y Excel. Con Excel 5, en 1993, llegó la tabla dinámica (PivotTable), una idea que Lotus había probado en Improv (1991).

Qué análisis permite: escenarios y resúmenes cruzados sin escribir código: «¿qué pasa con el margen si el precio sube 3 %?» o «ventas por producto contra mes». Por primera vez, el usuario de negocio arma su propio análisis.

Qué no permite: que dos personas lleguen al mismo número. La hoja trabaja sobre una extracción, y cada extracción es una copia. Desde entonces, la pregunta más cara en una junta de dirección es «¿cuál de los dos archivos es el bueno?».

Tercera generación: el cubo

En 1993, Edgar F. Codd —el creador del modelo relacional— publicó con dos coautores el documento que bautizó el OLAP (Online Analytical Processing): bases de datos organizadas para analizar, no para registrar transacciones. A esa familia pertenecen Essbase (1992), Cognos PowerPlay, Microsoft Analysis Services y, desde 1998, SAP BW con su herramienta de consultas BEx.

Qué análisis permite: multidimensional. Cortar el dato por cualquier eje (slice and dice), bajar por una jerarquía (región → zona → cliente) y comparar contra el mismo periodo del año anterior. Lo que en la hoja era una fórmula frágil, en el cubo es una función del motor.

Qué no permite: preguntar lo que no se modeló. El cubo contesta rápido, pero solo dentro de las dimensiones y medidas diseñadas por adelantado; una pregunta fuera del diseño regresa a la fila de requerimientos.

Cuarta generación: la capa semántica

El 27 de noviembre de 1991, Business Objects —hoy parte de SAP— solicitó en Estados Unidos la patente 5,555,403, otorgada en 1996. Su objetivo, en palabras del documento: que los usuarios consulten bases de datos relacionales «sin conocer la estructura relacional ni el lenguaje SQL». La pieza central se llamaba universo: una representación de la base de datos, fácil de entender, diseñada para un grupo de usuarios. Hoy le decimos semantic layer.

Qué análisis permite: consulta ad hoc (armada en el momento) y gobernada. El usuario arrastra objetos de negocio («Cliente», «Ingreso», «Región») y la herramienta escribe el SQL: «clientes con más de tres devoluciones este trimestre», sin esperar a nadie y con la definición de «ingreso» que aprobó finanzas.

Qué no permite: que el universo se mantenga solo. Alguien de TI tiene que agregar cada objeto, cada sinónimo y cada regla. Esta idea reaparece al final.

Quinta generación: el descubrimiento visual

En 2002, Chris Stolte, Diane Tang y Pat Hanrahan publicaron en Stanford Polaris, un sistema para consultar y graficar al mismo tiempo arrastrando campos; de ahí nació Tableau. En paralelo, QlikView llevó un motor asociativo que mostraba lo que coincidía con un filtro y también lo que quedaba fuera.

Qué análisis permite: exploratorio. Ver dónde se concentra la caída, encontrar un valor atípico en un mapa, descubrir una relación que nadie había pedido. Es la primera generación en la que el análisis empieza por mirar, no por preguntar.

Qué no permite: una sola verdad. Cada analista construye su propio libro de trabajo con sus propios cálculos. El descubrimiento visual multiplicó los análisis y también las definiciones.

Sexta generación: el self-service en la nube

Power BI salió a disponibilidad general el 24 de julio de 2015. Looker llevó el modelo semántico a código con LookML, su lenguaje de modelado, y SAP Analytics Cloud juntó BI, planeación y predicción en un solo producto.

Qué análisis permite: modelado propio y dashboards compartidos. El analista de negocio construye su modelo, escribe sus medidas (en Power BI, con el lenguaje DAX) y publica para su área. En SAC, además, planea sobre el mismo modelo con el que reporta.

Qué no permite: controlar la proliferación. La facilidad que democratizó el reporte produjo cientos de modelos con la misma medida calculada de formas distintas. El sello de «certificado» que analicé en la edición anterior busca poner orden aquí.

Séptima generación: la primera ola de inteligencia artificial

Aquí entran Q&A, Ask Data y Search to Insight, que intentaron que el usuario escribiera su pregunta. Junto con ellos llegó la analítica aumentada: funciones que buscaban explicaciones solas, como Key Influencers en Power BI, Explain Data en Tableau o Smart Insights en SAC.

Qué análisis permite: diagnóstico automatizado. «¿Qué factores explican que este cliente se vaya?» o «¿por qué este punto se sale de la tendencia?», sin que el analista arme el modelo estadístico.

Qué no permite: conversar. Estos motores reconocían palabras clave y las asociaban a columnas. Para que funcionaran, alguien tenía que capturar sinónimos y relaciones a mano; en Power BI, con Q&A Setup y la opción de «enseñarle» a Q&A. Si el usuario escribía «facturación» y el sinónimo no existía, no había respuesta. La idea no era mala; el método no escalaba.

Octava generación: el agente

La generación actual usa modelos de lenguaje grandes (LLM) para entender la intención de la pregunta, escribir la consulta, ejecutarla y explicar el resultado. Se le dice GenBI (BI generativo) o, cuando el sistema encadena varios pasos por su cuenta, analítica agéntica. Estos son los productos que hoy compiten, con una pregunta de ejemplo:

• Copilot en Power BI. Contesta sobre el modelo semántico, crea páginas de reporte y escribe consultas DAX; desde abril de 2025 funciona a partir de la capacidad Fabric más pequeña (F2). «Resúmeme qué cambió en el reporte de ventas esta semana.»
• Databricks Genie. Disponible de forma general desde junio de 2025. Contesta con texto, tabla y gráfica y enseña el SQL que usó; Databricks anunció además un modo de investigación que prueba varias hipótesis. «¿Por qué cayó el margen en el norte en agosto?»
• El agente de Snowflake. Disponible de forma general desde noviembre de 2025 como Snowflake Intelligence (hoy la documentación lo llama Snowflake CoWork). Usa Cortex Analyst para convertir preguntas en SQL sobre semantic views, vistas con las métricas y relaciones del negocio. «¿Cuáles son los diez clientes que más crecieron contra el año pasado?»
• SAP Analytics Cloud: Just Ask y Joule. Just Ask contesta sobre modelos de SAC previamente indexados; Joule recuerda el contexto de la pregunta anterior. «Ahora muéstramelo solo para el canal moderno.»
• Tableau Pulse. No espera la pregunta: vigila métricas definidas una sola vez en su capa de métricas y avisa cuando algo cambia y por qué. «Tu métrica de devoluciones subió 12 %; el principal factor es la región occidente.»
• Looker Conversational Analytics. Usa Gemini, el modelo de Google, y se apoya en LookML para que la respuesta use el mismo cálculo que el resto de la empresa.

Qué análisis permite: conversacional y de varios pasos. Una sola pregunta puede combinar lo descriptivo (qué pasó), lo diagnóstico (por qué) y una proyección (qué pasa si sigue así), con las palabras del negocio y no con las del modelo.

Qué no permite, todavía: garantizar la misma respuesta. Microsoft lo dice en su documentación: la preparación de datos para IA «no puede asegurar un resultado específico cada vez», porque el comportamiento de la IA no es determinista.

Desde México, un dato: según esa documentación, actualizada en septiembre, la experiencia independiente de Copilot en Power BI todavía no está disponible en la región de Azure de México. Conviene confirmar dónde vive la capacidad antes de diseñar la estrategia.

¿Qué tan bien contesta un agente?

La mejor referencia pública es Spider 2.0, un examen académico (benchmark) de text-to-SQL —traducir una pregunta a SQL— presentado en ICLR 2025: 632 problemas sobre bases de datos empresariales reales, muchas con más de mil columnas. Al publicarse, el mejor agente (sobre o1-preview de OpenAI) resolvía el 21.3 %; el mismo enfoque resolvía el 91.2 % de Spider 1.0, mucho más sencillo. Al 1 de octubre de 2026, en las variantes que hoy mantiene el leaderboard público (no idénticas al examen original), el primer lugar reporta 96.7 % sobre Snowflake y 76.2 % en la que mezcla varios motores de base de datos. El avance es real y rápido: menos de dos años.

En enero de 2026, en la conferencia CIDR, un equipo de la Universidad de Illinois revisó las respuestas de referencia de Spider 2.0 sobre Snowflake y de BIRD, otro benchmark muy usado: encontró errores de anotación en el 66.1 % y el 52.8 % de los problemas, respectivamente. Al corregirlos, el desempeño relativo de los sistemas cambió hasta 31 % y el ranking se movió hasta tres lugares. Parte de esas fallas eran de conocimiento de dominio: la respuesta «correcta» no entendía lo que pedía la pregunta de negocio.

La parte difícil no es que el agente escriba buen SQL, sino que alguien sepa cuál es la respuesta correcta.

[ Sube la figura 2: fig-misma-pregunta.png ]

Lo que no cambió en ocho generaciones

La documentación de los productos de la octava generación pide lo mismo antes de prometer nada:

• Power BI, en «Prep data for AI», pide preparar el modelo semántico con un esquema de datos para IA, respuestas verificadas (un visual que se devuelve ante cierta pregunta) e instrucciones de IA con la lógica y el vocabulario del negocio, y luego marcar el modelo como «aprobado para Copilot».
• Databricks dice que quien arma un agente de Genie «necesita entender los datos» y que los analistas que dominan SQL «normalmente tienen el conocimiento» para curarlo.
• Snowflake reconoce que las soluciones genéricas «tienen dificultades» para convertir texto a SQL «cuando solo tienen el esquema de la base de datos», porque al esquema le faltan las definiciones del proceso de negocio y de las métricas.
• SAP ofrece una revisión de preparación (readiness) del modelo antes de que Just Ask y Joule lo usen.

Gartner lo resumió en mayo: los modelos de datos basados solo en esquemas «ya no son suficientes» para la IA agéntica, porque les falta contexto de negocio y significado. En marzo había previsto que para 2030 las capas semánticas universales se tratarán como infraestructura crítica, al nivel de la plataforma de datos y la ciberseguridad.

El universo de 1991 resolvía el mismo problema: traducir el lenguaje del negocio a la estructura de la base de datos. Lo que pedía Q&A Setup —sinónimos, relaciones, enseñarle a la herramienta— es casi lo mismo que pide hoy Prep data for AI; en la tabla de migración de Microsoft, uno es el reemplazo oficial del otro. El producto cambió ocho veces. La tarea de decidir qué significa cada palabra del negocio nunca se fue.

[ Sube la figura 3: fig-escalera.png ]

Qué comprar según la pregunta

Ninguna generación eliminó a la anterior: la sábana sigue cuadrando cierres, Excel sigue en finanzas y el cubo sigue siendo la forma más rápida de comparar periodos. Para quien decide la inversión, la pregunta útil no es «¿cuál es la herramienta más nueva?», sino «¿qué tipo de pregunta necesita contestar el negocio?».

«Dame el detalle para conciliar» → Operativo, rastreable → Sábana / reporte tabular
«¿Qué pasa si…?» con supuestos propios → Escenarios → Hoja de cálculo o planeación (SAC)
«Compárame contra el año pasado por jerarquía» → Multidimensional → Cubo / modelo semántico
«Quiero ver dónde está el problema» → Exploratorio → Descubrimiento visual
«Cada mañana, los mismos indicadores» → Monitoreo → Dashboard o métricas con alerta (Pulse)
«¿Por qué pasó y qué sigue?», sin saber de antemano qué cruzar → Conversacional, de varios pasos → Agente (Copilot, Genie, Snowflake, Joule)

Tres recomendaciones para quien firma el presupuesto:

1. Antes de comprar el agente, haz el inventario de tu vocabulario. Si «venta neta» se calcula de tres formas en tres modelos, el agente va a escoger una, y con mucha seguridad. La capa semántica no es opcional: es lo que en realidad estás comprando.
2. Presupuesta al curador, no solo la licencia. Cada producto de la octava generación supone a alguien que escribe instrucciones, valida respuestas y mantiene ejemplos. Ese rol existe desde el universo de 1991; lo nuevo es que ahora su trabajo se puede medir.
3. Exige un examen y revísalo. Genie tiene benchmarks, Power BI tiene respuestas verificadas y Snowflake, verified queries. Úsalos, pero recuerda el estudio de Illinois: la respuesta de referencia también se equivoca, y quien la escriba tiene que conocer el negocio, no solo el SQL.

Si tu organización todavía tiene visuales de Q&A, tienes hasta febrero de 2027 para migrarlos. Es buena ocasión para preguntarte algo más de fondo: no qué herramienta los reemplaza, sino quién va a decidir qué significa cada pregunta que el negocio le haga al agente.

## CUERPO — copiar hasta aquí

---

## POST DE LANZAMIENTO (feed) — copiar de aquí

En febrero de 2027, los reportes de Power BI que todavía tengan un visual de Q&A van a mostrar un error donde antes había una respuesta.

Q&A salió en 2013 con una promesa: cualquiera podría preguntarle a sus datos en lenguaje natural. Tableau retiró su equivalente, Ask Data, en 2024. SAP sustituyó Search to Insight ese mismo año.

La primera generación de «pregúntale a tus datos» ya se retiró. La segunda se llama Copilot, Genie, Snowflake Intelligence, Just Ask, Joule.

Esta semana recorro ocho generaciones de reporting, producto por producto: la sábana, la hoja de cálculo, el cubo, la capa semántica, el descubrimiento visual, el self-service, la primera ola de IA y el agente. De cada una cuento qué análisis permitía y qué no.

Lo que más me llamó la atención fue la tabla de migración de Microsoft. El reemplazo oficial de Q&A Setup, donde se capturaban sinónimos a mano, es «Prep data for AI», donde se escriben instrucciones, respuestas verificadas y vocabulario del negocio.

El producto cambió ocho veces. La tarea de decidir qué significa cada palabra del negocio nunca se fue.

Y los benchmarks lo confirman. Un estudio presentado en CIDR 2026 encontró errores en las respuestas de referencia de dos de los exámenes de text-to-SQL más usados: en el 66 % de los problemas de uno y en el 53 % del otro. La parte difícil ya no es que el agente escriba buen SQL. Es que alguien sepa cuál es la respuesta correcta.

Cierro con una tabla de qué generación conviene según la pregunta del negocio, y con tres recomendaciones para quien firma el presupuesto.

Link en el primer comentario.

#GenBI #PowerBI #SAPAnalyticsCloud #Databricks #Snowflake #Tableau #CapaSemántica #ArquitecturaDeDatos

---

## PRIMER COMENTARIO (poner de inmediato)

Edición 14 completa, con las ocho generaciones, la misma pregunta escrita en SQL, MDX, DAX y como verified query, y la tabla de qué comprar según la pregunta:
https://rrbenavi-source.github.io/portfolio/publicaciones/de-la-sabana-al-agente

Y si te interesa la capa semántica a fondo, la edición 05, «La IA ya escribe SQL casi perfecto. ¿Con la semántica de quién?»:
https://rrbenavi-source.github.io/portfolio/publicaciones/semantica-de-quien

---

## VERSIÓN CORTA (para repostear en unos días)

La misma pregunta, en cuatro lenguajes.

«Venta del trimestre contra el mismo trimestre del año pasado, por región.»

En SQL la escribía sistemas. En MDX, «año anterior» era una función del cubo. En DAX, el analista la dejaba como medida en el modelo. Hoy, en un agente como Cortex Analyst de Snowflake, se guarda como verified query, y trae un campo que los otros tres no tenían: verified_by.

En los tres primeros, la definición vive en el código. En el último, además tiene nombre: alguien la verificó.

Antes de comprar el agente, conviene preguntarse quién va a ser ese alguien en tu organización.
