# Estandarizaron el diccionario, no la autoridad

*Cuatro plataformas que compiten entre sí acaban de declarar lo mismo: la capa de significado es el producto. Ninguna guarda quién firmó cada definición.*

**Brújula · Edición 07 · W34**
*Arquitectura de Datos · Capa Semántica*

---

Hace dos ediciones escribí aquí que la pregunta que decide si tus data agents dicen la
verdad no es qué modelo usas, sino **con la semántica de quién** responden. La
industria acaba de contestar esa pregunta, y la respuesta merece leerse con cuidado
porque viene envuelta en un anuncio que suena a solución.

En un solo tramo de semanas pasaron cuatro cosas. El 6 de julio, SAP cerró la compra de
Dremio. En julio también, el estándar abierto para intercambiar definiciones de negocio
entró a la Apache Software Foundation con el nombre de **Apache Ossie**. El 6 de
agosto, Databricks activó por defecto su **Genie Ontology** para todos los clientes. Y
el 12 de agosto, la misma Databricks publicó **Pages**. Microsoft ya venía desde junio
con Fabric IQ en disponibilidad general.

Cuatro competidores directos, un mismo movimiento: todos están construyendo —o
comprando— la capa donde vive el significado del negocio.

Es la validación más contundente que ha tenido esta tesis. Y también es donde conviene
abrir el archivo y leer, porque hay una ausencia que nadie está señalando.

## Qué estandariza el estándar

Empecemos por lo que es. Apache Ossie —antes Open Semantic Interchange, renombrado al
entrar a incubación— es un **formato de intercambio**: un archivo en JSON o YAML donde
escribes tus definiciones de negocio una vez y cualquier herramienta que hable ese
formato las lee igual. Que "venta neta" signifique lo mismo en tu plataforma de BI, en
tu motor de queries y en el agente de IA que te contesta en Teams.

No es un producto de nadie. Nació como iniciativa de Snowflake en septiembre de 2025 y
hoy lo gobierna la Apache Software Foundation, con listas públicas, votaciones sobre
cambios al spec y permisos de escritura que se ganan contribuyendo, no por el logo del
empleador. Pasó de 17 socios fundadores a **más de cincuenta organizaciones**. Entre
ellas, Snowflake y Databricks al mismo tiempo, que no es algo que uno vea seguido.

El core spec —la especificación central, hoy en versión 0.2.0, marcada explícitamente
como borrador— es corto y está bien hecho. Define cuatro piezas. **Datasets**: las
entidades de negocio, apuntando a una tabla o vista física. **Fields**: los atributos
con los que agrupas y filtras, separando el tipo de dato de su papel semántico.
**Relationships**: cómo se unen esas entidades, o sea las llaves foráneas que casi
ninguna base de datos productiva declara. Y **metrics**: las expresiones agregadas, con
soporte para escribir la misma métrica en varios dialectos de SQL a la vez.

Hay además un campo llamado `ai_context`, que es texto libre dirigido al modelo: el
lugar donde escribes la frase que la IA necesita leer antes de consultar.

Está bien pensado. Resuelve un problema real y llevábamos años pidiéndolo.

## Lo que no está en el archivo

Ahora la parte incómoda. Busca en ese spec las palabras **linaje**, **procedencia**,
**frescura** o **confianza**. No están. No hay campo, en ningún objeto, para registrar
quién aprobó esa definición, contra qué la verificó, cuándo fue la última vez que
alguien la revisó, ni qué tan seguro está de que siga siendo válida.

Esto no es una interpretación mía. Es una búsqueda de texto en un archivo público que
cualquiera puede repetir en dos minutos.

El estándar transporta **la definición**. No transporta **la autoridad de la
definición**. Y la diferencia entre esas dos cosas es todo lo que separa una respuesta
gobernada de una suposición con formato bonito.

Piénsalo desde el lado del que recibe. Un analista humano que abre un dashboard heredado
trae consigo un contexto que no está escrito: sabe que ese cálculo lo hizo Finanzas en
2021, que nunca se actualizó cuando cambió la política de descuentos, y que por eso
todos en el área lo cruzan a mano contra otra fuente. Un agente de IA no trae nada de
eso. Recibe un archivo con una definición y la trata como verdad, porque el archivo no
tiene forma de decirle otra cosa.

Hay un detalle más, y es de esos que solo aparecen al leer la letra chica. dbt Core, en
su versión 1.12, ya lee documentos Ossie de forma nativa: es el consumidor con la base
instalada más grande del ecosistema. Pero solo acepta las versiones 0.1.0 y 0.1.1 del
spec —cualquier otra cadena de versión produce un error de parseo— mientras la
especificación misma ya va en 0.2.0. Y cuando encuentra un elemento que no soporta, lo
**descarta con una advertencia y sigue cargando el resto**. Es una decisión de
ingeniería razonable. También es la manera exacta en que dos sistemas terminan creyendo
que comparten una definición mientras cada uno se quedó con una mitad distinta.

## La otra mitad: la autoridad calculada

Los vendors sí prometen resolver la confianza. Pero la resuelven **por inferencia**.

Databricks explicó en junio cómo decide su ontología qué definición manda cuando hay
varias. Usa un enfoque parecido al PageRank de Google: pesa de dónde salió la
definición, qué tan autoritativo es el autor de esa fuente, con qué frecuencia la gente
la usa, qué tan cerca está de activos certificados y qué tan fresca es. Con eso escoge
la que responde. Y el blog remata diciendo que así resuelve el problema del contexto
*sin pedirle a tus equipos que lo curen a mano*.

Seis semanas después, el 12 de agosto, la misma empresa publicó **Pages**: una función
para dar a cada término de negocio, acrónimo y KPI "una sola definición gobernada". Sus
propias notas de versión la describen como *la capa modelada por humanos* de esa misma
ontología.

Quiero ser preciso, porque esto no es una acusación: **es un acierto**. Que Databricks
haya entregado la capa curada a mano seis semanas después de anunciar que no hacía falta
es la mejor evidencia disponible de que sí hace falta. El producto está mejor que el
mensaje. Lo único que no se sostiene es seguir vendiendo la primera parte como si la
segunda fuera opcional.

Y del lado SAP el patrón se repite con otra forma. Lo que SAP integra de Dremio como
pieza estructural no es tanto el motor de consultas como el **catálogo**: la pieza que
va a dar a motores SAP y no-SAP acceso compartido al significado de negocio, las
relaciones, los permisos y —esta vez sí— el linaje, alimentando el Knowledge Graph. Es
la misma apuesta: el valor migró del cómputo al significado.

## Por qué esto se siente en la operación

Quien haya hecho una migración sabe exactamente dónde duele esto.

Cuando desarmas un reporte que lleva una década en producción, lo que encuentras nunca
es una definición limpia. Es una regla escrita en un exit de código, otra en una
condición de un filtro, otra en el criterio de alguien que ya no trabaja ahí. Y cuando
llegas al final del hilo, la pregunta que no puedes contestar no es *cómo se calcula*.
Eso lo lees en el código. La pregunta que no puedes contestar es **quién decidió que se
calculara así, y si esa persona tenía la autoridad para decidirlo**.

Ese es exactamente el campo que ningún formato de intercambio guarda.

Un preprint de este mes lo nombra bien, aunque conviene tomar sus cifras con reserva
—es de un investigador independiente, sin revisión por pares y sobre warehouses
sintéticos—: propone dejar de calificar a los agentes analíticos por exactitud de SQL y
calificarlos por **verdad de negocio**, porque el modo de falla caro no es la consulta
que truena. Es la consulta que corre bien, devuelve un número creíble y está mal. En su
benchmark, cerca de la mitad de las respuestas correctas no son un número: son una
aclaración, una abstención o un rechazo. La pregunta tenía dos lecturas válidas, o el
warehouse no podía contestarla, o la columna había quedado obsoleta.

Un agente que no sabe decir "no sé" no es un agente prudente al que le falta
entrenamiento. Es un agente al que nadie le dio con qué saberlo.

## Qué hacer el lunes

No estoy proponiendo que rechaces el estándar. Al contrario: adóptalo, es lo mejor que
le ha pasado a este problema en años, y tener un formato neutral gobernado por la ASF
en vez de por un proveedor es exactamente lo que había que pedir.

Lo que propongo es que no confundas exportar tus definiciones con haberlas gobernado.
Son dos trabajos distintos, y el segundo sigue siendo tuyo.

Tres cosas concretas:

**Uno.** Todo lo que el spec no guarda, guárdalo tú. El formato trae un campo de
extensiones para lo que no cupo en el estándar; ahí caben cuatro datos por cada
definición que exportes: quién la aprobó, contra qué evidencia se verificó, en qué
fecha, y cuándo caduca esa revisión. Si tu herramienta lo descarta al leerlo, al menos
tú sabrás qué se perdió.

**Dos.** Haz la prueba de la edición 05, ahora con el archivo enfrente. Toma las tres
métricas que más se pelean en tus juntas y escríbelas en el formato. Si el archivo
resultante no distingue entre la versión de Finanzas y la de Comercial —porque
estructuralmente no puede—, ya sabes qué va a recibir tu agente cuando lo conectes.

**Tres.** Ponle fecha. A partir de diciembre de 2027, las obligaciones de sistemas de
alto riesgo del AI Act europeo entran en aplicación; el aplazamiento ya se publicó y es
derecho vigente, no rumor. Quien opere filiales de matrices europeas va a recibir la
pregunta por gobierno corporativo mucho antes que por regulación local. Y la pregunta
va a ser esta: demuéstrame de dónde salió este número y quién autorizó que se calculara
así.

El diccionario ya está estandarizado. La firma al pie de cada definición sigue sin
tener dónde escribirse, y esa firma es tuya.
