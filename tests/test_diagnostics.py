"""Tests for diagnostics output."""

import unittest

from ancient_all_in_one.config import APP_NAME, GITHUB_REPO
from ancient_all_in_one.services.diagnostics import build_diagnostics


class DiagnosticsTest(unittest.TestCase):
    """Verify diagnostic details are accurate enough for support."""

    def test_diagnostics_include_app_and_repository(self):
        diagnostics = build_diagnostics()
        message = diagnostics.to_message()

        self.assertEqual(diagnostics.app_name, APP_NAME)
        self.assertEqual(diagnostics.github_repo, GITHUB_REPO)
        self.assertIn("Ancient All-in-One", message)
        self.assertIn("ancient-all-in-one", message)


if __name__ == "__main__":
    unittest.main()
