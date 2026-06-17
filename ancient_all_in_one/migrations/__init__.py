"""Schema migration registry for saved tracker data."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

Migration = Callable[[dict[str, Any]], dict[str, Any]]
MIGRATIONS: dict[int, Migration] = {}


class MigrationError(RuntimeError):
    """Raised when saved data cannot be migrated safely."""


def migrate_payload(
    payload: dict[str, Any],
    target_schema_version: int,
) -> tuple[dict[str, Any], bool]:
    """Run registered migrations until payload reaches target schema."""

    current_version = payload.get("schema_version", 1)
    if not isinstance(current_version, int) or current_version < 1:
        current_version = 1

    if current_version > target_schema_version:
        raise MigrationError(
            "Saved data schema is newer than this app supports: "
            f"{current_version} > {target_schema_version}."
        )

    migrated = False
    while current_version < target_schema_version:
        migration = MIGRATIONS.get(current_version)
        if migration is None:
            raise MigrationError(
                "No migration registered for schema "
                f"{current_version} -> {current_version + 1}."
            )
        payload = migration(payload)
        current_version += 1
        payload["schema_version"] = current_version
        migrated = True

    return payload, migrated
