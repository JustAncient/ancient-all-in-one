"""Application bootstrap."""

import logging

from ancient_all_in_one.config import APP_NAME
from ancient_all_in_one.services.storage import StateStore
from ancient_all_in_one.services.telemetry import setup_logging
from ancient_all_in_one.ui.main_window import MainWindow

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Start the desktop application."""

    setup_logging()
    LOGGER.info("Starting %s", APP_NAME)

    store = StateStore()
    state = store.load()
    window = MainWindow(state=state, store=store)
    window.mainloop()
    LOGGER.info("Application closed")
