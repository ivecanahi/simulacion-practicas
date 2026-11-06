"""Modelo: Generador Congruencial Lineal (LCG) y pruebas estadísticas."""
from math import gcd

A = 1664525
C = 1013904223
M = 2**32
SEED = 12345

# Valor crítico de chi-cuadrado con alfa = 0.05 para 9 grados de libertad (10 intervalos).
CHI2_CRITICAL_9_DF = 16.919


class LCG:
    """X(n+1) = (a·X(n) + c) mod m;  U(n) = X(n) / m."""

    def __init__(self, seed=SEED, a=A, c=C, m=M):
        if m <= 0:
            raise ValueError("m debe ser mayor que 0")
        if not (0 <= a < m and 0 <= c < m):
            raise ValueError("a y c deben estar en [0, m)")
        if not 0 <= seed < m:
            raise ValueError("la semilla debe estar en [0, m)")
        self.a, self.c, self.m = a, c, m
        self.state = seed

    def next_int(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def next_float(self):
        return self.next_int() / self.m

    def generate(self, n):
        """Devuelve n pares (X, U)."""
        values = []
        for _ in range(n):
            x = self.next_int()
            values.append((x, x / self.m))
        return values


def period(a, c, m, seed):
    """Longitud del ciclo de la secuencia (búsqueda exhaustiva, para m pequeño)."""
    seen = {}
    x, n = seed, 0
    while x not in seen:
        seen[x] = n
        x = (a * x + c) % m
        n += 1
    return n - seen[x]


def _prime_factors(n):
    factors, p = set(), 2
    while p * p <= n:
        while n % p == 0:
            factors.add(p)
            n //= p
        p += 1
    if n > 1:
        factors.add(n)
    return factors


def hull_dobell(a, c, m):
    """Condiciones del teorema de Hull-Dobell para período completo (período = m)."""
    return {
        "c y m son primos relativos": gcd(c, m) == 1,
        "a - 1 divisible por todo primo de m": all((a - 1) % p == 0 for p in _prime_factors(m)),
        "si 4 divide a m, 4 divide a a - 1": m % 4 != 0 or (a - 1) % 4 == 0,
    }


def mean(values):
    return sum(values) / len(values)


def variance(values):
    mu = mean(values)
    return sum((v - mu) ** 2 for v in values) / (len(values) - 1)


def chi_square_uniformity(values, bins=10):
    """Estadístico chi-cuadrado frente a U(0,1) y su valor crítico (alfa = 0.05)."""
    if bins != 10:
        raise ValueError("solo se tabula el valor crítico para 10 intervalos")
    observed = [0] * bins
    for u in values:
        observed[min(int(u * bins), bins - 1)] += 1
    expected = len(values) / bins
    statistic = sum((o - expected) ** 2 / expected for o in observed)
    return statistic, CHI2_CRITICAL_9_DF


def lag1_autocorrelation(values):
    mu = mean(values)
    num = sum((values[i] - mu) * (values[i + 1] - mu) for i in range(len(values) - 1))
    den = sum((v - mu) ** 2 for v in values)
    return num / den
