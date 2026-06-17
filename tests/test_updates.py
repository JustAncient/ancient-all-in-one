"""Tests for update comparison logic."""

import unittest

from maplestory_tracker.services.updates import UpdateChecker


class UpdateCheckerTest(unittest.TestCase):
    """Verify update comparison behavior."""

    def test_newer_version_detected(self):
        self.assertTrue(UpdateChecker._is_newer_version("0.2.0", "0.1.0"))

    def test_same_version_is_not_newer(self):
        self.assertFalse(UpdateChecker._is_newer_version("0.1.0", "0.1.0"))


if __name__ == "__main__":
    unittest.main()
