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


if __name__ == "__main__":
    unittest.main()
