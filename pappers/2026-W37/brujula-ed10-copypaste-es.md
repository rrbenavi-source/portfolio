# Brújula · Edición 10 — material listo para copiar y pegar

**Publicación: martes 8 de septiembre de 2026, 9:00 AM CDMX.**
Artículo en el portfolio: https://rrbenavi-source.github.io/portfolio/publicaciones/validar-migracion-extractores-s4hana

Cambia de tema respecto a las ediciones 08 y 09 (BW → Business Data Cloud). Esta vuelve a la migración de extractores ECC → S/4HANA y retoma explícitamente la edición 02 ("El diseño es la migración"), así que conviene enlazar esa en el primer comentario.

---

## Checklist

1. Crear la edición nueva en el editor de newsletter de LinkedIn.
2. Pegar **título** y **subtítulo** (abajo).
3. Subir la **portada**: `brujula-cover-10.png` (1920×1080).
4. Pegar el **cuerpo** entre los separadores, respetando la marca `[ Sube la figura: … ]`.
5. Subir la figura en su posición, con el **alt text** que viene más abajo.
6. Llenar los campos de **SEO** (título y descripción).
7. Publicar, y de inmediato hacer el **post de lanzamiento** en el feed.
8. Poner el **primer comentario** con los dos links. LinkedIn penaliza los links externos en el cuerpo del post.

---

## Título

Cómo validar una migración de extractores a S/4HANA

## Subtítulo

La carga corrió sin errores y trajo menos filas. Cuatro cosas que le pediría a un plan de trabajo —y dos a un contrato.

## SEO — título

Cómo validar una migración de extractores a S/4HANA: por qué el verde ya no basta

## SEO — descripción

Migrar extractores clásicos a CDS views mueve el riesgo de la lógica al metadato. Un error de metadato casi nunca aborta: entrega un dataset con la forma correcta y menos filas. Dos fallas silenciosas, un alcance que ninguna especificación contemplaba, y qué exigirle a un plan de trabajo.

---

## Alt text de las imágenes

- **Portada:** Portada de la edición 10 del newsletter Brújula, titulada "Cómo validar una migración de extractores a S/4HANA", sobre fondo oscuro con acento teal.
- **Figura 1** (`fig-cinco-seis.png`): Mapeo de los cinco segmentos del DataSource de una jerarquía de centro de coste hacia los seis grupos de la transformación en el destino. Cabecera, textos de cabecera, nodos, textos de nodo e intervalos encuentran su grupo; el sexto grupo, textos por nivel de jerarquía, se queda sin segmento de origen.

---

## CUERPO — copiar de aquí

Hace unas ediciones cerré un papper sobre migración de extractores con una práctica que me parecía obvia: *un extractor no está terminado cuando corre, está terminado cuando el dato cuadra contra el origen*. Fácil de escribir.

Estas semanas me tocó cumplirla. Estamos en construcción y validación de datos en desarrollo, migrando los extractores clásicos de un ECC hacia CDS views en S/4HANA, y la primera carga que puse a cuadrar **salió en verde**. Sin errores, sin registros rechazados, sin advertencias. Y con menos filas de las que había en el origen.

No fue un caso aislado. Terminó siendo la forma característica de fallar de esta arquitectura, y me obligó a revisar algo más incómodo que un mapeo: **el criterio con el que damos por buena una carga**. Esta edición es lo que encontramos, y por qué creo que cambia lo que hay que escribir en un plan de trabajo —y, si firmas el presupuesto, en un contrato.

Un modelo declarativo falla distinto

En ECC, un extractor era esencialmente un programa. Código que sabía qué tablas leer, en qué orden y con qué lógica. Cuando un programa se equivoca, normalmente se nota: aborta, deja un log, alguien lo ve en rojo.

En S/4HANA, el extractor es una **CDS view con anotaciones**. Las anotaciones son declaraciones —empiezan con @— y no son documentación: son instrucciones. Le dicen al framework de aprovisionamiento —**ODP**, la capa que expone los datos de SAP hacia el mundo analítico— qué clase de dato estás publicando, y el sistema destino construye su parte a partir de esa declaración.

Para que una vista sea extraíble hacen falta **dos declaraciones, no una**. La primera es el interruptor: @Analytics.dataExtraction.enabled. Sin ella la vista existe, se consulta y se reportea perfectamente, pero es invisible para la extracción. La segunda es la familia del dato, y ahí aparece la primera rareza: **las cuatro familias no viven en la misma anotación**. Datos maestros y transaccionales se declaran con @Analytics.dataCategory; textos y jerarquías, con @ObjectModel.dataCategory. Buscar "la anotación de categoría" te entrega la mitad del mapa y ninguna señal de que falta la otra mitad.

Que el contenedor destino se derive de ahí no es una metáfora. El objeto que se publica lleva el nombre técnico de la vista más un sufijo que sale de esa declaración: $P para atributos de datos maestros, $T para textos, $H para jerarquías, $F para transaccionales. **El tipo de lo que nace del otro lado está literalmente en el nombre**, y no se elige después.

Cuando la llave es compuesta

Y todo eso es cuando la llave es un solo campo. Los atributos de centro de coste, que es el objeto con el que trabajamos, no tienen una llave: tienen tres —sociedad de controlling, centro de coste y fecha de validez—, y una llave compuesta multiplica lo que hay que declarar. La regla es que **exactamente un campo de la llave es el representativo**, el que "es" la entidad, y se marca con @ObjectModel.representativeKey. En el ejemplo que usa SAP: una dimensión de ciudad con llave país + ciudad tiene como representativo la ciudad, no el país. Para centro de coste el representativo es el centro de coste; la sociedad de controlling es el prefijo que lo hace único.

Esa anotación parece de modelado analítico y no lo es: **sin ella el framework no publica la vista** —se queja de que no encuentra un campo representativo— y no hay extracción. Además apunta al **alias** del campo, no a su nombre de origen: si lo renombraste en la proyección, la anotación tiene que apuntar al nombre nuevo o no resuelve. De ahí salen tres obligaciones más, y ninguna es cosmética:

**Todos los demás campos de la llave necesitan una asociación** a su propia vista de datos maestros. La sociedad de controlling no puede ir suelta.

**La fecha de validez es la excepción, y trae dos reglas.** El campo "válido hasta" tiene que ser parte de la llave y llevar la semántica de fecha final; el "válido desde" va fuera de la llave. Y el "válido hasta" **no puede** tener asociación ni aparecer en la condición de ninguna otra.

**El texto se asocia al campo representativo**, no a la llave completa —aunque la condición de la asociación sí tenga que incluir todos los campos de la llave, y la vista de textos tenga que tener exactamente la misma llave.

El destino hereda esa forma: una llave compuesta en el origen se vuelve un **objeto compuesto** del otro lado —el centro de coste colgando de la sociedad de controlling— y qué cuelga de qué lo decide el campo que declaraste representativo. Si esa derivación no se puede resolver, al menos avisa: cuando otra vista intenta asociarse, la activación falla con RSODP056, *no se puede derivar el nombre del InfoObject*. Es de las pocas veces en toda esta fase en que el sistema nos detuvo.

Visto de lejos todo esto suena a simplificación. Menos código, menos superficie de error. Pero el riesgo no desapareció: **se movió de la lógica al metadato**. Y un error de metadato casi nunca produce un aborto. Produce una extracción que corre, que entrega un dataset con la forma correcta, y que está incompleto.

Es una diferencia de naturaleza, no de grado. **Un programa mal escrito falla ruidosamente. Una declaración mal puesta te entrega menos, en verde.**

El campo que nadie estaba mirando

El caso que mejor lo enseña es también el más tonto, que es justo lo que lo hace peligroso.

Volvamos a ese extractor de atributos de centro de coste. La vista traía, entre setenta y tantos campos, **el campo de idioma**. Un atributo más, sin relevancia analítica; nadie lo reportea. Nadie lo estaba mirando.

El sistema destino asigna la marca de *campo de idioma* a cualquier columna cuyo tipo de dato sea LANG. Por el tipo, no por lo que uno declare —lo comprobamos por eliminación: apagar la anotación semántica no cambió nada, y leer el campo de la tabla en vez de la vista estándar tampoco—. Y con esa marca, el proceso de carga asume que el dato es multiidioma y **añade un filtro por su cuenta**: pide únicamente los idiomas instalados en el sistema destino y descarta todo lo demás. Sin error, sin advertencia, sin línea en el log.

Vale la pena ver dónde acabó viviendo el criterio. Cuántas filas llegan no lo decide el extractor, ni la vista, ni la especificación funcional: lo decide **una lista de idiomas configurada en otro sistema**, que nadie del lado del origen tiene motivo para abrir.

Está documentado por SAP en el KBA **3219389**. Casi no lo encontramos: el título habla de un *text datasource*, así que uno lo descarta cuando el problema está en una vista de atributos. La causa real no tiene nada que ver con textos —es el tipo del campo— pero el título te manda a otro lado.

Y entonces vino la parte que sí es una decisión de arquitectura. **SAP documenta la solución únicamente del lado del destino**: cambiar a mano esa marca del campo. Funciona. El problema es que ese metadato se regenera cada vez que se replica el origen, así que la corrección se borra sola. Es un paso manual perpetuo, que sobrevive mientras la persona que lo conoce esté en el proyecto, y que alguien va a olvidar en producción exactamente el día que importa.

Preferimos resolverlo en el origen. La línea que funcionó rompe el tipo con una función de texto y lo vuelve a fijar como carácter simple, y además **renombra el campo**: si el tipo ya está corregido pero el nombre sigue siendo el estándar, el destino lo vuelve a detectar por el nombre. Son dos mecanismos distintos y hay que desactivar los dos. El mapeo del campo renombrado vive en la transformación, que es un objeto propio, se transporta y sobrevive a las replicaciones.

Eso es lo que cambió: no eliminamos el trabajo manual, lo **mudamos de un lugar que se borra a uno que persiste**. El precio es que el nombre técnico deja de coincidir con el del extractor original y hay que dejarlo escrito en la matriz de mapeo. Me parece un intercambio barato.

El permiso que devuelve menos datos

El segundo hallazgo tiene forma distinta y el mismo desenlace.

Las vistas estándar de SAP llevan controles de acceso propios, escritos en un lenguaje aparte —**DCL**, el dialecto con el que se declaran autorizaciones sobre una vista— y embebidos en el modelo. Cuando la vista los activa, el sistema no rechaza la consulta: **recorta el resultado** a lo que ese usuario tiene derecho a ver. Los perfiles de autorización estándar para la extracción no los cubren: habilitan el mecanismo, no el contenido.

Si al usuario técnico de la conexión le faltan las autorizaciones **de negocio** —una sociedad de controlling, un plan de cuentas— la extracción no se cae. Devuelve menos filas. O cero.

Piensa en lo que eso significa en una prueba integral. El equipo técnico ejecuta la carga, sale en verde, se marca la actividad como cerrada. El usuario funcional abre el reporte semanas después y ve una cifra menor. **Nadie tiene motivo para sospechar del permiso, porque el permiso nunca dijo que no.**

Lo que las dos fallas tienen en común

Un campo de idioma que nadie reportea y una autorización de negocio. No se parecen en nada, excepto en lo único que importa: **ninguna de las dos produjo un error**. Las dos entregaron un resultado plausible.

De ahí sale la tesis de esta edición, y es incómoda porque cuestiona un hábito que traíamos funcionando bien: **"la carga corrió sin error" dejó de ser evidencia de nada.** Era una señal razonable cuando el extractor era un programa. En un modelo declarativo, es apenas la confirmación de que el mecanismo se ejecutó.

La evidencia ahora es cuantitativa. Conteo de filas contra el origen, carga completa, sin filtros y sin *delta* —sin carga incremental, trayendo todo—, antes de comparar un solo valor. SAP tiene su propia herramienta de validación de transición de datos precisamente porque la reconciliación contra el origen es la prueba, no un paso opcional de aseguramiento.

Hasta la herramienta con la que uno prueba cambió, y de una forma que vale la pena contar. El chequeador de extractores clásico —RSA3, el primer reflejo de cualquiera que venga de ECC— no funciona con vistas CDS. Hay que usar otro reporte, RODPS_REPL_TEST, y ese reporte trae su propia trampa: **no simula**. Inicializar o correr un delta desde ahí abre una suscripción real en la cola de datos, que después alguien tiene que ir a limpiar. La herramienta de diagnóstico modifica el estado que estás diagnosticando, y tampoco lo anuncia.

Hay un corolario de secuencia que aprendimos por las malas y que vale más que muchas metodologías: **el delta va al final.** Activar la carga incremental antes de haber cuadrado la carga completa introduce diferencias de ventana temporal que se confunden con errores de mapeo, y se pierden días persiguiendo un defecto que no existe. Primero se demuestra que el dato es correcto; después se optimiza cómo llega.

El alcance que no estaba en ninguna especificación

Y aquí aparece el segundo tipo de sorpresa de la fase de construcción, que ya no es de calidad sino de alcance.

Las jerarquías —centros de coste, plan de cuentas— resultaron el objeto más caro y el que peor se había estimado. Tres razones.

La primera es que una jerarquía no es una tabla plana: declararla como jerarquía hace que el objeto nazca **con segmentos**. Cinco, en nuestro caso —cabecera, textos de cabecera, nodos, textos de nodo e intervalos—, y ese formato se deriva de la anotación. Declarar la familia equivocada no produce un error: produce el contenedor equivocado, que hay que borrar y rehacer. Ni siquiera viene todo de la misma vista: los textos de los nodos no los entrega la vista de jerarquía sino otra distinta, así que una sola jerarquía de centro de coste ya necesita **tres vistas en el origen**.

[ Sube la figura: fig-cinco-seis.png — "Cinco entran, seis esperan" ]

La segunda es que existen **dos sintaxis de jerarquías en CDS** y la que aparece primero en cualquier búsqueda es la equivocada. La nueva —una entidad propia, declarada con DEFINE HIERARCHY— sirve para consumo analítico y **no** para extracción; la vía de extracción sigue siendo la anotación @ObjectModel.dataCategory: #HIERARCHY. Lo verificamos de la forma dura: las **244 páginas** de la guía oficial de SAP sobre modelos de datos ABAP no mencionan ni una sola vez la extracción hacia el mundo analítico —ni la anotación que la habilita, ni el framework—. Es información correcta aplicada al escenario equivocado, que es la clase de error más difícil de detectar porque todo lo que lees es cierto.

La tercera es la que cambia el plan, y es consecuencia directa de la primera. Como los textos de nodo llegan por separado, para migrar esas jerarquías por la vía que SAP recomienda **hay que modificar objetos en el sistema destino**: agregarle al centro de coste dos características que hoy no existen —una para el identificador de la jerarquía y otra para el texto del nodo, compuesta a la anterior—, con longitudes fijas y mapeadas segmento por segmento. Eso no es parametrizar: **es modelar**. Lo verificamos contra el sistema: en dos de las tres jerarquías del alcance, esa configuración está literalmente vacía.

Ninguna de las especificaciones funcionales lo mencionaba. Y no por descuido: **están escritas desde el lado del origen**. Describen con precisión qué dato hay que sacar de S/4HANA, porque ahí es donde está la novedad y donde se concentró el análisis. El destino se da por sentado, porque "ya existe y ya funciona".

Ese supuesto es el que hay que romper. En una migración de este tipo, **el sistema que no estás migrando también tiene trabajo**, y ese trabajo no aparece en ningún documento hasta que alguien intenta cargar el primer árbol.

Qué le pediría a un plan de trabajo

Cuatro cosas concretas, y las dos últimas son para quien firma el alcance y el presupuesto, no para quien dirige el equipo.

**Que la definición de "terminado" sea un número, no un color.** Conteo contra el origen, carga completa, sin delta. Si la actividad se puede cerrar con una captura de pantalla en verde, el criterio está mal escrito.

**Que el delta esté planeado como una fase posterior**, no como parte de la construcción. Es una decisión de secuencia que ahorra semanas de diagnóstico falso.

**Que el alcance cubra explícitamente el sistema destino.** Si tus especificaciones sólo describen el origen, tienes un alcance a medias y una contingencia calculada sobre la mitad del trabajo. Vale la pena preguntar, antes de firmar: *¿qué hay que modificar del otro lado?*

**Que la prueba de autorizaciones sea de negocio, no técnica.** Que el usuario de conexión se pueda conectar no prueba nada sobre qué datos alcanza a ver. Esto se pide por escrito y se mide con un conteo.

El norte

Lo digo desde una región donde esto no es hipotético. Buena parte de las operaciones de las multinacionales instaladas en el noreste corre sobre plataformas SAP que están, o van a estar, en esta misma transición. La conversación sobre cómo se prueba una migración no es un detalle de implementación: es la diferencia entre descubrir un faltante en desarrollo o descubrirlo en un cierre.

La edición 02 de este newsletter defendía que el diseño es la migración. Lo sigo sosteniendo. Pero la fase de construcción me enseñó algo que el diseño no puede resolver solo: **incluso con la especificación correcta, la forma de comprobar que el dato llegó completo tuvo que cambiar.**

Migrar a un modelo declarativo no eliminó el riesgo: **lo dejó sin síntoma**. Y un riesgo sin síntoma es el argumento para hacer la validación más estricta, no más ligera. Menos código no significa menos pruebas. Significa otras pruebas: menos revisar lógica y más contar filas.

Si estás por entrar a esta fase, el cambio más barato que puedes hacer hoy no cuesta ni una línea de código. Es reescribir el criterio de aceptación de tus actividades de carga para que exija un número. Todo lo demás de esta edición lo descubrimos porque ese número no cuadraba.

---

## POST DE LANZAMIENTO (feed) — copiar de aquí

La primera carga que puse a cuadrar salió en verde. Sin errores, sin registros rechazados, sin advertencias.

Y con menos filas de las que había en el origen.

Estamos migrando extractores clásicos de ECC hacia CDS views en S/4HANA. En ECC, un extractor era un programa: cuando se equivocaba, abortaba. En S/4HANA es una vista con anotaciones, y ahí el riesgo se mudó de la lógica al metadato.

Un error de metadato casi nunca aborta. Entrega un dataset con la forma correcta y menos filas.

Dos ejemplos de esta semana:

Un campo de idioma que nadie reportea. El destino lo marca por su tipo de dato, y con esa marca el proceso de carga pide únicamente los idiomas instalados en el sistema destino y descarta el resto. Cuántas filas llegan lo acabó decidiendo una lista configurada en otro sistema, que nadie del lado del origen tiene motivo para abrir.

Una autorización de negocio faltante en el usuario técnico. No tumba la conexión: recorta el resultado. Sale verde, y semanas después alguien abre el reporte y ve una cifra menor.

Ninguna de las dos produjo un error. Las dos entregaron un resultado plausible.

De ahí la tesis de la edición 10: "la carga corrió sin error" dejó de ser evidencia de nada. Era una señal razonable cuando el extractor era un programa. En un modelo declarativo es apenas la confirmación de que el mecanismo se ejecutó.

El cambio más barato que puedes hacer hoy no cuesta una línea de código: reescribir el criterio de aceptación de tus actividades de carga para que exija un número, no un color.

Escribí las cuatro cosas que le pediría a un plan de trabajo —y las dos que le pediría a un contrato— en la edición de esta semana. Link en el primer comentario.

#SAP #S4HANA #BW4HANA #DataEngineering #Migracion #ArquitecturaDeDatos

---

## PRIMER COMENTARIO (poner de inmediato)

Edición 10 completa, con la figura de los cinco segmentos que llegan a seis casillas:
https://rrbenavi-source.github.io/portfolio/publicaciones/validar-migracion-extractores-s4hana

Y la edición 02, que es la que esta retoma —"El diseño es la migración":
https://rrbenavi-source.github.io/portfolio/publicaciones/diseno-es-la-migracion

---

## VERSIÓN CORTA (para repostear en unos días)

Migrar extractores a un modelo declarativo no elimina el riesgo. Lo deja sin síntoma.

Un programa mal escrito falla ruidosamente. Una declaración mal puesta te entrega menos, en verde.

Por eso "corrió sin errores" dejó de ser un criterio de aceptación válido, y por eso el único que sigue funcionando es un número: conteo de filas contra el origen, carga completa, sin delta, antes de comparar un solo valor.

Menos código no significa menos pruebas. Significa otras pruebas: menos revisar lógica y más contar filas.
