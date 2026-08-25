# Notas de edición — Papper W35 / Edición 08

Revisión editorial sobre `draft-es.md`, 24-ago-2026, previa a la publicación del martes
25-ago-2026. Todas las correcciones marcadas como **Corregido** ya están aplicadas en el
draft. Respaldo del archivo previo a la edición en el scratchpad de la sesión.

---

## Verificación de fechas — cerrada

Este bloque vivía dentro de `draft-es.md`. Es nota de trabajo, no de publicación: se sacó
del papper y quedó aquí. Ninguna edición previa (W32, W33, W34) publicó un apéndice así.

| Dato | Fuente | Estado |
|---|---|---|
| BW/4HANA 2023 — RTC y GA 30-oct-2023, fin mainstream **31-dic-2030** | PAM (SAP for Me) | Confirmado |
| BPC 2021 for BW/4HANA — RTC y GA 01-nov-2021, fin mainstream **31-dic-2030** | PAM (SAP for Me) | Confirmado |
| **No existe un release "BPC 2023"** | PAM + blog de mantenimiento de BPC | Confirmado |
| Compromiso de 2040 es de **línea de producto**, *"through a sequence of releases"* | Blog oficial de SAP | Confirmado |
| BW 7.5 NetWeaver — fin mainstream 31-dic-2027 | Alineado con Business Suite 7 | Confirmado |
| 20,000–30,000 clientes en BW 7.5 | SAPinsider / Sapphire 2025 | Confirmado (declaración de SAP, no censo) |

Las dos fechas de PAM se verificaron contra el Product Availability Matrix, no contra
blogs. Ese fue el error que la edición corrigió la semana pasada y no debe reaparecer.

---

## CRÍTICO (3) — todos corregidos

**C-1. La sección de ODP se apoyaba en documentación de vendors y quedaba coja.**
El draft decía *"en junio de 2026, según la documentación de los propios vendors afectados,
llegaron los parches"* — una de las dos citas marcadas con ⚠️ para re-verificar. Se
verificó, y el hallazgo es mejor de lo que estaba escrito:

- Nota **3255746** va en **versión 11, del 21-abr-2026**.
- El parche de seguridad de **junio de 2026** valida las llamadas entrantes y **bloquea**
  las de aplicaciones no autorizadas contra **S/4HANA, BW y ECC**.
- Existe un **opt-out temporal que las mantiene vivas solo hasta fin de 2026**.
- Nota **3439624**, publicada el **13-abr-2026**: herramienta de autoevaluación que
  inventaría todo el uso de ODP-RFC en el paisaje.

→ Corregido: la sección se reescribió como subsección propia, **"El único reloj que sí es
tuyo, y vence este año"**, y se amarró al cierre del papper. Es el mejor movimiento
editorial de la edición: el título promete que la fecha en rojo no es tuya, y ahora el
papper entrega la que sí lo es —con número de nota y una acción concreta para esta semana.
La fuente es SAPinsider (publicación de industria, no proveedor), no un vendor de ETL.

⚠️ **Único pendiente vivo:** confirmar el alcance exacto del opt-out en la propia nota
3255746 dentro de SAP for Me antes de comprometerlo con un cliente. Está anotado también
en la sección de Fuentes del papper.

**C-2. Cifras de capacity units sin ancla.** Se daban 25.60 / 10.54 / 72.85 / 820.43 sin
decir que **SAP no publica el precio de una capacity unit**. Sin eso el lector lee moneda
donde hay fichas y estima una factura que no existe. Contradice directamente
[[feedback-papper-jerga]]: presentar lo que se compara antes de dar cifras.
→ Corregido: párrafo de advertencia antes de los números.

**C-3. Cláusula de caducidad citada de una versión distinta a la del resto.** Todo el
análisis contractual sale del Supplement v7-2026, pero la frase *"Unused Capacity Units may
not be carried over"* es de la v10-2025. En un papper cuya tesis es *lee el documento*,
mezclar versiones sin decirlo es el error más caro posible.
→ Corregido: se declara la versión y se pide confirmarla en la que toque firmar.

---

## ALTO (4) — todos corregidos

**A-1. Longitud fuera de rango.** Después de las correcciones el cuerpo llegó a 2,899
palabras. Las ediciones previas corren en 1,595 (W33), 1,961 (W32) y 2,029 (W34).
→ Corregido parcialmente: se comprimieron siete pasajes hasta **2,738 palabras**. Sigue
siendo la edición más larga de Brújula. Es una decisión consciente —carga un análisis
contractual, uno de precio y dos relojes— pero si prefieres volver al rango, el candidato
natural a recortar es **"Lo que sí ganas, dicho sin adorno"**, que puede bajar a dos
bullets sin perder el argumento.

**A-2. Jerga sin definir en primera mención** ([[feedback-papper-jerga]]). Se glosaron:
*lift as-is*, *zero-copy*, *formation*, *control plane* y *campos Z*. Ya estaban bien
glosados desde el draft: *object store*, Parquet, Unity Catalog, PAM y capacity units.

**A-3. "Cuatro años y medio de pista".** De ago-2026 a dic-2030 hay cuatro años y cuatro
meses. Redondear a favor, en un papper que denuncia el redondeo de fechas ajenas, es
exactamente el error que el texto castiga.
→ Corregido a **"cuatro años y cuatro meses"**.

**A-4. El conteo de 259 data products venía de un socio de implementación y de enero.**
Era la segunda cita marcada con ⚠️. El catálogo público de SAP en el Discovery Center no
es consultable sin sesión desde aquí, así que el número no se pudo refrescar.
→ Corregido sin quitarlo: se conserva **fechado y atribuido**, y se remite al lector al
catálogo oficial para que cuente el inventario vigente el día que decida —que además es
mejor consejo que darle un número. Cumple [[feedback-papper-sourcing]]: la fuente neutral
queda como la que manda y la del socio como corroboración fechada.

---

## MEDIO (2)

**M-1. "En enero el reproche más citado…"** sin año, a mitad de un papper lleno de fechas.
→ Corregido a "en enero de 2026".

**M-2. Cierre sin hilo con la subsección nueva.** El papper cerraba en "la parte que
decides tú es el calendario" mientras el texto acababa de entregar un pedazo de calendario
que el lector ya no decide.
→ Corregido: el cierre amarra ODP y diciembre.

---

## Lo que se revisó y quedó como estaba

- **Confidencialidad** ([[feedback-papper-editorial]]): el papper no nombra cliente,
  sociedad ni sistema. El párrafo regional habla de perfil de parque instalado, no de una
  cuenta. Correcto.
- **Ancla regional** ([[feedback-papper-audiencia]]): "Escribo desde Monterrey" y el
  cierre de "decisión de 2028 disfrazada de urgencia de 2026". Es el mejor párrafo del
  papper para el lector que firma presupuesto. Intacto.
- **La inferencia de las Intelligent Applications** (comprar una que tu ERP no puede
  alimentar) está declarada como inferencia propia y no como declaración de SAP. Correcto:
  así se sostiene.
- **§3.3, §1.11, §3.5, §3.6, §2.6.4 y §2.4** se citan textualmente y con número de
  sección. No se tocaron.
- **Voz**: español mexicano hablado con términos técnicos en inglés
  ([[feedback-spanish-mexican-english-terms]]). Consistente en todo el texto.

---

## Fuentes agregadas en esta revisión

- SAP, nota **3439624** — herramienta de autoevaluación de uso de ODP-RFC (13-abr-2026).
- SAPinsider — *SAP Note 3255746: The June 2026 ODP-RFC Deadline Explained*.
- SAP — *SAP BDC Catalog*, Discovery Center (catálogo público de data products).

Y se cerró el ⚠️ de la entrada de la nota 3255746, que ahora cita versión y fecha.
