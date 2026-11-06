import unittest

from model import (A, C, M, SEED, LCG, chi_square_uniformity, hull_dobell,
                   lag1_autocorrelation, period)


class LCGTest(unittest.TestCase):
    def test_first_values_match_hand_calculation(self):
        gen = LCG()
        x1 = (A * SEED + C) % M
        x2 = (A * x1 + C) % M
        self.assertEqual(gen.next_int(), x1)
        self.assertEqual(gen.next_int(), x2)

    def test_known_first_value(self):
        self.assertEqual(LCG(seed=12345).next_int(), 87628868)

    def test_uniform_values_are_in_unit_interval(self):
        values = LCG().generate(10_000)
        self.assertTrue(all(0 <= u < 1 for _, u in values))
        self.assertEqual(len(values), 10_000)

    def test_same_seed_reproduces_sequence(self):
        self.assertEqual(LCG(seed=7).generate(50), LCG(seed=7).generate(50))

    def test_different_seed_changes_sequence(self):
        self.assertNotEqual(LCG(seed=7).generate(50), LCG(seed=8).generate(50))

    def test_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            LCG(m=0)
        with self.assertRaises(ValueError):
            LCG(seed=-1)
        with self.assertRaises(ValueError):
            LCG(seed=M)


class PeriodTest(unittest.TestCase):
    def test_full_period_when_hull_dobell_holds(self):
        self.assertEqual(period(a=5, c=3, m=16, seed=7), 16)

    def test_short_period_with_bad_parameters(self):
        self.assertEqual(period(a=5, c=4, m=16, seed=1), 2)   # c par: 1, 9, 1, ...
        self.assertEqual(period(a=4, c=2, m=16, seed=1), 1)   # a par: 1, 6, 10, 10, ...
        self.assertEqual(period(a=1, c=0, m=16, seed=5), 1)

    def test_hull_dobell_for_guide_parameters(self):
        self.assertTrue(all(hull_dobell(A, C, M).values()))

    def test_hull_dobell_detects_failure(self):
        self.assertFalse(all(hull_dobell(4, 2, 16).values()))

    def test_low_bits_have_short_period(self):
        for k in range(1, 9):
            self.assertEqual(period(a=A % 2**k, c=C % 2**k, m=2**k, seed=SEED % 2**k), 2**k)


class StatisticsTest(unittest.TestCase):
    def test_chi_square_accepts_uniform_sequence(self):
        uniforms = [u for _, u in LCG().generate(10_000)]
        statistic, critical = chi_square_uniformity(uniforms, bins=10)
        self.assertLess(statistic, critical)

    def test_lag1_autocorrelation_is_small(self):
        uniforms = [u for _, u in LCG().generate(10_000)]
        self.assertLess(abs(lag1_autocorrelation(uniforms)), 0.03)


if __name__ == "__main__":
    unittest.main()
