#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

log "Status dos containers:"
docker ps --filter "name=lab-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
log "Checando endpoints..."

check_http() {
  local name="$1" url="$2"
  if curl -sf -o /dev/null --max-time 3 "$url"; then
    ok "$name ($url)"
  else
    err "$name ($url)"
  fi
}

check_http "MinIO"        "http://localhost:9000/minio/health/live"
check_http "Dremio"       "http://localhost:9047"
check_http "RedisInsight" "http://localhost:5540"
check_http "pgAdmin" "http://localhost:5050/misc/ping"

# Mongo Express usa Basic Auth: 401 é esperado e significa "no ar"
MEXP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://localhost:8081")
if [ "$MEXP_CODE" = "200" ] || [ "$MEXP_CODE" = "401" ]; then
  ok "Mongo Express (http://localhost:8081) [$MEXP_CODE]"
else
  err "Mongo Express (http://localhost:8081) [$MEXP_CODE]"
fi

# Portainer usa HTTPS com certificado autoassinado
if curl -sfk -o /dev/null --max-time 3 "https://localhost:9443"; then
  ok "Portainer (https://localhost:9443)"
else
  err "Portainer (https://localhost:9443)"
fi

echo ""
log "Checando Postgres..."
if docker exec lab-postgres pg_isready -U "$(grep POSTGRES_USER "$ENV_FILE" | cut -d= -f2)" >/dev/null 2>&1; then
  ok "Postgres respondendo"
else
  err "Postgres não respondeu"
fi

log "Checando Redis..."
REDIS_PASS=$(grep REDIS_PASSWORD "$ENV_FILE" | cut -d= -f2)
if docker exec lab-redis redis-cli -a "$REDIS_PASS" ping 2>/dev/null | grep -q PONG; then
  ok "Redis respondendo"
else
  err "Redis não respondeu"
fi