import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from time_savings import calculate_time_savings


class TimeSavingsTests(unittest.TestCase):
    def test_calculation_reduces_manual_work(self):
        result = calculate_time_savings(20, 10)

        self.assertEqual(result["manual_minutes"], 360)
        self.assertEqual(result["automated_minutes"], 85.0)
        self.assertEqual(result["minutes_saved"], 275.0)
        self.assertEqual(result["percent_reduction"], 76.4)

    def test_zero_records_has_zero_reduction(self):
        result = calculate_time_savings(0, 0)
        self.assertEqual(result["percent_reduction"], 0)

    def test_invalid_exception_count_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_time_savings(5, 6)


if __name__ == "__main__":
    unittest.main()
