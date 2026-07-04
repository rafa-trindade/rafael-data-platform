# Projetos - Trilha de Estudos

Cada pasta aqui corresponde a um exercício numerado em [`../docs/projects.md`](../docs/projects.md). O número da pasta bate exatamente com o número do exercício - se você está lendo "Exercício 3.4c" no roadmap, o código está em `3.4-data-quality/`.

Cada projeto é autocontido: tem seu próprio `README.md`, `requirements.txt` e `.venv`, como se pudesse ser extraído e virar um repositório próprio a qualquer momento.

## Status geral

| Pasta | Camada | Status |
|---|---|---|
| `3.1-ingestao-ecommerce` | 3 - Pipelines | ⬜ não iniciado |
| `3.2-mongo-catalogo` | 3 - Pipelines | ⬜ não iniciado |
| `3.3-staging-load` | 3 - Pipelines | ⬜ não iniciado |
| `3.4-data-quality` | 3 - Pipelines | ⬜ não iniciado |
| `3.5-orquestracao` | 3 - Pipelines | ⬜ não iniciado |
| `3.6-cache-api` | 3 - Pipelines | ⬜ não iniciado |
| `4.1-4.2-dbt-analytics` | 4 - Analytics | ⬜ não iniciado |
| `4.3-dremio-avancado` | 4 - Analytics | ⬜ não iniciado |
| `4.4-bi-dashboards` | 4 - Analytics | ⬜ não iniciado |
| `5.x-topicos-avancados` | 5 - Avançado | ⬜ não iniciado |
| `6.x-cicd-secrets-dr-cloud` | 6 - Eng. de Software | ⬜ não iniciado |

Atualize a coluna Status conforme for avançando: ⬜ não iniciado · 🟨 em andamento · ✅ concluído.

## Serviços de pipeline (Airflow/Dagster, dbt, Metabase/Superset)

Esses não fazem parte da infra core - sobem via compose separado, só quando for estudar as camadas que os usam:

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.pipelines.yml up -d
```

Para voltar só à infra core:

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.pipelines.yml down
docker compose -f docker/docker-compose.yml up -d
```

## Convenção de cada projeto

```
<numero>-<nome>/
├── README.md          → objetivo, como rodar, o que consome/produz
├── requirements.txt   → dependências isoladas
├── .venv/             → ambiente virtual próprio (gitignored)
├── src/                → código
└── data/               → arquivos de exemplo pequenos (gitignored se grande)
```

Ao começar um exercício novo, copie `_TEMPLATE/README.md` como ponto de partida.

## Prática paralela (fora da numeração)

Essas pastas não correspondem a um exercício numerado da trilha - são prática recorrente, cada uma com sua própria estrutura interna documentada no README local:

| Pasta | O que é |
|---|---|
| [`sql-drill/`](sql-drill/) | Exercícios diários de SQL, cada drill isolado em seu próprio schema no Postgres |
| [`pandas_drill/`](pandas_drill/) | Exercícios de análise de dados com pandas, consumindo os schemas dos SQL Drills |
| [`python_drill/`](python_drill/) | Desafios de algoritmos e estruturas de dados no formato de entrevista técnica |

As pastas acima têm estrutura própria, documentada em cada README local - não seguem o molde numerado descrito na seção "Convenção de cada projeto" acima.