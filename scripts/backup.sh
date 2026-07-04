#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEST="$BACKUP_DIR/$TIMESTAMP"
mkdir -p "$DEST"

POSTGRES_USER=$(grep POSTGRES_USER "$ENV_FILE" | cut -d= -f2)
MONGO_USER=$(grep MONGO_USER "$ENV_FILE" | cut -d= -f2)
MONGO_PASSWORD=$(grep MONGO_PASSWORD "$ENV_FILE" | cut -d= -f2)

log "Backup iniciado em $DEST"

log "1/4 Postgres (todos os bancos)..."
mkdir -p "$DEST/postgres"

# Dump dos papéis/usuários e permissões globais (não pertence a nenhum banco específico)
docker exec lab-postgres pg_dumpall -U "$POSTGRES_USER" --globals-only \
  > "$DEST/postgres/_globals.sql"

# Lista todos os bancos, exceto os templates internos do Postgres
DATABASES=$(docker exec lab-postgres psql -U "$POSTGRES_USER" -d postgres -tAc \
  "SELECT datname FROM pg_database WHERE datistemplate = false;")

for DB in $DATABASES; do
  log "   -> dump de '$DB'"
  docker exec lab-postgres pg_dump -U "$POSTGRES_USER" "$DB" \
    > "$DEST/postgres/${DB}.sql"
done

ok "Postgres salvo (bancos: $(echo $DATABASES | tr '\n' ' '))."

log "2/4 MongoDB..."
docker exec lab-mongodb mongodump \
  --username "$MONGO_USER" --password "$MONGO_PASSWORD" \
  --authenticationDatabase admin \
  --archive="/tmp/mongo_backup.archive"
docker cp lab-mongodb:/tmp/mongo_backup.archive "$DEST/mongodb.archive"
docker exec lab-mongodb rm -f /tmp/mongo_backup.archive
ok "MongoDB salvo."

log "3/4 MinIO (volume completo)..."
docker run --rm \
  -v minio_data:/data:ro \
  -v "$DEST":/backup \
  alpine tar czf /backup/minio_data.tar.gz -C /data .
ok "MinIO salvo."

log "4/4 Dremio (metadados/volume completo)..."
docker run --rm \
  -v dremio_data:/data:ro \
  -v "$DEST":/backup \
  alpine tar czf /backup/dremio_data.tar.gz -C /data .
ok "Dremio salvo."

echo "$TIMESTAMP" > "$BACKUP_DIR/latest"

ok "Backup completo em: $DEST"
du -sh "$DEST"