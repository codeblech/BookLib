#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

VAULT="$HOME/obsidian/obsidian"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$HOME/obsidian/BookLib/BookLib/site"

echo "[1/3] Pulling latest vault changes..."
if [ -d "$VAULT/.git" ]; then
  (
    cd "$VAULT" || exit 0
    GIT_TERMINAL_PROMPT=0 git pull --ff-only 2>/dev/null || {
      echo "[!] Git pull failed or not available. Using local files."
    }
  )
else
  echo "[!] Vault is not a git repo. Using local files."
fi

echo "[2/3] Generating site..."
mkdir -p "$SITE_DIR"
python3 "$SCRIPT_DIR/generate.py" \
  --vault "$VAULT" \
  --output "$SITE_DIR/index.html"

echo "[3/3] Done. Site built at $SITE_DIR/index.html"
