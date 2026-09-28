# Cuadró en el go-live. ¿Y hoy?

## Casi todas las plataformas de datos ya te dejan ponerle a un modelo la palomita de «certificado». Ninguna te obliga a demostrar que hoy la merece. Los proyectos cuadran el número el día del go-live y luego no dejan nada que lo siga cuadrando. De ese testigo que falta va esta edición, y de quién lo debería firmar.

Esta edición no la planeé yo. La pidió una pregunta.

En la edición 09, «Lo que se omite en silencio», escribí sobre lo que se pierde cuando una query de BW
se lleva a Business Data Cloud: fórmulas, variables y autorizaciones que no viajan sin que nadie
avise. Una lectora que trabaja del lado de control de costos dejó ahí un comentario que explicaba el
problema de fondo mejor que yo:

> «Un dashboard construido sobre SAP HANA se sigue viendo sano —abre, trae números— aunque la query
> que lo alimenta haya perdido una fórmula de variación o una variable de autorización en el camino.
> El controller no tiene forma de saberlo desde el tablero; solo lo detecta si cuadra manualmente
> contra la fuente, celda por celda, algo que en la práctica casi nadie hace después de la puesta en
> marcha inicial.»

Luego preguntó si la edición tocaba la validación periódica, no nomás la de la migración. No la
tocaba. Esta es la otra mitad.

Conforme lo fui investigando me quedó claro que no es un tema de SAP. Da igual si el dato vive en
BW/4HANA, en Databricks o en Snowflake, y si lo consumes en SAP Analytics Cloud, en Power BI o
preguntándole en español a un asistente como Genie. La duda del negocio es la misma y casi ningún
proyecto la contesta: **¿cómo sé que el número con el que estoy decidiendo hoy es el correcto?**

## El dashboard que se ve sano

Te pongo un escenario ilustrativo. No es un cliente; es la suma de lo que he visto en varios
go-lives.

Un tablero de costos sale a productivo en marzo. Antes de liberarlo, el equipo lo cuadra contra el
mayor, el libro contable donde vive la cifra oficial: sociedad por sociedad, mes por mes, al peso.
Contraloría firma la validación, se cierra el proyecto y todos contentos. Con razón: el número
cuadraba.

En mayo, un transporte (el paquete con el que un cambio pasa de desarrollo a productivo) corrige un
filtro de la query y, sin querer, cambia la base de la variación contra el año anterior. En julio
reorganizan las zonas comerciales y la jerarquía del modelo se queda con la estructura vieja. En
agosto dan de alta una sociedad que no entra al filtro de la vista. En septiembre llega un upgrade.

Nada de eso rompe el tablero. Abre rápido y trae números que se ven razonables. Nadie recibe una
alerta, porque técnicamente todo funciona. Lo que se descompuso fue el significado.

Un día de octubre, en la junta de presupuesto, alguien del comité trae impreso el dato del mayor y
no coincide con el de la pantalla. A la mera hora ya nadie discute el presupuesto; discuten cuál de
los dos números es el bueno. La confianza que costó un proyecto entero se va en diez minutos.

Que los números se descuadren no tiene nada de raro; los sistemas cambian. Lo raro es que el
proyecto cuadró una vez y no dejó nada que siguiera cuadrando. **No dejó un testigo**: un control que
vuelva a comparar el número contra su fuente cada vez que algo cambia, sin que nadie se tenga que
acordar.

## La palomita no es un cuadre

Aquí viene la parte incómoda para los que vendemos y construimos plataformas. Casi todas traen ya
algún mecanismo de «certificación» o de calidad. Vale la pena leer qué certifica cada uno.

**Power BI y Microsoft Fabric** tienen el *endorsement*, un sello que se le pone al modelo: *Promoted*
o *Certified*. Según la documentación de Microsoft, *Certified* quiere decir que un revisor
autorizado por la organización dio fe de que el elemento *«cumple los estándares de calidad de la
organización»*, y solo pueden otorgarlo las personas que designa el administrador. O sea, certifica
que alguien lo revisó en algún momento. Si mañana cambia el modelo, el sello se queda donde estaba.

**Databricks** tiene en Unity Catalog, su capa de gobierno, una etiqueta de sistema,
`system.certification_status`. El valor `certified` indica que el activo *«cumplió los estándares
internos de exactitud, integridad y confianza»* y pone una palomita junto a la tabla, el dashboard
o el espacio de Genie. Se puede asignar a mano o con reglas automáticas que miran el uso, el dueño o
la antigüedad del activo. Ninguna de esas reglas mira si el número cuadra.

**Genie**, el asistente de Databricks que contesta preguntas de negocio en lenguaje natural y escribe
el SQL por su cuenta, es lo más parecido a un testigo que encontré. Tiene *benchmarks*: hasta 500
preguntas de prueba, cada una con el SQL que da la respuesta correcta, contra las que Genie califica
lo que genera como bueno, malo o «requiere revisión manual». Por qué no alcanza solo, lo explico más
abajo.

**Snowflake** trae *Data Metric Functions*, funciones que miden algo de una tabla (nulos, duplicados,
qué tan fresca está) y que, junto con una *expectation*, dan un «pasa» o «no pasa» con calendario
propio, cada hora por default. Es lo más cercano a un control continuo y pide la edición Enterprise.
Pero mide la calidad del dato, no si el KPI cuadra contra la contabilidad. Esa función la escribes
tú.

**En SAP**, el catálogo de Datasphere permite documentar un KPI con su fórmula en un glosario y
publicar activos como confiables. Sin una definición única no hay nada que cuadrar, así que hace
falta. Pero una definición bien escrita no prueba que el número de hoy la cumpla. En el caso del
comentario, un modelo que perdió media fórmula en la migración, el glosario sigue intacto y el
número ya no.

[ FIGURA 1 — «La palomita no es un cuadre»: cinco herramientas, qué sello ofrece cada una, qué
certifica en realidad y qué no hace. ]

No lo digo como crítica a los fabricantes; las herramientas hacen lo que prometen. El hueco está en
otro lado. **Un sello dice quién opinó que el dato era confiable. Un cuadre demuestra que hoy lo
es.** Y los proyectos entregan el sello, cuadran una vez para ganárselo y se van.

## Esto ya está resuelto, pero en otra industria

Lo que más me sorprendió es que no hay nada que inventar. Dos mundos llevan años obligados a
resolver esto y lo dejaron por escrito.

**El primero es la auditoría.** El PCAOB es el organismo que supervisa a los auditores de las
empresas que cotizan en Estados Unidos. Su norma de evidencia, la AS 1105, dice que cuando el
auditor usa información que produce la propia empresa (un reporte del sistema, por ejemplo; en el
gremio le dicen IPE, y el PCAOB le dice IPC) debe *«probar la exactitud y la integridad de la
información, o probar los controles sobre la exactitud y la integridad de esa información»*.
Exactitud: que cada renglón diga lo correcto. Integridad: que no falte ningún renglón y que los
totales cuadren.

Cuando el PCAOB inspecciona una auditoría y encuentra una deficiencia, se la notifica a la firma en
un *comment form*. En abril de 2024 publicó que en cerca del 17 % de los comment forms de sus ciclos
2021 y 2022 el problema fue ese: el auditor no probó lo suficiente la exactitud e integridad de los
reportes y datos de la empresa, o los controles sobre ellos. Casi uno de cada seis, en una profesión
con una norma que se lo exige. Un proyecto de BI no tiene ninguna.

El mismo reporte describe lo que hacen las firmas que sí lo resuelven: un repositorio central de
reportes, con la aplicación de donde sale cada uno, cómo se prueba y con qué conclusión. Literal, un
inventario de testigos.

Y esto nos toca más de lo que parece. Muchas empresas del noreste, sobre todo en manufactura y en
centros de servicios compartidos, reportan a un corporativo que cotiza en Estados Unidos. El tablero
que el controller abre aquí el lunes muchas veces es el mismo reporte que acaba en el paquete de
cierre mensual de allá. Esto es observación mía, no estadística; no conozco una cifra para México y
no la voy a inventar.

**El segundo mundo es la banca.** En 2013 el Comité de Supervisión Bancaria de Basilea publicó el
BCBS 239, sus principios para que los bancos grandes pudieran confiar en sus propios reportes de
riesgo después de la crisis de 2008. Son para bancos, pero es el texto mejor escrito que conozco
sobre este problema. Le tomo tres ideas:

1. **Conciliar contra la contabilidad.** El principio 3 pide que el dato *«se concilie contra las
   fuentes del banco, incluidos los datos contables cuando corresponda»*, y define conciliar como
   *«comparar partidas o resultados y explicar las diferencias»*. Comparar no alcanza.
2. **Un inventario de reglas y reportes de excepción.** El principio 7 pide, como mínimo, procesos
   definidos para conciliar los reportes, chequeos de razonabilidad con un inventario de las reglas
   de validación, y reportes de excepción que identifiquen y expliquen los errores.
3. **La materialidad como criterio.** Basilea pide medir la exactitud con un criterio *«análogo a la
   materialidad contable»*: si el error podría cambiar la decisión de quien lee el reporte, es
   material. No todo tiene que cuadrar al centavo; tiene que cuadrar dentro de una tolerancia que
   alguien de negocio firmó.

Ninguna de las dos fuentes menciona Databricks, SAC ni Genie. No hace falta: describen un control,
no una herramienta.

## El testigo

Con eso, la práctica que propongo cabe en seis puntos. Ninguno es caro. Se omiten porque ninguno
viene en la propuesta del proyecto.

**1. Cifras control, definidas por el negocio.** Una cifra control es un total conocido e
independiente contra el que se compara el reporte: el saldo del mayor por sociedad y periodo, las
unidades facturadas del mes, el total de la nómina. Por cada KPI crítico hay que dejar escrito
contra qué se concilia, a qué nivel y con qué tolerancia. La tolerancia no la pone TI; la pone y la
firma el dueño del número.

**2. Conciliación por evento, no nomás por calendario.** Correr el cuadre cada mes está bien, pero
el tablero del escenario no se rompió en una fecha: se rompió con un transporte, una reorganización y
un upgrade. El testigo tiene que correr también después de cada carga, de cada cambio al modelo
semántico (la capa donde viven las definiciones de los KPI), de cada transporte y de cada upgrade. En
la edición 09 lo vimos con el *model transfer* de BW: cada vez que se vuelve a transferir, es una
migración nueva.

**3. Celdas testigo y un usuario canario.** No hay que cuadrar celda por celda. Hay que escoger las
pocas intersecciones que se rompen primero: la variación contra el año anterior, un KPI con filtros
restringidos, el total por sociedad y un periodo ya cerrado, que nunca debería moverse. Las
autorizaciones fallan más callado que las fórmulas, así que para ellas va un usuario canario por
perfil: un usuario de prueba con los permisos de, digamos, un gerente regional, que corre el mismo
reporte en cada ciclo y compara lo que ve contra lo que debería ver.

**4. Un inventario de reglas y de reportes.** Una tabla sencilla: qué reporte, qué cifra control,
qué regla, cada cuándo, último resultado. Es el repositorio que el PCAOB pone como buena práctica y
el inventario que pide Basilea. Y es lo primero que te va a pedir un auditor.

**5. Excepciones con explicación.** Cuando el testigo no cuadra, la diferencia se registra, se le
asigna a alguien y se explica. Una diferencia sin explicación es un hallazgo, por chica que sea.

**6. El estado del cuadre, visible en el tablero.** Este punto contesta directo la pregunta de la
lectora. Si el controller no tiene forma de saber desde el tablero si el número cuadra, que el
tablero se lo diga: «Conciliado contra cifras control el 23-sep: 4 de 4 OK». Y si ayer no cuadró,
que lo diga también. La palomita se gana cada día.

El testigo no necesita una herramienta nueva. Se echa a andar con lo que ya tienes: una consulta
que compara el KPI del modelo contra el total del mayor y escribe el resultado en una tabla de
control.

```sql
-- Testigo: ventas netas del modelo semántico contra el mayor, por sociedad y periodo.
-- Parte del mayor, no del modelo: si una sociedad no llega al modelo, sale como EXCEPCION.
INSERT INTO control.conciliacion (fecha_ejecucion, kpi, sociedad, periodo,
                                  valor_modelo, valor_fuente, diferencia, estado)
SELECT CURRENT_TIMESTAMP,
       'VENTAS_NETAS',
       f.sociedad,
       f.periodo,
       COALESCE(m.ventas_netas, 0),
       f.saldo_mayor,
       COALESCE(m.ventas_netas, 0) - f.saldo_mayor,
       CASE WHEN ABS(COALESCE(m.ventas_netas, 0) - f.saldo_mayor)
                 <= t.tolerancia_pct * ABS(f.saldo_mayor)
            THEN 'OK' ELSE 'EXCEPCION' END
FROM (
       -- En el mayor (ACDOCA) los ingresos se registran en negativo, como abono:
       -- se invierte el signo para compararlos contra el KPI, que viene en positivo.
       SELECT sociedad, periodo, -1 * saldo AS saldo_mayor
       FROM   fuente.saldos_mayor
       WHERE  cuenta_grupo = 'VENTAS_NETAS'
     ) f
LEFT JOIN modelo.ventas_por_sociedad  m ON m.sociedad = f.sociedad
                                       AND m.periodo  = f.periodo
JOIN      control.tolerancias         t ON t.kpi = 'VENTAS_NETAS';
```

[ FIGURA 2 — «El testigo, en código»: la consulta anotada (la cifra control, la tolerancia que firma
el negocio, el estado que se publica) y abajo cómo se ve el resultado en el tablero. ]

La consulta es lo de menos. Fíjate en tres cosas, más un detalle de signo: parte del mayor y no del modelo, para que la
sociedad que no entró al filtro salga como excepción en vez de desaparecer; `control.tolerancias`
es una decisión de negocio guardada como dato; y la columna `estado` es la que acaba en el tablero. El detalle: en contabilidad las ventas son abonos y en ACDOCA viven con signo negativo, así que el testigo invierte el signo del mayor antes de comparar. Sin eso, todo sale como excepción el primer día y el testigo pierde credibilidad a la primera.
En Snowflake esto puede vivir como una *Data Metric Function* propia, programada para correr cada
vez que cambia la tabla; en Databricks, como un job después de cada carga. Si el reporte sale de una
vista CDS de S/4HANA, la fuente del cuadre es ACDOCA, la tabla de partidas contables del sistema.

## ¿Quién firma?

Esta es la otra pregunta que deja el comentario, y se me hace que es la que más discusión va a
generar.

Mi respuesta corta: **TI es responsable de que el testigo exista y corra. El negocio es dueño de que
el número signifique lo que dice.** La certificación la firma el dueño del dato, no el
administrador de la plataforma, y auditoría interna revisa que el control funcione.

No es ocurrencia mía. BCBS 239 pide definir los roles de propiedad y calidad del dato *«tanto para
las funciones de negocio como para las de TI»*, y le encarga al dueño de negocio que el dato siga
alineado con las definiciones. En gobierno de datos, la práctica que se apoya en el DAMA-DMBOK, el
marco más citado, separa lo mismo: el *data owner*, de negocio, responde por el dato de su dominio;
el *data steward* cuida definiciones y calidad en el día a día; el *data custodian*, de TI, se
encarga de lo técnico.

Aterrizado en una matriz de responsabilidades (quién hace, quién responde por el resultado, a quién
se consulta y a quién se informa), con un papel más que sí aparece en los proyectos: el dueño del
producto de datos, que responde por el entregable completo, del modelo al tablero.

| Actividad | Dueño de negocio (p. ej. Contraloría) | Dueño del producto de datos | Ingeniería / TI | Auditoría interna |
|---|---|---|---|---|
| Definir el KPI y su cifra control | Responde | Hace | Opina | Se entera |
| Fijar la tolerancia | Responde y hace | Opina | Se entera | Opina |
| Construir y correr el testigo | Se entera | Responde | Hace | Se entera |
| Explicar las excepciones | Responde si es de negocio | Hace | Hace si es técnica | Se entera |
| Mantener el KPI alineado al negocio | Responde | Hace | Opina | Se entera |
| Revisar que el control funcione | Opina | Opina | Se entera | Responde y hace |

[ FIGURA 3 — «¿Quién firma?»: la matriz simplificada, con la frase «TI construye el testigo; el
negocio es dueño del significado». ]

Hay una trampa en la que caemos casi todos los que venimos del lado técnico: asumir que, como
nosotros construimos el tablero, nos toca garantizar que el número sea correcto. Suena responsable,
pero no funciona. Desde TI puedo garantizar que el cálculo hace lo que dice la especificación. No
puedo garantizar que la especificación siga siendo lo que el negocio necesita después de una
reorganización que decidió dirección comercial. Por eso la alineación del KPI es del negocio y el
mecanismo que la vigila es de TI. Si falta uno de los dos, la palomita queda colgando de nadie.

## Y con la analítica conversacional, más

En un tablero al menos hay algo fijo que mirar. Cuando el negocio le pregunta en español a un
asistente y el asistente escribe la consulta cada vez, no hay un reporte que cuadrar: hay una
respuesta nueva por cada forma de preguntar.

Ahí los *benchmarks* de Genie son la herramienta correcta, con dos condiciones. La primera: que el
SQL de referencia esté conciliado contra las mismas cifras control del tablero, porque si ese SQL
está mal, el benchmark califica una respuesta contra otra respuesta. La segunda: que se corran
después de cada cambio al espacio. Hoy la documentación los plantea como algo que alguien con
permiso de edición lanza cuando quiere, y así se corren cuando alguien se acuerda.

## Lo que se lleva de aquí quien firma

Si firmas el presupuesto o el contrato de un proyecto de datos, tres cosas concretas:

1. **Que el testigo esté en el SOW y en la Definition of Done.** El SOW es el alcance que firma el
   proveedor; la *Definition of Done*, la lista de lo que tiene que cumplirse para dar un entregable
   por terminado. Pide en la propuesta las cifras control, la conciliación automática por evento, el
   inventario de testigos y el estado visible en el tablero, con horas y costo propios, no como
   «buena práctica» sin presupuesto. Y pon como criterio de aceptación el primer cierre mensual
   conciliado después del go-live, no el go-live.
2. **Que cada KPI crítico tenga un dueño con nombre.** No «Finanzas»: una persona que firma la
   tolerancia y a quien le llegan las excepciones.
3. **Que el tablero diga si cuadra.** Es la manera más barata de devolverle al negocio la certeza
   que hoy solo tiene quien cuadra a mano.

Nada de esto es tecnología nueva. Es disciplina que la auditoría y la banca ya se impusieron y que
en los proyectos de datos no hemos adoptado, porque nadie la pide en la propuesta.

Gracias a quien hizo la pregunta. El cuadre del go-live es una foto; el testigo es lo que la vuelve
película.

---

## Fuentes

- PCAOB — *AS 1105: Audit Evidence*, ¶.10 (información producida por la empresa: probar exactitud e
  integridad o los controles sobre ellas).
  https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
- PCAOB — *Spotlight: Inspection Observations Related to Auditor Use of Data and Reports*, abril de
  2024: ~17 % de los comment forms de los ciclos 2021 y 2022 con deficiencias en exactitud e
  integridad de información de la empresa; Staff Practice Alert 11; buena práctica del repositorio
  central de reportes.
  https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/data-and-reports-spotlight.pdf
- Basel Committee on Banking Supervision — *Principles for effective risk data aggregation and risk
  reporting* (BCBS 239), enero de 2013: Principio 3(c) y nota 17 (conciliación), ¶34 (roles de
  negocio y TI), ¶37 (diccionario), Principio 7 y ¶53 (inventario de reglas, reportes de
  excepción), ¶56 (materialidad).
  https://www.bis.org/publications/201301-guidelines-principles-effective-risk-data-aggregation-and-risk-reporting.pdf
- Microsoft Learn — *Endorse Fabric and Power BI items* (Promoted, Certified, Master data; revisores
  autorizados por el administrador).
  https://learn.microsoft.com/en-us/fabric/fundamentals/endorsement-promote-certify
- Databricks — *Flag data as certified or deprecated* (`system.certification_status`; asignación
  manual o por reglas de automatización sobre uso, dueño, antigüedad y etiquetas).
  https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data
- Databricks — *Genie benchmarks* (hasta 500 preguntas; calificación Good / Bad / Manual review;
  ejecución a demanda).
  https://docs.databricks.com/aws/en/genie/benchmarks
- Snowflake — *Introduction to data quality checks* (Data Metric Functions, expectations,
  calendario, Enterprise Edition).
  https://docs.snowflake.com/en/user-guide/data-quality-intro
- Snowflake — *Use SQL to set up data metric functions* (`DATA_METRIC_SCHEDULE`: cada N minutos,
  cron o `TRIGGER_ON_CHANGES`) y BCR 2025_07 (calendario por default de una hora).
  https://docs.snowflake.com/en/user-guide/data-quality-working
  https://docs.snowflake.com/en/release-notes/bcr-bundles/2025_07/bcr-2101
- SAP Help — *Governing and Publishing Data in the Catalog* (SAP Datasphere: glosario, KPIs,
  publicación de activos).
  https://help.sap.com/doc/5957319bdc7e4939a36ef363f844c60d/cloud/en-US/9a51a8731756457c935a49b5d510f63e.pdf
- DAMA International — *DAMA-DMBOK* (vía resumen de Dataversity), roles de data owner, data
  steward y data custodian.
  https://www.dataversity.net/data-concepts/what-is-the-data-management-body-of-knowledge-dmbok/
