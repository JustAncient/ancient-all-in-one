"""Application configuration constants."""

from pathlib import Path

from maplestory_tracker import __version__

APP_NAME = "MapleStory GMS Tracker"
APP_VERSION = __version__
SCHEMA_VERSION = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
USER_DATA_DIR = PROJECT_ROOT / "user_data"
DATA_FILE = USER_DATA_DIR / "tracker_data.json"

# Replace these when your GitHub repository is ready.
GITHUB_OWNER = "JustAncient"
GITHUB_REPO = "maplestory-tracker"
