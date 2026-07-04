#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

if [ $# -eq 0 ]; then
  err "Uso: ./restore.sh <timestamp>  (ex: 20260703_143000)"
  echo "Backups disponíveis:"
  ls -1 "$BACKUP_DIR" | grep -v latest
  exit 1
fi

SRC="$BACKUP_DIR/$1"
if [ ! -d "$SRC" ]; then
  err "Backup $1 não encontrado em $BACKUP_DIR"
  exit 1
fi

POSTGRES_USER=$(grep POSTGRES_USER "$ENV_FILE" | cut -d= -f2)
MONGO_USER=$(grep MONGO_USER "$ENV_FILE" | cut -d= -f2)
MONGO_PASSWORD=$(grep MONGO_PASSWORD "$ENV_FILE" | cut -d= -f2)

if [ ! -d "$SRC/postgres" ]; then
  err "Backup $1 está no formato antigo (sem pasta postgres/). Não é compatível com este restore.sh."
  echo "Rode um novo ./scripts/backup.sh para gerar um backup no formato atual antes de restaurar."
  exit 1
fi

read -rp "Isso vai SOBRESCREVER os dados atuais. Confirma? (digite 'sim'): " CONFIRM
[ "$CONFIRM" = "sim" ] || { err "Cancelado."; exit 1; }

log "1/4 Restaurando Postgres (todos os bancos)..."

# Restaura papéis/usuários e permissões globais primeiro
if [ -f "$SRC/postgres/_globals.sql" ]; then
  log "   -> restaurando papéis/permissões globais"
  cat "$SRC/postgres/_globals.sql" | docker exec -i lab-postgres psql -U "$POSTGRES_USER" -d postgres 2>/dev/null || true
fi

for DUMP_FILE in "$SRC"/postgres/*.sql; do
  [ -f "$DUMP_FILE" ] || continue
  DB=$(basename "$DUMP_FILE" .sql)
  [ "$DB" = "_globals" ] && continue

  log "   -> restaurando '$DB'"

  if [ "$DB" = "postgres" ]; then
    # banco de manutenção padrão: nunca dropar, só restaurar por cima
    cat "$DUMP_FILE" | docker exec -i lab-postgres psql -U "$POSTGRES_USER" -d "$DB" >/dev/null
  else
    # dropa e recria do zero, garantindo estado idêntico ao backup
    docker exec lab-postgres psql -U "$POSTGRES_USER" -d postgres -c \
      "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB' AND pid <> pg_backend_pid();" >/dev/null
    docker exec lab-postgres psql -U "$POSTGRES_USER" -d postgres -c "DROP DATABASE IF EXISTS \"$DB\";" >/dev/null
    docker exec lab-postgres psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE \"$DB\";" >/dev/null

    cat "$DUMP_FILE" | docker exec -i lab-postgres psql -U "$POSTGRES_USER" -d "$DB" >/dev/null
  fi
done

ok "Postgres restaurado."

log "2/4 Restaurando MongoDB..."
docker cp "$SRC/mongodb.archive" lab-mongodb:/tmp/mongo_backup.archive
docker exec lab-mongodb mongorestore \
  --username "$MONGO_USER" --password "$MONGO_PASSWORD" \
  --authenticationDatabase admin \
  --archive="/tmp/mongo_backup.archive" --drop
docker exec lab-mongodb rm -f /tmp/mongo_backup.archive
ok "MongoDB restaurado."

log "3/4 Restaurando MinIO..."
dc stop minio
docker run --rm -v minio_data:/data -v "$SRC":/backup alpine \
  sh -c "rm -rf /data/* && tar xzf /backup/minio_data.tar.gz -C /data"
dc start minio
ok "MinIO restaurado."

log "4/4 Restaurando Dremio..."
dc stop dremio
docker run --rm -v dremio_data:/data -v "$SRC":/backup alpine \
  sh -c "rm -rf /data/* && tar xzf /backup/dremio_data.tar.gz -C /data"
dc start dremio
ok "Dremio restaurado."

ok "Restore completo a partir de $1"