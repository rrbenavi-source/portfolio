#!/usr/bin/env bash
# Renderiza los pappers a PDF vía Chrome headless. Uso: bash build_pdf.sh <week_dir>
# Espera en <week_dir>: meta-es.txt / meta-en.txt (línea única: eyebrow|title|subtitle|meta)
# IMPORTANTE: ninguno de los 4 campos de meta-*.txt puede contener el carácter '|' literal
#             (es el delimitador del propio archivo); usa comas, guiones u otro separador
#             si necesitas encadenar ideas dentro de un campo.
# y body-es.html / body-en.html y sources-es.html / sources-en.html
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WEEK="${1:?Uso: build_pdf.sh <week_dir>}"
WEEK="$(cd "$WEEK" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
[ -x "$CHROME" ] || { echo "✗ Chrome no encontrado: $CHROME" >&2; exit 1; }

# Sustitución LITERAL de un único marcador {{MARKER}} por un valor arbitrario.
# No usa regex ni trata '&' / '\' como especiales (a diferencia de sed y de `awk -v`,
# que sí procesan backreferences '&' en el reemplazo y escapes '\' en el valor).
# El valor viaja por variable de entorno (ENVIRON) — nunca por `awk -v` — precisamente
# para que backslashes en el valor lleguen intactos a awk.
literal_sub() { # <infile> <marker> <value> <outfile>
  local infile="$1" marker="$2" value="$3" outfile="$4"
  REPL_MARKER="$marker" REPL_VALUE="$value" awk '
    BEGIN {
      marker = ENVIRON["REPL_MARKER"]
      value  = ENVIRON["REPL_VALUE"]
      mlen   = length(marker)
    }
    {
      line = $0; out = ""
      while ((idx = index(line, marker)) > 0) {
        out = out substr(line, 1, idx - 1) value
        line = substr(line, idx + mlen)
      }
      print out line
    }
  ' "$infile" > "$outfile"
}

# Valida que meta-$lang.txt produzca exactamente 4 campos no vacíos.
validate_meta_line() { # <rawline> <lang>
  local rawline="$1" lang="$2" nf
  nf=$(awk -F'|' '{print NF}' <<< "$rawline")
  if [ "$nf" -ne 4 ]; then
    echo "✗ meta-$lang.txt: se esperaban 4 campos 'eyebrow|title|subtitle|meta' separados por '|', se encontraron $nf" >&2
    exit 1
  fi
  awk -F'|' -v lang="$lang" '{
    for (i = 1; i <= 4; i++) {
      v = $i
      gsub(/^[ \t]+|[ \t]+$/, "", v)
      if (v == "") {
        print "✗ meta-" lang ".txt: el campo " i " de 4 está vacío" > "/dev/stderr"
        exit 1
      }
    }
  }' <<< "$rawline"
}

render() { # <lang> <theme> <out>
  local lang="$1" theme="$2" out="$3"
  local rawline eyebrow title subtitle metaline body sources html

  # `read` devuelve !=0 si al archivo le falta el salto de línea final, aunque las
  # variables sí queden pobladas; con `set -e` eso abortaría el script sin motivo real.
  IFS= read -r rawline < "$WEEK/meta-$lang.txt" || true
  [ -n "${rawline:-}" ] || { echo "✗ meta-$lang.txt está vacío o no se pudo leer" >&2; exit 1; }
  validate_meta_line "$rawline" "$lang"
  IFS='|' read -r eyebrow title subtitle metaline <<< "$rawline"

  body="$(cat "$WEEK/body-$lang.html")"
  sources="$(cat "$WEEK/sources-$lang.html")"

  html="$TMP/papper-$lang-$theme.html"
  # data-theme opera sobre una cadena fija (sin interpolación de contenido), sed es seguro aquí.
  sed -e "s/data-theme=\"light\"/data-theme=\"$theme\"/" "$DIR/papper.html" > "$html.stage0"
  literal_sub "$html.stage0" "{{EYEBROW}}"      "$eyebrow"  "$html.stage1"
  literal_sub "$html.stage1" "{{TITLE}}"        "$title"    "$html.stage2"
  literal_sub "$html.stage2" "{{SUBTITLE}}"     "$subtitle" "$html.stage3"
  literal_sub "$html.stage3" "{{META}}"         "$metaline" "$html.stage4"
  literal_sub "$html.stage4" "{{BODY_HTML}}"    "$body"     "$html.stage5"
  literal_sub "$html.stage5" "{{SOURCES_HTML}}" "$sources"  "$html"

  echo "→ $out (tema: $theme)"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$WEEK/$out" "file://$html" 2>/dev/null
  echo "  ✓ $(du -h "$WEEK/$out" | cut -f1)"
}

render es light "papper-es.pdf"
render en light "papper-en.pdf"
echo "Listo. PDFs en: $WEEK"
