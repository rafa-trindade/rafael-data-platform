# Backup

`scripts/backup.sh` gera um snapshot em `backups/<timestamp>/` contendo:

- `postgres/_globals.sql` - papéis, usuários e permissões globais (`pg_dumpall --globals-only`)
- `postgres/<nome_do_banco>.sql` - um dump completo por banco existente no Postgres (`pg_dump`), descoberto automaticamente - cobre todos os bancos, não só um fixo
- `mongodb.archive` - dump via `mongodump --archive`
- `minio_data.tar.gz` - cópia completa do volume do MinIO
- `dremio_data.tar.gz` - cópia completa do volume do Dremio (metadados/config)

## Uso

```bash
./scripts/backup.sh
```

O timestamp do último backup fica salvo em `backups/latest`.

## Como funciona a descoberta de bancos

O script consulta `pg_database` no Postgres (`SELECT datname FROM pg_database WHERE datistemplate = false`) e gera um dump separado para cada banco encontrado - incluindo o `postgres` (banco de manutenção padrão) e qualquer banco adicional criado depois (ex: bancos das Camadas 3/4 do projeto). Não é preciso editar o script quando novos bancos forem criados.

## Por que Postgres é separado em arquivo por banco (em vez de um `pg_dumpall` único)

Um `pg_dumpall` gera um único arquivo com tudo junto, dificultando restaurar **só um banco específico**. Com um arquivo por banco, o `restore.sh` pode restaurar seletivamente sem afetar os demais.

## Frequência recomendada

Para um lab pessoal, rodar manualmente antes de qualquer `update.sh` ou mudança estrutural já é suficiente. Se quiser automatizar, agende via `cron`:

```bash
0 3 * * * /opt/rafael-data-platform/scripts/backup.sh >> /opt/rafael-data-platform/backups/backup.log 2>&1
```