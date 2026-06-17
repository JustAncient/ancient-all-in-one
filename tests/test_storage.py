"""Tests for persistent tracker state."""

import tempfile
import unittest
from pathlib import Path

from ancient_all_in_one.models import NavItem
from ancient_all_in_one.services.storage import StateStore


class StateStoreTest(unittest.TestCase):
    """Verify state persistence behavior."""

    def test_store_creates_default_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tracker_data.json"
            store = StateStore(data_file)

            state = store.load()

            self.assertTrue(data_file.exists())
            self.assertEqual(
                [item.title for item in state.navigation],
                ["Daily/Weekly", "Goals"],
            )
            self.assertEqual(state.navigation[1].children[0].title, "Lv1 Hexa")
            self.assertEqual(state.navigation[1].children[1].title, "Sol Hecate")

    def test_store_preserves_user_added_goal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tracker_data.json"
            store = StateStore(data_file)
            state = store.load()

            goals = state.navigation[1]
            custom_goal = NavItem(title="Arcane Symbol Push", item_type="goal")
            goals.children.append(custom_goal)
            state.goals[custom_goal.item_id] = {
                "title": custom_goal.title,
                "notes": "Get more symbols.",
                "tasks": [],
            }
            store.save(state)

            reloaded = store.load()
            reloaded_goals = reloaded.navigation[1]

            self.assertEqual(
                reloaded_goals.children[-1].title,
                "Arcane Symbol Push",
            )
            self.assertEqual(
                reloaded.goals[custom_goal.item_id]["notes"],
                "Get more symbols.",
            )

    def test_store_adopts_legacy_data_when_new_file_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_file = temp_path / "app_data" / "tracker_data.json"
            legacy_file = temp_path / "legacy" / "tracker_data.json"
            legacy_store = StateStore(legacy_file, legacy_file)
            legacy_state = legacy_store.load()
            legacy_state.daily_weekly["dailies"] = ["Monster Park"]
            legacy_store.save(legacy_state)

            adopted_state = StateStore(data_file, legacy_file).load()

            self.assertTrue(data_file.exists())
            self.assertEqual(adopted_state.daily_weekly["dailies"], ["Monster Park"])

    def test_store_backs_up_corrupt_json_and_recovers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tracker_data.json"
            data_file.write_text("{broken json", encoding="utf-8")

            state = StateStore(data_file).load()
            backups = list(data_file.parent.glob("tracker_data.corrupt-*.json"))

            self.assertTrue(data_file.exists())
            self.assertEqual(len(backups), 1)
            self.assertEqual(state.navigation[0].title, "Daily/Weekly")

    def test_store_exports_and_imports_with_backup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_file = temp_path / "tracker_data.json"
            export_file = temp_path / "exports" / "data.json"
            import_file = temp_path / "import.json"
            store = StateStore(data_file)
            state = store.load()
            state.daily_weekly["dailies"] = ["Daily A"]
            store.save(state)

            store.export_to(export_file)
            import_file.write_text(
                export_file.read_text(encoding="utf-8"), encoding="utf-8"
            )
            imported = store.import_from(import_file)

            self.assertTrue(export_file.exists())
            self.assertEqual(imported.daily_weekly["dailies"], ["Daily A"])
            self.assertTrue(
                list((temp_path / "backups").glob("tracker_data-*pre-import*"))
            )

    def test_import_rejects_invalid_root_without_replacing_current_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_file = temp_path / "tracker_data.json"
            import_file = temp_path / "bad_import.json"
            store = StateStore(data_file)
            state = store.load()
            state.daily_weekly["dailies"] = ["Keep Me"]
            store.save(state)
            import_file.write_text("[]", encoding="utf-8")

            with self.assertRaises(ValueError):
                store.import_from(import_file)

            reloaded = store.load()
            self.assertEqual(reloaded.daily_weekly["dailies"], ["Keep Me"])

    def test_validation_repairs_malformed_saved_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tracker_data.json"
            data_file.write_text('{"navigation": "bad"}', encoding="utf-8")

            state = StateStore(data_file).load()

            self.assertEqual(state.navigation[0].title, "Daily/Weekly")


if __name__ == "__main__":
    unittest.main()
