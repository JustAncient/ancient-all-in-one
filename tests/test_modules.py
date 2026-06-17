"""Tests for module registry."""

import unittest

from ancient_all_in_one.modules import get_module, get_registered_modules


class ModuleRegistryTest(unittest.TestCase):
    """Verify module registry foundations."""

    def test_general_module_is_registered(self):
        modules = get_registered_modules()
        module_ids = {module.module_id for module in modules}

        self.assertIn("general", module_ids)
        self.assertEqual(get_module("general").name, "General Tracking")
        self.assertIsNone(get_module("missing"))


if __name__ == "__main__":
    unittest.main()
