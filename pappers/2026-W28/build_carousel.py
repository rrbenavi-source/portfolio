#!/usr/bin/env python3
"""Genera el carrusel PDF para LinkedIn (4:5, 1080x1350) del papper W28.

Produce dos HTML autocontenidos + dos PDFs vía Chrome headless:
  linkedin-carousel-es.pdf / linkedin-carousel-en.pdf

Identidad: tema oscuro, acento teal (#2bbd8f), Fraunces (display) + Inter (texto),
consistente con el whitepaper y el portfolio. Uso: python3 build_carousel.py
"""
import html
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------------------------------------------------------------- design system
CSS = """
:root{
  --bg:#14161a; --bg2:#191c22; --surface:#1e222a; --surface-hi:#242932;
  --line:#2c3038; --text:#ECEAE4; --dim:#A2A6AD; --faint:#71767f;
  --accent:#2BBD8F; --accent-dim:#1f8f6c; --gold:#CDA25A;
}
*{box-sizing:border-box;margin:0;padding:0;}
@page{ size:1080px 1350px; margin:0; }
html,body{ background:var(--bg); }
body{ font-family:Inter,system-ui,sans-serif; color:var(--text);
      -webkit-font-smoothing:antialiased; }

.slide{
  width:1080px; height:1350px; position:relative; overflow:hidden;
  padding:96px 92px 88px; display:flex; flex-direction:column;
  page-break-after:always;
  background:
    radial-gradient(1100px 700px at 100% -8%, rgba(43,189,143,.13), transparent 60%),
    radial-gradient(900px 640px at -12% 108%, rgba(205,162,90,.07), transparent 55%),
    var(--bg);
}
.slide:last-child{ page-break-after:auto; }
.slide::after{ /* grain / atmosphere */
  content:""; position:absolute; inset:0; pointer-events:none; opacity:.5;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='120' height='120' filter='url(%23n)' opacity='0.028'/></svg>");
}

/* shared chrome */
.eyebrow{ color:var(--accent); font-weight:600; letter-spacing:.18em;
  text-transform:uppercase; font-size:18px; }
.kicker-rule{ width:64px; height:3px; background:var(--accent); border-radius:2px;
  margin:26px 0 30px; }
.body-lg{ font-size:33px; line-height:1.5; color:var(--dim); font-weight:400; }
.body-lg strong{ color:var(--text); font-weight:600; }
.accent{ color:var(--accent); }
.disp{ font-family:Fraunces,Georgia,serif; font-weight:600; letter-spacing:-.015em;
  line-height:1.04; color:var(--text); }

.spacer{ flex:1 1 auto; }

.foot{ position:relative; z-index:2; display:flex; justify-content:space-between;
  align-items:center; border-top:1px solid var(--line); padding-top:26px; margin-top:40px; }
.foot .who{ font-size:17px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--faint); font-weight:600; }
.foot .who b{ color:var(--dim); font-weight:600; }
.foot .pg{ font-family:Fraunces,Georgia,serif; font-size:20px; color:var(--faint); }
.foot .pg b{ color:var(--accent); }
.mark{ display:inline-flex; align-items:center; gap:12px; }
.mark .dot{ width:11px; height:11px; border-radius:50%; background:var(--accent);
  box-shadow:0 0 0 5px rgba(43,189,143,.16); }

.topbar{ position:relative; z-index:2; display:flex; justify-content:space-between;
  align-items:center; margin-bottom:auto; }
.topbar .tag{ font-size:16px; letter-spacing:.16em; text-transform:uppercase; color:var(--faint); font-weight:600; }

/* cover */
.cover-title{ font-size:96px; margin:0 0 30px; }
.cover-sub{ font-size:34px; line-height:1.42; color:var(--dim); max-width:20ch; }
.cover-by{ display:flex; align-items:center; gap:16px; margin-top:44px;
  font-size:20px; color:var(--dim); }
.cover-by .sep{ color:var(--line); }
.swipe{ position:absolute; right:92px; bottom:150px; z-index:2; display:flex; align-items:center;
  gap:14px; color:var(--accent); font-size:19px; font-weight:600; letter-spacing:.04em; }
.swipe .arrow{ font-size:26px; }

/* statement */
.stmt{ font-size:70px; }
.stmt .em{ color:var(--accent); }

/* stat */
.stat-row{ display:flex; align-items:stretch; gap:34px; margin:8px 0 18px; }
.stat-card{ flex:1; background:linear-gradient(180deg,var(--surface),var(--bg2));
  border:1px solid var(--line); border-radius:26px; padding:46px 40px 40px; position:relative; }
.stat-card.hi{ border-color:var(--accent-dim);
  background:linear-gradient(180deg,rgba(43,189,143,.10),var(--bg2)); }
.stat-num{ font-family:Fraunces,Georgia,serif; font-weight:600; font-size:118px;
  line-height:.94; letter-spacing:-.03em; }
.stat-card.hi .stat-num{ color:var(--accent); }
.stat-lbl{ font-size:24px; color:var(--dim); line-height:1.4; margin-top:24px; }
.stat-tag{ font-size:17px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--faint); font-weight:600; margin-bottom:20px; }
.stat-note{ font-size:23px; color:var(--faint); line-height:1.5; }
.stat-note b{ color:var(--gold); font-weight:600; }

/* split */
.split{ display:flex; flex-direction:column; gap:30px; margin-top:6px; }
.split-card{ background:var(--surface); border:1px solid var(--line); border-radius:24px;
  padding:44px 46px; border-left:5px solid var(--accent); }
.split-card.warn{ border-left-color:var(--gold); }
.split-card h3{ font-family:Fraunces,Georgia,serif; font-weight:600; font-size:38px;
  margin-bottom:16px; }
.split-card.warn h3{ color:var(--gold); }
.split-card.good h3{ color:var(--accent); }
.split-card p{ font-size:29px; line-height:1.45; color:var(--dim); }
.split-card p strong{ color:var(--text); font-weight:600; }

/* steps */
.steps{ display:flex; flex-direction:column; gap:26px; margin-top:8px; }
.step{ display:flex; gap:34px; align-items:flex-start; background:var(--surface);
  border:1px solid var(--line); border-radius:22px; padding:38px 42px; }
.step .n{ font-family:Fraunces,Georgia,serif; font-weight:600; font-size:56px;
  color:var(--accent); line-height:1; min-width:76px; }
.step h3{ font-size:33px; margin-bottom:10px; font-weight:600; }
.step p{ font-size:25px; color:var(--dim); line-height:1.42; }

/* mono chips */
code{ font-family:'SF Mono',ui-monospace,Menlo,monospace; font-size:.86em;
  background:rgba(43,189,143,.12); border:1px solid var(--line);
  color:var(--accent); padding:.08em .34em; border-radius:7px; }

/* quote */
.quote-mark{ font-family:Fraunces,Georgia,serif; font-size:200px; line-height:.6;
  color:var(--accent); opacity:.5; height:110px; }
.quote{ font-family:Fraunces,Georgia,serif; font-weight:600; font-size:72px;
  line-height:1.14; letter-spacing:-.015em; margin-top:20px; }
.quote .em{ color:var(--accent); }
.quote-by{ font-size:21px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--faint); font-weight:600; margin-top:52px; }

/* cta */
.cta-title{ font-size:82px; margin-bottom:30px; }
.cta-lead{ font-size:32px; line-height:1.5; color:var(--dim); max-width:22ch; }
.cta-box{ margin-top:auto; background:var(--surface); border:1px solid var(--line);
  border-radius:24px; padding:44px 46px; }
.cta-box .lbl{ font-size:17px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--accent); font-weight:600; margin-bottom:18px; }
.cta-box .link{ font-size:30px; color:var(--text); font-weight:600; }
.cta-box .src{ font-size:19px; color:var(--faint); line-height:1.6; margin-top:26px;
  border-top:1px solid var(--line); padding-top:22px; }
.cta-box .src b{ color:var(--dim); font-weight:600; }
"""

def esc(s: str) -> str:
    return html.escape(s, quote=False)

# ---------------------------------------------------------------- slide renderers
def foot(who, n, total):
    return (f'<div class="foot"><span class="mark"><span class="dot"></span>'
            f'<span class="who">{who}</span></span>'
            f'<span class="pg"><b>{n:02d}</b> / {total:02d}</span></div>')

def cover(s, who, n, total):
    return f'''<section class="slide">
  <div class="topbar"><span class="tag">{esc(s["tag"])}</span><span class="tag">{esc(s["edition"])}</span></div>
  <div class="spacer"></div>
  <p class="eyebrow">{esc(s["eyebrow"])}</p>
  <div class="kicker-rule"></div>
  <h1 class="disp cover-title">{esc(s["title"])}</h1>
  <p class="cover-sub">{esc(s["subtitle"])}</p>
  <div class="cover-by">{esc(s["by"])}</div>
  <div class="spacer"></div>
  <div class="swipe">{esc(s["swipe"])} <span class="arrow">→</span></div>
  {foot(who, n, total)}
</section>'''

def content_head(s):
    return (f'<div class="topbar"><span class="tag">{esc(s["eyebrow"])}</span>'
            f'<span class="tag">{esc(s.get("idx",""))}</span></div>')

def statement(s, who, n, total):
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer"></div>
  <h2 class="disp stmt">{s["html"]}</h2>
  <div class="kicker-rule" style="margin:44px 0 34px"></div>
  <p class="body-lg">{s["body"]}</p>
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def stat(s, who, n, total):
    a, b = s["a"], s["b"]
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer"></div>
  <p class="eyebrow">{esc(s["eyebrow2"])}</p>
  <div class="kicker-rule"></div>
  <div class="stat-row">
    <div class="stat-card">
      <div class="stat-tag">{esc(a["tag"])}</div>
      <div class="stat-num">{esc(a["num"])}</div>
      <div class="stat-lbl">{a["lbl"]}</div>
    </div>
    <div class="stat-card hi">
      <div class="stat-tag">{esc(b["tag"])}</div>
      <div class="stat-num">{esc(b["num"])}</div>
      <div class="stat-lbl">{b["lbl"]}</div>
    </div>
  </div>
  <p class="stat-note">{s["note"]}</p>
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def split(s, who, n, total):
    cards = ""
    for c in s["cards"]:
        cls = "warn" if c.get("warn") else "good"
        cards += f'<div class="split-card {cls}"><h3>{esc(c["h"])}</h3><p>{c["p"]}</p></div>'
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer" style="flex:0 0 30px"></div>
  <h2 class="disp" style="font-size:52px;margin-bottom:14px">{esc(s["title"])}</h2>
  <div class="split">{cards}</div>
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def prose(s, who, n, total):
    paras = "".join(f'<p class="body-lg" style="margin-bottom:26px">{p}</p>' for p in s["paras"])
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer" style="flex:0 0 24px"></div>
  <h2 class="disp" style="font-size:56px;margin-bottom:34px">{esc(s["title"])}</h2>
  {paras}
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def steps(s, who, n, total):
    items = ""
    for i, st in enumerate(s["items"], 1):
        items += (f'<div class="step"><div class="n">{i:02d}</div>'
                  f'<div><h3>{esc(st["h"])}</h3><p>{st["p"]}</p></div></div>')
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer" style="flex:0 0 24px"></div>
  <h2 class="disp" style="font-size:56px;margin-bottom:12px">{esc(s["title"])}</h2>
  <div class="steps">{items}</div>
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def quote(s, who, n, total):
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer"></div>
  <div class="quote-mark">&ldquo;</div>
  <blockquote class="quote">{s["html"]}</blockquote>
  <div class="quote-by">{esc(s["by"])}</div>
  <div class="spacer"></div>
  {foot(who, n, total)}
</section>'''

def cta(s, who, n, total):
    return f'''<section class="slide">
  {content_head(s)}
  <div class="spacer"></div>
  <h2 class="disp cta-title">{s["title"]}</h2>
  <p class="cta-lead">{s["lead"]}</p>
  <div class="cta-box">
    <div class="lbl">{esc(s["boxlbl"])}</div>
    <div class="link">{esc(s["link"])}</div>
    <div class="src">{s["src"]}</div>
  </div>
  {foot(who, n, total)}
</section>'''

RENDER = {"cover":cover,"statement":statement,"stat":stat,"split":split,
          "prose":prose,"steps":steps,"quote":quote,"cta":cta}

def build_html(lang, who, slides):
    total = len(slides)
    body = ""
    for i, s in enumerate(slides, 1):
        body += RENDER[s["type"]](s, who, i, total) + "\n"
    return f'''<!doctype html>
<html lang="{lang}" data-theme="dark"><head><meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>{CSS}</style></head><body>
{body}</body></html>'''

# ---------------------------------------------------------------- content: ES
WHO_ES = "Ricardo&nbsp;Benavides &nbsp;·&nbsp; <b>Data&nbsp;Engineering&nbsp;SAP</b>"
SLIDES_ES = [
  {"type":"cover","tag":"Papper semanal","edition":"2026 · W28",
   "eyebrow":"Generative BI · Semantic Layer",
   "title":"El semantic layer decide si tus data agents dicen la verdad",
   "subtitle":"La generative BI confiable se gana en el contexto, no en el modelo.",
   "by":"Ricardo Benavides   ·   Data Architect & Data Engineering SAP   ·   julio 2026",
   "swipe":"Desliza"},

  {"type":"statement","eyebrow":"El punto de partida","idx":"El riesgo",
   "html":'Hay dos formas de fallar.<br/>Una es <span class="em">mucho peor</span>.',
   "body":'Un asistente de datos puede devolver un <strong>error</strong> —una molestia—, o devolver un <strong>número que se ve impecable y está equivocado</strong>. Lo segundo termina en una lámina de comité y mueve una decisión en la dirección equivocada.'},

  {"type":"prose","eyebrow":"La tesis","idx":"","title":"El problema casi nunca es el modelo",
   "paras":[
     'En la conversación sobre generative BI se pierde lo esencial: el modelo de lenguaje <strong>mejora cada trimestre y se abarata solo</strong>.',
     'Lo que decide si puedes confiar en la respuesta es el <strong>contexto</strong> —qué significa cada métrica, cuál es la tabla correcta, qué business rule aplica—. Ese contexto no lo aporta el modelo. Lo aportas tú, en el <strong>semantic layer</strong>.']},

  {"type":"stat","eyebrow":"Los números","idx":"dbt Labs · Benchmark 2026",
   "eyebrow2":"Acierto del text-to-SQL",
   "a":{"tag":"Set completo de preguntas","num":"64.5%",
        "lbl":'Text-to-SQL con buen prompting. <strong>Casi el doble</strong> que hace una generación (32.7%).'},
   "b":{"tag":"Dentro de un semantic layer","num":"~100%",
        "lbl":'Cuando las métricas y dimensiones ya están definidas, la query se vuelve <strong>determinista</strong>.'},
   "note":'Línea base sin ninguna capa de contexto: <b>~21–25%</b> de acierto.'},

  {"type":"split","eyebrow":"Lo que de verdad importa","idx":"Cómo falla cada uno",
   "title":"No es el porcentaje. Es cómo falla.",
   "cards":[
     {"good":True,"h":"El semantic layer","p":'Cuando <strong>no puede responder</strong>, te lo dice. Sabes que no sabe.'},
     {"warn":True,"h":"El text-to-SQL","p":'Entrega un dato <strong>equivocado con apariencia de verdad</strong>. Sin ninguna señal de alerta.'}]},

  {"type":"prose","eyebrow":"El concepto","idx":"Qué es, en concreto","title":"Una capa de traducción",
   "paras":[
     'Toma un schema de producción críptico y lo convierte en una <strong>interfaz de negocio</strong>, limpia y documentada, sobre la que la IA sí puede razonar.',
     'La clave: la lógica vive en la <strong>definición de la view</strong>, no en la memoria del modelo. Si <code>ingresos_netos</code> ya incluye <code>WHERE refund_flag = 0</code>, cada query hereda esa regla. La impone el <strong>motor SQL</strong>, no la buena voluntad del modelo.']},

  {"type":"quote","eyebrow":"La idea que hay que llevarse","idx":"",
   "html":'El modelo es un <span class="em">commodity</span>. El semantic layer es la <span class="em">ventaja defendible</span>.',
   "by":"— Y por eso Databricks apuesta por Genie Ontology, no por otro modelo"},

  {"type":"prose","eyebrow":"Si tu mundo es SAP","idx":"La lección","title":"Ya lo estabas construyendo",
   "paras":[
     'Al integrar SAP con Databricks, el valor no estuvo en el pipeline —mover datos es un problema resuelto—.',
     'Estuvo en el trabajo lento de <strong>definir qué significa cada métrica</strong> y dejarla gobernada en un solo lugar. Parecía deuda para que los reportes cuadraran. Era, sin saberlo, el <strong>semantic layer</strong> que hoy vuelve confiable a cualquier agente.']},

  {"type":"steps","eyebrow":"Cómo empezar","idx":"Sin intentar abarcarlo todo","title":"Empieza acotado",
   "items":[
     {"h":"Cinco métricas","p":"Las que tu negocio pregunta con más frecuencia. Ni una más."},
     {"h":"Modélalas bien","p":"Views documentadas y probadas para cada una."},
     {"h":"Valida contra la historia","p":"Compara las salidas del agente con valores que ya conoces. Luego, otras cinco."}]},

  {"type":"cta","eyebrow":"Cierre","idx":"2026 · W28",
   "title":'La pregunta no es qué <span class="accent">modelo</span> eliges.',
   "lead":"Es cuánto de tu negocio está codificado en un semantic layer gobernado. Ese porcentaje es el techo de lo que tus agentes pueden responder sin mentirte.",
   "boxlbl":"Análisis completo · con fuentes",
   "link":"rrbenavi-source.github.io/portfolio/publicaciones",
   "src":'<b>Fuentes:</b> dbt Labs (Benchmark 2026) · Dremio (A. Merced) · Databricks (Genie Ontology) · Snowflake Cortex Sense.'},
]

# ---------------------------------------------------------------- content: EN
WHO_EN = "Ricardo&nbsp;Benavides &nbsp;·&nbsp; <b>Data&nbsp;Engineering&nbsp;SAP</b>"
SLIDES_EN = [
  {"type":"cover","tag":"Weekly papper","edition":"2026 · W28",
   "eyebrow":"Generative BI · Semantic Layer",
   "title":"Your semantic layer decides whether your data agents tell the truth",
   "subtitle":"Reliable generative BI is won in the context, not in the model.",
   "by":"Ricardo Benavides   ·   Data Architect & Data Engineering SAP   ·   July 2026",
   "swipe":"Swipe"},

  {"type":"statement","eyebrow":"The stakes","idx":"The risk",
   "html":'There are two ways to fail.<br/>One is <span class="em">far worse</span>.',
   "body":'A data assistant can return an <strong>error</strong> —an inconvenience— or return a <strong>number that looks flawless and is wrong</strong>. The second ends up on a board slide and nudges a decision in the wrong direction.'},

  {"type":"prose","eyebrow":"The thesis","idx":"","title":"The problem is almost never the model",
   "paras":[
     'The generative-BI conversation misses the point: the language model <strong>gets better every quarter and cheaper on its own</strong>.',
     'What decides whether you can trust the answer is the <strong>context</strong> —what each metric means, which table is right, which business rule applies—. The model doesn’t supply that. You do, in the <strong>semantic layer</strong>.']},

  {"type":"stat","eyebrow":"The numbers","idx":"dbt Labs · 2026 Benchmark",
   "eyebrow2":"Text-to-SQL accuracy",
   "a":{"tag":"Full question set","num":"64.5%",
        "lbl":'Text-to-SQL with good prompting. <strong>Nearly double</strong> one generation ago (32.7%).'},
   "b":{"tag":"Inside a semantic layer","num":"~100%",
        "lbl":'Once metrics and dimensions are defined, query generation becomes <strong>deterministic</strong>.'},
   "note":'Baseline with no context layer at all: <b>~21–25%</b> accuracy.'},

  {"type":"split","eyebrow":"What actually matters","idx":"How each one fails",
   "title":"It isn’t the percentage. It’s how it fails.",
   "cards":[
     {"good":True,"h":"The semantic layer","p":'When it <strong>can’t answer</strong>, it tells you so. You know that it doesn’t know.'},
     {"warn":True,"h":"Text-to-SQL","p":'Hands you a <strong>wrong answer wearing the face of truth</strong>. Without blinking.'}]},

  {"type":"prose","eyebrow":"The concept","idx":"What it actually is","title":"A translation layer",
   "paras":[
     'It turns a cryptic production schema into a clean, documented <strong>business-friendly interface</strong> the AI can reason over.',
     'The key: the logic lives in the <strong>view definition</strong>, not the model’s head. If <code>net_revenue</code> already carries <code>WHERE refund_flag = 0</code>, every query inherits that rule. The <strong>SQL engine</strong> enforces it —not the model’s goodwill.']},

  {"type":"quote","eyebrow":"The idea to take away","idx":"",
   "html":'The model is a <span class="em">commodity</span>. The semantic layer is the <span class="em">moat</span>.',
   "by":"— Which is why Databricks is betting on Genie Ontology, not another model"},

  {"type":"prose","eyebrow":"If your world is SAP","idx":"The lesson","title":"You were already building it",
   "paras":[
     'When we integrated SAP with Databricks, the value wasn’t in the pipeline —moving data is a solved problem—.',
     'It was in the slow work of <strong>defining what each metric means</strong> and keeping it governed in one place. It felt like debt paid for consistent reports. It was, unknowingly, the <strong>semantic layer</strong> that now makes any agent trustworthy.']},

  {"type":"steps","eyebrow":"How to start","idx":"Without boiling the ocean","title":"Start narrow",
   "items":[
     {"h":"Five metrics","p":"The ones your business asks about most. Not one more."},
     {"h":"Model them well","p":"Documented, tested views for each one."},
     {"h":"Validate against history","p":"Check the agent’s output against values you already know. Then add five more."}]},

  {"type":"cta","eyebrow":"The close","idx":"2026 · W28",
   "title":'The question isn’t which <span class="accent">model</span> you pick.',
   "lead":"It’s how much of your business is encoded in a governed semantic layer. That share is the ceiling on what your agents can answer without lying to you.",
   "boxlbl":"Full analysis · with sources",
   "link":"rrbenavi-source.github.io/portfolio/en/publicaciones",
   "src":'<b>Sources:</b> dbt Labs (2026 Benchmark) · Dremio (A. Merced) · Databricks (Genie Ontology) · Snowflake Cortex Sense.'},
]

def render_pdf(lang, who, slides):
    html_path = HERE / f"linkedin-carousel-{lang}.html"
    pdf_path = HERE / f"linkedin-carousel-{lang}.pdf"
    html_path.write_text(build_html(lang, who, slides), encoding="utf-8")
    print(f"→ {pdf_path.name}")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ], check=True, stderr=subprocess.DEVNULL)
    print(f"  ✓ {pdf_path.stat().st_size // 1024} KB")

def main():
    if not Path(CHROME).exists():
        sys.exit(f"✗ Chrome no encontrado: {CHROME}")
    render_pdf("es", WHO_ES, SLIDES_ES)
    render_pdf("en", WHO_EN, SLIDES_EN)
    print("Listo.")

if __name__ == "__main__":
    main()
