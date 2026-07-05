# Git Drill - Controle de Versão para Engenharia de Dados

Prática recorrente de Git, com a mesma operação central em profundidade crescente por nível (não são temas diferentes - é a mesma habilidade em cenário cada vez mais realista e sob mais pressão).

## Estrutura

```
git_drill/
├── junior/challenges_junior.md   → fluxo básico, primeiro conflito simples, .gitignore
├── pleno/challenges_pleno.md     → conflito multi-arquivo, merge vs rebase, revert/reset, stash
└── senior/challenges_senior.md   → rebase interativo, bisect, conflito em lock file, estratégia de branching
```

## Como usar

Pratique num repositório de TESTE, não no `rafael-data-platform` real - crie um repo descartável só pra esses exercícios (`mkdir git-drill-sandbox && cd git-drill-sandbox && git init`), pra poder cometer erros e simular cenários destrutivos (force-push, reset --hard) sem risco algum ao projeto de verdade.