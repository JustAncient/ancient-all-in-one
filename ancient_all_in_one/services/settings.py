"""User preference storage separate from tracker progression data."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ancient_all_in_one.config import SETTINGS_FILE

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class AppSettings:
    """User preferences that should survive app restarts."""

    check_for_updates_on_startup: bool = True
    selected_game: str = "general"
    theme: str = "system"
    window_geometry: str = "1120x720"

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AppSettings:
        """Build settings from JSON with defensive defaults."""

        defaults = cls()
        return cls(
            check_for_updates_on_startup=bool(
                payload.get(
                    "check_for_updates_on_startup",
                    defaults.check_for_updates_on_startup,
                )
            ),
            selected_game=_clean_string(
                payload.get("selected_game"),
                defaults.selected_game,
            ),
            theme=_clean_string(payload.get("theme"), defaults.theme),
            window_geometry=_clean_string(
                payload.get("window_geometry"),
                defaults.window_geometry,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize settings for JSON storage."""

        return asdict(self)


class SettingsStore:
    """Load and save app preferences."""

    def __init__(self, settings_file: Path = SETTINGS_FILE) -> None:
        self.settings_file = settings_file

    def load(self) -> AppSettings:
        """Load settings or create defaults."""

        if not self.settings_file.exists():
            settings = AppSettings()
            self.save(settings)
            return settings

        try:
            with self.settings_file.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except json.JSONDecodeError:
            backup = self.settings_file.with_suffix(".corrupt.json")
            self.settings_file.replace(backup)
            LOGGER.warning("Settings were corrupt. Backed them up to %s", backup)
            settings = AppSettings()
            self.save(settings)
            return settings

        if not isinstance(payload, dict):
            LOGGER.warning("Settings root was not an object; restored defaults.")
            settings = AppSettings()
            self.save(settings)
            return settings

        settings = AppSettings.from_dict(payload)
        self.save(settings)
        return settings

    def save(self, settings: AppSettings) -> None:
        """Persist settings atomically."""

        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.settings_file.with_suffix(".json.tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(settings.to_dict(), file, indent=2, sort_keys=True)
            file.write("\n")
        temp_file.replace(self.settings_file)


def _clean_string(value: object, default: str) -> str:
    if not isinstance(value, str):
        return default
    cleaned = value.strip()
    return cleaned or default
