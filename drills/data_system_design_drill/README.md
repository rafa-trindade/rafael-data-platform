README# Data System Design Drill

Estudos de caso de arquitetura de dados - sem implementação em código, foco em raciocínio arquitetural. Cada case tem contexto, perguntas, **resposta modelo didática completa** (fase de estudo) e follow-ups que um entrevistador faria.

## Estrutura

```
data_system_design_drill/
├── junior/cases_junior.md   → batch vs streaming, idempotência, particionamento
├── pleno/cases_pleno.md     → ingestão incremental, retry/monitoramento, isolamento bronze/silver/gold
└── senior/cases_senior.md   → escala (500M eventos/dia), shuffle/broadcast join, Delta/Iceberg, múltiplos consumidores
```

## Como usar

Leia o contexto e as perguntas, **tente responder por escrito antes de ler a resposta modelo**. Depois compare com a resposta modelo e os follow-ups - o objetivo nessa fase é internalizar o padrão de raciocínio esperado, não só saber "a resposta certa" de memória.