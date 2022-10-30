"""
Módulo de ejercicios Práctica 0
"""

import re

def CribaDeErastotenes(n):
    """Imprime los números primos anteriores a n siguiendo 
    el algoritmo de Criba de Erastótenes"""
    
    # Crear una lista de booleanos
    # y iniciarlos a todos como True
    # Al final, los elementos no primos 
    # serán False

    prime = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):

        # Si prime[p] no ha cambiado
        # entonces es primo
        if (prime[p] == True):

            # Actualizamos todos los múltiplos de p
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1

    # Imprimir todos los primos anteriores a n.
    for p in range(2, n+1):
        if prime[p]:
            print(p)

def fibonacci(n):
    """Algoritmo iterativo n-ésimo elemento de la sucesión de fibonacci"""

    if n == 0: return 0
    if n == 1: return 1

    prevPrev = 0
    prev = 1
    for i in range(1, n):
        currentNumber = prevPrev + prev
        prevPrev = prev
        prev = currentNumber
    return currentNumber


def parentesisBalanceados(expr):
    """
    Compruba sin la expresión tiene los paréntesis blanaceados. 
    (()()) => True
    )( => False
    """

    stack = []
    for char in expr:
        if char == '(':
            stack.append('(')
        if char == ')':
            if stack: stack.pop()
    return not stack

def palabraEspacioMayuscula(texto):
    """
    Identificar cualquier palabra seguida de un espacio y una única letra
    mayúscula (por ejemplo: Apellido N).
    """
    return re.findall(r"\w+ [A-Z](?=\s|$)", texto)

def identificarEmails(texto):
    """
    Identificar correos electrónicos válidos
    """

    # No hay distinción entre mayúsculas y minúsculas
    # Se permiten como carácteres extraños . y _
    expr = r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"
    return re.findall(expr, texto)

def identificarTarjeta(texto):
    """
    Identificar números de tarjeta de crédito cuyos dígitos estén separados 
    por - o espacios en blanco cada paquete de cuatro dígitos: 
        1234-5678-9012-3456 ó  1234 5678 9012 3456. 
    """

    expr = r"(?:[\s-]?[0-9]){16}"
    return re.findall(expr, texto)
