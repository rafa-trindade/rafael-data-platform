# Arquitetura - Rafael Data Platform

Lab de engenharia de dados single-node em VPS, orquestrado via Docker Compose.

## Camadas

1. **Infraestrutura** - containers base (Postgres, MinIO, MongoDB, Redis, Dremio, Portainer)
2. **Conectividade** - Dremio como camada de consulta sobre Postgres e MinIO; MongoDB isolado
3. **Pipelines** - scripts de ingestão/ETL (a implementar)
4. **Analytics** - datasets modelados no Postgres, consultados via Dremio, com dados brutos no MinIO (data lake)

## Rede

Todos os serviços compartilham a rede externa `data-platform`, criada uma única vez fora do compose (`docker network create data-platform`), permitindo que outros stacks futuros se conectem à mesma rede sem redeploy.

## Compose modular

A infra core (`docker-compose.yml`) roda sempre e cobre os 9 serviços base. Ferramentas de pipeline/analytics mais pesadas (Airflow/Dagster, dbt runner, Metabase/Superset) ficam em `docker-compose.pipelines.yml`, um compose adicional que só sobe quando necessário:

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.pipelines.yml up -d
```

Isso evita que a VPS (12GB de RAM) rode permanentemente serviços pesados que só são usados durante exercícios específicos das Camadas 3.5, 4.1 e 4.4.

## Persistência

Todos os volumes principais (`docker_postgres_data`, `minio_data`, `mongodb_data`, `redis_data`, `redisinsight_data`, `dremio_data`, `portainer_data`, `pgadmin_data`) são **externos** (`external: true` + `name:` fixo no compose), criados automaticamente pelo `scripts/install.sh` caso não existam, e nunca gerenciados pelo ciclo de vida do compose. Isso garante:

- Nome fixo, independente de qual pasta o `docker compose` é executado
- Proteção contra perda acidental de dados via `docker compose down -v`
- Sobrevivem a reinstalações completas do projeto (clone + install), desde que os volumes não sejam removidos manualmente

O MongoDB também usa um volume anônimo (nome gerado automaticamente pelo Docker) para o diretório `/data/configdb`, interno da imagem oficial - não precisa de nome fixo, é gerenciado automaticamente.

## Diagrama lógico

```
                 ┌────────────┐
                 │  Dremio    │  (query engine)
                 └─────┬──────┘
           ┌───────────┴───────────┐
     ┌─────▼─────┐           ┌─────▼─────┐
     │ PostgreSQL │          │   MinIO   │
     │    (DW)    │          │(data lake)│
     └────────────┘          └───────────┘

     ┌────────────┐   ┌───────────┐
     │  MongoDB   │   │   Redis   │   (isolados, uso auxiliar)
     └────────────┘   └───────────┘

     ┌────────────┐
     │ Portainer  │   (observabilidade de containers)
     └────────────┘
```