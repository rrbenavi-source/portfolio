TÍTULO:  El near real time que el lakehouse no te iba a dar

SUBTÍTULO:  Por qué el reporte operativo de las 8 a.m. no siempre pertenece al data lake

PORTADA:  brujula-cover-03.png   ← (pendiente de render; ver nota al final)


═══════════════════════════════════════════════════════
  NEWSLETTER — copia desde aquí
═══════════════════════════════════════════════════════

[ Sube la portada: brujula-cover-03.png ]

Cuando llegué al proyecto, la arquitectura ya estaba decidida: llevar los datos a un lakehouse y reportar en la herramienta de BI corporativa. Es la respuesta por defecto de 2026, y en el papel cuesta discutirla —democratización, escalabilidad, todo en un solo lugar—.

Pero el requisito real la puso a prueba en la primera reunión. El negocio no quería otro reporte. Quería actuar durante el día, no enterarse al día siguiente.

El equipo de preventa necesitaba ver, en campo y desde el teléfono, cómo iba la colocación de pedidos cada media hora: cuánto volumen llevaban contra el mismo día del año pasado, qué cobertura de clientes tenían contra su plan de visitas, y dónde había una brecha contra la meta que exigiera moverse antes de que terminara la jornada.

El estado previo sí tiene números, y son lo único medido hasta ahora: la información salía de un reporte armado a mano, con solo tres cortes al día y unas quince horas-persona por semana de trabajo manual, con datos que ya nacían viejos y errores de captura. La pregunta de negocio no era "¿cómo me fue ayer?", era "¿alcanzo la meta hoy, y qué muevo ahora si no?".

Que esa pregunta importe no es una intuición. La investigación de MIT CISR con Insight Partners sobre real-time businesses encontró que las empresas en el cuartil superior de "real-time-ness" tuvieron 62% más crecimiento de ingresos y 97% más margen que las del cuartil inferior. Ese es el dato de la industria, no el mío: el dashboard apenas está por liberarse y el impacto real está por medirse. Lo que sí puedo defender hoy es la decisión de arquitectura. Y ahí la ruta "moderna" chocó con una verdad incómoda: para ese near real time, meter un data lake en medio no agregaba capacidad. Agregaba latencia.

[ Sube la figura: fig-premio-tiempo-real.png ]


La distinción que casi nadie hace explícita

Conviene ser preciso, porque es fácil caricaturizar el argumento. No estoy diciendo que un lakehouse no pueda hacer streaming —puede—. Lo que digo es más fino, y es la tesis de esta edición:

Cuando el dato transaccional y su lógica de negocio ya viven gobernados dentro de SAP, el camino más corto para monitoreo operativo en tiempo casi real es traer la query a donde vive la verdad —no mover la verdad para alcanzarla—.

Esto tiene nombre en arquitectura: data gravity. Mientras más grande y compleja es una masa de datos, más caro y lento es moverla; así que lo económico es acercar el cómputo al dato, no el dato al cómputo. Y no era un SELECT sobre una tabla plana: era volumen convertido a dos unidades por un motor de conversión, comparado contra el día equivalente del año anterior, restringido por las autorizaciones de cada usuario y fusionado con pedidos que llegan por una interfaz externa no-SAP. Toda esa lógica ya estaba construida y gobernada en el data warehouse.


El último kilómetro: donde el near real time se muere

Para servir eso desde un lake, el trabajo de verdad no es "conectar Databricks". Es replicar el stream hacia el object store, rearmar las capas Medallion y volver a implementar la semántica de SAP en una segunda plataforma. Y ese último kilómetro es donde los proyectos se atoran —y no lo dice un vendor que vive de venderte la transformación, lo dice la mismísima SAP—.

En un blog técnico de su comunidad, SAP lo reconoce con todas sus letras: el business context —conversiones de moneda, unidades de medida, jerarquías y configuraciones de seguridad— se puede perder al replicar hacia afuera, y necesitas trabajo extra en el destino para reconstruirlo. Con las autorizaciones es todavía más claro: al replicar hacia afuera se pierden todas las configuraciones de seguridad, y no queda más que volver a crear el control de acceso en el sistema destino de terceros.

Eso —conversión de moneda, jerarquías, seguridad row-level— es justo la lógica que mi requerimiento necesitaba y que ya vivía gobernada en el warehouse.

En la práctica, la rama del lake ni se acercaba. En el mejor de los casos la latencia end-to-end se iba a dos o tres horas; y siendo francos, el plan la dejó en dos cargas al día. En cualquiera de los dos escenarios estamos hablando de cuatro a seis veces la ventana de treinta minutos que el negocio necesitaba. El near real time se esfumaba justo en la capa que, se suponía, venía a modernizarlo.


El tiempo real no lo pone el destino, lo pone el extractor

La parte contraintuitiva es que el "casi tiempo real" no es un problema de la herramienta de visualización. Es un problema de ingeniería de extracción, y se resuelve donde nace el dato.

El flujo que sí entregó los treinta minutos es sobrio y aburrido, y por eso funciona: el DataSource estándar de posiciones de venta (2LIS_11_VAITM) alimenta vía ODP, con el extractor LO en modo queued delta para no golpear el performance del sistema transaccional. Esos micro-lotes aterrizan en un ADSO con change log activo, cuyas tablas inbound y active colapsan los deltas casi al instante, orquestado por Streaming Process Chains en bucle continuo. Encima, la visualización se conecta en modo Live: análisis sin replicación de datos, con la seguridad del sistema origen heredada tal cual. Elegir Live no fue estética: fue elegir no reimplementar la semántica de SAP en otra plataforma.

[ Sube la figura: fig-arquitectura-latencia.png ]

El resultado se libera como un dashboard móvil que el preventista abre en la calle, con el avance vs. el año anterior, la cobertura contra el visit list y la brecha contra la meta en una sola vista. No es una arquitectura vistosa. Es la que hace que el número de las 8 a.m. sea defendible a las 8:01.


Cuándo el lake sí paga

Nada de esto es un argumento contra el lakehouse. Es un argumento contra usarlo como respuesta por defecto a una pregunta que no es la suya. El lake paga —y mucho— cuando el caso es data science, cruce de datos SAP con no-SAP a gran escala, o machine learning sobre históricos profundos. Ahí la gravedad del dato juega al revés y mover todo a un motor abierto es exactamente lo correcto.

El error de arquitectura no es elegir Databricks. Es no separar dos problemas distintos: el reporte operativo near-real-time que el negocio necesita este trimestre, y la plataforma de analítica avanzada que la organización quiere construir. Son cadencias distintas, dueños distintos y caminos técnicos distintos. Cuando los fusionas en un solo proyecto "moderno", la ambición de plataforma se come el valor operativo que ya podías liberar hoy.


El norte

Que una iniciativa dé o no el número esperado es una hipótesis de negocio; que la arquitectura sea la correcta para el requisito es una decisión que ya se puede juzgar. La segunda no depende de la primera. El requisito era treinta minutos sin duplicar el dato ni reimplementar su semántica, y eso se cumplió.

“Antes de elegir la plataforma, pregunta dónde vive ya la lógica gobernada de tu número. Si la respuesta es 'en el sistema de origen', tu trabajo de arquitecto no es mudarla: es acortar la distancia entre esa verdad y quien tiene que actuar sobre ella.”

Y a veces la distancia más corta es la que no pasa por el lake. Ese es el norte que no conviene perder.


🧭 Brújula es mi newsletter semanal: de los datos a las decisiones, sin perder el norte. Cada semana, un análisis sin humo sobre arquitectura de datos, SAP, generative BI y la estrategia para volverte data-driven.

📖 El análisis completo, con las 8 fuentes enlazadas, está en mi portfolio:
https://rrbenavi-source.github.io/portfolio/publicaciones/near-real-time-lakehouse

Y una pregunta para ti que estás por "modernizar" un reporte: ¿ya te preguntaste dónde vive hoy la lógica gobernada de ese número… antes de decidir moverla?

═══════════════════════════════════════════════════════
  NEWSLETTER — copia hasta aquí
═══════════════════════════════════════════════════════




═══════════════════════════════════════════════════════
  POST DE LANZAMIENTO (para tu feed) — copia desde aquí
═══════════════════════════════════════════════════════

Llegué a un proyecto donde la arquitectura ya estaba decidida: todo al lakehouse y a reportar en la herramienta de BI corporativa. La respuesta por defecto de 2026.

Pero el negocio no quería otro reporte. Quería actuar durante el día: ver la colocación de pedidos cada 30 minutos y mover la brecha contra la meta antes de que cerrara la jornada.

Y ahí la ruta "moderna" chocó con una verdad incómoda:

Para ese near real time, meter un data lake en medio no agregaba capacidad. Agregaba latencia.

→ La ruta corta (extracción ODP en streaming → BW/4HANA → SAC Live) entregaba ~30 minutos.
→ La ruta lake, en el mejor caso, se iba a 2–3 horas; el plan la dejó en 2 cargas diarias. Cuatro a seis veces la ventana que el negocio necesitaba.

¿Por qué? Porque el "último kilómetro" no es "conectar Databricks": es volver a implementar la semántica de SAP —moneda, jerarquías, seguridad row-level— en una segunda plataforma. Y no lo digo yo, lo admite la propia SAP: ese business context se pierde al replicar hacia afuera.

La lección, en una línea:

El tiempo real no lo pone el destino, lo pone el extractor.

Esto NO es "el lake es malo". El lake paga —y mucho— en data science y ML. El error es no separar dos problemas: el reporte operativo de este trimestre y la plataforma de analítica que quieres construir.

Nueva edición de Brújula 🧭. El análisis completo, con el caso y las fuentes, en el primer comentario. 👇

#DataEngineering #SAP #BW4HANA #Lakehouse #Databricks #RealTimeAnalytics #Arquitecturadedatos

═══════════════════════════════════════════════════════
  POST — copia hasta aquí
═══════════════════════════════════════════════════════


PRIMER COMENTARIO (pégalo aparte, debajo de tu post):

📖 Edición 03 de Brújula, completa y con fuentes:
https://rrbenavi-source.github.io/portfolio/publicaciones/near-real-time-lakehouse
