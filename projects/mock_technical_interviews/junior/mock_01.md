# Mock Interview - Junior - Sessão 01 (45-60 min)

## Contexto
Você está entrevistando para uma vaga de Engenheiro de Dados Junior.
O entrevistador vai alternar entre SQL, Python, Pandas e uma pergunta
rápida de modelagem/arquitetura. Cronometre cada parte - o objetivo é
simular pressão de tempo real, não só acertar a resposta.

## Cronograma

| Parte | Tempo | Tema |
|---|---|---|
| 1 | 15 min | SQL |
| 2 | 10 min | Python |
| 3 | 10 min | Pandas |
| 4 | 10 min | Modelagem |
| 5 | 5-10 min | Arquitetura (mini-case) |

---

## Parte 1 - SQL (15 min)

Use o schema `drill_sql_01` (banco `estudos`).

**1.1** Liste todos os pedidos com o nome do cliente correspondente,
ordenado pela data do pedido (mais recente primeiro).

**1.2** Qual o faturamento total por segmento de cliente (considerando
só pedidos com status = 'pago')?

---

## Parte 2 - Python (10 min)

**2.1** Implemente a função `two_sum` (dado uma lista de números e um
alvo, retorne os índices dos dois elementos que somam o alvo).

**2.2** Cenário: você recebe uma lista de vendas que pode ter
duplicatas (mesmo `venda_id`). Escreva uma função que remove as
duplicatas mantendo a primeira ocorrência.

---

## Parte 3 - Pandas (10 min)

Use os dados do schema `drill_sql_02` (via `pandas_drill`).

**3.1** Carregue `sales` e `products` e faça o merge pra mostrar o
nome do produto ao lado de cada venda.

**3.2** Mostre o valor total vendido por categoria, ordenado do maior
para o menor.

---

## Parte 4 - Modelagem (10 min)

Considerando o schema de `drill_sql_01` (clientes, vendedores,
produtos, pedidos, itens_pedido, vendas_vendedor):

**4.1** Se você fosse montar um modelo dimensional (star schema) a
partir dessas tabelas, qual seria a tabela fato? Justifique.

**4.2** Quais seriam as dimensões?

---

## Parte 5 - Mini-case de Arquitetura (5-10 min)

Uma equipe quer atualizar o estoque do site sempre que uma venda
acontece numa loja física. Você recomendaria batch ou streaming?
Justifique em 3-4 frases.

---

## Follow-ups que o entrevistador faria

- "Na 1.1, o que acontece se um pedido não tiver cliente correspondente? Sua query mostraria ele ou não?"
- "Na 2.2, sua solução funciona se a lista tiver 10 milhões de registros? O que mudaria?"
- "Na 4.1, por que não a tabela `itens_pedido` como fato, em vez de `pedidos`?"

## Pontos-chave esperados (para autoavaliação)

- [ ] SQL 1.1 usa LEFT JOIN ou INNER JOIN corretamente e ordena por data
- [ ] SQL 1.2 filtra status = 'pago' ANTES de agregar (WHERE, não HAVING)
- [ ] Python 2.1 resolve em O(n) com dict, não O(n²) com loop duplo
- [ ] Python 2.2 preserva ordem original
- [ ] Pandas 3.1 usa merge com a chave correta (not concat)
- [ ] Modelagem 4.1 identifica `pedidos` OU `itens_pedido` como fato, com justificativa de granularidade
- [ ] Arquitetura 5 menciona latência aceitável como critério central (ver `data_system_design_drill/junior/cases_junior.md`, Case 1, para a resposta modelo completa)