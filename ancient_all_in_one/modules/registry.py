"""Registry of available game modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameModule:
    """Metadata for a game or shared tracking module."""

    module_id: str
    name: str
    description: str
    nav_item_types: tuple[str, ...]


_REGISTERED_MODULES = (
    GameModule(
        module_id="general",
        name="General Tracking",
        description="Shared daily, weekly, and goal tracking primitives.",
        nav_item_types=("daily_weekly", "goal_group", "goal"),
    ),
)


def get_registered_modules() -> tuple[GameModule, ...]:
    """Return all registered modules."""

    return _REGISTERED_MODULES


def get_module(module_id: str) -> GameModule | None:
    """Find a registered module by id."""

    for module in _REGISTERED_MODULES:
        if module.module_id == module_id:
            return module
    return None
