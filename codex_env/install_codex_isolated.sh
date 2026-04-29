#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR"
export NVM_DIR="$BASE_DIR/.nvm"
export CODEX_HOME="$BASE_DIR/.codex"
NVM_INSTALLER="$SCRIPT_DIR/vendor/nvm-install.sh"

mkdir -p "$BASE_DIR" "$CODEX_HOME" "$NVM_DIR"

echo "[1/5] Installing dependencies..."
if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y curl ca-certificates git
fi

echo "[2/5] Installing nvm..."
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    bash "$NVM_INSTALLER"
fi

source "$NVM_DIR/nvm.sh"

echo "[3/5] Installing Node.js LTS..."
nvm install --lts
nvm alias default 'lts/*'
nvm use default

echo "[4/5] Installing Codex CLI..."
npm install -g @openai/codex

echo "[5/5] Securing Codex directory..."
chmod 700 "$CODEX_HOME"


chmod +x "$SCRIPT_DIR/start_codex.sh"

echo
echo "Done."
echo "Codex path: $(command -v codex)"
echo "Node path:  $(command -v node)"
echo
echo "Next:"
echo "  $SCRIPT_DIR/start_codex.sh"
