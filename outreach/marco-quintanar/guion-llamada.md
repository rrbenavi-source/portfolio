# Guión de primera llamada — Marco Quintanar

**Objetivo de la llamada:** entender su entorno real y salir con un SOW chico y
cerrado propuesto. No es una llamada de demo ni de capacidades.

**Fuente:** `dossier.md`, bloques 4 (dolor con confianza), 7 (objeciones), 9 (ruta de
compra).

**Regla que gobierna todo el guión:** nada etiquetado `Inferido` o `Especulativo` en
el bloque 4 se afirma. Se pregunta. Él tiene los datos; nosotros la hipótesis.

---

## 1. Preguntas de descubrimiento

En este orden. Las primeras cuatro son las que importan; las últimas dos dependen de
cómo vaya.

**1. ¿Cuántos sistemas fuente terminan alimentando la capa analítica del VECE COE?**
Abre el mapa sin asumir nada. En Johnson Controls manejó 34 ERPs, así que la pregunta
le resulta natural y no invasiva.

**2. ¿SAP está en ese conjunto? ¿Quién lo opera hoy — equipo interno, un integrador,
o el corporativo global?**
Esta es LA pregunta. Todo el encaje de D&C depende de la respuesta. Está etiquetada
`Inferido` en el dossier: se pregunta, no se da por hecho.

**3. Cuando un número del lakehouse no cuadra con el del ERP, ¿quién lo reconcilia
hoy y cuánto tarda?**
Aquí aparece el dolor real, si existe. Escuchar más que hablar.

**4. ¿Quién firma que el número es correcto antes de que llegue a un ejecutivo?**
Separa "el proceso corrió" de "el número es defendible". Es el gate de correctitud —
y es el terreno donde D&C tiene algo que ofrecer que su equipo no cubre.

**5. ¿Qué es lo que hoy está frenando el roadmap de 18 meses?**
Pregunta abierta de prioridades. Sirve para saber dónde cabe un primer trato.

**6. Sobre el rol que traes abierto: ¿qué trabajo concreto está esperando a esa
persona?**
⚠️ **SOLO si él saca el tema de la vacante.** Nunca se introduce desde nuestro lado —
regla 2 del bloque 8. Si él la menciona, esta pregunta abre naturalmente la
conversación de Fábrica de Datos.

---

## 2. Señales de compra

**Verde — avanzar hacia alcance:**

- Describe un caso concreto de reconciliación que le duele (con nombre y fecha, no en
  abstracto)
- Menciona plazos, cierres o auditorías
- Pregunta cómo cobramos o cómo se estructura un trato
- Mete a alguien más a la conversación, o propone una segunda llamada con su equipo
- Corrige nuestra hipótesis con detalle — significa que está pensando en serio

**Roja — no forzar:**

- Pide "una propuesta" sin haber conversado nada del problema (está delegando el
  rechazo a procurement)
- Deriva a compras de inmediato
- Habla solo en condicional: "si algún día", "eventualmente", "cuando tengamos
  presupuesto"
- Da respuestas cortas y genéricas a las preguntas 2 y 3

Ante señal roja: cerrar bien, agradecer, no insistir. Este contacto vale más a largo
plazo que un trato forzado.

---

## 3. Aterrizaje en alcance cerrado

Marco viene de procurement: insourceó un BPO de $5M, corrió RFPs de 400 carriers y
negoció $3B. **Quiere** un SOW con precio y fin — no hay que convencerlo del formato,
hay que llegar con él.

**Qué proponer:** un primer trato chico, cerrado y evaluable en semanas. Ejemplo
concreto según lo que aparezca en el descubrimiento:

> Diagnóstico de una sola fuente SAP, con entregable de reconciliación
> origen↔destino documentada: qué cuadra, qué no, y por qué. Alcance fijo, precio
> fijo, X semanas.

**Por qué chico:** pasa por debajo de la fricción de vendor onboarding de una cuenta
global, y es fácil de aprobar y de evaluar. El marco grande —o la Fábrica de Datos
sobre un dominio completo— se conversa después de una entrega que sostenga, nunca
antes (bloque 9 del dossier).

**Cerrar la llamada con tres cosas definidas:**

1. Qué incluye exactamente el primer alcance
2. Quién firma y en qué plazo
3. Cuándo volvemos a hablar

Si no salen las tres, la llamada no terminó — se agenda seguimiento con fecha.

**Sobre vendor onboarding:** si lo saca, no minimizarlo. Él conoce ese proceso mejor
que nadie. Reconocerlo y proponer el alcance chico precisamente como forma de
evitarlo al principio.

---

## 4. Objeciones en vivo

Versión hablada, 2–3 líneas. En llamada no se recita un párrafo. Detalle completo en
el bloque 7 del dossier.

**"Ya tenemos equipo de datos."**
> Y por lo que vi, fuerte del lado de Databricks. No es esa cancha. Lo que cubro es
> la capa SAP —BW/4HANA, ECC, reportes Z— que es otra especialidad.

**"¿Por qué no contrato a alguien?"**
> Contratar resuelve headcount, no integridad de dato. Lo nuestro no es meter una
> persona bajo tu mando: es recibir un requerimiento y devolver el producto con
> garantía de integridad y calidad, facturado por uso.

**"Trabajas en Heineken, ¿esto es un side business?"**
> Te lo digo de frente: soy socio de D&C y dirijo Data Engineering SAP en Heineken.
> Esa es la credencial — no te hablo de un caso que vi de lejos, sino de la
> operación que corro.

**"Meter un proveedor mexicano a una cuenta global es fricción."**
> Ese proceso lo conoces mejor que yo. Por eso propongo empezar chico y cerrado, no
> con un contrato marco.

**"¿Qué casos tienen fuera de Heineken?"**
> D&C tiene 15 años y cartera Tier-1, pero lo que puedo documentar con cifras y
> sostener si me lo cuestionas es Heineken, porque es lo que yo operé. No te voy a
> inflar casos de otros.

---

## 5. Lo que NO se hace en esta llamada

- Presentar el deck completo de D&C
- Hablar de capacidades antes de entender su problema
- Prometer que el vendor onboarding "no es problema"
- Dar un precio sin alcance definido
- Mencionar su vacante si él no la sacó
