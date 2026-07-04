# Conectando o Dremio às fontes de dados

Guia de configuração das fontes do Dremio via UI (`http://SEU_IP:9047`). Essas conexões não ficam em arquivo de config - são feitas manualmente na interface, então este doc serve como referência/checklist sempre que precisar recriar ou revisar.

## Pré-requisito

Ter a conta admin do Dremio já criada (primeiro acesso à UI pede isso automaticamente).

---

## 1. PostgreSQL → `postgres-dw`

**Sources → `+` → PostgreSQL**

| Campo | Valor |
|---|---|
| Name | `postgres-dw` |
| Host | `lab-postgres` (nome do container - Dremio e Postgres estão na mesma rede `data-platform`) |
| Port | `5432` (porta **interna** do container, não a `5434` mapeada externamente) |
| Database Name | valor de `POSTGRES_DB` em `docker/.env` |
| Username | valor de `POSTGRES_USER` em `docker/.env` |
| Password | valor de `POSTGRES_PASSWORD` em `docker/.env` |
| Encrypt connection | desmarcado |

Salvar → o database deve aparecer na árvore de Sources, navegável até as tabelas.

---

## 2. MinIO → `minio-lake`

**Sources → `+` → Amazon S3**

| Campo | Valor |
|---|---|
| Name | `minio-lake` |
| AWS Access Key | valor de `MINIO_ROOT_USER` em `docker/.env` |
| AWS Access Secret | valor de `MINIO_ROOT_PASSWORD` em `docker/.env` |
| Encrypt connection | desmarcado |

Em **Advanced Options**:

| Campo | Valor |
|---|---|
| Enable compatibility mode | ✅ marcado |
| `fs.s3a.endpoint` | `lab-minio:9000` |
| `fs.s3a.path.style.access` | `true` |

Salvar → os buckets do MinIO aparecem na árvore (se estiver vazio, é porque ainda não existe bucket criado no console `http://SEU_IP:9001`).

---

## Troubleshooting

| Sintoma | Causa provável |
|---|---|
| Connection refused | Usou `localhost` em vez do hostname do container (`lab-postgres`/`lab-minio`) |
| Falha de autenticação no MinIO | Valores do `.env` copiados com espaço/erro de digitação |
| Não aparece campo de endpoint customizado no S3 | Esqueceu de abrir "Advanced Options" antes de salvar |
| Bucket não aparece | Nenhum bucket criado ainda no MinIO console |
