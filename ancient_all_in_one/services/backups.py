"""Backup helpers for user-owned data files."""

from __future__ import annotations

import re
import shutil
from datetime import UTC, datetime
from pathlib import Path

from ancient_all_in_one.config import BACKUP_DIR

_REASON_PATTERN = re.compile(r"[^a-zA-Z0-9_.-]+")


class BackupManager:
    """Create timestamped backups with simple retention."""

    def __init__(self, backup_dir: Path = BACKUP_DIR, keep_last: int = 20) -> None:
        self.backup_dir = backup_dir
        self.keep_last = keep_last

    def create_backup(self, source_file: Path, reason: str) -> Path | None:
        """Copy a source file into the backup folder if it exists."""

        if not source_file.exists():
            return None

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")
        safe_reason = _sanitize_reason(reason)
        backup_file = self.backup_dir / (
            f"{source_file.stem}-{timestamp}-{safe_reason}{source_file.suffix}"
        )
        shutil.copy2(source_file, backup_file)
        self._prune_backups(source_file.stem)
        return backup_file

    def _prune_backups(self, stem: str) -> None:
        backups = sorted(
            self.backup_dir.glob(f"{stem}-*"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        for old_backup in backups[self.keep_last :]:
            old_backup.unlink(missing_ok=True)


def _sanitize_reason(reason: str) -> str:
    cleaned = _REASON_PATTERN.sub("-", reason.strip()).strip("-")
    return cleaned or "backup"
