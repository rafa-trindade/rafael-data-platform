# Mock Interview - Senior - Sessão 01 (75-90 min)

## Contexto
Vaga de Engenheiro de Dados Sênior. Entrevista mais pesada em
arquitetura e trade-offs - espera-se que você justifique decisões,
não só produza a resposta "certa".

## Cronograma

| Parte | Tempo | Tema |
|---|---|---|
| 1 | 15 min | SQL avançado |
| 2 | 20 min | Python (algoritmo + cenário DE) |
| 3 | 10 min | Modelagem/dbt |
| 4 | 30-45 min | Arquitetura (case grande + discussão) |

---

## Parte 1 - SQL avançado (15 min)

Use `drill_sql_01`.

**1.1** Usando CTEs, encontre o produto mais vendido (em quantidade)
em cada categoria.

**1.2** Calcule a taxa de retenção mensal: quantos clientes que
compraram no mês M também compraram no mês M+1?

---

## Parte 2 - Python (20 min)

**2.1** Algoritmo: implemente Top-K usando heap (dado uma lista de
registros com campo `valor`, retorne os K com maior valor sem
ordenar a lista inteira).

**2.2** Cenário DE: seu pipeline processa 1000 arquivos em sequência
e falha no arquivo 601. Implemente uma função de checkpoint que
permite retomar exatamente de onde parou, sem reprocessar os 600
primeiros.

---

## Parte 3 - Modelagem/dbt (10 min)

**3.1** Como você organizaria um projeto dbt com as camadas
staging → intermediate → marts para o schema de `drill_sql_01`?
Descreva a estrutura de pastas e o que cada camada faz.

**3.2** Como você garantiria que o lineage (lineage graph) do dbt
está correto e é útil pro time entender de onde vem cada coluna de
`fct_vendas`?

---

## Parte 4 - Arquitetura (30-45 min)

Case principal (ver `data_system_design_drill/senior/cases_senior.md`,
Case 1, pra resposta modelo completa depois - responda antes de
consultar):

**"Projete a arquitetura de um pipeline para processar 500 milhões
de eventos por dia, com necessidade de análises tanto near-real-time
quanto batch consolidado."**

Cubra, na ordem que fizer sentido pra você (não precisa seguir essa
ordem exata - um bom candidato adapta a discussão):

1. Batch, streaming, ou ambos? Justifique.
2. Desenho de ponta a ponta (componentes concretos, não abstrato).
3. Como garantir idempotência nessa escala?
4. Como monitorar a saúde desse pipeline?
5. Como escalaria se o volume triplicasse?

**Discussão adicional** (o entrevistador pode desviar pra qualquer um
destes, dependendo da sua resposta acima):
- Quando você usaria broadcast join nesse pipeline?
- Você usaria Delta Lake ou Iceberg? Por quê?
- Como isolaria bronze/silver/gold nessa escala?

---

## Follow-ups que o entrevistador faria

- "Na 1.2, sua query lida bem com clientes que compraram em M mas não existiam ainda em M-1? Isso afeta o cálculo?"
- "Na 2.1, qual a complexidade da sua solução? O(n log k) ou O(n log n)? Isso importa aqui?"
- "Na 2.2, o que acontece se o processo travar entre salvar o checkpoint e realmente persistir o dado processado? Existe uma janela de inconsistência?"
- "Na parte 4, você mencionou Kafka - o que acontece se uma partição específica ficar com hot-key (um usuário gerando 10% de todo o tráfego)?"
- "Se o time de negócio pedir consistência forte entre o dashboard near-real-time e o relatório batch, o que muda na sua arquitetura?"

## Pontos-chave esperados

- [ ] SQL 1.1 resolve corretamente com window function (ROW_NUMBER particionado) ou subquery de max, não solução ambígua
- [ ] SQL 1.2 trata corretamente o join entre meses consecutivos (CTE + self-join por mês+1)
- [ ] Python 2.1 usa heapq corretamente (O(n log k))
- [ ] Python 2.2 mantém checkpoint atualizado incrementalmente, não só no final
- [ ] dbt 3.1/3.2 demonstra entendimento real de staging/intermediate/marts, não só nomeia as pastas
- [ ] Arquitetura cobre os 5 pontos do case, com justificativa em cada (não apenas resposta "que ferramenta usar")
- [ ] Candidato reconhece hotspot de particionamento como risco de escalabilidade, não só "adicionar mais servidores"