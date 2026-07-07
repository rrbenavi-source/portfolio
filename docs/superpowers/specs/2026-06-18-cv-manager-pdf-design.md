# Spec — CV de manager, PDF premium (HTML→PDF)

**Fecha:** 2026-06-18 · **Para:** Ricardo Benavides · Proyecto: CV RB

## Objetivo
CV de manager con diseño profesional, en **PDF de alta gama** (ES + EN), consistente
con el portfolio web y con el **posicionamiento final** ("Data Architect & Data
Engineering SAP Leader", 20+ años, equipo ~15, Genie/Databricks).

## Decisiones (aprobadas)
- **Formato:** PDF de alta gama vía **HTML→PDF**. El `build_docx.py`/`.docx` actuales
  quedan intactos como respaldo editable.
- **Idiomas:** Español + Inglés (dos PDFs).
- **Posicionamiento:** wording final del web (rebrand aplicado). Se conservan hechos
  históricos: cert "SAP NetWeaver 2004s — Business Intelligence", rol "Líder Técnico BI/BPC".
- **Dirección visual:** **híbrido** — cabecera oscura de marca + cuerpo claro a dos columnas.

## Pipeline
- Fuentes: `CV/cv-es.html`, `CV/cv-en.html` (autocontenidos, print-optimizados A4).
- Render: `CV/build_pdf.sh` corre Chrome headless `--print-to-pdf` sobre cada HTML →
  `CV/CV-Ricardo-Benavides-ES.pdf` y `CV/CV-Ricardo-Benavides-EN.pdf`.
- Motor: `/Applications/Google Chrome.app/.../Google Chrome --headless`. Sin deps extra.

## Layout
- **Cabecera oscura** (full-width): nombre (serif display), título
  "Data Architect & Data Engineering SAP Leader", eyebrow, línea de contacto.
- **Cuerpo claro** a dos columnas:
  - *Sidebar (~34%)*: Contacto · Competencias (Liderazgo / Arquitectura SAP / Analítica & Cloud) ·
    Idiomas · Certificación · Formación · Clientes.
  - *Main (~66%)*: Perfil + métricas/logros · Experiencia (Heineken→CEMEX) · Caso €1.5M.
- Tipografía: serif display (Fraunces/Source Serif 4) + sans (Inter) vía Google Fonts con
  fallback de sistema. Paleta: carbón `#15171a`/`#1f2937`, verde SAP `#0F7A5A`, teal de acento,
  blanco hueso `#fbfbf9`, grafito de texto.
- Print CSS: `@page { size: A4; margin: 0 }`, `-webkit-print-color-adjust: exact`.
- Objetivo: 1 página densa pero respirable (máx. 2).

## Contenido (canónico, de web/i18n)
- Título/footer: "Data Architect & Data Engineering SAP Leader".
- Hero ES eyebrow: "Líder de Data Engineering SAP & Arquitecto de Datos · Monterrey, MX".
- Perfil: lead de `perfil.lead`. Métricas: 20+ años, €1.5M, ~15 liderados, −50% SAC.
- Experiencia Heineken lidera con Genie Sales Assistant + producto de datos SAP ECC→Databricks,
  luego SAC→AfO −50%, 300+ reportes, BW/4HANA 2023, Data Intelligence, BO→SAC.
- Resto de trayectoria: AlEn, Pueblo Bonito, Fibra Inn, CEMEX (de `trayectoria.items`).
- Caso €1.5M: `dcsol` (manufactura multi-planta HEINEKEN, €1.4M + €100k, €0 infra).
- Clientes: lista de `clients.list`. Formación + Cert + Idiomas de `trayectoria`.
- Contacto: rbenavides@dcsol.com.mx · rrbenavi@gmail.com · linkedin.com/in/rrbenavi · Monterrey, MX.

## Criterio de éxito
- Dos PDFs renderizados, A4, una página, sin overflow, colores fieles, texto seleccionable.
- Wording 100% consistente con el web. Hechos históricos preservados.
