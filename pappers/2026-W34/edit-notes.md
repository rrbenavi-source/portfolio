# Notas de edición — Papper W34 / Edición 07

Revisión del agente `papper-editor` sobre `draft-es.md`, 17-ago-2026.
Todas las correcciones marcadas como "Corregido" **ya están aplicadas** en el draft.
Este archivo lo volcó la sesión principal porque el agente no tenía permiso de escritura.

---

## Verificación contra fuente primaria

**Ninguna cifra quedó sin confirmar. No hubo que eliminar ningún número.**

| Cifra | Estado |
|---|---|
| 19% de brecha, 22–25 años (Stanford, rev. ago-2026) | Confirmada |
| 15% en la cosecha de julio de 2025 | Confirmada |
| "No hay desplazamiento generalizado" como hallazgo #1 | Confirmada |
| Caída por menor contratación, no por separaciones | Confirmada |
| Mecanismo conocimiento codificado vs. tácito | Confirmada (redacción casi literal de Stanford) |
| Descriptivo/no causal + brecha se encoge por escolaridad | Confirmadas |
| Stanford controla por trabajo remoto y la divergencia persiste | Confirmada **con matiz** — ver C-3 |
| LSE: 243M contrataciones, 407M vacantes, 4 países, 2017–2025 | Confirmadas |
| LSE: coeficiente GenAI "indistinguible de cero" junto con WFH | Confirmada textualmente |
| Revelio: 27% plantilla; +31% senior / +6% junior | Confirmadas, y **son de Revelio, no de Stanford** |
| Census CES-WP-26-27: 12%, 22–24 años, 10 trimestres | Confirmada (autor: Lee C. Tucker) |
| Fed de Dallas: ≈0.1 pp agregado | Confirmada |
| ETH/CHI: divergencia solo en tareas no familiares | Confirmada |
| Muestra 5 seniors / 10 juniors | Confirmada parcialmente — ver A-2 |

---

## CRÍTICO (4) — todos corregidos

**C-1. "Dos equipos serios, mirando los mismos datos".** Falso: Stanford usa nómina
administrativa de ADP en EE.UU.; la LSE usa contrataciones y publicaciones de vacantes en
cuatro países. → Corregido a **"con datos distintos"**.

**C-2. El 27% de Revelio se presentaba como efecto de la IA.** El propio tracker advierte
que las empresas adoptantes ya crecían más rápido antes de adoptar. Omitirlo convertía una
correlación con selección evidente en efecto causal — justo lo que el papper le exige a
Stanford. → Corregido: la advertencia del proveedor entra en el mismo párrafo.

**C-3. "Stanford responde de frente: controla por la medida de trabajo remoto de ese mismo
estudio".** Sobreafirmado por partida doble: (a) la medida de WFH se atribuye a **Hansen et
al. (2023) y a Lambert & Schindler (2026)**, no solo al segundo; (b) es una prueba de
robustez entre varias, no una réplica dirigida. → Corregido con la atribución completa.

**C-4. No había sección de Fuentes.** Varias cifras quedaban sin rastro. → Corregido: se
agregó `## Fuentes` con seis referencias, URLs y las salvedades metodológicas de cada una.

---

## ALTO (5) — todos corregidos

**A-1. Corroboración sesgada.** Se invocaba a Censo y Fed de Dallas como "apuntan en la
misma dirección" sin dar una cifra, y omitiendo que el hallazgo de Dallas es que el impacto
**agregado** es ≈0.1 pp. Usar a Dallas solo por la parte que confirma es lo contrario a "sin
humo". → Corregido: entran el 12% del Censo y el 0.1 pp de Dallas, cerrando con "Es un
problema de composición, no de volumen."

**A-2. Fecha y atribución del estudio de CHI.** arXiv:2602.00496 es de **febrero** de 2026 y
se presentó en **CHI 2026** (abril). Autores: Dana Feng, Bhada Yun y April Yi Wang — solo
Wang es de ETH Zúrich, así que "un estudio de ETH Zúrich publicado en abril" era doblemente
impreciso. → Corregido a "un estudio cualitativo presentado en abril en la conferencia CHI",
y se explicitó la muestra.
**Decisión pendiente de Ricardo:** si quiere nombrar a ETH de todos modos.

**A-3. Salto lógico en "los seniors de 2031".** La premisa implícita era "nadie está formando
juniors", que el propio 6% de Revelio contradice. → Corregido a un argumento proporcional:
"No es que nadie forme juniors —ese 6% dice que sí—. Es que se forman a una quinta parte del
ritmo al que se contrata experiencia ya hecha."

**A-4. Fecha que envejece mal.** "Hace cinco días" era cierto el 17-ago y falso al publicar el
18. Y la frase seguía con una predicción sin sustento ("la conversación más importante de los
próximos tres años"). → Corregido a "Esta semana apareció un dato…".

**A-5. Afirmaciones absolutas sin respaldo** (estándar de la ed. 06):
- "Revisar enseña más que producir, **y es lo único que ya no se puede delegar**" → eliminada
  la segunda cláusula.
- Título "La mitad de la que **nadie** habla" → "La mitad que falta en la conversación" (el
  propio estudio de CHI habla de eso).

---

## MEDIO (5)

**M-1.** "407 millones de vacantes" → son *publicaciones* de vacantes. Corregido.

**M-2.** "Los equipos de datos no se están achicando": Revelio mide plantilla de **empresas**,
no equipos de datos. → Corregido a "plantillas" en los dos lugares.
**Decisión pendiente de Ricardo:** el mismo tracker reporta que en las ocupaciones más
expuestas —y nombra explícitamente a *data engineers*— la demanda de nuevas contrataciones
cayó **36%** desde nov-2022. Es dato de vendor, pero es el único que aterriza el argumento en
el oficio concreto. ¿Entra o no?

**M-3.** "todos estos estudios son de EE.UU., RU, Canadá y Australia" era impreciso: Stanford,
Censo, Dallas y Revelio son solo EE.UU. → Corregido a "mercados anglosajones —Estados Unidos
casi siempre, más Reino Unido, Canadá y Australia en el caso de la LSE—".

**M-4.** El paper de la LSE circuló en SSRN el 18-may-2026 y como CEP DP 2193 en junio. "En
junio" es defendible; se dejó, con el DP identificado en Fuentes.

**M-5. Jerga, orden de presentación y confidencialidad: cumple.** Cada término técnico se
define en su primera mención; se dice qué se compara antes de dar cifras; no hay cliente,
sociedad ni consultora identificable. La anécdota de los once pesos y la pregunta de la venta
neta no identifican a nadie.

---

## BAJO (4) — corregidos

- "Antes de seguir, la parte que este newsletter está obligado a decir." → eliminada (relleno
  y tono defensivo).
- "Es una advertencia honesta y hay que respetarla" → eliminada (el respeto se demuestra
  citando, no anunciándolo).
- Eco de "las plantillas no se están reduciendo" en el medio y en el cierre → se fusionó la
  primera aparición para que el cierre pegue.
- Reflow de líneas con salto irregular tras las ediciones.

---

## Estructura del argumento

El arco se sostiene: dato → mecanismo → consecuencia de formación → contrapunto → acción.

- **El contrapunto de la LSE está tratado con seriedad**, no como trámite. El movimiento
  fuerte es el párrafo de "la conclusión práctica es la misma en los dos casos": desactiva la
  disputa científica sin fingir que está resuelta.
- **La sección de CHI es la más floja** por peso de evidencia (muestra chica, y sobre
  ingeniería de software, no de datos). Está bien etiquetada como observación de campo. Si hay
  que recortar, es de donde sale el corte con menos daño.

## Extensión

- Antes: ≈1,750 palabras de cuerpo. Después: **≈1,790–1,810** (más ≈300 de Fuentes, que no
  cuentan).
- Se recortaron ~130 palabras de relleno, pero las correcciones CRÍTICAS obligaron a añadir
  ~180 (el 12% del Censo, el 0.1 pp de Dallas, la advertencia de selección de Revelio, la
  precisión del control de WFH). Quedó ~100 palabras arriba del techo de 1,700.
- **Decisión pendiente de Ricardo:** para bajar esas 100 palabras sin dañar el argumento, las
  opciones son comprimir la sección de CHI a dos párrafos, o fusionar los puntos Uno y Dos de
  "Qué hacer el lunes" (comparten la idea de cambiar el tipo de exposición, no la dificultad).
  El editor no lo hizo porque sacrifica contenido, no relleno.

---

# Post-edición — cambios posteriores a la revisión del agente

## 1. Sustitución de la fuente del párrafo bisagra (decisión de Ricardo, 17-ago)

Se descartó incorporar el 36% de Revelio y en su lugar **Indeed Hiring Lab pasa a ser la
fuente principal** del párrafo que sostiene el argumento senior/junior. Razones:

- Es serie pública y reproducible (consultable en FRED, Banco de la Reserva Federal de
  San Luis, serie `IHLIDXUSTPSOFTDEVE`); el dato de Revelio hay que creérselo.
- **Corrobora el reparto senior/junior con datos y metodología independientes**: Indeed
  mide 71% del rebote en plazas senior; Revelio mide +31% senior contra +6% junior. El
  argumento deja de depender de un solo proveedor.
- Nombra explícitamente *análisis de datos* (≈30% por debajo de febrero de 2020), lo que
  aterriza el argumento en el oficio.
- Aporta un reencuadre más honesto y más fuerte: el mercado **no se derrumbó, se está
  recuperando** — pero salteándose el primer escalón. La metáfora del título deja de ser
  adorno.

Se eliminó del cuerpo el "27% más de plantilla" de Revelio, que era el dato con problema
de selección (C-2). Revelio queda como corroboración secundaria, con su etiqueta de
proveedor puesta. Se agregó la entrada de Indeed a `## Fuentes` y se reescribió la de
Revelio.

**Costo de extensión:** +125 palabras. Ricardo decidió **no** aplicar el recorte de la
sección de CHI que proponía el editor. El cuerpo quedó en ≈1,935 palabras, ~235 arriba
del techo de 1,700. Decisión consciente, no descuido.

## 2. Pase de voz (humanizer)

**No existe el agente `papper-humanizer`** que menciona la spec del pipeline: en
`.claude/agents/` solo está `papper-editor`. El pase de voz lo hizo la sesión principal
contra `voice-profile.md`. Fue ligero, porque el borrador ya se escribió en esa voz:

- Se destrabaron dos construcciones telegráficas que dejaron los recortes del editor
  ("Nada de eso me quitó el sueño. Lo que sí: la parte nueva…" y "La consecuencia de
  gestión que no habíamos sacado:").
- Reflow de nueve párrafos con saltos de línea irregulares tras las ediciones.
- Verificados los anti-patrones de `voice-profile.md`: sin aperturas genéricas, sin
  listas mecánicas de tres con adjetivos vacíos, sin conectores de relleno, sin
  conclusiones que reformulan la introducción. Sin jerga regional difícil.

## 3. Versión EN

`draft-en.md` — 1,899 palabras de cuerpo más la sección de Fuentes. Misma voz, no
traducción literal. Título: *We took away the first rung*. Se conservó la anécdota de los
once pesos (contexto mexicano real) y el apunte de que no hay serie equivalente para
México.

## Estado del pipeline

Hecho: draft ES → editor → correcciones → sustitución de fuente → pase de voz → draft EN.
**Pendiente: gate de aprobación de Ricardo**, y después figuras, portada, publicación en
el portfolio y material de LinkedIn.

## 4. Pase de conectores en español de México (17-ago)

Ricardo señaló que los puentes entre párrafos sonaban a español neutro de traducción, no
a español de México. 21 ajustes de conectores y giros: "Lo que comparan es esto" →
"El ejercicio es sencillo"; "Dicho de otro modo" → "Dicho en corto"; "Su argumento va
contra" → "le pega de frente a"; "Lo notable es que, para un líder" → "Y aquí está lo
importante para quien dirige"; "muy fino" → "muy atinado"; "los que conducen de los que
son conducidos" → "el que conduce del que va de pasajero"; "tableros" → "dashboards"
(el perfil de voz pide términos técnicos en inglés). Se agregó el puente que faltaba
antes de la sección del contrapunto, que arrancaba en frío, y se espejeó en el EN.

## 5. Registro ejecutivo y ancla regional (17-ago)

El papper se publica desde Monterrey y lo leen profesionales, varios de ellos CIOs de
multinacionales. Tres cambios:
- **Cierre anclado en el noreste:** buena parte del trabajo de entrada de la región vivió
  en los centros de servicios compartidos que las multinacionales instalaron aquí
  precisamente porque ese trabajo era codificado y documentable. La región se especializó
  en la capa que la IA absorbe primero. Va como observación propia, no como dato — se
  mantiene el "no conozco una serie equivalente para México, y no la voy a inventar".
- **Consecuencia de cadena de proveedores:** la experiencia que se renta (consultor,
  integrador, centro de servicios) sale del mismo embudo. "Esa es una conversación de
  contrato, no de recursos humanos."
- **Quinto punto de acción** para quien firma contratos: preguntar a quién está formando
  el proveedor.

## 6. Ajuste de extensión (17-ago)

Objetivo acordado con Ricardo: **~2,010 palabras** de cuerpo, no las 1,700 originales —
con esta densidad de fuentes y un contrapunto académico tratado en serio, 1,700 obligaba
a sacrificar rigor.

Recortes aplicados, sin perder ninguna idea (solo desarrollo): corroboración de Censo +
Dallas comprimida con cifras intactas; bloque de Indeed de tres párrafos a dos (se fue
el 37% de puestos que mencionan IA en el título, secundario y presente en Fuentes);
descripción metodológica de la LSE; los cinco puntos de acción, una oración menos cada
uno; sección de CHI a dos párrafos; párrafo de proveedores y cierre de Monterrey.

**Resultado: ES 2,029 palabras de cuerpo, EN 2,036.** Ambos ~1% arriba del objetivo.
