"""Tests for update comparison logic."""

import unittest

from maplestory_tracker.services.updates import UpdateChecker


class UpdateCheckerTest(unittest.TestCase):
    """Verify update comparison behavior."""

    def test_newer_version_detected(self):
        self.assertTrue(UpdateChecker._is_newer_version("0.2.0", "0.1.0"))

    def test_same_version_is_not_newer(self):
        self.assertFalse(UpdateChecker._is_newer_version("0.1.0", "0.1.0"))

    def test_v_prefixed_release_is_supported(self):
        self.assertTrue(UpdateChecker._is_newer_version("v0.1.1", "0.1.0"))

    def test_release_notes_are_truncated(self):
        notes = "x" * 701

        cleaned = UpdateChecker._clean_release_notes(notes)

        self.assertEqual(len(cleaned), 703)
        self.assertTrue(cleaned.endswith("..."))


if __name__ == "__main__":
    unittest.main()
