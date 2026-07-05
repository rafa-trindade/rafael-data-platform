#%%
# =========================================================
# PYTHON DRILL - NÍVEL SÊNIOR
# Complexidade, heaps, sliding window, two pointers,
# grafos, union-find, DP aplicada, design leve
# =========================================================

#%%
# 1. Big-O - análise (conceitual, sem código pra rodar)
#
# Compare as duas funções abaixo e responda nos comentários:
# a) Qual a complexidade de tempo de cada uma?
# b) Qual a complexidade de espaço de cada uma?
# c) Para uma lista com 1 milhão de elementos, qual você escolheria e por quê?
#
# def tem_duplicado_v1(nums):
#     for i in range(len(nums)):
#         for j in range(i + 1, len(nums)):
#             if nums[i] == nums[j]:
#                 return True
#     return False
#
# def tem_duplicado_v2(nums):
#     vistos = set()
#     for n in nums:
#         if n in vistos:
#             return True
#         vistos.add(n)
#     return False
#
# Sua resposta:
#


#%%
# 2. Árvore binária - inserir e percorrer in-order
# Implemente uma árvore de busca binária (BST) com insert e um
# percurso in-order (deve retornar os valores em ordem crescente).

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        pass

    def in_order(self) -> list:
        pass

#%%
# Teste manual
bst_demo = BST()
for v in [5, 3, 8, 1, 4, 7, 9]:
    bst_demo.insert(v)
print(bst_demo.in_order())

#%%
bst = BST()
for v in [5, 3, 8, 1, 4, 7, 9]:
    bst.insert(v)
assert bst.in_order() == [1, 3, 4, 5, 7, 8, 9]

#%%
# 3. Árvore binária - BFS (percurso por nível)
# Usando a BST do exercício 2, implemente um percurso em largura
# (level order), retornando uma lista de listas (um sublista por nível).

def level_order(root: TreeNode) -> list:
    pass

#%%
# Teste manual
bst2_demo = BST()
for v in [5, 3, 8, 1, 4]:
    bst2_demo.insert(v)
print(level_order(bst2_demo.root))

#%%
bst2 = BST()
for v in [5, 3, 8, 1, 4]:
    bst2.insert(v)
assert level_order(bst2.root) == [[5], [3, 8], [1, 4]]

#%%
# 4. Top-K com heap
# Dado uma lista de registros (dicts com 'nome' e 'valor'), retorne
# os K registros com maior 'valor', SEM ordenar a lista inteira
# (use o módulo heapq - heapq.nlargest, ou implemente com heapify+heappush).
#
# Cenário real: "top 5 clientes por faturamento" numa lista de milhões
# de registros - ordenar tudo é O(n log n) e desperdiça memória;
# um heap de tamanho K resolve em O(n log k).

import heapq

def top_k(records: list, k: int) -> list:
    pass

#%%
# Teste manual
dados_demo = [
    {"nome": "A", "valor": 100}, {"nome": "B", "valor": 500},
    {"nome": "C", "valor": 50}, {"nome": "D", "valor": 900},
    {"nome": "E", "valor": 300},
]
print(top_k(dados_demo, 2))

#%%
dados = [
    {"nome": "A", "valor": 100}, {"nome": "B", "valor": 500},
    {"nome": "C", "valor": 50}, {"nome": "D", "valor": 900},
    {"nome": "E", "valor": 300},
]
result = top_k(dados, 2)
assert [r["nome"] for r in result] == ["D", "B"]

#%%
# 5. Merge K Sorted Lists (k-way merge)
# Dado uma lista de listas, cada uma já ORDENADA, retorne uma única
# lista ordenada com todos os elementos (use heapq pra fazer o merge
# eficiente, sem concatenar tudo e ordenar de novo).
#
# Cenário real: merge de N arquivos/partições já ordenadas (compaction
# de arquivos Parquet particionados, merge de shards de um índice).

def merge_k_sorted(lists: list) -> list:
    pass

#%%
# Teste manual
print(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]))

#%%
assert merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert merge_k_sorted([[1, 2], [], [3]]) == [1, 2, 3]
assert merge_k_sorted([]) == []

#%%
# 6. Sliding Window - soma máxima de subarray de tamanho fixo
# Dado uma lista de números e um tamanho de janela k, retorne a
# maior soma possível de uma janela contígua de tamanho k.
# Faça em O(n), sem recalcular a soma da janela do zero a cada posição.
#
# Cenário real: agregação móvel sobre uma janela de tempo fixa
# (ex: "maior faturamento em qualquer janela de 7 dias consecutivos").

def max_sum_window(nums: list, k: int) -> int:
    pass

#%%
# Teste manual
print(max_sum_window([2, 1, 5, 1, 3, 2], 3))

#%%
assert max_sum_window([2, 1, 5, 1, 3, 2], 3) == 9  # janela [5,1,3]
assert max_sum_window([1, 1, 1, 1], 2) == 2
assert max_sum_window([5], 1) == 5

#%%
# 7. Sliding Window - maior janela sem repetição
# Dado uma string, retorne o TAMANHO da maior substring sem
# caracteres repetidos, usando janela deslizante (dois ponteiros),
# não força bruta.

def longest_unique_substring(s: str) -> int:
    pass

#%%
# Teste manual
print(longest_unique_substring("abcabcbb"))

#%%
assert longest_unique_substring("abcabcbb") == 3  # "abc"
assert longest_unique_substring("bbbbb") == 1
assert longest_unique_substring("") == 0

#%%
# 8. Two Pointers - par com soma alvo em lista ORDENADA
# Dado uma lista ORDENADA e um alvo, retorne True se existir um par
# de elementos que somam o alvo. Use dois ponteiros (início e fim),
# não força bruta O(n²).

def has_pair_with_sum(nums: list, target: int) -> bool:
    pass

#%%
# Teste manual
print(has_pair_with_sum([1, 2, 4, 7, 11, 15], 15))

#%%
assert has_pair_with_sum([1, 2, 4, 7, 11, 15], 15) == True
assert has_pair_with_sum([1, 2, 4, 7, 11, 15], 100) == False
assert has_pair_with_sum([], 5) == False

#%%
# 9. Two Pointers - remover duplicados de lista ordenada in-place
# Dado uma lista ORDENADA com duplicados, remova-os IN-PLACE
# (sem criar uma lista nova) e retorne o novo tamanho lógico.
# Cenário real: dedup de um stream já ordenado por chave, sem
# alocar memória extra proporcional ao tamanho da entrada.

def remove_duplicates_sorted_inplace(nums: list) -> int:
    pass

#%%
# Teste manual
nums_demo = [1, 1, 2, 2, 2, 3, 4, 4]
n_demo = remove_duplicates_sorted_inplace(nums_demo)
print(n_demo, nums_demo[:n_demo])

#%%
nums_test = [1, 1, 2, 2, 2, 3, 4, 4]
n = remove_duplicates_sorted_inplace(nums_test)
assert n == 4
assert nums_test[:n] == [1, 2, 3, 4]

#%%
# 10. Coin change (única DP mantida - a mais aplicável em entrevista de DE)
# Dado um valor alvo e uma lista de moedas disponíveis (quantidade
# ilimitada de cada), retorne o número MÍNIMO de moedas pra formar
# o valor. Se não for possível, retorne -1.

def coin_change(coins: list, amount: int) -> int:
    pass

#%%
# Teste manual
print(coin_change([1, 2, 5], 11))
print(coin_change([2], 3))

#%%
assert coin_change([1, 2, 5], 11) == 3
assert coin_change([2], 3) == -1
assert coin_change([1], 0) == 0

#%%
# 11. Hash map do zero (com tratamento de colisão)
# Implemente um hash map simples com chaining (lista de buckets,
# cada bucket é uma lista de pares chave-valor).

class SimpleHashMap:
    def __init__(self, size=16):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key) -> int:
        return hash(key) % self.size

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def delete(self, key):
        pass

#%%
# Teste manual
hm_demo = SimpleHashMap(size=4)
hm_demo.put("a", 1)
hm_demo.put("b", 2)
print(hm_demo.get("a"))
hm_demo.delete("a")
print(hm_demo.get("a"))

#%%
hm = SimpleHashMap(size=4)
hm.put("a", 1)
hm.put("b", 2)
hm.put("a", 10)
assert hm.get("a") == 10
assert hm.get("b") == 2
hm.delete("a")
assert hm.get("a") is None

#%%
# 12. LRU Cache
# Implemente um cache com capacidade fixa que remove o item usado
# menos recentemente quando a capacidade é excedida.

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity

    def get(self, key):
        pass

    def put(self, key, value):
        pass

#%%
# Teste manual
cache_demo = LRUCache(2)
cache_demo.put(1, "a")
cache_demo.put(2, "b")
cache_demo.put(3, "c")
print(cache_demo.get(2))
print(cache_demo.get(3))

#%%
cache = LRUCache(2)
cache.put(1, "a")
cache.put(2, "b")
assert cache.get(1) == "a"
cache.put(3, "c")
assert cache.get(2) is None
assert cache.get(3) == "c"

#%%
# 13. Grafo - detectar ciclo
# Dado um grafo direcionado representado como lista de adjacência
# (dict), detecte se existe ciclo.

def has_cycle_graph(graph: dict) -> bool:
    pass

#%%
# Teste manual
print(has_cycle_graph({"a": ["b"], "b": ["c"], "c": ["a"]}))
print(has_cycle_graph({"a": ["b"], "b": ["c"], "c": []}))

#%%
graph_with_cycle = {"a": ["b"], "b": ["c"], "c": ["a"]}
graph_no_cycle = {"a": ["b"], "b": ["c"], "c": []}
assert has_cycle_graph(graph_with_cycle) == True
assert has_cycle_graph(graph_no_cycle) == False

#%%
# 14. Grafo - caminho mais curto (BFS)
# Dado um grafo não-ponderado (lista de adjacência), retorne o
# número de arestas do caminho mais curto entre origem e destino.
# Se não houver caminho, retorne -1.

def shortest_path(graph: dict, start: str, end: str) -> int:
    pass

#%%
# Teste manual
g_demo = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": []}
print(shortest_path(g_demo, "a", "e"))

#%%
g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": []}
assert shortest_path(g, "a", "e") == 3
assert shortest_path(g, "a", "a") == 0
assert shortest_path(g, "e", "a") == -1

#%%
# 15. Union-Find - resolução de entidades / dedup transitivo
# Cenário real: você tem pares de registros considerados "o mesmo
# cliente" (ex: mesmo CPF, ou mesmo email), mas essas relações são
# transitivas - se A~B e B~C, então A, B e C são a mesma entidade,
# mesmo que A e C nunca tenham sido comparados diretamente.
#
# Implemente Union-Find (com union por rank ou union simples) e uma
# função que, dado uma lista de pares equivalentes, retorna os grupos
# finais (cada grupo = um conjunto de IDs que são a mesma entidade).

class UnionFind:
    def __init__(self, ids: list):
        self.parent = {i: i for i in ids}

    def find(self, x):
        pass

    def union(self, x, y):
        pass

def resolve_entities(ids: list, pairs: list) -> list:
    """Retorna uma lista de grupos (cada grupo é uma lista de ids)."""
    pass

#%%
# Teste manual
ids_demo = ["A", "B", "C", "D", "E"]
pairs_demo = [("A", "B"), ("B", "C"), ("D", "E")]
print(resolve_entities(ids_demo, pairs_demo))

#%%
ids_test = ["A", "B", "C", "D", "E"]
pairs_test = [("A", "B"), ("B", "C"), ("D", "E")]
groups = resolve_entities(ids_test, pairs_test)
groups_as_sets = sorted([sorted(g) for g in groups])
assert groups_as_sets == [["A", "B", "C"], ["D", "E"]]

#%%
# 16. Rate limiter simples (fixed window)
# Implemente um rate limiter que permite no máximo `max_requests`
# chamadas por `window_seconds`. allow() retorna True se a chamada
# for permitida, False se exceder o limite na janela atual.

import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.window_start = time.time()
        self.count = 0

    def allow(self) -> bool:
        pass

#%%
# Teste manual
rl_demo = RateLimiter(max_requests=2, window_seconds=1)
print(rl_demo.allow())
print(rl_demo.allow())
print(rl_demo.allow())

#%%
rl = RateLimiter(max_requests=2, window_seconds=1)
assert rl.allow() == True
assert rl.allow() == True
assert rl.allow() == False
time.sleep(1.1)
assert rl.allow() == True