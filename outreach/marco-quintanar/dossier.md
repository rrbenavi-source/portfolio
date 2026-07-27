# Dossier de cuenta — Marco Quintanar (Honeywell)

**Fecha:** 2026-07-27
**Estado:** documento de trabajo interno. No se envía a nadie, es la fuente de
verdad para redactar el mensaje de LinkedIn, el one-pager y el guión de llamada.
**Origen:** Marco Quintanar agregó a Ricardo Benavides en LinkedIn tras la
publicación de la edición 03 del newsletter Brújula (papper W30).

---

## 1. Identidad y mandato

| Campo | Dato |
|---|---|
| Nombre | Marco Quintanar |
| Perfil | `linkedin.com/in/marco-quintanar-m/` |
| Puesto | Director, Data Science, AI Engineering & Transformation |
| Empresa | Honeywell (feb 2024 – actualidad) |
| Ubicación | Monterrey, Nuevo León · híbrido |
| Área | VECE COE (Value Engineering / Cost Engineering Center of Excellence) |
| Alcance | Global Industrials |
| Red | 5,078 seguidores · +500 contactos · 29+ contactos en común con Ricardo |
| Grado | 1er (ya conectados — DM directo, sin límite de 300 caracteres) |

*(Confirmado — LinkedIn, consultado 2026-07-27)*

---

## 2. Stack declarado (palabras textuales)

Lo que él mismo describe en su experiencia de Honeywell, sin parafrasear:

Azure · Databricks · Delta Lake **Medallion** · **Unity Catalog** · data quality
frameworks · lineage · Databricks AutoML · MLflow · Model Registry · PSI drift
monitoring · Databricks **Vector Search** · **Mosaic AI Model Serving** ·
Mendix (low-code) vía REST.

*(Confirmado — descrito por él en su propio perfil)*

---

## 3. Trayectoria y lo que revela

| Periodo | Rol | Señal relevante |
|---|---|---|
| 2013–2018 | Carrier México — Supply Chain / Indirect Procurement | **Origen en negocio, no en TI** |
| 2019–2021 | Johnson Controls — Sr Mgr Logistics Procurement Analytics COE | Plataforma de $900M; migración a Azure Synapse; Informatica CDQ + dbt; Jaggaer ASO |
| 2021–2024 | Johnson Controls — Director Digital Transformation & Analytics (Global Sourcing COE) | Insourcing de BPO de $5M → $2M ahorro anual duro; equipo de +30 desde cero; **34 ERPs, 500+ proveedores, 20,000+ partes**; Keelvar sobre portafolio de $3B |
| 2024–hoy | Honeywell — Director DS/AI Eng & Transformation | Infraestructura AI-Ready sobre Azure/Databricks; sistema ML de dos modelos; motor de detección de ideas duplicadas sobre pipeline con **$1B+ de valor de oportunidad**; roadmap a 18 meses |

*(Confirmado — LinkedIn, consultado 2026-07-27)*

**Lo que revela esta trayectoria** (lectura directa de los datos de arriba, sin
extrapolar hacia Honeywell — eso se etiqueta aparte en el bloque 4):

- Nunca fue un técnico que subió a director. Es un operador de negocio
  (procurement, sourcing, logística) que construyó capacidad técnica encima. Su
  perfil está escrito en dólares — $2M de ahorro, $3B de spend, $1B+ de
  oportunidad — no en arquitectura. Eso condiciona cómo hay que hablarle: un
  argumento de "esto no cuadra y eso cuesta" entra donde un pitch de
  capacidades técnicas rebota.
- Su relación histórica con los ERPs fue siempre de **integración desde
  afuera** — 34 ERPs, lead times, freight audit, RFPs — nunca de arquitectura
  SAP por dentro.
- En trece años de perfil público, **cero menciones de SAP.** No es un hueco
  casual: es consistente en las cuatro etapas de su carrera.
- Corrió RFPs de $3B y evaluó proveedores a diario durante años. Detecta al
  instante una técnica de venta o una cifra inflada. No se le vende con
  discurso; se le demuestra criterio y se deja que él vea la aplicación.

---

## 4. Mapa de dolor con nivel de confianza

| Afirmación | Confianza | Evidencia |
|---|---|---|
| Vacante Senior AI Data Engineer abierta 2+ meses | Confirmado | Él la publicó; a los ~2 meses seguía con "Still looking for great Data Engineers!" |
| Su stack corre en niveles altos de madurez (ML productivo, Unity Catalog, Vector Search) | Confirmado | Descrito por él en su experiencia de Honeywell |
| No tiene experiencia SAP en su trayectoria | Confirmado | Cero menciones de SAP en 13 años de perfil |
| Honeywell usa SAP como fuente de manufactura/finanzas | Inferido | Industrial global de ese tamaño; alta probabilidad, no verificado |
| Su capa fuente arrastra la madurez del ecosistema AI-Ready | Especulativo | Es la tesis a validar con él, no un hecho |
| Tiene autoridad de presupuesto para servicios | Inferido | Director con COE propio y roadmap de 18 meses |

---

## 5. Su vocabulario

**Términos textuales suyos — usar sin traducir:**

`AI-Ready data` · `production-grade` · `Data Products` · `Dollar-Weighted Yield
Rate` · `Medallion` · `Unity Catalog` · `data quality frameworks` · `lineage` ·
`drift monitoring` · `Value Engineering / VECE COE`

**Términos a evitar — vocabulario de vendor genérico:**

"transformación digital" · "sinergias" · "soluciones de punta a punta" ·
"partner estratégico"

Estos términos son la firma universal del mensaje automatizado. Si aparecen,
el mensaje se lee como plantilla de LinkedIn Sales Navigator, no como algo
escrito por un par.

---

## 6. Encaje D&C ↔ su stack (complemento vs. redundancia)

| Complemento | Redundante | Paralelo |
|---|---|---|
| Capa SAP: BW/4HANA, ECC, extractores, ODP, reportes Z — la pieza que su stack no tiene y su trayectoria confirma que nunca tuvo | Databricks / Azure / ML — él ya lo corre y lo hace bien (AutoML, MLflow, Model Registry, drift monitoring); no hay nada que D&C le aporte aquí que él no tenga resuelto | AI/BI Genie — ambos lo usan (D&C sobre su stack Databricks, él dentro de Honeywell); es punto de conversación técnica entre pares, no un gancho de venta |

**Lectura para el mensaje:** no se le ofrece algo ajeno a su mundo. Se le
ofrece la pieza faltante de su propio stack — la capa fuente SAP que, *si el
patrón que se observa en otros industriales le aplica a él* (Especulativo,
ver bloque 4: es la tesis a validar con él, no un hecho asumido), es la que
sostiene o limita el nivel de madurez que ya construyó del lado de
Databricks. Ricardo no llega afirmando que su ecosistema la necesita; llega
con la pregunta de si el patrón le aplica, y deja que Marco lo confirme o lo
descarte.

---

## 7. Objeciones esperadas y respuesta

**1. "Ya tenemos equipo de datos."**
No compito con tu equipo. Tu equipo vive del lado de Databricks/Azure y ahí
está fuerte — eso lo veo en tu propio perfil. Lo que cubro es la capa SAP que
no aparece en la trayectoria de nadie de tu área: BW/4HANA, ECC, extractores,
reportes Z. No es la misma cancha.

**2. "¿Por qué no contrato a alguien?"**
Porque contratar resuelve headcount, no integridad de dato. La Fábrica de
Datos no es meter una persona bajo tu mando — eso es staffing, y ya sé que
eso te tiene saturado de reclutadoras con tu vacante abierta. Es un equipo en
pool que recibe un requerimiento y responde por integridad, calidad y consumo
del producto de datos que entrega, facturado por uso. Es un producto con
garantía, no una persona que hay que reclutar, entrenar y retener.

**3. "Trabajas en Heineken, ¿esto es un side business?"**
Te lo digo de frente: soy socio de D&C Solutions y, en paralelo, dirijo el
equipo de Data Engineering SAP en Heineken México. No es un side business —
es exactamente la credencial operativa. No te hablo desde un caso que vi de
lejos como proveedor; te hablo desde la operación que corro todos los días:
300+ reportes migrados de SAP ECC a Databricks, −50% de licenciamiento, un
equipo de ~15 personas. Esas son las cicatrices, no un case study.

**4. "Somos cuenta global, meter un proveedor mexicano es fricción."**
Tú conoces ese proceso mejor que yo — corriste RFPs de $3B y sourcing global
en Johnson Controls. No te lo voy a explicar. Lo que propongo es empezar con
un alcance chico y cerrado, no con un contrato marco: algo que quepa por
debajo del radar de fricción de onboarding y que se pueda evaluar en semanas,
no en trimestres.

**5. "¿Qué casos tienen fuera de Heineken?"**
Honestidad completa: D&C tiene 15 años y cartera Tier-1 — FEMSA, CEMEX,
Metalsa, Deacero, Copamex, Nemak — pero el material que puedo documentar con
cifras y detalle es Heineken, porque es la operación que yo dirijo. No te voy
a inflar casos de otros clientes que no operé de primera mano. Prefiero que
confíes en lo que puedo sostener si me lo cuestionas, no en un logo.

---

## 8. Qué no decirle

1. **No diagnosticar Honeywell.** No se conoce el estado real de su capa SAP.
   Afirmarlo desde afuera, a quien lleva 2.5 años construyendo esa
   infraestructura, ofende.
2. **No mencionar su vacante abierta.** Es la trampa mayor: activa de
   inmediato el reflejo de "otro que me quiere vender gente".
3. **No pedir llamada en el primer contacto.** Nada que le cueste calendario
   antes de que haya interés real.
4. **No adjuntar deck ni one-pager sin que lo pida.** Convierte la
   conversación en pitch.
5. **No liderar con HEINEKEN.** Es su empleador y el único caso documentado;
   invita la pregunta equivocada demasiado pronto en la conversación.
6. **No usar "vi tu perfil y me pareció impresionante" ni frases equivalentes.**
   Es la firma universal del mensaje automatizado.
7. **No traducir sus términos al español.** `AI-Ready data`, `production-grade`,
   `Data Products`, `Unity Catalog`, etc. se usan tal cual — traducirlos
   suena a que no se domina el vocabulario real de su mundo.

---

## 9. Ruta de compra en Honeywell

Marco viene de procurement, no de TI — insourceó un BPO de $5M, corrió RFPs de
400 carriers y negoció un portafolio de $3B en Johnson Controls. Habla el
idioma nativo de comprar servicios: **SOW, alcance, precio y fin.** No es una
cuenta que se cierre con un contrato marco de entrada; es una cuenta que se
gana con un primer trato pequeño, cerrado y medible, y que después escala si
el resultado sostiene.

**Secuencia recomendada:**

1. Primer trato pequeño con alcance cerrado — proyecto puntual con entregable
   definido, no compromiso abierto. Objetivo: que sea fácil de aprobar y fácil
   de evaluar en semanas.
2. Solo después de una entrega que sostenga, se conversa sobre un marco más
   amplio (proyecto recurrente o Fábrica de Datos sobre un dominio más grande).
3. La fricción de **vendor onboarding** en una cuenta global como Honeywell es
   real — proveedor mexicano pequeño entrando a un procurement corporativo.
   No se resuelve en el chat de LinkedIn ni prometiendo que "no es problema":
   se resuelve en la llamada, con Marco, que conoce ese proceso mejor que
   cualquiera que se lo explique desde afuera.

**Regla derivada:** el guión de la primera llamada debe llegar con preguntas
de descubrimiento sobre su entorno (cuántos ERPs, cómo se reconcilia hoy,
quién firma que el número cuadra) y aterrizar rápido en la propuesta de un
SOW chico — es el formato que él reconoce y aprueba, no uno que hay que
convencerlo de aceptar.
