"""Genera las figuras y la portada de la ed. 13 (ES/EN) como HTML y las renderiza con Chrome headless."""
import html
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

# ---------- Figura 1: la palomita no es un cuadre ----------
FIG1_CSS = """
 .tbl{margin-top:34px;display:flex;flex-direction:column;gap:14px;}
 .hdr,.row{display:grid;grid-template-columns:210px 1fr 1fr;gap:0 20px;align-items:start;}
 .hdr{font-family:"Space Grotesk";font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--faint);padding:0 18px;}
 .row{border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,#1b2027,#171a1f);padding:22px 20px;}
 .tool{font-size:23px;color:var(--text);font-weight:600;line-height:1.2;}
 .seal{display:inline-block;margin-top:10px;font-family:"JetBrains Mono";font-size:14px;color:var(--teal);border:1px solid rgba(43,189,143,.45);border-radius:6px;padding:3px 8px;}
 .yes,.no{font-size:18.5px;line-height:1.4;color:var(--dim);}
 .no{color:#d9c9c3;} .no b{color:var(--red);font-weight:600;}
 .yes b{color:var(--text);font-weight:600;}
 .row.w{border-color:rgba(43,189,143,.6);background:linear-gradient(180deg,rgba(43,189,143,.16),rgba(43,189,143,.03));}
 .row.w .tool{color:var(--teal);}
 .row.w .no{color:var(--text);} .row.w .no b{color:var(--teal);}
"""

FIG1 = {
    "es": {
        "eyebrow": "Brújula · Edición 13",
        "title": 'La palomita <span class="em">no es</span> un cuadre',
        "lede": "Qué sello trae cada plataforma, qué certifica en realidad y lo que ninguno hace: comparar el número de hoy contra su fuente.",
        "hdr": ("Herramienta", "Qué certifica", "Qué no hace"),
        "rows": [
            ("Power BI / Fabric", "Certified", "Que un revisor autorizado <b>dio fe</b> de que cumple los estándares de la organización.", "Si el modelo cambia mañana, <b>el sello se queda</b> donde estaba."),
            ("Databricks Unity Catalog", "certification_status", "Que el activo <b>cumplió estándares internos</b>. A mano o con reglas de uso, dueño o antigüedad.", "Ninguna regla <b>revisa si el número cuadra</b>."),
            ("Genie", "benchmarks", "Hasta 500 preguntas con su <b>SQL de referencia</b>; califica bueno, malo o revisión manual.", "Corre <b>cuando alguien lo lanza</b>. Si el SQL de referencia está mal, califica contra otro error."),
            ("Snowflake", "Data Metric Functions", "Nulos, duplicados, frescura, con <b>calendario propio</b>: cada hora por default.", "Mide <b>calidad del dato</b>, no si el KPI cuadra contra la contabilidad."),
            ("SAP Datasphere", "catálogo · glosario", "Que el KPI tiene <b>una definición</b> escrita y el activo está publicado.", "Una buena definición <b>no prueba</b> que el número de hoy la cumpla."),
        ],
        "witness": ("El testigo", "cifras control", "Compara el KPI contra el mayor <b>después de cada carga, transporte y upgrade</b>.", "Dice si <b>hoy</b> cuadra, y lo publica en el tablero."),
        "kicker": "Un sello dice quién opinó que el dato era confiable. Un cuadre demuestra que hoy lo es.",
        "src": "Fuentes: Microsoft Learn, <i>Endorse Fabric and Power BI items</i> · Databricks, <i>Flag data as certified or deprecated</i> y <i>Genie benchmarks</i> · Snowflake, <i>Introduction to data quality checks</i> · SAP Help, catálogo de SAP Datasphere.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 13",
        "title": 'A checkmark <span class="em">is not</span> a reconciliation',
        "lede": "The badge each platform offers, what it really certifies, and what none of them does: compare today's number against its source.",
        "hdr": ("Tool", "What it certifies", "What it doesn't do"),
        "rows": [
            ("Power BI / Fabric", "Certified", "That an authorized reviewer <b>attested</b> it meets the organization's standards.", "If the model changes tomorrow, <b>the badge stays</b> where it was."),
            ("Databricks Unity Catalog", "certification_status", "That the asset <b>met internal standards</b>. By hand or via rules on usage, owner or age.", "No rule <b>checks whether the number reconciles</b>."),
            ("Genie", "benchmarks", "Up to 500 questions with their <b>reference SQL</b>; grades good, bad or manual review.", "Runs <b>when someone launches it</b>. If the reference SQL is wrong, it grades against another error."),
            ("Snowflake", "Data Metric Functions", "Nulls, duplicates, freshness, on <b>their own schedule</b>: hourly by default.", "Measures <b>data quality</b>, not whether the KPI ties to the books."),
            ("SAP Datasphere", "catalog · glossary", "That the KPI has <b>a written definition</b> and the asset is published.", "A good definition <b>doesn't prove</b> today's number meets it."),
        ],
        "witness": ("The witness", "control totals", "Compares the KPI against the ledger <b>after every load, transport and upgrade</b>.", "Says whether it reconciles <b>today</b>, and shows it on the dashboard."),
        "kicker": "A badge says who thought the data was trustworthy. A reconciliation proves it is today.",
        "src": "Sources: Microsoft Learn, <i>Endorse Fabric and Power BI items</i> · Databricks, <i>Flag data as certified or deprecated</i> and <i>Genie benchmarks</i> · Snowflake, <i>Introduction to data quality checks</i> · SAP Help, SAP Datasphere catalog.",
    },
}


def fig1_body(d):
    rows = "".join(
        f'<div class="row"><div><div class="tool">{t}</div><span class="seal">{s}</span></div>'
        f'<div class="yes">{y}</div><div class="no">{n}</div></div>'
        for t, s, y, n in d["rows"]
    )
    t, s, y, n = d["witness"]
    witness = (f'<div class="row w"><div><div class="tool">{t}</div><span class="seal">{s}</span></div>'
               f'<div class="yes">{y}</div><div class="no">{n}</div></div>')
    h = "".join(f"<div>{x}</div>" for x in d["hdr"])
    return f'<div class="tbl"><div class="hdr">{h}</div>{rows}{witness}</div>'


# ---------- Figura 2: el testigo, en código ----------
FIG2_CSS = """
 .code{margin-top:24px;border:1px solid var(--line);border-radius:10px;background:#101216;padding:18px 20px;position:relative;}
 pre{font-family:"JetBrains Mono",monospace;font-size:15px;line-height:1.6;font-variant-ligatures:none;color:var(--code);white-space:pre;}
 .kw{color:#8fa3bf;} .cm{color:var(--faint);font-style:italic;} .st{color:#c7b27a;}
 .hl{background:rgba(43,189,143,.14);border-radius:3px;color:var(--text);}
 .n{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:var(--teal);color:#0f1a16;font-family:"Space Grotesk";font-weight:700;font-size:13px;margin-left:8px;vertical-align:1px;}
 .notes{display:grid;grid-template-columns:1fr 1fr;gap:14px 24px;margin-top:20px;}
 .note{display:flex;gap:10px;font-size:17px;color:var(--dim);line-height:1.38;}
 .note .n{margin:1px 0 0;flex:none;} .note b{color:var(--text);font-weight:600;}
 .dash{margin-top:22px;border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,#1b2027,#171a1f);padding:14px 18px;}
 .dash .t{font-family:"Space Grotesk";font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--faint);}
 .badge{margin-top:12px;display:flex;align-items:center;gap:12px;font-size:19px;color:var(--text);}
 .dot{width:12px;height:12px;border-radius:50%;background:var(--teal);box-shadow:0 0 0 4px rgba(43,189,143,.18);}
 .dot.r{background:var(--red);box-shadow:0 0 0 4px rgba(224,120,95,.18);}
 .grid{margin-top:12px;display:grid;grid-template-columns:1.1fr 1fr 1fr 1fr 1fr;font-family:"JetBrains Mono";font-size:15px;font-variant-ligatures:none;color:var(--code);}
 .grid div{padding:5px 8px;border-top:1px solid var(--line);}
 .grid .h{color:var(--faint);border-top:none;}
 .ok{color:var(--teal);font-weight:600;} .ex{color:var(--red);font-weight:600;}
"""

SQL = {
    "es": """<span class="cm">-- Testigo: ventas netas del modelo contra el mayor, por sociedad y periodo</span>
<span class="kw">INSERT INTO</span> control.conciliacion
<span class="kw">SELECT</span> CURRENT_TIMESTAMP, <span class="st">'VENTAS_NETAS'</span>, f.sociedad, f.periodo,
       COALESCE(m.ventas_netas, 0)                 <span class="kw">AS</span> valor_modelo,
       f.saldo_mayor                               <span class="kw">AS</span> valor_fuente,
       <span class="kw">CASE WHEN</span> ABS(COALESCE(m.ventas_netas,0) - f.saldo_mayor)
            &lt;= <span class="hl">t.tolerancia_pct</span> * ABS(f.saldo_mayor)<span class="n">3</span>
            <span class="kw">THEN</span> <span class="st">'OK'</span> <span class="kw">ELSE</span> <span class="st">'EXCEPCION'</span> <span class="kw">END</span> <span class="hl"><span class="kw">AS</span> estado</span><span class="n">4</span>
<span class="kw">FROM</span> (<span class="kw">SELECT</span> sociedad, periodo,
             <span class="hl">-1 * saldo <span class="kw">AS</span> saldo_mayor</span><span class="n">2</span>  <span class="cm">-- ingresos = abono</span>
      <span class="kw">FROM</span> fuente.saldos_mayor
      <span class="kw">WHERE</span> cuenta_grupo = <span class="st">'VENTAS_NETAS'</span>) f
<span class="hl"><span class="kw">LEFT JOIN</span> modelo.ventas_por_sociedad m</span><span class="n">1</span>
       <span class="kw">ON</span> m.sociedad = f.sociedad <span class="kw">AND</span> m.periodo = f.periodo
<span class="kw">JOIN</span> control.tolerancias t <span class="kw">ON</span> t.kpi = <span class="st">'VENTAS_NETAS'</span>;""",
    "en": """<span class="cm">-- Witness: net sales from the model against the ledger, by company code and period</span>
<span class="kw">INSERT INTO</span> control.reconciliation
<span class="kw">SELECT</span> CURRENT_TIMESTAMP, <span class="st">'NET_SALES'</span>, f.company_code, f.period,
       COALESCE(m.net_sales, 0)                    <span class="kw">AS</span> model_value,
       f.ledger_balance                            <span class="kw">AS</span> source_value,
       <span class="kw">CASE WHEN</span> ABS(COALESCE(m.net_sales,0) - f.ledger_balance)
            &lt;= <span class="hl">t.tolerance_pct</span> * ABS(f.ledger_balance)<span class="n">3</span>
            <span class="kw">THEN</span> <span class="st">'OK'</span> <span class="kw">ELSE</span> <span class="st">'EXCEPTION'</span> <span class="kw">END</span> <span class="hl"><span class="kw">AS</span> status</span><span class="n">4</span>
<span class="kw">FROM</span> (<span class="kw">SELECT</span> company_code, period,
             <span class="hl">-1 * balance <span class="kw">AS</span> ledger_balance</span><span class="n">2</span>  <span class="cm">-- revenue = credit</span>
      <span class="kw">FROM</span> source.ledger_balances
      <span class="kw">WHERE</span> account_group = <span class="st">'NET_SALES'</span>) f
<span class="hl"><span class="kw">LEFT JOIN</span> model.sales_by_company m</span><span class="n">1</span>
       <span class="kw">ON</span> m.company_code = f.company_code <span class="kw">AND</span> m.period = f.period
<span class="kw">JOIN</span> control.tolerances t <span class="kw">ON</span> t.kpi = <span class="st">'NET_SALES'</span>;""",
}

FIG2 = {
    "es": {
        "eyebrow": "Brújula · Edición 13",
        "title": 'El testigo, <span class="em">en código</span>',
        "lede": "Una consulta que compara el KPI del modelo contra el mayor después de cada carga y deja el resultado en una tabla de control.",
        "notes": [
            "<b>Parte del mayor, no del modelo.</b> La sociedad que no entró al filtro sale como excepción en vez de desaparecer.",
            "<b>Invierte el signo.</b> En ACDOCA las ventas son abonos y viven en negativo; sin esto, todo falla el primer día.",
            "<b>La tolerancia la firma el negocio.</b> Vive como dato en <code>control.tolerancias</code>, no escondida en el código.",
            "<b>El estado se publica.</b> La columna que acaba en el tablero para que el controller no tenga que cuadrar a mano.",
        ],
        "dash_t": "Así se ve en el tablero",
        "badge_ok": "Conciliado contra cifras control el 23-sep: <b>&nbsp;3 de 4 OK</b>",
        "grid_h": ("sociedad", "periodo", "modelo", "mayor", "estado"),
        "grid": [
            ("MX01", "2026-08", "48,210,550", "48,210,550", "OK"),
            ("MX02", "2026-08", "31,904,120", "31,905,000", "OK"),
            ("MX03", "2026-08", "12,775,300", "12,775,300", "OK"),
            ("MX04 · nueva", "2026-08", "0", "6,420,880", "EXCEPCION"),
        ],
        "kicker": "La consulta es lo de menos. Lo que importa es que corre sola después de cada cambio y que el tablero dice si hoy cuadra.",
        "src": "Código de ejemplo, simplificado; cifras ilustrativas. Tolerancia de ejemplo: 0.01 %. Fuente de un reporte desde S/4HANA: ACDOCA.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 13",
        "title": 'The witness, <span class="em">in code</span>',
        "lede": "A query that compares the model's KPI against the ledger after every load and writes the result to a control table.",
        "notes": [
            "<b>Starts from the ledger, not the model.</b> The company code that fell outside the filter shows up as an exception instead of vanishing.",
            "<b>Flips the sign.</b> In ACDOCA sales are credits and live as negatives; without this, everything fails on day one.",
            "<b>The business signs the tolerance.</b> It lives as data in <code>control.tolerances</code>, not buried in code.",
            "<b>The status gets published.</b> The column that lands on the dashboard so the controller doesn't reconcile by hand.",
        ],
        "dash_t": "How it looks on the dashboard",
        "badge_ok": "Reconciled against control totals on Sep 23: <b>&nbsp;3 of 4 OK</b>",
        "grid_h": ("company", "period", "model", "ledger", "status"),
        "grid": [
            ("MX01", "2026-08", "48,210,550", "48,210,550", "OK"),
            ("MX02", "2026-08", "31,904,120", "31,905,000", "OK"),
            ("MX03", "2026-08", "12,775,300", "12,775,300", "OK"),
            ("MX04 · new", "2026-08", "0", "6,420,880", "EXCEPTION"),
        ],
        "kicker": "The query is the least of it. What matters is that it runs on its own after every change and the dashboard says whether it reconciles today.",
        "src": "Sample code, simplified; illustrative figures. Sample tolerance: 0.01%. Source for a report built on S/4HANA: ACDOCA.",
    },
}


def fig2_body(d, lang):
    notes = "".join(f'<div class="note"><span class="n">{i}</span><div>{t}</div></div>'
                    for i, t in enumerate(d["notes"], 1))
    cells = "".join(f'<div class="h">{h}</div>' for h in d["grid_h"])
    for row in d["grid"]:
        st = row[4]
        cls = "ok" if st == "OK" else "ex"
        cells += "".join(f"<div>{c}</div>" for c in row[:4]) + f'<div class="{cls}">{st}</div>'
    return (f'<div class="code"><pre>{SQL[lang]}</pre></div><div class="notes">{notes}</div>'
            f'<div class="dash"><div class="t">{d["dash_t"]}</div>'
            f'<div class="badge"><span class="dot r"></span><span>{d["badge_ok"]}</span></div>'
            f'<div class="grid">{cells}</div></div>')


# ---------- Figura 3: ¿quién firma? ----------
FIG3_CSS = """
 .mx{margin-top:36px;display:grid;grid-template-columns:300px repeat(4,1fr);grid-auto-rows:minmax(84px,auto);gap:10px;}
 .ch{font-family:"Space Grotesk";font-size:14px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:var(--dim);line-height:1.3;padding:0 6px 8px;align-self:end;text-align:center;}
 .ch small{display:block;font-family:Inter;text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint);font-size:13px;margin-top:4px;}
 .act{font-size:20px;color:var(--text);line-height:1.3;padding:14px 14px;border:1px solid var(--line);border-radius:8px;background:#181b21;display:flex;align-items:center;}
 .c{border-radius:8px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:16.5px;line-height:1.25;padding:10px 8px;border:1px solid var(--line);color:var(--faint);background:#15181d;}
 .c.a{background:rgba(43,189,143,.22);border-color:rgba(43,189,143,.7);color:var(--text);font-weight:600;}
 .c.d{background:rgba(143,163,191,.14);border-color:rgba(143,163,191,.45);color:var(--text);}
 .c.o{color:var(--dim);}
 .legend{display:flex;gap:26px;margin-top:22px;font-size:15px;color:var(--dim);}
 .legend span{display:inline-flex;align-items:center;gap:8px;}
 .sw{width:16px;height:16px;border-radius:4px;display:inline-block;border:1px solid var(--line);}
"""

FIG3 = {
    "es": {
        "eyebrow": "Brújula · Edición 13",
        "title": '¿Quién <span class="em">firma</span>?',
        "lede": "TI es responsable de que el testigo exista y corra. El negocio es dueño de que el número signifique lo que dice. Auditoría revisa que el control funcione.",
        "cols": [("Dueño de negocio", "p. ej. Contraloría"), ("Dueño del producto de datos", "del modelo al tablero"), ("Ingeniería / TI", "data custodian"), ("Auditoría interna", "tercera línea")],
        "rows": [
            ("Definir el KPI y su cifra control", ["a:Responde", "d:Hace", "o:Opina", ":Se entera"]),
            ("Fijar la tolerancia", ["a:Responde y hace", "o:Opina", ":Se entera", "o:Opina"]),
            ("Construir y correr el testigo", [":Se entera", "a:Responde", "d:Hace", ":Se entera"]),
            ("Explicar las excepciones", ["a:Responde si es de negocio", "d:Hace", "d:Hace si es técnica", ":Se entera"]),
            ("Mantener el KPI alineado al negocio", ["a:Responde", "d:Hace", "o:Opina", ":Se entera"]),
            ("Revisar que el control funcione", ["o:Opina", "o:Opina", ":Se entera", "a:Responde y hace"]),
        ],
        "legend": ("Responde por el resultado", "Hace el trabajo", "Opina / Se entera"),
        "kicker": "TI construye el testigo; el negocio es dueño del significado. Si falta uno de los dos, la palomita queda colgando de nadie.",
        "src": "Fuentes: BCBS 239 (2013), ¶34, roles de negocio y de TI · DAMA-DMBOK: data owner, data steward, data custodian. Matriz simplificada.",
    },
    "en": {
        "eyebrow": "Brújula · Edition 13",
        "title": 'Who <span class="em">signs</span>?',
        "lede": "IT is accountable for the witness existing and running. The business owns the number meaning what it says. Audit reviews that the control works.",
        "cols": [("Business owner", "e.g. Controller"), ("Data product owner", "from model to dashboard"), ("Engineering / IT", "data custodian"), ("Internal audit", "third line")],
        "rows": [
            ("Define the KPI and its control total", ["a:Accountable", "d:Does", "o:Consulted", ":Informed"]),
            ("Set the tolerance", ["a:Accountable and does", "o:Consulted", ":Informed", "o:Consulted"]),
            ("Build and run the witness", [":Informed", "a:Accountable", "d:Does", ":Informed"]),
            ("Explain exceptions", ["a:Accountable if business", "d:Does", "d:Does if technical", ":Informed"]),
            ("Keep the KPI aligned to the business", ["a:Accountable", "d:Does", "o:Consulted", ":Informed"]),
            ("Review that the control works", ["o:Consulted", "o:Consulted", ":Informed", "a:Accountable and does"]),
        ],
        "legend": ("Accountable for the result", "Does the work", "Consulted / Informed"),
        "kicker": "IT builds the witness; the business owns the meaning. If either one is missing, the checkmark hangs from nobody.",
        "src": "Sources: BCBS 239 (2013), ¶34, business and IT roles · DAMA-DMBOK: data owner, data steward, data custodian. Simplified matrix.",
    },
}


def fig3_body(d):
    cells = '<div></div>' + "".join(f'<div class="ch">{t}<small>{s}</small></div>' for t, s in d["cols"])
    for act, vals in d["rows"]:
        cells += f'<div class="act">{act}</div>'
        for v in vals:
            cls, txt = v.split(":", 1)
            cells += f'<div class="c {cls}">{txt}</div>'
    a, dd, o = d["legend"]
    legend = (f'<div class="legend"><span><i class="sw" style="background:rgba(43,189,143,.35)"></i>{a}</span>'
              f'<span><i class="sw" style="background:rgba(143,163,191,.3)"></i>{dd}</span>'
              f'<span><i class="sw" style="background:#15181d"></i>{o}</span></div>')
    return f'<div class="mx">{cells}</div>{legend}'


# ---------- Portada ----------
COVER = (HERE.parent / "2026-W39" / "brujula-cover-12.html").read_text()
COVER_TXT = {
    "es": ("Edición 13 · 2026 · W40", "Calidad de Datos · Gobierno",
           'Cuadró en el go-live.<br/>¿Y <span class="em">hoy</span>?',
           "Los proyectos cuadran el número el día del go-live y no dejan nada que lo siga cuadrando. El testigo que falta, y quién lo debería firmar.",
           "De los datos a las decisiones, sin perder el norte"),
    "en": ("Edition 13 · 2026 · W40", "Data Quality · Governance",
           'It reconciled at go-live.<br/>What about <span class="em">today</span>?',
           "Projects reconcile the number on go-live day and leave nothing behind to keep reconciling it. The missing witness, and who should sign for it.",
           "From data to decisions, without losing north"),
}


def cover(lang):
    ed, eyebrow, h1, sub, tag = COVER_TXT[lang]
    out = COVER.replace("Edición 12 · 2026 · W39", ed)
    out = out.replace("Arquitectura de Datos · SAP", eyebrow)
    out = out.replace('Quitamos BW.<br/>El <span class="em">motor</span> se quedó.', h1)
    old_sub = out.split('<p class="sub">')[1].split("</p>")[0]
    out = out.replace(old_sub, sub)
    out = out.replace("De los datos a las decisiones, sin perder el norte", tag)
    out = out.replace('<html lang="es">', f'<html lang="{lang}">')
    return out


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
            f"fig-palomita{sfx}.html": page(lang, FIG1[lang], FIG1_CSS, fig1_body(FIG1[lang])),
            f"fig-testigo{sfx}.html": page(lang, FIG2[lang], FIG2_CSS, fig2_body(FIG2[lang], lang)),
            f"fig-quien-firma{sfx}.html": page(lang, FIG3[lang], FIG3_CSS, fig3_body(FIG3[lang])),
        }
        for name, content in pages.items():
            p = HERE / name
            p.write_text(content)
            render(p, 1080, 1350)
        cp = HERE / f"brujula-cover-13{sfx}.html"
        cp.write_text(cover(lang))
        render(cp, 1920, 1080)


if __name__ == "__main__":
    main()
