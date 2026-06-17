"""Tests for saved-state validation."""

import unittest

from ancient_all_in_one.services.validation import validate_state_payload


class ValidationTest(unittest.TestCase):
    """Verify malformed saved state can be repaired."""

    def test_invalid_root_restores_default_state(self):
        result = validate_state_payload([])

        self.assertTrue(result.errors)
        self.assertEqual(result.payload["navigation"][0]["title"], "Daily/Weekly")

    def test_malformed_sections_are_normalized(self):
        result = validate_state_payload(
            {
                "schema_version": "bad",
                "navigation": [{"title": "  Test  ", "item_type": "goal"}],
                "goals": [],
                "daily_weekly": "bad",
            }
        )

        self.assertTrue(result.warnings)
        self.assertEqual(result.payload["schema_version"], 1)
        self.assertEqual(result.payload["navigation"][0]["title"], "Test")
        self.assertEqual(result.payload["goals"], {})
        self.assertIsInstance(result.payload["daily_weekly"], dict)


if __name__ == "__main__":
    unittest.main()
