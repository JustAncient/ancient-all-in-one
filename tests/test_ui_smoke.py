"""Smoke tests for UI wiring."""

import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from ancient_all_in_one.config import APP_NAME
from ancient_all_in_one.services.settings import AppSettings, SettingsStore
from ancient_all_in_one.services.storage import StateStore
from ancient_all_in_one.ui.main_window import MainWindow


class UISmokeTest(unittest.TestCase):
    """Verify the main window can be constructed without entering mainloop."""

    def test_main_window_constructs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = StateStore(temp_path / "tracker_data.json")
            settings_store = SettingsStore(temp_path / "settings.json")
            settings = AppSettings(check_for_updates_on_startup=False)
            state = store.load()

            try:
                window = MainWindow(
                    state=state,
                    store=store,
                    settings=settings,
                    settings_store=settings_store,
                )
            except tk.TclError as exc:
                self.skipTest(f"Tk is not available in this environment: {exc}")

            try:
                window.update_idletasks()
                self.assertEqual(window.title(), APP_NAME)
                self.assertIsNotNone(window.selected_item)
            finally:
                window.destroy()


if __name__ == "__main__":
    unittest.main()
