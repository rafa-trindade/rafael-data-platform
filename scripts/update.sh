#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

log "Puxando imagens mais recentes..."
dc pull

log "Recriando containers com as novas imagens..."
dc up -d --remove-orphans

log "Limpando imagens antigas não usadas..."
docker image prune -f

ok "Update concluído."