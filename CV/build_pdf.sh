#!/usr/bin/env bash
# Renderiza los CV HTML a PDF de alta gama vía Chrome headless (--print-to-pdf).
# Genera 4 PDFs: ES/EN × claro/oscuro. Uso: bash build_pdf.sh
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [ ! -x "$CHROME" ]; then
  echo "✗ No se encontró Google Chrome en: $CHROME" >&2
  exit 1
fi

# render <html_src> <theme: light|dark> <out_pdf>
render() {
  local src="$1" theme="$2" out="$3"
  local tmp="$TMP/$(basename "$src" .html)-$theme.html"
  sed "s/data-theme=\"light\"/data-theme=\"$theme\"/" "$DIR/$src" > "$tmp"
  echo "→ $out  (tema: $theme)"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$DIR/$out" "file://$tmp" 2>/dev/null
  echo "  ✓ $(du -h "$DIR/$out" | cut -f1)"
}

# Diseño 1 — Ejecutivo (barra lateral)
render "cv-es.html" light "CV-Ricardo-Benavides-ES-claro.pdf"
render "cv-es.html" dark  "CV-Ricardo-Benavides-ES-oscuro.pdf"
render "cv-en.html" light "CV-Ricardo-Benavides-EN-light.pdf"
render "cv-en.html" dark  "CV-Ricardo-Benavides-EN-dark.pdf"

# Diseño 2 — Bento / KPI dashboard
render "cv-es-bento.html" light "CV-Ricardo-Benavides-ES-bento-claro.pdf"
render "cv-es-bento.html" dark  "CV-Ricardo-Benavides-ES-bento-oscuro.pdf"
render "cv-en-bento.html" light "CV-Ricardo-Benavides-EN-bento-light.pdf"
render "cv-en-bento.html" dark  "CV-Ricardo-Benavides-EN-bento-dark.pdf"

echo "Listo. PDFs en: $DIR"
