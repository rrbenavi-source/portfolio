---
title: La IA ya escribe SQL casi perfecto. ¿Con la semántica de quién?
subtitle: El benchmark que movió el cuello de botella del modelo al modelado
format: opinión
date: 2026-08-04
---

_Borrador semilla — Idea 1 del digest W32. Formato: opinión, 2–3 páginas.
Pendiente de `papper-editor` (rigor y estructura) y `papper-humanizer` (voz).
No es texto final._

---

Hay un número nuevo esta semana que cierra un debate y abre otro. dbt Labs publicó
su benchmark 2026 de text-to-SQL: los modelos de frontera, solos contra el
warehouse, aciertan entre 84% y 90% de las preguntas. Los mismos modelos, con
grounding en un semantic layer, suben a 98.2% y hasta 100%. Léelo dos veces: el
modelo que "no sabía SQL" ya casi no existe. Lo que separa un copiloto de juguete
de uno de producción ya no es el modelo — es si alguien modeló la semántica sobre
la que responde.

Ese es el debate que se cerró. El que se abre es más incómodo: ¿quién modela?

## El benchmark mide lo que ya sabíamos operar

Un 90% de exactitud suena alto hasta que lo pones en operación. En un tablero
ejecutivo que responde cien preguntas al día, 90% significa diez números
equivocados diarios, servidos con la misma seguridad que los correctos. Nadie que
haya firmado un cierre acepta esa tasa. El salto de 90 a 98–100 no es incremental:
es la diferencia entre demo y producción.

Pero el benchmark tiene una letra chica que casi nadie lee: el semantic layer que
produce ese salto no se descarga. Se construye. Alguien tuvo que sentarse a
definir qué es "venta neta", contra qué tipo de cambio se convierte, qué canal
incluye y cuál excluye, en qué momento un pedido se vuelve venta. El modelo no
aporta esa semántica; la consume.

## En un shop SAP, la semántica ya existe. Ese es el problema

Aquí es donde el debate aterriza en mi terreno. En una operación SAP de veinte
años, esa capa semántica ya está definida — con una precisión que envidiaría
cualquier semantic layer moderno. El detalle es dónde vive: enterrada en
extractores, en rutinas de usuario, en las mil líneas de un reporte Z que calcula
"venta neta" de una forma que ningún documento describe.

Cuando escribí sobre la autopsia del reporte Z, el punto era exactamente este: la
lógica de negocio no vive en el código, vive en las decisiones acumuladas que el
código cristalizó. El benchmark de dbt le pone número a esa tesis. Si el grounding
semántico vale entre 8 y 16 puntos de exactitud, entonces la autopsia de tu capa
SAP no es deuda técnica: es el activo que decide si tu copiloto de datos dice la
verdad.

## El error de compra que viene

Preveo una ola de proyectos que van a comprar el copiloto y saltarse el modelado.
El pitch es irresistible: "conéctalo al warehouse y pregunta en lenguaje natural".
Y va a funcionar — en la demo, con las preguntas fáciles, con las tablas limpias.
En producción, la pregunta del CFO no es fácil: cruza canal, segmento de precio,
moneda y un ajuste que solo existe porque en 2019 alguien decidió tratar las
devoluciones de cierta forma.

La secuencia correcta es la aburrida: primero extraer la semántica de donde vive
(y en industriales de este lado del mundo, vive en SAP), después modelarla en una
capa que el modelo pueda consumir, y al final — solo al final — conectar el
copiloto. Es el mismo orden que el benchmark implica y que veinte años de
disciplina de datos confirman: el techo lo pone la fuente, no el destino.

## Cierre (accionable, por desarrollar)

Antes de evaluar un copiloto de datos, haz una prueba más barata: toma tus tres
métricas más peleadas y pide a dos personas de negocio que las definan. Si las
definiciones no coinciden, el copiloto no es tu siguiente paso; el modelado lo es.

---

**Fuentes citadas:**
- dbt Developer Blog — Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update.
  https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- Solid — Text2SQL vs. Semantic Layer? The real question is who does the modeling.
  https://www.getsolid.ai/resources/text2sql-vs-semantic-layer-the-real-zxqgr7
- Atlan — Text-to-SQL for Enterprise: Metric Drift and Context Layer (2026).
  https://atlan.com/know/ai-agent/data-for-ai/text-to-sql-for-enterprise/
