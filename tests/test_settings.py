"""Tests for settings persistence."""

import tempfile
import unittest
from pathlib import Path

from ancient_all_in_one.services.settings import AppSettings, SettingsStore


class SettingsStoreTest(unittest.TestCase):
    """Verify app settings are separate and durable."""

    def test_settings_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_file = Path(temp_dir) / "settings.json"
            store = SettingsStore(settings_file)
            settings = AppSettings(
                check_for_updates_on_startup=False,
                selected_game="general",
                theme="system",
                window_geometry="900x700",
            )

            store.save(settings)
            reloaded = store.load()

            self.assertFalse(reloaded.check_for_updates_on_startup)
            self.assertEqual(reloaded.window_geometry, "900x700")

    def test_corrupt_settings_are_backed_up(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_file = Path(temp_dir) / "settings.json"
            settings_file.write_text("{broken", encoding="utf-8")

            settings = SettingsStore(settings_file).load()

            self.assertTrue(settings_file.exists())
            self.assertTrue((Path(temp_dir) / "settings.corrupt.json").exists())
            self.assertTrue(settings.check_for_updates_on_startup)


if __name__ == "__main__":
    unittest.main()
