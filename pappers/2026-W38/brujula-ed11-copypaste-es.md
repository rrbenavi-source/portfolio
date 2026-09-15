# Brújula · Edición 11 — material listo para copiar y pegar

**Publicación: martes 15 de septiembre de 2026, 9:00 AM CDMX.**
Artículo en el portfolio: https://rrbenavi-source.github.io/portfolio/publicaciones/la-aduana

Continúa la línea SAP de las ediciones 08–10, pero cambia el eje: ya no es cómo migrar bien, sino **quién es dueño de la puerta de salida del dato**. Es la primera edición con una fecha límite real encima (fin de 2026), así que el post de lanzamiento debe llevar esa urgencia sin sonar a alarma de vendor.

---

## Checklist

1. Crear la edición nueva en el editor de newsletter de LinkedIn.
2. Pegar **título** y **subtítulo** (abajo).
3. Subir la **portada**: `brujula-cover-11.png` (1920×1080).
4. Pegar el **cuerpo** entre los separadores, respetando la marca `[ Sube la figura: … ]`.
5. Subir la **figura** en su posición, con el **alt text** que viene más abajo.
6. Llenar los campos de **SEO** (título y descripción).
7. Publicar, y de inmediato hacer el **post de lanzamiento** en el feed.
8. Poner el **primer comentario** con los links. LinkedIn penaliza los links externos en el cuerpo del post.

---

## Título

La aduana

## Subtítulo

Salir de SAP del lado analítico ya no es una decisión de plataforma. Es una decisión de contrato: la puerta tiene dueño, tiene medidor y no tiene corte.

## SEO — título

La aduana: lo que cuesta sacar tus datos de SAP hacia Fabric

## SEO — descripción

Desde junio de 2026 un parche de SAP bloquea técnicamente las llamadas ODP-RFC de aplicaciones no-SAP. Quedan cuatro puertas legítimas, un medidor que cobra por gigabyte y no tiene corte, y un inventario que no existe hasta el día que lo instalas.

---

## Alt text de las imágenes

- **Portada:** Portada de la edición 11 del newsletter Brújula, titulada "La aduana", sobre fondo oscuro con acento teal y la aguja del compás.
- **Figura** (`fig-cuatro-puertas.png`): Las cuatro rutas legítimas para sacar datos de un sistema ABAP hacia una plataforma que no es de SAP, con el peaje de cada una. SAP Datasphere con Premium Outbound Integration, que cobra bloques de 20 GB al mes y no corta al excederse; la API OData de ODP, sin costo por gigabyte pero limitada por throughput; un conector certificado de partner con Open Mirroring, que cambia el peaje por una licencia de software; y SAP Business Data Cloud, una suscripción a una plataforma nueva.

---

## CUERPO — copiar de aquí

Un cliente con el que trabajamos tomó una decisión que voy a ver muchas veces en los próximos tres años. Venía de un ECC con reporting en **BW 7.5** —la generación previa del data warehouse de SAP, la que sigue viva en media industria— y se fue a S/4HANA. Hasta ahí, la película conocida.

Lo interesante pasó del otro lado. Cuando llegó el momento de decidir la plataforma analítica, no siguieron el camino de casa. No fueron a BW/4HANA ni a SAC. Se fueron a **Microsoft Fabric** y a un lago de datos. La integración quedó así: **CDS views** en S/4HANA —las vistas que exponen el dato del ERP ya con contexto de negocio, no como tabla cruda—, consumidas por **replication flows de SAP Datasphere**, que las aterrizan listas para Fabric.

Es una arquitectura defendible y me parece bien resuelta. Pero encierra una paradoja que vale la pena decir en voz alta: **para poder salir de la analítica de SAP, tuvieron que comprar un producto de analítica de SAP.**

Eso no es un accidente de este proyecto. Es la forma que tomó el mercado este año, y muy poca gente lo tiene en su business case.

Hasta hace poco, la puerta era gratis

Durante quince años la respuesta a "¿cómo saco mis datos de SAP?" fue prácticamente universal: **ODP** —Operational Data Provisioning, la capa que expone los datos de SAP hacia el mundo analítico— y en particular su interfaz por RFC, **ODP-RFC**. Cualquier herramienta de integración del mercado se conectaba por ahí. Era la puerta de servicio: no estaba en el folleto, pero estaba abierta y todo el mundo la usaba.

SAP la cerró. Y no lo hizo de golpe ni en silencio.

La nota **3255746** —"Unpermitted usage of ODP Data Replication APIs"— se publicó en 2022 diciendo que esas APIs eran de uso interno y no estaban soportadas para terceros. Hoy va en su **versión 12, liberada el 9 de junio de 2026**, y su redacción ya no deja espacio interpretativo: cualquier uso de ODP-RFC por parte del cliente o de aplicaciones de terceros para acceder a sistemas ABAP que contengan PI_BASIS, SAP BW o SAP BW/4HANA, on-premise o en private cloud, **está prohibido**.

Y no se quedó en la política. La misma nota anuncia el mecanismo: una nota de seguridad —la **3748819**, del Patch Day de junio de 2026, con las correcciones de código en la **3635619**— que valida las llamadas entrantes contra los tipos de suscriptor permitidos y **bloquea** las que no lo son.

Hay una válvula de escape, y vale la pena leer sus términos completos. La nota **3731818** entrega un reporte que suspende temporalmente ese bloqueo. SAP lo describe como estrictamente limitado en el tiempo, pensado solo para mitigar interrupciones operativas de corto plazo y aplicable **bajo riesgo del propio cliente**. Y cierra diciendo que la excepción expira a fin de 2026, y que después se restablecen las protecciones "enforced without exception".

Enforced without exception. Eso no es una fecha objetivo. Es una fecha de vencimiento.

Y hay dos líneas más en la 3255746 que un CIO debería leer antes que cualquier diagrama de arquitectura: que **SAP se reserva el derecho de modificar los módulos de ODP-RFC en cualquier momento sin aviso previo**, y que **cualquier incidente derivado de un uso fuera de las guías de SAP es responsabilidad exclusiva del cliente**. La segunda no es una advertencia técnica. Es un traslado de responsabilidad.

La señal de que esto tampoco es folclore de consultoría: **Microsoft lo documenta en su propia guía.** Su conector SAP CDC lleva una advertencia textual que remite a la nota 3255746 "para determinar si es relevante para tu licenciamiento actual de SAP". Y la guía abre, antes de cualquier tema técnico, pidiendo verificar los entitlements de licencia de la organización antes de empezar cualquier extracción. Que el proveedor del destino te recuerde que revises la licencia del origen dice bastante sobre dónde está el riesgo real.

Conviene leer el cambio sin dramatismo: **no es un deprecation técnico, es una decisión de titularidad.** SAP dejó de tratar la extracción como un detalle de infraestructura y empezó a tratarla como un producto. Es legítimo. Pero cambia la naturaleza de la pregunta: "cómo saco mis datos" dejó de ser un tema de ETL y pasó a ser un tema de arquitectura y de contrato.

El inventario que todavía no existe

SAP también entregó la herramienta para saber quién está tocando esa puerta hoy: la nota **3439624**, en su versión 34 liberada el 9 de septiembre de 2026, instala un reporte que clasifica cada llamada en cuatro estados: permitida, no permitida, "poco clara" (reservado a SAP Data Services y HANA Smart Data Integration, que hay que verificar a mano) y sin información.

Tiene dos propiedades que cambian por completo **cuándo** hay que actuar.

La primera: **evalúa las llamadas a partir del momento en que se instala, y no evalúa llamadas históricas.** Tu inventario de uso de ODP-RFC no está esperándote en ningún log. Empieza a existir el día que implementas la nota. Cada semana que se pospone es una semana de ceguera que no se recupera hacia atrás, contra una fecha límite que está en diciembre. Y en un paisaje BW 7.5 eso no es un clic: llega por support package, o sea que tu inventario depende de una ventana de mantenimiento de basis y de su calendario, no del tuyo.

La segunda es una admisión que hay que agradecerle a SAP, porque es justo la que evita un falso positivo de tranquilidad. Textual: "Please note that the above report does not provide conclusive results of the non-existence of unpermitted calls to the ODP-RFC interface."

El reporte puede decirte que **encontró** llamadas no permitidas. No puede decirte que **no las hay**. Un tablero en verde ahí no es evidencia de cumplimiento: es evidencia de que en la ventana observada no apareció nada. Y como ODP-RFC es dependiente de mandante, hay que correrlo en cada cliente relevante de cada sistema, no una vez por paisaje.

Es, otra vez, la forma de fallar de la que hablé en la edición anterior: el sistema no te detiene, te entrega verde.

Cuatro puertas y su peaje

Si hoy tienes que sacar dato de un ABAP —ECC o S/4HANA— hacia una plataforma que no es de SAP, las opciones legítimas se cuentan con los dedos de una mano. Vale la pena verlas juntas, porque la mayoría de los proyectos elige la primera que le presentaron.

[ Sube la figura: fig-cuatro-puertas.png ]

Hay un detalle que se pasa por alto y que sostiene todo el argumento de esta edición: **la nota 3255746 no menciona Datasphere entre las alternativas.** No es un olvido. Datasphere no aparece como alternativa porque no es una alternativa para ti: es una aplicación SAP, y por eso su tráfico está permitido por definición. **La prohibición nunca fue sobre el protocolo. Fue sobre quién está del otro lado del cable.**

Las cuatro puertas son defendibles. Lo que no es defendible es llegar a la cuarta reunión de diseño sin haber escrito **por qué** se eligió una.

El medidor

Aquí es donde el business case se rompe casi siempre, y la mecánica está en la documentación pública de SAP.

Para usar **cualquier destino no-SAP** en un replication flow de Datasphere —Azure Data Lake Storage Gen2, Amazon S3, Google Cloud Storage, BigQuery, Kafka, SFTP— necesitas **Premium Outbound Integration**, y tu administrador tiene que asignar al menos un bloque. La unidad es clara: "Each block gives you 20 GB of data volume for transfer." Un bloque, 20 GB, al mes. Microsoft lo confirma del lado del destino, en su página de mirroring para SAP: el precio de Premium Outbound Integration aplica cuando haces mirroring de datos de SAP vía Datasphere.

Y ahora la línea que a mi juicio debería estar en la primera diapositiva de cualquier plan de migración de este tipo. Es de SAP, textual, sobre qué pasa cuando te pasas del volumen asignado: "If you exceed the assigned volume, your data integration processes (such as replication flow runs) continues running to avoid interrupting critical integration scenarios, which can result in additional costs."

Léela otra vez. **El medidor no tiene corte.** Y está bien diseñado así: cortar la integración de una empresa a mitad de un cierre mensual sería peor. Pero significa que el costo de salida es **recurrente, variable y sin tope técnico**, y que la única protección es organizacional: que alguien esté mirando el consumo.

Hay una consecuencia de segundo orden que casi nadie modela. **Este costo crece con el éxito del proyecto.** Cada nuevo caso de uso en Fabric, cada tabla que alguien pide "por si acaso", cada histórico que se recarga porque cambió una regla, cruza la puerta y se cobra. En BW, servir un reporte más costaba prácticamente cero al margen. En esta arquitectura, no.

Visto de frente, eso no es solo un riesgo: también es un incentivo sano. Es la primera vez en mi carrera que el diseño de extracción tiene un **precio directo y visible**. Extraer lo que se usa, con la granularidad con la que se usa, dejó de ser una buena práctica de ingeniería para convertirse en una línea del presupuesto. Los equipos que ya trabajaban así no van a notar el cambio. Los que extraían tablas completas "para tener todo disponible" lo van a notar en la factura del tercer mes.

Datasphere como aduana, no como warehouse

Este es el reencuadre que quiero dejar, y es el que me parece más útil para quien está diseñando algo parecido.

En esta arquitectura, **Datasphere no es el data warehouse. Es la aduana.** Es la capa de tránsito donde el dato acredita que puede salir, paga su derecho de paso y sigue su camino. No es donde se modela, no es donde se gobierna el significado, no es de donde se reportea. Todo eso vive del otro lado, en Fabric y en el lago.

La primera consecuencia: **una aduana es un sistema en operación, no un componente pasivo.** Tiene monitoreo, tiene ventanas de carga, se cae, tiene dueño. En el papel del diagrama es una flecha; en la realidad es un sistema más que alguien opera de guardia. Si tu organigrama de la nueva plataforma no tiene a nadie sentado ahí, lo vas a descubrir el primer lunes de cierre.

La segunda es más incómoda: **hay que decidir explícitamente que la aduana no va a crecer.** El comportamiento por defecto de cualquier organización que ya compró una herramienta es empezar a usarla. Alguien va a proponer "ya que tenemos Datasphere, modelemos aquí esta dimensión". Y en seis meses tienes dos capas semánticas, cada una a medias, y la conversación de gobierno que creías haber cerrado al elegir Fabric vuelve a abrirse, ahora con dos dueños. La disciplina de mantener la aduana como aduana es una decisión que se escribe, se comunica y se defiende. No se sostiene sola.

El segundo peaje: lo que no viaja

El peaje del que nadie habla no se cobra en gigabytes. Se cobra en meses de gente.

**Un replication flow mueve filas. No mueve significado.** Una parte del significado sí cruza, y por eso la elección de CDS views como punto de extracción es correcta: una CDS view ya trae el contexto de negocio del ERP —los joins, los filtros, las descripciones, la lógica de qué es una orden abierta—. Eso es exactamente lo que no tienes cuando lees tablas crudas.

Pero el otro contexto, el que vivía en BW, no viaja. Veinte años de key figures calculados y restringidos, jerarquías, reglas de consolidación, autorizaciones analíticas. Nada de eso está en la CDS view ni cabe en un archivo Parquet. Alguien lo tiene que volver a escribir del otro lado.

En este caso **las reglas de negocio se rehicieron a mano, y en muchos casos no estaban 100 % documentadas.** Quiero ser preciso con lo que eso significa, porque suena a un problema de documentación y es otra cosa: buena parte de ese trabajo no fue migración, fue **arqueología**. Abrir la query vieja, leer la fórmula, encontrar a quien se acuerde de por qué en 2014 se excluyeron ciertos tipos de documento, y decidir si esa regla sigue siendo correcta o simplemente sigue viva.

Y aquí hay un reloj que casi nadie mira. **BW 7.5 tiene mantenimiento mainstream hasta fin de 2027 y extendido hasta 2030.** Mientras ese sistema siga prendido, las reglas no documentadas todavía se pueden leer: están en las queries, en las transformaciones, en la cabeza de la gente que las mantiene. El día que se apaga, lo que no se documentó deja de ser recuperable. La ventana para hacer esa arqueología con red de seguridad es finita, y se está cerrando en paralelo a la migración, no después.

Qué le pediría a un business case

Cinco cosas concretas. Las tres primeras son para quien firma el contrato, no para quien dirige el equipo técnico.

**Que el egress esté modelado como gasto recurrente y creciente, no como costo de proyecto.** Con la cifra del estimador de capacidad de SAP y, mínimo, tres escenarios: año 1, año 3, y el año en que el 80 % de tus reportes ya vive en la nueva plataforma. La pregunta correcta no es cuántos GB cruzan hoy; es cuántos van a cruzar cuando el proyecto haya tenido éxito.

**Que el medidor tenga alarma y dueño con nombre.** SAP dejó escrito que no corta. Entonces la protección tiene que existir de tu lado: umbral, alerta y una persona que responda por ella.

**Que la elección de puerta esté escrita, con su razón.** Cuál de las cuatro, por qué, y qué pasa si SAP vuelve a mover la línea. Es un anexo de dos párrafos que te ahorra una discusión de seis meses.

**Que el autodiagnóstico de ODP-RFC quede instalado este trimestre, no el próximo.** No lo pidas como tarea de cumplimiento; pídelo porque es la única forma de que el inventario exista: el reporte no ve hacia atrás. Y pídelo con la advertencia puesta —verde ahí significa "no vi nada en la ventana observada", no "no hay nada"—. La válvula temporal vence a fin de 2026 y SAP ya dejó escrito que después se aplica sin excepción. Si tienes integraciones viejas apuntando a esa interfaz, no se van a degradar: se van a detener.

**Que la reconstrucción de reglas de negocio aparezca con nombre, estimación y calendario**, y que se ejecute mientras el sistema origen sigue encendido. No es una tarea de cierre del proyecto. Es la tarea que más depende de que el sistema viejo todavía exista.

Lo digo desde una región donde esto es rutina, no hipótesis. Buena parte de la operación de las multinacionales instaladas en el noreste corre sobre SAP, y muchas de ellas están decidiendo justo ahora dónde va a vivir su analítica. En esas conversaciones, la puerta de salida se trata como un detalle de implementación que se resuelve después de firmar. Es exactamente al revés: **es de las pocas decisiones que se negocian bien una sola vez, al principio, y se pagan todos los meses si se negocian mal.**

El norte

La arquitectura de este cliente me parece correcta. CDS views como contrato de extracción, un solo formato de aterrizaje, un lago abierto del otro lado, y una plataforma analítica que eligieron por sus razones y no por inercia de proveedor. Volvería a firmar ese diseño.

Lo que cambió no es el diseño. Es que **"salimos de SAP del lado analítico" dejó de ser una decisión de plataforma.** Es una decisión sobre quién es dueño de la puerta por la que va a pasar tu dato durante los próximos diez años, cuánto cobra por abrirla, y qué parte del significado se queda de este lado cuando el dato cruza.

Si estás por entrar a esta discusión, hay una sola pregunta que ordena todas las demás, y no es técnica: **¿cuántos gigabytes al mes van a cruzar tu aduana el año en que el proyecto ya haya funcionado?** Si nadie en la sala puede responderla, todavía no tienes un business case. Tienes una preferencia de herramienta.

## CUERPO — copiar hasta aquí

---

## POST DE LANZAMIENTO (feed) — copiar de aquí

Un cliente decidió salir de SAP del lado analítico. Se fue a Fabric y a un lago de datos.

Para poder salir, tuvo que comprar un producto de analítica de SAP.

No es una contradicción del proyecto. Es la forma que tomó el mercado este año, y la mayoría de los business cases todavía no la refleja.

Durante quince años, sacar datos de SAP se hacía por ODP-RFC. Era la puerta de servicio: no estaba en el folleto, pero estaba abierta y todo el mundo la usaba.

Desde junio de 2026 esa puerta se cierra sola. Un parche de seguridad valida cada llamada entrante y bloquea las que no vienen de una aplicación SAP. Hay una excepción temporal, y SAP ya escribió que vence a fin de año y que después se aplica "enforced without exception".

Eso mueve la pregunta de lugar. "¿Cómo saco mis datos de SAP?" dejó de ser un tema de ETL y pasó a ser uno de arquitectura y de contrato.

Tres cosas que me parece que hay que poner sobre la mesa antes de firmar:

Quedan cuatro puertas legítimas, y cada una cobra distinto. Dos de ellas cobran todos los meses.

La que eligió este cliente cobra por gigabyte de salida, en bloques de 20 GB al mes. Y SAP dejó documentado que al excederse la integración no se detiene: sigue corriendo, con costo adicional. El medidor no tiene corte, y ese costo crece con el éxito del proyecto.

El inventario de quién usa hoy esa interfaz no existe todavía. La herramienta de autodiagnóstico de SAP solo evalúa llamadas a partir del día que la instalas: no ve hacia atrás. Y admite, textualmente, que no puede probar la ausencia de llamadas no permitidas. Verde ahí no significa que estés limpio; significa que en la ventana observada no apareció nada.

Hay un segundo peaje que no se cobra en gigabytes sino en meses de gente: un replication flow mueve filas, no mueve significado. Veinte años de reglas de negocio de BW no viajan en el pipe. En este caso se rehicieron a mano, y en muchos casos no estaban documentadas del todo. Eso no fue migración, fue arqueología. Y solo se puede hacer mientras el sistema viejo siga prendido.

La edición de esta semana desarrolla las cuatro puertas, el medidor y lo que le pediría a un business case. Link en el primer comentario.

#SAP #S4HANA #MicrosoftFabric #SAPDatasphere #DataEngineering #ArquitecturaDeDatos

---

## PRIMER COMENTARIO (poner de inmediato)

Edición 11 completa, con la figura de las cuatro puertas y su peaje:
https://rrbenavi-source.github.io/portfolio/publicaciones/la-aduana

Y la edición anterior, que trata la otra cara del mismo proyecto —cómo validar que el dato llegó completo cuando el sistema ya no te avisa:
https://rrbenavi-source.github.io/portfolio/publicaciones/validar-migracion-extractores-s4hana

---

## VERSIÓN CORTA (para repostear en unos días)

Datasphere no es tu data warehouse. Es tu aduana.

Es la capa de tránsito donde el dato acredita que puede salir, paga su derecho de paso y sigue su camino. No es donde modelas, no es donde gobiernas el significado, no es de donde reporteas.

Dos consecuencias que casi nadie escribe en el diagrama.

Una aduana es un sistema en operación, no una flecha: tiene monitoreo, ventanas de carga, se cae y necesita dueño. Si tu organigrama no tiene a nadie sentado ahí, lo vas a descubrir el primer lunes de cierre.

Y hay que decidir explícitamente que no va a crecer. El comportamiento por defecto de cualquier organización que ya compró una herramienta es empezar a usarla. En seis meses tienes dos capas semánticas a medias y la conversación de gobierno que creías cerrada, ahora con dos dueños.

Mantener la aduana como aduana es una decisión que se escribe, se comunica y se defiende. No se sostiene sola.
