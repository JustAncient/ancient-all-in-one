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
from ancient_all_in_one.models import AppState

LOGGER = logging.getLogger(__name__)


class StateStore:
    """Load, migrate, and save tracker state."""

    def __init__(
        self,
        data_file: Path = DATA_FILE,
        legacy_data_file: Path = LEGACY_DATA_FILE,
    ) -> None:
        self.data_file = data_file
        self.legacy_data_file = legacy_data_file

    def load(self) -> AppState:
        """Load saved state or create first-run defaults."""

        self._adopt_legacy_data()
        if not self.data_file.exists():
            LOGGER.info("Creating default state at %s", self.data_file)
            state = build_default_state()
            self.save(state)
            return state

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except json.JSONDecodeError:
            backup = self._backup_corrupt_file()
            LOGGER.warning(
                "State file was corrupt. Backed it up to %s",
                backup,
            )
            state = build_default_state()
            self.save(state)
            return state

        state = AppState.from_dict(payload)
        migrated = self._migrate(state)
        if migrated:
            self.save(state)
        return state

    def save(self, state: AppState) -> None:
        """Persist state as formatted JSON."""

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.data_file.with_suffix(".json.tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(state.to_dict(), file, indent=2, sort_keys=True)
            file.write("\n")
        temp_file.replace(self.data_file)

    def _migrate(self, state: AppState) -> bool:
        """Apply lightweight schema migrations.

        User-created goals and navigation items live in this file, so future
        app updates should evolve the schema here rather than replacing data.
        """

        if state.schema_version >= SCHEMA_VERSION:
            return False

        state.schema_version = SCHEMA_VERSION
        return True

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
