# Notas de edición — Papper W38 / Brújula edición 11

**Tema:** ECC + BW 7.5 → S/4HANA, con salida de la analítica de SAP hacia Microsoft Fabric + lago.
Integración: CDS views → replication flows de SAP Datasphere → ADLS Gen2 (Parquet) → OneLake.

**Tesis aprobada (Tesis A, «La aduana»):** desde junio de 2026 la puerta de salida del dato de SAP
es una decisión de arquitectura y de contrato, no de ETL. Quien decide salir de la analítica de
SAP termina comprando un producto de SAP — no como warehouse, sino como aduana; y el peaje se
cobra por gigabyte, cada mes, sin corte técnico.

**Alcance del caso (definido por Ricardo):** solo la **forma** de la arquitectura, anonimizada
(sin cliente, sociedad ni consultoría) — más un hecho real: **las reglas de negocio se rehicieron
a mano y en muchos casos no estaban 100 % documentadas.** Sin volúmenes, sin conteos, sin fases,
sin estado del proyecto.

**Fecha de publicación LinkedIn:** martes **15-sep-2026** (W38, misma semana ISO).

---

## PENDIENTE DE VERIFICACIÓN — bloqueante antes de publicar

Aplica [[feedback-papper-sourcing]]: nada de cifras ni fechas que vengan de un resumen de búsqueda
o de un vendor cuando existe fuente de primera mano.

1. ~~**Notas SAP 3255746 y 3439624 — abrir en SAP for Me.**~~ ✅ **CERRADO el 9-sep-2026.** Ricardo
   descargó las tres notas a `notas_sap/` (PDFs oficiales, 09-sep-2026). Se reemplazó todo lo que
   venía de SAPinsider por texto de la nota, y **SAPinsider salió de las fuentes**. Correcciones
   de hecho que hizo la fuente primaria:
   - La 3255746 va en **versión 12, liberada el 09-jun-2026** — no v11 del 21-abr-2026. Ese dato
     era la foto de SAPinsider y estaba desactualizado. *(Nueva evidencia para
     [[feedback-papper-sourcing]]: la prensa de industria envejece; la nota se mueve.)*
   - **La nota que bloquea es la 3748819** (June 2026 Patch Day), con correcciones de código en la
     **3635619**. Yo había supuesto que la 3731818 era el parche: **la 3731818 es el opt-out**
     (v4, 27-jul-2026, reporte `RODPS_REPL_SECUREACCESS_OPTOUT`).
   - La 3439624 va en **versión 34, liberada el 09-sep-2026** — se actualizó el mismo día.
   - Alcance exacto de la prohibición: sistemas ABAP con **PI_BASIS, SAP BW o SAP BW/4HANA**,
     **on-premise o private cloud**.
   - Alternativas que la nota nombra: **SAP Business Data Cloud** y **la API OData de ODP**.
     **Datasphere NO aparece** — porque no es alternativa para el cliente, es aplicación SAP. Ese
     hallazgo se volvió el párrafo que sostiene la tesis de la aduana.
   - Dos líneas de traslado de responsabilidad que entraron textuales al draft: SAP se reserva
     modificar los módulos sin aviso, y los incidentes son responsabilidad exclusiva del cliente.
   - La 3439624 **audita su propio instrumento**: *"does not provide conclusive results of the
     non-existence of unpermitted calls"*. Aplica el patrón de [[feedback-papper-sourcing]]
     (cuando un estudio audita su instrumento, cítalo — fortalece). Con eso + «no evalúa llamadas
     históricas» nació la sección nueva **«El inventario que todavía no existe»**.
2. **Fechas de mantenimiento de BW 7.5 — PAM en SAP for Me.** El draft dice mainstream **fin de
   2027** y extendido **2030**, citando la página oficial de estrategia de mantenimiento de SAP
   Community. Es primera parte, pero la regla que fijamos en W35 es **PAM, no blog**: cuatro
   líneas (producto, RTC, GA, fin de mantenimiento). Esta consulta la haces tú.
3. **Costo real del bloque de Premium Outbound Integration en Capacity Units.** Circula «500 CU
   por 20 GB» en blogs de consultoría (Expertum, Seapark) y **no lo puse en el draft**. La fuente
   buena es el *SAP Datasphere Capacity Unit Estimator* de SAP:
   https://datasphere-estimator-sac-saceu10.cfapps.eu10.hana.ondemand.com/
   Si sacas la cifra, el párrafo de «El medidor» gana mucho: pasa de mecánica a costo.

---

## Decisiones editoriales tomadas

- **Título «La aduana».** Corto, con gancho, y con ancla regional implícita — es una palabra que
  en el noreste se lee sin traducción. El subtítulo carga la carne del argumento
  ([[feedback-papper-editorial]]: el título engancha, no describe).
- **Jerga definida en primera mención** ([[feedback-papper-jerga]]): BW 7.5, CDS view, ODP,
  ODP-RFC, replication flow, Premium Outbound Integration, Open Mirroring, zero-copy. `CDS_EXTRACTION`
  se menciona como detalle verificable, no como instrucción.
- **La sección «Cuatro puertas y su peaje» presenta las opciones antes de comparar peajes**, según
  la misma regla.
- **Anti-humo:** ningún impacto atribuido al proyecto. El único dato del caso —reglas rehechas a
  mano, sin documentación completa— se presenta como costo, no como logro, y se reencuadra como
  *arqueología*, que es lo que le da credibilidad al cierre.
- **Registro CIO** ([[feedback-papper-audiencia]]): la sección de acciones marca explícitamente que
  las tres primeras son para quien firma el contrato. El ancla regional (noreste / multinacionales
  con SAP) va como observación propia, sin dato inventado.
- **Continuidad de la serie:** se referencia la edición 08 (BW → BDC) al mencionar Business Data
  Cloud, sin repetir su argumento.

## Riesgo editorial a vigilar

El argumento del «segundo peaje» (lo que no viaja: el semantic layer de BW) es lo bastante fuerte
como para haber sido su propia edición — era la Tesis B que descartamos. Está contenido en una
sección y subordinado a la tesis de la aduana. **Si al releer se come el argumento principal, hay
que recortarlo, no ampliarlo**, y guardar el tema completo para una edición futura.

## Producción — estado al 15-sep-2026

- [x] `draft-en.md` — «The customs house»
- [x] Portadas `brujula-cover-11.png` / `-en.png` (1920×1080)
- [x] Tres figuras ES/EN (1080×1350): `fig-camino-del-dato`, `fig-reloj-odp` y `fig-cuatro-puertas`
- [x] Publicación **13** en el portfolio, slug `la-aduana` (ES y EN), con hero + figura
- [x] Build en verde (42 páginas); render verificado a 1280×900 y sin regresión de overflow móvil
      (scrollWidth 485 = 485 contra la publicación 12)
- [x] `brujula-ed11-copypaste-es.md` para el newsletter del martes 15-sep
- [ ] **Publicar en LinkedIn** (paso manual de Ricardo)

## Pendiente que NO bloquea la publicación

- **PAM de BW 7.5.** El texto dice mainstream fin de 2027 / extendido 2030, citando la página
  oficial de estrategia de mantenimiento de SAP Community (primera parte). La regla de W35 pide
  PAM. Si el PAM dice otra cosa, se corrige el párrafo del «segundo peaje» en ES, EN y portfolio.
- **CU por bloque de Premium Outbound Integration.** Sigue fuera del texto a propósito. Si sacas
  la cifra del *Capacity Unit Estimator*, el párrafo de «El medidor» pasa de mecánica a costo —
  es la mejora de mayor impacto pendiente para un lector que firma presupuesto.
