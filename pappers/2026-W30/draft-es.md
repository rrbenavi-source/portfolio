# El eval verde es el nuevo "200 OK"

### Por qué medir que un agente pasó no es medir que hizo lo correcto

_Borrador semilla — Idea 1 del digest W30. Formato: opinión / autoridad, 2–3
páginas. Pendiente de `papper-editor` (rigor y estructura) y `papper-humanizer`
(voz). No es texto final._

---

Hay un número de esta semana que debería incomodar a cualquiera que esté
poniendo agentes en producción: la mitad de las empresas desplegó un agente que
**pasó sus propios evals internos y después falló frente a un cliente**. Un
cuarto lo vivió más de una vez. Y sin embargo, dos tercios ya permiten —o están
construyendo hacia— desplegar cambios a producción con la evaluación automática
como único gate, sin un humano revisando. Solo el 5% dice confiar plenamente en
esos evals.

Lo leo y pienso en un patrón que la ingeniería de datos conoce desde hace veinte
años: un HTTP 200 con la respuesta vacía se ve idéntico a una llamada que
funcionó. El status dice "todo bien". El contenido dice otra cosa. Nadie que haya
operado un pipeline serio confunde las dos cosas. Un eval en verde es, hoy, ese
mismo 200: una señal de que *el proceso terminó*, no de que *el resultado es
correcto*.

## Pasó la prueba no es hizo lo correcto

El error de fondo es de medición, no de tecnología. Estamos tratando un pass/fail
al final del proceso como si fuera una prueba de correctitud, cuando en realidad
es una prueba de terminación. El propio dato de la encuesta lo confirma desde otro
ángulo: el 51% de las empresas monitorea únicamente si el agente *funciona*
—uptime, trazas, logs del gateway— y apenas el 23% monitorea si sus respuestas
son *correctas*. Tres de cada cuatro organizaciones tienen visibilidad de que el
sistema está de pie y de cuánto cuesta, y toman la correctitud de sus respuestas
como acto de fe.

Esto no es un problema de cobertura que se arregle con más tests. El defecto más
citado por las propias empresas es que sus evaluaciones "no se alinean con los
resultados del mundo real". Es un problema de *tipo* de prueba. Puedes tener mil
casos de eval y todos verdes, y aun así el agente hace algo que ningún caso
anticipó, porque el agente es un sistema path-dependent: una sola llamada a una
tool, un paso de compresión de contexto, una recuperación de error, cambia todo
lo que sigue. Como bien resume la gente que trabaja en trazas de agentes, el
resultado final pass/fail no basta; necesitas el **trace completo** como capa de
evidencia — dónde se desvió, qué paso quemó los tokens, si el cambio de prompt
mejoró el sistema o solo tuvo suerte. La evaluación real vive en el camino, no en
el destino.

## El gate que SAP ya tenía

Aquí es donde la disciplina de datos "aburrida" tiene algo que decir. En un
entorno serio no publicas un reporte financiero porque el job terminó en verde.
Lo publicas cuando *cuadra*: control de totales, reconciliación contra la fuente,
un cierre que hace match, y un dueño que firma. Ese es un gate de **correctitud**,
no de éxito. La diferencia no es burocracia; es la distinción entre "el proceso
corrió" y "el número es defendible ante un auditor". Cuando migramos cientos de
reportes, el trabajo duro nunca fue que el pipeline corriera —eso es lo fácil—;
fue demostrar que el número de destino era el mismo que el de origen, y poder
explicar cada diferencia.

Los agentes no cambian esa exigencia, la intensifican. Un buen ingeniero que
revisa el trabajo de un agente aprende rápido la misma lección que aprendemos con
nuestro propio código asistido por IA: un árbol de git limpio no es un estado
known-good. El agente puede crear archivos, luego borrarlos porque nada los
referencia, y dejarte un diff neto de cero que no te dice nada de lo que
realmente pasó. El resumen que el modelo escribe en el chat es una *narrativa*;
el diff es lo que *hizo*. Todo el riesgo vive en la brecha entre ambos, y esa
brecha es justo donde tiene que estar tu atención. La versión agéntica de este
principio es simple: lee la evidencia, no el resumen.

## El error caro no es automatizar el deployment, es automatizar la confianza

Nada de esto es un argumento contra la automatización. El human-in-the-loop no
tiene que revisar cada respuesta de cada agente para siempre; eso no escala y no
es la propuesta. El punto es más fino y más incómodo: **el orden importa**. Las
empresas están removiendo el gate humano *antes* de que sus evals reflejen la
realidad. Están automatizando la decisión de deployment sobre la base de una
prueba en la que ellas mismas no confían. Eso no es madurez operativa; es
institucionalizar la falsa confianza, y por diseño hace que los fallos de la
mitad de las empresas escalen en vez de encogerse.

La secuencia correcta es al revés. Primero instrumentas correctitud en
producción —no uptime, correctitud—: chequeos de calidad sobre el tráfico vivo,
trazas que puedas consultar y reproducir, y un umbral por debajo del cual la
salida no toca una decisión de negocio sin firma humana. Después, cuando puedas
demostrar con datos de producción que el eval predice el resultado real, quitas
al humano de los casos de bajo riesgo. No al revés. Probar tus evaluaciones
contra resultados de producción, y no contra benchmarks internos, es el paso que
casi nadie está dando y el único que convierte el "confío" en algo verificable.

Para quien lidera un equipo, la conclusión es directa y va contra la corriente
del momento: automatizar el deployment de un agente es fácil, casi gratis.
Automatizar la *confianza* en que ese agente hace lo correcto es el trabajo real,
y es donde está el costo si te lo saltas. El human-in-the-loop bien puesto no
frena la escala. Es exactamente lo que te permite decir "sí, a producción" sin
apostar la operación a un semáforo que tú mismo no crees.

Un eval verde no es un agente que funciona. Es un 200. Antes de quitar al humano
que lee el cuerpo de la respuesta, asegúrate de que alguien —o algo— sigue
comprobando que no viene vacío.

---

_Fuentes base (ver `digest.md` para detalle):_
- _VentureBeat, "The agent evaluation gap" (16-jul-2026)._
- _VentureBeat, "Wall Street is debating the AI buildout…" (10-jul, act. 14-jul-2026) — monitoreo de calidad vs uptime._
- _Databend, "Trace is Evals" (2-jul-2026) — el trace como capa de evidencia._
- _philliant, "The Danger of Trusting the Agent" (8-jul-2026) — clean tree ≠ known-good; lee el diff._
