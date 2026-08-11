# Digest 2026-W33

Barrido: lunes 10-ago-2026 (ventana 03-ago → 10-ago).
Edición objetivo: **06** del newsletter Brújula, martes 11-ago-2026.

> Notas del barrido:
> - LinkedIn feed (fuente `news`) sigue sin ser accesible en headless — omitido.
> - SAP Community devolvió **403** en fetch directo; la nota sobre BW (Idea 3) está
>   sostenida en fuentes secundarias y **requiere verificación** antes de escribirse.
> - Semana floja en anuncios de producto: Databricks y Microsoft no publicaron nada
>   nuevo en la ventana (lo grande sigue siendo DAIS/Build de junio). El gancho fuerte
>   de la semana no vino de un vendor, vino de **investigación** y de **regulación**.

---

## Idea 1 — El examen estaba mal calificado ⭐

- **Formato:** opinión
- **Tesis:** la semana pasada publicamos que la IA ya escribe SQL casi perfecto y que
  lo que decide es la capa semántica. Ahora aparece el peldaño de abajo: un estudio
  audita los dos benchmarks de text-to-SQL más usados y encuentra que **más de la
  mitad de las preguntas están mal anotadas** — BIRD Mini-Dev 52.8%, Spider 2.0-Snow
  62.8%. Al corregirlas y reevaluar los 16 agentes del leaderboard de BIRD, el
  desempeño se mueve entre −7% y +31% y las posiciones se mueven hasta ±9 lugares.
  El ranking sobre el set sin corregir correlaciona fuerte con el oficial
  (Spearman 0.85) y **débil con el corregido (0.32)**: es decir, el leaderboard que
  te enseña el vendor mide en buena parte ruido.
  El giro que lo hace nuestro: el patrón de error dominante **no es SQL mal escrito,
  es la pregunta ambigua** — desalineación entre lo que la pregunta significa y la
  lógica que el query pretendía. Gente que arma datasets de texto-a-SQL para vivir,
  con el esquema enfrente y pagada por ser precisa, falló en la mitad de los casos.
  ¿Qué probabilidad le das entonces a "dame las ventas netas del mes" dicho en una
  junta, contra un modelo de datos que nadie documentó?
  Corolario accionable y continuidad directa con la edición 05: **el único examen que
  cuenta es el tuyo.** La prueba de las tres métricas peleadas deja de ser una
  recomendación simpática y pasa a ser el único criterio de compra defendible.
- **Por qué ahora:** el paper se presentó en **CIDR 2026** y el preprint es de
  **13-ene-2026**; no es noticia de esta semana, pero es la respuesta natural —y aún
  no dicha— a la edición 05 que Ricardo acaba de publicar. El gancho es editorial,
  no de calendario: pocas veces se puede publicar el contrapeso de tu propia tesis
  con evidencia primaria. Refuerza el posicionamiento "sin humo".
- **Riesgo a vigilar:** sería la **tercera edición seguida** rondando text-to-SQL
  (05 fue exactamente eso). Se resuelve si el papper no habla de benchmarks sino de
  **cómo se define una pregunta de negocio**, usando el estudio como evidencia y
  aterrizando en el terreno SAP (la ambigüedad vive en los extractores y reportes Z
  — continuidad con W31).
- **Fuentes:**
  - https://arxiv.org/abs/2601.08778 — *Pervasive Annotation Errors Break Text-to-SQL
    Benchmarks and Leaderboards*. Jin, Choi, Zhu, Kang (UIUC). 13-ene-2026.
    **Fuente primaria, neutral, académica.** De aquí salen todas las cifras.
  - https://www.vldb.org/cidrdb/papers/2026/p5-jin.pdf — versión CIDR 2026,
    *Text-to-SQL Benchmarks are Broken*. ⚠️ **Discrepancia a resolver:** una fuente
    secundaria le atribuye 66.1% a Spider 2.0-Snow contra el 62.8% del abstract de
    arXiv. Usar el número de arXiv y verificar el PDF de CIDR antes de citar.
  - https://arxiv.org/html/2409.02038v3 — BEAVER, benchmark enterprise de text-to-SQL
    (contraste: por qué los benchmarks públicos no se parecen a tu warehouse).
  - https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — el benchmark de
    dbt ya citado en la edición 05; se reusa como el "antes" del argumento.

## Idea 2 — Te movieron la fecha, no el problema

- **Formato:** opinión
- **Tesis:** el 2-ago-2026 entró en aplicación la mayor parte del AI Act europeo
  (transparencia del Art. 50, poderes sancionadores sobre modelos de propósito
  general, autoridades nacionales de vigilancia de mercado). Pero lo que casi todo
  mundo estaba preparando —las obligaciones de sistemas de **alto riesgo** del Anexo
  III— **se corrió a 2-dic-2027** vía el Digital Omnibus, y a 2-ago-2028 para IA
  embebida en producto regulado. Dieciséis meses de aire.
  La tesis: la prórroga es una trampa de incentivos. Lo que exigen los artículos 10,
  12 y 13 —procedencia documentada de cada dataset, versionado, registro automático
  de eventos, trazabilidad de la decisión— **no es trabajo de cumplimiento, es la
  misma línea de linaje que necesitas para que tu agente sirva de algo.** Quien
  postergue el linaje porque el regulador le dio prórroga, va a llegar a diciembre de
  2027 sin cumplimiento *y* sin agentes que funcionen. La fecha se movió; el defecto
  arquitectónico no.
  Ángulo México: relevante para filiales de matrices europeas, que van a recibir el
  requerimiento por gobierno corporativo mucho antes que por regulación local.
- **Por qué ahora:** el hito es de hace **8 días** (2-ago-2026) y la confusión sobre
  qué aplicó y qué no está fresca — varias fuentes secundarias siguen publicando que
  el alto riesgo entró en agosto. Corregir eso con la fuente oficial ya es valor.
- **Riesgo a vigilar:** tema regulatorio, no técnico; hay que evitar sonar a abogado
  o a consultora de compliance. Solo funciona si el papper se queda en el terreno de
  arquitectura de datos (linaje, versionado, logging) y no en el legal.
- **Fuentes:**
  - https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act
    — **timeline oficial de la Comisión Europea.** Fuente de primera parte, verificada
    en este barrido: 2-ago-2026 mayoría de reglas + inicio de enforcement;
    2-dic-2027 Anexo III; 2-ago-2028 Anexo I.
  - https://artificialintelligenceact.eu/article/26/ — Art. 26, obligaciones del
    *deployer* (el que usa, no el que fabrica): es el artículo que aplica a un
    corporativo que compra un copiloto de datos.
  - https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai — marco
    regulatorio oficial, para el detalle de Arts. 10/12/13.
  - ⚠️ Verificar antes de escribir: fecha exacta de publicación del Digital Omnibus
    en el Diario Oficial (las fuentes secundarias dan 8-jul-2026 de firma, "pendiente
    de publicación").

## Idea 3 — La decisión de BW que ya no puedes seguir posponiendo

- **Formato:** deep-dive
- **Tesis:** SAP extendió mantenimiento —BW/4HANA hasta 2040, BW 7.5 hasta 2027 con
  extendido a 2030— y a la vez retiró Datasphere y SAC del catálogo de servicios
  elegibles BTPEA/CPEA/PAYG para suscripciones nuevas desde el 1-ene-2026: si los
  quieres, es dentro de **Business Data Cloud**. La lectura honesta: no es una
  extensión de vida, es un embudo. Y el "Data Product Generator" prometido para
  migrar artefactos BW existentes reedita exactamente el problema del W31 — una
  herramienta que mueve objetos no migra la semántica que vive en el user exit.
- **Por qué ahora:** gancho **débil de calendario** (los anuncios son de meses
  atrás); su valor es de autoridad, no de actualidad. Es el tema donde Ricardo tiene
  la ventaja más grande sobre cualquier otro que escriba de esto.
- **Fuentes (⚠️ TODAS por verificar — SAP Community dio 403 en el fetch):**
  - https://community.sap.com/t5/technology-blog-posts-by-sap/announcement-sap-datasphere-and-sap-analytics-cloud-availability-via-sap/ba-p/14140920
    — anuncio oficial SAP de disponibilidad vía BDC.
  - https://barc.com/end-of-maintenance-sap-bw/ — BARC (analista neutral) sobre fin de
    mantenimiento de BW.
  - https://sapinsider.org/blogs/sap-extends-maintenance-for-sap-netweaver-7-5-and-sap-bw-4hana/
    — la extensión de mantenimiento.
  - Falta: **la nota SAP oficial** con las fechas. No citar fechas sin ella.

## Idea 4 — El 60% que Gartner predijo se cumple este año

- **Formato:** opinión
- **Tesis:** Gartner predijo que "hasta 2026" las organizaciones abandonarían el 60%
  de sus proyectos de IA por falta de datos AI-ready. Estamos en el año del veredicto.
  Los agentes no rompieron nada: exhibieron veinte años de deuda semántica.
- **Por qué ahora:** el ciclo de encuestas de mediados de 2026 está publicando cifras
  de fracaso (88% de pilotos que no llegan a producción, 95% sin impacto medible).
- **Por qué NO esta semana:** el sustento es **de encuesta y de vendor**, justo lo que
  [[feedback-papper-sourcing]] pide evitar cuando hay algo neutral mejor; el dato de
  Gartner es de un press release de **feb-2025** con encuesta de **3T-2024** — viejo y
  ya muy citado. Además canibaliza la Idea 4 del digest W32, que ya se descartó por lo
  mismo. Se deja registrada, no se recomienda.
- **Fuentes:**
  - https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk
    — press release original (26-feb-2025, Roxane Edjlali; encuesta 3T-2024, n=248).

---

## Ranking sugerido

1. **Idea 1 — El examen estaba mal calificado.** La mejor de la semana por mucho.
   Evidencia primaria, académica y neutral; cifras duras y verificables; y es la
   jugada editorial más fuerte disponible: poner el contrapeso a tu propia tesis de
   la semana pasada, con datos. Eso es exactamente lo que construye reputación de
   arquitecto honesto y no de vocero de tendencia. Cierra con la prueba de las tres
   métricas de la edición 05, que pasa de sugerencia a criterio de compra.
2. **Idea 2 — Te movieron la fecha.** Gancho de calendario más fresco (8 días) y
   fuente oficial de primera parte. Buena si prefieres un tema distinto al de la
   semana pasada. Se puede guardar sin perder vigencia hasta W34-W35.
3. **Idea 3 — La decisión de BW.** Máxima autoridad propia, mínimo gancho. Guardarla
   para una semana sin noticia, y solo tras verificar fechas con la nota SAP.
4. **Idea 4 — El 60% de Gartner.** No recomendada; se registra para cerrar el barrido.

## Combinación recomendada

Idea 1 como papper, tomando **de la Idea 2 un solo párrafo** de cierre: si el
regulador te va a pedir en 2027 que demuestres de dónde salió cada número, el
inventario de definiciones que hoy no tienes deja de ser higiene y se vuelve fecha
comprometida. Une el argumento técnico con la consecuencia de negocio sin convertir
el papper en una pieza de compliance.
