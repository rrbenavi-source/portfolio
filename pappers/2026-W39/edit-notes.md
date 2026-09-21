# Notas de edición — Papper W39 / Brújula edición 12

**Tema:** ECC + BW 7.3 + BusinessObjects → S/4HANA reportando directo a SAC (live mayoría, import
algunos) con vistas CDS de consumo.
**Título aprobado (21-sep-2026):** «Quitamos BW. El motor se quedó.»
**Tesis:** el motor OLAP de BW sigue ejecutando cada query de SAC, embebido en S/4HANA (2C, InA,
RSRT); y el semantic layer de BO/BEx no desaparece: se reconstruye en CDS (capas 2 y 3, con
anotaciones) o se cuela en cada story.
**Fecha de publicación LinkedIn:** martes **22-sep-2026** (W39, misma semana ISO).

**Alcance del caso (definido por Ricardo):** anónimo. Hechos permitidos: cuadre BO vs SAC (año
histórico, filtros no identificados, redondeo), lógica de negocio en la story (mapeo de CEDIS),
pruebas por RSRT. **No** usar: reparto de esfuerzo, horas, montos, nombre del cliente. Ricardo
pidió incluir cómo construir las capas CDS y las anotaciones necesarias → secciones «Tres capas» y
«Las anotaciones que sí importan».

---

## Figuras planeadas (3, una por beat) — pendientes de render ES/EN 1080×1350

1. `fig-motor` — **«El motor se quedó»**: SAC → InA → transient query `2C…` → analytic engine
   (OLAP) → cubo CDS → tablas de S/4HANA. Al lado, tachado, el camino viejo BO → universo → BW
   → BEx → OLAP. Kicker: *Quitamos BW. El motor se quedó.*
2. `fig-tres-capas` — **«Tres capas, tres responsabilidades»**: dimensión / cubo / query con las
   anotaciones clave de cada una (`#DIMENSION` + representativeKey + text; `#CUBE` + currency/unit
   + DefaultAggregation; `query: true` + AnalyticsDetails). Kicker: *Lo que no anotes aquí, lo vas
   a reescribir en cada story.*
3. `fig-universo` — **«El universo escondido»**: antes (universo BO, query BEx) → después: dos
   destinos posibles, la CDS (una vez) o la story (cada vez). Con los cuatro hallazgos del cuadre.
   Kicker: *El semantic layer no desaparece cuando apagas la herramienta.*

---

## PENDIENTE DE VERIFICACIÓN — antes de publicar

1. **SAP Note 2715030** (features soportados y restricciones del live a S/4HANA) y **2595552**
   (detalles técnicos CDS) — detrás de SAP for Me → **Ricardo**. El draft solo las nombra como
   referencia de la documentación de SAC, no cita su contenido.
2. **KBA 3763590** completa (BO 4.3 EoMM 31-dic-2026): el título es público; confirmar en SAP for
   Me que no cambió. **PAM** para BW 7.3 (fin 2020) y, si se menciona, BI 2025.
3. **KBA 3466290** (blending en optimized mode): el preview cita SAC 2024.8.1 / S/4 2022. El draft
   ya lo acota con "al menos en las versiones que la nota describe". Si Ricardo puede abrir la
   nota, ajustar.
4. **Convención `2C<sqlViewName>`**: aplica a vistas clásicas con `@AbapCatalog.sqlViewName`. Para
   *CDS view entities* (sin SQL view) el nombre del proveedor transitorio se deriva del nombre de la
   entidad; el draft usa vistas clásicas, como en el caso, y no afirma nada sobre entities.
5. Frase citada del validador ("hay filtros que no identificamos…") — es paráfrasis fiel del
   documento interno, sin nombre ni empresa. Confirmar con Ricardo que se puede citar así.

## Extensión
Draft ES: ~2,700 palabras con código (objetivo ≤ 2,900). No recortar en pasadas; si sobra, sacar
la sección «Live o import» a un post aparte.

---

## Pasada `papper-editor` — 21-sep-2026

### CRÍTICO (aplicado)
- **L33 — Analysis for Office no usa InA contra BW.** AO usa BICS por RFC; InA lo usan Design
  Studio, SAC live y las herramientas de BusinessObjects (blog Ishii). Corregido a "Design Studio y
  las herramientas de BusinessObjects para consultar HANA y BW".
- **L60 — confidencialidad.** El nombre de ejemplo del cliente ficticio delataba la industria del
  cliente real. Cambiado a "Comercial del Norte".
- **L184 y L275 — cifras sin fuente.** "el noventa por ciento de las veces" y "el 70 por ciento del
  camino" no están respaldadas en research.md. Sustituidas por "casi siempre" y "la mayor parte del
  camino".
- **L242 — fórmulas del motor en import.** "las fórmulas del motor no viajan: el modelo de SAC las
  tiene que rehacer" no tiene fuente en research.md y el SoW del caso decía lo contrario ("no es
  necesario desarrollar modelos en SAC para el cálculo de indicadores en modelos Import"). Si la
  query se publica con `@OData.publish: true` el servicio OData es analítico y pasa por el motor.
  Clausula eliminada; restaurar solo si Ricardo lo confirma con la Note 2715030 o su experiencia.
- **L249-252 — blending en optimized mode.** El KBA 3466290 (SAC 2024.8) ya no describe el estado
  actual: desde 2024 QRC3 los blended charts con modelos BW live sí están en optimized story (KBA
  3507024; tablas blended planeadas después). Redactado en pasado con la aclaración de que SAP lo ha
  ido habilitando por partes; KBA 3507024 agregado a Fuentes.

### IMPORTANTE (aplicado)
- **L143-144 — nombre en RSRT.** La query en RSRT se busca con el proveedor delante
  (`2CZISALESCUBE/2CZCSALESQ`), como en la UT del caso (`2CZIZTBFILLRCUB/2CZCZTBFILLRATE`). Añadido.
- **L188 — Quick Sizer.** La fuente dice "maximum runtime is expected to be 10 seconds", no habla
  de "query pesada". Quitado el adjetivo.

### IMPORTANTE — resuelto tras la pasada (21-sep, mismo día)
- Aplicado: hedge «la explicación más probable» en el año histórico; códigos genéricos en el mapeo
  (01→Norte, 06→Centro); «agregaciones de excepción» en F8 vs motor; tríadas rotas (3 de 5),
  transición «le duele al CIO» eliminada, subtítulo partido en dos. Sigue pendiente solo la frase
  del validador (confirmar con Ricardo) y las notas de SAP for Me.

### IMPORTANTE (detalle original del editor)
- **L209-214 — causa del año histórico que no cuadra.** El documento de validación solo registra que
  2022 no cuadra; la explicación (datos que BW cargó y que en S/4 "ya no estaban igual") es
  inferencia. Sugerencia: "la explicación más probable es que…" o confirmar con el equipo del caso.
- **L216-218 — códigos literales del mapeo (PT01→MOL, PT06→MTY).** Son valores reales de la story del
  cliente. El argumento no pierde nada con códigos genéricos ("si el puesto es X entonces Monterrey").
  Decidir si se dejan.
- **L203-204 — frase del validador entre comillas.** Ya anotada como pendiente; sigue pendiente.
- **L42-45 — F8 vs motor.** Correcto según blog Reddy. Matiz: la agregación simple sí la empuja el
  motor a HANA; lo que solo resuelve el motor es la semántica (exception aggregation, fórmulas,
  textos, jerarquías). Si se quiere precisión, cambiar "Las agregaciones" por "Las agregaciones de
  excepción". Opcional.

### Verificado, sin cambios
- `@AnalyticsDetails.query.axis` acepta `#ROWS`, `#COLUMNS`, `#FREE`; `.display: #KEY_TEXT` existe.
- `@AnalyticsDetails.query.formula: 'NetAmount / BillingQuantity'` con `0 as AveragePrice` es la
  sintaxis usada en ejemplos publicados para vistas CDS clásicas (con `$projection.` también es
  válida; en analytical projection views es obligatoria junto con `@Aggregation.default: #FORMULA`).
- Resto de anotaciones de los tres bloques (`@VDM.viewType`, `@Analytics.dataCategory`,
  `@ObjectModel.representativeKey`, `@ObjectModel.foreignKey.association`, `@Semantics.*`,
  `@DefaultAggregation`, `@AbapCatalog.sqlViewName`, `@EndUserText.label`): existen y aplican a la
  capa donde se usan.
- Transient query `2C<sqlViewName>`, InA, RSRT, "solo las vistas con `@Analytics.query: true`
  aparecen en live", import = OData sin navegación 1:n: respaldado por SAP Help.
- BW 7.3 (NW 7.3x) fuera de mainstream desde 31-dic-2020; BO 4.3 EoMM 31-dic-2026 (KBA 3763590,
  título público; prensa coincide). "Este año" es correcto a fecha de publicación.
- `#CUBE` = datos factuales con redundancia permitida: SAP Help NW 7.5.
- "de esa hablé en la edición pasada" (dataExtraction/ODP): la ed. 11 trata ODP-RFC. Correcto.

### MENOR (estilo; para `papper-humanizer`)
- Exceso de tríadas en secuencia: L5-7 ("tres sistemas, tres equipos, tres lugares"), L14 ("un solo
  sistema, un solo front, y el ERP"), L181 ("no calcula, no persiste, pide y muestra"), L269-270
  ("es barato, es la herramienta…, y es donde…"), L273-274 ("el motor sigue ahí, el protocolo sigue
  ahí, la transacción sigue ahí"). Cada una funciona sola; juntas suenan a plantilla. Romper dos.
- L138-140 y L222-226: el patrón "si X, se toca Y" y "una vez / cada vez" se repite en dos secciones.
- "Ahora la parte que le duele al CIO" (L195): frase de transición prescindible.
- El subtítulo (L3) tiene 68 palabras; cabría partirlo en dos oraciones.

## Estado 21-sep-2026 (madrugada) — ✅ LISTO PARA PUBLICAR
- Pasada de `papper-editor` hecha y ajustes aplicados; pasada de humanización con registro regio.
- `draft-en.md`, portadas `brujula-cover-12{,-en}.png`, **cuatro figuras** ES/EN (`fig-motor`,
  `fig-tres-capas`, `fig-anotaciones`, `fig-universo`), `brujula-ed12-copypaste-es.md`.
- Publicación 14 en `web/src/i18n/{es,en}.ts` (slug `quitamos-bw-el-motor-se-quedo`), build OK.
- `research.md` queda fuera del repo (`.gitignore`): trae nombres de cliente, horas y montos.
- Pendiente Ricardo: post de LinkedIn martes 22-sep 9:00; notas 2715030/2595552 en SAP for Me.
