# Linux Drill — Terminal para Engenharia de Dados

Prática recorrente de linha de comando, focada em cenários reais de operação de pipelines e infraestrutura de dados — não é curso genérico de Linux, é o subconjunto que você realmente usa no dia a dia (e que aparece em entrevista prática: "abre um terminal e me mostra").

## Estrutura

```
linux_drill/
├── junior/challenges_junior.md   → navegação, permissões, grep/find/wc, pipes, redirecionamento
├── pleno/challenges_pleno.md     → awk/sed, sort+uniq, cron, variáveis de ambiente, gestão de processos
└── senior/challenges_senior.md   → logs gigantes, xargs+paralelismo, diagnóstico de disco/memória/CPU, scripts robustos
```

## Como usar

Cada exercício tem: **Cenário** (a situação real), **Tarefa** (o que fazer) e **Verificação** (como confirmar que funcionou — geralmente um comando que mostra o resultado esperado). Rode direto na sua VPS (`rafael-data-platform`) sempre que possível — você já tem containers, logs e arquivos reais pra praticar em cima, em vez de dados fake.

**Loop**: termine os três níveis, comece de novo do zero sem consultar nada. O objetivo é o comando saltar da memória, não "saber que existe".