"""calculadora.py

Módulo simples que fornece funções básicas de cálculo.

Funções disponíveis:
- add(a, b)
- sub(a, b)
- mul(a, b)
- div(a, b)  # Levanta ZeroDivisionError se b for zero

Também inclui uma classe Calculator que encapsula essas operações.
"""

def add(a, b):
    """Retorna a soma de a e b."""
    return a + b


def sub(a, b):
    """Retorna a subtração de b de a (a - b)."""
    return a - b


def mul(a, b):
    """Retorna a multiplicação de a por b."""
    return a * b


def div(a, b):
    """Retorna a divisão de a por b.

    Levanta ZeroDivisionError se b for zero.
    """
    if b == 0:
        raise ZeroDivisionError("Divisão por zero não é permitida.")
    return a / b


class Calculator:
    """Classe simples que oferece métodos de cálculo.

    Exemplo de uso:
        calc = Calculator()
        result = calc.add(2, 3)
    """

    def add(self, a, b):
        return add(a, b)

    def sub(self, a, b):
        return sub(a, b)

    def mul(self, a, b):
        return mul(a, b)

    def div(self, a, b):
        return div(a, b)
