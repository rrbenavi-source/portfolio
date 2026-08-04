---
title: La IA ya escribe SQL casi perfecto. ¿Con la semántica de quién?
subtitle: El benchmark que movió el cuello de botella del modelo al modelado
format: opinión
date: 2026-08-04
---

Hay un número que lleva unos meses circulando y que todavía no aterriza en cómo
las empresas están comprando sus copilotos de datos. En abril, dbt Labs publicó
la actualización 2026 de su benchmark de text-to-SQL: los modelos de frontera,
solos contra la base de datos, aciertan entre 84% y 90% de las preguntas
analíticas. Los mismos modelos, respondiendo sobre un semantic layer bien
modelado, suben a 98.2% y hasta 100%.

Léelo dos veces, porque cierra un debate de años. El modelo que "no
sabía SQL" ya casi no existe: Claude Sonnet 4.6 pasó de 90.0 a 98.2; GPT-5.3
Codex, de 84.1 a 100. Lo que separa un copiloto de demo de uno de producción ya
no es el modelo. Es si alguien modeló la semántica sobre la que responde.

Ese es el debate que se cerró. El que se abre es más incómodo: ¿quién modela?

## 90% suena alto hasta que lo pones a operar

En un tablero ejecutivo que responde cien preguntas al día, 90% de exactitud
significa diez números equivocados diarios — servidos con la misma seguridad que
los correctos. Nadie que haya firmado un cierre acepta esa tasa. El salto de 90 a
98–100 no es una mejora incremental; es la diferencia entre una demo impresionante
y algo que puedes poner frente a un CFO.

Y hay un detalle del benchmark más revelador que la cifra principal: los dos
enfoques no fallan igual. Cuando el text-to-SQL se equivoca, suele
devolver un número plausible e incorrecto, con total confianza. Cuando el
semantic layer no puede responder, lo dice: error explícito, fuera de alcance.
Uno te miente con seguridad; el otro te avisa que no sabe. En un entorno donde
alguien firma el número antes de que llegue a un ejecutivo — que es como debería
operar cualquier plataforma seria — esa diferencia vale más que los puntos de
exactitud. Un error visible se corrige; un número plausible y falso viaja.

## La letra chica: la semántica no se descarga

El benchmark tiene una honestidad que se agradece. Para que el text-to-SQL puro
compitiera, los autores cargaron el esquema completo de la base como contexto del
modelo — y ellos mismos advierten que eso no es práctico en datasets grandes.
Piénsalo desde una operación SAP: miles de tablas, nombres como VBAK, VBAP, KONV,
lógica repartida en extractores y rutinas. No hay ventana de contexto que
aguante eso, y aunque la hubiera, el esquema no contiene lo que importa. El
esquema te dice que existe un campo; no te dice por qué en 2019 alguien decidió
que las devoluciones de cierto canal se netean distinto.

También es justo decir el tamaño de la prueba: once preguntas, veinte corridas
por configuración, sobre un dataset de seguros semi-complejo. No es la escala de
una operación real. Pero la dirección del resultado es consistente con lo que
cualquiera que opere plataformas de datos ha visto en carne propia: el grounding
semántico no es un lujo, es la condición para que el número sea defendible.

Y ahí está la letra chica completa: el semantic layer que produce ese salto no se
descarga. Se construye. Alguien tuvo que sentarse a definir qué es "venta neta",
contra qué tipo de cambio se convierte, qué canal incluye y cuál excluye, en qué
momento un pedido se convierte en venta. El modelo no aporta esa semántica. La
consume.

## En un shop SAP, la semántica ya existe. Ese es exactamente el problema

Aquí es donde el benchmark aterriza en mi terreno. En una operación SAP de veinte
años, esa capa semántica ya está definida — con una precisión que envidiaría
cualquier semantic layer moderno. Cada regla de negocio pasó por auditorías,
cierres y usuarios que reclaman cuando el número no cuadra. El detalle es dónde
vive: enterrada en extractores, en rutinas de usuario, en las mil líneas de un
reporte Z que calcula "venta neta" de una forma que ningún documento describe.

Hace unas semanas escribí que migrar un reporte Z no es traducir ABAP: es una
autopsia. La lógica de negocio no vive en el código; vive en las decisiones
acumuladas que el código cristalizó. El benchmark de dbt le pone número a esa
tesis. Si el grounding semántico vale entre 8 y 16 puntos de exactitud — y la
diferencia entre mentir con confianza y avisar que no sabes —, entonces la
autopsia de tu capa SAP no es deuda técnica. Es el activo que decide si tu
copiloto de datos dice la verdad.

## El error de compra que viene

Viene una ola de proyectos que van a comprar el copiloto y saltarse el modelado.
El pitch es irresistible: conéctalo al warehouse y pregunta en lenguaje natural.
Y va a funcionar — en la demo, con las preguntas fáciles, con las tablas limpias.
En producción, la pregunta del CFO no es fácil: cruza canal, segmento de precio,
moneda y un ajuste que solo existe porque alguien lo decidió hace siete años y ya
no está en la empresa.

La secuencia correcta es la aburrida. Primero extraer la semántica de donde vive
— y en las operaciones industriales de este lado del mundo, vive en SAP. Después
modelarla en una capa que el modelo pueda consumir: métricas definidas una vez,
gobernadas, con dueño. Y al final, solo al final, conectar el copiloto. Es el
mismo orden que el benchmark implica y que veinte años de disciplina de datos
confirman: el techo lo pone la fuente, no el destino.

## La prueba barata antes de comprar

Antes de evaluar cualquier copiloto de datos, corre una prueba que no cuesta
licencias: toma tus tres métricas más peleadas y pídele a dos personas de negocio
que te las definan por escrito. Si las definiciones no coinciden — y en mi
experiencia, no coinciden —, tu siguiente paso no es el copiloto. Es el modelado.
El copiloto solo va a responder, con mucha seguridad, la versión de la métrica
que nadie acordó.

---

**Fuentes:**
- Ganz, J. & Perigaud, B. (dbt Labs) — *Semantic Layer vs. Text-to-SQL: 2026
  Benchmark Update*, 7-abr-2026. Cifras, metodología (11 preguntas × 20 corridas,
  dataset ACME Insurance) y caveat del esquema como contexto.
  https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- Solid — *Text2SQL vs. Semantic Layer? The real question is who does the
  modeling*. El mismo argumento desde el ángulo del modelado.
  https://journey.getsolid.ai/p/text2sql-vs-semantic-layer-the-real
- Atlan — *Text-to-SQL for Enterprise: Metric Drift and Context Layer* (2026).
  Metric drift y capa de contexto en entornos enterprise.
  https://atlan.com/know/ai-agent/data-for-ai/text-to-sql-for-enterprise/
