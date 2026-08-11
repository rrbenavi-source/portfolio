# Edit notes — W33 / Edición 06

Pasada del agente `papper-editor` sobre `draft-es.md`, 10-ago-2026.
**1 CRÍTICO · 5 IMPORTANTE · 7 MENOR.** Título intacto.
Sin "plomería"/"plomeo" en ninguna parte (verificado con grep). Confidencialidad limpia.

> ⚠️ **El objetivo de longitud NO se cumplió.** El editor reportó ~1,455 palabras, pero
> la medición real da **1,706** — el cuerpo *subió* 76 palabras respecto a las 1,630
> originales, no bajó. Las definiciones agregadas pesaron bastante más de lo que la
> tabla de recortes estima. **Falta una pasada de recorte real de ~200-350 palabras**
> para llegar al formato opinión (2-3 páginas). Es el mismo defecto que se marcó en la
> edición 05, así que conviene no dejarlo pasar otra vez.

---

## CRÍTICO — resuelto

### 1. Misatribución de DORA: el párrafo entero era falso

El draft decía *"el reporte DORA de Google, sobre telemetría de unos 22,000
desarrolladores… Lo llaman acceleration whiplash"*. **Falso, y por partida doble:**

- La telemetría de ~22,000 desarrolladores (4,000+ equipos), el término
  *acceleration whiplash* y las cifras +54% / +242.7% / +441% / 31% son del
  **AI Engineering Report 2026: The Acceleration Whiplash, de Faros AI** — un
  **vendor** de analítica de ingeniería.
- El **DORA 2025** (*State of AI-assisted Software Development*, sept-2025) es una
  **encuesta de ~5,000 profesionales**, no telemetría, y su tesis es **distinta**: la
  IA *amplifica* las fortalezas y disfunciones que ya tenías. El propio reporte de
  Faros marca que sus datos **contradicen** a DORA en ese punto.

No era "cifras de análisis secundario de DORA": era **otro estudio atribuido a DORA**,
con la tesis del estudio real invertida. **Párrafo eliminado del cuerpo** y entrada de
DORA eliminada de fuentes (−78 palabras). No se suavizó ni se inventaron números.

**Origen del error:** vino del barrido inicial, donde una fuente secundaria mezcló
ambos reportes. Lección para el pipeline: cuando una cifra llega vía resumen de
búsqueda y no vía la fuente, **no se escribe hasta abrir la fuente** — aunque el
número "suene" correcto.

**⏳ Decisión de Ricardo.** Versión correcta si se quiere el respaldo cross-domain,
con disclosure de vendor al estilo GitClear (+66 palabras, dejaría el cuerpo en ~1,545,
apenas arriba del rango):

> No es un problema exclusivo de datos. Faros AI —que vende analítica de ingeniería, y
> cuyo dato juega en contra de lo que le convendría vender— midió dos años de
> telemetría de 22,000 desarrolladores y encontró el mismo patrón: más entregas por
> persona, y al mismo tiempo más bugs, más incidentes por pull request y más cambios
> integrados sin que nadie los revise. Lo llaman *acceleration whiplash*: la ganancia
> arriba, el costo compuesto en cada capa de abajo.

Si se inserta, compensar quitando "Es el mejor uso que le he encontrado" o el segundo
párrafo de "Dónde vive esto en un shop SAP".

---

## IMPORTANTE

### 2. Posible doble conteo entre el 32.5% y la auditoría — ✅ RESUELTO
El editor marcó el único punto donde el rigor quedaba expuesto: ¿el 32.51% ya
incorpora las correcciones al examen, o la sección de la auditoría está restando dos
veces? **Verificado contra ELT-Bench-Verified: el 32.51% ES el número corregido.** El
mismo agente (SWE-Agent + Claude Sonnet 4.5) obtenía **22.66%** con la calificación
original y **32.51%** con la corregida — 46/203 modelos contra 66/203.

Aplicado al draft como párrafo propio en la sección de la auditoría. El argumento sale
**más fuerte**: casi diez puntos de diferencia que no venían del modelo sino de los
errores del examen.

### 3. Continuidad con la edición 04 — era inexacta (aplicado)
El draft decía *"Leer 300 reportes Z ajenos… Es exactamente el trabajo que describí en
la edición 04."* La edición 04 (W31, *"Migrar un reporte Z no es traducir ABAP: es una
autopsia"*) describe la autopsia de **un solo** reporte de casi 3,000 líneas; el "300
reportes Z" viene del portafolio, no de esa edición. Corregido a: *"Es, a escala, el
trabajo que describí en la edición 04: la autopsia de un solo reporte Z."*
La continuidad con la **edición 02** ("el diseño es la migración") sí es exacta —
verificada contra W29.

### 4. Salto de benchmark a operación real, sin puente (aplicado)
El draft pasaba de un resultado de laboratorio a "si tu trabajo consiste en mantener
esas conexiones…" y cerraba con "la extracción y la carga ya no son tu trabajo".
Agregado: *"Es un examen controlado y no tu operación —ahí las fuentes están más
sucias—, pero la dirección del dato es inequívoca."* Blinda el cierre.

### 5. "Tres veces más rápido" era una inferencia indebida (aplicado)
72% y 24% son **prioridades declaradas**, no velocidades medidas. Corregido a *"Se está
priorizando la creación tres veces más que el control."* También: "ocho de cada diez" →
"casi ocho de cada diez **líderes**", porque el 77% es solo de líderes y el 71% es del
total.

### 6. Rango 96–98% sin explicar (aplicado)
Quedaba como incertidumbre. Agregado: *"El rango de arriba no es incertidumbre: son dos
agentes distintos con el mismo modelo, y el más simple de los dos fue el que sacó
98%."* Exacto (SWE-Agent 96%, baseline ReAct 98%) y mete un dato incómodo y bueno.

---

## MENOR (aplicados)

7. "Ese contraste es el **papper** entero" → "el **argumento** entero". Ninguna edición
   publicada usa "papper" en el cuerpo.
8. "Claude 3.7 Sonnet con razonamiento extendido" → "**Spider-Agent con** Claude 3.7
   Sonnet y razonamiento extendido". El 57% es del arnés, no del modelo suelto.
9. El 82.7% anclado explícitamente a **las 81** tareas de transformación fallidas.
10. **Escala del 57.8%:** agregado que las 30 columnas son **el 1.2% del total**. Sin
    ese dato, quien abra el PDF puede acusar de inflar el hallazgo; con él, el
    argumento sigue intacto. También "Cuando pusieron a varios expertos…" → "Puestos a
    interpretar la misma especificación, los expertos coincidieron…", que es lo que la
    fuente sostiene sin extrapolar a todas las columnas.
11. **Atribución del costo:** los $343 son de la corrida de ELT-Bench-**Verified**
    (2026), no de ELT-Bench 2025, que reporta $4.30 por pipeline. Corregido.
12. **Definiciones agregadas en primera mención** (regla de [[feedback-papper-jerga]]):
    `pipeline`, `data model`, `user exit`, `extractor`, `benchmark`, `alucinadas`,
    `stakeholders`, `linaje`, `gate de control`. Ya estaban bien definidos: ELT, agente
    de IA, ground truth. `throughput` desapareció con el párrafo eliminado.

---

## Cifras verificadas (todas cuadran contra fuente primaria)

100 pipelines · 835 tablas fuente · 203 data models · 57% y 3.9% · 96% / 98% / 32.51%
(y 22.66% pre-corrección) · 82.7% de 81 tareas · 33% de desajustes a nivel columna ·
30 columnas = 1.2%, acuerdo entre expertos 57.8% · ~$343 y 2d 7h · $4.30 y 89.3 pasos
por pipeline · dbt n=363 con 72/24/71/77 · "dieciséis meses" (abr-2025 → ago-2026) ·
"se multiplicó por ocho" (8.3×) · "cuatro de cada diez" → "una de cada treinta"
(43% → 2–4%) · "dos de cada tres" (67.5%).

## Recortes

| Recorte | Palabras |
|---|---|
| Párrafo DORA + entrada de fuentes | −78 |
| Compresión del párrafo de la curva | −14 |
| Transición de relleno ("Aquí es donde el estudio se pone verdaderamente interesante…") | −11 |
| "dos frases que valen más que cualquier lista de herramientas" → "dos reglas" | −9 |
| Compresiones menores | −18 |
| Definiciones y precisiones agregadas | +48 |
| Párrafo del 22.66% (resolución del punto 2) | +25 |

---

## Decisiones de Ricardo (11-ago-2026) — aplicadas

1. **Faros AI: fuera.** No se reinserta el párrafo de respaldo del mundo del software.
   La pieza se sostiene sola sobre ELT-Bench, ELT-Bench-Verified y dbt. Se eliminó
   también la "Nota de verificación" del pie del draft — era andamiaje de proceso, y
   el registro del fact-check vive aquí. **El papper ya no cita DORA ni Faros.**
2. **"Con la regulación que viene deja de ser higiene y se vuelve fecha comprometida":
   fuera.** Era la única afirmación sin fuente del papper.
3. **Se conserva** el tercer uso: *"El linaje —de dónde viene cada número y por dónde
   pasó— y la documentación que nadie escribió."* Queda como afirmación limpia, sin la
   cláusula regulatoria.

## ⏳ Pendientes de criterio de Ricardo

1. **"Conviene que lo sepas por un estudio y no por un presupuesto que no te
   aprobaron."** Veredicto del editor: no cruza la línea —apunta al interés del lector,
   no a su competencia— pero una parte de la audiencia **vive** de construir esas
   conexiones y va a leerlo como amenaza. Alternativa medio grado más suave sin perder
   filo: *"conviene enterarte por un estudio y no por una renovación de contrato"*.
2. **Longitud:** falta la pasada de recorte (ver aviso arriba).
3. **Dato desaprovechado (opcional, ~20 palabras):** **Tengjun Jin firma los dos
   papers** — ELT-Bench y ELT-Bench-Verified. Gente que audita su propio instrumento y
   publica que subestimaba a los agentes. Es el estándar de rigor que le pedimos a un
   proyecto de datos, y le daría autoridad extra a la sección de la auditoría.

## Veredictos que el editor cerró (no requieren decisión)

- **Cierre** (*"La extracción y la carga ya no son tu trabajo. Empieza a comportarte
  como si eso fuera cierto."*): funciona, es lo mejor de la pieza. Era demasiado
  absoluto solo porque nada lo matizaba antes; con el puente del punto 4 ya se
  sostiene. **No tocar.**
- **Colocación del 57.8%:** bien colocado — llega después de que el lector aceptó el
  32.5%, y la triple frase corta *"Léelo otra vez. Expertos. Con la definición escrita
  enfrente."* le da el peso que merece. La estructura
  **57%/3.9% → 96%/32.5% → por qué → 57.8% → dónde vive en SAP → la factura → dónde sí
  paga → regla** no tiene saltos lógicos y el título la sostiene.
