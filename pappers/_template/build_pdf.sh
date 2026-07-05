#!/usr/bin/env bash
# Renderiza los pappers a PDF vía Chrome headless. Uso: bash build_pdf.sh <week_dir>
# Espera en <week_dir>: meta-es.txt / meta-en.txt (líneas: eyebrow|title|subtitle|meta)
# y body-es.html / body-en.html y sources-es.html / sources-en.html
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WEEK="${1:?Uso: build_pdf.sh <week_dir>}"
WEEK="$(cd "$WEEK" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
[ -x "$CHROME" ] || { echo "✗ Chrome no encontrado: $CHROME" >&2; exit 1; }

render() { # <lang> <theme> <out>
  local lang="$1" theme="$2" out="$3"
  local meta body sources html
  IFS='|' read -r eyebrow title subtitle metaline < "$WEEK/meta-$lang.txt"
  body="$(cat "$WEEK/body-$lang.html")"
  sources="$(cat "$WEEK/sources-$lang.html")"
  html="$TMP/papper-$lang-$theme.html"
  sed -e "s/data-theme=\"light\"/data-theme=\"$theme\"/" \
      -e "s|{{EYEBROW}}|$eyebrow|" -e "s|{{TITLE}}|$title|" \
      -e "s|{{SUBTITLE}}|$subtitle|" -e "s|{{META}}|$metaline|" \
      "$DIR/papper.html" > "$html.stage"
  # inyectar bloques HTML multilínea con awk (evita problemas de sed con saltos)
  awk -v b="$body" '{gsub(/\{\{BODY_HTML\}\}/,b)}1' "$html.stage" > "$html.stage2"
  awk -v s="$sources" '{gsub(/\{\{SOURCES_HTML\}\}/,s)}1' "$html.stage2" > "$html"
  echo "→ $out (tema: $theme)"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$WEEK/$out" "file://$html" 2>/dev/null
  echo "  ✓ $(du -h "$WEEK/$out" | cut -f1)"
}

render es light "papper-es.pdf"
render en light "papper-en.pdf"
echo "Listo. PDFs en: $WEEK"
