#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

VAULT="$HOME/obsidian/obsidian"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$HOME/obsidian/BookLib/BookLib/site"

echo "[1/2] Generating site..."
mkdir -p "$SITE_DIR"
python3 "$SCRIPT_DIR/generate.py" \
  --vault "$VAULT" \
  --output "$SITE_DIR/index.html"

echo "[2/2] Done. Site built at $SITE_DIR/index.html"
