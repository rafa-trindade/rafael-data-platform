# Serviços

| Serviço       | Container         | Porta(s)                       | Credenciais (via .env)                 | Acesso |
|---------------|--------------------|--------------------------------|------------------------------------------|--------|
| PostgreSQL    | lab-postgres       | 5434 → 5432 (só em `127.0.0.1`) | POSTGRES_USER / POSTGRES_PASSWORD       | via túnel SSH - ver [`docs/security.md`](security.md) |
| MongoDB       | lab-mongodb        | 27017 (só em `127.0.0.1`)       | MONGO_USER / MONGO_PASSWORD             | via túnel SSH - ver [`docs/security.md`](security.md) |
| Redis         | lab-redis          | 6379 (só em `127.0.0.1`)        | REDIS_PASSWORD                          | via túnel SSH - ver [`docs/security.md`](security.md) |
| MinIO         | lab-minio          | 9000 (API), 9001 (console)     | MINIO_ROOT_USER / MINIO_ROOT_PASSWORD   | http://SEU_IP:9001 |
| Mongo Express | lab-mongo-express  | 8081                            | mesmo user/senha do Mongo (Basic Auth)  | http://SEU_IP:8081 |
| RedisInsight  | lab-redisinsight   | 5540                            | -                                        | http://SEU_IP:5540 |
| Dremio        | lab-dremio         | 9047 (UI), 31010 (JDBC), 45678 | criado no primeiro acesso                | http://SEU_IP:9047 |
| Portainer     | lab-portainer      | 8000, 9443                     | criado no primeiro acesso                | https://SEU_IP:9443 |

> Todas as senhas ficam em `docker/.env`, nunca commitado (ver `.gitignore`).

## Segurança de rede

Postgres, MongoDB e Redis não são expostos publicamente - veja [`docs/security.md`](security.md) para o racional completo e como acessá-los via túnel SSH.

As UIs administrativas (MinIO console, Dremio, Mongo Express, RedisInsight, Portainer) continuam expostas publicamente por conveniência de acesso via navegador. Melhorias futuras estão listadas no backlog de [`docs/projects.md`](projects.md) (reverse proxy com TLS, Fail2ban).