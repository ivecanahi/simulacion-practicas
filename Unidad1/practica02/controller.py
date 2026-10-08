"""
Controlador (C de MVC): toma el arreglo de datos, estima los parametros y
ejecuta los cuatro modelos y los escenarios de analisis (r, sigma, dt).
No calcula formulas por si mismo ni dibuja nada: solo orquesta.
"""
import numpy as np

from model import (
    deterministic_model,
    discrete_model,
    stochastic_model,
    continuous_model,
    estimate_parameters,
    error_metrics,
)

# Datos entregados por la guia (poblacion observada en cada periodo).
BASE_DATA = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

# Paso de tiempo por defecto para el modelo continuo (Euler).
DEFAULT_DT = 0.1

# Semilla fija para que las corridas estocasticas sean reproducibles.
SEED = 42


class PopulationSimulationController:
    """Ejecuta los modelos de crecimiento poblacional sobre un arreglo de datos."""

    def __init__(self, data, dt=DEFAULT_DT, seed=SEED):
        self.data = list(data)
        self.dt = dt
        self.seed = seed
        self.params = estimate_parameters(self.data)

    def _rng(self):
        return np.random.default_rng(self.seed)

    def run_all(self):
        """Corre los cuatro modelos con los parametros estimados de los datos."""
        p0, r, sigma, time = (self.params[k] for k in ("p0", "r", "sigma", "time"))
        return {
            "Deterministico": deterministic_model(p0, r, time),
            "Discreto": discrete_model(p0, r, time),
            "Estocastico": stochastic_model(p0, r, sigma, time, rng=self._rng()),
            "Continuo (Euler)": continuous_model(p0, r, time, self.dt),
        }

    def errors(self, results):
        """MAE y RMSE de cada modelo frente a los datos, evaluado en t = 0..n."""
        periods = np.arange(len(self.data))
        table = {}
        for name, (t, p) in results.items():
            predicted = np.interp(periods, t, p)
            table[name] = error_metrics(self.data, predicted)
        return table

    def rate_scenarios(self, rates):
        """Influencia de r: modelo discreto con distintas tasas (positivas y negativas)."""
        p0, time = self.params["p0"], self.params["time"]
        return {r: discrete_model(p0, r, time) for r in rates}

    def noise_scenarios(self, sigmas, runs=30):
        """Efecto de sigma: varias corridas del modelo estocastico por cada nivel de ruido."""
        p0, r, time = self.params["p0"], self.params["r"], self.params["time"]
        rng = self._rng()
        return {
            sigma: [stochastic_model(p0, r, sigma, time, rng=rng) for _ in range(runs)]
            for sigma in sigmas
        }

    def dt_scenarios(self, dts):
        """Efecto de dt: modelo continuo con distintos tamanos de paso."""
        p0, r, time = self.params["p0"], self.params["r"], self.params["time"]
        return {dt: continuous_model(p0, r, time, dt) for dt in dts}
