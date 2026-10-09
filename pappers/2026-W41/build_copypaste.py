"""Convierte el cuerpo de draft-es.md en texto para el editor de LinkedIn: un párrafo = una línea."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
FIG_FILES = ("fig-nlq-retirada.png", "fig-misma-pregunta.png", "fig-escalera.png")


def unwrap(block: str) -> str:
    return " ".join(ln.strip() for ln in block.splitlines())


def to_linkedin(md: str) -> str:
    body = md.split("\n## ", 2)[2]  # quita título y subtítulo (van en sus propios campos)
    body = body.split("\n---\n")[0]  # quita Fuentes
    body = "## " + body
    out: list[str] = []
    intro, rest = md.split("\n## ", 2)[1].split("\n", 1)[1], body
    fig_n = 0
    for para in re.split(r"\n\s*\n", intro.strip() + "\n\n" + rest.strip()):
        para = para.strip()
        if para.startswith("## "):
            out.append(para[3:].strip())
        elif para.startswith("[ FIG"):
            fig_n += 1
            out.append(f"[ Sube la figura {fig_n}: {FIG_FILES[fig_n - 1]} ]")
        elif para.startswith("|"):
            rows = [ln for ln in para.splitlines() if not ln.startswith("|---")][1:]
            cells = [[c.strip() for c in ln.strip("|").split("|")] for ln in rows]
            out.append("\n".join(" → ".join(c) for c in cells))
        elif para.startswith("- ") or re.match(r"^\d+\. ", para):
            items = re.split(r"\n(?=- |\d+\. )", para)
            out.append("\n".join(unwrap(it).replace("- ", "• ", 1) if it.startswith("- ") else unwrap(it)
                                 for it in items))
        else:
            out.append(unwrap(para))
    if fig_n != 3:
        sys.exit(f"se esperaban 3 figuras, hubo {fig_n}")
    text = "\n\n".join(out)
    return re.sub(r"\*{1,2}([^*]+?)\*{1,2}", r"\1", text)  # LinkedIn no interpreta markdown


if __name__ == "__main__":
    print(to_linkedin((HERE / "draft-es.md").read_text()))
