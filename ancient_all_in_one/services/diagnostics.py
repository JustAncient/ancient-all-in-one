"""Application diagnostics for support and debugging."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ancient_all_in_one.config import (
    APP_NAME,
    APP_VERSION,
    BACKUP_DIR,
    DATA_FILE,
    EXPORTS_DIR,
    GITHUB_OWNER,
    GITHUB_REPO,
    LOG_FILE,
    SCHEMA_VERSION,
    SETTINGS_FILE,
    USER_DATA_DIR,
)
from ancient_all_in_one.modules import get_registered_modules


@dataclass(frozen=True, slots=True)
class AppDiagnostics:
    """Important runtime paths and versions for troubleshooting."""

    app_name: str
    app_version: str
    schema_version: int
    user_data_dir: Path
    data_file: Path
    settings_file: Path
    backup_dir: Path
    exports_dir: Path
    log_file: Path
    github_owner: str
    github_repo: str
    registered_modules: tuple[str, ...]

    def to_message(self) -> str:
        """Format diagnostics for display in the desktop UI."""

        return "\n".join(
            [
                f"Application: {self.app_name}",
                f"Version: {self.app_version}",
                f"Schema version: {self.schema_version}",
                f"User data folder: {self.user_data_dir}",
                f"Data file: {self.data_file}",
                f"Settings file: {self.settings_file}",
                f"Backup folder: {self.backup_dir}",
                f"Exports folder: {self.exports_dir}",
                f"Log file: {self.log_file}",
                f"GitHub: {self.github_owner}/{self.github_repo}",
                f"Modules: {', '.join(self.registered_modules)}",
            ]
        )


def build_diagnostics() -> AppDiagnostics:
    """Build a diagnostics snapshot from current configuration."""

    modules = tuple(module.module_id for module in get_registered_modules())
    return AppDiagnostics(
        app_name=APP_NAME,
        app_version=APP_VERSION,
        schema_version=SCHEMA_VERSION,
        user_data_dir=USER_DATA_DIR,
        data_file=DATA_FILE,
        settings_file=SETTINGS_FILE,
        backup_dir=BACKUP_DIR,
        exports_dir=EXPORTS_DIR,
        log_file=LOG_FILE,
        github_owner=GITHUB_OWNER,
        github_repo=GITHUB_REPO,
        registered_modules=modules,
    )
