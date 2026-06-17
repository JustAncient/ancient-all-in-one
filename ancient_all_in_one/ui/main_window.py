"""Main application window."""

from __future__ import annotations

import logging
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from types import TracebackType

from ancient_all_in_one.config import APP_NAME
from ancient_all_in_one.models import AppState, NavItem
from ancient_all_in_one.services.diagnostics import build_diagnostics
from ancient_all_in_one.services.settings import AppSettings, SettingsStore
from ancient_all_in_one.services.storage import StateStore
from ancient_all_in_one.services.updates import UpdateChecker, UpdateResult
from ancient_all_in_one.ui.navigation import NavigationSidebar
from ancient_all_in_one.ui.pages import PageFactory

LOGGER = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    """Desktop shell for the progression tracker."""

    def __init__(
        self,
        state: AppState,
        store: StateStore,
        settings: AppSettings | None = None,
        settings_store: SettingsStore | None = None,
    ) -> None:
        super().__init__()
        self.state = state
        self.store = store
        self.settings = settings or AppSettings()
        self.settings_store = settings_store
        self.selected_item: NavItem | None = None
        self.content_frame: ttk.Frame | None = None

        self.title(APP_NAME)
        self.geometry(self.settings.window_geometry)
        self.minsize(880, 560)
        self.protocol("WM_DELETE_WINDOW", self._close)

        self._configure_styles()
        self._build_menu_bar()
        self._build_layout()

        first_item = self.state.navigation[0]
        self.select_item(first_item)
        if self.settings.check_for_updates_on_startup:
            self.after(600, self._check_for_updates_on_open)

    def select_item(self, item: NavItem) -> None:
        """Show a navigation item in the main content area."""

        self.selected_item = item
        self.sidebar.set_selected(item.item_id)

        if self.content_frame is not None:
            self.content_frame.destroy()

        factory = PageFactory(
            master=self.workspace,
            state=self.state,
            on_save=self.save_state,
        )
        self.content_frame = factory.build(item)
        self.content_frame.grid(row=0, column=0, sticky="nsew")

    def add_child_item(self, parent: NavItem) -> None:
        """Prompt for a submenu item and persist it."""

        title = simpledialog.askstring(
            title="New Goal",
            prompt="Goal name:",
            parent=self,
        )
        if title is None:
            return

        cleaned_title = title.strip()
        if not cleaned_title:
            messagebox.showwarning("Goal name required", "Enter a goal name.")
            return

        new_item = NavItem(title=cleaned_title, item_type="goal")
        parent.children.append(new_item)
        self.state.goals[new_item.item_id] = {
            "title": new_item.title,
            "notes": "",
            "tasks": [],
        }
        self.save_state()
        self.sidebar.set_items(self.state.navigation)
        self.select_item(new_item)

    def save_state(self) -> None:
        """Persist current user data."""

        self.store.save(self.state)

    def _build_menu_bar(self) -> None:
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Save", command=self.save_state)
        file_menu.add_separator()
        file_menu.add_command(label="Export Data...", command=self._export_data)
        file_menu.add_command(label="Import Data...", command=self._import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._close)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=False)
        edit_menu.add_command(
            label="Add Goal",
            command=self._add_goal_from_menu,
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menu_bar, tearoff=False)
        view_menu.add_command(label="Daily/Weekly", command=self._show_home)
        menu_bar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(
            label="Check for Updates",
            command=self._show_update_result,
        )
        help_menu.add_command(label="Diagnostics", command=self._show_diagnostics)
        help_menu.add_command(label="About", command=self._show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def _build_layout(self) -> None:
        self.configure(background="#181a1f")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = NavigationSidebar(
            self,
            on_select=self.select_item,
            on_add_child=self.add_child_item,
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.configure(width=230)
        self.sidebar.grid_propagate(False)
        self.sidebar.set_items(self.state.navigation)

        self.workspace = ttk.Frame(self, style="Content.TFrame")
        self.workspace.grid(row=0, column=1, sticky="nsew")
        self.workspace.columnconfigure(0, weight=1)
        self.workspace.rowconfigure(0, weight=1)

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Sidebar.TFrame", background="#1f2229")
        style.configure("Content.TFrame", background="#f6f7f9")
        style.configure("NavItem.TFrame", background="#1f2229")
        style.configure("Selected.NavItem.TFrame", background="#303540")
        style.configure(
            "NavLabel.TLabel",
            background="#1f2229",
            foreground="#d7dce5",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Selected.NavLabel.TLabel",
            background="#303540",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("Icon.TButton", padding=(2, 0))
        style.configure(
            "Title.TLabel",
            background="#f6f7f9",
            foreground="#16181d",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#f6f7f9",
            foreground="#596070",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Body.TLabel",
            background="#f6f7f9",
            foreground="#252932",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Section.TLabel",
            background="#f6f7f9",
            foreground="#252932",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("TLabelframe", background="#f6f7f9")
        style.configure("TLabelframe.Label", background="#f6f7f9")

    def _export_data(self) -> None:
        export_path = filedialog.asksaveasfilename(
            parent=self,
            title="Export Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="ancient-all-in-one-data.json",
        )
        if not export_path:
            return

        saved_path = self.store.export_to(Path(export_path))
        messagebox.showinfo(
            "Export Complete",
            f"Data exported to:\n{saved_path}",
            parent=self,
        )

    def _import_data(self) -> None:
        import_path = filedialog.askopenfilename(
            parent=self,
            title="Import Data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not import_path:
            return

        confirmed = messagebox.askyesno(
            "Import Data",
            "Importing replaces current tracker data after creating a backup. "
            "Continue?",
            parent=self,
        )
        if not confirmed:
            return

        self.state = self.store.import_from(Path(import_path))
        self.sidebar.set_items(self.state.navigation)
        self.select_item(self.state.navigation[0])
        messagebox.showinfo(
            "Import Complete", "Data imported successfully.", parent=self
        )

    def _add_goal_from_menu(self) -> None:
        goals = self._find_first_item("goal_group")
        if goals is not None:
            self.add_child_item(goals)

    def _show_home(self) -> None:
        home = self._find_first_item("daily_weekly")
        if home is not None:
            self.select_item(home)

    def _show_about(self) -> None:
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\nA modular all-in-one progression tracker.",
            parent=self,
        )

    def _show_diagnostics(self) -> None:
        diagnostics = build_diagnostics()
        messagebox.showinfo(
            "Diagnostics",
            diagnostics.to_message(),
            parent=self,
        )

    def report_callback_exception(
        self,
        exc: type[BaseException],
        value: BaseException,
        trace: TracebackType | None,
    ) -> None:
        LOGGER.exception(
            "Unhandled UI callback error",
            exc_info=(exc, value, trace),
        )
        messagebox.showerror(
            "Unexpected Error",
            "An unexpected error occurred. Check the app log for details.",
            parent=self,
        )

    def _show_update_result(self) -> None:
        result = UpdateChecker().check()
        self._show_update_dialog(result)

    def _check_for_updates_on_open(self) -> None:
        result = UpdateChecker().check()
        if result.update_available:
            self._show_update_dialog(result)

    def _show_update_dialog(self, result: UpdateResult) -> None:
        detail = [
            result.message,
            f"Current version: {result.current_version}",
        ]
        if result.latest_version:
            detail.append(f"Latest version: {result.latest_version}")
        if result.release_name:
            detail.append(f"Release: {result.release_name}")
        if result.release_notes:
            detail.append("")
            detail.append(result.release_notes)

        if result.update_available and result.has_release_url:
            detail.append("")
            detail.append("Open the release page to download the update?")
            should_open = messagebox.askyesno(
                "Update Available",
                "\n".join(detail),
                parent=self,
            )
            if should_open and result.release_url is not None:
                webbrowser.open(result.release_url)
            return

        messagebox.showinfo("Updates", "\n".join(detail), parent=self)

    def _close(self) -> None:
        self.settings.window_geometry = self.geometry()
        if self.settings_store is not None:
            self.settings_store.save(self.settings)
        self.destroy()

    def _find_first_item(self, item_type: str) -> NavItem | None:
        for item in self.state.navigation:
            if item.item_type == item_type:
                return item
            for child in item.children:
                if child.item_type == item_type:
                    return child
        return None
