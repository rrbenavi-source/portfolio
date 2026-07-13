# Notas de edición — draft-es.md (W29)

Revisión del agente `papper-editor` (2026-07-10). Veredicto: opinión sólida, bien
estructurada y citada. Confidencialidad **limpia** (sin cliente/sociedad/consultoría;
solo objetos SAP estándar públicos).

## CRÍTICO (aplicado)
- **C1 — RFC en "Cloud Private" (L23).** Era incorrecto: en S/4HANA Cloud **Private**
  Edition (PCE/RISE) el RFC / S-API clásico sigue disponible (aunque deprecado); el
  caso sin RFC es **Public** Edition. Corregido y reformulado a enunciado general
  ("en la nube pública, el camino clásico por RFC ya ni siquiera existe").

## IMPORTANTE (aplicado)
- **I1 — Cifras sin fuente (L39).** "de unos cientos en 2019 a varios miles en 2025"
  se leía como estadística citable sin referencia → sustituido por "creció release
  tras release".
- **I2 — Falsa precisión (L129).** "El 80% de los errores caros que he visto" → "La
  mayoría…"; queda como observación de experiencia, no dato.

## MENOR (aplicado por RB)
- **M1 — Precisión NASA.** Se separó el rango: decenas en integración/pruebas, cientos
  en producción (fiel al desglose verificado).
- M2/M3 — sin cambio (retórica de opinión legítima).

## Verificado sin objeción
ODP-CDS reemplaza S-API + `@Analytics.dataExtraction.enabled`; released ≠ extraction-enabled
+ `I_DataExtractionEnabledView`; CDC delta trigger-based; clean core key-user vs developer
extensibility; ACDOCA/Universal Journal + carryforward = documentos de Período 0;
0FI_GL_10 saldos vs 0FI_GL_14 partidas; Horváth 2025 >60% desvíos.
