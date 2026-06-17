"""Tests for schema migration registry."""

import unittest

from ancient_all_in_one.migrations import MigrationError, migrate_payload


class MigrationTest(unittest.TestCase):
    """Verify migration registry safety behavior."""

    def test_current_schema_needs_no_migration(self):
        payload = {"schema_version": 1}

        migrated_payload, migrated = migrate_payload(payload, 1)

        self.assertIs(migrated_payload, payload)
        self.assertFalse(migrated)

    def test_newer_schema_is_rejected(self):
        with self.assertRaises(MigrationError):
            migrate_payload({"schema_version": 99}, 1)

    def test_missing_migration_is_rejected(self):
        with self.assertRaises(MigrationError):
            migrate_payload({"schema_version": 1}, 2)


if __name__ == "__main__":
    unittest.main()
