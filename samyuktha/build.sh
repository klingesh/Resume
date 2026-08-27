#!/usr/bin/env bash
# Renders samyuktha/resume.html into Samyuktha_Ajay_Resume.pdf (A4, single page).
#
# Requires a Chromium/Chrome binary. Set CHROME to override the default path.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="${1:-$HERE/../Samyuktha_Ajay_Resume.pdf}"
CHROME="${CHROME:-/opt/playwright/chromium-1232/chrome-linux64/chrome}"

"$CHROME" \
  --headless --no-sandbox --disable-gpu \
  --allow-file-access-from-files \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" \
  "file://$HERE/resume.html"

echo "wrote $OUT"
