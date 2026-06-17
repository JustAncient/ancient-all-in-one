"""Application bootstrap."""

from maplestory_tracker.services.storage import StateStore
from maplestory_tracker.ui.main_window import MainWindow


def main() -> None:
    """Start the desktop application."""

    store = StateStore()
    state = store.load()
    window = MainWindow(state=state, store=store)
    window.mainloop()
