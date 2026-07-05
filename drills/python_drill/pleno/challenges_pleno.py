#%%
# =========================================================
# PYTHON DRILL - NÍVEL PLENO
# Estruturas de dados e algoritmos clássicos
# =========================================================

#%%
# 1. Pilha (Stack) do zero
# Implemente uma pilha usando uma lista Python como armazenamento interno,
# com push, pop e peek. pop/peek em pilha vazia deve levantar IndexError.

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        pass

    def pop(self):
        pass

    def peek(self):
        pass

    def is_empty(self) -> bool:
        pass

#%%
# Teste manual
s = Stack()
s.push(1)
s.push(2)
print(s.peek())
print(s.pop())
print(s.is_empty())

#%%
s2 = Stack()
s2.push(1)
s2.push(2)
assert s2.peek() == 2
assert s2.pop() == 2
assert s2.pop() == 1
assert s2.is_empty() == True

#%%
# 2. Parênteses balanceados (usa a Stack acima)
# Verifique se uma string de parênteses/chaves/colchetes está balanceada.

def is_balanced(s: str) -> bool:
    pass

#%%
# Teste manual
print(is_balanced("({[]})"))
print(is_balanced("([)]"))

#%%
assert is_balanced("({[]})") == True
assert is_balanced("([)]") == False
assert is_balanced("") == True
assert is_balanced("(()") == False

#%%
# 3. Fila (Queue) do zero
# Implemente uma fila com enqueue e dequeue (FIFO), usando uma lista.

class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        pass

    def dequeue(self):
        pass

    def is_empty(self) -> bool:
        pass

#%%
# Teste manual
q = Queue()
q.enqueue("a")
q.enqueue("b")
print(q.dequeue())
print(q.dequeue())

#%%
q2 = Queue()
q2.enqueue("a")
q2.enqueue("b")
assert q2.dequeue() == "a"
assert q2.dequeue() == "b"
assert q2.is_empty() == True

#%%
# 4. Busca binária
# Implemente busca binária iterativa numa lista ORDENADA.
# Retorne o índice do elemento, ou -1 se não encontrado.

def binary_search(nums: list, target: int) -> int:
    pass

#%%
# Teste manual
print(binary_search([1, 3, 5, 7, 9, 11], 7))
print(binary_search([1, 3, 5, 7, 9, 11], 4))

#%%
assert binary_search([1, 3, 5, 7, 9, 11], 7) == 3
assert binary_search([1, 3, 5, 7, 9, 11], 4) == -1
assert binary_search([], 1) == -1

#%%
# 5. Bubble sort
# Implemente o bubble sort manualmente (sem usar sorted() ou .sort()).

def bubble_sort(nums: list) -> list:
    pass

#%%
# Teste manual
print(bubble_sort([5, 2, 9, 1, 5, 6]))

#%%
assert bubble_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
assert bubble_sort([]) == []
assert bubble_sort([1]) == [1]

#%%
# 6. Insertion sort
# Implemente o insertion sort manualmente.

def insertion_sort(nums: list) -> list:
    pass

#%%
# Teste manual
print(insertion_sort([5, 2, 9, 1, 5, 6]))

#%%
assert insertion_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
assert insertion_sort([3, 1]) == [1, 3]

#%%
# 7. Linked List - inverter
# Implemente uma lista encadeada simples e uma função que a inverte.

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def build_linked_list(values: list) -> Node:
    head = None
    tail = None
    for v in values:
        node = Node(v)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head

def linked_list_to_list(head: Node) -> list:
    result = []
    while head:
        result.append(head.value)
        head = head.next
    return result

def reverse_linked_list(head: Node) -> Node:
    pass

#%%
# Teste manual
ll_demo = build_linked_list([1, 2, 3, 4])
print(linked_list_to_list(reverse_linked_list(ll_demo)))

#%%
ll = build_linked_list([1, 2, 3, 4])
reversed_ll = reverse_linked_list(ll)
assert linked_list_to_list(reversed_ll) == [4, 3, 2, 1]

#%%
# 8. Linked List - detectar ciclo
# Usando a classe Node acima, detecte se uma lista encadeada tem ciclo
# (algoritmo de Floyd, dois ponteiros).

def has_cycle(head: Node) -> bool:
    pass

#%%
# Teste manual
print(has_cycle(build_linked_list([1, 2, 3])))

#%%
ll_no_cycle = build_linked_list([1, 2, 3])
assert has_cycle(ll_no_cycle) == False

n1, n2, n3 = Node(1), Node(2), Node(3)
n1.next = n2
n2.next = n3
n3.next = n2
assert has_cycle(n1) == True

#%%
# 9. Anagrama
# Verifique se duas strings são anagramas (mesmas letras, mesma quantidade).

def is_anagram(a: str, b: str) -> bool:
    pass

#%%
# Teste manual
print(is_anagram("roma", "amor"))
print(is_anagram("python", "java"))

#%%
assert is_anagram("roma", "amor") == True
assert is_anagram("python", "java") == False
assert is_anagram("", "") == True

#%%
# 10. Permutações de uma lista
# Gere todas as permutações possíveis de uma lista (recursivo,
# sem usar itertools.permutations).

def permutations(nums: list) -> list:
    pass

#%%
# Teste manual
print(permutations([1, 2, 3]))

#%%
result = permutations([1, 2, 3])
assert len(result) == 6
assert [1, 2, 3] in result
assert [3, 2, 1] in result

#%%
# 11. Torre de Hanói
# Retorne o número mínimo de movimentos para resolver a Torre de Hanói
# com n discos (implemente via recursão real, contando os movimentos).

def hanoi_moves(n: int) -> int:
    pass

#%%
# Teste manual
print(hanoi_moves(3))

#%%
assert hanoi_moves(1) == 1
assert hanoi_moves(3) == 7
assert hanoi_moves(4) == 15

#%%
# 12. Merge de duas listas ordenadas
# Combine duas listas já ordenadas em uma única lista ordenada,
# sem usar sorted() no resultado final (faça o merge manual, O(n+m)).

def merge_sorted_lists(a: list, b: list) -> list:
    pass

#%%
# Teste manual
print(merge_sorted_lists([1, 3, 5], [2, 4, 6]))

#%%
assert merge_sorted_lists([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
assert merge_sorted_lists([], [1, 2]) == [1, 2]
assert merge_sorted_lists([1, 2], []) == [1, 2]