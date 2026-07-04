#%%
# =========================================================
# PYTHON DRILL - NÍVEL JUNIOR
# Fundamentos de lógica, string e lista
# =========================================================

#%%
# 1. Palíndromo
# Escreva uma função que verifica se uma string é um palíndromo
# (ignorando maiúsculas/minúsculas e espaços).

def is_palindrome(s: str) -> bool:
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

#%%
# Teste manual
print(is_palindrome("arara"))
print(is_palindrome("Roma"))

#%%
assert is_palindrome("arara") == True
assert is_palindrome("Roma") == False
assert is_palindrome("A mala nada na lama") == True
assert is_palindrome("") == True

#%%
# 2. Número primo
# Escreva uma função que verifica se um número é primo.

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

#%%
# Teste manual
print(is_prime(17))
print(is_prime(15))

#%%
assert is_prime(2) == True
assert is_prime(17) == True
assert is_prime(1) == False
assert is_prime(0) == False
assert is_prime(15) == False

#%%
# 3. Fibonacci
# Escreva uma função iterativa (sem recursão) que retorna o n-ésimo
# número da sequência de Fibonacci (0, 1, 1, 2, 3, 5, 8, ...).

def fibonacci(n: int) -> int:
    pass

#%%
# Teste manual
print(fibonacci(6))
print(fibonacci(10))

#%%
assert fibonacci(0) == 0
assert fibonacci(1) == 1
assert fibonacci(6) == 8
assert fibonacci(10) == 55

#%%
# 4. Fatorial
# Escreva uma função que calcula o fatorial de um número (sem usar math.factorial).

def factorial(n: int) -> int:
    pass

#%%
# Teste manual
print(factorial(5))

#%%
assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120

#%%
# 5. Contar vogais
# Escreva uma função que conta quantas vogais existem em uma string.

def count_vowels(s: str) -> int:
    pass

#%%
# Teste manual
print(count_vowels("engenharia de dados"))

#%%
assert count_vowels("engenharia de dados") == 8
assert count_vowels("xyz") == 0
assert count_vowels("AEIOU") == 5

#%%
# 6. Inverter string sem slicing
# Inverta uma string SEM usar s[::-1] ou reversed().

def reverse_string(s: str) -> str:
    pass

#%%
# Teste manual
print(reverse_string("python"))

#%%
assert reverse_string("python") == "nohtyp"
assert reverse_string("") == ""
assert reverse_string("a") == "a"

#%%
# 7. FizzBuzz
# Retorne uma lista de 1 a n. Múltiplos de 3 vira "Fizz", de 5 vira "Buzz",
# de ambos vira "FizzBuzz", os demais permanecem como número (int).

def fizzbuzz(n: int) -> list:
    pass

#%%
# Teste manual
print(fizzbuzz(15))

#%%
assert fizzbuzz(15) == [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
                         11, "Fizz", 13, 14, "FizzBuzz"]

#%%
# 8. Maior valor sem max()
# Encontre o maior valor de uma lista SEM usar a função max().

def find_max(nums: list) -> int:
    pass

#%%
# Teste manual
print(find_max([3, 7, 2, 9, 4]))

#%%
assert find_max([3, 7, 2, 9, 4]) == 9
assert find_max([-5, -1, -10]) == -1
assert find_max([42]) == 42

#%%
# 9. Remover duplicados sem set()
# Remova valores duplicados de uma lista, preservando a ordem original,
# SEM usar set().

def remove_duplicates(nums: list) -> list:
    pass

#%%
# Teste manual
print(remove_duplicates([1, 2, 2, 3, 1, 4]))

#%%
assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]
assert remove_duplicates([]) == []
assert remove_duplicates([5, 5, 5]) == [5]

#%%
# 10. Two Sum
# Dado uma lista de números e um alvo, retorne os ÍNDICES dos dois
# elementos que somam o alvo. Assuma que existe exatamente uma solução.

def two_sum(nums: list, target: int) -> tuple:
    pass

#%%
# Teste manual
print(two_sum([2, 7, 11, 15], 9))

#%%
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)
assert two_sum([3, 3], 6) == (0, 1)

#%%
# 11. Contar frequência de caracteres sem Counter
# Retorne um dicionário com a contagem de cada caractere na string,
# SEM usar collections.Counter.

def char_frequency(s: str) -> dict:
    pass

#%%
# Teste manual
print(char_frequency("banana"))

#%%
assert char_frequency("banana") == {"b": 1, "a": 3, "n": 2}
assert char_frequency("") == {}

#%%
# 12. Lista ordenada
# Verifique se uma lista está em ordem crescente, SEM usar sorted()
# para comparar.

def is_sorted(nums: list) -> bool:
    pass

#%%
# Teste manual
print(is_sorted([1, 2, 3, 4]))
print(is_sorted([1, 3, 2]))

#%%
assert is_sorted([1, 2, 3, 4]) == True
assert is_sorted([1, 3, 2]) == False
assert is_sorted([]) == True
assert is_sorted([5]) == True