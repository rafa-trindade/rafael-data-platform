# Rafael Data Platform

Lab pessoal de engenharia de dados, self-hosted em VPS via Docker Compose.

## Stack

PostgreSQL · pgAdmin · MinIO · Dremio · MongoDB · Mongo Express · Redis · RedisInsight · Portainer

Veja detalhes em [`docs/architecture.md`](docs/architecture.md), [`docs/services.md`](docs/services.md) e [`docs/security.md`](docs/security.md).

---

## 🎯 Propósito

Este projeto é um laboratório pessoal de engenharia de dados: uma plataforma completa (data lake, DW, query engine, NoSQL, cache) usada como campo de treino para uma trilha estruturada de estudos - de pipelines e orquestração até dbt, CI/CD e disaster recovery.

📚 A trilha completa de exercícios e projetos está em [`docs/projects.md`](docs/projects.md).

---

## 🚀 Primeira execução (setup do zero)

```bash
# 1. Clonar o repositório
git clone <url_do_repositorio> /opt/rafael-data-platform
cd /opt/rafael-data-platform

# 2. Criar o .env a partir do exemplo e ajustar as senhas
cp docker/.env.example docker/.env
nano docker/.env

# 3. Dar permissão de execução aos scripts
chmod +x scripts/*.sh

# 4. Instalar (cria rede, valida .env, sobe a stack)
./scripts/install.sh

# 5. Conferir se subiu tudo certo
./scripts/health.sh
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
| `backup.sh` | Gera um snapshot em `backups/<timestamp>/` com dump de **todos os bancos** do Postgres (um arquivo por banco + papéis globais), dump do MongoDB e cópia completa dos volumes de MinIO e Dremio. Ver [`docs/backup.md`](docs/backup.md). |
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