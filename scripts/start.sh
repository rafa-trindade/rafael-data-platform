#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

log "Subindo todos os serviços..."
dc up -d
ok "Stack no ar."