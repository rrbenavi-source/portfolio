# Outreach Marco Quintanar — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Producir los cuatro entregables de documentación que permiten a Ricardo
escribirle en frío a Marco Quintanar (Director DS/AI Eng, Honeywell) y sostener la
conversación hasta una llamada de descubrimiento.

**Arquitectura:** Cuatro documentos en cascada. El dossier es la fuente de verdad;
de él se derivan los mensajes, el one-pager y el guión. Se construye en ese orden
porque cada uno consume decisiones del anterior. Nada se envía: este plan produce
documentos, el envío lo ejecuta Ricardo.

**Formato:** Markdown plano. Sin build, sin dependencias, sin tooling.

**Spec:** `docs/superpowers/specs/2026-07-27-outreach-marco-quintanar-design.md`

## Global Constraints

Estas reglas aplican a **todos** los entregables. Copiadas literalmente del spec.

- **Idioma:** español mexicano hablado, con términos técnicos en inglés sin
  traducir (`AI-Ready data`, `production-grade`, `Data Products`, `lakehouse`,
  `Unity Catalog`). Nunca español peninsular ni inglés corporativo.
- **Tesis única (§5):** "el techo de madurez lo pone la fuente, no el destino".
  Siempre formulada como **patrón observado en industriales**, jamás como
  diagnóstico de Honeywell.
- **Niveles de confianza (§8.1):** toda afirmación sobre Honeywell se etiqueta
  `Confirmado` / `Inferido` / `Especulativo`. Prohibido afirmar sin etiqueta.
- **Caso Heineken (§9.1):** se presenta como **experiencia operativa propia**
  ("la operación que dirijo"), nunca como portafolio de cliente. No aparece en el
  Mensaje 1.
- **Cartera restante** (FEMSA, CEMEX, Metalsa, Deacero, Copamex, Nemak): solo como
  trayectoria de la firma. **Prohibido inventarles casos, cifras o resultados.**
- **Fábrica de Datos:** equipo en pool que recibe requerimiento y responde por
  integridad, calidad y consumo por uso. Siempre distinguida explícitamente de
  staffing. **No se menciona en el Mensaje 1.**
- **Cifras verificables únicamente:** −50% licenciamiento, 300+ reportes, ~15
  personas, €1.5M (€1.4M directos + €100k evitados). Ninguna otra cifra de impacto.
- **Nada se envía.** Ningún task incluye mandar mensajes ni abrir LinkedIn.

**Directorio base:** `outreach/marco-quintanar/`

---

## File Structure

| Archivo | Responsabilidad |
|---|---|
| `outreach/marco-quintanar/dossier.md` | Fuente de verdad: perfil, dolor con confianza, vocabulario, objeciones, ruta de compra |
| `outreach/marco-quintanar/mensajes.md` | M1 + 2 variantes + M2 por rama + nota de reactivación |
| `outreach/marco-quintanar/one-pager-honeywell.md` | Una página, se envía solo si él lo pide |
| `outreach/marco-quintanar/guion-llamada.md` | Descubrimiento, señales de compra, aterrizaje en alcance |
| `outreach/README.md` | Índice del directorio y regla de uso |

**Orden obligatorio:** Task 1 → 2 → 3 → 4 → 5. El dossier alimenta a los demás.

---

### Task 1: Dossier de cuenta

**Files:**
- Create: `outreach/marco-quintanar/dossier.md`
- Source: `docs/superpowers/specs/2026-07-27-outreach-marco-quintanar-design.md` §2, §3, §4

**Interfaces:**
- Consumes: nada (primer task).
- Produces: los nueve bloques que los tasks 2–4 citan por número. En particular el
  **bloque 5 (vocabulario)** y el **bloque 7 (objeciones)**, que se reutilizan
  literalmente en mensajes y guión.

- [ ] **Step 1: Crear el archivo con los bloques 1–3**

Bloque 1 (identidad), 2 (stack declarado), 3 (trayectoria) se transcriben de las
tablas del spec §2.1–2.3. Sin reinterpretar: son datos verificados de LinkedIn
consultado 2026-07-27.

- [ ] **Step 2: Escribir el bloque 4 — mapa de dolor con niveles de confianza**

Cada fila lleva etiqueta. Contenido mínimo obligatorio:

| Afirmación | Confianza | Evidencia |
|---|---|---|
| Vacante Senior AI Data Engineer abierta 2+ meses | Confirmado | Él la publicó; a los ~2 meses seguía con "Still looking for great Data Engineers!" |
| Su stack corre en niveles altos de madurez (ML productivo, Unity Catalog, Vector Search) | Confirmado | Descrito por él en su experiencia de Honeywell |
| No tiene experiencia SAP en su trayectoria | Confirmado | Cero menciones de SAP en 13 años de perfil |
| Honeywell usa SAP como fuente de manufactura/finanzas | Inferido | Industrial global de ese tamaño; alta probabilidad, no verificado |
| Su capa fuente arrastra la madurez del ecosistema AI-Ready | Especulativo | Es la tesis a validar con él, no un hecho |
| Tiene autoridad de presupuesto para servicios | Inferido | Director con COE propio y roadmap de 18 meses |

- [ ] **Step 3: Escribir el bloque 5 — vocabulario**

Términos textuales suyos, para usar sin traducir: `AI-Ready data`,
`production-grade`, `Data Products`, `Dollar-Weighted Yield Rate`, `Medallion`,
`Unity Catalog`, `data quality frameworks`, `lineage`, `drift monitoring`,
`Value Engineering / VECE COE`.

Y términos a **evitar**: "transformación digital", "sinergias", "soluciones de
punta a punta", "partner estratégico". Vocabulario de vendor genérico.

- [ ] **Step 4: Escribir el bloque 6 — encaje D&C ↔ su stack**

Tres columnas: dónde D&C es **complemento** (capa SAP: BW/4HANA, ECC, extractores,
ODP, reportes Z), dónde es **redundante** (Databricks/Azure/ML: él ya lo tiene y lo
hace bien), y dónde es **paralelo** (AI/BI Genie — ambos lo usan; punto de
conversación técnica, no de venta).

- [ ] **Step 5: Escribir el bloque 7 — objeciones y respuesta**

Mínimo estas cinco, cada una con respuesta redactada en primera persona:

1. *"Ya tenemos equipo de datos"* → no compites con su equipo; cubres la capa SAP
   que su equipo no tiene en su perfil.
2. *"¿Por qué no contrato a alguien?"* → Fábrica de Datos ≠ headcount; producto con
   garantía de integridad y calidad vs. una persona que hay que reclutar y formar.
3. *"Trabajas en Heineken, ¿esto es un side business?"* → declararlo de frente:
   socio de D&C, y la operación Heineken es precisamente la credencial operativa.
4. *"Somos cuenta global, meter un proveedor mexicano es fricción"* → él conoce el
   proceso mejor que nadie; se aborda con alcance cerrado y chico primero.
5. *"¿Qué casos tienen fuera de Heineken?"* → honestidad: la firma tiene 15 años y
   cartera Tier-1, el material documentado es Heineken, y esa es la operación que
   Ricardo dirige. **No inventar.**

- [ ] **Step 6: Escribir los bloques 8 y 9**

Bloque 8 (qué NO decirle): las seis reglas del spec §6.4, más "no traducir sus
términos al español".

Bloque 9 (ruta de compra): viene de procurement — habla SOW, alcance, precio y fin.
Primer trato pequeño y cerrado antes que marco maestro. Vendor onboarding de
Honeywell es real y se resuelve en llamada, no en chat.

- [ ] **Step 7: Verificar contra el spec**

Comprobar: (a) ningún dato de Honeywell sin etiqueta de confianza; (b) ninguna
cifra fuera de la lista blanca de Global Constraints; (c) ningún caso atribuido a
Metalsa/Nemak/CEMEX/Deacero/Copamex/FEMSA.

- [ ] **Step 8: Commit**

```bash
git add outreach/marco-quintanar/dossier.md
git commit -m "docs(outreach): dossier de cuenta de Marco Quintanar"
```

---

### Task 2: Secuencia de mensajes

**Files:**
- Create: `outreach/marco-quintanar/mensajes.md`
- Source: dossier bloques 5, 7, 8 + spec §6

**Interfaces:**
- Consumes: vocabulario (dossier §5), reglas de exclusión (dossier §8).
- Produces: el M1 canónico que el one-pager y el guión asumen ya enviado.

- [ ] **Step 1: Redactar el Mensaje 1 canónico**

Restricciones duras: **120–160 palabras**, español, cinco tiempos del spec §6.3
(anclaje → pretexto → tesis como patrón → credencial de una línea → cierre de costo
cero). El cierre debe regalar la salida: *"¿te suena, o en Honeywell ya lo tienen
resuelto?"*.

Prohibido (spec §6.4): diagnosticar Honeywell, mencionar su vacante, pedir llamada,
adjuntar material, liderar con Heineken, elogiar su perfil.

- [ ] **Step 2: Contar las palabras**

Verificar 120–160. Si excede, recortar del bloque de credencial — nunca del cierre.

- [ ] **Step 3: Escribir 2 variantes de tono**

Variante A: más técnica (entra directo por el patrón SAP→lakehouse).
Variante B: más conversacional (entra por la observación de industriales).
Mismas restricciones de longitud y mismas exclusiones.

- [ ] **Step 4: Escribir M2 rama A — interés técnico**

Profundiza sin vender. Incluye **una** pregunta de descubrimiento (cuántos ERPs
alimentan su capa analítica hoy). One-pager solo si él pregunta qué hacen.

- [ ] **Step 5: Escribir M2 rama B — tibio**

Máximo 40 palabras. Cierra bien, deja puerta abierta, **cero insistencia**.

- [ ] **Step 6: Escribir la nota de rama C — silencio**

No hay M2. Reactivación en 3–4 semanas solo con contenido nuevo. Prohibida la
frase "solo dando seguimiento" y cualquier variante.

- [ ] **Step 7: Verificar las seis reglas de exclusión**

Revisar M1 y ambas variantes contra la tabla del spec §6.4, regla por regla.
Confirmar además que ni Heineken ni Fábrica de Datos aparecen en ningún M1.

- [ ] **Step 8: Commit**

```bash
git add outreach/marco-quintanar/mensajes.md
git commit -m "docs(outreach): secuencia de mensajes para Marco Quintanar"
```

---

### Task 3: One-pager para Honeywell

**Files:**
- Create: `outreach/marco-quintanar/one-pager-honeywell.md`
- Source: spec §4, §8.3, §9.1 + `DC-Analitica/D&C - Data & Analytics Solutions.pdf`

**Interfaces:**
- Consumes: modalidades y encaje (dossier §6), reencuadre del caso (spec §9.1).
- Produces: el documento que el guión de llamada asume ya leído.

- [ ] **Step 1: Encabezar con la regla de uso**

Primera línea del archivo, visible: **"Se envía solo si Marco lo pide. Nunca
adjunto en frío."**

- [ ] **Step 2: Escribir la sección de tesis**

El techo de madurez lo pone la fuente. Reusar el Modelo de Madurez de D&C (5
niveles) como marco de diagnóstico, no de venta.

- [ ] **Step 3: Escribir la sección de capacidad SAP ↔ Databricks**

Lo que D&C aporta que su equipo no tiene: BW/4HANA, ECC, extractores, ODP,
reconciliación, semántica de reportes Z. Y lo que ya comparten: Databricks
Lakehouse, AI/BI Genie, Azure. Escrito como complemento, no como reemplazo.

- [ ] **Step 4: Escribir las dos modalidades**

**Proyecto cerrado:** alcance, precio y fin definidos.
**Fábrica de Datos:** equipo en pool, recibe requerimiento, responde por
integridad/calidad/consumo por uso.

Incluir la distinción explícita frente a staffing: no es poner gente bajo su mando,
es entregar producto de datos con garantía.

- [ ] **Step 5: Escribir la prueba**

Experiencia operativa propia (§9.1): 300+ reportes migrados, −50% licenciamiento,
~15 personas, SAP ECC → Databricks en producción. Redactado en primera persona de
operador. Cartera de la firma mencionada como trayectoria, sin cifras.

- [ ] **Step 6: Verificar longitud y honestidad**

Debe caber en una página (~500 palabras). Confirmar: cero cifras fuera de la lista
blanca, cero casos atribuidos a clientes distintos de Heineken, doble posición
declarada de frente.

- [ ] **Step 7: Commit**

```bash
git add outreach/marco-quintanar/one-pager-honeywell.md
git commit -m "docs(outreach): one-pager de D&C dirigido a Honeywell"
```

---

### Task 4: Guión de primera llamada

**Files:**
- Create: `outreach/marco-quintanar/guion-llamada.md`
- Source: dossier bloques 4, 7, 9 + spec §8.4

**Interfaces:**
- Consumes: mapa de dolor (dossier §4), objeciones (dossier §7), ruta de compra
  (dossier §9).
- Produces: entregable final. Nada depende de él.

- [ ] **Step 1: Escribir las preguntas de descubrimiento**

Mínimo seis, específicas de su entorno:
- ¿Cuántos sistemas fuente alimentan la capa analítica del VECE COE?
- ¿SAP está en ese conjunto, y quién lo opera hoy?
- Cuando un número del lakehouse no cuadra con el ERP, ¿quién lo reconcilia?
- ¿Quién firma que el número es correcto antes de que llegue a un ejecutivo?
- ¿Qué le está frenando el roadmap de 18 meses hoy?
- El rol que trae abierto, ¿qué trabajo concreto está esperando a esa persona?

La última se hace **solo si él saca el tema** de la vacante.

- [ ] **Step 2: Escribir las señales de compra**

Verde: describe dolor concreto de reconciliación; menciona plazos; pregunta cómo
cobran; mete a alguien más a la conversación.
Rojo: pide "una propuesta" sin conversación previa; deriva a procurement de
inmediato; habla solo en futuro condicional.

- [ ] **Step 3: Escribir el aterrizaje en alcance cerrado**

Viene de procurement: quiere SOW con precio y fin. Proponer un primer alcance
chico y verificable (ej. diagnóstico de una fuente SAP con entregable de
reconciliación) antes que un marco grande. Definir quién firma y en qué plazo.

- [ ] **Step 4: Escribir el manejo de objeciones en vivo**

Traer las cinco del dossier §7, condensadas a respuesta hablada de 2–3 líneas cada
una. En llamada no se lee un párrafo.

- [ ] **Step 5: Verificar**

Confirmar que ninguna pregunta asume hechos etiquetados como `Inferido` o
`Especulativo` en el dossier §4 — se preguntan, no se afirman.

- [ ] **Step 6: Commit**

```bash
git add outreach/marco-quintanar/guion-llamada.md
git commit -m "docs(outreach): guión de primera llamada con Marco Quintanar"
```

---

### Task 5: Índice del directorio

**Files:**
- Create: `outreach/README.md`

**Interfaces:**
- Consumes: los cuatro entregables anteriores.
- Produces: nada.

- [ ] **Step 1: Escribir el índice**

Tabla con los cuatro archivos, qué es cada uno y **cuándo se usa**. Marcar
explícitamente que el one-pager no se envía en frío y que nada de este directorio
se manda sin decisión de Ricardo.

- [ ] **Step 2: Anotar el estado del contacto**

Sección corta y editable: fecha de envío del M1, rama de respuesta observada,
siguiente acción. Se actualiza a mano conforme avance.

- [ ] **Step 3: Commit**

```bash
git add outreach/README.md
git commit -m "docs(outreach): índice del directorio de outreach"
```

---

## Self-Review

**Cobertura del spec:**

| Sección del spec | Task |
|---|---|
| §2 perfil, §3 análisis | Task 1 (bloques 1–4) |
| §4 D&C y modalidades | Task 1 (bloque 6), Task 3 (step 4) |
| §5 tesis | Task 2 (step 1), Task 3 (step 2) |
| §6 arquitectura y anatomía del M1 | Task 2 (steps 1–3, 7) |
| §7 ramas de seguimiento | Task 2 (steps 4–6) |
| §8.1 dossier | Task 1 completo |
| §8.2 mensajes | Task 2 completo |
| §8.3 one-pager | Task 3 completo |
| §8.4 guión | Task 4 completo |
| §9.1 reencuadre del caso | Task 1 (bloque 7, obj. 5), Task 3 (step 5) |

Sin huecos.

**Placeholders:** ninguno. Cada step nombra el contenido concreto a escribir.

**Consistencia:** los tasks 2–4 citan bloques del dossier por número; la numeración
coincide con la definida en Task 1.
