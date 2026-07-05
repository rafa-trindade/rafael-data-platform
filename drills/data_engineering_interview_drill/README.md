# Data Engineering Interview Drill

Exercícios práticos que simulam problemas reais de entrevista de Engenharia de Dados - sem perguntas teóricas isoladas, sempre com um cenário concreto por trás (idempotência, CDC, watermark, dedup, schema evolution, etc).

## Estrutura

```
data_engineering_interview_drill/
├── junior/challenges_junior.py    → dedup, chunking, particionamento, validação de schema, retry, upsert
├── pleno/challenges_pleno.py      → CDC, merge incremental, watermark, late data, hash join, merge de duplicatas
└── senior/challenges_senior.py    → schema evolution, formatos de arquivo, checkpoint/resume, data quality gate, mini-ETL
```

## Como usar

Mesmo padrão dos outros drills: cada exercício tem contexto real + stub de função, uma célula de teste manual (`print`) e uma célula de `assert` para validação. Sem dependências externas - Python puro.