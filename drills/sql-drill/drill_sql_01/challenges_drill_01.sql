--==========================
--EXERCÍCIOS DE ENTREVISTA
--==========================

--Abaixo estão os exercícios organizados por tema.
--Tente resolver cada um antes de consultar o GABARITO.

-- docker exec -it PostgreSQL psql -U rafael -d analytics_engineer_interview_lab

--━━━━━━━━━━━━━━━━━━━━━━━━━
--JOINS
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 1. Liste todos os pedidos com o nome do cliente correspondente.
--    (Colunas: pedido_id, nome do cliente, data_pedido, valor_pedido, status)



-- 2. Liste todos os clientes, inclusive os que nunca fizeram pedidos.
--    (Colunas: cliente_id, nome, total de pedidos - zero para quem nunca comprou)



-- 3. Liste quais produtos cada cliente comprou, mostrando o nome do cliente,
--    o nome do produto e a quantidade total comprada.

-- clientes -> pedidos -> itens_pedido -> produtos



-- 4. Existe algum pedido sem cliente correspondente na tabela clientes?
--    Mostre esses pedidos (se existirem).



-- 5. Liste vendedores e os nomes dos clientes que cada um atendeu,
--    sem repetir a mesma combinação vendedor–cliente.

-- clientes -> vendas_vendedor -> vendedores




--━━━━━━━━━━━━━━━━━━━━━━━━━
--GROUP BY
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 6.  Quais são os 10 clientes com maior faturamento total em pedidos PAGOS?
--     (Considere apenas pedidos com status = 'pago')




-- 7.  Qual o faturamento total por estado, ordenado do maior para o menor?




-- 8.  Quantos pedidos cada cliente fez? Ordene do cliente com mais pedidos
--     para o com menos.





-- 9.  Qual o ticket médio (valor médio por pedido) de cada cliente?
--     Mostre apenas clientes com ao menos 2 pedidos.





-- 10. Qual o faturamento total por segmento de cliente?




--━━━━━━━━━━━━━━━━━━━━━━━━━
--COUNT(DISTINCT)
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 11. Quantos clientes únicos realizaram ao menos um pedido?
--     Retorne apenas uma linha com essa informação.




--━━━━━━━━━━━━━━━━━━━━━━━━━
--COALESCE
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 12. Liste todos os clientes e a quantidade de pedidos que fizeram.
--     Clientes sem pedidos também devem aparecer.



--━━━━━━━━━━━━━━━━━━━━━━━━━
--COALESCE + COUNT(DISTINCT)
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 13. Para cada estado, mostre:
--
--     estado
--     quantidade de clientes únicos que fizeram pedidos
--
--     Caso um estado não tenha nenhum cliente com pedido,
--     exiba 0.
--
--     Ordene do maior para o menor.




-- 14. Liste todos os produtos e o total de unidades vendidas.
--
--     Produtos sem venda também devem aparecer.
--
--     Exiba:
--     nome_produto
--     total_unidades_vendidas
--
--     Substitua valores nulos por 0.
--
--     Ordene do maior para o menor.





--━━━━━━━━━━━━━━━━━━━━━━━━━
--HAVING
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 15. Liste clientes cujo faturamento total (pedidos pagos) supera R$ 10.000.



-- 16. Liste clientes que fizeram mais de 5 pedidos.





-- 17. Liste os estados onde o total de pedidos (qualquer status) é maior que 50.




-- 18. Liste produtos cujo total de unidades vendidas está acima
--     da média de unidades por produto.




--━━━━━━━━━━━━━━━━━━━━━━━━━
--CTE (Common Table Expressions)
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 19. Crie uma CTE chamada faturamento_cliente que calcule o total de vendas
--     (pedidos pagos) por cliente. Em seguida, selecione todos os dados dela.




-- 20. Usando a CTE do exercício anterior (ou uma nova), liste apenas os clientes
--     cujo faturamento está acima da média geral de faturamento por cliente.




-- 21. Usando CTEs, encontre os três meses com maior volume de vendas
--     (pedidos pagos). Mostre ano, mês e valor total.




-- 22. Usando CTEs, encontre o produto mais vendido (em quantidade) em cada
--     categoria.




--━━━━━━━━━━━━━━━━━━━━━━━━━
--WINDOW FUNCTIONS
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 23. Crie um ranking de clientes por faturamento total (pedidos pagos)
--     usando RANK(). Mostre posição, nome do cliente e faturamento.



-- 24. Repita o exercício 19 usando DENSE_RANK() e compare a diferença.



-- 25. Para cada cliente, mostre o pedido mais recente usando ROW_NUMBER()
--     particionado por cliente_id e ordenado por data_pedido DESC.



-- 26. Para cada venda do vendedor 1, mostre o valor da venda anterior
--     usando LAG(). Calcule também a diferença entre a venda atual e a anterior.



-- 27. Para cada venda do vendedor 1, mostre o valor da próxima venda
--     usando LEAD(). Calcule a diferença entre a próxima e a atual.



-- 28. Calcule o faturamento acumulado mês a mês em pedidos pagos
--     usando SUM() OVER (ORDER BY ...).



-- 29. Calcule a média móvel de 3 meses no faturamento mensal de pedidos pagos
--     usando AVG() OVER (ROWS BETWEEN ...).



--━━━━━━━━━━━━━━━━━━━━━━━━━
-- DATAS E MÉTRICAS AVANÇADAS
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 30. Qual o número de pedidos realizados nos últimos 90 dias?
--     Considere a data atual como referência.
--     (Dica: use CURRENT_DATE ou NOW())



-- 31. Liste o faturamento total por mês e ano (pedidos pagos),
--     formatando o resultado como 'YYYY-MM'.
--     Ordene cronologicamente.
--     (Dica: DATE_TRUNC ou EXTRACT)



-- 32. Qual a variação percentual do faturamento mês a mês (pedidos pagos)?
--     Mostre: ano_mes, faturamento_atual, faturamento_anterior,
--     variacao_percentual arredondada em 2 casas.
--     (Dica: LAG() + cálculo de variação)



-- 33. Para cada cliente, calcule:
--
--     - data do primeiro pedido
--     - data do último pedido
--     - quantidade de dias entre o primeiro e o último pedido (tempo de vida)
--     - quantidade total de pedidos
--
--     Ordene pelo tempo de vida DESC.



-- 34. Liste os pedidos feitos em finais de semana (sábado ou domingo).
--     Mostre: pedido_id, data_pedido, dia_da_semana, valor_pedido.
--     (Dica: EXTRACT(DOW FROM ...) ou TO_CHAR(..., 'D'))



-- 35. Calcule a taxa de retenção mensal: quantos clientes que compraram
--     no mês M também compraram no mês M+1?
--     Mostre: mes_base, clientes_no_mes, clientes_retidos_no_mes_seguinte,
--     taxa_retencao (%) arredondada em 1 casa.
--     (Dica: CTEs + JOIN entre meses consecutivos)



-- 36. Para cada mês, mostre o número de clientes novos (primeiro pedido
--     aconteceu naquele mês) versus clientes recorrentes (já tinham
--     comprado antes).
--     Colunas: ano_mes, clientes_novos, clientes_recorrentes.



-- 37. Identifique clientes inativos: aqueles que fizeram ao menos um pedido,
--     mas não compram há mais de 180 dias.
--     Mostre: cliente_id, nome, ultimo_pedido, dias_sem_compra.



-- 38. Usando uma CTE, calcule o faturamento acumulado do ano corrente
--     (YTD - Year To Date) por mês, considerando apenas pedidos pagos.
--     Mostre: mes, faturamento_mensal, faturamento_acumulado_ytd.



-- 39. Calcule o tempo médio (em dias) entre pedidos consecutivos
--     de um mesmo cliente.
--     Mostre apenas clientes com ao menos 3 pedidos.
--     Colunas: cliente_id, nome, media_dias_entre_pedidos.
--     (Dica: LAG() para pegar a data do pedido anterior por cliente)



-- ====================================================================
-- QUERIES BÔNUS: Consultas analíticas completas para prática extra
-- ====================================================================

-- Bônus 1: Cohort de primeiros pedidos por mês de cadastro
WITH primeiro_pedido AS (
    SELECT
        c.cliente_id,
        c.nome,
        DATE_TRUNC('month', c.data_cadastro)::DATE AS mes_cadastro,
        MIN(p.data_pedido) AS data_primeiro_pedido,
        DATE_TRUNC('month', MIN(p.data_pedido))::DATE AS mes_primeiro_pedido
    FROM clientes c
    LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.status = 'pago'
    GROUP BY c.cliente_id, c.nome, c.data_cadastro
)
SELECT
    TO_CHAR(mes_cadastro, 'YYYY-MM') AS cohort,
    COUNT(cliente_id)                AS total_clientes,
    COUNT(data_primeiro_pedido)      AS clientes_que_compraram,
    ROUND(
        100.0 * COUNT(data_primeiro_pedido) / COUNT(cliente_id), 1
    ) AS taxa_conversao_pct
FROM primeiro_pedido
GROUP BY mes_cadastro
ORDER BY mes_cadastro;


-- Bônus 2: Pareto - 20% dos clientes geram 80% do faturamento?
WITH fat_cliente AS (
    SELECT
        c.cliente_id,
        c.nome,
        SUM(p.valor_pedido) AS faturamento
    FROM clientes c
    INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
    WHERE p.status = 'pago'
    GROUP BY c.cliente_id, c.nome
),
total AS (
    SELECT SUM(faturamento) AS total_geral FROM fat_cliente
),
ranking AS (
    SELECT
        fc.*,
        t.total_geral,
        ROW_NUMBER() OVER (ORDER BY fc.faturamento DESC) AS rn,
        COUNT(*) OVER () AS total_clientes,
        SUM(fc.faturamento) OVER (
            ORDER BY fc.faturamento DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS faturamento_acumulado
    FROM fat_cliente fc
    CROSS JOIN total t
)
SELECT
    rn                                                     AS posicao,
    nome,
    faturamento,
    ROUND(100.0 * rn / total_clientes, 1)                 AS pct_clientes_acumulado,
    ROUND(100.0 * faturamento_acumulado / total_geral, 1) AS pct_faturamento_acumulado
FROM ranking
ORDER BY rn;


-- Bônus 3: RFM - Recência, Frequência, Monetário (base de segmentação)
WITH rfm_base AS (
    SELECT
        c.cliente_id,
        c.nome,
        MAX(p.data_pedido)               AS ultima_compra,
        CURRENT_DATE - MAX(p.data_pedido) AS recencia_dias,
        COUNT(p.pedido_id)               AS frequencia,
        SUM(p.valor_pedido)              AS monetario
    FROM clientes c
    INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
    WHERE p.status = 'pago'
    GROUP BY c.cliente_id, c.nome
)
SELECT
    cliente_id,
    nome,
    recencia_dias,
    frequencia,
    monetario,
    -- Classificação simples R/F/M (1=melhor, 3=pior)
    CASE
        WHEN recencia_dias <= 90  THEN 1
        WHEN recencia_dias <= 180 THEN 2
        ELSE 3
    END AS score_recencia,
    CASE
        WHEN frequencia >= 10 THEN 1
        WHEN frequencia >= 5  THEN 2
        ELSE 3
    END AS score_frequencia,
    CASE
        WHEN monetario >= 10000 THEN 1
        WHEN monetario >= 3000  THEN 2
        ELSE 3
    END AS score_monetario
FROM rfm_base
ORDER BY monetario DESC;



--━━━━━━━━━━━━━━━━━━━━━━━━━
--MODELAGEM
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 1. Qual a granularidade da tabela pedidos? O que representa cada linha?

-- 2. Qual a granularidade da tabela itens_pedido? Como ela se diferencia
--     de pedidos?

-- 3. Em um modelo dimensional, qual(is) tabela(s) seria(m) fato?
--     Justifique.

-- 4. Quais tabelas seriam dimensões? Justifique.

-- 5. Desenhe (ou descreva textualmente) como ficaria o Star Schema dessas
--     tabelas.

--━━━━━━━━━━━━━━━━━━━━━━━━━
--ANALYTICS ENGINEERING
--━━━━━━━━━━━━━━━━━━━━━━━━━

-- 1. Como você organizaria essas tabelas em um projeto dbt?
--     Descreva a estrutura de pastas.

-- 2. Quais modelos ficariam na camada staging?
--     O que é responsabilidade dessa camada?

-- 3. Quais modelos ficariam na camada intermediate?
--     Dê exemplos de transformações adequadas para ela.

-- 4. Quais modelos ficariam na camada marts?
--     Quem consome essa camada?

-- 5. Quais testes de qualidade de dados você aplicaria?
--     Dê exemplos concretos usando dbt tests.

-- 6. Como você documentaria esse projeto no dbt?
--     O que deve constar em schema.yml?

-- 7. Como garantir consistência entre os dashboards e os modelos de dados?
--     Quais práticas ajudam a evitar divergências?
