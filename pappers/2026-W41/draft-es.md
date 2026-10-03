# De la sábana al agente

## En febrero de 2027 Microsoft apaga Power BI Q&A, la función con la que en 2013 prometió que cualquiera podría preguntarle en lenguaje natural a sus datos. Tableau ya retiró Ask Data y SAP retiró Search to Insight. La primera generación de «pregúntale a tus datos» terminó, y la segunda ya está aquí. Esta edición recorre ocho generaciones de reporting, producto por producto: qué permitía cada una, qué no, y qué tipo de análisis estamos comprando hoy.

En febrero de 2027, los reportes de Power BI que todavía tengan un visual de Q&A van a mostrar un
error donde antes había una respuesta. Microsoft lo anunció en diciembre de 2025 para finales de 2026
y en septiembre extendió el plazo dos meses. El reemplazo oficial es Copilot.

Q&A nació en septiembre de 2013, en el preview de Power BI for Office 365. Era la función estrella:
escribías «ventas por región en 2013» y aparecía una gráfica. Tableau lanzó su equivalente, Ask Data,
en 2019 y lo retiró en febrero de 2024. SAP Analytics Cloud tenía Search to Insight; desde finales de
2024 su sucesor es Just Ask. Los tres fabricantes llegaron a la misma conclusión en menos de tres
años: la primera forma de preguntarle a los datos en lenguaje natural no sobrevivió.

Vale la pena entender por qué, y para eso hay que ver el camino completo. Llevo más de veinte años
construyendo reportes en casi todas las generaciones que siguen, y hay un patrón que se repite: cada
producto nuevo cambia **qué tipo de pregunta** puede hacer el negocio sin pedirle nada a TI. Ninguno
ha cambiado quién decide qué significa el número.

## Primera generación: la sábana

En los equipos de finanzas y operaciones de México le decimos **sábana** al reporte tabular largo:
cientos o miles de renglones impresos, o hoy exportados, con todas las columnas que alguien pidió
alguna vez. Es el reporte batch de los mainframes, el listado en COBOL o RPG, el ALV de ABAP en SAP y,
desde los noventa, Crystal Reports.

**Qué análisis permite:** operativo. Listar, filtrar, ordenar, subtotalizar. «Dame las facturas
abiertas de la sucursal 12 con más de 60 días.» Es la generación más vieja y la que menos ha muerto:
sigue siendo el formato con el que se cuadra un cierre, porque cada renglón se puede rastrear hasta
un documento.

**Qué no permite:** hacer una pregunta nueva. Cada variación es un requerimiento a sistemas. A
mediados de los setenta, IBM creó los *information centers* precisamente para atender la fila de
solicitudes que el área de sistemas no alcanzaba a resolver. El *backlog* de reportes es más viejo
que el PC.

## Segunda generación: la hoja de cálculo

VisiCalc salió en 1979 para la Apple II y se suele citar como la aplicación que convirtió a la
computadora personal en herramienta de negocio. Después vinieron Lotus 1-2-3 y Excel. Con Excel 5, en
1993, llegó la **tabla dinámica** (*PivotTable*), una idea que Lotus había probado antes en Improv.

**Qué análisis permite:** escenarios y resúmenes cruzados. «¿Qué pasa con el margen si el precio sube
3 %?» y «ventas por producto contra mes» sin escribir código. Es la primera vez que el usuario de
negocio arma su propio análisis.

**Qué no permite:** que dos personas lleguen al mismo número. La hoja trabaja sobre una extracción, y
cada extracción es una copia. Desde entonces, la pregunta más cara en una junta de dirección es
«¿cuál de los dos archivos es el bueno?».

## Tercera generación: el cubo

En 1993, Edgar F. Codd —el creador del modelo relacional— publicó con dos coautores el documento
que bautizó el **OLAP** (*Online Analytical Processing*): bases de datos organizadas para analizar,
no para registrar transacciones. Llegaron Essbase, Cognos PowerPlay, Microsoft Analysis Services y,
en 1998, SAP BW con su herramienta de consultas BEx.

**Qué análisis permite:** multidimensional. Cortar el dato por cualquier eje (*slice and dice*),
bajar por una jerarquía (región → zona → cliente) y comparar contra el mismo periodo del año
anterior con un clic. La comparación de periodos, que en la hoja era una fórmula frágil, en el cubo
es una función del motor.

**Qué no permite:** preguntar lo que no se modeló. El cubo contesta muy rápido, pero solo dentro de
las dimensiones y medidas que alguien diseñó por adelantado. Una pregunta fuera del diseño regresa
a la fila de requerimientos.

## Cuarta generación: la capa semántica

El 27 de noviembre de 1991, Business Objects presentó en Estados Unidos la patente 5,555,403. Su
objetivo, en palabras del documento: permitir que los usuarios consulten bases de datos relacionales
«sin conocer la estructura relacional ni el lenguaje SQL». La pieza central se llamaba **universo**:
una representación de la base de datos, fácil de entender, diseñada para un grupo de usuarios. Hoy le
decimos *semantic layer*. La patente, por cierto, hoy pertenece a SAP.

**Qué análisis permite:** consulta *ad hoc* gobernada. El usuario arrastra objetos de negocio
(«Cliente», «Ingreso», «Región») y la herramienta escribe el SQL. «Clientes con más de tres
devoluciones este trimestre», sin esperar a nadie y con la definición de «ingreso» que aprobó
finanzas.

**Qué no permite:** que el universo se mantenga solo. Alguien de TI tiene que agregar cada objeto,
cada sinónimo y cada regla. Conviene quedarse con esta idea, porque reaparece al final.

## Quinta generación: el descubrimiento visual

En 2002, Chris Stolte, Diane Tang y Pat Hanrahan publicaron en Stanford el sistema Polaris: un
lenguaje para consultar y graficar al mismo tiempo, arrastrando campos. De ahí nació Tableau. En
paralelo, QlikView llevó un motor asociativo que mostraba no solo lo que coincidía con un filtro, sino
también lo que quedaba fuera.

**Qué análisis permite:** exploratorio. Ver dónde se concentra la caída, encontrar un valor atípico en
un mapa, descubrir una relación que nadie había pedido. Es la primera generación en la que el análisis
empieza por mirar, no por preguntar.

**Qué no permite:** una sola verdad. Cada analista construye su propio libro de trabajo con sus
propios cálculos. El descubrimiento visual multiplicó los análisis y también las definiciones.

## Sexta generación: el self-service en la nube

Power BI salió a disponibilidad general el 24 de julio de 2015, después de un preview en el que
participaron más de 500,000 usuarios de 45,000 empresas, según Microsoft. Looker llevó el modelo
semántico a código (LookML) y SAP Analytics Cloud juntó BI, planeación y predicción en un solo
producto.

**Qué análisis permite:** modelado propio y dashboards compartidos. El analista de negocio construye
su modelo, escribe sus medidas (en DAX, en el caso de Power BI) y publica para su área. En SAC,
además, planea sobre el mismo modelo con el que reporta.

**Qué no permite:** controlar la proliferación. La misma facilidad que democratizó el reporte produjo
cientos de modelos con la misma medida calculada de formas distintas. La palomita de «certificado»
que analicé en la edición anterior nació para poner orden aquí.

## Séptima generación: la primera ola de inteligencia artificial

Aquí entran los productos del principio. Power BI Q&A (2013), Tableau Ask Data (2019) y SAC Search to
Insight intentaron que el usuario escribiera su pregunta. Junto con ellos llegó la **analítica
aumentada**: funciones que buscaban explicaciones solas, como Key Influencers en Power BI, Explain
Data en Tableau o Smart Insights en SAC.

**Qué análisis permite:** diagnóstico automatizado. «¿Qué factores explican que este cliente se
vaya?» o «¿por qué este punto se sale de la tendencia?», sin que el analista arme el modelo
estadístico.

**Qué no permite:** conversar. Estos motores reconocían palabras clave y las asociaban a columnas.
Para que funcionaran, alguien tenía que capturar sinónimos y relaciones a mano: en Power BI se llamaba
*Q&A Setup*, con su diccionario de sinónimos, sus relaciones lingüísticas y la opción de «enseñarle» a
Q&A. Si el usuario escribía «facturación» y el sinónimo no existía, no había respuesta. Por eso se
retiraron: no era mala idea, era un método que no escalaba.

## Octava generación: el agente

La generación actual usa modelos de lenguaje grandes (LLM) para entender la intención de la pregunta,
escribir la consulta, ejecutarla y explicar el resultado. Se le dice *GenBI* (BI generativo) o, cuando
el sistema encadena varios pasos por su cuenta, analítica agéntica. Estos son los productos que hoy
compiten, con una pregunta de ejemplo para cada uno:

- **Copilot en Power BI.** Contesta preguntas sobre el modelo semántico, analiza los visuales de un
  reporte, crea páginas nuevas y escribe consultas DAX. Desde este año está disponible a partir de la
  capacidad Fabric más chica (F2). *«Resúmeme qué cambió en el reporte de ventas esta semana.»*
- **Databricks Genie.** Disponible de forma general desde junio de 2025. Contesta con texto, tabla y
  gráfica, y enseña el SQL que usó. Databricks anunció además un modo de investigación para preguntas
  de varios pasos que plantea y prueba varias hipótesis. *«¿Por qué cayó el margen en el norte en
  agosto?»*
- **El agente de Snowflake.** Lanzado como Snowflake Intelligence y disponible de forma general desde
  noviembre de 2025 (la documentación hoy lo llama Snowflake CoWork). Se apoya en Cortex Analyst para
  convertir preguntas en SQL sobre *semantic views*. *«¿Cuáles son los diez clientes que más crecieron
  contra el año pasado?»*
- **SAP Analytics Cloud: Just Ask y Joule.** Just Ask contesta preguntas sobre modelos de SAC que
  previamente se indexan; Joule agrega la conversación, es decir, recuerda el contexto de la pregunta
  anterior. *«Ahora muéstramelo solo para el canal moderno.»*
- **Tableau Pulse.** No espera la pregunta: vigila métricas definidas una sola vez en su *metrics
  layer* y avisa cuando algo cambia y por qué. *«Tu métrica de devoluciones subió 12 %; el principal
  factor es la región occidente.»*
- **Looker Conversational Analytics.** Usa Gemini y se apoya en las definiciones de LookML para que la
  respuesta use el mismo cálculo que el resto de la empresa.

**Qué análisis permite:** conversacional y de varios pasos. Por primera vez, una sola pregunta puede
combinar lo descriptivo (qué pasó), lo diagnóstico (por qué) y una proyección (qué pasa si sigue
así). Y la pregunta se hace con las palabras del negocio, no con las del modelo.

**Qué no permite, todavía:** garantizar la misma respuesta. Lo dice Microsoft en su propia
documentación: la preparación de datos para IA «no puede asegurar un resultado específico cada vez»,
porque el comportamiento de la IA no es determinista.

Hay un dato que conviene tener presente desde Monterrey: según la documentación de Microsoft
actualizada en septiembre, la experiencia independiente de Copilot en Power BI todavía no está
disponible en la región de Azure de México. Antes de diseñar la estrategia, vale la pena confirmar
dónde vive la capacidad.

## ¿Qué tan bien contesta un agente?

La mejor referencia pública es Spider 2.0, un benchmark académico presentado en ICLR 2025 con 632
problemas tomados de bases de datos empresariales reales, muchas con más de mil columnas. Cuando
salió, el mejor agente (sobre el modelo o1-preview de OpenAI) resolvía el **21.3 %** de las tareas; ese
mismo enfoque resolvía 91.2 % en el benchmark anterior, mucho más sencillo. A octubre de 2026, el
primer lugar del *leaderboard* en la versión sobre Snowflake reporta **96.7 %**. En la versión que
mezcla varios motores de base de datos, el primer lugar está en **76.2 %**. El avance es real y fue
rápido: menos de dos años.

Pero hay un dato que me parece más importante. En enero de 2026, un equipo de la Universidad de
Illinois revisó las respuestas de referencia de dos benchmarks muy usados. En la versión de Spider 2.0
sobre Snowflake encontró errores de anotación en el **66.1 %** de los problemas, y en BIRD, en el
**52.8 %**. Al corregirlos, el desempeño de los sistemas cambió hasta 31 % y el ranking se movió hasta
tres lugares. Varias de esas fallas son de conocimiento de dominio: la respuesta «correcta» no
entendía lo que la pregunta de negocio realmente pedía.

Dicho de otra forma: la parte difícil no es que el agente escriba buen SQL. Es que alguien sepa cuál
es la respuesta correcta.

## Lo que no cambió en ocho generaciones

Si se lee la documentación de los productos de la octava generación, todos piden lo mismo antes de
prometer nada:

- **Power BI** pide preparar el modelo semántico con un esquema de datos para IA, **respuestas
  verificadas** (un visual que se devuelve cuando alguien hace cierta pregunta) e **instrucciones de
  IA** con la lógica y el vocabulario del negocio. Y después, marcar el modelo como «aprobado para
  Copilot».
- **Databricks** dice que quien arme un espacio de Genie «necesita entender los datos» y que «los
  analistas que dominan SQL normalmente tienen el conocimiento» para curarlo. Recomienda empezar «lo
  más pequeño posible» y seguir agregando contexto según la retroalimentación de los usuarios.
- **Snowflake** reconoce que las soluciones genéricas «batallan» para convertir texto a SQL «cuando
  solo tienen el esquema de la base de datos», porque al esquema le faltan las definiciones del
  proceso de negocio y de las métricas.
- **SAP** ofrece una revisión de *readiness* para dejar el modelo listo antes de que Just Ask y Joule
  lo usen.

Gartner lo dijo en mayo sin rodeos: los modelos de datos basados solo en esquemas «ya no son
suficientes» para la IA agéntica, porque les falta contexto de negocio y significado. Y en marzo
predijo que para 2030 las capas semánticas universales se tratarán como infraestructura crítica, al
mismo nivel que la plataforma de datos y la ciberseguridad.

Vuelvo al universo de 1991. El problema que resolvía era el mismo: traducir el lenguaje del negocio a
la estructura de la base de datos. Lo que pedía Q&A Setup en 2013 —sinónimos, relaciones, enseñarle
a la herramienta— es casi lo mismo que pide hoy «Prep data for AI». Microsoft lo hizo explícito: en su
tabla de migración, el reemplazo de Q&A Setup es precisamente Prep data for AI. **El producto cambió
ocho veces. La tarea de decidir qué significa cada palabra del negocio nunca se fue.**

## Qué comprar según la pregunta

Ninguna generación eliminó a la anterior. La sábana sigue cuadrando cierres, Excel sigue en todas las
áreas de finanzas y el cubo sigue siendo la forma más rápida de comparar
periodos. Para quien decide la inversión, la pregunta útil no es «¿cuál es la herramienta más nueva?»
sino «¿qué tipo de pregunta necesita contestar el negocio?».

| Si la pregunta es… | El análisis es… | La generación que mejor la contesta |
|---|---|---|
| «Dame el detalle para conciliar» | Operativo, rastreable | Sábana / reporte tabular |
| «¿Qué pasa si…?» con supuestos propios | Escenarios | Hoja de cálculo o planeación (SAC) |
| «Compárame contra el año pasado por jerarquía» | Multidimensional | Cubo / modelo semántico |
| «Quiero ver dónde está el problema» | Exploratorio | Descubrimiento visual |
| «Cada mañana, los mismos indicadores» | Monitoreo | Dashboard o métricas con alerta (Pulse) |
| «¿Por qué pasó y qué sigue?», sin saber de antemano qué cruzar | Conversacional, de varios pasos | Agente (Copilot, Genie, Snowflake, Joule) |

Tres recomendaciones para quien firma el presupuesto:

1. **Antes de comprar el agente, haz el inventario de tu vocabulario.** Si «venta neta» se calcula de
   tres formas en tres modelos, el agente va a escoger una, y lo hará con mucha seguridad. El trabajo
   de la capa semántica no es opcional; es lo que se está comprando en realidad.
2. **Presupuesta al curador, no solo la licencia.** Cada producto de la octava generación nombra a
   alguien que escribe instrucciones, valida respuestas y mantiene ejemplos. Ese rol existe desde el
   universo de 1991; lo nuevo es que ahora su trabajo se puede medir.
3. **Exige un examen y revísalo.** Genie tiene *benchmarks*, Power BI tiene respuestas verificadas,
   Snowflake tiene *verified queries*. Úsalos, pero recuerda el estudio de Illinois: la respuesta de
   referencia también se equivoca. Quien la escriba tiene que conocer el negocio, no solo el SQL.

Si tu organización todavía tiene visuales de Q&A, tienes hasta febrero para migrarlos. Es una buena
ocasión para preguntarse algo más de fondo: no qué herramienta los reemplaza, sino quién va a decidir,
de aquí en adelante, qué significa cada pregunta que el negocio le haga al agente.

---

## Fuentes

- Microsoft Fabric Community, Power BI Updates Blog — *Power BI Q&A retirement reminder: February 2027
  timeline update* (Mohammad Ali, Power BI Team, sep-2026): retiro extendido de dic-2026 a feb-2027;
  tabla de reemplazos (Q&A Setup → Prep Data for AI); Copilot desde capacidad F2.
  https://community.fabric.microsoft.com/blog/fbc_pbiupdatesblog/power-bi-qa-retirement-reminder-february-2027-timeline-update/5365841
- Microsoft 365 Message Center — MC1218421, *Retirement of Power BI Q&A* (16-ene-2026).
  https://mc.merill.net/message/MC1218421
- Microsoft SQL Server Blog — *Microsoft Updates Power BI for Office 365 Preview with New Natural
  Language Search…* (25-sep-2013).
  https://www.microsoft.com/en-us/sql-server/blog/2013/09/25/microsoft-updates-power-bi-for-office-365-preview-with-new-natural-language-search-mapping-capabilities/
- Microsoft Learn — *Prepare your data for AI to improve Copilot results* (act. 16-sep-2026): AI data
  schema, verified answers, AI instructions, «Approved for Copilot», no determinismo, disponibilidad
  regional.
  https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai
- Microsoft Power BI Blog — *Power BI is Generally Available today* (24-jul-2015) y Official
  Microsoft Blog (10-jul-2015): 500,000 usuarios de 45,000 empresas en el preview.
  https://blogs.microsoft.com/blog/2015/07/10/over-500000-unique-users-from-45000-companies-across-185-countries-helped-shape-the-new-power-bi/
- Tableau Help — *Automatically Build Views with Ask Data*: retiro en Tableau Cloud (feb-2024) y
  Tableau Server 2024.2.
  https://help.tableau.com/current/pro/desktop/en-us/ask_data.htm
- SAP Knowledge Base Article 3532315 — *Deprecation of Search to Insight feature in SAP Analytics
  Cloud* (deprecación desde QRC Q4 2024; sucesor Just Ask).
  https://userapps.support.sap.com/sap/support/knowledge/en/3532315
- SAP Help Portal — *Check Your Model's Readiness for Just Ask and Joule Analytical Insights*.
  https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/18850a0e13944f53aa8a8b7c094ea29e/121c342e23124efb8295f1bb785b2cc0.html
- Databricks — *AI/BI Genie is now Generally Available* (12-jun-2025).
  https://www.databricks.com/blog/aibi-genie-now-generally-available
- Databricks — *Curate an effective Genie space* (best practices, act. 11-sep-2026).
  https://docs.databricks.com/aws/en/genie/best-practices
- Snowflake — Release note *Nov 04, 2025: Snowflake CoWork (General availability)* y documentación de
  *Cortex Analyst* (semantic views, verified queries).
  https://docs.snowflake.com/en/release-notes/2025/other/2025-11-04-snowflake-intelligence
  https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
- Google Cloud — *Conversational Analytics in Looker overview*.
  https://docs.cloud.google.com/looker/docs/conversational-analytics-overview
- Tableau — *Now Available in 2024.1 Release: Tableau Pulse, Metrics Layer…*
  https://www.tableau.com/blog/release-tableau-pulse-metrics-layer-viz-navigation
- Cambot, J.-M. y Liautaud, B. — US Patent 5,555,403, *Relational database access system using
  semantically dynamic objects* (presentada 27-nov-1991, otorgada 10-sep-1996).
  https://patents.google.com/patent/US5555403A/en
- Stolte, C., Tang, D. y Hanrahan, P. — *Polaris: A System for Query, Analysis, and Visualization of
  Multidimensional Relational Databases*. IEEE TVCG 8(1):52-65, 2002.
- Codd, E. F., Codd, S. B. y Salley, C. T. — *Providing OLAP to User-Analysts: An IT Mandate* (1993).
- Carr, H. H. — *Information Centers: The IBM Model vs. Practice*. MIS Quarterly 11(3):325-338, 1987.
  https://aisel.aisnet.org/misq/vol11/iss3/5/
- Lei, F. et al. — *Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL
  Workflows*. ICLR 2025. Leaderboard consultado el 1-oct-2026.
  https://spider2-sql.github.io/
- Jin, T., Choi, Y., Zhu, Y. y Kang, D. — *Text-to-SQL Benchmarks are Broken: An In-Depth Analysis of
  Annotation Errors*. CIDR 2026.
  https://www.vldb.org/cidrdb/papers/2026/p5-jin.pdf
- Gartner — *Gartner Announces Top Predictions for Data and Analytics in 2026* (11-mar-2026) y
  *Gartner Says Lack of Semantics Causes Inaccurate AI Agents and Wasted Spending* (11-may-2026).
  https://www.gartner.com/en/newsroom/press-releases/2026-03-11-gartner-announces-top-predictions-for-data-and-analytics-in-2026
  https://www.gartner.com/en/newsroom/press-releases/2026-05-11-gartner-says-lack-of-semantics-causes-inaccurate-artificial-intelligence-agents-and-wasted-spending
