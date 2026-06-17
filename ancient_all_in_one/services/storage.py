"""Persistence for user-owned tracker data."""

from __future__ import annotations

import json
from pathlib import Path

from ancient_all_in_one.config import DATA_FILE, SCHEMA_VERSION
from ancient_all_in_one.data.default_state import build_default_state
from ancient_all_in_one.models import AppState


class StateStore:
    """Load, migrate, and save tracker state."""

    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self.data_file = data_file

    def load(self) -> AppState:
        """Load saved state or create first-run defaults."""

        if not self.data_file.exists():
            state = build_default_state()
            self.save(state)
            return state

        with self.data_file.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        state = AppState.from_dict(payload)
        migrated = self._migrate(state)
        if migrated:
            self.save(state)
        return state

    def save(self, state: AppState) -> None:
        """Persist state as formatted JSON."""

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(state.to_dict(), file, indent=2, sort_keys=True)
            file.write("\n")

    def _migrate(self, state: AppState) -> bool:
        """Apply lightweight schema migrations.

        User-created goals and navigation items live in this file, so future
        app updates should evolve the schema here rather than replacing data.
        """

        if state.schema_version >= SCHEMA_VERSION:
            return False

        state.schema_version = SCHEMA_VERSION
        return True
