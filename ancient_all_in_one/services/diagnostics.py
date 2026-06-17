"""Application diagnostics for support and debugging."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ancient_all_in_one.config import (
    APP_NAME,
    APP_VERSION,
    DATA_FILE,
    GITHUB_OWNER,
    GITHUB_REPO,
    LOG_FILE,
    SCHEMA_VERSION,
    USER_DATA_DIR,
)


@dataclass(frozen=True, slots=True)
class AppDiagnostics:
    """Important runtime paths and versions for troubleshooting."""

    app_name: str
    app_version: str
    schema_version: int
    user_data_dir: Path
    data_file: Path
    log_file: Path
    github_owner: str
    github_repo: str

    def to_message(self) -> str:
        """Format diagnostics for display in the desktop UI."""

        return "\n".join(
            [
                f"Application: {self.app_name}",
                f"Version: {self.app_version}",
                f"Schema version: {self.schema_version}",
                f"User data folder: {self.user_data_dir}",
                f"Data file: {self.data_file}",
                f"Log file: {self.log_file}",
                f"GitHub: {self.github_owner}/{self.github_repo}",
            ]
        )


def build_diagnostics() -> AppDiagnostics:
    """Build a diagnostics snapshot from current configuration."""

    return AppDiagnostics(
        app_name=APP_NAME,
        app_version=APP_VERSION,
        schema_version=SCHEMA_VERSION,
        user_data_dir=USER_DATA_DIR,
        data_file=DATA_FILE,
        log_file=LOG_FILE,
        github_owner=GITHUB_OWNER,
        github_repo=GITHUB_REPO,
    )
