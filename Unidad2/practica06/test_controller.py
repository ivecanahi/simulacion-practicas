import shutil
import tempfile
import unittest
from pathlib import Path

import controller as ctl
from model import CONFIGURATIONS, LCG, chi_square_test, ks_test


@unittest.skipIf(shutil.which("javac") is None, "requiere el JDK")
class PythonJavaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctl.compile_java()

    def test_same_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            java_values = ctl.java_sequence(1000, 12345, Path(tmp) / "java.csv")
        py_values = LCG(seed=12345).uniforms(1000)
        self.assertEqual([f"{u:.10f}" for u in py_values], [f"{u:.10f}" for u in java_values])

    def test_same_statistics_for_every_configuration(self):
        for name, config in CONFIGURATIONS.items():
            with self.subTest(name):
                values = LCG(**config).uniforms(2000)
                chi, ks = chi_square_test(values), ks_test(values)
                java = ctl.java_tests(config, 2000)
                self.assertAlmostEqual(java["chi2"], chi["estadistico"], places=5)
                self.assertAlmostEqual(java["d"], ks["estadistico"], places=7)
                self.assertAlmostEqual(java["p_chi2"], chi["p"], delta=1e-6 * max(chi["p"], 1e-300))
                self.assertAlmostEqual(java["p_ks"], ks["p"], delta=1e-6)

    def test_same_pi_estimate(self):
        rows = ctl.pi_table([10_000])
        self.assertEqual(rows[0]["pi"], rows[0]["pi_java"])


class RepeatedTestsTest(unittest.TestCase):
    def test_rejection_rate_close_to_alpha(self):
        results = ctl.repeated_tests(blocks=200, block_size=500)
        rate = sum(r["chi"] < 0.05 for r in results) / len(results)
        self.assertLess(rate, 0.12)


if __name__ == "__main__":
    unittest.main()
