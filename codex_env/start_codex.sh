#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR"
DEFAULT_WORKDIR="$PWD"
export NVM_DIR="$BASE_DIR/.nvm"
export CODEX_HOME="$BASE_DIR/.codex"

if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    echo "nvm is not installed under $NVM_DIR. Run $SCRIPT_DIR/install_codex_isolated.sh first." >&2
    exit 1
fi

source "$NVM_DIR/nvm.sh"
nvm use default >/dev/null

cd "${1:-$DEFAULT_WORKDIR}"


export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:27897}"
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:27897}"
export ALL_PROXY="${ALL_PROXY:-socks5h://127.0.0.1:27897}"

exec codex
