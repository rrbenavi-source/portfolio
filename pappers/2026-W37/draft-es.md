# Cómo validar una migración de extractores a S/4HANA

## Lo que la fase de construcción reveló en una migración ECC → S/4HANA: fallas que no producen error y alcance que no estaba en ninguna especificación

Hace unas ediciones cerré un papper sobre migración de extractores con una práctica que me
parecía obvia: *un extractor no está terminado cuando corre, está terminado cuando el dato
cuadra contra el origen*. Fácil de escribir.

Estas semanas me tocó cumplirla. Estamos en construcción y validación de datos en desarrollo,
migrando los extractores clásicos de un ECC hacia CDS views en S/4HANA, y la primera carga que
puse a cuadrar salió en verde. Sin errores, sin registros rechazados, sin advertencias. Y con
menos filas de las que había en el origen.

No fue un caso aislado. Terminó siendo la forma característica de fallar de esta arquitectura, y
me obligó a revisar algo más incómodo que un mapeo: **el criterio con el que damos por buena una
carga**. Esta edición es lo que encontramos, y por qué creo que cambia lo que hay que escribir en
un plan de trabajo —y, si firmas el presupuesto, en un contrato.

## Un modelo declarativo falla distinto

En ECC, un extractor era esencialmente un programa. Código que sabía qué tablas leer, en qué
orden y con qué lógica. Cuando un programa se equivoca, normalmente se nota: aborta, deja un log,
alguien lo ve en rojo.

En S/4HANA, el extractor es una CDS view con anotaciones. Las anotaciones son declaraciones
—empiezan con `@`— y no son documentación: son instrucciones. Le dicen al framework de
aprovisionamiento —ODP, la capa que expone los datos de SAP hacia el mundo analítico— qué clase de
dato estás publicando, y el sistema destino construye su parte a partir de esa declaración.

Para que una vista sea extraíble hacen falta dos declaraciones, no una. La primera es el
interruptor: `@Analytics.dataExtraction.enabled`. Sin ella la vista existe, se consulta y se
reportea perfectamente, pero es invisible para la extracción. La segunda es la familia del dato, y
ahí aparece la primera rareza: **las cuatro familias no viven en la misma anotación.** Datos
maestros y transaccionales se declaran con `@Analytics.dataCategory`; textos y jerarquías, con
`@ObjectModel.dataCategory`. Buscar "la anotación de categoría" te entrega la mitad del mapa y
ninguna señal de que falta la otra mitad.

Que el contenedor destino se derive de ahí no es una metáfora. El objeto que se publica lleva el
nombre técnico de la vista más un sufijo que sale de esa declaración: `$P` para atributos de datos
maestros, `$T` para textos, `$H` para jerarquías, `$F` para transaccionales. El tipo de lo que
nace del otro lado está literalmente en el nombre, y no se elige después.

Y todo eso es cuando la llave es un solo campo. Los atributos de centro de coste, que es el objeto
con el que trabajamos, no tienen una llave: tienen tres —sociedad de controlling, centro de coste y fecha
de validez—, y una llave compuesta multiplica lo que hay que declarar. La regla es que
**exactamente un campo de la llave es el representativo**, el que "es" la entidad, y se marca con
`@ObjectModel.representativeKey`. En el ejemplo que usa SAP: una dimensión de ciudad con llave país
+ ciudad tiene como representativo la ciudad, no el país. Para centro de coste el representativo es
el centro de coste; la sociedad de controlling es el prefijo que lo hace único.

Esa anotación parece de modelado analítico y no lo es: sin ella el framework no publica la vista
—se queja de que no encuentra un campo representativo— y no hay extracción. Además apunta al
**alias** del campo, no a su nombre de origen: si lo renombraste en la proyección, la anotación
tiene que apuntar al nombre nuevo o no resuelve. De ahí salen tres obligaciones más, y ninguna es
cosmética:

- **Todos los demás campos de la llave necesitan una asociación** a su propia vista de datos
  maestros. La sociedad de controlling no puede ir suelta.
- **La fecha de validez es la excepción, y trae dos reglas.** El campo "válido hasta" tiene que ser
  parte de la llave y llevar la semántica de fecha final; el "válido desde" va fuera de la llave. Y
  el "válido hasta" **no puede** tener asociación ni aparecer en la condición de ninguna otra.
- **El texto se asocia al campo representativo**, no a la llave completa —aunque la condición de la
  asociación sí tenga que incluir todos los campos de la llave, y la vista de textos tenga que
  tener exactamente la misma llave.

El destino hereda esa forma: una llave compuesta en el origen se vuelve un objeto compuesto del
otro lado —el centro de coste colgando de la sociedad de controlling— y qué cuelga de qué lo decide
el campo que declaraste representativo. Si esa derivación no se puede resolver, al menos avisa:
cuando otra vista intenta asociarse, la activación falla con `RSODP056`, *no se puede derivar el
nombre del InfoObject*. Es de las pocas veces en toda esta fase en que el sistema nos detuvo.

Visto de lejos todo esto suena a simplificación. Menos código, menos superficie de error. Pero el
riesgo no desapareció: **se movió de la lógica al metadato**. Y un error de metadato casi nunca
produce un aborto. Produce una extracción que corre, que entrega un dataset con la forma correcta,
y que está incompleto.

Es una diferencia de naturaleza, no de grado. Un programa mal escrito falla ruidosamente. Una
declaración mal puesta te entrega menos, en verde.

## El campo que nadie estaba mirando

El caso que mejor lo enseña es también el más tonto, que es justo lo que lo hace peligroso.

Volvamos a ese extractor de atributos de centro de coste. La vista traía, entre setenta y tantos
campos, el campo de idioma. Un atributo más, sin relevancia analítica; nadie lo reportea.
Nadie lo estaba mirando.

El sistema destino asigna la marca de *campo de idioma* a cualquier columna cuyo tipo de dato sea
`LANG`. Por el tipo, no por lo que uno declare —lo comprobamos por eliminación: apagar la anotación
semántica no cambió nada, y leer el campo de la tabla en vez de la vista estándar tampoco—. Y con
esa marca, el proceso de carga asume que el dato es multiidioma y **añade un filtro por su
cuenta**: pide únicamente los idiomas instalados en el sistema destino y descarta todo lo demás.
Sin error, sin advertencia, sin línea en el log.

Vale la pena ver dónde acabó viviendo el criterio. Cuántas filas llegan no lo decide el extractor,
ni la vista, ni la especificación funcional: lo decide una lista de idiomas configurada en **otro
sistema**, que nadie del lado del origen tiene motivo para abrir.

Está documentado por SAP en el KBA 3219389. Casi no lo encontramos: el título habla de un
*text datasource*, así que uno lo descarta cuando el problema está en una vista de atributos. La
causa real no tiene nada que ver con textos —es el tipo del campo— pero el título te manda a otro
lado.

Y entonces vino la parte que sí es una decisión de arquitectura. **SAP documenta la solución
únicamente del lado del destino**: cambiar a mano esa marca del campo. Funciona. El problema es
que ese metadato se regenera cada vez que se replica el origen, así que la corrección se borra
sola. Es un paso manual perpetuo, que sobrevive mientras la persona que lo conoce esté en el
proyecto, y que alguien va a olvidar en producción exactamente el día que importa.

Preferimos resolverlo en el origen. La línea que funcionó rompe el tipo con una función de texto y
lo vuelve a fijar como carácter simple, y además renombra el campo: si el tipo ya está corregido
pero el nombre sigue siendo el estándar, el destino lo vuelve a detectar por el nombre. Son dos
mecanismos distintos y hay que desactivar los dos.

El mapeo del campo renombrado vive en la transformación, que es un objeto propio, se transporta y
sobrevive a las replicaciones.

Eso es lo que cambió: no eliminamos el trabajo manual, lo **mudamos de un lugar que se borra a uno
que persiste**. El precio es que el nombre técnico deja de coincidir con el del extractor original
y hay que dejarlo escrito en la matriz de mapeo. Me parece un intercambio barato.

```abap
@AbapCatalog.sqlViewName: 'ZVCOSTCENTER'
@EndUserText.label: 'BW 0COSTCENTER_ATTR — atributos de centro de coste'

// Las dos declaraciones que hacen extraíble la vista
@Analytics.dataCategory: #DIMENSION
@Analytics.dataExtraction.enabled: true

// Apunta al alias del campo, no a su nombre de origen
@ObjectModel.representativeKey: 'KOSTL'

define view ZI_CostCenter_Attr_BW
  as select from I_CostCenter as _CC
    left outer to one join CSKS as _Z
      on  _CC.ControllingArea = _Z.KOKRS
      and _CC.CostCenter      = _Z.KOSTL
      and _CC.ValidityEndDate = _Z.DATBI
{
  // Llave compuesta: sociedad CO + centro de coste + validez
  key _CC.ControllingArea    as KOKRS,
  key _CC.CostCenter         as KOSTL,

  // El «válido hasta» va dentro de la llave; el «válido desde», fuera
  @Semantics.businessDate.to: true
  key _CC.ValidityEndDate    as DATETO,

  @Semantics.businessDate.from: true
      _CC.ValidityStartDate  as DATEFROM,

  // ... setenta y tantos atributos: organización, dirección, bloqueos ...

  // El campo de idioma: se rompe el tipo LANG y se renombra (KBA 3219389)
      cast( left( _Z.SPRAS, 1 ) as abap.char( 1 ) ) as ZZSPRAS
}
```

**Fig. 1 — El extractor de atributos de centro de coste**, recortado a las líneas que deciden el
resultado: las dos declaraciones que lo hacen extraíble, la llave compuesta con su campo
representativo y el corte del campo de idioma. Nombres y estructura son ilustrativos.

## El permiso que devuelve menos datos

El segundo hallazgo tiene forma distinta y el mismo desenlace.

Las vistas estándar de SAP llevan controles de acceso propios, escritos en un lenguaje aparte
—DCL, el dialecto con el que se declaran autorizaciones sobre una vista— y embebidos en el modelo.
Cuando la vista los activa, el sistema no rechaza la consulta: **recorta el resultado** a lo que
ese usuario tiene derecho a ver. Los perfiles de autorización estándar para la extracción no los
cubren: habilitan el mecanismo, no el contenido.

Si al usuario técnico de la conexión le faltan las autorizaciones **de negocio** —una sociedad de
controlling, un plan de cuentas— la extracción no se cae. Devuelve menos filas. O cero.

Piensa en lo que eso significa en una prueba integral. El equipo técnico ejecuta la carga, sale en
verde, se marca la actividad como cerrada. El usuario funcional abre el reporte semanas después y
ve una cifra menor. Nadie tiene motivo para sospechar del permiso, porque el permiso nunca dijo
que no.

## Lo que las dos fallas tienen en común

Un campo de idioma que nadie reportea y una autorización de negocio. No se parecen en nada,
excepto en lo único que importa: **ninguna de las dos produjo un error**. Las dos entregaron un
resultado plausible.

De ahí sale la tesis de esta edición, y es incómoda porque cuestiona un hábito que traíamos
funcionando bien: **"la carga corrió sin error" dejó de ser evidencia de nada.** Era una señal
razonable cuando el extractor era un programa. En un modelo declarativo, es apenas la confirmación
de que el mecanismo se ejecutó.

La evidencia ahora es cuantitativa. Conteo de filas contra el origen, carga completa, sin filtros y
sin *delta* —sin carga incremental, trayendo todo—, antes de comparar un solo valor. SAP tiene su
propia herramienta de validación de transición de datos precisamente porque la reconciliación
contra el origen es la prueba, no un paso opcional de aseguramiento.

Hasta la herramienta con la que uno prueba cambió, y de una forma que vale la pena contar. El
chequeador de extractores clásico —`RSA3`, el primer reflejo de cualquiera que venga de ECC— no
funciona con vistas CDS. Hay que usar otro reporte, `RODPS_REPL_TEST`, y ese reporte trae su propia
trampa: no simula. Inicializar o correr un delta desde ahí abre una suscripción real en la cola de
datos, que después alguien tiene que ir a limpiar. La herramienta de diagnóstico modifica el estado
que estás diagnosticando, y tampoco lo anuncia.

Hay un corolario de secuencia que aprendimos por las malas y que vale más que muchas
metodologías: **el delta va al final.** Activar la carga incremental antes de haber cuadrado la
carga completa introduce diferencias de ventana temporal que se confunden con errores de mapeo, y
se pierden días persiguiendo un defecto que no existe. Primero se demuestra que el dato es
correcto; después se optimiza cómo llega.

## El alcance que no estaba en ninguna especificación

Y aquí aparece el segundo tipo de sorpresa de la fase de construcción, que ya no es de calidad
sino de alcance.

Las jerarquías —centros de coste, plan de cuentas— resultaron el objeto más caro y el que peor se
había estimado. Tres razones.

La primera es que una jerarquía no es una tabla plana: declararla como jerarquía hace que el objeto
nazca **con segmentos**. Cinco, en nuestro caso —cabecera, textos de cabecera, nodos, textos de
nodo e intervalos—, y ese formato se deriva de la anotación. Declarar la familia equivocada no
produce un error: produce el contenedor equivocado, que hay que borrar y rehacer. Ni siquiera viene
todo de la misma vista: los textos de los nodos no los entrega la vista de jerarquía sino otra
distinta, así que una sola jerarquía de centro de coste ya necesita tres vistas en el origen.

La segunda es que existen dos sintaxis de jerarquías en CDS y la que aparece primero en cualquier
búsqueda es la equivocada. La nueva —una entidad propia, declarada con `DEFINE HIERARCHY`— sirve
para consumo analítico y **no** para extracción; la vía de extracción sigue siendo la anotación
`@ObjectModel.dataCategory: #HIERARCHY`. Lo verificamos de la forma dura: las 244 páginas de la
guía oficial de SAP sobre modelos de datos ABAP no mencionan ni una sola vez la extracción hacia el
mundo analítico —ni la anotación que la habilita, ni el framework—. Es información correcta
aplicada al escenario equivocado, que es la clase de error más difícil de detectar porque todo lo
que lees es cierto.

La tercera es la que cambia el plan, y es consecuencia directa de la primera. Como los textos de
nodo llegan por separado, para migrar esas jerarquías por la vía que SAP recomienda **hay que
modificar objetos en el sistema destino**: agregarle al centro de coste dos características que hoy
no existen —una para el identificador de la jerarquía y otra para el texto del nodo, compuesta a la
anterior—, con longitudes fijas y mapeadas segmento por segmento. Eso no es parametrizar: es
modelar. Lo verificamos contra el sistema: en dos de las tres jerarquías del alcance, esa
configuración está literalmente vacía.

Ninguna de las especificaciones funcionales lo mencionaba. Y no por descuido: **están escritas
desde el lado del origen**. Describen con precisión qué dato hay que sacar de S/4HANA, porque ahí
es donde está la novedad y donde se concentró el análisis. El destino se da por sentado, porque
"ya existe y ya funciona".

Ese supuesto es el que hay que romper. En una migración de este tipo, el sistema que no estás
migrando también tiene trabajo, y ese trabajo no aparece en ningún documento hasta que alguien
intenta cargar el primer árbol.

## Qué le pediría a un plan de trabajo

Cuatro cosas concretas, y las dos últimas son para quien firma el alcance y el presupuesto, no
para quien dirige el equipo:

- **Que la definición de "terminado" sea un número, no un color.** Conteo contra el origen, carga
  completa, sin delta. Si la actividad se puede cerrar con una captura de pantalla en verde, el
  criterio está mal escrito.
- **Que el delta esté planeado como una fase posterior**, no como parte de la construcción. Es una
  decisión de secuencia que ahorra semanas de diagnóstico falso.
- **Que el alcance cubra explícitamente el sistema destino.** Si tus especificaciones sólo
  describen el origen, tienes un alcance a medias y una contingencia calculada sobre la mitad del
  trabajo. Vale la pena preguntar, antes de firmar: *¿qué hay que modificar del otro lado?*
- **Que la prueba de autorizaciones sea de negocio, no técnica.** Que el usuario de conexión se
  pueda conectar no prueba nada sobre qué datos alcanza a ver. Esto se pide por escrito y se mide
  con un conteo.

Lo digo desde una región donde esto no es hipotético. Buena parte de las operaciones de las
multinacionales instaladas en el noreste corre sobre plataformas SAP que están, o van a estar, en
esta misma transición. La conversación sobre cómo se prueba una migración no es un detalle de
implementación: es la diferencia entre descubrir un faltante en desarrollo o descubrirlo en un
cierre.

## El norte

La edición 02 de este newsletter defendía que el diseño es la migración. Lo sigo sosteniendo. Pero
la fase de construcción me enseñó algo que el diseño no puede resolver solo: **incluso con la
especificación correcta, la forma de comprobar que el dato llegó completo tuvo que cambiar.**

Migrar a un modelo declarativo no eliminó el riesgo: lo dejó sin síntoma. Y un riesgo sin síntoma
es el argumento para hacer la validación más estricta, no más ligera. Menos código no significa
menos pruebas. Significa otras pruebas: menos revisar lógica y más contar filas.

Si estás por entrar a esta fase, el cambio más barato que puedes hacer hoy no cuesta ni una línea
de código. Es reescribir el criterio de aceptación de tus actividades de carga para que exija un
número. Todo lo demás de esta edición lo descubrimos porque ese número no cuadraba.

---

### Fuentes

- SAP Learning — *Working with ODP Context: CDS view based extraction* (condiciones de extraibilidad: `@Analytics.dataCategory` **o** `@ObjectModel.dataCategory` **y** `@Analytics.dataExtraction.enabled`; sufijos `$P`/`$T`/`$H`/`$F` del ODP): https://learning.sap.com/courses/upgrading-your-sap-bw-skills-to-sap-bw-4hana/working-with-odp-context-cds-view-based-extraction_f01df9a0-0e79-4d76-be38-d2cfac4dde42
- SAP Learning — *Working with Hierarchy Views* (las cinco vistas de una jerarquía: fuente, jerarquía, directorio, textos de directorio y nodos; la vista de jerarquía no admite asociaciones; asociación recursiva al padre, al directorio y a las dimensiones por tipo de nodo): https://learning.sap.com/courses/developing-analytical-models-with-cds-based-analytical-projection-views/working-with-hierarchy-views
- SAP Learning — *Working with Dimension and Text Views* (llave compuesta: un solo `@ObjectModel.representativeKey`; los demás campos de la llave requieren asociación; reglas de `@Semantics.businessDate.to`/`.from`): https://learning.sap.com/courses/developing-analytical-models-with-cds-based-analytical-projection-views/working-with-dimension-and-text-views
- SAP Help — *Analytics Annotations* (`dataExtraction.enabled`, `dataCategory`, delta): https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/c2/dd92fb83784c4a87e16e66abeeacbd/content.htm
- SAP Help — *ObjectModel Annotations* (`dataCategory` para textos y jerarquías, `representativeKey`, `foreignKey.association`, `hierarchy.association`): https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/89/6496ecfe4f4f8b857c6d93d4489841/content.htm
- SAP KBA **3219389** — el proceso de carga filtra automáticamente por los idiomas instalados en el sistema destino cuando el DataSource tiene un campo marcado como *Language Field*; válido también para DataSources basados en vistas CDS de S/4HANA: https://userapps.support.sap.com/sap/support/knowledge/en/3219389
- SAP KBA **2754750** — `RSODP056`, *cannot derive InfoObject name*, cuando la vista destino de una asociación tiene característica compuesta (más de un campo clave, uno de ellos `representativeKey`): https://userapps.support.sap.com/sap/support/knowledge/en/2754750
- SAP KBA **3062210** — autorizaciones dependientes de usuario en vistas CDS vía DCL y `@AccessControl.authorizationCheck`: https://userapps.support.sap.com/sap/support/knowledge/en/3062210
- SAP Help — *ABAP Data Models* (guía oficial de modelos de datos ABAP; su capítulo de jerarquías no cubre extracción): https://help.sap.com/docs/abap-cloud/abap-data-models/abap-data-models
- SAP — *ABAP CDS: DEFINE HIERARCHY* (la sintaxis de jerarquía para consumo analítico, distinta de la vía de extracción): https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abencds_f1_define_hierarchy.htm
- SAP Community (S. Kranig, SAP) — *CDS based data extraction, Part III: Miscellaneous* (jerarquías: los textos de nodo llegan en una vista aparte y obligan a dos características externas en el destino; `RSA3` no aplica, se usa `RODPS_REPL_TEST` y no es simulación): https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/cds-based-data-extraction-part-iii-miscellaneous/ba-p/13452148
- SAP Community (RIG) — *An Introduction to the Data Transition Validation Tool* (reconciliación source-to-target como prueba de éxito): https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/an-introduction-to-the-data-transition-validation-tool/ba-p/13541524
