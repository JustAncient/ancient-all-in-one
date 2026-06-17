"""Tests for application configuration."""

import unittest

from ancient_all_in_one import __version__
from ancient_all_in_one.config import APP_BASE_NAME, APP_NAME, APP_VERSION


class ConfigTest(unittest.TestCase):
    """Verify app metadata stays consistent."""

    def test_app_name_includes_current_version(self):
        self.assertEqual(APP_VERSION, __version__)
        self.assertEqual(APP_NAME, f"{APP_BASE_NAME} v{APP_VERSION}")


if __name__ == "__main__":
    unittest.main()
