# LinkedIn — ES

**Hook**
Hay dos formas de que un asistente de datos falle. Una es devolver un error.
La otra —mucho peor— es devolver un número que se ve impecable y está equivocado.

**Cuerpo**
Esa segunda forma es exactamente como falla el text-to-SQL cuando lo dejas operar
sin contexto sobre un data warehouse real. Y es el punto que se pierde en casi toda
la conversación sobre generative BI: el problema rara vez es el modelo de lenguaje.
El modelo mejora cada trimestre y se abarata solo.

Lo que decide si puedes confiar en la respuesta es el contexto —qué significa cada
métrica, cuál es la tabla correcta, qué regla de negocio aplica—. Eso vive en el
semantic layer, y no lo aporta el modelo: lo aportas tú.

Los números lo confirman. En el benchmark 2026 de dbt Labs, el text-to-SQL acierta
64.5% sobre el set completo de preguntas; dentro del alcance de un semantic layer
bien modelado, el acierto se acerca al 100%. Pero lo importante no es el porcentaje,
sino cómo falla cada uno: el semantic layer, cuando no puede responder, te lo dice.
El text-to-SQL entrega un dato equivocado con apariencia de verdad.

Después de años integrando SAP con un lakehouse, esta es la lección que me llevo:
el modelo es un commodity; el contexto gobernado es la ventaja defendible. Y se
construye igual que siempre: empieza por las cinco métricas más consultadas,
modélalas bien, valida contra la historia.

**CTA**
Escribí el análisis completo (con las fuentes) en mi papper de esta semana. Link al
PDF en los comentarios. ¿Tu organización está invirtiendo en el modelo o en el contexto?

_(Subida manual — recuerda adjuntar el PDF o el link a /publicaciones.)_
