# Trilha de Estudos - Engenharia de Dados

Roadmap de aprendizado prático usando a infraestrutura deste projeto como campo de treino real, com foco em engenharia de dados: pipelines, orquestração e qualidade de dados.

---

## Camada 1 - Infraestrutura ✅

Docker Compose com todos os serviços base rodando de forma estável e reproduzível.

**O que foi aprendido na prática:** Docker networking, volumes externos vs. gerenciados, healthchecks, hardening de rede (bind em loopback + túnel SSH em vez de exposição direta - ver `docs/security.md`).

---

## Camada 2 - Conectividade ✅

- [x] Conectar Dremio → PostgreSQL (source JDBC) (ver `docs/dremio-connections`)
- [x] Conectar Dremio → MinIO (source S3-compatible) (ver `docs/dremio-connections`)
- [ ] **Exercício:** validar uma query federada real no Dremio, unindo uma tabela do Postgres com um arquivo do MinIO numa única consulta SQL. Serve pra confirmar que a camada de query engine está funcionando de ponta a ponta, não só "conectada".

---

## Camada 3 - Pipelines (foco atual)

Objetivo: sair de scripts manuais isolados para um pipeline com ingestão, transformação, qualidade e orquestração - o ciclo real de um pipeline de engenharia de dados.

### 3.1 Ingestão batch (Extract)
- [ ] Script Python/bash que pega um CSV ou JSON de exemplo e sobe pro MinIO (usando `boto3` ou `mc`, o client CLI do MinIO)
- [ ] **Exercício:** ingerir pelo menos 2 fontes diferentes (ex: um CSV de vendas fictício + um JSON de eventos) em buckets separados no MinIO, seguindo uma convenção de pastas por data (`bronze/vendas/2026-07-04/arquivo.csv`) - introduz o conceito de **data lake em camadas** (bronze/silver/gold)

### 3.2 Carga para staging (Load)
- [ ] Script que lê do MinIO (bronze) e carrega num schema de staging no Postgres
- [ ] **Exercício:** criar um schema `staging` (separado do `estudos` ou de produção) e carregar os dados brutos sem transformação - prática de separar "dados crus" de "dados tratados"

### 3.3 Qualidade de dados
- [ ] Checks básicos antes de promover dados de staging pra um schema "confiável": nulos inesperados, duplicatas, tipos incorretos, ranges de valores
- [ ] **Exercício:** escrever um script simples de validação (pode ser SQL puro com `SELECT COUNT(*) WHERE ...`, ou uma lib como Great Expectations/Pandera se quiser ir mais a fundo) que rejeita a carga se as regras falharem - introduz o conceito de **data quality gate**

### 3.4 Orquestração
- [ ] Adicionar um orquestrador como **serviço containerizado do próprio projeto** (não instalação solta na VPS) - candidatos: Airflow (mais usado no mercado, mais pesado) ou Dagster (mais moderno, mais leve para um lab pessoal)
- [ ] Novo serviço no `docker-compose.yml`, mesma rede `data-platform`, container próprio (`lab-airflow`/`lab-dagster`)
- [ ] **Exercício:** montar uma DAG/pipeline que executa a sequência completa (3.1 → 3.2 → 3.3) automaticamente, agendada (ex: diária), com log de execução e tratamento de falha (retry, alerta)

---

## Camada 4 - Analytics

- [ ] Modelagem dimensional no Postgres (schema `analytics`, fato + dimensões a partir dos dados tratados na Camada 3)
- [ ] Datasets curados no Dremio (reflections, pra acelerar consultas repetidas)
- [ ] Dashboards de consumo (Metabase/Superset - avaliar qual se encaixa melhor; também entraria como serviço containerizado do projeto, seguindo o mesmo padrão)

---

## Melhorias de infraestrutura (backlog)

- [x] Segurança de rede: bancos isolados via bind em loopback + túnel SSH (ver `docs/security.md`)
- [ ] Backup automatizado via cron
- [ ] Alertas básicos de saúde dos containers
- [ ] Fail2ban para SSH
- [ ] Reverse proxy com TLS para as UIs administrativas

---

## Princípio geral da trilha

Cada camada deve deixar algo **testável e demonstrável** antes de avançar pra próxima - não só "implementado", mas comprovado funcionando com dados reais passando por ele (do jeito que fizemos com backup/restore: só consideramos "pronto" depois de testar o ciclo completo, não só escrever o script).