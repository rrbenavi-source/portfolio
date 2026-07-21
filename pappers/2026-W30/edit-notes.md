# Edit-notes — Papper W30 "El near real time que el lakehouse no te iba a dar"

Revisión del agente `papper-editor` sobre `draft-es-nrt.md` (Fase 2).

**Veredicto general:** draft sólido, bien estructurado y honesto (cumple el
anti-humo). **Sin errores factuales duros (CRÍTICO).** Afirmaciones técnicas SAP
correctas; tesis bien acotada (no cae en "Databricks no puede hacer tiempo real").
Hallazgos son de integridad de cita (IMPORTANTE) y precisión/estilo (MENOR).

## Verificación del dato externo clave (MIT CISR)
Verificado por búsqueda web. El estudio de Peter Weill (MIT CISR) con Insight
Partners (~260 empresas) reporta que el cuartil superior tuvo **62% más
crecimiento de ingresos y 97% más margen de utilidad**; la difusión también usa
"**más de 50%**". El "+50%" del draft es **correcto, conservador y bien atribuido
como dato de industria**. Opción: usar la cifra fuerte (62%/97%) para más impacto.

## CRÍTICO
- Ninguno. No hay afirmaciones de resultado medido del proyecto. El AS-IS (3
  cortes/día, ~15 h-persona/sem, manual, datos viejos) se presenta como punto de
  partida. El +50% queda explícitamente atribuido como externo. El cierre separa
  "capacidad entregada" de "facturación por medir". Cumple anti-humo.

## IMPORTANTE
1. **[APLICADO por el editor] Cita SAP presentada como textual.** La lista de
   beneficios de la Live Data Connection entre comillas era un paráfrasis
   compuesto/traducido, no verbatim. Corregido a paráfrasis atribuida ("la
   documentación oficial de SAP describe la Live Data Connection en esos mismos
   términos —…"), conservando sustancia y voz.
2. **[DECISIÓN DE RICARDO] Comillas en fuentes traducidas.** El mismo patrón
   (comillas alrededor de traducciones) aparece en Coalesce, Beyond Zero Copy,
   cirqlone, AtScale/TechTarget y Business Model Analyst. Convención común de cita
   traducida, no incorrecta. Para blindar autoridad: reservar comillas solo para
   verbatim corto y parafrasear el resto, o confirmar fidelidad al original.
3. **[DECISIÓN DE RICARDO] Título vs. tesis.** El título ("el lakehouse no te iba
   a dar") roza el over-claim que la propia pieza desmonta; el cuerpo lo resuelve
   en el 2.º párrafo, así que funciona como hook de opinión. El subtítulo ya
   matiza ("no siempre pertenece al data lake").

## MENOR
1. **[APLICADO] Precisión ODP/queued delta/EOIO.** *Queued delta* es el modo de
   actualización del extractor LO (cola LBWQ + job V3, lo que evita golpear el
   transaccional); *EOIO* es la garantía de serialización de la entrega ODP al
   suscriptor. La frase original los fundía. Tensada para separar ambos hechos.
2. ADSO change log (inbound→active colapsa deltas): correcto. Sin cambio.
3. Streaming Process Chains como reemplazo de RDA: correcto. Sin cambio.
4. Data gravity / McCrory 2010: atribución correcta. Sin cambio.
5. AY/LY "364 días" = alineación por día de semana: consistente. Sin cambio.

## CONFIDENCIALIDAD
1. **Sin filtraciones duras.** No hay cliente, sociedad, consultoría, persona ni
   transacción Z propietaria. Términos SAP genéricos usados correctamente.
2. **[DECISIÓN DE RICARDO] Asimetría de marcas.** El cuerpo nombra "Databricks"
   pero anonimiza la herramienta de BI como "la herramienta de BI corporativa"
   (en vez de Power BI). Ninguno identifica al cliente y "Databricks" funciona
   como categoría/stand-in del lake, central a la retórica ("no es SAP vs.
   Databricks"). Recomendación del editor: aceptable dejarlo. Alternativa estricta:
   generalizar Databricks a "un lakehouse / motor abierto" en las tres menciones.

## Fuentes de verificación
- MIT CISR / MIT Sloan press: 62% más ingresos, 97% más margen.
  https://mitsloan.mit.edu/press/new-mit-cisr-research-reports-leading-real-time-businesses-had-62-higher-revenue-and-97-higher-profit-margins
- MIT CISR — How Real-Time Businesses Outperform. https://cisr.mit.edu/content/how-real-time-businesses-outperform
