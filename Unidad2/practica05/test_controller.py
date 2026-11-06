import shutil
import tempfile
import unittest
from pathlib import Path

import controller as ctl


@unittest.skipIf(shutil.which("javac") is None, "requiere el JDK")
class PythonJavaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctl.compile_java()

    def test_java_and_python_produce_the_same_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            for seed in (0, 12345, 2**32 - 1):
                py_rows = ctl.python_sequence(1000, seed)
                java_rows = ctl.java_sequence(1000, seed, Path(tmp) / "java.csv")
                self.assertEqual(ctl.compare(py_rows, java_rows), (1000, 1000))

    def test_csv_round_trip(self):
        rows = ctl.python_sequence(5, 12345)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "py.csv"
            ctl.write_csv(rows, path)
            self.assertEqual([r[1] for r in ctl.read_csv(path)], [r[1] for r in rows])


class PeriodExamplesTest(unittest.TestCase):
    def test_low_bits_double_their_period(self):
        self.assertEqual(ctl.low_bit_periods(12345, 4), [(1, 2), (2, 4), (3, 8), (4, 16)])


if __name__ == "__main__":
    unittest.main()
