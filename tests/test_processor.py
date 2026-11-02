import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processor import classify, load_candidates


class ProcessorTests(unittest.TestCase):
    def test_sample_data_loads_and_reports_one_invalid_row(self):
        data_path = Path(__file__).resolve().parents[1] / "data" / "employees.csv"
        candidates, errors = load_candidates(str(data_path))

        self.assertEqual(len(candidates), 20)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["row"], 22)

    def test_complete_candidate_is_ready(self):
        candidates, _ = load_candidates(str(Path(__file__).resolve().parents[1] / "data" / "employees.csv"))
        result = classify(candidates[0], date(2026, 11, 2))

        self.assertEqual(result.status, "Ready")
        self.assertEqual(result.priority, "Urgent")
        self.assertEqual(result.missing_items, ())

    def test_missing_identity_is_blocked(self):
        candidates, _ = load_candidates(str(Path(__file__).resolve().parents[1] / "data" / "employees.csv"))
        result = classify(candidates[2], date(2026, 11, 2))

        self.assertEqual(result.status, "Blocked")
        self.assertIn("Identity document", result.missing_items)


if __name__ == "__main__":
    unittest.main()
