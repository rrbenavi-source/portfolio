TÍTULO:  El diseño es la migración

SUBTÍTULO:  Por qué en un salto ECC → S/4HANA las especificaciones deciden si tus datos nacen bien

PORTADA:  brujula-cover-02.png


═══════════════════════════════════════════════════════
  NEWSLETTER — copia desde aquí
═══════════════════════════════════════════════════════

[ Sube la portada: brujula-cover-02.png ]

Hay una frase que escucho en casi todos los proyectos de migración a S/4HANA. Suena inofensiva y es la más cara del proyecto:

"los extractores solo hay que pasarlos a CDS views."

Suena a tarea mecánica. Un extractor clásico entra, una CDS view sale, se reapunta la transformación de BW y listo. Es la promesa del lift-and-shift: mismo dato, nueva plataforma, cero pensamiento.

Y es justo ahí, en ese "cero pensamiento", donde una migración se pierde meses antes de que alguien escriba una línea de código.

Mi tesis, y la sostengo desde el rol de arquitecto: el diseño es la base del cambio, y la especificación funcional es la garantía de que la migración salga bien. No el desarrollo. No las herramientas. El diseño. Todo lo demás ejecuta una decisión que ya se tomó —bien o mal— cuando se redactó la spec.


La extracción a CDS no es un renombre, es una cadena de decisiones

Cuando SAP movió el mundo a S/4HANA, también cambió la forma de sacar datos hacia BW. La extracción clásica por S-API dejó de ser la vía estratégica; su reemplazo es la extracción basada en CDS views sobre el contexto ODP (ODP-CDS), habilitada con la anotación @Analytics.dataExtraction.enabled. En la nube pública, el camino clásico por RFC ya ni siquiera existe.

Hasta aquí, todo el mundo asiente. El problema empieza con tres verdades que la spec mecánica ignora:

1. Released no significa extractora. Que una CDS view exista, esté liberada y hasta lleve el dato que buscas no implica que puedas usarla como DataSource. SAP incluso publica una vista de sistema, I_DataExtractionEnabledView, precisamente para que verifiques cuáles extraen de fábrica y cuáles no. Si tu spec asume que "hay una CDS para eso", no está diseñando: está adivinando.

2. No es un mapeo 1:1. La técnica de delta cambia —del timestamp clásico al Change Data Capture por triggers— y eso condiciona el diseño de la propia vista: una con demasiados joins o agregaciones puede quedar sin delta. Elegir la vista es una decisión de arquitectura, no una búsqueda en un catálogo.

3. La extensibilidad tiene reglas, y esas reglas son clean core. Un objeto puede estar liberado para key user extensibility y aun así NO estarlo para developer extensibility; sin ese contrato, no lo puedes consumir en un select from dentro de una CDS Z bajo ABAP Cloud. Eso no se descubre programando. Se decide en el diseño.

Tres decisiones. Ninguna se resuelve tecleando. Todas viven o mueren en la spec.


Un extractor de saldos que parecía trivial

Déjame aterrizarlo con el caso que mejor enseña esto: migrar un extractor de saldos de contabilidad general, 0FI_GL_10. En el papel, el candidato perfecto para el lift-and-shift. La spec inicial lo trataba como un swap directo. Tres cosas la desmentían.

Uno: la clase de objeto. 0FI_GL_10 extrae saldos (totales acumulados). Su hermano 0FI_GL_14 extrae partidas (line items). En S/4HANA el corazón es ACDOCA, el Universal Journal, que guarda documentos —partidas—, no saldos. Y el saldo de arrastre no se reproduce sumando las partidas del período: se materializa como documentos técnicos de "Período 0". Mapear un extractor de saldos contra una vista de partidas produce el peor error posible en BI financiera: un número plausible y equivocado. Cuadra a la vista, pasa desapercibido, y aparece mal en el saldo inicial de un reporte de directorio.

Dos: la capacidad de extracción. El cubo que parecía la respuesta, I_GLAcctBalanceCube, no viene habilitado para extracción. Es un proveedor de datos para consultas analíticas, no una fuente de extracción. La Primera Verdad, hecha carne.

Tres: el clean core. Ese cubo no está liberado para developer extensibility. La decisión ya no era técnica, era de arquitectura: envolverlo en un Z-wrapper por ABAP clásico —pragmático, pero fuera de clean core— o reconstruir la lógica de saldos sobre ACDOCA —limpio, sostenible, más pesado—. No hay respuesta universal. Hay una que se documenta, se justifica y se firma. O una que alguien improvisa en desarrollo, tarde y sin contexto.

[ Sube la figura: fig-3-trampas.png ]

El punto no es 0FI_GL_10. El punto es que el extractor que parecía un swap de un minuto escondía tres decisiones de arquitectura, y las tres pertenecen al diseño. Si la spec no las resuelve, no desaparecen: se posponen al momento y a la persona equivocados.


Lo que cuesta equivocarse tarde

Aquí no estoy filosofando: hay números. Que un defecto cueste más mientras más tarde se corrige es una de las reglas más viejas de la ingeniería, y la NASA la midió. Tomando como base 1 el costo de corregir un error en la fase donde nace —requisitos—, atraparlo en diseño cuesta de 3 a 8 veces más; en integración y pruebas, decenas de veces más; y en producción, cientos de veces más.

[ Sube la figura: fig-costo-defecto.png ]

Y no es teoría de laboratorio. Un estudio de Horváth de 2025 sobre transformaciones S/4HANA encontró que más del 60% se desvía en presupuesto y plazo, con la migración de datos y las fases de prueba entre las causas más subestimadas. Traducción: el trabajo que la gente trata como "mecánico" es justo el que descarrila los proyectos.

Lo más revelador: SAP mismo trata la reconciliación como la prueba de éxito de una migración financiera. Entrega herramientas dedicadas —el Data Transition Validation Tool, frameworks de validación, checks de consistencia previos— cuyo único propósito es cazar exactamente ese fallo: un saldo que no cuadra, un carryforward que no se reprodujo. Que esas herramientas existan es la confesión de la industria: el número equivocado es tan común que hubo que construir una disciplina entera para atraparlo.

“La tecnología casi siempre funciona exactamente como la configuraste. El trabajo del arquitecto es asegurarse de que la configuración sea la correcta antes de que funcione.”


La especificación como contrato, no como papeleo

Si el diseño es la base, la especificación es donde ese diseño se vuelve exigible. Una buena spec de extractor no describe, contrata; y contrata con trazabilidad: enlaza el requisito de negocio con el objeto CDS elegido, ese objeto con cada campo, cada campo con su regla de derivación, y esa regla con la prueba que la valida.

Cinco prácticas que separan una migración que nace bien de una que nace endeudada:

•  Fit-to-standard primero. Antes de diseñar un Z, pregunta si ya existe una CDS released que extraiga lo que necesitas. Si no la hay, construir es una decisión consciente, no un default.

•  Verifica capacidad y release, no las asumas. I_DataExtractionEnabledView existe para eso. "Creo que hay una vista para esto" no es una spec.

•  Valida la clase de objeto campo por campo. Saldo o partida. Total o line item. La mayoría de los errores caros viven en esta confusión, y se atrapan leyendo, no compilando.

•  Decide el clean core con los ojos abiertos. La deuda técnica aceptada a conciencia es una decisión; la contraída por descuido es una trampa.

•  Reconciliación como definición de "hecho". Un extractor no está terminado cuando corre. Está terminado cuando el dato en S/4HANA cuadra contra el origen.


El norte

Una migración a S/4HANA no se gana en el build. Se gana —o se pierde— en el diseño, y la especificación es el documento donde esa apuesta queda por escrito. El extractor que parece trivial suele ser el que esconde la decisión más difícil. Tratarlo como un renombre es la forma más silenciosa de heredar, a la nueva plataforma, los errores que veníamos a dejar atrás.

Ese es el norte que no conviene perder.


🧭 Brújula es mi newsletter semanal: de los datos a las decisiones, sin perder el norte. Cada semana, un análisis sin humo sobre arquitectura de datos, SAP, generative BI y la estrategia para volverte data-driven.

📖 El análisis completo, con las 9 fuentes enlazadas, está en mi portfolio:
https://rrbenavi-source.github.io/portfolio/publicaciones/diseno-es-la-migracion

Y una pregunta para ti que estás en una migración S/4HANA: el extractor que hoy tratas como un swap de un minuto… ¿ya sabes qué decisión de arquitectura esconde?

═══════════════════════════════════════════════════════
  NEWSLETTER — copia hasta aquí
═══════════════════════════════════════════════════════




═══════════════════════════════════════════════════════
  POST DE LANZAMIENTO (para tu feed) — copia desde aquí
═══════════════════════════════════════════════════════

En casi todos los proyectos de migración a S/4HANA escucho la misma frase inofensiva:

"los extractores solo hay que pasarlos a CDS views."

Suena a tarea mecánica. Y es la decisión más cara del proyecto disfrazada de trámite.

Migrar un extractor de saldos como 0FI_GL_10 parecía un swap de un minuto. Escondía tres decisiones de arquitectura:

→ que una CDS view esté released no significa que sea extractora.
→ el saldo no se reconstruye sumando partidas: en ACDOCA vive como documentos de "Período 0". Confundirlo produce el peor error de la BI financiera: un número plausible y equivocado.
→ exponerlo a BW obliga a elegir entre salirte del clean core o reconstruir la lógica. No hay respuesta universal; hay una que se firma y otra que alguien improvisa tarde.

Ninguna de las tres se resuelve tecleando. Las tres viven o mueren en la especificación.

Y el costo de posponerlas no es opinión: la NASA lo midió. Un defecto que atrapas en requisitos cuesta 1; en producción, cientos. Horváth: +60% de las transformaciones S/4HANA se pasan de presupuesto y plazo, con la migración de datos entre las causas más subestimadas.

La tesis de esta edición de Brújula 🧭 en una línea:

Una migración a S/4HANA no se gana en el build. Se gana —o se pierde— en el diseño.

Escribí el análisis completo, con el caso y las fuentes. Enlace en el primer comentario. 👇

#SAP #S4HANA #DataEngineering #CDSViews #CleanCore #Arquitecturadedatos

═══════════════════════════════════════════════════════
  POST — copia hasta aquí
═══════════════════════════════════════════════════════


PRIMER COMENTARIO (pégalo aparte, debajo de tu post):

📖 Edición 02 de Brújula, completa y con fuentes:
https://rrbenavi-source.github.io/portfolio/publicaciones/diseno-es-la-migracion
