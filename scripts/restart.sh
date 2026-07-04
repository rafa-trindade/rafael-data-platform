#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

if [ $# -eq 0 ]; then
  log "Reiniciando todos os serviços..."
  dc restart
else
  log "Reiniciando: $*"
  dc restart "$@"
fi
ok "Reinício concluído."