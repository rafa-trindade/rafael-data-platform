#%%
# =========================================================
# PYTHON DRILL - NÍVEL SÊNIOR
# Complexidade, árvores, grafos, DP, design de sistema leve
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
# 4. Árvore balanceada
# Verifique se uma árvore binária é balanceada (a diferença de altura
# entre subárvore esquerda e direita de qualquer nó é <= 1).

def is_balanced(root: TreeNode) -> bool:
    pass

#%%
# Teste manual
balanced_demo = BST()
for v in [5, 3, 8]:
    balanced_demo.insert(v)
print(is_balanced(balanced_demo.root))

#%%
balanced = BST()
for v in [5, 3, 8]:
    balanced.insert(v)
assert is_balanced(balanced.root) == True

unbalanced_root = TreeNode(1)
unbalanced_root.left = TreeNode(2)
unbalanced_root.left.left = TreeNode(3)
unbalanced_root.left.left.left = TreeNode(4)
assert is_balanced(unbalanced_root) == False

#%%
# 5. Subsequência comum máxima (LCS) - programação dinâmica
# Retorne o TAMANHO da maior subsequência comum entre duas strings.

def lcs_length(a: str, b: str) -> int:
    pass

#%%
# Teste manual
print(lcs_length("abcde", "ace"))

#%%
assert lcs_length("abcde", "ace") == 3
assert lcs_length("abc", "abc") == 3
assert lcs_length("abc", "xyz") == 0

#%%
# 6. Problema da mochila (Knapsack 0/1)
# Dado pesos, valores e uma capacidade máxima, retorne o valor máximo
# que pode ser carregado sem exceder a capacidade (cada item só pode
# ser usado uma vez).

def knapsack(weights: list, values: list, capacity: int) -> int:
    pass

#%%
# Teste manual
print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))

#%%
assert knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
assert knapsack([2, 3], [3, 4], 1) == 0

#%%
# 7. Coin change
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
# 8. Hash map do zero (com tratamento de colisão)
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
# 9. LRU Cache
# Implemente um cache com capacidade fixa que remove o item usado
# menos recentemente quando a capacidade é excedida.
# (Pode usar collections.OrderedDict, mas entenda o mecanismo por trás.)

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
# 10. Grafo - detectar ciclo
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
# 11. Grafo - caminho mais curto (BFS)
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
# 12. Rate limiter simples (fixed window)
# Implemente um rate limiter que permite no máximo `max_requests`
# chamadas por `window_seconds`. allow() retorna True se a chamada
# for permitida, False se exceder o limite na janela atual.
# Dica: use time.time() para controlar a janela.

import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

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