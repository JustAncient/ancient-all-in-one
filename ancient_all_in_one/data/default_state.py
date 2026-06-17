"""Default state for first-time users."""

from ancient_all_in_one.config import SCHEMA_VERSION
from ancient_all_in_one.models import AppState, NavItem


def build_default_state() -> AppState:
    """Create starter data for the tracker."""

    return AppState(
        schema_version=SCHEMA_VERSION,
        navigation=[
            NavItem(title="Daily/Weekly", item_type="daily_weekly"),
            NavItem(
                title="Goals",
                item_type="goal_group",
                children=[],
                can_add_child=True,
            ),
        ],
        goals={},
        daily_weekly={
            "dailies": [],
            "weeklies": [],
        },
    )
