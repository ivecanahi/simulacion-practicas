"""
Modelo (M de MVC): los cuatro modelos de crecimiento poblacional de la guia
y la estimacion de parametros a partir del arreglo de datos.

    Deterministico:  P(t)      = P0 * e^(r*t)
    Discreto:        P(t+1)    = P(t) + r*P(t)
    Estocastico:     P(t+1)    = P(t) + r*P(t) + e(t),   e(t) ~ N(0, sigma^2)
    Continuo:        dP/dt     = r*P   (resuelto con Euler)
                     P(t+dt)   = P(t) + dt*(r*P(t))

Cada funcion devuelve (tiempo, poblacion) como arreglos de NumPy.
Este modulo no imprime ni grafica: solo calcula.
"""
import numpy as np


def deterministic_model(p0, r, time, points=200):
    """Crecimiento exponencial exacto evaluado en un vector de tiempo denso."""
    t = np.linspace(0, time, points)
    p = p0 * np.exp(r * t)
    return t, p


def discrete_model(p0, r, time):
    """La poblacion cambia solo en periodos enteros: P(t+1) = P(t) + r*P(t)."""
    population = [p0]
    for _ in range(time):
        current = population[-1]
        increment = r * current
        population.append(current + increment)
    return np.arange(time + 1), np.array(population, dtype=float)


def stochastic_model(p0, r, sigma, time, rng=None):
    """
    Igual al discreto pero sumando un ruido normal N(0, sigma) en cada periodo.
    Si la poblacion queda negativa se corta en 0 (no existen poblaciones < 0).
    Se puede pasar un rng con semilla para que la corrida sea reproducible.
    """
    rng = rng if rng is not None else np.random.default_rng()
    population = [p0]
    for _ in range(time):
        noise = rng.normal(0, sigma)
        current = population[-1]
        new_population = current + r * current + noise
        population.append(max(new_population, 0.0))
    return np.arange(time + 1), np.array(population, dtype=float)


def continuous_model(p0, r, time, dt):
    """Aproximacion numerica de dP/dt = r*P con el metodo de Euler y paso dt."""
    steps = int(round(time / dt))
    t = np.linspace(0, steps * dt, steps + 1)
    population = [p0]
    for _ in range(steps):
        current = population[-1]
        change = r * current
        population.append(current + dt * change)
    return t, np.array(population, dtype=float)


def estimate_parameters(data):
    """
    Obtiene los parametros de la simulacion a partir del arreglo de entrada:
      - p0:    primer dato (poblacion inicial).
      - r:     promedio de la tasa de crecimiento por periodo (P(t+1)-P(t))/P(t).
      - sigma: desviacion estandar de lo que el modelo discreto NO explica
               (residuo = dato real - prediccion del discreto un paso adelante).
      - time:  numero de periodos (cantidad de datos - 1).
    """
    data = np.asarray(data, dtype=float)
    rates = np.diff(data) / data[:-1]
    r = float(np.mean(rates))
    residuals = data[1:] - (data[:-1] + r * data[:-1])
    sigma = float(np.std(residuals, ddof=1)) if len(residuals) > 1 else 0.0
    return {"p0": float(data[0]), "r": r, "sigma": sigma, "time": len(data) - 1}


def error_metrics(data, predicted):
    """Error medio absoluto (MAE) y raiz del error cuadratico medio (RMSE)."""
    data = np.asarray(data, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    error = data - predicted
    return float(np.mean(np.abs(error))), float(np.sqrt(np.mean(error ** 2)))
