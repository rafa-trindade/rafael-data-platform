# Mock Interview - Pleno - Sessão 01 (60-75 min)

## Contexto
Vaga de Engenheiro de Dados Pleno. A entrevista mistura profundidade
técnica (window functions, CDC, SCD) com uma discussão arquitetural
mais longa no final.

## Cronograma

| Parte | Tempo | Tema |
|---|---|---|
| 1 | 15 min | SQL (window functions) |
| 2 | 15 min | Python (cenário de engenharia de dados) |
| 3 | 10 min | Pandas |
| 4 | 10 min | Modelagem (SCD) |
| 5 | 5 min | dbt |
| 6 | 15-20 min | Discussão de arquitetura |

---

## Parte 1 - SQL (15 min)

Use `drill_sql_01`.

**1.1** Crie um ranking de clientes por faturamento total (pedidos
pagos) usando `RANK()`. Mostre posição, nome e faturamento.

**1.2** Calcule a variação percentual do faturamento mês a mês
(pedidos pagos), usando `LAG()`.

---

## Parte 2 - Python (15 min)

**2.1** Cenário CDC: dado dois snapshots de uma tabela (antigo e
novo), implemente uma função que retorna o que foi inserido, deletado
e atualizado (comparando por chave).

**2.2** Follow-up verbal (sem código): se você não tivesse acesso a
snapshots completos, só a um stream de eventos de mudança, como isso
mudaria sua abordagem?

---

## Parte 3 - Pandas (10 min)

Usando `drill_sql_01` (via `pandas_drill`):

**3.1** Calcule o ticket médio (valor médio por pedido) de cada
cliente, mostrando apenas clientes com pelo menos 2 pedidos.

---

## Parte 4 - Modelagem: SCD (10 min)

**4.1** O que é uma dimensão SCD Tipo 2? Dê um exemplo prático usando
a tabela `produtos` (imagine que o preço do produto muda ao longo do
tempo).

**4.2** Como você implementaria isso no schema `analytics` via dbt?
Quais colunas adicionais você precisaria (ex: `valido_de`, `valido_ate`, `is_atual`)?

---

## Parte 5 - dbt (5 min)

**5.1** Quais testes nativos do dbt você aplicaria num model de
`fct_vendas` que referencia `dim_produto` e `dim_cliente`?

---

## Parte 6 - Discussão de Arquitetura (15-20 min)

Case: pipeline de ingestão incremental de uma tabela de 50 milhões
de linhas, atualizando um dashboard de hora em hora (ver
`data_system_design_drill/pleno/cases_pleno.md`, Case 1, se quiser
revisar a resposta modelo depois).

Responda, sem consultar antes:
1. Estratégia de incremental
2. Como lidar com updates
3. Como lidar com late arriving data
4. Desenhe o fluxo bronze → silver → gold

---

## Follow-ups que o entrevistador faria

- "Na 1.1, qual a diferença entre RANK() e DENSE_RANK() aqui? Import isso pra esse caso?"
- "Na 2.1, sua solução escala bem se as tabelas tiverem 10 milhões de linhas? O que você mudaria?"
- "Na 4.2, o que acontece com queries que fazem JOIN direto sem filtrar `is_atual = true`? Isso é um risco?"
- "Na parte 6, e se a fonte não tiver `updated_at`? Qual seria o plano B?"

## Pontos-chave esperados

- [ ] SQL 1.1 usa PARTITION/ORDER corretamente com RANK()
- [ ] SQL 1.2 usa LAG() com particionamento adequado (se necessário) e calcula variação percentual corretamente
- [ ] Python 2.1 usa hashing/dict pra comparar por chave em O(n), não nested loop
- [ ] Python 2.2 menciona CDC real (Debezium/logical replication) como alternativa a snapshot diff
- [ ] Modelagem 4.1/4.2 explica SCD2 com colunas de vigência corretamente
- [ ] dbt 5.1 cita unique, not_null, relationships no mínimo
- [ ] Arquitetura cobre watermark/CDC, upsert, janela de reprocessamento pra late data