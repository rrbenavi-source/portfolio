# Notas de edición — W37 "Verde no es evidencia"

Revisión del `draft-es.md` contra fuentes públicas (SAP Help, SAP Learning, KBAs, blogs de SAP).
Fecha de verificación: 2026-09-04.

---

## A. Las anotaciones que se necesitan (verificado)

La condición de extraibilidad son **dos requisitos simultáneos**, no uno:

| # | Requisito | Anotación | Valores |
|---|---|---|---|
| 1 | Habilitar la extracción | `@Analytics.dataExtraction.enabled` | `true` |
| 2 | Declarar la familia del dato | `@Analytics.dataCategory` **o** `@ObjectModel.dataCategory` | ver abajo |

Fuente literal (SAP Learning, *Working with ODP Context*):
> `@Analytics.dataCategory(#DIMENSION, #FACT or #CUBE)` **OR** `@ObjectModel.dataCategory(#TEXT or #HIERARCHY)` **AND** `@Analytics.dataExtraction.enabled`

### Mapeo declaración → contenedor destino

| Anotación y valor | Familia | Sufijo del ODP |
|---|---|---|
| `@Analytics.dataCategory: #DIMENSION` | Datos maestros (atributos) | `$P` |
| `@Analytics.dataCategory: #FACT` / `#CUBE` | Transaccional / hechos | `$F` |
| `@ObjectModel.dataCategory: #TEXT` | Textos | `$T` |
| `@ObjectModel.dataCategory: #HIERARCHY` | Jerarquías | `$H` |
| (sin categoría) | Otros | `$E` |

El nombre del ODP es el `@AbapCatalog.sqlViewName` + ese sufijo. **Esto es evidencia dura y barata
de la tesis del papper**: el contenedor destino literalmente hereda su tipo del sufijo que produce
la declaración. Vale la pena meterlo.

### Anotaciones de apoyo (no obligatorias, pero salen en el alcance real)
- `@Analytics.dataExtraction.delta.byElement.name` — delta por timestamp (desde S/4HANA 2018).
- `@Analytics.dataExtraction.delta.byElement.maxDelayInSeconds` — default 1800.
- `@Analytics.dataExtraction.delta.changeDataCapture` — CDC (desde S/4HANA 2019). SAP recomienda
  CDC si necesitas capturar borrados.
- `@ObjectModel.representativeKey` — obligatoria en vistas que son destino de foreign key y en
  vistas de texto (identifica a qué clave se refieren los textos).
- `@ObjectModel.text.element` / `@ObjectModel.text.association` — enlazan atributo con su texto.
- `@ObjectModel.hierarchy.association` — en la vista de datos maestros, apunta a la vista de jerarquía.
- `@AccessControl.authorizationCheck: #CHECK` — activa el chequeo DCL (ver hallazgo 2).

---

## B. Correcciones al texto

### B1. "Hay una sola anotación estrictamente obligatoria" — impreciso
El draft dice que hay una obligatoria y que "después hay que declarar de qué familia es el dato, y
ahí ya hay cuatro caminos". Suena a una anotación con cuatro valores. **Son dos anotaciones
distintas** repartiéndose las cuatro familias, y esa asimetría es en sí misma parte del argumento:
maestros y transaccionales viven en `@Analytics`, textos y jerarquías en `@ObjectModel`. Buscar
"la anotación de categoría" en la documentación te lleva a la mitad del mapa.

**Sugerencia:** dejar la frase de que `dataExtraction.enabled` es el interruptor, pero corregir el
segundo paso a "dos anotaciones distintas, cuatro familias".

### B2. El filtro de idioma — precisar el mecanismo
Dos ajustes, ambos verificables:

1. **No se descarta "todo lo que no coincide".** Lo que sobrevive son *los idiomas instalados en el
   sistema BW destino* (`zcsa/installed_languages` / RSCPINST). KBA 3219389, literal: *"only the
   languages installed in BW system will be extracted to BW side. The language will be used as
   filter automatically."* Y confirma que aplica a DataSources basados en vistas CDS de S/4HANA.
   Decirlo así es **mejor** para el papper: el filtro depende de la configuración de otro sistema,
   que nadie revisó, y por eso el número no cuadra.

2. **La detección por tipo `LANG` no está documentada públicamente así.** La referencia estándar
   (data element `RSDS_ISLANGDEP`) dice: *"A DataSource is language-dependent if it has a selection
   field that is defined as a language field. For DataSources in an SAP or BW source system, the
   corresponding selection field with field name **LANGU or SPRAS** are already defined."* Es decir,
   la documentación pública apunta al **nombre**, no al tipo. Tu observación de campo (tipo primero,
   nombre como respaldo) es coherente con lo que hicieron —romper el tipo *y* renombrar—, pero hoy
   el draft la presenta como hecho del sistema sin fuente.

   **Sugerencia:** presentarla como lo que es —lo que observamos en el sistema— y dejar el hecho
   documentado (el filtro automático por idiomas instalados) como la parte citada. Encaja con la
   regla de no atribuir lo que no se midió, y de hecho refuerza el papper: la corrección tuvo que
   atacar tipo *y* nombre porque el comportamiento real no estaba escrito en ningún lado.

### B3. Jerarquías: cuidado con nombrar la "otra sintaxis"
El draft dice bien que hay otra sintaxis "que sirve para consumo analítico y no para extracción",
pero no la nombra. Si se nombra, hay que hacerlo con precisión:

- **Vía de extracción:** `@ObjectModel.dataCategory: #HIERARCHY` (+ `@Hierarchy.parentChild` con
  las asociaciones a padre, a directorio y a las vistas de nodo/dimensión).
- **Vía analítica, la que sale primero:** la entidad `DEFINE HIERARCHY ... AS PARENT CHILD
  HIERARCHY(SOURCE ... CHILD TO PARENT ASSOCIATION ...)`, disponible desde S/4HANA 2023 on-premise
  y 2308 Cloud.

**Trampa a evitar:** `@Hierarchy.parentChild` pertenece a la vía **buena**, no a la equivocada. Si
el texto lo nombra como el camino falso, el papper se equivoca en el dato central de esa sección.

### B4. Jerarquías: el hallazgo del destino se puede volver mucho más concreto
Está corroborado por SAP y es más fuerte de lo que el draft dice hoy. Simon Kranig (SAP),
*CDS based data extraction Part III*, literal: *"You will need to equip a characteristic Cost
Center [...] with two additional external characteristics in the hierarchy: One characteristic for
the Cost Center Hierarchy ID (CHAR40). One characteristic for the Cost Center Hierarchy Node Text
(CHAR50, compounded to the Hierarchy ID)"*. La razón: *"the node texts are not delivered by the
actual hierarchy CDS view, but a separate one."*

O sea: una jerarquía de centro de coste necesita **tres vistas CDS** en el origen
(`I_COSTCENTERHIERARCHYNODE`, `I_COSTCENTERHIERARCHYNODET`, `I_COSTCENTERTEXT`) y **dos
características nuevas** en el destino.

**Esto es el mejor párrafo disponible del papper** y hoy está dicho en abstracto ("agregándoles
características que hoy no existen"). Con el número —tres vistas, dos características, longitudes
fijas— la sección de "alcance que no estaba en ninguna especificación" deja de ser una opinión y
pasa a ser una cuenta. Y es cita de SAP, no interpretación tuya.

### B5. Las cinco estructuras de la jerarquía — sin fuente pública
El draft afirma cinco segmentos: cabecera, textos de cabecera, nodos, textos de nodo e intervalos.
No encontré una fuente pública que los enumere así. Lo que sí está: Kranig menciona el segmento
0003 (nodos) y `source_package_4` (textos de nodo), lo que confirma que hay una estructura de
segmentos numerados, no un solo plano. La KBA 2440562 (*ODP: Hierarchy extraction*) confirma que
"only the first segment of the hierarchy will be extracted" es un síntoma conocido.

**Opciones:** (a) citar la fuente interna si la tienes del sistema; (b) bajar a "varias estructuras
distintas —nodos, textos de nodo, cabecera, intervalos— en segmentos numerados"; o (c) usar el dato
de Kranig, que es el que puedes citar. Yo iría por (c): el argumento no necesita el número cinco,
necesita que no sea una tabla.

### B6. Autorizaciones: nombrar el mecanismo y citarlo
El hallazgo es correcto y el mecanismo tiene nombre: las vistas llevan **access controls definidos
en DCL** (Data Control Language) que se activan con `@AccessControl.authorizationCheck: #CHECK` y
se resuelven contra objetos de autorización PFCG vía `aspect pfcg_auth`. El resultado es un
**recorte silencioso del result set**, no un error — que es exactamente tu punto. Hoy esta sección
es la única del papper sin una sola fuente. Ver §C.

### B7. Jerga sin definir (dos casos)
- **ODP** aparece una vez ("los perfiles de autorización estándar para extracción ODP") sin
  definirse. Es la sigla del framework de aprovisionamiento que hace posible toda la extracción;
  merece media línea en su primera mención.
- **delta**: el draft usa "el delta va al final" y recién después dice "carga incremental". Invertir
  el orden, o glosarlo en la primera aparición.

---

## C. Fuentes que faltan en la lista

1. **La guía de modelos de datos ABAP** se cita en el cuerpo ("la guía oficial de SAP sobre modelos
   de datos ABAP dedica un capítulo entero a jerarquías y no menciona ni una sola vez la
   extracción") pero **no está en la lista de fuentes**. Es:
   `https://help.sap.com/docs/abap-cloud/abap-data-models/abap-data-models`
   Como el argumento es una afirmación negativa —"no menciona"— la cita es obligatoria.
2. **Autorizaciones (§B6):** hoy sin respaldo. Candidatas:
   - KBA **3211519** — *ABAP_CDS: CDS View extraction authorization information*:
     `https://userapps.support.sap.com/sap/support/knowledge/en/3211519`
   - KBA **3062210** — *BW Queries Based on CDS Views: How to Manage User Dependent Access
     Restrictions* (menciona `@AccessControl.authorizationCheck` y DCL):
     `https://userapps.support.sap.com/sap/support/knowledge/en/3062210`
3. **Jerarquías / segmentos (opcional):** KBA **2440562** — *ODP: Hierarchy extraction*:
   `https://userapps.support.sap.com/sap/support/knowledge/en/2440562`
4. **Sintaxis nueva de jerarquías (si se nombra en §B3):** ABAP Keyword Documentation, *CDS DDL –
   DEFINE HIERARCHY*:
   `https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abencds_f1_define_hierarchy.htm`

Las seis fuentes actuales verificaron bien. Nota menor: las dos de SAP Help apuntan a NetWeaver
7.5, no a S/4HANA. El contenido de las anotaciones sigue siendo válido y la página de SAP Learning
lo confirma para el escenario S/4HANA → BW/4HANA, pero si alguien las abre va a ver "7.5". Vale un
paréntesis o cambiarlas por la referencia de anotaciones CDS actual.

---

## D. Dos datos que fortalecen la tesis y hoy no están

Ambos son de la misma fuente (Kranig, Part III) y aterrizan el "verde no es evidencia" en algo
operativo:

1. **RSA3 no sirve.** El chequeador de extractores clásico —el reflejo de cualquiera que venga de
   ECC— no funciona con vistas CDS habilitadas para extracción. Hay que usar el reporte
   `RODPS_REPL_TEST`, con la advertencia de que **no es simulación**: inicializar o correr un delta
   ahí crea una suscripción real en la cola ODQ, que después hay que limpiar con *Reset Delta*.
   Es literalmente el mismo patrón del papper: la herramienta con la que creías validar dejó de
   aplicar, y la nueva tiene un efecto secundario que no anuncia.

2. **Existe un inventario.** Desde S/4HANA 2020, la vista `I_DataExtractionEnabledView` lista las
   vistas CDS habilitadas para extracción, e incluye el campo `DELTACHGDATACAPTUREISSUPPORTED`
   para saber cuáles soportan CDC. Es un dato de una línea que le sirve a cualquiera que esté
   entrando a la fase — encaja en el cierre de "el cambio más barato que puedes hacer hoy".

---

## E. Pendientes de pipeline (no bloquean la edición)

- `draft-en.md`
- Figura (las últimas ediciones llevan una; candidata natural: el mapeo declaración → contenedor
  del §A, o la comparación "falla ruidosa vs. falla en verde")
- Render web (portfolio ES/EN) y `linkedin-es.md` / `linkedin-en.md`

---

## F. Datos maestros con llave compuesta (investigación adicional, aplicada)

Caso: atributos de centro de coste. Llave = sociedad de controlling + centro de coste + fecha de
validez. Reglas verificadas (SAP Learning, *Working with Dimension and Text Views*):

```abap
@Analytics.dataCategory: #DIMENSION
@Analytics.dataExtraction.enabled: true
@ObjectModel.representativeKey: 'CostCenter'      -- uno y sólo uno
define view entity ... {
      @ObjectModel.foreignKey.association: '_ControllingArea'
      @ObjectModel.text.association: '_ControllingAreaText'
  key kokrs  as ControllingArea,                  -- campo de llave NO representativo → asociación

      @ObjectModel.text.association: '_Text'
      @ObjectModel.hierarchy.association: '_CostCenterHierarchyNode'
  key kostl  as CostCenter,                       -- representativo

      @Semantics.businessDate.to: true
  key datbi  as ValidityEndDate,                  -- key, sin asociación, fuera de todo ON

      @Semantics.businessDate.from: true
      datab  as ValidityStartDate,                -- NO key
      ...
}
```

1. **Exactamente un `@ObjectModel.representativeKey`**, y tiene que ser campo clave. Es el "más
   específico" de la llave: en el ejemplo de SAP, dimensión de ciudad con llave país + ciudad → la
   ciudad. Para centro de coste → el centro de coste, no la sociedad.
2. **Todo campo de llave que no sea el representativo necesita `foreignKey.association` (o
   `text.association`) a una vista de datos maestros.** Excepciones: campos de fecha/hora y, en
   vistas de texto, el campo de idioma (`@Semantics.language`).
3. **Time-dependency:** el campo "válido hasta" va en la llave con `@Semantics.businessDate.to`; el
   "válido desde" fuera de la llave con `@Semantics.businessDate.from`. Regla dura y fácil de
   romper: *"The key field which is assigned @Semantics.businessDate.to must not be included in the
   ON condition of any foreign key association and it must not have a foreign key association."*
4. **Textos:** `@ObjectModel.text.association` va sobre el campo **representativo**, pero la
   condición ON debe incluir **todos** los campos de la llave y la vista de textos debe tener
   **exactamente la misma llave**. Si no hay vista de textos, `@Semantics.text: true` en el campo
   de texto + `@ObjectModel.text.element` en el representativo.
5. **Jerarquía:** si la vista de jerarquía es de la vía antigua (`@Hierarchy`),
   `@ObjectModel.hierarchy.association` va sobre el campo representativo.
6. **Asociaciones con cardinalidad [0..1]** y con todos los campos clave del destino mapeados.

### Por qué esto es relevante para el papper
La llave compuesta del origen se convierte en **compounding** en el destino (el centro de coste
colgando de la sociedad de controlling), y qué cuelga de qué lo decide el campo declarado
representativo. Cuando la derivación falla, sí hay ruido: `RSODP056` — *cannot derive InfoObject
name* — en tiempo de activación, cuando otra vista intenta asociarse a una vista con característica
compuesta (KBA 2754750). Eso da el contraste que le faltaba a la sección: **la declaración
estructural aborta; la declaración semántica pasa en verde.**

---

## G. Estado de aplicación (2026-09-04)

Aplicado a `draft-es.md`:
- B1 — dos anotaciones / cuatro familias, + sufijos `$P`/`$T`/`$H`/`$F` como evidencia.
- **§F completo** — nuevo pasaje sobre llave compuesta + `RSODP056`.
- B2 — "idiomas instalados en el destino"; el tipo vs. nombre pasa a observación de campo declarada
  como tal. Corregida la frase que atribuía la causa al tipo ("es la marca de idioma en un campo
  cualquiera").
- B3 — nombradas las dos sintaxis con precisión (`DEFINE HIERARCHY` = vía analítica;
  `@ObjectModel.dataCategory: #HIERARCHY` = vía de extracción).
- B4 — jerarquías: tres vistas CDS en origen, dos características nuevas en destino.
- B5 — "cinco estructuras" → "segmentos numerados", sin número sin fuente.
- B6 — DCL nombrado; el recorte silencioso explicitado.
- B7 — ODP y *delta* definidos en su primera mención.
- D1 — `RSA3` no aplica / `RODPS_REPL_TEST` no simula.
- §C — lista de fuentes reescrita: 11 entradas, todas verificadas, con lo que respalda cada una.

Pendiente: `draft-en.md`, figura, render web ES/EN, `linkedin-es.md` / `linkedin-en.md`.

---

## H. Cómo se arman las vistas de jerarquía (investigación adicional, aplicada)

**No hay carpetas de S/4HANA en el disco.** `~/Documents/SAP` sólo contiene exports de SAP GUI
(xls). La búsqueda se hizo contra la documentación de S/4HANA en SAP Help / SAP Learning.

### Las cinco vistas (modelo analítico) — fuente: SAP Learning, *Working with Hierarchy Views*

| # | Vista | ¿Obligatoria? | Qué aporta |
|---|---|---|---|
| 1 | **Source view** | Sí | Lista plana de campos **y todas las asociaciones**. Existe porque la vista de jerarquía no las admite. |
| 2 | **Hierarchy view** (`define hierarchy`) | Sí | Lee la source view y construye el árbol. **No se pueden definir asociaciones aquí.** |
| 3 | **Hierarchy directory view** | Opcional | Metadatos de cada instancia de jerarquía (p. ej. `@Semantics.systemDateTime.lastChangedAt`). Obligatoria si la vista contiene más de una jerarquía. |
| 4 | **Hierarchy directory text view** | Opcional | Textos multiidioma de la descripción de la jerarquía. |
| 5 | **Hierarchy node view** | Opcional | Atributos y textos de los nodos que no corresponden a un valor de dimensión. Técnicamente **es una dimension view**. |

**Esto reemplaza la afirmación de "cinco estructuras" del draft original**, que enumeraba segmentos
del DataSource (cabecera, textos de cabecera, nodos, textos de nodo, intervalos). Las dos cosas son
ciertas y son cosas distintas: cinco **vistas** en el origen, segmentos numerados en el DataSource
destino. El draft ahora dice ambas y las distingue.

### Reglas de construcción (vía de extracción: `@ObjectModel.dataCategory: #HIERARCHY`)

Cabecera de la vista de jerarquía:
```abap
@ObjectModel: { dataCategory: #HIERARCHY }
@Hierarchy.parentChild: [{
  name          : 'CostCenterHierarchy',        -- obligatorio si NO hay directory
  label         : '...',
  recurse       : { parent: 'ParentNode', child: 'HierarchyNode' },
  siblingsOrder : [{ by: 'SequenceNumber', direction: 'ASC' }],
  directory     : '_Hierarchy',
  orphanedNode.handling : #ROOT_NODES,
  rootNode.visibility   : #DO_NOT_ADD_ROOT_NODE
}]
```

Tres clases de asociación, y las tres tienen reglas:

1. **Auto-asociación al padre** — define la relación padre/hijo. Tiene que ser self-association
   (mismo origen y destino); en el ON sólo `=` unidas con `AND`, mismo número de campos y mismo
   tipo a cada lado. **El hijo va en campos clave; el padre es atributo.**
2. **Asociación al directorio** — necesaria si la vista contiene más de una jerarquía. **Los campos
   del ON tienen que ser campos clave.** Regla que amarra las dos: *todos* los campos clave deben
   pertenecer o a la asociación al directorio o a la recursiva.
3. **Asociaciones por tipo de nodo** a las vistas de dimensión/texto. **Una es obligatoria**: su
   destino tiene que ser la dimension view que lleva `@ObjectModel.hierarchy.association` apuntando
   de vuelta a esta jerarquía. Esos registros son las hojas.

Dos trampas de la vía antigua (la de extracción), que no existen en la nueva:
- **El orden de las asociaciones importa.** Para cada registro se evalúan en el orden en que están
  listadas y gana la primera cuyo ON se cumple; por eso hacen falta condiciones extra en el ON
  (`carrid = ''`, `connid = '0000'`). En la vía nueva esto se resuelve con un campo `nodetype` y el
  orden deja de importar.
- **Las asociaciones hay que exponerlas en la lista de elementos**; si no, no están disponibles
  aunque estén declaradas arriba.

Del lado de datos maestros: `@ObjectModel.hierarchy.association: '_Hier'` sobre el campo
representativo de la dimension view (ver §F).

### Centro de coste, caso real
Las vistas estándar se asocian por la llave compuesta completa: `I_CostCenterHierarchy` por
`CostCenterHierarchy` + `ControllingArea` + `ValidityEndDate`; `I_CostCenterHierarchyNodeT` por
`CostCenterHierarchy` + `HierarchyNode` + `ControllingArea`. Es decir: la llave compuesta de §F
reaparece en cada condición ON del árbol. Un error ahí no aborta — devuelve un árbol incompleto.

---

## I. Revisión contra la documentación del proyecto (2026-09-04) — CORRIGE §B2 y §B5

Fuente: `~/Documents/ Claude Files/S4HANA/` (repo del proyecto). Documentos revisados:
`notas/Newsletter_Anotaciones_CDS_Extraccion.md`, `DOCUMENTACION JERARQUIAS/Conexion_ODP_CDS_Requisitos.md`,
`DOCUMENTACION JERARQUIAS/0COSTCENTER_0101_HIER_DataSource.md`,
`DOCUMENTACION JERARQUIAS/Transformacion_0COSTCENTER_HIER.md`.

### I1. Me equivoqué al suavizar la detección por tipo (revierte §B2)
El proyecto lo tiene verificado **con controles negativos**, que es más fuerte que la doc pública:
BW asigna *Field Type = Language Field* a **cualquier** campo cuyo Data type sea `LANG`.
Lo que NO funcionó y quedó descartado: `@Semantics.language: false` (la marca no viene de la
anotación); `cast(campo as abap.char(1))` directo (error de sintaxis, `LANG` no está en la matriz
de conversiones); leer el campo de la tabla en vez de la vista released (mismo efecto → **es el
tipo, no la herencia de anotaciones**). Ocurrió en `0COSTCENTER_ATTR`, campo `SPRAS` — vista de
**atributos**, no de textos, justo como dice el papper.

La línea que funcionó: `cast( left( _Z.SPRAS, 1 ) as abap.char( 1 ) ) as ZZSPRAS` — la función de
cadena rompe el `LANG` y el cast fija `CHAR 1`. **Y** hay que renombrar, porque con el tipo ya
corregido BW lo vuelve a detectar por nombre. **Son dos mecanismos, no uno.** Draft corregido.

### I2. Los cinco segmentos eran correctos (revierte §B5)
Confirmado contra el DataSource real: 0001 cabecera, 0002 textos de cabecera, 0003 nodos, 0004
textos de nodos, 0005 hojas/intervalos. La enumeración original del draft era exacta. Restaurada.

**Dato adicional no usado (candidato a figura):** la *transformación* tiene **6 grupos** — los
cinco segmentos más "Textos por nivel de jerarquía", que el origen **no alimenta**. El destino
espera seis, el origen entrega cinco. Es la asimetría del papper en una sola imagen.

### I3. `representativeKey` bloquea la extracción (mejora §F)
No es anotación de adorno analítico: sin ella el ODP no publica la vista ("no muestra un campo
representativo"). Y **referencia el ALIAS, no el nombre de origen** — igual que `text.element` y
`foreignKey.association`; las `@Semantics.*` van sobre el campo y no les afecta el renombrado.
Añadido al draft: es la tesis del papper en miniatura (metadato que parece decorativo y sostiene
la carga).

### I4. La afirmación negativa, con número
La guía *ABAP Data Models* son **244 páginas** y no mencionan ni una vez
`@Analytics.dataExtraction.enabled`, `#HIERARCHY`, ODP ni extracción BW. El draft decía "dedica un
capítulo entero a jerarquías y no menciona la extracción"; ahora usa el número verificado.

### I5. Confirmaciones (sin cambio en el draft)
- **Dos características externas:** `0COSTCENTER` y `0ACCOUNT` muestran "External Characteristics
  in Hierarchies (0)"; `0PROFIT_CTR` ya tiene 2. → "dos de las tres" es exacto.
- **DCL / autorizaciones de negocio:** el proyecto lo clasifica como *el riesgo principal de la
  conexión*, con el mismo modo de fallo (menos filas o cero, sin error). Dimensiones: sociedad CO
  para centro de coste y centro de beneficio, plan de cuentas para cuenta de mayor.
- **`RSA3` no sirve / `RODPS_REPL_TEST` no simula / Reset Delta.** Confirmado.
- **`#MASTER_DATA` no existe.** Una vista de atributos no lleva `@ObjectModel.dataCategory` en
  absoluto; lleva `@Analytics.dataCategory: #DIMENSION`.

### I6. Material del proyecto NO usado (candidatos para una edición futura)
- **Las asociaciones nunca se extraen.** Sólo viajan campos planos del SELECT; una asociación
  expuesta no llega al DataSource. De ahí que el patrón dominante sea el **Z-wrapper**: una CDS Z
  que envuelve la released, aplana y publica. Es una decisión de arquitectura completa y da para
  su propia edición.
- **El DataSource congela la lista de campos al crearse.** Cambios posteriores en la CDS no se
  propagan; hay que borrar y recrear. Caso real: la CDS tenía `DATEFROM` + tres textos y el
  DataSource mostraba sólo las 4 claves — fallo **estructural**, no de tipos.
- **Un source system = un contexto ODP.** No se "reapunta" la conexión de `[SAPI]` a `[ABAP_CDS]`:
  es source system nuevo, sistema lógico nuevo, destinos RFC nuevos, y los tres DataSources de
  jerarquía se re-crean. Alcance oculto puro, de la misma familia que la tesis del papper.
- **~4.700 extractores CDS released en S/4HANA 2025**, ~18% con capacidad delta. Cifra útil para
  el argumento de "verificar si ya existe la estándar antes de construir".

### I7. Confidencialidad
Nada de lo aplicado al draft lleva nombre de cliente, sociedad, sistema, mandante ni socio
implementador. Los identificadores del proyecto (SID, mandante, source system, código de sociedad,
nombre del partner) se quedan fuera por diseño.

---

## J. Producción completa (2026-09-04)

| Entregable | Archivo | Estado |
|---|---|---|
| Draft ES | `draft-es.md` (3.049 palabras) | ✅ corregido con §I |
| Draft EN | `draft-en.md` (3.026 palabras) | ✅ |
| Portada ES | `brujula-cover-10.html` / `.png` (1920×1080) | ✅ |
| Portada EN | `brujula-cover-10-en.html` / `.png` | ✅ |
| Figura 1 ES | `fig-cinco-seis.html` / `.png` (1080×1350) | ✅ |
| Figura 1 EN | `fig-cinco-seis-en.html` / `.png` | ✅ |
| Publicación web ES | `web/src/i18n/es.ts` → `verde-no-es-evidencia` (idx 12) | ✅ |
| Publicación web EN | `web/src/i18n/en.ts` → `verde-no-es-evidencia` (idx 12) | ✅ |
| Assets web | copiados a `web/src/assets/publicaciones/` | ✅ |
| Build | `npm run build` — 40 páginas, sin errores | ✅ |
| Render verificado | 1280×900 con base path `/portfolio/` | ✅ |
| Copypaste LinkedIn | `brujula-ed10-copypaste-es.md` | ✅ sin hard wrap |

**Edición 10 · 2026 · W37.** Publicación de newsletter prevista: martes 8-sep-2026, 9:00 CDMX.

URLs una vez desplegado:
- ES: https://rrbenavi-source.github.io/portfolio/publicaciones/verde-no-es-evidencia
- EN: https://rrbenavi-source.github.io/portfolio/en/publicaciones/verde-no-es-evidencia

**Sin commitear.** El working tree tiene `pappers/2026-W37/` nuevo y `web/src/i18n/{es,en}.ts`,
`web/src/assets/publicaciones/` y `web/dist/` modificados.

---

## K. Cambio de título (2026-09-04)

**«Verde no es evidencia» → «Cómo validar una migración de extractores a S/4HANA».**
Razón del cambio: el título anterior no daba visibilidad del tema. La gente tiene que entender
de qué trata la edición **antes** de entrar. Se rompe a propósito con el estilo elíptico de las
ediciones 08–09 («El reloj que no es tuyo», «Lo que se omite en silencio») a favor de claridad y
alcance en búsqueda.

- **EN:** *How to validate an extractor migration to S/4HANA*
- **Slug (ES y EN):** `validar-migracion-extractores-s4hana`
- **Subtítulo ES:** «La carga corrió sin errores y trajo menos filas. Cuatro cosas que le pediría a
  un plan de trabajo —y dos a un contrato.»
- **SEO título:** «Cómo validar una migración de extractores a S/4HANA: por qué el verde ya no basta»

Propagado a: `draft-es.md`, `draft-en.md`, portadas ES/EN (h1 bajado de 96px a 74px, itálica sobre
*validar*), `web/src/i18n/es.ts`, `web/src/i18n/en.ts`, `brujula-ed10-copypaste-es.md` y assets.
Build verificado: 40 páginas, rutas nuevas en ES y EN, cero rastros del título anterior en `dist/`.

URLs finales:
- ES: https://rrbenavi-source.github.io/portfolio/publicaciones/validar-migracion-extractores-s4hana
- EN: https://rrbenavi-source.github.io/portfolio/en/publicaciones/validar-migracion-extractores-s4hana

Nota: el cuerpo del papper conserva la frase «verde no es evidencia» como tesis interna —sigue
funcionando como remate, ya no como título.

---

## L. Figuras para LinkedIn (2026-09-08)

La web ganó una **Fig. 1 de código** (commit `2da5ebc`, hecho fuera de esta sesión): un bloque
`type: 'code'` con la vista CDS del extractor de atributos de centro de coste. En la web funciona
—el texto es seleccionable— pero **LinkedIn no renderiza bloques de código**, así que el copypaste
se quedó con una sola imagen.

**Solución:** `fig-codigo-cds.png` / `-en.png` (1080×1350) — el mismo código renderizado como
imagen de marca, con resaltado sobre las dos anotaciones que habilitan la extracción y sobre la
línea del `cast`/rename del campo de idioma. Queda como **Figura 1** del material de LinkedIn;
`fig-cinco-seis` pasa a **Figura 2**. Así LinkedIn y la web quedan con la misma numeración.

La web **no se toca**: ahí el código sigue como bloque de texto, que es mejor para leer y copiar.

### Extra disponible, sin usar
`fig-dos-anotaciones.png` / `-en.png` — mapa de las anotaciones: la obligatoria
`@Analytics.dataExtraction.enabled` arriba, y abajo las dos anotaciones `dataCategory`
repartiéndose las cuatro familias con su sufijo ODP (`$P`/`$F`/`$T`/`$H`), más la nota de que
`$E` es «sin clasificar» y de que `#MASTER_DATA` no existe. La construí antes de ver el commit
del código. Es el activo más «guardable» de la edición, pero serían tres figuras: queda
disponible por si la quieres para la web, para un carrusel aparte o para una edición futura.
