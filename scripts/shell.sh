#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

set -a
source "$PROJECT_ROOT/docker/.env"
set +a

if [ $# -eq 0 ]; then
  err "Uso: ./scripts/shell.sh <serviço>"
  echo
  echo "Serviços disponíveis:"
  echo "  postgres"
  echo "  mongodb"
  echo "  redis"
  echo "  minio"
  echo "  dremio"
  echo "  portainer"
  echo "  mongo-express"
  echo "  redisinsight"
  exit 1
fi

SERVICE="$1"
CONTAINER="lab-$SERVICE"

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  err "Container '$CONTAINER' não está rodando."
  exit 1
fi

case "$SERVICE" in
  postgres)
    docker exec -it "$CONTAINER" \
      psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
    ;;

  mongodb)
    docker exec -it "$CONTAINER" \
      mongosh -u "$MONGO_USER" -p "$MONGO_PASSWORD" admin
    ;;

  redis)
    docker exec -it -e REDISCLI_AUTH="$REDIS_PASSWORD" "$CONTAINER" \
      redis-cli
    ;;

  *)
    docker exec -it "$CONTAINER" bash 2>/dev/null || \
    docker exec -it "$CONTAINER" sh
    ;;
esac