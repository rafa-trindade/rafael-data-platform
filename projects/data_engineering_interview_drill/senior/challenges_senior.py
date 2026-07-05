#%%
# =========================================================
# DATA ENGINEERING INTERVIEW DRILL - NÍVEL SÊNIOR
# Schema evolution, formatos de arquivo, checkpoint/resume,
# data quality gate, mini-orquestração
# =========================================================

#%%
# 1. Schema evolution - normalizar registros heterogêneos
#
# CENÁRIO: sua tabela de origem evoluiu ao longo do tempo. Registros
# antigos não têm o campo 'categoria' (adicionado depois). Um campo
# antigo 'preco_str' (string) foi substituído por 'preco' (float).
# Você precisa normalizar tudo pro schema ATUAL antes de carregar.
#
# TAREFA: implemente normalize_schema(records, target_schema) onde
# target_schema é um dict {campo: valor_default}. Para cada registro,
# preencha campos faltantes com o default do target_schema, e ignore
# campos extras que não estão no target_schema (schema evolution
# "forward compatible": campos antigos obsoletos são descartados,
# campos novos ganham default).

def normalize_schema(records: list, target_schema: dict) -> list:
    result = []
    for r in records:
        normalized = {}
        for field, default in target_schema.items():
            normalized[field] = r.get(field, default)
        result.append(normalized)
    return result

#%%
# Teste manual
target_demo = {"id": None, "nome": "", "categoria": "desconhecida", "preco": 0.0}
regs_demo = [
    {"id": 1, "nome": "A", "preco_str": "10.50"},  # sem categoria, campo obsoleto preco_str
    {"id": 2, "nome": "B", "categoria": "eletronicos", "preco": 99.9},
]
print(normalize_schema(regs_demo, target_demo))

#%%
target = {"id": None, "nome": "", "categoria": "desconhecida", "preco": 0.0}
regs = [
    {"id": 1, "nome": "A", "preco_str": "10.50"},
    {"id": 2, "nome": "B", "categoria": "eletronicos", "preco": 99.9},
]
result = normalize_schema(regs, target)
assert result[0]["categoria"] == "desconhecida"
assert result[0]["preco"] == 0.0
assert "preco_str" not in result[0]
assert result[1]["categoria"] == "eletronicos"

#%%
# 2. Escolha de formato de arquivo (cenário, resposta em comentário)
#
# CENÁRIO: você precisa decidir o formato de armazenamento pra três
# casos diferentes:
#
# a) Camada bronze de um data lake, ingestão bruta, schema muda com
#    frequência, precisa de leitura ocasional linha a linha.
# b) Camada gold, consumida por dashboards de BI que fazem agregações
#    pesadas em poucas colunas de tabelas com centenas de colunas.
# c) Uma tabela que recebe UPDATEs e DELETEs frequentes vindos de CDC,
#    e precisa suportar "time travel" (consultar como estava ontem).
#
# Para cada caso, escreva nos comentários abaixo: qual formato você
# escolheria entre CSV/JSON, Parquet, Avro, e um formato de tabela
# aberta (Iceberg/Delta Lake) - e por quê.
#
# Sua resposta:
# a)
# b)
# c)


#%%
# 3. Reprocessamento com checkpoint (falha parcial)
#
# CENÁRIO: seu pipeline processa uma lista de 1000 arquivos. Ele
# falha no arquivo 601 (rede caiu). Reprocessar os 600 primeiros de
# novo é caro e desnecessário - você quer retomar exatamente de onde
# parou.
#
# TAREFA: implemente process_with_checkpoint(items, process_fn,
# checkpoint) onde checkpoint é um dict mutável {'last_processed': -1}.
# A função processa os itens em ordem a partir de checkpoint['last_processed']+1,
# atualizando o checkpoint após CADA item processado com sucesso.
# Se process_fn levantar exceção num item, a função deve parar
# (sem processar os seguintes) e deixar o checkpoint no último
# item processado com sucesso, permitindo retomar depois.

def process_with_checkpoint(items: list, process_fn, checkpoint: dict) -> list:
    pass

#%%
# Teste manual - simula falha no item de índice 2
def process_fn_demo(item):
    if item == "C":
        raise ValueError("falhou")
    return item.lower()

checkpoint_demo = {"last_processed": -1}
try:
    process_with_checkpoint(["A", "B", "C", "D"], process_fn_demo, checkpoint_demo)
except ValueError:
    pass
print(checkpoint_demo)

# retomar depois da falha corrigida
def process_fn_demo_fixed(item):
    return item.lower()

result_demo = process_with_checkpoint(["A", "B", "C", "D"], process_fn_demo_fixed, checkpoint_demo)
print(result_demo, checkpoint_demo)

#%%
def process_fn(item):
    if item == "C":
        raise ValueError("falhou")
    return item.lower()

checkpoint = {"last_processed": -1}
try:
    process_with_checkpoint(["A", "B", "C", "D"], process_fn, checkpoint)
    assert False, "deveria ter levantado exceção"
except ValueError:
    pass
assert checkpoint["last_processed"] == 1  # processou índices 0 e 1 (A, B) com sucesso

def process_fn_fixed(item):
    return item.lower()

result = process_with_checkpoint(["A", "B", "C", "D"], process_fn_fixed, checkpoint)
assert result == ["c", "d"]  # retomou de onde parou
assert checkpoint["last_processed"] == 3

#%%
# 4. Data Quality Gate configurável
#
# CENÁRIO: antes de promover dados de staging pra um schema
# confiável, você quer rodar um conjunto de regras de qualidade
# configuráveis, e bloquear a promoção se alguma regra falhar
# acima de um threshold de tolerância.
#
# TAREFA: implemente run_quality_gate(records, rules, fail_threshold)
# onde rules é uma lista de funções (cada uma recebe um registro e
# retorna True/False), e fail_threshold é a fração máxima aceitável
# de falhas (ex: 0.05 = 5%). Retorne um dict:
# {'passed': bool, 'failure_rate': float, 'failed_records': list}

def run_quality_gate(records: list, rules: list, fail_threshold: float) -> dict:
    pass

#%%
# Teste manual
regs_demo4 = [{"id": 1, "valor": 10}, {"id": 2, "valor": -5}, {"id": 3, "valor": 20}]
rule_positivo = lambda r: r["valor"] >= 0
print(run_quality_gate(regs_demo4, [rule_positivo], fail_threshold=0.5))
print(run_quality_gate(regs_demo4, [rule_positivo], fail_threshold=0.1))

#%%
regs4 = [{"id": 1, "valor": 10}, {"id": 2, "valor": -5}, {"id": 3, "valor": 20}]
rule = lambda r: r["valor"] >= 0
report_ok = run_quality_gate(regs4, [rule], fail_threshold=0.5)
assert report_ok["passed"] == True
assert len(report_ok["failed_records"]) == 1

report_fail = run_quality_gate(regs4, [rule], fail_threshold=0.1)
assert report_fail["passed"] == False

#%%
# 5. Mini-orquestração ETL com tratamento de erro por etapa
#
# CENÁRIO: seu ETL tem 3 etapas (extract, transform, load). Se uma
# etapa falhar, você quer saber EXATAMENTE em qual etapa parou, sem
# que o erro de uma etapa derrube o processo de forma silenciosa ou
# sem contexto.
#
# TAREFA: implemente run_etl(extract_fn, transform_fn, load_fn) que
# executa as três em sequência, e se qualquer uma falhar, capture a
# exceção e retorne um dict {'success': False, 'failed_stage': str,
# 'error': str}. Se tudo funcionar, retorne {'success': True,
# 'result': <retorno do load_fn>}.

def run_etl(extract_fn, transform_fn, load_fn) -> dict:
    pass

#%%
# Teste manual - transform falha
def extract_demo():
    return [1, 2, 3]

def transform_fail_demo(data):
    raise RuntimeError("transformação inválida")

def load_demo(data):
    return f"carregado {len(data)} registros"

print(run_etl(extract_demo, transform_fail_demo, load_demo))

#%%
def extract():
    return [1, 2, 3]

def transform_ok(data):
    return [x * 2 for x in data]

def transform_fail(data):
    raise RuntimeError("transformação inválida")

def load(data):
    return f"carregado {len(data)} registros"

result_ok = run_etl(extract, transform_ok, load)
assert result_ok == {"success": True, "result": "carregado 3 registros"}

result_fail = run_etl(extract, transform_fail, load)
assert result_fail["success"] == False
assert result_fail["failed_stage"] == "transform"