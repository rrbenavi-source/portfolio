# Notas de edición — Papper W41 / Brújula edición 14

**Título:** «De la sábana al agente»
**Tesis:** ocho generaciones de reporting, producto por producto (qué análisis permite cada una y qué
no). La NLQ de primera generación se retiró (Q&A → feb-2027, Ask Data → feb-2024, Search to Insight →
Q4 2024). La tarea de curar el vocabulario reaparece en Prep data for AI, Genie y Cortex Analyst.
**Pasada de `papper-editor`:** 8-oct-2026, rigor y recorte en una sola revisión.
**Extensión (`wc -w`, cuerpo sin Fuentes):** 2,711 → **2,505** (2,476 sin los separadores de la tabla).
El objetivo era ~2,300.

## Críticos: errores de hecho (corregidos en el draft)

1. **Copilot desde F2.** El texto decía «desde este año»; Microsoft lo abrió el 30-abr-2025 (Fabric
   Updates Blog). Ahora dice «desde abril de 2025».
2. **Patente 5,555,403.** La solicitud se presentó en 1991 y la patente se otorgó en 1996. Ya venció,
   así que el texto ahora dice «Business Objects —hoy parte de SAP— solicitó…» y no que la patente
   pertenece a SAP.
3. **«Q&A Setup en 2013».** Esa herramienta llegó después de 2013, así que se quitó el año.
4. **Spider 2.0.** El 21.3 % se midió sobre los 632 problemas originales. El 96.7 % y el 76.2 % son de
   las variantes que hoy mantiene el leaderboard, con resultados que reportan los propios equipos.
   El texto ahora lo aclara.
5. **CIDR 2026.** El «hasta 31 %» es un cambio relativo (de −3 % a +31 %). El equipo es de UIUC
   (Daniel Kang) y la conferencia fue del 18 al 21 de enero de 2026.
6. **Fechas de Q&A.** El anuncio fue en dic-2025 (blog *Deprecating Power BI Q&A*). El MC1218421 es un
   aviso posterior. «Extendió dos meses» se cambió por «lo movió a febrero».
7. **«Menos de tres años»** no cuadraba con las fechas. Ahora dice «Entre 2024 y 2027…».
8. **Essbase (1992)** es anterior al documento de Codd de 1993. Ahora dice «A esa familia pertenecen…».
9. **«Por eso se retiraron»** atribuía una causa que los fabricantes no documentan. Ahora dice «La
   idea no era mala; el método no escalaba».
10. **«Batallan» (Snowflake)** era un regionalismo. Ahora dice «tienen dificultades» (*struggle*).

**Verificado sin cambios:** Codd 1993; Excel 5 PivotTable 1993; Lotus Improv 1991; information
centers de IBM (Carr 1987); Spider 2.0 (632, 21.3 %, 91.2 %); Gartner de may/mar-2026 (sin el «60 %
solo-MCP»); Genie GA 12-jun-2025; Snowflake GA 4-nov-2025; Copilot standalone no disponible en la
región de México; Joule con contexto conversacional (SAP Learning).

## Estructura y fuentes

- Se quitó la cifra del preview de Power BI (500,000 usuarios).
- Se agregaron tres fuentes: el blog *Deprecating Power BI Q&A*, el blog de Fabric sobre F2 y SAP
  Learning sobre Joule.
- Se definieron en su primera mención: benchmark, text-to-SQL, leaderboard, ad hoc, LookML, DAX,
  semantic views, capa de métricas, Gemini y readiness.
- Genie: la doc de sep-2026 dice «Genie Agent», así que el texto ahora dice «agente de Genie».

## Pendientes de decisión (Ricardo)

1. ✅ «Más de veinte años»: confirmado por Ricardo.
2. ✅ «Palomita» → «sello de certificado» (decisión de Ricardo, 9-oct).
3. «Le decimos sábana… en México» se dejó porque es el gancho del título.
4. ✅ Extensión: se queda en ~2,500 (decisión de Ricardo, 9-oct). No hay más recorte.
5. Deep Research de Genie queda como «anunció», porque no se confirmó que esté en GA.
6. SAP readiness: la página de help.sap.com no cargó; abrirla antes de publicar.

## Figuras planeadas (3) — pendientes de render ES/EN 1080×1350

1. Escalera de 8 generaciones: producto, tipo de análisis y lo que no permite.
2. Línea de tiempo de la NLQ retirada: Q&A 2013→2027, Ask Data 2019→2024, Search to Insight→2024.
3. Figura con código: la misma pregunta en SQL / MDX / DAX / verified query.
