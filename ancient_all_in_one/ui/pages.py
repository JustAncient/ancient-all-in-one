"""Content pages rendered in the main workspace."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from ancient_all_in_one.models import AppState, NavItem

SaveCallback = Callable[[], None]


class PageFactory:
    """Create page frames for selected navigation items."""

    def __init__(
        self,
        master: tk.Misc,
        state: AppState,
        on_save: SaveCallback,
    ) -> None:
        self.master = master
        self.state = state
        self.on_save = on_save

    def build(self, item: NavItem) -> ttk.Frame:
        """Build the correct content page for a navigation item."""

        if item.item_type == "daily_weekly":
            return DailyWeeklyPage(self.master, self.state, self.on_save)
        if item.item_type == "goal":
            return GoalPage(self.master, self.state, item, self.on_save)
        if item.item_type == "goal_group":
            return GoalGroupPage(self.master, self.state)
        return PlaceholderPage(self.master, item)


class BasePage(ttk.Frame):
    """Shared page helpers."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, style="Content.TFrame", padding=24)
        self.columnconfigure(0, weight=1)

    def add_title(self, title: str, subtitle: str) -> None:
        heading = ttk.Label(self, text=title, style="Title.TLabel")
        heading.grid(row=0, column=0, sticky="w")

        detail = ttk.Label(self, text=subtitle, style="Subtitle.TLabel")
        detail.grid(row=1, column=0, sticky="w", pady=(4, 18))


class DailyWeeklyPage(BasePage):
    """Daily and weekly tracker placeholder page."""

    def __init__(
        self,
        master: tk.Misc,
        state: AppState,
        on_save: SaveCallback,
    ) -> None:
        super().__init__(master)
        self.state = state
        self.on_save = on_save

        self.add_title(
            "Daily/Weekly",
            "Track recurring game tasks here as modules are added.",
        )

        dailies = ttk.LabelFrame(self, text="Dailies", padding=12)
        dailies.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        dailies.columnconfigure(0, weight=1)
        ttk.Label(
            dailies,
            text="Daily task rows will live here: bosses, symbols, events.",
            style="Body.TLabel",
        ).grid(row=0, column=0, sticky="w")

        weeklies = ttk.LabelFrame(self, text="Weeklies", padding=12)
        weeklies.grid(row=3, column=0, sticky="ew")
        weeklies.columnconfigure(0, weight=1)
        ttk.Label(
            weeklies,
            text="Weekly reset content can be added without changing nav code.",
            style="Body.TLabel",
        ).grid(row=0, column=0, sticky="w")


class GoalGroupPage(BasePage):
    """Overview page for the Goals section."""

    def __init__(self, master: tk.Misc, state: AppState) -> None:
        super().__init__(master)
        self.add_title(
            "Goals",
            "Use the + button beside Goals to create more progression pages.",
        )

        goal_count = len(state.goals)
        ttk.Label(
            self,
            text=f"{goal_count} goal pages are currently saved.",
            style="Body.TLabel",
        ).grid(row=2, column=0, sticky="w")


class GoalPage(BasePage):
    """Editable goal page for user-created progression goals."""

    def __init__(
        self,
        master: tk.Misc,
        state: AppState,
        item: NavItem,
        on_save: SaveCallback,
    ) -> None:
        super().__init__(master)
        self.state = state
        self.item = item
        self.on_save = on_save

        goal = self.state.goals.setdefault(
            item.item_id,
            {"title": item.title, "notes": "", "tasks": []},
        )

        self.add_title(item.title, "Goal notes and task widgets can grow here.")

        ttk.Label(self, text="Notes", style="Section.TLabel").grid(
            row=2,
            column=0,
            sticky="w",
        )

        self.notes = tk.Text(
            self,
            height=10,
            wrap="word",
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=10,
        )
        self.notes.insert("1.0", goal.get("notes", ""))
        self.notes.grid(row=3, column=0, sticky="nsew", pady=(6, 12))
        self.rowconfigure(3, weight=1)

        save_button = ttk.Button(
            self,
            text="Save Goal",
            command=self._save_goal,
        )
        save_button.grid(row=4, column=0, sticky="e")

    def _save_goal(self) -> None:
        notes = self.notes.get("1.0", "end").strip()
        self.state.goals[self.item.item_id] = {
            **self.state.goals.get(self.item.item_id, {}),
            "title": self.item.title,
            "notes": notes,
        }
        self.on_save()


class PlaceholderPage(BasePage):
    """Fallback page for future module types."""

    def __init__(self, master: tk.Misc, item: NavItem) -> None:
        super().__init__(master)
        self.add_title(item.title, "This module is ready for implementation.")
