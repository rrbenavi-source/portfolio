# Pappers — pipeline semanal

Sistema de producción de un papper semanal. Ver spec:
`docs/superpowers/specs/2026-07-03-weekly-papper-pipeline-design.md`.

## Uso
- **Fase 1 (lunes 9:30, automática):** launchd corre `/papper-digest` → `pappers/AAAA-Www/digest.md` + borrador semilla.
- **Fase 2 (cuando estés listo):** corre `/papper` → elige idea → editor → humanizer → EN → apruebas → render PDF+web+LinkedIn.

## Estructura semanal
`pappers/AAAA-Www/`: `digest.md`, `draft-es.md`, `draft-en.md`, `edit-notes.md`,
`papper-es.pdf`, `papper-en.pdf`, `linkedin-es.md`, `linkedin-en.md`.

## Config
- `sources.yaml` — fuentes por categoría (edítalo cuando quieras).
- `voice-profile.md` — tu voz autoral para el humanizer.
