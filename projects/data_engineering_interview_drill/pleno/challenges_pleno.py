#%%
# =========================================================
# DATA ENGINEERING INTERVIEW DRILL - NÍVEL PLENO
# CDC, merge incremental, watermark, late data, joins grandes
# =========================================================

#%%
# 1. CDC simplificado (diff entre snapshots)
#
# CENÁRIO: você não tem acesso a um CDC de verdade (Debezium/logical
# replication), só a dois snapshots completos da tabela de origem
# (ontem e hoje). Você precisa derivar o que mudou.
#
# TAREFA: dado dois snapshots (listas de dicts com 'id'), retorne um
# dict com três listas: 'inserted' (ids que só existem no novo),
# 'deleted' (ids que só existem no antigo), 'updated' (ids que existem
# nos dois mas com algum campo diferente).

def diff_snapshots(old: list, new: list, key: str = "id") -> dict:
    old_map = {r[key]: r for r in old}
    new_map = {r[key]: r for r in new}

    old_ids = set(old_map.keys())
    new_ids = set(new_map.keys())

    inserted = sorted(new_ids - old_ids)
    deleted = sorted(old_ids - new_ids)
    updated = sorted(
        k for k in (old_ids & new_ids)
        if old_map[k] != new_map[k]
    )

    return {"inserted": inserted, "deleted": deleted, "updated": updated}

#%%
# Teste manual
old_demo = [{"id": 1, "valor": 100}, {"id": 2, "valor": 200}, {"id": 3, "valor": 300}]
new_demo = [{"id": 1, "valor": 100}, {"id": 2, "valor": 999}, {"id": 4, "valor": 400}]
print(diff_snapshots(old_demo, new_demo))

#%%
old = [{"id": 1, "valor": 100}, {"id": 2, "valor": 200}, {"id": 3, "valor": 300}]
new = [{"id": 1, "valor": 100}, {"id": 2, "valor": 999}, {"id": 4, "valor": 400}]
result = diff_snapshots(old, new)
assert result["inserted"] == [4]
assert result["deleted"] == [3]
assert result["updated"] == [2]

#%%
# 2. Merge incremental (upsert em lote com auditoria)
#
# CENÁRIO: além de fazer o upsert, seu time de dados quer saber
# QUANTOS registros foram inseridos vs atualizados em cada carga,
# pra monitorar o pipeline.
#
# TAREFA: implemente merge_incremental(table, records, key) que faz
# o upsert E retorna um relatório {'inserted': N, 'updated': N}.

def merge_incremental(table: dict, records: list, key: str) -> dict:
    pass

#%%
# Teste manual
tabela_demo = {1: {"id": 1, "valor": 100}}
report_demo = merge_incremental(tabela_demo, [{"id": 1, "valor": 999}, {"id": 2, "valor": 200}], "id")
print(report_demo, tabela_demo)

#%%
tabela = {1: {"id": 1, "valor": 100}}
report = merge_incremental(tabela, [{"id": 1, "valor": 999}, {"id": 2, "valor": 200}], "id")
assert report == {"inserted": 1, "updated": 1}
assert tabela[1]["valor"] == 999
assert tabela[2]["valor"] == 200

#%%
# 3. Leitura incremental com watermark
#
# CENÁRIO: seu pipeline não pode reler a tabela de origem inteira
# a cada execução - só quer os registros novos desde a última vez
# que rodou. Você usa uma coluna de timestamp como "watermark".
#
# TAREFA: dado uma lista de eventos (com campo 'timestamp', inteiro
# simulando epoch) e o último watermark processado, retorne uma
# tupla (novos_eventos, novo_watermark) - novos_eventos são só os
# com timestamp > watermark; novo_watermark é o maior timestamp
# entre os retornados (ou o watermark antigo, se não houver novos).

def read_incremental(events: list, last_watermark: int) -> tuple:
    pass

#%%
# Teste manual
eventos_demo = [{"id": 1, "timestamp": 100}, {"id": 2, "timestamp": 200}, {"id": 3, "timestamp": 150}]
print(read_incremental(eventos_demo, 120))

#%%
eventos = [{"id": 1, "timestamp": 100}, {"id": 2, "timestamp": 200}, {"id": 3, "timestamp": 150}]
novos, novo_wm = read_incremental(eventos, 120)
assert [e["id"] for e in novos] == [2, 3]
assert novo_wm == 200

novos2, novo_wm2 = read_incremental(eventos, 500)
assert novos2 == []
assert novo_wm2 == 500

#%%
# 4. Late arriving data - detectar e marcar pra reprocessamento
#
# CENÁRIO: um evento com data_evento de "ontem" chega no seu pipeline
# só "hoje de manhã" (atraso de rede, sistema de origem lento, etc).
# Se sua agregação diária já rodou pra ontem, esse dado atrasado fica
# de fora, a menos que você o detecte e sinalize a janela pra reprocessar.
#
# TAREFA: dado uma lista de eventos com 'timestamp_evento' e
# 'timestamp_chegada' (ambos epoch em segundos), e um threshold de
# atraso aceitável (em segundos), retorne a lista de eventos
# considerados "atrasados" (chegada - evento > threshold), e o
# conjunto de "janelas" afetadas (aqui simplificado: o dia, no
# formato de string 'YYYY-MM-DD', derivado do timestamp_evento via
# time.strftime).

import time as time_module

def detect_late_events(events: list, threshold_seconds: int) -> tuple:
    pass

#%%
# Teste manual - evento de ontem chegando bem depois
eventos_late_demo = [
    {"id": 1, "timestamp_evento": 1000, "timestamp_chegada": 1005},   # no prazo
    {"id": 2, "timestamp_evento": 1000, "timestamp_chegada": 90000},  # atrasado
]
print(detect_late_events(eventos_late_demo, threshold_seconds=3600))

#%%
eventos_late = [
    {"id": 1, "timestamp_evento": 1000, "timestamp_chegada": 1005},
    {"id": 2, "timestamp_evento": 1000, "timestamp_chegada": 90000},
]
late, windows = detect_late_events(eventos_late, threshold_seconds=3600)
assert [e["id"] for e in late] == [2]
assert len(windows) == 1

#%%
# 5. Hash join eficiente entre grandes volumes
#
# CENÁRIO: você precisa juntar uma tabela de "vendas" (milhões de
# linhas) com uma tabela de "produtos" (milhares de linhas) por
# produto_id. Um nested loop (O(n*m)) explode em tempo de execução.
#
# TAREFA: implemente um hash join - construa um dict (hash table) da
# tabela menor, depois percorra a maior UMA VEZ (O(n+m), não O(n*m)).
# Retorne a lista de vendas enriquecidas com o nome do produto.

def hash_join(vendas: list, produtos: list, join_key: str) -> list:
    pass

#%%
# Teste manual
vendas_demo2 = [{"venda_id": 1, "produto_id": 10, "valor": 50}, {"venda_id": 2, "produto_id": 20, "valor": 30}]
produtos_demo = [{"produto_id": 10, "nome": "Caneta"}, {"produto_id": 20, "nome": "Caderno"}]
print(hash_join(vendas_demo2, produtos_demo, "produto_id"))

#%%
vendas2 = [{"venda_id": 1, "produto_id": 10, "valor": 50}, {"venda_id": 2, "produto_id": 20, "valor": 30}]
produtos2 = [{"produto_id": 10, "nome": "Caneta"}, {"produto_id": 20, "nome": "Caderno"}]
result2 = hash_join(vendas2, produtos2, "produto_id")
assert result2[0]["nome"] == "Caneta"
assert result2[1]["nome"] == "Caderno"

#%%
# 6. Deduplicação com merge de campos (near-duplicate)
#
# CENÁRIO: duas fontes mandam o "mesmo" registro (mesma chave), mas
# cada uma preenche campos diferentes (uma tem telefone, outra tem
# email). Você não quer descartar nenhuma informação - quer MESCLAR
# os campos não-nulos das duplicatas numa versão consolidada.
#
# TAREFA: dado uma lista de registros com chave repetida, retorne uma
# lista com um registro por chave, mesclando campos: se um campo é
# None/ausente numa ocorrência mas presente em outra, usa o valor
# presente. Em caso de conflito real (ambos não-nulos e diferentes),
# mantenha o valor da ocorrência MAIS RECENTE (assuma que a lista já
# vem ordenada da mais antiga pra mais nova).

def merge_duplicates(records: list, key: str) -> list:
    pass

#%%
# Teste manual
regs_demo3 = [
    {"id": 1, "telefone": "111", "email": None},
    {"id": 1, "telefone": None, "email": "a@x.com"},
]
print(merge_duplicates(regs_demo3, "id"))

#%%
regs3 = [
    {"id": 1, "telefone": "111", "email": None},
    {"id": 1, "telefone": None, "email": "a@x.com"},
]
result3 = merge_duplicates(regs3, "id")
assert len(result3) == 1
assert result3[0]["telefone"] == "111"
assert result3[0]["email"] == "a@x.com"