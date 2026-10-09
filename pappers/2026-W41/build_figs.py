"""Genera las figuras y la portada de la ed. 14 (ES/EN) como HTML y las renderiza con Chrome headless."""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

HEAD = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<style>
 :root{{--bg:#14161a;--teal:#2BBD8F;--text:#ECEAE4;--dim:#A2A6AD;--faint:#71767f;--line:#2c3038;--code:#c9ced6;--red:#E0785F;--amber:#D9B45A;}}
 *{{box-sizing:border-box;margin:0;padding:0;}} body{{width:1080px;height:1350px;}}
 .f{{width:1080px;height:1350px;padding:64px 64px 60px;display:flex;flex-direction:column;font-family:Inter,sans-serif;position:relative;overflow:hidden;
   background:radial-gradient(760px 560px at 108% -8%,rgba(43,189,143,.15),transparent 58%),var(--bg);}}
 .eyebrow{{font-family:"Space Grotesk";color:var(--teal);font-weight:600;font-size:19px;letter-spacing:.2em;text-transform:uppercase;display:flex;align-items:center;gap:16px;}}
 .eyebrow .ln{{width:44px;height:2px;background:var(--teal);}}
 h2{{font-family:Fraunces,serif;font-weight:600;font-size:56px;line-height:1.06;letter-spacing:-.02em;color:var(--text);margin-top:20px;}}
 h2 .em{{color:var(--teal);font-style:italic;}}
 .lede{{font-size:21px;color:var(--dim);margin-top:12px;line-height:1.4;max-width:52ch;}}
 .kicker{{margin-top:22px;border-left:3px solid var(--teal);padding-left:22px;font-size:21px;color:var(--text);line-height:1.4;}}
 .src{{margin-top:auto;border-top:1px solid var(--line);padding-top:12px;padding-right:150px;font-size:14px;color:var(--faint);line-height:1.5;}}
 .wm{{position:absolute;right:60px;bottom:44px;font-family:Fraunces,serif;font-size:23px;color:#3a4048;}}
 {extra}
</style></head><body>
<div class="f">
  <div class="eyebrow"><span class="ln"></span>{eyebrow}</div>
  <h2>{title}</h2>
  <p class="lede">{lede}</p>
  {body}
  <div class="kicker">{kicker}</div>
  <div class="src">{src}</div>
  <div class="wm">Brújula</div>
</div></body></html>"""

# ---------- Figura 1: la escalera de ocho generaciones ----------
FIG1_CSS = """
 .tbl{margin-top:30px;display:flex;flex-direction:column;gap:10px;}
 .hdr,.row{display:grid;grid-template-columns:44px 250px 1fr 1fr;gap:0 18px;align-items:center;}
 .hdr{font-family:"Space Grotesk";font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--faint);padding:0 16px;}
 .row{border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,#1b2027,#171a1f);padding:19px 16px;}
 .num{font-family:Fraunces,serif;font-size:30px;color:var(--faint);}
 .gen{font-size:21px;color:var(--text);font-weight:600;line-height:1.15;}
 .prod{display:block;margin-top:4px;font-family:"JetBrains Mono";font-size:12.5px;font-weight:400;color:var(--teal);line-height:1.35;}
 .yes{font-size:17.5px;line-height:1.35;color:var(--text);} .yes b{color:var(--teal);font-weight:600;}
 .no{font-size:17.5px;line-height:1.35;color:#d9c9c3;}
 .row.w{border-color:rgba(43,189,143,.6);background:linear-gradient(180deg,rgba(43,189,143,.16),rgba(43,189,143,.03));}
 .row.w .num{color:var(--teal);}
"""

FIG1 = {
    "es": {
        "eyebrow": "Brújula · Edición 14",
        "title": 'Ocho generaciones, <span class="em">una</span> tarea',
        "lede": "Cada producto cambió qué pregunta puede hacer el negocio sin pedirle nada a TI. Ninguno cambió quién decide qué significa el número.",
        "hdr": ("", "Generación", "Análisis que permite", "Lo que no permite"),
        "rows": [
            ("La sábana", "COBOL · ALV · Crystal", "<b>Operativo:</b> listar, filtrar, rastrear hasta el documento", "Hacer una pregunta nueva sin pedírsela a sistemas"),
            ("La hoja de cálculo", "VisiCalc 1979 · Excel 5 1993", "<b>Escenarios</b> y tablas dinámicas sin código", "Que dos personas lleguen al mismo número"),
            ("El cubo", "Essbase · SSAS · BW/BEx", "<b>Multidimensional:</b> cortar, bajar por jerarquía, año contra año", "Preguntar lo que no se modeló"),
            ("La capa semántica", "Universo BO 1991", "<b>Ad hoc gobernado</b> con objetos de negocio", "Mantenerse sola: alguien agrega cada objeto"),
            ("El descubrimiento visual", "Polaris/Tableau 2002 · Qlik", "<b>Exploratorio:</b> mirar antes de preguntar", "Una sola verdad: cada libro, sus cálculos"),
            ("El self-service", "Power BI 2015 · Looker · SAC", "<b>Modelado propio</b> y dashboards compartidos", "Controlar la proliferación de modelos"),
            ("La primera ola de IA", "Q&amp;A · Ask Data · Search to Insight", "<b>Diagnóstico automatizado</b> y frases clave", "Conversar: sinónimos capturados a mano"),
            ("El agente", "Copilot · Genie · Cortex · Joule · Pulse", "<b>Conversacional</b> y de varios pasos", "Garantizar la misma respuesta cada vez"),
        ],
        "kicker": "El producto cambió ocho veces. La tarea de decidir qué significa cada palabra del negocio nunca se fue.",
        "src": "Fuentes: Codd et al. (1993) · US Patent 5,555,403 · Stolte, Tang y Hanrahan (2002) · documentación de Microsoft, Tableau, SAP, Databricks y Snowflake. Fechas de referencia, no exhaustivas.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 14",
        "title": 'Eight generations, <span class="em">one</span> job',
        "lede": "Each product changed what question the business could ask without asking IT. None changed who decides what the number means.",
        "hdr": ("", "Generation", "Analysis it enables", "What it doesn't allow"),
        "rows": [
            ("The bedsheet", "COBOL · ALV · Crystal", "<b>Operational:</b> list, filter, trace back to the document", "Asking a new question without a request to IT"),
            ("The spreadsheet", "VisiCalc 1979 · Excel 5 1993", "<b>Scenarios</b> and pivot tables without code", "Two people arriving at the same number"),
            ("The cube", "Essbase · SSAS · BW/BEx", "<b>Multidimensional:</b> slice, drill down, year over year", "Asking what wasn't modeled"),
            ("The semantic layer", "BO universe 1991", "<b>Governed ad hoc</b> with business objects", "Maintaining itself: someone adds every object"),
            ("Visual discovery", "Polaris/Tableau 2002 · Qlik", "<b>Exploratory:</b> look before you ask", "A single truth: every workbook, its own math"),
            ("Self-service", "Power BI 2015 · Looker · SAC", "<b>Self-built models</b> and shared dashboards", "Controlling model sprawl"),
            ("The first AI wave", "Q&amp;A · Ask Data · Search to Insight", "<b>Automated diagnosis</b> and keyword phrases", "Conversation: synonyms captured by hand"),
            ("The agent", "Copilot · Genie · Cortex · Joule · Pulse", "<b>Conversational</b> and multi-step", "Guaranteeing the same answer every time"),
        ],
        "kicker": "The product changed eight times. The job of deciding what each business word means never went away.",
        "src": "Sources: Codd et al. (1993) · US Patent 5,555,403 · Stolte, Tang and Hanrahan (2002) · Microsoft, Tableau, SAP, Databricks and Snowflake documentation. Reference dates, not exhaustive.",
    },
}


def fig1_body(d):
    h = "".join(f"<div>{x}</div>" for x in d["hdr"])
    last = len(d["rows"])
    rows = "".join(
        f'<div class="row{" w" if i == last else ""}"><div class="num">{i}</div>'
        f'<div class="gen">{g}<span class="prod">{p}</span></div>'
        f'<div class="yes">{y}</div><div class="no">{n}</div></div>'
        for i, (g, p, y, n) in enumerate(d["rows"], 1)
    )
    return f'<div class="tbl"><div class="hdr">{h}</div>{rows}</div>'


# ---------- Figura 2: la primera NLQ, retirada ----------
YEAR0, YEAR1 = 2012, 2028
TRACK_W = 640  # px de la pista de años


def x_of(year: float) -> float:
    return (year - YEAR0) / (YEAR1 - YEAR0) * TRACK_W


FIG2_CSS = f"""
 .tl{{margin-top:48px;display:flex;flex-direction:column;gap:30px;}}
 .lane{{display:grid;grid-template-columns:250px {TRACK_W}px;gap:0 20px;align-items:center;}}
 .lab{{font-size:23px;font-weight:600;color:var(--text);line-height:1.2;}}
 .lab small{{display:block;font-weight:400;font-size:15px;color:var(--dim);margin-top:4px;}}
 .track{{position:relative;height:90px;}}
 .bar{{position:absolute;top:20px;height:34px;border-radius:6px;background:linear-gradient(90deg,rgba(162,166,173,.35),rgba(224,120,95,.55));}}
 .bar.unk{{background:linear-gradient(90deg,transparent,rgba(224,120,95,.55) 70%);}}
 .end{{position:absolute;top:10px;width:3px;height:54px;background:var(--red);}}
 .tag{{position:absolute;top:64px;font-family:"JetBrains Mono";font-size:15px;color:var(--dim);white-space:nowrap;}}
 .tag.r{{color:var(--red);}}
 .axis{{display:grid;grid-template-columns:250px {TRACK_W}px;gap:0 20px;}}
 .ticks{{position:relative;height:30px;border-top:1px solid var(--line);}}
 .ticks span{{position:absolute;top:8px;transform:translateX(-50%);font-family:"JetBrains Mono";font-size:15px;color:var(--faint);}}
 .now{{position:absolute;top:-336px;bottom:0;width:0;border-left:1px dashed rgba(43,189,143,.6);}}
 .now b{{position:absolute;top:-22px;left:6px;font-family:"Space Grotesk";font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);white-space:nowrap;}}
 .map{{margin-top:56px;border:1px solid rgba(43,189,143,.6);border-radius:10px;background:linear-gradient(180deg,rgba(43,189,143,.14),rgba(43,189,143,.02));padding:26px 24px;}}
 .map .t{{font-family:"Space Grotesk";font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--teal);}}
 .pair{{margin-top:14px;display:grid;grid-template-columns:1fr 50px 1fr;align-items:center;gap:0 12px;}}
 .box{{border:1px solid var(--line);border-radius:8px;background:#15181d;padding:16px 18px;font-size:19px;line-height:1.35;color:var(--dim);}}
 .box b{{display:block;color:var(--text);font-size:22px;margin-bottom:4px;}}
 .arrow{{text-align:center;font-size:28px;color:var(--teal);}}
"""

FIG2 = {
    "es": {
        "eyebrow": "Brújula · Edición 14",
        "title": 'La primera NLQ, <span class="em">retirada</span>',
        "lede": "Los tres fabricantes retiran entre 2024 y 2027 su primera forma de preguntarle a los datos en lenguaje natural (NLQ).",
        "lanes": [
            ("Power BI Q&amp;A", "reemplazo: Copilot", 2013.7, 2027.1, "sep-2013", "feb-2027", False),
            ("Tableau Ask Data", "reemplazo: Tableau Pulse", 2019.0, 2024.1, "2019", "feb-2024", False),
            ("SAC Search to Insight", "reemplazo: Just Ask + Joule", 2018.0, 2024.85, "", "Q4 2024", True),
        ],
        "now": "hoy · oct-2026",
        "map_t": "La tabla de migración de Microsoft",
        "old": ("Q&amp;A Setup", "sinónimos, relaciones lingüísticas, «enseñarle» a Q&amp;A"),
        "new": ("Prep data for AI", "esquema de datos para IA, respuestas verificadas, instrucciones de IA"),
        "kicker": "El buscador por palabras clave se retiró. La tarea de enseñarle el vocabulario del negocio pasó, casi igual, a la generación siguiente.",
        "src": "Fuentes: Microsoft SQL Server Blog (25-sep-2013) · Power BI Updates Blog, <i>Q&amp;A retirement reminder: February 2027</i> · Tableau Help, <i>Ask Data</i> · SAP KBA 3532315. La fecha de lanzamiento de Search to Insight no se indica.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 14",
        "title": 'The first NLQ, <span class="em">retired</span>',
        "lede": "Between 2024 and 2027 all three vendors retire their first way of asking data questions in natural language (NLQ).",
        "lanes": [
            ("Power BI Q&amp;A", "replacement: Copilot", 2013.7, 2027.1, "Sep 2013", "Feb 2027", False),
            ("Tableau Ask Data", "replacement: Tableau Pulse", 2019.0, 2024.1, "2019", "Feb 2024", False),
            ("SAC Search to Insight", "replacement: Just Ask + Joule", 2018.0, 2024.85, "", "Q4 2024", True),
        ],
        "now": "today · Oct 2026",
        "map_t": "Microsoft's migration table",
        "old": ("Q&amp;A Setup", "synonyms, linguistic relationships, “teaching” Q&amp;A"),
        "new": ("Prep data for AI", "AI data schema, verified answers, AI instructions"),
        "kicker": "The keyword search engine was retired. The job of teaching it the business vocabulary moved, almost unchanged, to the next generation.",
        "src": "Sources: Microsoft SQL Server Blog (Sep 25, 2013) · Power BI Updates Blog, <i>Q&amp;A retirement reminder: February 2027</i> · Tableau Help, <i>Ask Data</i> · SAP KBA 3532315. Search to Insight launch date not shown.",
    },
}


def fig2_body(d):
    lanes = ""
    for name, repl, start, end, s_lbl, e_lbl, unknown_start in d["lanes"]:
        x0, x1 = x_of(start), x_of(end)
        cls = "bar unk" if unknown_start else "bar"
        start_tag = f'<span class="tag" style="left:{x0:.0f}px">{s_lbl}</span>' if s_lbl else ""
        lanes += (f'<div class="lane"><div class="lab">{name}<small>{repl}</small></div><div class="track">'
                  f'<div class="{cls}" style="left:{x0:.0f}px;width:{x1 - x0:.0f}px"></div>'
                  f'<div class="end" style="left:{x1:.0f}px"></div>{start_tag}'
                  f'<span class="tag r" style="left:{x1 - 30:.0f}px">{e_lbl}</span></div></div>')
    ticks = "".join(f'<span style="left:{x_of(y):.0f}px">{y}</span>' for y in range(2013, 2028, 2))
    now = f'<div class="now" style="left:{x_of(2026.77):.0f}px"><b>{d["now"]}</b></div>'
    axis = f'<div class="axis"><div></div><div class="ticks">{ticks}{now}</div></div>'
    (ot, od), (nt, nd) = d["old"], d["new"]
    mapping = (f'<div class="map"><div class="t">{d["map_t"]}</div><div class="pair">'
               f'<div class="box"><b>{ot}</b>{od}</div><div class="arrow">→</div>'
               f'<div class="box"><b>{nt}</b>{nd}</div></div></div>')
    return f'<div class="tl">{lanes}</div>{axis}{mapping}'


# ---------- Figura 3: la misma pregunta, cuatro lenguajes ----------
FIG3_CSS = """
 .stack{margin-top:28px;display:flex;flex-direction:column;gap:16px;}
 .blk{display:grid;grid-template-columns:180px 1fr;gap:0 16px;border:1px solid var(--line);border-radius:10px;background:#101216;padding:20px 16px;align-items:start;}
 .blk.w{border-color:rgba(43,189,143,.6);}
 .who{font-family:"Space Grotesk";font-size:20px;font-weight:600;color:var(--text);line-height:1.2;}
 .who small{display:block;font-family:Inter;font-size:14px;font-weight:400;color:var(--dim);margin-top:4px;line-height:1.35;}
 .who .lg{display:inline-block;margin-bottom:6px;font-family:"JetBrains Mono";font-size:12px;color:var(--teal);border:1px solid rgba(43,189,143,.45);border-radius:6px;padding:2px 7px;}
 pre{font-family:"JetBrains Mono",monospace;font-size:14.5px;line-height:1.6;font-variant-ligatures:none;color:var(--code);white-space:pre;}
 .kw{color:#8fa3bf;} .cm{color:var(--faint);font-style:italic;} .st{color:#c7b27a;}
 .hl{background:rgba(43,189,143,.16);border-radius:3px;color:var(--text);}
"""

CODE = {
    "sql": """<span class="kw">SELECT</span> r.region,
       <span class="kw">SUM</span>(<span class="kw">CASE WHEN</span> f.anio = 2026 <span class="kw">THEN</span> f.venta_neta <span class="kw">END</span>) <span class="kw">AS</span> venta_2026,
       <span class="kw">SUM</span>(<span class="kw">CASE WHEN</span> <span class="hl">f.anio = 2025</span> <span class="kw">THEN</span> f.venta_neta <span class="kw">END</span>) <span class="kw">AS</span> venta_2025
<span class="kw">FROM</span>   fact_ventas f <span class="kw">JOIN</span> dim_region r <span class="kw">ON</span> r.region_id = f.region_id
<span class="kw">WHERE</span>  f.trimestre = 3 <span class="kw">AND</span> f.anio <span class="kw">IN</span> (2025, 2026)
<span class="kw">GROUP BY</span> r.region;""",
    "mdx": """<span class="kw">WITH MEMBER</span> [Measures].[Venta AA] <span class="kw">AS</span>
  ( [Measures].[Venta Neta],
    <span class="hl"><span class="kw">PARALLELPERIOD</span>([Fecha].[Fiscal].[Año], 1,</span>
    <span class="hl">               [Fecha].[Fiscal].<span class="kw">CurrentMember</span>)</span> )
<span class="kw">SELECT</span> { [Measures].[Venta Neta], [Measures].[Venta AA] } <span class="kw">ON COLUMNS</span>,
       [Región].[Región].<span class="kw">Members ON ROWS</span>
<span class="kw">FROM</span>   [Ventas] <span class="kw">WHERE</span> [Fecha].[Fiscal].[2026].[T3]""",
    "dax": """<span class="cm">-- medida en el modelo semántico; el visual pone región y trimestre</span>
Venta Neta AA =
<span class="kw">CALCULATE</span> ( [Venta Neta], <span class="hl"><span class="kw">SAMEPERIODLASTYEAR</span> ( 'Fecha'[Fecha] )</span> )""",
    "yaml": """<span class="kw">verified_queries</span>:
  - <span class="kw">name</span>: venta_trimestre_vs_aa
    <span class="kw">question</span>: <span class="st">"¿Cómo va la venta del trimestre vs. el año pasado, por región?"</span>
    <span class="kw">sql</span>: <span class="st">SELECT region, venta_neta, venta_neta_aa FROM __ventas WHERE …</span>
    <span class="hl"><span class="kw">verified_by</span>: Contraloría</span>
    <span class="kw">verified_at</span>: 1759708800""",
}

FIG3 = {
    "es": {
        "eyebrow": "Brújula · Edición 14",
        "title": 'La misma pregunta, <span class="em">cuatro</span> lenguajes',
        "lede": "«Venta del trimestre contra el mismo trimestre del año pasado, por región.» Cambia quién la escribe. Sigue habiendo que decidir qué es «año pasado».",
        "blocks": [
            ("sql", "SQL", "La sábana y el universo", "Lo escribe sistemas, o el universo lo genera."),
            ("mdx", "MDX", "El cubo", "«Año anterior» es una función del motor."),
            ("dax", "DAX", "El self-service", "El analista lo deja como medida en el modelo."),
            ("yaml", "Verified query", "El agente", "Una persona firma la respuesta de referencia."),
        ],
        "kicker": "En los tres primeros, la definición vive en el código. En el último, además tiene nombre: alguien la verificó.",
        "src": "Código ilustrativo; nombres de tablas y medidas inventados. Sintaxis: MDX <i>PARALLELPERIOD</i>, DAX <i>SAMEPERIODLASTYEAR</i> y <i>verified_queries</i> del modelo semántico de Snowflake Cortex Analyst.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 14",
        "title": 'Same question, <span class="em">four</span> languages',
        "lede": "“Quarter sales versus the same quarter last year, by region.” Who writes it changes. Someone still has to decide what “last year” means.",
        "blocks": [
            ("sql", "SQL", "The bedsheet and the universe", "Written by IT, or generated by the universe."),
            ("mdx", "MDX", "The cube", "“Prior year” is a function of the engine."),
            ("dax", "DAX", "Self-service", "The analyst leaves it as a measure in the model."),
            ("yaml", "Verified query", "The agent", "A person signs off on the reference answer."),
        ],
        "kicker": "In the first three, the definition lives in the code. In the last one, it also has a name: someone verified it.",
        "src": "Illustrative code; table and measure names are made up (kept in Spanish). Syntax: MDX <i>PARALLELPERIOD</i>, DAX <i>SAMEPERIODLASTYEAR</i> and <i>verified_queries</i> in the Snowflake Cortex Analyst semantic model.",
    },
}


def fig3_body(d):
    last = len(d["blocks"])
    blocks = "".join(
        f'<div class="blk{" w" if i == last else ""}"><div class="who"><span class="lg">{lg}</span><br/>{gen}<small>{note}</small></div>'
        f'<pre>{CODE[key]}</pre></div>'
        for i, (key, lg, gen, note) in enumerate(d["blocks"], 1)
    )
    return f'<div class="stack">{blocks}</div>'


# ---------- Portada ----------
COVER_SRC = HERE.parent / "2026-W40" / "brujula-cover-13.html"
COVER_TXT = {
    "es": ("Edición 14 · 2026 · W41", "Analítica · GenBI",
           'De la sábana<br/>al <span class="em">agente</span>',
           "Ocho generaciones de reporting, producto por producto: qué análisis permitía cada una, qué no, y qué estamos comprando hoy.",
           "De los datos a las decisiones, sin perder el norte"),
    "en": ("Edition 14 · 2026 · W41", "Analytics · GenBI",
           'From the bedsheet<br/>to the <span class="em">agent</span>',
           "Eight generations of reporting, product by product: what analysis each one enabled, what it didn't, and what we are buying today.",
           "From data to decisions, without losing north"),
}
COVER_OLD = ("Edición 13 · 2026 · W40", "Calidad de Datos · Gobierno",
             'Cuadró en el go-live.<br/>¿Y <span class="em">hoy</span>?')


def cover(lang):
    ed, eyebrow, h1, sub, tag = COVER_TXT[lang]
    out = COVER_SRC.read_text()
    for old, new in zip(COVER_OLD, (ed, eyebrow, h1)):
        if old not in out:
            raise ValueError(f"La portada base no contiene: {old}")
        out = out.replace(old, new)
    old_sub = out.split('<p class="sub">')[1].split("</p>")[0]
    out = out.replace(old_sub, sub)
    out = out.replace("De los datos a las decisiones, sin perder el norte", tag)
    return out.replace('<html lang="es">', f'<html lang="{lang}">')


def page(lang, d, css, body):
    return HEAD.format(lang=lang, extra=css, eyebrow=d["eyebrow"], title=d["title"],
                       lede=d["lede"], body=body, kicker=d["kicker"], src=d["src"])


def render(html_path: Path, w: int, h: int):
    png = html_path.with_suffix(".png")
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu",
                    f"--window-size={w},{h}", "--virtual-time-budget=6000",
                    f"--screenshot={png}", html_path.as_uri()],
                   check=True, capture_output=True)
    print("ok", png.name)


def main():
    for lang in ("es", "en"):
        sfx = "" if lang == "es" else "-en"
        pages = {
            f"fig-escalera{sfx}.html": page(lang, FIG1[lang], FIG1_CSS, fig1_body(FIG1[lang])),
            f"fig-nlq-retirada{sfx}.html": page(lang, FIG2[lang], FIG2_CSS, fig2_body(FIG2[lang])),
            f"fig-misma-pregunta{sfx}.html": page(lang, FIG3[lang], FIG3_CSS, fig3_body(FIG3[lang])),
        }
        for name, content in pages.items():
            p = HERE / name
            p.write_text(content)
            render(p, 1080, 1350)
        cp = HERE / f"brujula-cover-14{sfx}.html"
        cp.write_text(cover(lang))
        render(cp, 1920, 1080)


if __name__ == "__main__":
    main()
