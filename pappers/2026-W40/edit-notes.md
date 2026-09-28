# Notas de edición — Papper W40 / Brújula edición 13

**Tema:** validación periódica después del go-live: el «testigo» (cifras control + conciliación
automática + estado visible en el tablero) y quién lo firma.
**Título:** «Cuadró en el go-live. ¿Y hoy?»
**Tesis:** las plataformas venden sellos de certificación (endorsement, `certification_status`,
glosarios), pero un sello no es un cuadre; los proyectos cuadran una vez y no dejan un control que
siga cuadrando. TI construye y corre el testigo, el negocio es dueño del significado y firma la
tolerancia, auditoría interna revisa.
**Fecha de publicación LinkedIn:** martes **29-sep-2026**.

**Alcance:** escenario ilustrativo, declarado como tal. Sin cliente, sociedad ni consultoría. La
lectora que originó la edición va **sin nombre** (decisión de Ricardo, 27-sep): «una lectora que
trabaja del lado de control de costos», comentario en la ed. 09 «Lo que se omite en silencio».
Revisado: no hay ningún nombre propio de la lectora en el draft.

---

## Figuras planeadas (3) — pendientes de render ES/EN 1080×1350

1. `fig-palomita` — **«La palomita no es un cuadre»**: cinco herramientas (Fabric/Power BI,
   Unity Catalog, Genie, Snowflake DMF, Datasphere), qué sello ofrece cada una, qué certifica y qué
   no hace. **Sin fila de SAC** (no tiene certificación de contenido).
2. `fig-testigo-codigo` — **«El testigo, en código»**: el SQL anotado (cifra control, tolerancia,
   estado; ojo: ya parte del mayor con `LEFT JOIN`) y abajo el badge «Conciliado… 4 de 4 OK».
3. `fig-quien-firma` — **«¿Quién firma?»**: matriz simplificada. Kicker: *TI construye el testigo;
   el negocio es dueño del significado.*

---

## Pasada `papper-editor` — 27-sep-2026

### CRÍTICO (aplicado)
- **L108-114 — cifra del PCAOB mal descrita.** El draft decía «el 17 % de las observaciones» y
  «se les pasa uno de cada seis» (a los auditores). El Spotlight de abr-2024 dice ~17 % de los
  **comment forms** de los ciclos 2021-2022. Corregido: se explica qué es un comment form y la
  frase queda como «casi uno de cada seis» comment forms, no auditorías ni auditores.
- **SQL del testigo — no detectaba el caso de su propio escenario.** Arrancaba del modelo con
  `INNER JOIN` al mayor: la sociedad dada de alta en agosto que «no entra al filtro de la vista»
  nunca aparece en el modelo, así que el testigo no la reportaba. Es exactamente el fallo de
  integridad (completeness) que el papper dice cubrir. Reescrito: parte de `fuente.saldos_mayor`,
  `LEFT JOIN` al modelo, `COALESCE(m.ventas_netas, 0)`, filtro de cuenta en el `WHERE`. Se añadió
  un comentario en el código y una frase en la prosa que lo explica.
- **L55-56 y subtítulo — «Todas las plataformas» traen certificación.** Falso para SAC (no tiene
  sello de contenido) y Snowflake no ofrece un sello sino checks de calidad. Suavizado a «Casi
  todas… algún mecanismo de certificación o de calidad».
- **L64-69 — Databricks «Nada la vuelve a evaluar».** La doc actual permite asignar
  `certification_status` con reglas de automatización (uso, antigüedad, dueño, descripción,
  etiquetas). Corregido: «se puede asignar a mano o con reglas automáticas… ninguna mira si el
  número cuadra». URL de la fuente corregida a `/aws/en/…`.
- **L220 — «la pregunta que dejé abierta en mi respuesta a ese comentario».** No hay registro en
  research.md de que Ricardo haya respondido el comentario. Cambiado a «la otra pregunta que deja
  el comentario». Si sí hubo respuesta, se puede restaurar.

### IMPORTANTE (aplicado)
- **Jerga sin definir en primera mención:** mayor, transporte, testigo (ahora definido al cerrar
  el escenario, no hasta la sección 5), modelo semántico, comment form, IPE/IPC, SOW, dueño del
  producto de datos. Todos con aposición corta.
- **IPE vs IPC.** El PCAOB usa «information produced by the company» (IPC); IPE es el término del
  gremio (AICPA / Big Four). Se presentan los dos para no confundir al lector que viene de SOX.
- **Genie duplicado.** Los dos «peros» de los benchmarks estaban en la sección de plataformas y
  otra vez en analítica conversacional. Quedan solo en la segunda; la primera remite «más abajo».
  Se quitó la mención a *trusted assets* (no aportaba al argumento) y su fuente.
- **Tesis de responsabilidad incompleta en «¿Quién firma?».** La respuesta corta no mencionaba a
  auditoría interna (solo en la tabla). Añadido «y auditoría interna revisa que el control
  funcione».
- **Acción para quien firma.** El punto 1 se concretó: pedir el testigo en el **SOW** con horas y
  costo propios, incluir el inventario de testigos como entregable y poner como **criterio de
  aceptación el primer cierre mensual conciliado después del go-live**, no el go-live.
- **Snowflake + «por evento».** La doc de DMF permite `TRIGGER_ON_CHANGES` (correr cuando hay DML
  en la tabla). Se usa en la prosa del SQL porque refuerza el punto 2 (conciliación por evento).
  Fuente añadida (`data-quality-working` + BCR 2025_07 del default de una hora).
- **Ancla regional.** «Manufactura y centros de servicios compartidos del noreste» y «cierre
  mensual» con corporativo, declarado como observación propia (ya lo estaba; se precisó).
- **Recorte:** ~3,160 → ~2,800 palabras (estimado, sin fuentes, con SQL). Analítica conversacional
  de ~170 a ~95 palabras; Genie en plataformas a la mitad; PCAOB, Basilea y DAMA compactados. No se
  eliminó ninguna sección ni el bloque SQL.

### PENDIENTE — decisión de Ricardo
1. **La cita textual del comentario (L12-16).** Es un comentario público en LinkedIn: aunque no
   nombremos a la lectora, citarlo literal la hace localizable en dos clics. Si la decisión de
   anonimato busca que no se le identifique, parafrasear en vez de citar entre comillas. Si solo
   busca no «usar» su nombre, se puede dejar. Confirmar además que la cita es textual y no
   paráfrasis.
2. **Convención de signo en el SQL.** En ACDOCA los ingresos van con signo negativo (haber). Si
   `saldo_mayor` viene crudo y `ventas_netas` en positivo, todo sale EXCEPCION. Se puede dejar
   implícito (es ilustrativo) o añadir `-f.saldo_mayor` / un comentario. No lo toqué para no
   complicar la figura.
3. **Ed. 09 y el *model transfer*** (punto 2 del testigo): research.md lo respalda («cada
   re-transfer es una migración nueva»); confirmar que la ed. 09 usa ese término literal.
4. **Genie benchmarks «a demanda».** Verificado en la doc (CAN EDIT, «at any time»). Existe un
   *Genie Space Optimizer* en `databricks-solutions` que corre benchmarks como Job, pero es un
   acelerador de campo, no producto; no se menciona. Si Databricks lo vuelve producto antes del
   29-sep, ajustar la frase de L270.

### Verificado, sin cambios
- AS 1105 ¶10: «test the accuracy and completeness… or test the controls over…» — correcto.
- PCAOB Spotlight abr-2024: ~17 % comment forms 2021-2022; repositorio central de reportes como
  buena práctica; SPA 11. Correcto (con la corrección de arriba).
- Fabric endorsement: *Certified* = revisor autorizado por la organización, «meets the
  organization's quality standards»; solo usuarios que designa el admin (delegable por dominio).
  Se quitó la segunda cita entre comillas («revisó el elemento») porque no la pude confirmar
  textual; queda como paráfrasis.
- Unity Catalog `system.certification_status` `certified`/`deprecated`; «met internal standards for
  accuracy, completeness, and trust»; palomita en tablas, dashboards y Genie spaces. Correcto.
- Genie benchmarks: hasta 500 preguntas, Good / Bad / Manual review needed. Correcto.
- Snowflake DMF + expectations, Enterprise Edition, default una hora. Correcto.
- BCBS 239 P3(c), nota 17, ¶34, P7 ¶53, ¶56: citas contra research.md (el PDF de bis.org no se
  pudo abrir desde aquí). Coinciden con el texto que conozco del documento; la redacción del ¶53
  se ajustó a «chequeos de razonabilidad» sin añadir matices que no están en la fuente.
- ACDOCA = Universal Journal de S/4HANA. Correcto.
- No hay afirmaciones sobre certificación de contenido en SAC. No se usa la cifra de Gartner.

### MENOR (estilo; ya aplicado en la pasada de humanización)
- Rotas las construcciones «El problema no es X. El problema es Y» (cierre del escenario) y «no es
  un "ahí va"; es un hallazgo» (punto 5).
- Negritas reducidas: fuera las de mitad de párrafo en Fabric, Genie, Snowflake, PCAOB y punto 6;
  quedan la pregunta central, «No dejó un testigo», la frase sello/cuadre y la respuesta corta.
- Registro regio moderado: «nomás» (2), «a la mera hora», «se me hace», «echar a andar», «cuadra».
- DAMA: «data custodian» no es un rol canónico del DMBOK (el libro habla de *technical data
  steward*); se atribuye a «la práctica que se apoya en el DMBOK» y la fuente se marca como resumen
  secundario (Dataversity). Si se quiere, sustituir por la cita directa del DMBOK 2.ª ed., cap. 3.
