"""
Pruebas del modelo (python3 -m unittest test_model.py).
Verifican que cada modelo cumpla su formula de la guia.
"""
import math
import unittest

import numpy as np

from model import (
    deterministic_model,
    discrete_model,
    stochastic_model,
    continuous_model,
    estimate_parameters,
)


class DeterministicModelTest(unittest.TestCase):
    def test_follows_exponential_formula(self):
        t, p = deterministic_model(p0=1000, r=0.1, time=5)
        self.assertEqual(len(t), len(p))
        self.assertAlmostEqual(p[0], 1000)
        self.assertAlmostEqual(p[-1], 1000 * math.exp(0.1 * 5))

    def test_negative_rate_decreases(self):
        _, p = deterministic_model(p0=1000, r=-0.1, time=5)
        self.assertTrue(np.all(np.diff(p) < 0))


class DiscreteModelTest(unittest.TestCase):
    def test_follows_difference_equation(self):
        t, p = discrete_model(p0=1000, r=0.1, time=3)
        np.testing.assert_allclose(t, [0, 1, 2, 3])
        np.testing.assert_allclose(p, [1000, 1100, 1210, 1331])


class StochasticModelTest(unittest.TestCase):
    def test_sigma_zero_equals_discrete(self):
        _, p_disc = discrete_model(p0=1000, r=0.1, time=6)
        _, p_sto = stochastic_model(p0=1000, r=0.1, sigma=0, time=6, rng=np.random.default_rng(1))
        np.testing.assert_allclose(p_sto, p_disc)

    def test_same_seed_same_result(self):
        _, a = stochastic_model(1000, 0.1, 50, 6, rng=np.random.default_rng(7))
        _, b = stochastic_model(1000, 0.1, 50, 6, rng=np.random.default_rng(7))
        np.testing.assert_allclose(a, b)

    def test_population_never_negative(self):
        _, p = stochastic_model(10, -0.5, 500, 30, rng=np.random.default_rng(0))
        self.assertTrue(np.all(p >= 0))


class ContinuousModelTest(unittest.TestCase):
    def test_dt_one_equals_discrete(self):
        _, p_disc = discrete_model(p0=1000, r=0.1, time=6)
        _, p_cont = continuous_model(p0=1000, r=0.1, time=6, dt=1)
        np.testing.assert_allclose(p_cont, p_disc)

    def test_small_dt_approaches_exponential(self):
        _, p = continuous_model(p0=1000, r=0.1, time=6, dt=0.001)
        self.assertAlmostEqual(p[-1], 1000 * math.exp(0.6), delta=1.0)


class EstimateParametersTest(unittest.TestCase):
    def test_constant_growth_data(self):
        params = estimate_parameters([1000, 1100, 1210, 1331])
        self.assertAlmostEqual(params["p0"], 1000)
        self.assertAlmostEqual(params["r"], 0.1)
        self.assertAlmostEqual(params["sigma"], 0.0)
        self.assertEqual(params["time"], 3)


class ShortDataTest(unittest.TestCase):
    """Con pocos datos sigma da 0: la simulacion completa no debe caerse."""

    def test_main_runs_with_two_points(self):
        import os
        import tempfile
        import main
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                main.main([1000, 1100])
                self.assertTrue(os.path.exists("efecto_sigma.png"))
                self.assertTrue(os.path.exists("efecto_dt.png"))
            finally:
                os.chdir(cwd)

    def test_estimate_parameters_rejects_single_point(self):
        with self.assertRaises(ValueError):
            estimate_parameters([1000])

    def test_estimate_parameters_rejects_zero_population(self):
        with self.assertRaises(ValueError):
            estimate_parameters([1000, 0, 500])


if __name__ == "__main__":
    unittest.main()
