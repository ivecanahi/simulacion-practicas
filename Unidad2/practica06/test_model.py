import importlib.util
import math
import unittest

from model import (CONFIGURATIONS, LCG, chi2_sf, chi_square_test, ks_sf, ks_test,
                   monte_carlo_pi)


class LCGTest(unittest.TestCase):
    def test_first_value_of_guide_configuration(self):
        self.assertEqual(LCG(seed=12345).next_int(), 87628868)

    def test_uniforms_in_unit_interval(self):
        self.assertTrue(all(0 <= u < 1 for u in LCG().uniforms(5000)))

    def test_configurations_are_valid(self):
        for config in CONFIGURATIONS.values():
            LCG(**config)


class PValueTest(unittest.TestCase):
    def test_chi2_sf_known_values(self):
        # Valores críticos tabulados: P(chi2_9 > 16.919) = 0.05 y P(chi2_9 > 21.666) = 0.01
        self.assertAlmostEqual(chi2_sf(16.919, 9), 0.05, places=4)
        self.assertAlmostEqual(chi2_sf(21.666, 9), 0.01, places=4)
        self.assertAlmostEqual(chi2_sf(0.0, 9), 1.0)
        # gl = 2: P(X > x) = exp(-x/2)
        self.assertAlmostEqual(chi2_sf(3.0, 2), math.exp(-1.5), places=10)

    def test_ks_sf_known_values(self):
        # Valor crítico asintótico de Kolmogorov para alfa = 0.05: lambda = 1.358
        self.assertAlmostEqual(ks_sf(1.358), 0.05, places=3)
        self.assertAlmostEqual(ks_sf(0.0), 1.0)


class ChiSquareTest(unittest.TestCase):
    def test_perfectly_uniform_sample(self):
        values = [(i + 0.5) / 100 for i in range(100)]
        result = chi_square_test(values, k=10)
        self.assertEqual(result["observadas"], [10] * 10)
        self.assertEqual(result["estadistico"], 0)
        self.assertEqual(result["gl"], 9)
        self.assertFalse(result["rechaza"])

    def test_concentrated_sample_is_rejected(self):
        values = [0.05 + 0.001 * i for i in range(100)]   # todo en [0.05, 0.15)
        self.assertTrue(chi_square_test(values)["rechaza"])

    def test_hand_calculated_statistic(self):
        values = [0.05] * 3 + [0.95] * 1                  # O = [3,0,...,0,1], E = 0.4
        expected = ((3 - 0.4) ** 2 + 8 * 0.4 ** 2 + (1 - 0.4) ** 2) / 0.4
        self.assertAlmostEqual(chi_square_test(values)["estadistico"], expected)


class KSTest(unittest.TestCase):
    def test_hand_calculated_statistic(self):
        result = ks_test([0.1, 0.5, 0.6])
        # D+ = max(i/n - u_i) = max(1/3-0.1, 2/3-0.5, 1-0.6) = 0.4
        # D- = max(u_i - (i-1)/n) = max(0.1, 0.5-1/3, 0.6-2/3) = 0.1667
        self.assertAlmostEqual(result["d_mas"], 0.4)
        self.assertAlmostEqual(result["d_menos"], 0.5 - 1 / 3)
        self.assertAlmostEqual(result["estadistico"], 0.4)

    def test_uniform_lcg_sample_is_not_rejected(self):
        self.assertFalse(ks_test(LCG().uniforms(10_000))["rechaza"])

    def test_skewed_sample_is_rejected(self):
        values = [u ** 2 for u in LCG().uniforms(1000)]
        self.assertTrue(ks_test(values)["rechaza"])


class MonteCarloPiTest(unittest.TestCase):
    def test_estimate_close_to_pi(self):
        estimate = monte_carlo_pi(100_000)
        self.assertLess(abs(estimate - math.pi), 0.02)

    def test_reproducible(self):
        self.assertEqual(monte_carlo_pi(1000, seed=7), monte_carlo_pi(1000, seed=7))


@unittest.skipIf(importlib.util.find_spec("scipy") is None, "SciPy no instalado (validación opcional)")
class SciPyValidationTest(unittest.TestCase):
    def test_p_values_match_scipy(self):
        from scipy import stats
        for config in CONFIGURATIONS.values():
            values = LCG(**config).uniforms(5000)
            chi = chi_square_test(values)
            self.assertAlmostEqual(chi["p"], stats.chisquare(chi["observadas"]).pvalue, places=10)
            ks = ks_test(values)
            reference = stats.kstest(values, "uniform")
            self.assertAlmostEqual(ks["estadistico"], reference.statistic, places=12)
            self.assertAlmostEqual(ks["p"], reference.pvalue, delta=0.005)


if __name__ == "__main__":
    unittest.main()
