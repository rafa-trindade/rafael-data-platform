# Pandas Drill - Prática de Análise de Dados

Exercícios de pandas conectando direto no Postgres da VPS (via túnel SSH), usando os dados já populados pelos SQL drills.

## Pré-requisito: túnel SSH ativo

```bash
ssh -L 5434:localhost:5434 rafael@_ip_
```

Deixe esse terminal aberto enquanto rodar os drills.

## Setup

```bash
cd drills/pandas_drill
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name=pandas_drill --display-name="Python (pandas_drill)"
CTRL+SHIFT+P > Developer: Reload Window
cp .env.example .env
# edite .env com as credenciais (mesmas do docker/.env do projeto principal)
```

## Drills

| Arquivo | Fonte de dados | Tema |
|---|---|---|
| `scripts/challenges_drill_01.py` | `drill_sql_01` (schema no banco `estudos`) | E-commerce - joins, group by, window functions, cohort/Pareto/RFM |
| `scripts/challenges_drill_02.py` | `drill_sql_02` (schema no banco `estudos`) | Vendas de mercado - fundamentos, window functions, datas/nulos/pivot |

## Nota sobre as credenciais

Este projeto **não** lê `docker/.env` diretamente - tem seu próprio `.env`, com host/porta específicos de acesso externo via túnel (`localhost:5434`), diferente da rede interna dos containers. Usuário e senha são os mesmos do `docker/.env`, copiados manualmente.