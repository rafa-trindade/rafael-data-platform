# Arquitetura - Rafael Data Platform

Lab de engenharia de dados single-node em VPS, orquestrado via Docker Compose.

## Camadas

1. **Infraestrutura** - containers base (Postgres, MinIO, MongoDB, Redis, Dremio, Portainer)
2. **Conectividade** - Dremio como camada de consulta sobre Postgres e MinIO; MongoDB isolado
3. **Pipelines** - scripts de ingestão/ETL (a implementar)
4. **Analytics** - datasets modelados no Postgres, consultados via Dremio, com dados brutos no MinIO (data lake)

## Rede

Todos os serviços compartilham a rede externa `data-platform`, criada uma única vez fora do compose (`docker network create data-platform`), permitindo que outros stacks futuros se conectem à mesma rede sem redeploy.

## Persistência

Todos os volumes (`docker_postgres_data`, `minio_data`, `mongodb_data`, `redis_data`, `redisinsight_data`, `dremio_data`, `portainer_data`) são gerenciados pelo compose, criados automaticamente no primeiro `docker compose up -d`.

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