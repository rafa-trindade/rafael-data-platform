#%%
# =========================================================
# SETUP E IMPORTAÇÃO DE DADOS
# Schema: drill_sql_01 (banco estudos)
# =========================================================
import pandas as pd
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))
from config.db_connection import get_engine

engine = get_engine()

df_clientes = pd.read_sql("SELECT * FROM drill_sql_01.clientes", engine)
df_vendedores = pd.read_sql("SELECT * FROM drill_sql_01.vendedores", engine)
df_produtos = pd.read_sql("SELECT * FROM drill_sql_01.produtos", engine)
df_pedidos = pd.read_sql("SELECT * FROM drill_sql_01.pedidos", engine)
df_itens_pedido = pd.read_sql("SELECT * FROM drill_sql_01.itens_pedido", engine)
df_vendas_vendedor = pd.read_sql("SELECT * FROM drill_sql_01.vendas_vendedor", engine)

df_pedidos.head(3)


#%%
# =========================================================
# 🟢 JOINS
# =========================================================

#%%
# 1. Liste todos os pedidos com o nome do cliente correspondente.
#    (Colunas: pedido_id, nome do cliente, data_pedido, valor_pedido, status)
#    Dica: merge(df_pedidos, df_clientes, on='cliente_id')


#%%
# 2. Liste todos os clientes, inclusive os que nunca fizeram pedidos.
#    (Colunas: cliente_id, nome, total de pedidos - zero para quem nunca comprou)
#    Dica: merge(how='left') + groupby + fillna(0)


#%%
# 3. Liste quais produtos cada cliente comprou, mostrando o nome do cliente,
#    o nome do produto e a quantidade total comprada.
#    clientes -> pedidos -> itens_pedido -> produtos (encadeie 3 merges)


#%%
# 4. Existe algum pedido sem cliente correspondente na tabela clientes?
#    Mostre esses pedidos (se existirem).
#    Dica: merge(how='left', indicator=True) e filtre _merge == 'left_only'


#%%
# 5. Liste vendedores e os nomes dos clientes que cada um atendeu,
#    sem repetir a mesma combinação vendedor-cliente.
#    clientes -> vendas_vendedor -> vendedores
#    Dica: merge + drop_duplicates(subset=[...])


#%%
# =========================================================
# 🟢 GROUP BY
# =========================================================

#%%
# 6. Quais são os 10 clientes com maior faturamento total em pedidos PAGOS?
#    (Considere apenas pedidos com status == 'pago')


#%%
# 7. Qual o faturamento total por estado, ordenado do maior para o menor?


#%%
# 8. Quantos pedidos cada cliente fez? Ordene do cliente com mais pedidos
#    para o com menos.


#%%
# 9. Qual o ticket médio (valor médio por pedido) de cada cliente?
#    Mostre apenas clientes com ao menos 2 pedidos.
#    Dica: groupby + agg(['mean', 'count']) + filtro


#%%
# 10. Qual o faturamento total por segmento de cliente?


#%%
# =========================================================
# 🟢 COUNT(DISTINCT) e COALESCE
# =========================================================

#%%
# 11. Quantos clientes únicos realizaram ao menos um pedido?
#     Retorne apenas um número.
#     Dica: df_pedidos['cliente_id'].nunique()


#%%
# 12. Liste todos os clientes e a quantidade de pedidos que fizeram.
#     Clientes sem pedidos também devem aparecer (fillna(0)).


#%%
# 13. Para cada estado, mostre:
#     estado, quantidade de clientes únicos que fizeram pedidos.
#     Estados sem nenhum cliente com pedido devem aparecer com 0.
#     Ordene do maior para o menor.


#%%
# 14. Liste todos os produtos e o total de unidades vendidas.
#     Produtos sem venda também devem aparecer, com 0.
#     Ordene do maior para o menor.


#%%
# =========================================================
# 🔵 FILTROS PÓS-AGREGAÇÃO (equivalente a HAVING)
# =========================================================

#%%
# 15. Liste clientes cujo faturamento total (pedidos pagos) supera R$ 10.000.


#%%
# 16. Liste clientes que fizeram mais de 5 pedidos.


#%%
# 17. Liste os estados onde o total de pedidos (qualquer status) é maior que 50.


#%%
# 18. Liste produtos cujo total de unidades vendidas está acima
#     da média de unidades por produto.


#%%
# =========================================================
# 🔵 AGREGAÇÕES ENCADEADAS (equivalente a CTE)
# =========================================================

#%%
# 19. Calcule o faturamento total (pedidos pagos) por cliente e
#     guarde num DataFrame chamado faturamento_cliente.


#%%
# 20. Usando faturamento_cliente, liste apenas os clientes cujo faturamento
#     está acima da média geral de faturamento por cliente.


#%%
# 21. Encontre os três meses com maior volume de vendas (pedidos pagos).
#     Mostre ano, mês e valor total.
#     Dica: dt.year, dt.month, groupby, nlargest(3)


#%%
# 22. Encontre o produto mais vendido (em quantidade) em cada categoria.
#     Dica: groupby(['categoria']) + idxmax(), ou sort + groupby.head(1)


#%%
# =========================================================
# 🟣 WINDOW FUNCTIONS (rank, shift, cumsum, rolling)
# =========================================================

#%%
# 23. Crie um ranking de clientes por faturamento total (pedidos pagos)
#     usando rank(method='min'). Mostre posição, nome do cliente e faturamento.


#%%
# 24. Repita o exercício 23 usando rank(method='dense') e compare a diferença.


#%%
# 25. Para cada cliente, mostre o pedido mais recente.
#     Dica: sort_values + groupby('cliente_id').head(1),
#     ou groupby + transform com rank


#%%
# 26. Para cada venda do vendedor 1, mostre o valor da venda anterior
#     usando shift(). Calcule também a diferença entre a venda atual e a anterior.


#%%
# 27. Para cada venda do vendedor 1, mostre o valor da próxima venda
#     usando shift(-1). Calcule a diferença entre a próxima e a atual.


#%%
# 28. Calcule o faturamento acumulado mês a mês em pedidos pagos
#     usando cumsum() sobre a série ordenada por data.


#%%
# 29. Calcule a média móvel de 3 meses no faturamento mensal de pedidos pagos
#     usando rolling(window=3).mean().


#%%
# =========================================================
# 🟣 DATAS E MÉTRICAS AVANÇADAS
# =========================================================

#%%
# 30. Qual o número de pedidos realizados nos últimos 90 dias?
#     Considere a data atual como referência (pd.Timestamp.now()).


#%%
# 31. Liste o faturamento total por mês e ano (pedidos pagos),
#     formatando o resultado como 'YYYY-MM'.
#     Ordene cronologicamente.
#     Dica: dt.to_period('M') ou dt.strftime('%Y-%m')


#%%
# 32. Qual a variação percentual do faturamento mês a mês (pedidos pagos)?
#     Mostre: ano_mes, faturamento_atual, faturamento_anterior,
#     variacao_percentual arredondada em 2 casas.
#     Dica: shift() + pct_change()


#%%
# 33. Para cada cliente, calcule:
#     - data do primeiro pedido
#     - data do último pedido
#     - quantidade de dias entre o primeiro e o último pedido (tempo de vida)
#     - quantidade total de pedidos
#     Ordene pelo tempo de vida DESC.


#%%
# 34. Liste os pedidos feitos em finais de semana (sábado ou domingo).
#     Mostre: pedido_id, data_pedido, dia_da_semana, valor_pedido.
#     Dica: dt.dayofweek (5=sábado, 6=domingo)


#%%
# 35. Calcule a taxa de retenção mensal: quantos clientes que compraram
#     no mês M também compraram no mês M+1?
#     Mostre: mes_base, clientes_no_mes, clientes_retidos_no_mes_seguinte,
#     taxa_retencao (%) arredondada em 1 casa.


#%%
# 36. Para cada mês, mostre o número de clientes novos (primeiro pedido
#     aconteceu naquele mês) versus clientes recorrentes (já tinham
#     comprado antes).
#     Colunas: ano_mes, clientes_novos, clientes_recorrentes.


#%%
# 37. Identifique clientes inativos: aqueles que fizeram ao menos um pedido,
#     mas não compram há mais de 180 dias.
#     Mostre: cliente_id, nome, ultimo_pedido, dias_sem_compra.


#%%
# 38. Calcule o faturamento acumulado do ano corrente (YTD) por mês,
#     considerando apenas pedidos pagos.
#     Mostre: mes, faturamento_mensal, faturamento_acumulado_ytd.


#%%
# 39. Calcule o tempo médio (em dias) entre pedidos consecutivos
#     de um mesmo cliente.
#     Mostre apenas clientes com ao menos 3 pedidos.
#     Colunas: cliente_id, nome, media_dias_entre_pedidos.
#     Dica: groupby + diff() na coluna de datas


#%%
# =========================================================
# QUERIES BÔNUS: análises completas para prática extra
# =========================================================

#%%
# Bônus 1: Cohort de primeiros pedidos por mês de cadastro.
#    Para cada mês de cadastro, mostre: total de clientes cadastrados,
#    quantos converteram (fizeram ao menos 1 pedido pago), e a taxa de conversão (%).


#%%
# Bônus 2: Pareto - 20% dos clientes geram 80% do faturamento?
#    Ranqueie clientes por faturamento (pedidos pagos) e calcule o
#    percentual acumulado de clientes vs percentual acumulado de faturamento.


#%%
# Bônus 3: RFM - Recência, Frequência, Monetário.
#    Para cada cliente: dias desde a última compra, número de pedidos pagos,
#    valor total gasto, e um score de 1 a 3 para cada dimensão.

