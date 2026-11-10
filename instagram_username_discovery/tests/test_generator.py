import tempfile
import unittest
from pathlib import Path

from username_discovery.generator import (
    generate_candidates,
    is_syntactically_valid,
    two_character_count,
)
from username_discovery.ledger import export_candidates, validate_csv


class GeneratorTests(unittest.TestCase):
    def test_two_character_count(self):
        self.assertEqual(two_character_count(), 1369)

    def test_period_cannot_appear_in_two_character_handle(self):
        candidates = set(generate_candidates(2, 2))
        self.assertNotIn(".a", candidates)
        self.assertNotIn("a.", candidates)
        self.assertNotIn("..", candidates)

    def test_underscore_and_digits_are_retained_as_candidates(self):
        candidates = set(generate_candidates(2, 2))
        self.assertIn("_a", candidates)
        self.assertIn("a_", candidates)
        self.assertIn("a7", candidates)
        self.assertIn("77", candidates)
        self.assertIn("__", candidates)

    def test_syntax_validation(self):
        self.assertTrue(is_syntactically_valid("ab"))
        self.assertTrue(is_syntactically_valid("_7"))
        self.assertFalse(is_syntactically_valid(".a"))
        self.assertFalse(is_syntactically_valid("a."))
        self.assertFalse(is_syntactically_valid("a..b"))
        self.assertFalse(is_syntactically_valid("a-b"))

    def test_export_and_validate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "candidates.csv"
            self.assertEqual(export_candidates(output, 2, 2), 1369)
            count, errors = validate_csv(output)
            self.assertEqual(count, 1369)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
