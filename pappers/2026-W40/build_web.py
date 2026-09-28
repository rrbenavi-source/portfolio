"""Convierte draft-es.md / draft-en.md de la ed. 13 en la entrada TS del portfolio y la agrega a es.ts / en.ts."""
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).parent
WEB = HERE.parent.parent / "web" / "src"
ASSETS = WEB / "assets" / "publicaciones"
SLUG = "cuadro-en-el-go-live-y-hoy"

META = {
    "es": {
        "subtitle": "Calidad de Datos · Gobierno",
        "title": "Cuadró en el go-live. ¿Y hoy?",
        "role": "Autor: Ricardo Benavides",
        "lead": "Casi todas las plataformas de datos ya te dejan ponerle a un modelo la palomita de «certificado». Ninguna te obliga a demostrar que hoy la merece.",
        "summary": "Los proyectos de datos cuadran el número el día del go-live y luego no dejan nada que lo siga cuadrando. Da igual si el dato vive en BW/4HANA, Databricks o Snowflake, o si se consume en SAC, Power BI o Genie: los sellos de certificación dicen quién opinó que el dato era confiable, no que hoy lo sea. Esta edición toma lo que la auditoría (PCAOB AS 1105) y la banca (BCBS 239) ya resolvieron, lo aterriza en un testigo de seis puntos con su código SQL, y contesta quién lo firma: TI construye y corre el testigo, el negocio es dueño del significado y auditoría interna revisa que el control funcione.",
        "tags": ["Calidad de Datos", "Gobierno de Datos", "Conciliación", "SAP", "Databricks", "Snowflake", "Power BI"],
        "sources": "Fuentes",
        "code_label": "SQL · el testigo",
        "sfx": "",
        "figs": [
            ("fig-palomita.png",
             "Tabla de cinco herramientas (Power BI y Fabric, Databricks Unity Catalog, Genie, Snowflake y SAP Datasphere) con el sello que ofrece cada una, qué certifica y qué no hace; abajo, resaltado, el testigo: compara el KPI contra el mayor después de cada cambio y dice si hoy cuadra.",
             "Un sello dice quién opinó que el dato era confiable. Un cuadre demuestra que hoy lo es."),
            ("fig-testigo.png",
             "La consulta SQL del testigo con cuatro anotaciones numeradas: parte del mayor con LEFT JOIN, invierte el signo de ACDOCA, la tolerancia que firma el negocio y el estado que se publica. Abajo, cómo se ve en el tablero: tres sociedades OK y una sociedad nueva como excepción.",
             "La consulta es lo de menos. Lo que importa es que corre sola después de cada cambio y que el tablero dice si hoy cuadra."),
            ("fig-quien-firma.png",
             "Matriz de responsabilidades con seis actividades y cuatro papeles: dueño de negocio, dueño del producto de datos, ingeniería/TI y auditoría interna; marca quién responde, quién hace y a quién se consulta o se informa.",
             "TI construye el testigo; el negocio es dueño del significado."),
        ],
    },
    "en": {
        "subtitle": "Data Quality · Governance",
        "title": "It reconciled at go-live. What about today?",
        "role": "Author: Ricardo Benavides",
        "lead": "Almost every data platform now lets you put a \"certified\" checkmark on a model. None of them makes you prove it still deserves it today.",
        "summary": "Data projects reconcile the number on go-live day and then leave nothing behind to keep reconciling it. Whether the data lives in BW/4HANA, Databricks or Snowflake, and whether it's consumed in SAC, Power BI or Genie, certification badges say who thought the data was trustworthy, not that it is today. This edition takes what audit (PCAOB AS 1105) and banking (BCBS 239) already solved, turns it into a six-point witness with its SQL, and answers who signs for it: IT builds and runs the witness, the business owns the meaning, and internal audit reviews that the control works.",
        "tags": ["Data Quality", "Data Governance", "Reconciliation", "SAP", "Databricks", "Snowflake", "Power BI"],
        "sources": "Sources",
        "code_label": "SQL · the witness",
        "sfx": "-en",
        "figs": [
            ("fig-palomita-en.png",
             "Table of five tools (Power BI and Fabric, Databricks Unity Catalog, Genie, Snowflake and SAP Datasphere) with the badge each one offers, what it certifies and what it doesn't do; below, highlighted, the witness: it compares the KPI against the ledger after every change and says whether it reconciles today.",
             "A badge says who thought the data was trustworthy. A reconciliation proves it is today."),
            ("fig-testigo-en.png",
             "The witness SQL query with four numbered annotations: starts from the ledger with a LEFT JOIN, flips the ACDOCA sign, the tolerance the business signs, and the status that gets published. Below, how it looks on the dashboard: three company codes OK and a new one as an exception.",
             "The query is the least of it. What matters is that it runs on its own after every change and the dashboard says whether it reconciles today."),
            ("fig-quien-firma-en.png",
             "Responsibility matrix with six activities and four roles: business owner, data product owner, engineering/IT and internal audit; it marks who is accountable, who does the work, and who is consulted or informed.",
             "IT builds the witness; the business owns the meaning."),
        ],
    },
}


def inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


def link(url: str) -> str:
    host = urlparse(url).netloc.removeprefix("www.")
    return f'<a href="{url}" target="_blank" rel="noopener">{host}</a>'


def parse(md: str, meta: dict) -> list[dict]:
    body = md.split("\n## ", 2)[2]  # quita el título y el subtítulo largo (ya van como lead)
    intro, rest = md.split("\n## ", 2)[1].split("\n", 1)[1], body
    chunks = [("", intro)] + [
        (sec.split("\n", 1)[0].strip(), sec.split("\n", 1)[1] if "\n" in sec else "")
        for sec in ("## " + rest).split("\n## ")
    ]
    blocks: list[dict] = []
    fig_i = 0
    for heading, text in chunks:
        heading = heading.removeprefix("## ").strip()
        if heading in ("Fuentes", "Sources"):
            items = []
            for raw in re.split(r"\n- ", "\n" + text.strip())[1:]:
                lines = [ln.strip() for ln in raw.strip().splitlines()]
                urls = [ln for ln in lines if ln.startswith("http")]
                desc = " ".join(ln for ln in lines if not ln.startswith("http"))
                items.append(inline(desc) + " " + " · ".join(link(u) for u in urls))
            blocks.append({"type": "list", "heading": meta["sources"], "items": items})
            continue
        paras: list[str] = []
        pending_heading = heading or None

        def flush():
            nonlocal paras, pending_heading
            if paras:
                blk = {"type": "prose"}
                if pending_heading:
                    blk["heading"] = pending_heading
                    pending_heading = None
                blk["body"] = paras
                blocks.append(blk)
                paras = []

        text = text.replace("\n---\n", "\n").strip()
        for para in re.split(r"\n\s*\n", text):
            para = para.strip()
            if not para:
                continue
            if para.startswith("```"):
                flush()
                code = "\n".join(para.splitlines()[1:-1])
                blocks.append({"type": "code", "label": meta["code_label"], "code": code})
            elif para.startswith(">"):
                flush()
                q = " ".join(ln.lstrip("> ").strip() for ln in para.splitlines())
                blocks.append({"type": "quote", "text": inline(q)})
            elif para.startswith("[ FIG"):
                flush()
                src, alt, cap = meta["figs"][fig_i]
                fig_i += 1
                blocks.append({"type": "figure", "src": src, "alt": alt, "caption": cap})
            elif para.startswith("|"):
                continue  # la matriz va como figura 3
            elif re.match(r"^\d+\. ", para):
                flush()
                items = [" ".join(ln.strip() for ln in it.splitlines())
                         for it in re.split(r"\n(?=\d+\. )", para)]
                blocks.append({"type": "list", "items": [inline(re.sub(r"^\d+\. ", "", it)) for it in items]})
            else:
                paras.append(inline(" ".join(ln.strip() for ln in para.splitlines())))
        flush()
    assert fig_i == 3, f"se esperaban 3 figuras, hubo {fig_i}"
    return blocks


def entry_ts(lang: str) -> str:
    m = META[lang]
    md = (HERE / f"draft-{lang}.md").read_text()
    entry = {
        "idx": "15",
        "slug": SLUG,
        "subtitle": m["subtitle"],
        "title": m["title"],
        "role": m["role"],
        "meta": "2026",
        "hero": f"brujula-cover-13{m['sfx']}.png",
        "lead": m["lead"],
        "summary": m["summary"],
        "tags": m["tags"],
        "body": parse(md, m),
    }
    js = json.dumps(entry, ensure_ascii=False, indent=2)
    return "\n".join("      " + ln for ln in js.splitlines()) + ","


def insert(lang: str):
    p = WEB / "i18n" / f"{lang}.ts"
    s = p.read_text()
    if f'"slug": "{SLUG}"' in s:
        raise SystemExit(f"{p.name}: la entrada ya existe")
    anchor = "\n    ],\n  },\n  contacto: {"
    assert s.count(anchor) == 1, f"{p.name}: no encontré el cierre de publicaciones"
    s = s.replace(anchor, "\n" + entry_ts(lang) + anchor)
    p.write_text(s)
    print("ok", p.name)


def copy_assets():
    for sfx in ("", "-en"):
        for name in ("fig-palomita", "fig-testigo", "fig-quien-firma", "brujula-cover-13"):
            shutil.copy2(HERE / f"{name}{sfx}.png", ASSETS / f"{name}{sfx}.png")


if __name__ == "__main__":
    copy_assets()
    insert("es")
    insert("en")
