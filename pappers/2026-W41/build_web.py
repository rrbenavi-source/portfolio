"""Convierte draft-es.md / draft-en.md de la ed. 14 en la entrada TS del portfolio y la agrega a es.ts / en.ts."""
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).parent
WEB = HERE.parent.parent / "web" / "src"
ASSETS = WEB / "assets" / "publicaciones"
SLUG = "de-la-sabana-al-agente"
COVER = "brujula-cover-14"
FIG_NAMES = ("fig-nlq-retirada", "fig-misma-pregunta", "fig-escalera")

META = {
    "es": {
        "subtitle": "Analítica · GenBI",
        "title": "De la sábana al agente",
        "role": "Autor: Ricardo Benavides",
        "lead": "En febrero de 2027 Microsoft apaga Power BI Q&A, la función con la que en 2013 prometió que cualquiera podría preguntarle a sus datos en lenguaje natural. Tableau ya retiró Ask Data y SAP, Search to Insight.",
        "summary": "Ocho generaciones de reporting, producto por producto: la sábana, la hoja de cálculo, el cubo, la capa semántica, el descubrimiento visual, el self-service en la nube, la primera ola de IA y el agente (Copilot, Genie, Snowflake, Just Ask y Joule, Tableau Pulse, Looker). Para cada una, qué análisis permite y qué no. La primera forma de preguntarle a los datos en lenguaje natural ya se retiró, y lo que pedía —sinónimos, relaciones, enseñarle a la herramienta— reaparece casi igual en «Prep data for AI». Los benchmarks muestran que el agente ya escribe buen SQL; lo difícil es que alguien sepa cuál es la respuesta correcta. Cierra con una tabla de qué generación comprar según la pregunta y tres recomendaciones para quien firma el presupuesto.",
        "tags": ["GenBI", "Analítica", "Capa Semántica", "Power BI", "SAP Analytics Cloud", "Databricks", "Snowflake", "Tableau"],
        "sources": "Fuentes",
        "code_label": "Código",
        "sfx": "",
        "figs": [
            ("Línea de tiempo de 2013 a 2027 con tres funciones de pregunta en lenguaje natural: Power BI Q&A (septiembre de 2013 a febrero de 2027, reemplazo Copilot), Tableau Ask Data (2019 a febrero de 2024, reemplazo Tableau Pulse) y SAC Search to Insight (retirado en Q4 2024, reemplazo Just Ask y Joule). Abajo, la tabla de migración de Microsoft: Q&A Setup pasa a Prep data for AI.",
             "El buscador por palabras clave se retiró. La tarea de enseñarle el vocabulario del negocio pasó, casi igual, a la generación siguiente."),
            ("La misma pregunta, venta del trimestre contra el mismo trimestre del año pasado por región, escrita en cuatro lenguajes: SQL de la sábana y el universo, MDX del cubo con PARALLELPERIOD, una medida DAX con SAMEPERIODLASTYEAR y una verified query del modelo semántico de Snowflake con el campo verified_by resaltado.",
             "En los tres primeros, la definición vive en el código. En el último, además tiene nombre: alguien la verificó."),
            ("Escalera de ocho generaciones de reporting —la sábana, la hoja de cálculo, el cubo, la capa semántica, el descubrimiento visual, el self-service, la primera ola de IA y el agente— con productos de ejemplo, el análisis que permite cada una y lo que no permite.",
             "El producto cambió ocho veces. La tarea de decidir qué significa cada palabra del negocio nunca se fue."),
        ],
    },
    "en": {
        "subtitle": "Analytics · GenBI",
        "title": "From the bedsheet report to the agent",
        "role": "Author: Ricardo Benavides",
        "lead": "In February 2027 Microsoft switches off Power BI Q&A, the feature it launched in 2013 with the promise that anyone could ask their data a question in plain language. Tableau has already retired Ask Data, and SAP has retired Search to Insight.",
        "summary": "Eight generations of reporting, product by product: the bedsheet report, the spreadsheet, the cube, the semantic layer, visual discovery, cloud self-service, the first AI wave and the agent (Copilot, Genie, Snowflake, Just Ask and Joule, Tableau Pulse, Looker). For each one, what analysis it enables and what it doesn't. The first way of asking data questions in natural language has already been retired, and what it required (synonyms, relationships, teaching the tool) comes back almost unchanged in \"Prep data for AI\". Benchmarks show the agent already writes good SQL; the hard part is having someone who knows the right answer. It closes with a table of which generation to buy depending on the question, and three recommendations for whoever signs the budget.",
        "tags": ["GenBI", "Analytics", "Semantic Layer", "Power BI", "SAP Analytics Cloud", "Databricks", "Snowflake", "Tableau"],
        "sources": "Sources",
        "code_label": "Code",
        "sfx": "-en",
        "figs": [
            ("Timeline from 2013 to 2027 with three natural-language question features: Power BI Q&A (September 2013 to February 2027, replaced by Copilot), Tableau Ask Data (2019 to February 2024, replaced by Tableau Pulse) and SAC Search to Insight (retired in Q4 2024, replaced by Just Ask and Joule). Below, Microsoft's migration table: Q&A Setup becomes Prep data for AI.",
             "The keyword search engine was retired. The job of teaching it the business vocabulary moved, almost unchanged, to the next generation."),
            ("The same question, quarter sales versus the same quarter last year by region, written in four languages: SQL for the bedsheet report and the universe, MDX for the cube with PARALLELPERIOD, a DAX measure with SAMEPERIODLASTYEAR and a Snowflake semantic-model verified query with the verified_by field highlighted.",
             "In the first three, the definition lives in the code. In the last one, it also has a name: someone verified it."),
            ("Ladder of eight reporting generations (the bedsheet report, the spreadsheet, the cube, the semantic layer, visual discovery, self-service, the first AI wave and the agent) with sample products, the analysis each one enables and what it doesn't allow.",
             "The product changed eight times. The job of deciding what each business word means never went away."),
        ],
    },
}

def inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text



def table_items(para: str) -> list[str]:
    """Convierte la tabla markdown en renglones «pregunta → análisis → generación» (el portfolio no tiene tablas)."""
    rows = [ln for ln in para.splitlines() if ln.startswith("|") and not ln.startswith("|---")]
    items = []
    for ln in rows[1:]:
        q, kind, gen = (c.strip() for c in ln.strip("|").split("|"))
        items.append(f"{inline(q)} → <strong>{inline(kind)}</strong> → {inline(gen)}")
    return items


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
                alt, cap = meta["figs"][fig_i]
                src = f"{FIG_NAMES[fig_i]}{meta['sfx']}.png"
                fig_i += 1
                blocks.append({"type": "figure", "src": src, "alt": alt, "caption": cap})
            elif para.startswith("|"):
                flush()
                blocks.append({"type": "list", "items": table_items(para)})
            elif para.startswith("- "):
                flush()
                items = [" ".join(ln.strip() for ln in it.splitlines())
                         for it in re.split(r"\n(?=- )", para)]
                blocks.append({"type": "list", "items": [inline(it[2:]) for it in items]})
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
        "idx": "16",
        "slug": SLUG,
        "subtitle": m["subtitle"],
        "title": m["title"],
        "role": m["role"],
        "meta": "2026",
        "hero": f"{COVER}{m['sfx']}.png",
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
        for name in (*FIG_NAMES, COVER):
            shutil.copy2(HERE / f"{name}{sfx}.png", ASSETS / f"{name}{sfx}.png")


if __name__ == "__main__":
    copy_assets()
    insert("es")
    insert("en")
