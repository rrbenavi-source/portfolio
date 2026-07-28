# Secuencia de mensajes — Marco Quintanar

**Canal:** DM de LinkedIn (1er grado, sin límite de 300 caracteres).
**Envío:** miércoles 29 o jueves 30 de julio de 2026 — uno o dos días DESPUÉS de
que salga la edición 04 del newsletter, nunca el mismo día.
**Fuente:** `dossier.md`, bloques 5 (vocabulario), 7 (objeciones), 8 (qué no decir).

---

## Mensaje 1 — canónico

> Marco, qué tal. Nos conectamos hace unas semanas a raíz de la newsletter — soy
> Ricardo, el que escribe los pappers de datos que de repente te aparecen.
>
> Esta semana publiqué uno sobre migrar reportería Z de SAP hacia un lakehouse, y
> escribiéndolo me quedé pensando en tu terreno.
>
> El patrón que veo seguido en industriales es este: se construye un ecosistema
> `AI-Ready` impecable del lado de Databricks —Medallion, Unity Catalog, gobierno,
> lineage, todo bien puesto— y al final el techo real se lo pone la capa fuente. El
> dato que sale de SAP sin su semántica no se arregla con más gobierno del lado del
> lake; se arregla en la extracción, que es donde casi nadie quiere meterse.
>
> Llevo quince años metido justo en esa capa —BW/4HANA, ECC, reportes Z— con
> industriales del norte.
>
> ¿Te suena el patrón, o en Honeywell ya lo tienen resuelto por ese lado?

**149 palabras.** Dentro del rango 120–160.

**Verificación de las 7 reglas del bloque 8 del dossier:**

| Regla | Cumple |
|---|---|
| No diagnosticar Honeywell | ✅ Es patrón en tercera persona + pregunta abierta. Nunca afirma nada de su operación |
| No mencionar su vacante | ✅ Ni una palabra |
| No pedir llamada | ✅ El cierre es una pregunta de chat |
| No adjuntar material | ✅ Sin links, sin deck |
| No liderar con Heineken | ✅ No aparece |
| No elogiar el perfil | ✅ Sin "vi tu perfil", sin adulación |
| No traducir sus términos | ✅ `AI-Ready`, Medallion, Unity Catalog, lineage, lakehouse intactos |

**Por qué el cierre funciona:** "¿o ya lo tienen resuelto?" le regala la salida. Puede
contestar que sí y quedar bien, lo cual hace barato contestar. Una pregunta que solo
se puede responder aceptando una llamada, no se contesta.

---

## Variante A — más técnica

Para si se prefiere entrar directo por el problema, sin rodeo.

> Marco, qué tal. Soy Ricardo — nos conectamos por la newsletter hace unas semanas.
>
> Publiqué esta semana un papper sobre por qué migrar un reporte Z de SAP no es
> traducir ABAP: la lógica de negocio no vive en el código, vive en veinte años de
> decisiones que nadie documentó. Cuando eso pasa a un lakehouse sin autopsia
> previa, el número llega distinto y nadie sabe por qué.
>
> Es el punto ciego que veo en varios industriales: la capa Databricks queda
> `production-grade` y la capa fuente sigue siendo un acto de fe. El gobierno del
> lado del lake no alcanza a cubrir lo que se perdió en la extracción.
>
> Quince años en esa capa —BW/4HANA, ECC, extractores— con manufactura del norte.
>
> ¿Lo has visto de ese lado, o en Honeywell entran por otro camino?

**134 palabras.**

---

## Variante B — más conversacional

Para si se prefiere que pese más la conversación entre pares que el argumento.

> Marco, qué tal. Soy Ricardo, nos conectamos por la newsletter hace poco.
>
> Escribí esta semana sobre algo que me tiene dando vueltas: llevo años viendo
> equipos que hacen todo bien del lado moderno —Medallion, Unity Catalog, `Data
> Products` gobernados— y que aun así se topan con un techo que no está ahí, sino
> en la fuente. Casi siempre SAP, y casi siempre la parte que nadie quiere tocar.
>
> Me da curiosidad tu lectura porque tu terreno es justo donde eso pega: industrial
> global, muchos sistemas fuente, y un COE que tiene que responder por el número.
>
> Yo llevo quince años del lado feo de esa capa —BW/4HANA, ECC, reportes Z—.
>
> ¿Te hace sentido el patrón, o en Honeywell ya está resuelto ese pedazo?

**123 palabras.**

---

## M2 — Rama A: responde con interés técnico

Cuando pregunta, discute o comparte su contexto. **Profundizar sin vender.** Una sola
pregunta de descubrimiento, no un interrogatorio.

> Eso que dices tiene sentido. Lo que me sigue pareciendo el punto más difícil no es
> el pipeline —eso es lo fácil— sino demostrar que el número de destino es el mismo
> que el de origen, y poder explicar cada diferencia cuando alguien pregunta.
>
> En tu caso, con `Global Industrials`, ¿cuántos sistemas fuente terminan alimentando
> lo que ve el VECE COE? Es la variable que en mi experiencia decide si el problema
> es de ingesta o de semántica.

**Regla:** el one-pager NO se manda aquí. Solo si él pregunta explícitamente "¿y
ustedes qué hacen?" o equivalente. Ver `one-pager-honeywell.md`.

**Si menciona su vacante primero** (y solo si él la saca), ahí sí se puede introducir
la Fábrica de Datos — nunca antes. Respuesta corta:

> Por eso te preguntaba. Nosotros ese trabajo lo entregamos como producto, no como
> headcount: un equipo en pool recibe el requerimiento y responde por integridad,
> calidad y consumo, facturado por uso. Es otra cosa que contratar a alguien.

---

## M2 — Rama B: responde cortés pero tibio

"Interesante, gracias por compartir" y poco más. **Cerrar bien, cero insistencia.**

> Va, gracias por leerlo. Si en algún momento te topas con ese tema por tu lado, con
> gusto te comparto lo que hemos aprendido. Suerte con el roadmap.

**28 palabras.** No hay M3. Insistir después de un tibio quema el contacto de forma
permanente con este perfil.

---

## Rama C: silencio

**No hay M2.** No se manda nada.

Reactivación natural en 3–4 semanas, y solo con contenido nuevo que sea genuinamente
relevante para él — una edición del newsletter que toque su terreno, no un recordatorio.

**Frases prohibidas** en cualquier reactivación:

- "Solo dando seguimiento"
- "Retomando mi mensaje anterior"
- "¿Tuviste oportunidad de leer…?"
- "No sé si viste mi mensaje"

Todas confirman que el primer mensaje era de venta. Si se reactiva, se reactiva con
algo de valor y sin referencia al mensaje ignorado.
