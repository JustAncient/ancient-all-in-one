"""Application configuration constants."""

from pathlib import Path

from ancient_all_in_one import __version__

APP_VERSION = __version__
APP_BASE_NAME = "Ancient All-in-One"
APP_NAME = f"{APP_BASE_NAME} v{APP_VERSION}"
SCHEMA_VERSION = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
USER_DATA_DIR = PROJECT_ROOT / "user_data"
DATA_FILE = USER_DATA_DIR / "tracker_data.json"

# Replace these when your GitHub repository is ready.
GITHUB_OWNER = "JustAncient"
GITHUB_REPO = "ancient-all-in-one"
