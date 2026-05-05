#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

VAULT="${VAULT:-$HOME/obsidian}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$VAULT/BookLib/site"

echo "[1/3] Pulling latest changes..."
cd "$VAULT"
git pull

echo "[2/3] Generating site..."
mkdir -p "$SITE_DIR"
python3 "$SCRIPT_DIR/generate.py" \
  --vault "$VAULT" \
  --output "$SITE_DIR/index.html"

echo "[3/3] Done. Site built at $SITE_DIR/index.html"
