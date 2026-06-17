"""Framework for checking GitHub releases without touching user data."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from ancient_all_in_one.config import APP_VERSION, GITHUB_OWNER, GITHUB_REPO


@dataclass(frozen=True, slots=True)
class UpdateResult:
    """Result of an update check."""

    current_version: str
    latest_version: str | None
    update_available: bool
    message: str
    release_url: str | None = None
    release_name: str | None = None
    release_notes: str | None = None

    @property
    def has_release_url(self) -> bool:
        """Return whether the result can send users to a release page."""

        return bool(self.release_url)


class UpdateChecker:
    """Check GitHub releases for newer versions."""

    def __init__(
        self,
        owner: str = GITHUB_OWNER,
        repo: str = GITHUB_REPO,
        current_version: str = APP_VERSION,
    ) -> None:
        self.owner = owner
        self.repo = repo
        self.current_version = current_version

    def check(self) -> UpdateResult:
        """Return update status from the latest GitHub release."""

        if self.owner == "your-github-user":
            return UpdateResult(
                current_version=self.current_version,
                latest_version=None,
                update_available=False,
                message="Update checker is ready. Add your GitHub owner/repo.",
            )

        url = (
            "https://api.github.com/repos/"
            f"{self.owner}/{self.repo}/releases/latest"
        )

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return UpdateResult(
                current_version=self.current_version,
                latest_version=None,
                update_available=False,
                message=f"Could not check for updates: {exc}",
            )

        latest = str(payload.get("tag_name", "")).lstrip("v")
        is_newer = self._is_newer_version(latest, self.current_version)
        release_url = payload.get("html_url")
        release_name = payload.get("name") or payload.get("tag_name")
        release_notes = self._clean_release_notes(payload.get("body", ""))

        return UpdateResult(
            current_version=self.current_version,
            latest_version=latest,
            update_available=is_newer,
            message=(
                "Update available."
                if is_newer
                else "You are running the latest version."
            ),
            release_url=release_url,
            release_name=release_name,
            release_notes=release_notes,
        )

    @staticmethod
    def _is_newer_version(latest: str, current: str) -> bool:
        """Compare simple dotted numeric versions."""

        def parts(version: str) -> tuple[int, ...]:
            numeric_parts = re.findall(r"\d+", version)
            return tuple(int(part) for part in numeric_parts[:3])

        return parts(latest) > parts(current)

    @staticmethod
    def _clean_release_notes(notes: str, max_length: int = 700) -> str:
        """Normalize release notes for compact in-app display."""

        cleaned = notes.strip()
        if len(cleaned) <= max_length:
            return cleaned
        return f"{cleaned[:max_length].rstrip()}..."
