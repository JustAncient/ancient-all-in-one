"""Application configuration constants."""

import os
from pathlib import Path

from ancient_all_in_one import __version__

APP_VERSION = __version__
APP_BASE_NAME = "Ancient All-in-One"
APP_NAME = f"{APP_BASE_NAME} v{APP_VERSION}"
SCHEMA_VERSION = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEGACY_USER_DATA_DIR = PROJECT_ROOT / "user_data"
LEGACY_DATA_FILE = LEGACY_USER_DATA_DIR / "tracker_data.json"

_LOCAL_APP_DATA = os.environ.get("LOCALAPPDATA")
if _LOCAL_APP_DATA:
    USER_DATA_DIR = Path(_LOCAL_APP_DATA) / APP_BASE_NAME
else:
    USER_DATA_DIR = LEGACY_USER_DATA_DIR

DATA_FILE = USER_DATA_DIR / "tracker_data.json"
LOG_DIR = USER_DATA_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

GITHUB_OWNER = "JustAncient"
GITHUB_REPO = "ancient-all-in-one"
