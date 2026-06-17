"""Core data models used across the tracker."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class NavItem:
    """A sidebar item that can optionally contain child items."""

    title: str
    item_type: str
    item_id: str = field(default_factory=lambda: uuid4().hex)
    children: list["NavItem"] = field(default_factory=list)
    can_add_child: bool = False

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "NavItem":
        """Build a navigation item from saved JSON data."""

        children = [
            cls.from_dict(child) for child in payload.get("children", [])
        ]
        return cls(
            title=payload["title"],
            item_type=payload["item_type"],
            item_id=payload.get("item_id", uuid4().hex),
            children=children,
            can_add_child=payload.get("can_add_child", False),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize a navigation item for JSON storage."""

        return {
            "title": self.title,
            "item_type": self.item_type,
            "item_id": self.item_id,
            "children": [child.to_dict() for child in self.children],
            "can_add_child": self.can_add_child,
        }


@dataclass(slots=True)
class AppState:
    """User-owned state that should survive application updates."""

    schema_version: int
    navigation: list[NavItem]
    goals: dict[str, dict[str, Any]] = field(default_factory=dict)
    daily_weekly: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AppState":
        """Build application state from saved JSON data."""

        return cls(
            schema_version=payload.get("schema_version", 1),
            navigation=[
                NavItem.from_dict(item)
                for item in payload.get("navigation", [])
            ],
            goals=payload.get("goals", {}),
            daily_weekly=payload.get("daily_weekly", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize state for JSON storage."""

        return {
            "schema_version": self.schema_version,
            "navigation": [item.to_dict() for item in self.navigation],
            "goals": self.goals,
            "daily_weekly": self.daily_weekly,
        }
