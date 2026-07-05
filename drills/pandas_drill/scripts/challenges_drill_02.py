#%%
# =========================================================
# SETUP E IMPORTAÇÃO DE DADOS
# =========================================================
import pandas as pd
import sys
import os

# Adiciona a raiz do projeto ao path para achar a pasta config
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))
from config.db_connection import get_engine

# 1. Puxa a Engine
engine = get_engine()

# 2. Carrega as tabelas direto da VPS para DataFrames na memória
df_category = pd.read_sql("SELECT * FROM drill_sql_02.category", engine)
df_products = pd.read_sql("SELECT * FROM drill_sql_02.products", engine)
df_users = pd.read_sql("SELECT * FROM drill_sql_02.users", engine)
df_sales = pd.read_sql("SELECT * FROM drill_sql_02.sales", engine)

# Exibe as primeiras linhas para confirmar
df_sales.head(3)


#%%
# =========================================================
# 🟢 JUNIOR (INTERMEDIÁRIO - Fundamentos e Limpeza)
# =========================================================

#%%
# 1. Liste todas as vendas com produto, categoria, cliente e vendedor, ordenado por valor.
# Preparando os DataFrames de Dimensão (renomeando a coluna 'name' para evitar colisão)



#%%
# 2. Liste os produtos com suas respectivas categorias.



#%%
# 3. Liste todas as vendas com nome do cliente e nome do vendedor.
    

#%%
# 4. Mostre o valor total vendido por categoria.


#%%
# 5. Qual o total geral de vendas da base?


#%%
# 6. Qual o total de vendas por cliente?


#%%
# 7. Qual o total de vendas por vendedor?


#%%
# 8. Qual categoria tem maior número de produtos?


#%%
# 9. Qual categoria tem maior receita total?


#%%
# 10. Qual produto gera maior receita total?


#%%
# 11. Qual cliente comprou mais produtos da categoria "Dairy"?


#%%
# 12. Liste clientes que nunca compraram nada da categoria "Dairy".


#%%
# 13. Liste produtos que nunca foram vendidos.


#%%
# 14. Limpeza de Strings: Extraia apenas o domínio de e-mail de cada cliente (tudo que vem após o "@") e conte quantos clientes usam cada domínio.


#%%
# =========================================================
# 🔵 PLENO (WINDOW FUNCTIONS, JOINS AVANÇADOS E FILTROS)
# =========================================================

#%%
# 15. Rank de clientes por total gasto usando DENSE_RANK().


#%%
# 16. Top 3 vendedores por receita usando window function.


#%%
# 17. Compra mais cara de cada cliente (ROW_NUMBER).


#%%
# 18. Running total de vendas ordenado por sale_id.


#%%
# 19. Diferença de cada venda vs média geral (AVG OVER).


#%%
# 20. Mostre o cliente que teve o maior valor de compra e o vendedor que teve o maior valor de venda.


#%%
# 21. Para cada vendedor, mostre a lista de clientes que ele atendeu.


#%%
# 22. Self Join: Identifique pares de produtos que pertencem à mesma categoria e possuem uma diferença de preço menor que $1.


#%%
# 23. Agregação com HAVING: Retorne os vendedores que geraram mais de $50 em receita total, mas que realizaram menos de 5 transações (foco em ticket médio alto).


#%%
# =========================================================
# 🟣 SÊNIOR | ANALYTICS (DATAS, NULOS, PIVOT E RETENÇÃO)
# =========================================================

#%%
# 24. Inteligência de Tempo: Extraia o ano e o mês da data de venda e mostre a receita total por mês (dt.year / dt.month).


#%%
# 25. Crescimento Mensal (MoM): Calcule a variação percentual da receita em relação ao mês imediatamente anterior usando a função shift().


#%%
# 26. Agregação Condicional (Pivot): Mostre o gasto total de cada cliente, mas divida esse valor em colunas dedicadas por categoria (ex: Gasto_Meat, Gasto_Dairy, Gasto_Outros) usando pivot_table ou np.where.


#%%
# 27. Classificação de LTV: Classifique os clientes em faixas de negócio como "Premium" (gasto total > 100), "Regular" (entre 50 e 100) e "Starter" (< 50) e traga a contagem de clientes em cada faixa.


#%%
# 28. Tratamento de Nulos: Liste todos os clientes e os responsáveis pelo atendimento. Se não houver vendedor associado à venda, exiba a string 'Venda Direta Automática' (usando fillna).


#%%
# 29. Auditoria de Qualidade de Dados (Data Quality): Identifique as vendas inconsistentes, ou seja, onde o total faturado registrado difere da multiplicação da quantidade vendida pelo preço base do produto.


#%%
# 30. Recência: Calcule a quantidade de dias entre a última compra de cada cliente e a data atual (ou data máxima do dataset).


#%%
# 31. Tempo de Vida (Lifetime): Calcule a diferença em dias entre a data da primeira e da última compra de cada cliente para entender a janela de relacionamento.


#%%
# 32. Retenção de Clientes (Cohorts): Identifique os clientes fidelizados - traga apenas aqueles que realizaram compras no mês passado E TAMBÉM voltaram a comprar no mês atual.


#%%
# 33. Engajamento de Vendas: Identifique gaps de vendas calculando a quantidade de dias que cada vendedor ficou sem registrar nenhuma transação.


#%%
# 34. Média Móvel (Rolling Average): Calcule a média móvel de faturamento dos últimos 3 dias para cada vendedor usando rolling().


#%%
# 35. Deduplicação de Registros: Crie uma lógica que filtre transações duplicadas (mesmo cliente, produto e data), mantendo apenas o registro com o maior total faturado (drop_duplicates).


#%%
# 36. Acumulado no Ano (YTD - Year-to-Date): Calcule o faturamento acumulado particionado por ano e por categoria (cumsum), reiniciando a contagem a cada virada de ano.#%%
# =========================================================
# SETUP E IMPORTAÇÃO DE DADOS
# =========================================================
import pandas as pd
import sys
import os

# Adiciona a raiz do projeto ao path para achar a pasta config
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))
from config.db_connection import get_engine

# 1. Puxa a Engine
engine = get_engine()

# 2. Carrega as tabelas direto da VPS para DataFrames na memória
df_category = pd.read_sql("SELECT * FROM drill_sql_02.category", engine)
df_products = pd.read_sql("SELECT * FROM drill_sql_02.products", engine)
df_users = pd.read_sql("SELECT * FROM drill_sql_02.users", engine)
df_sales = pd.read_sql("SELECT * FROM drill_sql_02.sales", engine)

# Exibe as primeiras linhas para confirmar
df_sales.head(3)


#%%
# =========================================================
# 🟢 JUNIOR (INTERMEDIÁRIO - Fundamentos e Limpeza)
# =========================================================

#%%
# 1. Liste todas as vendas com produto, categoria, cliente e vendedor, ordenado por valor.
# Preparando os DataFrames de Dimensão (renomeando a coluna 'name' para evitar colisão)



#%%
# 2. Liste os produtos com suas respectivas categorias.



#%%
# 3. Liste todas as vendas com nome do cliente e nome do vendedor.
    

#%%
# 4. Mostre o valor total vendido por categoria.


#%%
# 5. Qual o total geral de vendas da base?


#%%
# 6. Qual o total de vendas por cliente?


#%%
# 7. Qual o total de vendas por vendedor?


#%%
# 8. Qual categoria tem maior número de produtos?


#%%
# 9. Qual categoria tem maior receita total?


#%%
# 10. Qual produto gera maior receita total?


#%%
# 11. Qual cliente comprou mais produtos da categoria "Dairy"?


#%%
# 12. Liste clientes que nunca compraram nada da categoria "Dairy".


#%%
# 13. Liste produtos que nunca foram vendidos.


#%%
# 14. Limpeza de Strings: Extraia apenas o domínio de e-mail de cada cliente (tudo que vem após o "@") e conte quantos clientes usam cada domínio.


#%%
# =========================================================
# 🔵 PLENO (WINDOW FUNCTIONS, JOINS AVANÇADOS E FILTROS)
# =========================================================

#%%
# 15. Rank de clientes por total gasto usando DENSE_RANK().


#%%
# 16. Top 3 vendedores por receita usando window function.


#%%
# 17. Compra mais cara de cada cliente (ROW_NUMBER).


#%%
# 18. Running total de vendas ordenado por sale_id.


#%%
# 19. Diferença de cada venda vs média geral (AVG OVER).


#%%
# 20. Mostre o cliente que teve o maior valor de compra e o vendedor que teve o maior valor de venda.


#%%
# 21. Para cada vendedor, mostre a lista de clientes que ele atendeu.


#%%
# 22. Self Join: Identifique pares de produtos que pertencem à mesma categoria e possuem uma diferença de preço menor que $1.


#%%
# 23. Agregação com HAVING: Retorne os vendedores que geraram mais de $50 em receita total, mas que realizaram menos de 5 transações (foco em ticket médio alto).


#%%
# =========================================================
# 🟣 SÊNIOR | ANALYTICS (DATAS, NULOS, PIVOT E RETENÇÃO)
# =========================================================

#%%
# 24. Inteligência de Tempo: Extraia o ano e o mês da data de venda e mostre a receita total por mês (dt.year / dt.month).


#%%
# 25. Crescimento Mensal (MoM): Calcule a variação percentual da receita em relação ao mês imediatamente anterior usando a função shift().


#%%
# 26. Agregação Condicional (Pivot): Mostre o gasto total de cada cliente, mas divida esse valor em colunas dedicadas por categoria (ex: Gasto_Meat, Gasto_Dairy, Gasto_Outros) usando pivot_table ou np.where.


#%%
# 27. Classificação de LTV: Classifique os clientes em faixas de negócio como "Premium" (gasto total > 100), "Regular" (entre 50 e 100) e "Starter" (< 50) e traga a contagem de clientes em cada faixa.


#%%
# 28. Tratamento de Nulos: Liste todos os clientes e os responsáveis pelo atendimento. Se não houver vendedor associado à venda, exiba a string 'Venda Direta Automática' (usando fillna).


#%%
# 29. Auditoria de Qualidade de Dados (Data Quality): Identifique as vendas inconsistentes, ou seja, onde o total faturado registrado difere da multiplicação da quantidade vendida pelo preço base do produto.


#%%
# 30. Recência: Calcule a quantidade de dias entre a última compra de cada cliente e a data atual (ou data máxima do dataset).


#%%
# 31. Tempo de Vida (Lifetime): Calcule a diferença em dias entre a data da primeira e da última compra de cada cliente para entender a janela de relacionamento.


#%%
# 32. Retenção de Clientes (Cohorts): Identifique os clientes fidelizados - traga apenas aqueles que realizaram compras no mês passado E TAMBÉM voltaram a comprar no mês atual.


#%%
# 33. Engajamento de Vendas: Identifique gaps de vendas calculando a quantidade de dias que cada vendedor ficou sem registrar nenhuma transação.


#%%
# 34. Média Móvel (Rolling Average): Calcule a média móvel de faturamento dos últimos 3 dias para cada vendedor usando rolling().


#%%
# 35. Deduplicação de Registros: Crie uma lógica que filtre transações duplicadas (mesmo cliente, produto e data), mantendo apenas o registro com o maior total faturado (drop_duplicates).


#%%
# 36. Acumulado no Ano (YTD - Year-to-Date): Calcule o faturamento acumulado particionado por ano e por categoria (cumsum), reiniciando a contagem a cada virada de ano.