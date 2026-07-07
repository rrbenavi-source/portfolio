Hay dos formas de que un data agent falle.

Una es devolver un error. La otra —mucho peor— es devolver un número que se ve impecable y está equivocado.

El error lo detectas y sigues. El número equivocado no: se convierte en una lámina de comité y mueve una decisión en la dirección incorrecta, sin que nadie lo note. Y así es exactamente como falla el text-to-SQL cuando lo dejas operar sin contexto sobre un data warehouse real.

Ese es el punto que se pierde en casi toda la conversación sobre generative BI: el problema rara vez es el modelo de lenguaje. El modelo mejora cada trimestre y se abarata solo. Lo que decide si puedes confiar en la respuesta es el contexto —qué significa cada métrica, cuál es la tabla correcta, qué business rule aplica—. Eso no lo aporta el modelo. Lo aportas tú, en el semantic layer.

¿Qué es un semantic layer, en concreto? Una capa de traducción. Toma un schema de producción críptico y lo convierte en una interfaz de negocio, limpia y documentada, sobre la que la IA puede razonar con confianza. Y la parte que casi todos subestiman: la lógica de negocio vive en la definición de la view, no en la memoria del modelo. Si "ingresos netos" ya excluye reembolsos y cuentas de prueba, cada query hereda esa regla. La impone el motor SQL, no la buena voluntad del modelo.

Los números lo confirman. Sin ninguna capa de contexto, el text-to-SQL ronda 21–25% de acierto. Con buen prompting, el benchmark 2026 de dbt Labs lo sube a 64.5%. Y dentro del alcance de un semantic layer bien modelado, se acerca al 100%.

Pero lo más importante no es el porcentaje. Es cómo falla cada uno. El semantic layer, cuando no puede responder, te lo dice. El text-to-SQL entrega un dato equivocado con apariencia de verdad, sin una sola señal de alerta. Para explorar, esa flexibilidad se agradece. Para un número que va a un auditor, a un OKR o a un KPI de la compañía, la diferencia lo es todo.

Y no es casualidad hacia dónde se movió la industria. El anuncio más comentado de Databricks esta temporada no fue un modelo, sino Genie Ontology: una capa de contexto que codifica cómo el negocio define sus propias métricas. Dejamos de competir por el modelo y empezamos a competir por el contexto.

Después de 20+ años integrando SAP con un lakehouse, esta es la lección que me llevo: el modelo es un commodity; el contexto gobernado es la ventaja defendible. Y se construye sin heroísmos: empieza por las cinco métricas que tu negocio más pregunta, modélalas bien y valida contra la historia. Cuando esas cinco sean confiables, agregas otras cinco.

Escribí el análisis completo —con las fuentes y el cómo empezar paso a paso— en mi portfolio. 👇

🧭 Es la primera edición de Brújula, mi newsletter semanal: de los datos a las decisiones, sin perder el norte. Cada semana, un análisis sin humo sobre generative BI, agentes de IA y la estrategia para volverte data-driven.

📖 https://rrbenavi-source.github.io/portfolio/publicaciones/semantic-layer-data-agents

¿Tu organización está invirtiendo en el modelo… o en el contexto?

#DataAnalytics #GenerativeBI #SemanticLayer #SAP #Databricks #DataDriven #IA
