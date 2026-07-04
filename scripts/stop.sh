#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

log "Parando e removendo containers (volumes preservados)..."
dc down
ok "Stack parada."