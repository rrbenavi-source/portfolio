# Brújula — Edición 06 (2026-W33) · Material copy-paste

_Publica: martes 2026-08-18, 9:00 AM CDMX. Todo lo de abajo está listo para
pegar; las marcas `[ Sube la figura: … ]` indican dónde insertar cada imagen en
el editor de LinkedIn._

---

## Título del artículo

Automatizar el pipeline no es automatizar las reglas de negocio

## Subtítulo

El primer benchmark de agentes sobre pipelines reales dice exactamente dónde se rompen

## Portada

[ Sube la portada: `brujula-cover-06.png` (1920×1080) ]

---
---

## CUERPO DEL ARTÍCULO (pegar completo)

En abril de 2025, tres investigadores de la Universidad de Illinois publicaron el primer examen serio a una pregunta que muchos nos hacíamos en voz baja: ¿puede un agente de IA —un modelo que no solo responde, sino que ejecuta comandos, escribe archivos y corrige sus propios errores— construir un pipeline de datos completo, de principio a fin?

El examen se llama ELT-Bench, por las tres etapas de un pipeline, la cadena que mueve el dato del sistema origen al reporte: extract (sacarlo de la fuente), load (aterrizarlo en el warehouse) y transform (convertirlo en las tablas de negocio con las que alguien decide).

No son ejercicios triviales: 100 pipelines, 835 tablas fuente y 203 data models, cada uno con su regla de cálculo adentro. El agente se conecta a las fuentes, lee documentación, escribe código y SQL, y orquesta cada etapa.

El mejor agente de aquella corrida —Spider-Agent con Claude 3.7 Sonnet y razonamiento extendido— obtuvo 57% en extracción y carga. Y 3.9% en transformación.

Ese contraste es el argumento entero. Pero hay que decir algo que casi nadie dice al citar un estudio de IA: fue hace dieciséis meses, y en este campo dieciséis meses son una era.

**Un año después, la mitad del problema desapareció**

En abril de 2026, un equipo de IBM Research y ETH Zúrich volvió a correr el examen con modelos actuales y publicó ELT-Bench-Verified. Los números nuevos:

Extracción y carga: de 57% (Claude 3.7 Sonnet, 2025) a 96–98% (Claude Sonnet 4.5, 2026)
Transformación: de 3.9% a 32.5%

El rango no es incertidumbre: son dos agentes distintos con el mismo modelo, y el más simple obtuvo 98%.

Conectar la fuente, autenticarse, aterrizar el dato en el warehouse: eso se resolvió. Pasó de fallar cuatro de cada diez veces a fallar una de cada treinta. Es un examen controlado y no tu operación —ahí las fuentes están más sucias—, pero la tendencia es inequívoca. Si tu trabajo, o el de tu proveedor, consiste en construir y mantener esas conexiones, conviene enterarte por un estudio y no por una renovación de contrato.

La transformación también mejoró, y mucho: se multiplicó por ocho. Pero sigue fallando dos de cada tres veces.

Observa el orden, no solo los números: la brecha se cierra de abajo hacia arriba, primero lo mecánico y al final lo semántico. Y no es casualidad.

[ Sube la figura: `fig-abajo-hacia-arriba.png` — La brecha se cierra de abajo hacia arriba: lo mecánico se resolvió; lo semántico apenas se movió ]

La IA es extraordinaria con lo que está escrito en algún lugar del mundo, e inútil con lo que nunca se escribió. Cómo autenticarse contra la API de Salesforce está documentado en mil tutoriales. Qué es una venta neta en tu empresa —qué descuentos entran, qué devoluciones se restan, en qué momento del calendario fiscal se reconoce, por qué esas tres sociedades no consolidan igual— no está escrito en ninguna parte. Vive en la cabeza de tres personas y en un user exit de 2009: código a la medida injertado en el estándar de SAP.

**El dato que cambia la pregunta**

Aquí el estudio de 2026 deja de hablar de la IA y empieza a hablar de nosotros.

Antes de publicarlos, el equipo auditó por qué fallaban los agentes en transformación. Revisaron a mano las 81 tareas fallidas esperando errores del modelo. Encontraron otra cosa.

De los desajustes a nivel de columna, un tercio no eran errores del agente: eran errores del examen. Falsos positivos de la evaluación, descripciones ambiguas, y ground truth —la respuesta contra la que se califica— que simplemente estaba mal. El 82.7% de esas tareas fallidas tenía algún problema de este tipo.

El 32.5% de arriba, de hecho, ya es el número corregido. Con la calificación original, ese mismo agente obtenía 22.66%. Casi diez puntos que no venían del modelo: venían de los errores del examen.

Y el detalle que a mí me detuvo en seco: hubo 30 columnas —el 1.2% del total— que tuvieron que eliminar del examen porque no lograron establecer la respuesta correcta. ¿La razón? Al interpretar la misma especificación, los expertos coincidieron apenas el 57.8% de las veces.

Léelo otra vez. Expertos. Con la definición escrita enfrente. Poniéndose de acuerdo sobre qué significa una columna poco más de la mitad del tiempo.

[ Sube la figura: `fig-acuerdo-experto.png` — Un tercio de los desajustes eran errores del examen; y los expertos solo coincidieron el 57.8% de las veces al leer la misma especificación ]

Ese número replantea el problema. La transformación no se resiste porque el modelo sea limitado. Se resiste porque la regla de negocio nunca se escribió sin ambigüedad — y cuando obligas a gente experta a escribirla, descubres que ni entre ellos hay acuerdo. El cuello de botella no está en la máquina que ejecuta: está en la definición que nadie cerró.

Si eso pasa en un benchmark académico —una prueba construida a propósito para ser evaluable— con gente pagada para ser precisa: ¿qué probabilidad le das a "dame las ventas netas del mes", dicho en una junta, contra un modelo de datos que nadie documentó?

**Dónde vive esto en una operación SAP**

Si trabajas sobre SAP, ya sabes exactamente dónde está tu 32.5%.

Está en el extractor —el programa que saca el dato del sistema— que alguien parchó en 2011 para excluir tres tipos de documento, sin dejar comentario. Está en el user exit que reescribe el centro de beneficio bajo una condición que solo conoce quien lo programó. Está en el reporte Z que la dirección usa cada mes y que produce un número distinto al del dashboard oficial, y en la respuesta que todos aceptamos: "es que ese reporte calcula diferente".

Esa es tu capa de transformación. No está en el pipeline: está enterrada en veinte años de decisiones correctas, tomadas por gente competente que resolvió un problema real un martes y no tuvo tiempo de documentarlo.

Ninguna herramienta de migración automática va a extraer eso, porque no es código: es intención. La herramienta traduce lo que el código hace; la pregunta que decide tu proyecto es por qué lo hace.

**La factura que se está acumulando**

Mientras tanto, los equipos de datos están usando la IA exactamente al revés de lo que convendría.

El State of Analytics Engineering 2026 de dbt Labs —363 profesionales y líderes de datos— encontró que 72% prioriza la IA para escribir código, y solo 24% la prioriza para gestionar el pipeline: pruebas, observabilidad, control de calidad. Se está priorizando la creación tres veces más que el control.

En el mismo reporte, 71% teme que salidas incorrectas o alucinadas —números que el modelo inventa y entrega con total naturalidad— lleguen a los stakeholders que van a decidir con ellos. Y 77% de los líderes reporta estar empujando a sus equipos a producir más rápido con IA.

Siete de cada diez temen la consecuencia que casi ocho de cada diez líderes están acelerando.

Nadie está comprando velocidad. Están comprando volumen sin punto de control: sin nadie que revise antes de que el número salga.

**Dónde sí rinde**

Nada de esto es un argumento contra la IA. Yo la uso todos los días: este newsletter y el portafolio donde se publica están construidos con ella. El argumento es sobre dónde ponerla.

Hay tres trabajos donde la IA sí le rinde a un arquitecto de datos.

Completar especificaciones. Llevar una especificación del 60% al 95%, porque el modelo pregunta por los casos límite que tú ya no ves de tan cerca que los tienes. Es el mejor uso que le he encontrado, y conecta con la edición 02: el diseño es la migración. Una especificación que contempla el caso raro vale más que un pipeline escrito rápido.

La autopsia semántica de los sistemas heredados. Leer 300 reportes Z ajenos y extraer la regla de negocio enterrada en cada uno. Ningún humano cansado le gana a una máquina en eso: es volumen, es tedioso, y el resultado se verifica contra datos reales. Es, a escala, la edición 04: la autopsia de un solo reporte Z.

El linaje —de dónde viene cada número y por dónde pasó— y la documentación que nadie escribió.

Los tres comparten la misma firma, y ahí está la regla práctica: el insumo está escrito pero disperso, y el resultado se verifica en minutos. Cuando una tarea cumple esas dos condiciones, la IA es un multiplicador enorme. Cuando no, estás moviendo trabajo, no eliminándolo.

**La regla y su corolario**

De todo lo anterior salen dos reglas.

La primera: nunca le pidas a la IA algo que no sepas verificar. Si no puedes evaluar el resultado en menos tiempo del que te habría tomado producirlo, no ganaste nada: moviste el trabajo a donde ya no lo estás midiendo. Y no es un costo teórico: una corrida completa del examen de 2026 costó alrededor de $343 y más de dos días. Verificar en serio siempre cuesta; la pregunta es si lo pagas a propósito o por accidente.

La segunda es la que de verdad decide el año: cada hora que la IA te ahorra en el trabajo mecánico tiene que reinvertirse en las reglas de negocio, que es lo único que no puede hacer sola.

Si ese ahorro se convierte en más pipelines en lugar de mejores definiciones, compraste deuda a plazos. Y la primera mensualidad llega el día que un agente conteste una pregunta de negocio con un número impecable que nadie firmó.

La extracción y la carga ya no son tu trabajo. Empieza a comportarte como si eso fuera cierto.

—

📍 La versión completa, con las fuentes verificadas (arXiv, IBM Research + ETH Zúrich, dbt Labs), está en mi portfolio — link en el primer comentario.

---
---

## POST DE LANZAMIENTO (feed, publicar el martes al salir la edición)

Un agente de IA ya construye la mitad de tu pipeline. La otra mitad no la va a tocar.

En abril de 2025, ELT-Bench midió por primera vez a los agentes construyendo pipelines completos: 100 pipelines, 835 tablas fuente, 203 data models. El mejor agente: 57% en extracción y carga, 3.9% en transformación.

Un año después, IBM Research y ETH Zúrich volvieron a correr el examen con modelos actuales.

📈 Extracción y carga: 96–98%. Eso se resolvió.
📉 Transformación: 32.5%. Sigue fallando dos de cada tres veces.

La brecha se cierra de abajo hacia arriba: primero lo mecánico, al final lo semántico. Y no es casualidad. La IA es extraordinaria con lo que está escrito en algún lugar del mundo, e inútil con lo que nunca se escribió.

🔍 Pero el dato que me detuvo en seco está en la auditoría del examen. Al revisar por qué fallaban los agentes, encontraron que un tercio de los desajustes no eran errores del modelo: eran errores del examen. Y 30 columnas tuvieron que eliminarse porque, al interpretar la misma especificación escrita, los expertos coincidieron apenas el 57.8% de las veces.

Expertos. Con la definición enfrente. De acuerdo poco más de la mitad del tiempo.

La transformación no se resiste porque el modelo sea limitado. Se resiste porque la regla de negocio nunca se escribió sin ambigüedad.

🏭 Si trabajas sobre SAP, ya sabes dónde está tu 32.5%: en el extractor que alguien parchó en 2011 sin dejar comentario, en el user exit que reescribe el centro de beneficio, en el reporte Z que da otro número y todos aceptamos que "calcula diferente".

⚠️ Y mientras tanto, dbt Labs encontró que 72% de los equipos prioriza la IA para escribir código y solo 24% para controlar el pipeline. Siete de cada diez temen que un número alucinado llegue a un stakeholder — y casi ocho de cada diez líderes están acelerando exactamente eso.

En la Edición 06 de Brújula: los dos benchmarks completos, dónde sí rinde la IA para un arquitecto de datos, y la regla que decide el año.

👉 La regla: cada hora que la IA te ahorra en el trabajo mecánico tiene que reinvertirse en las reglas de negocio. Si ese ahorro se convierte en más pipelines en lugar de mejores definiciones, compraste deuda a plazos.

¿Cuántas de tus reglas de negocio están escritas en algún lado — y cuántas viven en la cabeza de tres personas?

#DataEngineering #IA #Agentes #SAP #Analytics #dbt

---
---

## PRIMER COMENTARIO (pegar inmediatamente después de publicar el post)

La versión completa, con fuentes verificadas y las dos figuras, está aquí 👇

📄 Artículo: https://rrbenavi-source.github.io/portfolio/publicaciones/automatizar-el-pipeline

🇬🇧 English version: https://rrbenavi-source.github.io/portfolio/en/publicaciones/automatizar-el-pipeline
