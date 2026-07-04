#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

log "Verificando rede 'data-platform'..."
docker network inspect data-platform >/dev/null 2>&1 || {
  log "Criando rede 'data-platform'..."
  docker network create data-platform
}

log "Verificando volumes externos..."
EXTERNAL_VOLUMES=(docker_postgres_data minio_data mongodb_data redis_data redisinsight_data dremio_data portainer_data pgadmin_data)

for VOL in "${EXTERNAL_VOLUMES[@]}"; do
  if ! docker volume inspect "$VOL" >/dev/null 2>&1; then
    log "  -> criando volume '$VOL' (não existia)"
    docker volume create "$VOL"
  fi
done

if [ ! -f "$ENV_FILE" ]; then
  err "Arquivo docker/.env não encontrado. Copie docker/.env.example para docker/.env e ajuste as senhas."
  exit 1
fi

mkdir -p "$BACKUP_DIR"

log "Subindo stack..."
dc up -d

ok "Instalação concluída. Use scripts/health.sh para verificar o status."