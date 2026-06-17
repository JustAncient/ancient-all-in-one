"""Tests for timestamped backup behavior."""

import tempfile
import unittest
from pathlib import Path

from ancient_all_in_one.services.backups import BackupManager


class BackupManagerTest(unittest.TestCase):
    """Verify user data backup behavior."""

    def test_backup_file_is_created_with_reason(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source = temp_path / "tracker_data.json"
            source.write_text('{"ok": true}', encoding="utf-8")
            manager = BackupManager(temp_path / "backups")

            backup = manager.create_backup(source, "pre import")

            self.assertIsNotNone(backup)
            self.assertTrue(backup.exists())
            self.assertIn("pre-import", backup.name)
            self.assertEqual(backup.read_text(encoding="utf-8"), '{"ok": true}')

    def test_backup_retention_prunes_old_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source = temp_path / "tracker_data.json"
            manager = BackupManager(temp_path / "backups", keep_last=2)

            for index in range(3):
                source.write_text(str(index), encoding="utf-8")
                manager.create_backup(source, f"copy-{index}")

            backups = list((temp_path / "backups").glob("tracker_data-*"))
            self.assertEqual(len(backups), 2)


if __name__ == "__main__":
    unittest.main()
