#!/usr/bin/env bash
# Renders the LinkedIn / Open Graph thumbnail (1200×630) from og-template.html
# via headless Chrome — same pipeline as CV/build_pdf.sh. Output → web/public/og-image.png
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$DIR/../public/og-image.png"

"$CHROME" --headless=new \
  --screenshot="$OUT" \
  --window-size=1200,630 \
  --force-device-scale-factor=2 \
  --hide-scrollbars \
  --virtual-time-budget=2500 \
  --default-background-color=00000000 \
  "file://$DIR/og-template.html"

echo "✅ og-image.png → $OUT"
