# Trilha de Estudos - Engenharia de Dados

Roadmap de aprendizado prático usando a infraestrutura deste projeto como campo de treino real. Cada fase usa os serviços já existentes e se conecta à anterior - os dados criados num exercício alimentam o seguinte, simulando o ciclo de vida real de uma plataforma de dados.

**Serviços cobertos pela trilha:** PostgreSQL · MinIO · Dremio · MongoDB · Redis · Mongo Express · RedisInsight · Portainer - sem exceção. Serviços que ainda não existem na stack (orquestrador, dbt, BI, CDC) entram como **novos containers do próprio projeto** (mesma rede `data-platform`, container `lab-*`, nunca instalação solta na VPS).

---

## Onde o código vive

Cada exercício numerado aqui tem uma pasta correspondente em [`../projects/`](../projects/), com o mesmo número (ex: Exercício 3.4c → pasta `projects/3.4-data-quality/`). Cada pasta é autocontida - README próprio, dependências próprias, ambiente virtual próprio - como se pudesse virar um repositório separado a qualquer momento.

Veja [`projects/README.md`](../projects/README.md) para o índice de status de cada exercício e a convenção de estrutura interna de cada pasta (`_TEMPLATE/` tem o molde pronto pra copiar ao iniciar um exercício novo).

Ferramentas pesadas de pipeline/analytics (Airflow/Dagster, dbt, Metabase/Superset) não rodam na infra core - sobem via `docker-compose.pipelines.yml` só quando a camada correspondente estiver em estudo:

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.pipelines.yml up -d
```

---

## Camada 1 - Infraestrutura ✅

Docker Compose com todos os serviços base rodando de forma estável, segura e reproduzível.

---

## Camada 2 - Conectividade

- [x] Conectar Dremio → PostgreSQL (source JDBC)
- [x] Conectar Dremio → MinIO (source S3-compatible)
- [ ] **Exercício 2.1 - Query federada:** subir um CSV qualquer num bucket do MinIO, criar uma tabela pequena no Postgres, e escrever uma query no Dremio que faça JOIN entre os dois numa única consulta SQL. Prova que a camada de query engine funciona de ponta a ponta.
  - *Ferramentas: Dremio, MinIO, Postgres (pgAdmin ou psql para inspeção manual antes da query federada)*

---

## Camada 3 - Pipelines

Objetivo: construir um pipeline completo de ingestão → staging → qualidade → orquestração, usando um dataset fictício de e-commerce (vendas, produtos, clientes, eventos de navegação) que será reaproveitado em todas as camadas seguintes.

### 3.1 Ingestão batch - Extract (MinIO como data lake)
- [ ] **Exercício 3.1a:** gerar dados fictícios de e-commerce com Python (`faker`): um CSV de vendas e um CSV de clientes. Subir pro MinIO com `boto3` seguindo a convenção de camadas: `bronze/vendas/YYYY-MM-DD/arquivo.csv`
- [ ] **Exercício 3.1b:** gerar um JSON de eventos de navegação (cliques, page views) e subir pra `bronze/eventos/YYYY-MM-DD/`. Introduz ingestão de dados semiestruturados
- [ ] **Exercício 3.1c:** explorar os arquivos bronze **direto no Dremio** (a fonte `minio-lake` já enxerga os buckets) - consultar CSV/JSON sem carregar em banco nenhum. Conceito: *schema-on-read*
  - *Ferramentas: MinIO, Python, Dremio*
  - *Conexão: os dados gerados aqui alimentam todos os exercícios seguintes*

### 3.2 NoSQL como fonte operacional
- [ ] **Exercício 3.2a:** modelar um catálogo de produtos como documentos no MongoDB (produto com atributos variáveis por categoria - exatamente o caso de uso que justifica NoSQL vs relacional). Popular via script Python (`pymongo`)
- [ ] **Exercício 3.2b:** usar o **Mongo Express** pra inspecionar as collections visualmente, criar índices e comparar performance de queries com/sem índice (`explain()`)
- [ ] **Exercício 3.2c:** escrever um script de **extração Mongo → MinIO**: exportar o catálogo pra `bronze/produtos/YYYY-MM-DD/produtos.json`. O MongoDB vira uma *fonte* do pipeline, como sistemas operacionais reais são
  - *Ferramentas: MongoDB, Mongo Express, MinIO, Python*
  - *Conexão: o catálogo extraído aqui é o que dá dimensão de produto às vendas do 3.1*

### 3.3 Carga para staging - Load (Postgres)
- [ ] **Exercício 3.3a:** criar um schema `staging` no Postgres e carregar os dados bronze do MinIO (vendas, clientes, produtos) sem transformação, via Python (`psycopg2`/`sqlalchemy`)
- [ ] **Exercício 3.3b:** implementar carga **idempotente**: rodar o mesmo script duas vezes não pode duplicar dados (estratégias: truncate-and-load ou upsert por chave). Conceito fundamental de pipelines confiáveis
  - *Ferramentas: Postgres, MinIO, Python*
  - *Conexão: usa os dados de 3.1 e 3.2c*

### 3.4 Qualidade de dados - Data Quality Gate
- [ ] **Exercício 3.4a:** escrever validações SQL sobre o staging: nulos em campos obrigatórios, duplicatas de chave, valores fora de range (ex: venda com valor negativo), integridade referencial (venda apontando pra produto inexistente)
- [ ] **Exercício 3.4b:** evoluir para uma lib de qualidade (Great Expectations ou Pandera) e fazer a carga **falhar** se as regras não passarem - o dado ruim não avança
- [ ] **Exercício 3.4c (usando Redis):** gravar o resultado de cada execução de qualidade no **Redis** (chave `dq:last_run:<tabela>` com status, timestamp e contagem de erros). O pipeline seguinte consulta o Redis antes de rodar: se a qualidade falhou, não processa. Introduz Redis como *camada de estado/coordenação entre pipelines*
- [ ] **Exercício 3.4d:** acompanhar essas chaves em tempo real pelo **RedisInsight** enquanto o pipeline roda
  - *Ferramentas: Postgres, Redis, RedisInsight, Python*
  - *Conexão: valida os dados carregados em 3.3; o estado no Redis é pré-requisito do 3.5*

### 3.5 Orquestração
- [ ] **Decisão de ferramenta:** adicionar um orquestrador como serviço do projeto - opções: **Airflow** (padrão de mercado, mais pesado) ou **Dagster** (mais moderno, mais leve pra VPS de 12GB). Novo container `lab-airflow`/`lab-dagster` no compose, rede `data-platform`
- [ ] **Exercício 3.5a:** montar a DAG/pipeline completa: gerar dados (3.1) → extrair Mongo (3.2c) → carregar staging (3.3) → validar qualidade (3.4) → só avança se o gate passar
- [ ] **Exercício 3.5b:** agendar execução diária, configurar retry com backoff e alerta em caso de falha
- [ ] **Exercício 3.5c:** usar o **Portainer** pra acompanhar o consumo de recursos (CPU/RAM) dos containers durante a execução da DAG - a VPS tem 12GB, e o orquestrador + Dremio juntos são pesados; aprender a dimensionar é parte do estudo
  - *Ferramentas: Airflow/Dagster (novo), Portainer, todos os anteriores*
  - *Conexão: automatiza tudo que foi construído manualmente de 3.1 a 3.4*

### 3.6 Cache de aplicação (Redis, segundo caso de uso)
- [ ] **Exercício 3.6:** criar uma API mínima (FastAPI, container `lab-api`) que consulta o catálogo de produtos, com cache no Redis (TTL de 5 min) - medir a diferença de latência com/sem cache usando o RedisInsight pra observar hits/misses. Introduz o caso de uso clássico de Redis, diferente do 3.4c
  - *Ferramentas: Redis, RedisInsight, MongoDB, Python*

---

## Camada 4 - Transformação e Analytics

### 4.1 Transformação com dbt
- [ ] **Decisão de ferramenta:** adicionar **dbt** ao projeto (dbt-core rodando em container `lab-dbt`, ou como step do orquestrador - avaliar as duas abordagens)
- [ ] **Exercício 4.1a:** modelar as camadas `staging` → `intermediate` → `marts` no Postgres com dbt: models, sources, refs
- [ ] **Exercício 4.1b:** implementar testes do dbt (`unique`, `not_null`, `relationships`) - comparar com o que foi feito manualmente em 3.4 e entender o que cada abordagem cobre
- [ ] **Exercício 4.1c:** gerar a documentação automática do dbt (`dbt docs`) e explorar o lineage graph
  - *Ferramentas: dbt (novo), Postgres*
  - *Conexão: transforma o staging de 3.3 nos marts que alimentam 4.2*

### 4.2 Modelagem dimensional (DW no Postgres)
- [ ] **Exercício 4.2a:** desenhar e implementar via dbt um star schema no schema `analytics`: `fct_vendas` + `dim_produto`, `dim_cliente`, `dim_data`
- [ ] **Exercício 4.2b:** implementar uma dimensão **SCD Type 2** (histórico de mudanças de preço do produto) - um dos conceitos mais cobrados em entrevistas de engenharia de dados
  - *Ferramentas: dbt, Postgres*
  - *Conexão: usa os marts de 4.1; é a fonte das análises de 4.3 e dashboards de 4.4*

### 4.3 Query engine avançado (Dremio a fundo)
- [ ] **Exercício 4.3a:** criar Virtual Datasets no Dremio combinando o star schema do Postgres com dados bronze do MinIO
- [ ] **Exercício 4.3b:** configurar **Reflections** (aceleração de queries do Dremio) num dataset pesado e medir o antes/depois no tempo de resposta
- [ ] **Exercício 4.3c:** escrever a mesma análise (ex: receita por categoria por mês) de três formas - SQL direto no Postgres, query federada no Dremio sem reflection, e com reflection - e comparar os planos de execução
  - *Ferramentas: Dremio, Postgres, MinIO*
  - *Conexão: consome o DW de 4.2 e o lake de 3.1*

### 4.4 Visualização
- [ ] **Decisão de ferramenta:** adicionar BI como serviço do projeto - opções: **Metabase** (mais simples, ideal pra começar) ou **Superset** (mais completo, mais pesado). Container `lab-metabase`/`lab-superset`
- [ ] **Exercício 4.4a:** conectar o BI ao Postgres (schema `analytics`) e montar um dashboard de vendas: receita ao longo do tempo, top produtos, funil por categoria
- [ ] **Exercício 4.4b:** conectar o BI ao Dremio (via JDBC, porta 31010) e comparar a experiência vs conexão direta ao Postgres
  - *Ferramentas: Metabase/Superset (novo), Postgres, Dremio*
  - *Conexão: consome exclusivamente o que foi modelado em 4.2/4.3 - se o dashboard ficou fácil de montar, a modelagem foi bem feita*

---

## Camada 5 - Tópicos avançados

- [ ] **5.1 Streaming/CDC:** capturar mudanças do MongoDB (change streams) ou Postgres (logical replication/Debezium) e refletir no lake em near-real-time - exige avaliar Kafka/Redpanda como novo serviço (pesado; verificar RAM disponível antes)
- [ ] **5.2 Data Lakehouse:** converter a camada bronze de CSV/JSON para **Parquet** e depois para um formato de tabela aberta (Apache Iceberg - o Dremio tem suporte nativo), comparando tamanho de storage e velocidade de query
- [ ] **5.3 Observabilidade do pipeline:** métricas de execução (duração, volume, falhas) gravadas no Postgres e expostas num dashboard do BI - "monitorar o pipeline com o próprio pipeline"

---

## Camada 6 - Engenharia de Software aplicada a Dados

A partir daqui o foco muda: não é mais "fazer o pipeline funcionar", é tratá-lo como software profissional - versionado, testado, implantável e recuperável.

### 6.1 CI/CD do projeto (GitHub Actions)
- [ ] **Exercício 6.1a - CI de validação:** workflow que roda a cada push: lint dos scripts shell (`shellcheck`), validação do compose (`docker compose config`), lint do Python dos pipelines (`ruff`)
- [ ] **Exercício 6.1b - CI do dbt:** rodar `dbt build` (models + testes) contra um Postgres efêmero (service container do próprio Actions) a cada PR - nenhuma mudança de modelagem entra sem os testes passarem
- [ ] **Exercício 6.1c - CD para a VPS:** deploy automatizado via SSH no merge pra `main`: `git pull` + `docker compose up -d` na VPS. Introduz deploy key, secrets do GitHub e a diferença entre CI (validar) e CD (entregar)
  - *Ferramentas: GitHub Actions (novo, fora da VPS), todos os serviços*
  - *Conexão: automatiza a entrega de tudo construído nas camadas 3 e 4 - a DAG do 3.5 e os models do 4.1 passam a chegar na VPS sem SSH manual*

### 6.2 Secrets Management
- [ ] **Exercício 6.2:** substituir senhas fracas do `.env` por senhas geradas (`openssl rand`), e avaliar `sops`+`age` para versionar secrets criptografados no repo (alternativa leve a um Vault, adequada ao single-node)
  - *Conexão: pré-requisito do 6.1c - o CD não pode depender de um `.env` que só existe na sua máquina*

### 6.3 Disaster Recovery
- [ ] **Exercício 6.3:** simular perda total da VPS: a partir **apenas** do repo Git + último backup em local externo, reconstruir a plataforma inteira (clone → install → restore) e cronometrar. O tempo medido é seu RTO real - documentar o resultado
  - *Conexão: teste final de tudo - README (setup), backup.sh/restore.sh (dados) e docs. Se algo faltar, a documentação tinha buraco*
  - *Pré-requisito honesto: hoje os backups ficam na própria VPS; este exercício exige antes resolver o item "backup externo" do backlog*

### 6.4 Tradução para cloud (AWS como exercício, não migração)
> O lab permanece na VPS por decisão de projeto. Esta seção é sobre **falar a língua da cloud**, não sobre migrar.

- [ ] **Exercício 6.4a - Mapa de equivalência:** documentar em `docs/cloud-mapping.md` o equivalente AWS de cada peça: MinIO→S3, Postgres→RDS, Dremio→Athena/Redshift Spectrum, MongoDB→DocumentDB, Redis→ElastiCache, Airflow→MWAA, dbt→dbt Cloud/ECS, Metabase→QuickSight - com prós/contras e ordem de grandeza de custo mensal vs o da VPS
- [ ] **Exercício 6.4b - Interoperabilidade real:** criar um bucket S3 no free tier da AWS e adaptar o script de ingestão do 3.1 pra escrever nele **sem mudar o código** - só trocando endpoint e credenciais (a API do MinIO é S3-compatible; provar isso na prática é o ponto do exercício)
  - *Conexão: reusa o pipeline do 3.1; o mapa do 6.4a vira seu material de estudo pra entrevistas*

---

## Melhorias de infraestrutura (backlog)

- [x] Segurança de rede: bancos isolados via bind em loopback + túnel SSH (ver `docs/security.md`)
- [ ] Backup externo à VPS (rclone → S3/B2/Google Drive) - pré-requisito do exercício 6.3
- [ ] Backup automatizado via cron
- [ ] Alertas básicos de saúde dos containers
- [ ] Fail2ban para SSH
- [ ] Reverse proxy com TLS para as UIs administrativas

---

## Mapa de cobertura ferramenta × exercícios

| Serviço | Exercícios que o utilizam |
|---|---|
| PostgreSQL | 2.1, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.3 |
| pgAdmin | 2.1, 3.3, 4.2 |
| MinIO | 2.1, 3.1, 3.2c, 3.3, 4.3, 5.2 |
| Dremio | 2.1, 3.1c, 4.3, 4.4b, 5.2 |
| MongoDB | 3.2, 3.6, 5.1 |
| Mongo Express | 3.2b |
| Redis | 3.4c, 3.6 |
| RedisInsight | 3.4d, 3.6 |
| Portainer | 3.5c |
| Airflow/Dagster *(a adicionar)* | 3.5 |
| dbt *(a adicionar)* | 4.1, 4.2 |
| Metabase/Superset *(a adicionar)* | 4.4, 5.3 |
| GitHub Actions *(a adicionar)* | 6.1 |
| sops/age *(a adicionar)* | 6.2 |
| AWS S3 *(exercício externo)* | 6.4b |
| SQL (via sql-drill) | prática paralela, não numerada |
| pandas (via pandas_drill) | prática paralela, não numerada |
| Python (algoritmos, via python_drill) | prática paralela, não numerada |
| Cenários de pipeline (via data_engineering_interview_drill) | prática paralela, não numerada |
| Arquitetura/System Design (via data_system_design_drill) | prática paralela, não numerada |
| Simulação completa (via mock_technical_interviews) | prática paralela, não numerada |

---

## Prática paralela: SQL Drills

Fora da sequência de camadas, [`drills/sql-drill/`](../drills/sql-drill/) contém exercícios diários de SQL para manter fluência de sintaxe - independentes entre si, cada um isolado em seu próprio schema no Postgres.

---

## Prática paralela: Pandas Drills

Também fora da sequência de camadas, [`drills/pandas_drill/`](../drills/pandas_drill/) contém exercícios de análise de dados com pandas, conectando direto no Postgres da VPS via túnel SSH. Os drills consomem os mesmos schemas populados pelos SQL Drills - por exemplo, `drill_pandas_02.py` usa os dados de `drill_sql_02`, permitindo praticar a mesma pergunta analítica primeiro em SQL puro, depois em pandas.

---

## Prática paralela: Python Drills

Também fora da sequência de camadas, [`drills/python_drill/`](../drills/python_drill/) contém desafios de algoritmos e estruturas de dados no formato clássico de entrevista técnica, organizados em três níveis (Junior/Pleno/Sênior). Sem pandas, sem banco de dados - foco em lógica, complexidade e implementação de estruturas na mão (pilha, fila, árvore, grafo, hash map).

---

## Prática paralela: Data Engineering Interview Drill

[`drills/data_engineering_interview_drill/`](../drills/data_engineering_interview_drill/) contém cenários práticos de entrevista de Engenharia de Dados - dedup, CDC, watermark, late arriving data, schema evolution, checkpoint/resume - sempre com contexto real de pipeline, sem perguntas teóricas isoladas.

---

## Prática paralela: Data System Design Drill

[`drills/data_system_design_drill/`](../drills/data_system_design_drill/) contém estudos de caso de arquitetura de dados, sem código - cada case tem resposta modelo didática completa (fase de estudo), cobrindo batch vs streaming, idempotência, particionamento, CDC, shuffle/broadcast join, Delta/Iceberg, e arquitetura em escala.

---

## Prática paralela: Mock Technical Interviews

[`drills/mock_technical_interviews/`](../drills/mock_technical_interviews/) simula entrevistas completas cronometradas, misturando SQL, Python, Pandas, modelagem, dbt e arquitetura numa única sessão - remixa exercícios dos outros módulos pra treinar troca de contexto sob pressão de tempo.

---

## Princípio geral da trilha

Cada exercício deve deixar algo **testável e demonstrável** antes de avançar - não só "implementado", mas comprovado funcionando com dados reais passando por ele. E cada nova ferramenta entra sempre como serviço containerizado do próprio projeto, documentada em `docs/services.md` e coberta pelo `backup.sh` quando tiver estado persistente.