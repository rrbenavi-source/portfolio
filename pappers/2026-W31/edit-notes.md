# Edit notes — W31 "Migrar un reporte Z no es traducir ABAP" (papper-editor, fase 2)

## CRÍTICO
Ninguno. Verificación de los tres datos sensibles:
- **Note 3255746 / ODP-RFC:** el draft lo enuncia correctamente (bloqueo técnico
  desde jun-2026 solo para aplicaciones no-SAP, opt-out hasta 31-dic-2026),
  consistente con la fuente SAPinsider verificada en el digest.
- **Fechas EoM de BW:** confirmadas contra BARC (BW 7.5 mainstream fines de
  2027, extendido 2030; BW/4HANA 2040). Correctas en intro y fuentes.
- **Protiviti 3–4×:** correctamente atribuida como estimación ("Protiviti
  estimó… esa estimación es creíble, pero con un matiz"), no como medición.

## IMPORTANTE (aplicado)
1. **Intro, párr. 1:** "esa promesa dejó de ser opcional" → "la decisión dejó de
   ser opcional". Lo que expira no es la promesa del vendor, es la decisión de
   migrar; el salto lógico debilitaba la apertura.
2. **Sección final:** eliminado "que se está imponiendo en el mercado" (claim de
   mercado sin fuente). Queda como juicio profesional propio.
3. **Fuentes:** verificadas las dos URLs marcadas; quitadas ambas marcas
   "_(verificar URL directa)_". BARC ahora con título y autora reales (*End of
   Maintenance for SAP BW: What's Next?*, Larissa Baier). El post de SAP
   Community existe en la URL exacta citada.
4. **Metadata:** estado actualizado a "editado, pendiente pase de voz → EN".

## PENDIENTE DE DECISIÓN DE RICARDO
- **IVA vs IEPS:** el digest dice que el caso real es IEPS/RTDs; el draft dice
  "IVA". _Resolución posterior (orquestador): NO es alteración — el POC tiene
  tres workstreams y el report Z migrado es el de facturado+IVA (workstream b);
  el cálculo IEPS es otro workstream (a). "IVA" es factualmente correcto._
- **"Miles de organizaciones" (intro):** defendible por la base instalada de BW,
  pero es la afirmación menos sustentada del texto. Opción conservadora:
  "muchas organizaciones".

## MENOR (no aplicado — para el humanizer o criterio de Ricardo)
- "documentado/documenta" aparece 6+ veces; es temático (el acta de defunción)
  pero conviene variar alguna.
- "seguridad row-level" es consistente con W30; se mantiene.
- La repetición deadline ODP + EoM BW en intro y cierre funciona como bookend
  (el cierre añade el giro "la fecha límite es para decidir la arquitectura de
  extracción, no para congelar reportes"); no es conclusión-que-reformula-intro.

## Chequeos estructurales
- **Tesis:** el blockquote (vive / muere / nunca estuvo viva) se sostiene
  sección por sección: dead code (muere) → lógica en configuración y FM perdido
  (vive fuera del código) → cadena nunca ejecutada (nunca estuvo viva) → método
  spec + golden case → escala a portafolio.
- **Extensión:** ~1,690 palabras de cuerpo — dentro de la meta 1,400–1,700.
- **Confidencialidad:** limpio. Sin cliente, sociedad, marcas, nombres de
  objetos Z, importes ni UUIDs. Solo tablas/transacciones estándar. AUGBL
  correctamente anonimizado como "el campo que encadena la navegación".
- **Citas:** todo claim externo tiene fuente; el único dato huérfano detectado
  (práctica de mercado) fue corregido.

## Fuentes verificadas en esta pasada
- BARC — End of Maintenance for SAP BW: What's Next? — https://barc.com/end-of-maintenance-sap-bw/
- BARC Executive Briefing — SAP BW End of Life 2027 — https://barc.com/sap-bw-end-of-life-2027-data-architecture-analytics-ai/
- SAP Community — The SAP BW Migration Decision: Your Real Options in 2026 — https://community.sap.com/t5/technology-blog-posts-by-members/the-sap-bw-migration-decision-your-real-options-in-2026/ba-p/14359306
