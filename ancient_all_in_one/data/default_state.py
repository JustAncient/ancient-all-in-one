"""Default state for first-time users."""

from ancient_all_in_one.config import SCHEMA_VERSION
from ancient_all_in_one.models import AppState, NavItem


def build_default_state() -> AppState:
    """Create starter data for the tracker."""

    level_one_hexa = NavItem(title="Lv1 Hexa", item_type="goal")
    sol_hecate = NavItem(title="Sol Hecate", item_type="goal")

    return AppState(
        schema_version=SCHEMA_VERSION,
        navigation=[
            NavItem(title="Daily/Weekly", item_type="daily_weekly"),
            NavItem(
                title="Goals",
                item_type="goal_group",
                children=[level_one_hexa, sol_hecate],
                can_add_child=True,
            ),
        ],
        goals={
            level_one_hexa.item_id: {
                "title": level_one_hexa.title,
                "notes": "",
                "tasks": [],
            },
            sol_hecate.item_id: {
                "title": sol_hecate.title,
                "notes": "",
                "tasks": [],
            },
        },
        daily_weekly={
            "dailies": [],
            "weeklies": [],
        },
    )
