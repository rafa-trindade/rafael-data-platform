# Serviços

| Serviço       | Container         | Porta(s)                  | Credenciais (via .env)        | UI/Acesso |
|---------------|--------------------|-----------------------------|--------------------------------|-----------|
| PostgreSQL    | lab-postgres       | 5434 → 5432                | POSTGRES_USER / POSTGRES_PASSWORD | psql / DBeaver |
| MinIO         | lab-minio          | 9000 (API), 9001 (console) | MINIO_ROOT_USER / MINIO_ROOT_PASSWORD | http://SEU_IP:9001 |
| MongoDB       | lab-mongodb        | 27017                       | MONGO_USER / MONGO_PASSWORD    | mongosh |
| Mongo Express | lab-mongo-express  | 8081                         | mesmo user/senha do Mongo (Basic Auth) | http://SEU_IP:8081 |
| Redis         | lab-redis          | 6379                         | REDIS_PASSWORD                 | redis-cli -a |
| RedisInsight  | lab-redisinsight   | 5540                         | -                               | http://SEU_IP:5540 |
| Dremio        | lab-dremio         | 9047 (UI), 31010 (JDBC), 45678 | criado no primeiro acesso     | http://SEU_IP:9047 |
| Portainer     | lab-portainer      | 8000, 9443                  | criado no primeiro acesso       | https://SEU_IP:9443 |

> Todas as senhas ficam em `docker/.env`, nunca commitado (ver `.gitignore`).

## Recomendação de segurança

A VPS expõe essas portas publicamente por padrão (`0.0.0.0`). Para produção/uso sério, recomenda-se:
- Restringir por firewall (UFW) as portas administrativas (9443, 9047, 8081, 5540) ao seu IP
- Ou colocar atrás de um reverse proxy com autenticação (Traefik/Nginx + Basic Auth)

Isso é uma melhoria futura, não bloqueante para o lab.