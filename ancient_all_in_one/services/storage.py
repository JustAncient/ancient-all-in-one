"""Persistence for user-owned tracker data."""

from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from time import time

from ancient_all_in_one.config import (
    DATA_FILE,
    LEGACY_DATA_FILE,
    SCHEMA_VERSION,
)
from ancient_all_in_one.data.default_state import build_default_state
from ancient_all_in_one.migrations import MigrationError, migrate_payload
from ancient_all_in_one.models import AppState
from ancient_all_in_one.services.backups import BackupManager
from ancient_all_in_one.services.validation import validate_state_payload

LOGGER = logging.getLogger(__name__)


class StateStore:
    """Load, migrate, save, import, and export tracker state."""

    def __init__(
        self,
        data_file: Path = DATA_FILE,
        legacy_data_file: Path = LEGACY_DATA_FILE,
        backup_manager: BackupManager | None = None,
    ) -> None:
        self.data_file = data_file
        self.legacy_data_file = legacy_data_file
        self.backup_manager = backup_manager or BackupManager(
            self.data_file.parent / "backups"
        )

    def load(self) -> AppState:
        """Load saved state or create first-run defaults."""

        self._adopt_legacy_data()
        if not self.data_file.exists():
            LOGGER.info("Creating default state at %s", self.data_file)
            state = build_default_state()
            self.save(state)
            return state

        try:
            payload = self._read_payload(self.data_file)
        except json.JSONDecodeError:
            backup = self._backup_corrupt_file()
            LOGGER.warning(
                "State file was corrupt. Backed it up to %s",
                backup,
            )
            state = build_default_state()
            self.save(state)
            return state

        state, should_save = self._state_from_payload(
            payload, source_file=self.data_file
        )
        if should_save:
            self.save(state)
        return state

    def save(
        self,
        state: AppState,
        *,
        create_backup: bool = False,
        backup_reason: str = "manual-save",
    ) -> None:
        """Persist state as formatted JSON."""

        if create_backup:
            self.backup_manager.create_backup(self.data_file, backup_reason)

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.data_file.with_suffix(".json.tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(state.to_dict(), file, indent=2, sort_keys=True)
            file.write("\n")
        temp_file.replace(self.data_file)

    def export_to(self, export_file: Path) -> Path:
        """Export current tracker data to a user-selected JSON file."""

        state = self.load()
        self.save(state)
        export_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.data_file, export_file)
        LOGGER.info("Exported tracker data to %s", export_file)
        return export_file

    def import_from(self, import_file: Path) -> AppState:
        """Import tracker data from a JSON file after validation."""

        payload = self._read_payload(import_file)
        state, _should_save = self._state_from_payload(
            payload,
            source_file=import_file,
            backup_before_migration=False,
            reject_validation_errors=True,
        )
        self.save(state, create_backup=True, backup_reason="pre-import")
        LOGGER.info("Imported tracker data from %s", import_file)
        return state

    def _state_from_payload(
        self,
        payload: object,
        *,
        source_file: Path,
        backup_before_migration: bool = True,
        reject_validation_errors: bool = False,
    ) -> tuple[AppState, bool]:
        validation = validate_state_payload(payload)
        for issue in validation.errors:
            LOGGER.error("State validation error in %s: %s", source_file, issue)
        if validation.errors and reject_validation_errors:
            raise ValueError(
                "Imported data failed validation: " + "; ".join(validation.errors)
            )
        for issue in validation.warnings:
            LOGGER.warning("State validation warning in %s: %s", source_file, issue)

        normalized_payload = validation.payload
        migrated = False
        try:
            if normalized_payload.get("schema_version", 1) < SCHEMA_VERSION:
                if backup_before_migration:
                    self.backup_manager.create_backup(source_file, "pre-migration")
                normalized_payload, migrated = migrate_payload(
                    normalized_payload,
                    SCHEMA_VERSION,
                )
        except MigrationError:
            LOGGER.exception("Could not migrate state from %s", source_file)
            raise

        state = AppState.from_dict(normalized_payload)
        return state, validation.changed or migrated

    def _read_payload(self, source_file: Path) -> object:
        with source_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _adopt_legacy_data(self) -> None:
        """Copy project-local data into the app-data folder on first launch."""

        if self.data_file.exists() or self.data_file == self.legacy_data_file:
            return
        if not self.legacy_data_file.exists():
            return

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.legacy_data_file, self.data_file)
        LOGGER.info(
            "Adopted legacy state file from %s into %s",
            self.legacy_data_file,
            self.data_file,
        )

    def _backup_corrupt_file(self) -> Path:
        """Move unreadable JSON aside so it can be inspected later."""

        backup = self.data_file.with_suffix(f".corrupt-{int(time())}.json")
        self.data_file.replace(backup)
        return backup
