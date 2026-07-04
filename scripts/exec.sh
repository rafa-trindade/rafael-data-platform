#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

if [ $# -eq 0 ]; then
  err "Uso: ./shell.sh <serviço>  (ex: postgres, mongodb, minio, redis, dremio)"
  exit 1
fi

CONTAINER="lab-$1"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  err "Container $CONTAINER não está rodando."
  exit 1
fi

# tenta bash, cai pra sh se não existir
docker exec -it "$CONTAINER" bash 2>/dev/null || docker exec -it "$CONTAINER" sh