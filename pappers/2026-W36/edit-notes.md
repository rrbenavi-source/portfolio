# Notas de edición — Papper W36 / Edición 09

Revisión editorial sobre `draft-es.md`, 31-ago-2026, previa a la publicación del martes
1-sep-2026. Todas las correcciones marcadas como **Corregido** ya están aplicadas en el
draft. Respaldo previo a la edición en el scratchpad de la sesión.

Contexto: la edición 09 es la segunda mitad de la serie que abrió la edición 08 (*"El reloj
que no es tuyo"*, publicada en LinkedIn el martes 25-ago-2026). Aquella cerró en la
decisión de contrato y precio; ésta responde qué le pasa al reporte cuando la decisión ya
se tomó.

---

## Pendientes ⚠️ que traía el draft — estado

Este bloque vivía dentro de `draft-es.md`. Es nota de trabajo, no de publicación, así que
se sacó del papper y quedó aquí (misma decisión que en la edición 08).

| # | Pendiente | Estado |
|---|---|---|
| a | Versión vigente de la nota **2932647** | **Abierto** — solo tú puedes verlo (SAP for Me) |
| b | Alcance de **Analysis for Office** contra el SP en uso (KBA 3297935 y 2436382) | **Abierto** — solo tú puedes verlo |
| c | Leer completa la **sección 6 del Supplement** (add-ons y modificaciones) | ✅ **Cerrado** — ver abajo |

**Sobre (a):** la nota va en versión 18, del 18-dic-2025, según la transcripción completa
que hiciste en `pappers/2026-W35/SAP_Note_2932647.md`. A la fecha de publicación eso son
más de ocho meses. El papper ya se protege solo —cierra la estación 2 diciendo que la lista
de hoy no va a ser la de tu proyecto—, así que la verificación no bloquea la publicación,
pero sí bloquea comprometer la lista con un cliente.

**Sobre (b):** el papper cita la KBA 3297935 y la matriz de conexiones 2436382. La
afirmación publicada —Analysis for Office alcanza vistas y perspectivas de Datasphere pero
no modelos analíticos— está sostenida por esas dos fuentes. Lo que falta verificar es si tu
SP concreto ya lo cambió. Riesgo bajo para publicar, alto para prometer.

---

## CRÍTICO (1) — corregido

**C-1. La estación 6 especulaba sobre un documento que sí se podía leer.**
El draft decía que el Supplement *"define con cuidado Add-on, Additional Add-on, Customer
ABAP Add-on y Modification"* y que *"que esas definiciones existan significa que hay
reglas"*. Escribir "significa que hay reglas" sobre un documento público, sin leerlo, es
justamente el pecado que el papper le reprocha a los demás. El PDF v7-2026 está en el Trust
Center, sin registro; se descargó y se extrajo completo (13 páginas).

Lo que dice es más fuerte, y además desmiente la ubicación:

- Las definiciones **no están en la sección 6**, están en la **1**: Add-on §1.1, Customer
  ABAP Add-on §1.7, Modification §1.9, SAP-provided Add-on §1.10.
- **§1.1 vs §1.9 es la línea que importa.** Un Add-on agrega funcionalidad nueva e
  independiente *sin modificar* la funcionalidad SAP existente. Una Modification es un
  cambio al código o metadatos entregados, o cualquier desarrollo que personalice o altere
  funcionalidad existente. Script logic, BAdIs, exits y buena parte de los Z de BPC caen del
  lado de Modification.
- **§6.7.2 enumera** los servicios donde el cliente tiene derecho a desarrollar y usar
  Modifications: las cuatro variantes de S/4HANA Cloud private edition. Los *BW Capacity
  Services* **no están en esa lista**. Para BW, el §6.7.1 concede Customer ABAP Add-ons.
- **§6.7.2** también: el SLA y el Support Schedule **no aplican** a los Customer ABAP
  Add-ons; el cliente responde por instalación, soporte, compatibilidad y vulnerabilidades.
- **§6.7.2 (iv):** SAP se reserva restringir o exigir la remoción de cualquier Add-on o
  Modification que *"enable the extraction of Data Products to non-SAP applications through
  any means not authorized via SAP"*.
- **§6.7.4:** la propiedad intelectual de **toda Modification** es de SAP. (Los Customer
  ABAP Add-ons quedan del cliente por §6.7.3, pero no se pueden comercializar.)
- **§6.10.2:** los checks de simplificación e incompatibilidad en cada upgrade los ejecuta
  el cliente.

→ Corregido: la estación 6 se reescribió con las citas por sección. La pregunta que el
papper le pide al lector dejó de ser "lee esa sección" y pasó a ser una pregunta concreta y
por escrito: *¿mis desarrollos actuales alrededor de BPC siguen siendo admisibles dentro
del BW en la nube de SAP, y bajo qué figura?* Se marca explícitamente que la redacción de
§6.7.2 es ambigua —el documento usa *BW Capacity Services* de forma elástica— para no
sobrevender el hallazgo.

---

## ALTO (2) — corregidos

**A-1. La frontera contractual mezclaba dos documentos y dos alcances distintos.**
El draft citaba *"Use of OData APIs for data extraction is prohibited"* y el tope de 2,000
llamadas por GB atribuyéndolos a "el Supplement, sección 5.5", pero esas cláusulas son de
la **versión 10-2025** y gobiernan el **consumo de Datasphere**. En la v7-2026 la sección
5.5 no existe con ese contenido y la numeración es otra. En un papper cuya tesis es *lee el
documento*, citar mal el documento es descalificante — es la misma corrección C-3 que hubo
que hacer en la edición 08.

→ Corregido: la estación 4 ahora separa **dos puertas con dos reglas**:
1. *Sacar datos de Datasphere* → términos de esa capacidad (v10-2025): OData prohibido para
   extracción, tope de 2,000 llamadas por GB de memoria por tenant al mes.
2. *Sacar datos del BW en la nube de SAP* → **§6.2.5 del v7-2026**, dentro del apartado de
   la HANA runtime edition: *"Customer is expressly prohibited from performing the mass
   extraction of any data"*, salvo con herramientas SAP licenciadas y **hacia seis destinos
   enumerados** (HANA enterprise, HANA standard, HANA service de SAP Cloud Platform, HANA
   Cloud, HANA EE Cloud, Datasphere). Los seis son SAP.

Ese segundo hallazgo es mejor que el que había: es del documento vigente, es más duro, y la
lista cerrada de seis destinos es el dato que un director entiende de inmediato.

**A-2. La fecha de BDC Connect for Fabric quedaba vieja el día de la publicación.**
El draft decía *"disponibilidad general planeada para el tercer trimestre de 2026"*. Se
publica el 1-sep-2026: ese trimestre es el que está corriendo y cierra en septiembre. Leído
así, suena a futuro lejano cuando en realidad vence en cuatro semanas.
→ Verificado (SAP News, blog de Microsoft Fabric, comunidad Fabric): sigue como **planeada
para Q3 2026**, anunciada en Ignite, sin GA confirmada. Corregido: el papper ahora dice que
es el trimestre en curso y que al momento de escribir sigue siendo promesa con calendario,
y pide **la fecha por escrito**.

---

## MEDIO (2) — corregidos

**M-1. Absoluto sin fuente.** *"Ese objeto, o uno igualito, existe en **todos** los BW de
manufactura y consumo masivo del país."* No hay censo que lo respalde y el diminutivo baja
el registro por debajo del perfil de voz.
→ Corregido: *"o uno casi idéntico, existe en prácticamente todos"*.

**M-2. Jerga sin definir en primera mención.** Regla de
[[feedback-papper-jerga]]: **CompositeProvider** aparecía en el párrafo del ejemplo —el más
importante del papper, el que tiene que entender quien firma— sin una sola palabra de
contexto.
→ Corregido: glosa en línea, *"el objeto de BW que junta varias fuentes en una sola vista
para reportar"*. El resto de los términos densos (analytic model, fact view, Data Access
Controls, delta share) sí llegan explicados por contexto en su propio párrafo.

---

## Verificaciones que se corrieron y salieron limpias

| Dato | Contra qué se verificó | Resultado |
|---|---|---|
| Los 4 bloqueantes duros del Model Transfer | Transcripción íntegra de la nota 2932647, secciones 7.2 y 8.1 | Exactos |
| *"Solo pueden transferirse queries sobre un CompositeProvider (HCPR)"* | Nota 2932647, texto original en inglés | Textual |
| Regla de omisión silenciosa (*"simply skipped and removed"*) | Nota 2932647 | Textual |
| Desconexión por diseño del modelo transferido | Nota 2932647 | Textual |
| Query Template Generator publicado el 30-jul-2026 | Verificado en la edición 08 | Se mantiene |
| BDC Connect for Fabric — GA planeada Q3 2026 | SAP News, Microsoft Fabric blog | Confirmado, sigue sin GA |

---

## Extensión — decisión tomada

Cuerpo de **3,020 palabras**, la edición más larga hasta hoy (ed. 08: 2,738; rango normal de
Brújula: 1,595–2,029). Se propuso un recorte medido de ~220 palabras y Ricardo eligió
publicarla completa: el material contractual nuevo es de fuente primaria y ninguna de las
piezas se repite con la edición 08. **No es precedente**, igual que no lo fue la ed. 08.

---

## Material verificado que NO entró y conviene guardar

- **§6.8, Customer Data Return.** Al terminar la suscripción SAP entrega un export final, y
  el cliente tiene **dos semanas** para verificar que es usable; si no lo hace, *"the
  exported Customer Data shall be deemed usable"*. Es una cláusula de salida excelente, pero
  pertenece al territorio de la edición 08 (el contrato), no al de ésta (el viaje del
  número). Guardada para asesoría a clientes o para una edición futura sobre exit strategy.
- **§6.10.1 y §6.10.3.** El cliente debe mantener el sistema en una release cubierta por
  mainstream maintenance; si no, SAP no responde por fiabilidad, desempeño, disponibilidad,
  funcionalidad ni seguridad. Amarra directo con la tesis de los relojes de la edición 08.
- **§6.7.5.** No se puede usar ningún otro software provisto por el cliente dentro de los BW
  Capacity Services, **incluido a nivel de sistema operativo**.
- **§6.10.5, Point of Demarcation.** La responsabilidad de SAP termina en su firewall de
  salida. Es el respaldo contractual del punto de la estación 1 sobre dimensionar el enlace.
