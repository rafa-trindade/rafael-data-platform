# Python Drill - Algoritmos para Entrevista

Exercícios de algoritmos e estruturas de dados focados no formato de entrevista técnica, organizados por nível. Diferente do `pandas_drill`, aqui não há conexão com banco de dados nem uso de pandas - o foco é lógica pura, complexidade e estruturas de dados na mão.

## Estrutura

```
python_drill/
├── junior/challenges_junior.py    → fundamentos de lógica, string, lista
├── pleno/challenges_pleno.py      → pilha, fila, busca/ordenação, linked list, recursão
└── senior/challenges_senior.py    → árvores, grafos, programação dinâmica, hash map, design leve
```

## Como usar

Cada exercício vem em duas células (`#%%`): o enunciado + stub da função, e depois um bloco de `assert` para você validar sua própria implementação. Implemente a função, rode a célula de asserts - se não der erro, está correto.

Abra qualquer arquivo no VS Code com a extensão Jupyter/Python ativa e use "Run Cell" célula por célula (não precisa de venv específico, é só Python padrão - nenhuma dependência externa).

## Cobertura por nível

| Nível | Temas |
|---|---|
| Junior | palíndromo, número primo, fibonacci, fatorial, manipulação de string/lista, two sum |
| Pleno | pilha/fila do zero, busca binária, bubble/insertion sort, linked list, anagrama, permutações, recursão (Hanói) |
| Sênior | Big-O, árvore binária (BST, BFS, balanceamento), programação dinâmica (LCS, knapsack, coin change), hash map do zero, LRU cache, grafos (ciclo, caminho mais curto), rate limiter |