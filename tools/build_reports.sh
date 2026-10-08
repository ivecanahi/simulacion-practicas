#!/usr/bin/env bash
# Generates every practice report PDF from its reporte/reporte.html with headless Chrome.
# Usage: tools/build_reports.sh
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
chrome="$(command -v google-chrome || command -v chromium || command -v chromium-browser)"

for html in "$root"/Unidad*/practica*/reporte/reporte.html; do
  practice_dir="$(dirname "$(dirname "$html")")"
  number="$(basename "$practice_dir" | sed 's/practica//')"
  output="$practice_dir/Reporte_Practica_${number}.pdf"
  "$chrome" --headless=new --disable-gpu --no-pdf-header-footer \
    --allow-file-access-from-files --print-to-pdf="$output" "file://$html" 2>/dev/null
  echo "OK  $output"
done
