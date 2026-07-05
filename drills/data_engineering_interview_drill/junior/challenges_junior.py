#%%
# =========================================================
# DATA ENGINEERING INTERVIEW DRILL - NÍVEL JUNIOR
# Cenários práticos de pipeline, sem teoria abstrata
# =========================================================

#%%
# 1. Deduplicação por chave (idempotência básica)
#
# CENÁRIO: Você recebe diariamente um CSV de vendas que pode conter
# a mesma venda duplicada (o sistema de origem às vezes reenvia o
# mesmo arquivo, ou o mesmo registro duas vezes por retry de rede).
#
# TAREFA: escreva uma função que recebe uma lista de dicts e retorna
# a lista deduplicada por uma chave, mantendo a PRIMEIRA ocorrência.
#
# POR QUE ISSO IMPORTA: pipelines não-idempotentes duplicam receita
# em relatórios sempre que um job é re-executado - bug clássico e caro.

def deduplicate_by_key(records: list, key: str) -> list:
    seen = set()
    result = []
    for r in records:
        if r[key] not in seen:
            seen.add(r[key])
            result.append(r)
    return result

#%%
# Teste manual
vendas_demo = [
    {"venda_id": 1, "valor": 100}, {"venda_id": 2, "valor": 200},
    {"venda_id": 1, "valor": 100},
]
print(deduplicate_by_key(vendas_demo, "venda_id"))

#%%
vendas = [
    {"venda_id": 1, "valor": 100}, {"venda_id": 2, "valor": 200},
    {"venda_id": 1, "valor": 100},
]
result = deduplicate_by_key(vendas, "venda_id")
assert len(result) == 2
assert [r["venda_id"] for r in result] == [1, 2]

#%%
# 2. Processar arquivo gigante sem carregar tudo na memória
#
# CENÁRIO: você recebe um arquivo de 50GB de logs, mas sua máquina
# tem 8GB de RAM. Ler tudo com uma lista normal vai quebrar.
#
# TAREFA: implemente um GERADOR (generator, usando yield) que lê
# "linhas" de uma fonte (aqui simulada por uma lista, no mundo real
# seria um arquivo) e processa uma por vez, sem nunca ter mais de
# uma linha na memória. Retorne a soma dos valores, processando
# via generator.

def sum_via_generator(source: list) -> int:
    def line_generator():
        for line in source:
            yield line
    pass

#%%
# Teste manual
print(sum_via_generator([10, 20, 30, 40]))

#%%
assert sum_via_generator([10, 20, 30, 40]) == 100
assert sum_via_generator([]) == 0

#%%
# 3. Particionamento por data
#
# CENÁRIO: você vai escrever dados no data lake seguindo a convenção
# `bronze/vendas/ano=YYYY/mes=MM/dia=DD/`. Antes de escrever nos
# arquivos, você precisa agrupar os registros por essa partição.
#
# TAREFA: dado uma lista de registros com campo 'data' (string
# 'YYYY-MM-DD'), retorne um dict onde a chave é a partição no formato
# "ano=YYYY/mes=MM/dia=DD" e o valor é a lista de registros daquele dia.

def partition_by_date(records: list) -> dict:
    pass

#%%
# Teste manual
regs_demo = [
    {"id": 1, "data": "2026-01-15"}, {"id": 2, "data": "2026-01-15"},
    {"id": 3, "data": "2026-02-01"},
]
print(partition_by_date(regs_demo))

#%%
regs = [
    {"id": 1, "data": "2026-01-15"}, {"id": 2, "data": "2026-01-15"},
    {"id": 3, "data": "2026-02-01"},
]
result = partition_by_date(regs)
assert len(result["ano=2026/mes=01/dia=15"]) == 2
assert len(result["ano=2026/mes=02/dia=01"]) == 1

#%%
# 4. Validação de schema simples
#
# CENÁRIO: antes de carregar um lote no staging, você precisa
# garantir que todo registro tem os campos obrigatórios.
#
# TAREFA: dado uma lista de registros e uma lista de campos
# obrigatórios, retorne uma tupla (validos, invalidos) - invalidos
# é a lista de registros que faltam algum campo obrigatório.

def validate_required_fields(records: list, required: list) -> tuple:
    pass

#%%
# Teste manual
regs2_demo = [
    {"id": 1, "nome": "A", "valor": 10},
    {"id": 2, "valor": 20},  # falta 'nome'
]
print(validate_required_fields(regs2_demo, ["id", "nome", "valor"]))

#%%
regs2 = [
    {"id": 1, "nome": "A", "valor": 10},
    {"id": 2, "valor": 20},
]
validos, invalidos = validate_required_fields(regs2, ["id", "nome", "valor"])
assert len(validos) == 1
assert len(invalidos) == 1
assert invalidos[0]["id"] == 2

#%%
# 5. Retry com backoff exponencial
#
# CENÁRIO: uma chamada de API externa (extração de dados) falha
# de forma intermitente. Você não quer desistir na primeira falha,
# mas também não quer martelar o serviço sem espaçar as tentativas.
#
# TAREFA: implemente uma função retry(func, max_attempts) que chama
# `func`, e se ela levantar exceção, tenta de novo até max_attempts
# vezes, esperando 2^tentativa segundos entre tentativas (backoff
# exponencial). Se todas as tentativas falharem, relança a exceção.
# Para o teste, use um sleep bem pequeno (não precisa esperar de verdade
# em produção seria segundos reais).

import time

def retry(func, max_attempts: int = 3, base_delay: float = 0.01):
    pass

#%%
# Teste manual - função que falha 2 vezes e funciona na 3ª
attempts_demo = {"count": 0}
def flaky_demo():
    attempts_demo["count"] += 1
    if attempts_demo["count"] < 3:
        raise ValueError("falhou")
    return "sucesso"

print(retry(flaky_demo, max_attempts=5, base_delay=0.01))
print(attempts_demo["count"])

#%%
attempts = {"count": 0}
def flaky():
    attempts["count"] += 1
    if attempts["count"] < 3:
        raise ValueError("falhou")
    return "sucesso"

assert retry(flaky, max_attempts=5, base_delay=0.01) == "sucesso"
assert attempts["count"] == 3

def always_fails():
    raise ValueError("sempre falha")

try:
    retry(always_fails, max_attempts=2, base_delay=0.01)
    assert False, "deveria ter levantado exceção"
except ValueError:
    pass

#%%
# 6. Upsert idempotente numa "tabela" simulada
#
# CENÁRIO: seu pipeline de carga roda todo dia e precisa inserir
# registros novos e ATUALIZAR os que já existem - sem duplicar,
# mesmo se o job for executado duas vezes com os mesmos dados.
#
# TAREFA: implemente upsert(table: dict, records: list, key: str)
# que aplica cada registro na "tabela" (um dict de dicts, indexado
# pela chave): se a chave já existe, sobrescreve; se não, insere.
# Rodar a mesma função duas vezes com o mesmo input deve deixar
# a tabela no mesmo estado (idempotência).

def upsert(table: dict, records: list, key: str) -> dict:
    pass

#%%
# Teste manual
tabela_demo = {}
upsert(tabela_demo, [{"id": 1, "valor": 100}, {"id": 2, "valor": 200}], "id")
print(tabela_demo)
upsert(tabela_demo, [{"id": 1, "valor": 999}], "id")
print(tabela_demo)

#%%
tabela = {}
upsert(tabela, [{"id": 1, "valor": 100}, {"id": 2, "valor": 200}], "id")
assert tabela[1]["valor"] == 100
upsert(tabela, [{"id": 1, "valor": 999}], "id")
assert tabela[1]["valor"] == 999
assert len(tabela) == 2
# rodar de novo com o mesmo input não deve mudar nada nem duplicar
upsert(tabela, [{"id": 1, "valor": 999}], "id")
assert len(tabela) == 2