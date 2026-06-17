"""Application bootstrap."""

from ancient_all_in_one.services.storage import StateStore
from ancient_all_in_one.ui.main_window import MainWindow


def main() -> None:
    """Start the desktop application."""

    store = StateStore()
    state = store.load()
    window = MainWindow(state=state, store=store)
    window.mainloop()
