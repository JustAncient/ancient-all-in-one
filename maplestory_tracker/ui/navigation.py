"""Left navigation components."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from maplestory_tracker.models import NavItem

SelectCallback = Callable[[NavItem], None]
AddCallback = Callable[[NavItem], None]


class NavigationSidebar(ttk.Frame):
    """Codex-style left navigation with expandable sections."""

    def __init__(
        self,
        master: tk.Misc,
        on_select: SelectCallback,
        on_add_child: AddCallback,
    ) -> None:
        super().__init__(master, style="Sidebar.TFrame", padding=(8, 8))
        self.on_select = on_select
        self.on_add_child = on_add_child
        self._selected_id: str | None = None
        self._items: list[NavItem] = []

        self.columnconfigure(0, weight=1)

    def set_items(self, items: list[NavItem]) -> None:
        """Replace visible navigation items."""

        self._items = items
        self._render()

    def set_selected(self, item_id: str) -> None:
        """Mark a navigation item as selected."""

        self._selected_id = item_id
        self._render()

    def _render(self) -> None:
        for child in self.winfo_children():
            child.destroy()

        row = 0
        for item in self._items:
            self._render_item(item, row=row, depth=0)
            row += 1
            for child_item in item.children:
                self._render_item(child_item, row=row, depth=1)
                row += 1

    def _render_item(self, item: NavItem, row: int, depth: int) -> None:
        selected = item.item_id == self._selected_id
        style = "Selected.NavItem.TFrame" if selected else "NavItem.TFrame"
        item_frame = ttk.Frame(self, style=style, padding=(8, 3))
        item_frame.grid(row=row, column=0, sticky="ew", pady=1)
        item_frame.columnconfigure(0, weight=1)

        title = ttk.Label(
            item_frame,
            text=item.title,
            style="Selected.NavLabel.TLabel" if selected else "NavLabel.TLabel",
        )
        title.grid(row=0, column=0, sticky="ew", padx=(depth * 16, 4))

        if item.can_add_child:
            ttk.Button(
                item_frame,
                text="+",
                width=3,
                style="Icon.TButton",
                command=lambda nav_item=item: self.on_add_child(nav_item),
            ).grid(row=0, column=1, sticky="e")

        self._bind_select(item_frame, item)
        self._bind_select(title, item)

    def _bind_select(self, widget: tk.Widget, item: NavItem) -> None:
        widget.bind("<Button-1>", lambda _event: self.on_select(item))
