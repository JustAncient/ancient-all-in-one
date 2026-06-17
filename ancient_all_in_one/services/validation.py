"""Validation for saved tracker state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ancient_all_in_one.data.default_state import build_default_state


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Validated state payload and any validation notes."""

    payload: dict[str, Any]
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """Return whether validation had to repair or replace anything."""

        return bool(self.errors or self.warnings)


def validate_state_payload(payload: Any) -> ValidationResult:
    """Validate and normalize raw JSON state before model loading."""

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        errors.append("State file root must be a JSON object.")
        return ValidationResult(
            payload=build_default_state().to_dict(),
            errors=errors,
            warnings=warnings,
        )

    default_payload = build_default_state().to_dict()
    cleaned: dict[str, Any] = {}

    schema_version = payload.get("schema_version", default_payload["schema_version"])
    if isinstance(schema_version, int) and schema_version > 0:
        cleaned["schema_version"] = schema_version
    else:
        warnings.append("Invalid schema_version; defaulted to current schema.")
        cleaned["schema_version"] = default_payload["schema_version"]

    navigation = payload.get("navigation")
    if isinstance(navigation, list):
        cleaned_navigation = [
            item
            for item in (_clean_nav_item(item, warnings) for item in navigation)
            if item
        ]
    else:
        cleaned_navigation = []
        warnings.append("navigation must be a list; restored default navigation.")

    if not cleaned_navigation:
        cleaned_navigation = default_payload["navigation"]
        warnings.append("No valid navigation items found; restored default navigation.")
    cleaned["navigation"] = cleaned_navigation

    goals = payload.get("goals", {})
    if isinstance(goals, dict):
        cleaned["goals"] = {
            str(goal_id): goal
            for goal_id, goal in goals.items()
            if isinstance(goal, dict)
        }
        if len(cleaned["goals"]) != len(goals):
            warnings.append("Ignored malformed goal entries.")
    else:
        cleaned["goals"] = {}
        warnings.append("goals must be an object; restored empty goals.")

    daily_weekly = payload.get("daily_weekly", default_payload["daily_weekly"])
    if isinstance(daily_weekly, dict):
        cleaned["daily_weekly"] = daily_weekly
    else:
        cleaned["daily_weekly"] = default_payload["daily_weekly"]
        warnings.append("daily_weekly must be an object; restored defaults.")

    return ValidationResult(payload=cleaned, errors=errors, warnings=warnings)


def _clean_nav_item(item: Any, warnings: list[str]) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        warnings.append("Ignored non-object navigation item.")
        return None

    title = item.get("title")
    item_type = item.get("item_type")
    if not isinstance(title, str) or not title.strip():
        warnings.append("Ignored navigation item without a title.")
        return None
    if not isinstance(item_type, str) or not item_type.strip():
        warnings.append(f"Ignored navigation item {title!r} without an item_type.")
        return None

    children = item.get("children", [])
    if not isinstance(children, list):
        warnings.append(
            f"Navigation item {title!r} had invalid children; reset to empty."
        )
        children = []

    cleaned_children = [
        child
        for child in (_clean_nav_item(child, warnings) for child in children)
        if child
    ]

    return {
        "title": title.strip(),
        "item_type": item_type.strip(),
        "item_id": str(item.get("item_id", "")).strip() or None,
        "children": cleaned_children,
        "can_add_child": bool(item.get("can_add_child", False)),
    }
