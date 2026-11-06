"""Modelo: generador LCG, pruebas Chi-cuadrado y Kolmogorov-Smirnov, y Monte Carlo para π."""
import math

ALPHA = 0.05

# Configuraciones del generador que se comparan en la práctica.
CONFIGURATIONS = {
    "Guía (Numerical Recipes)": {"a": 1664525, "c": 1013904223, "m": 2**32, "seed": 12345},
    "RANDU (IBM, 1960s)": {"a": 65539, "c": 0, "m": 2**31, "seed": 1},
    "Módulo pequeño (m = 256)": {"a": 137, "c": 187, "m": 256, "seed": 57},
    "Incremento fijo (a = 1)": {"a": 1, "c": 429496731, "m": 2**32, "seed": 12345},
    "Multiplicador par (a = 1664524)": {"a": 1664524, "c": 1013904223, "m": 2**32, "seed": 12345},
}


class LCG:
    """X(n+1) = (a·X(n) + c) mod m;  U(n) = X(n) / m."""

    def __init__(self, seed=12345, a=1664525, c=1013904223, m=2**32):
        if m <= 0 or not (0 <= a < m and 0 <= c < m and 0 <= seed < m):
            raise ValueError("se requiere m > 0 y a, c, semilla en [0, m)")
        self.a, self.c, self.m = a, c, m
        self.state = seed

    def next_int(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def uniforms(self, n):
        return [self.next_int() / self.m for _ in range(n)]


# ---------------------------------------------------------------- valores p

def _regularized_gamma_q(s, x):
    """Q(s, x) = Γ(s, x) / Γ(s), función gamma incompleta superior regularizada."""
    if x <= 0:
        return 1.0
    log_prefix = -x + s * math.log(x) - math.lgamma(s)
    if x < s + 1:                                   # serie para P(s, x)
        term = total = 1.0 / s
        k = s
        while abs(term) > abs(total) * 1e-15:
            k += 1
            term *= x / k
            total += term
        return 1.0 - total * math.exp(log_prefix)
    # Fracción continua de Lentz para Q(s, x)
    tiny = 1e-300
    b = x + 1 - s
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 300):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return h * math.exp(log_prefix)


def chi2_sf(statistic, df):
    """P(χ²_df > statistic): valor p de la prueba Chi-cuadrado."""
    return _regularized_gamma_q(df / 2, statistic / 2)


def ks_sf(lam):
    """Distribución de Kolmogorov: P(K > λ) = 2 Σ (-1)^(j-1) e^(-2 j² λ²)."""
    if lam < 0.2:
        return 1.0
    total = 0.0
    for j in range(1, 101):
        term = (-1) ** (j - 1) * math.exp(-2 * j * j * lam * lam)
        total += term
        if abs(term) < 1e-16:
            break
    return max(0.0, min(1.0, 2 * total))


# ---------------------------------------------------------------- pruebas

def chi_square_test(values, k=10, alpha=ALPHA):
    n = len(values)
    observed = [0] * k
    for u in values:
        observed[min(int(u * k), k - 1)] += 1
    expected = n / k
    statistic = sum((o - expected) ** 2 / expected for o in observed)
    df = k - 1
    p_value = chi2_sf(statistic, df)
    return {"observadas": observed, "esperada": expected, "estadistico": statistic,
            "gl": df, "p": p_value, "rechaza": p_value < alpha}


def ks_test(values, alpha=ALPHA):
    ordered = sorted(values)
    n = len(ordered)
    d_plus = max((i + 1) / n - u for i, u in enumerate(ordered))
    d_minus = max(u - i / n for i, u in enumerate(ordered))
    d = max(d_plus, d_minus)
    sqrt_n = math.sqrt(n)
    p_value = ks_sf((sqrt_n + 0.12 + 0.11 / sqrt_n) * d)   # corrección de Stephens
    return {"d_mas": d_plus, "d_menos": d_minus, "estadistico": d,
            "p": p_value, "rechaza": p_value < alpha}


def monte_carlo_pi(n, seed=12345):
    """Estima π con n puntos (U1, U2) en el cuadrado unitario."""
    gen = LCG(seed=seed)
    inside = 0
    for _ in range(n):
        x = gen.next_int() / gen.m
        y = gen.next_int() / gen.m
        if x * x + y * y <= 1.0:
            inside += 1
    return 4 * inside / n
