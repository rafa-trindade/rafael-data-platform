# Rafael Data Platform

Lab pessoal de engenharia de dados, self-hosted em VPS via Docker Compose.

## Stack

PostgreSQL · MinIO · Dremio · MongoDB · Mongo Express · Redis · RedisInsight · Portainer

Veja detalhes em [`docs/architecture.md`](docs/architecture.md) e [`docs/services.md`](docs/services.md).
Veja detalhes em [`docs/architecture.md`](docs/architecture.md), [`docs/services.md`](docs/services.md) e [`docs/security.md`](docs/security.md).

---

## 🚀 Primeira execução (setup do zero)

```bash
# 1. Criar a estrutura de pastas
mkdir -p /opt/rafael-data-platform/{docker,docs,scripts,backups}
cd /opt/rafael-data-platform

# 2. Colar cada arquivo no caminho correspondente
#    (docker/docker-compose.yml, docker/.env, docker/.env.example,
#     scripts/*.sh, docs/*.md, README.md, LICENSE, .gitignore)

# 3. Dar permissão de execução aos scripts
chmod +x scripts/*.sh

# 4. Garantir que o volume do Postgres existe (cria só se não existir)
docker volume inspect docker_postgres_data >/dev/null 2>&1 || docker volume create docker_postgres_data

# 5. Instalar (cria rede, valida .env, sobe a stack)
./scripts/install.sh

# 6. Conferir se subiu tudo certo
./scripts/health.sh
```

Se `install.sh` reclamar de `docker/.env` ausente, copie o exemplo e ajuste as senhas antes de rodar de novo:

```bash
cp docker/.env.example docker/.env
nano docker/.env
```

---

## 🛠️ O que cada script faz

| Script | O que faz |
|--------|-----------|
| `install.sh` | Setup inicial: cria a rede `data-platform` se não existir, valida se o volume externo do Postgres existe, checa se `docker/.env` foi criado, cria a pasta `backups/` e sobe todos os containers (`up -d`). Rodar só uma vez (ou depois de um reset total). |
| `start.sh` | Sobe todos os serviços (`docker compose up -d`). Usa se a stack já foi instalada e só precisa ser (re)ligada. |
| `stop.sh` | Para e remove os containers (`docker compose down`), **sem apagar volumes**. Os dados continuam intactos, só os containers somem até o próximo `start.sh`. |
| `restart.sh` | Reinicia todos os serviços, ou só um específico se você passar o nome: `./scripts/restart.sh postgres`. |
| `logs.sh` | Mostra logs em tempo real. Sem argumento, mostra de todos os serviços; com argumento, só do serviço pedido: `./scripts/logs.sh minio`. |
| `health.sh` | Checagem de saúde: lista status dos containers e testa se cada endpoint HTTP (MinIO, Dremio, Mongo Express, RedisInsight, Portainer) responde, além de testar conexão real no Postgres e no Redis. |
| `update.sh` | Puxa as imagens mais recentes (`docker compose pull`), recria os containers com elas e limpa imagens antigas não usadas. |
| `shell.sh` | Conecta direto no cliente nativo do serviço, já autenticado com as credenciais do `.env`: `psql` (postgres), `mongosh` (mongodb), `redis-cli` (redis). Para os demais serviços (minio, dremio, portainer, mongo-express, redisinsight), abre um shell genérico (`bash`/`sh`) dentro do container. |
| `exec.sh` | Abre um shell genérico (`bash`/`sh`) dentro de qualquer container, sem lógica de autenticação - útil pra debug bruto: `./scripts/exec.sh postgres`. |
| `backup.sh` | Gera um snapshot em `backups/<timestamp>/` com dump do Postgres, dump do MongoDB e cópia completa dos volumes de MinIO e Dremio. Ver [`docs/backup.md`](docs/backup.md). |
| `restore.sh` | Restaura um snapshot gerado pelo `backup.sh`, pedindo confirmação antes de sobrescrever os dados. Ver [`docs/restore.md`](docs/restore.md). |

---

## Operação do dia a dia (referência rápida)

| Ação | Comando |
|------|---------|
| Subir tudo | `./scripts/start.sh` |
| Parar tudo | `./scripts/stop.sh` |
| Reiniciar um serviço | `./scripts/restart.sh postgres` |
| Ver logs | `./scripts/logs.sh minio` |
| Checar saúde | `./scripts/health.sh` |
| Atualizar imagens | `./scripts/update.sh` |
| Entrar num container (cliente nativo) | `./scripts/shell.sh mongodb` |
| Entrar num container (shell bruto) | `./scripts/exec.sh mongodb` |
| Backup | `./scripts/backup.sh` |
| Restore | `./scripts/restore.sh <timestamp>` |
| Acessar Postgres/Mongo/Redis do seu PC | Abrir túnel SSH - ver [`docs/security.md`](docs/security.md) |

## Estrutura

```
docker/     → compose + env
docs/       → documentação
scripts/    → automação operacional
backups/    → snapshots gerados por backup.sh
```

## Licença

MIT - veja [LICENSE](LICENSE).