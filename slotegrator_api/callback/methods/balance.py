from typing import Literal

from .base import SlotegratorCallback


class Balance(SlotegratorCallback):
    """Balance method."""

    action: Literal["balance"]
    player_id: str
    currency: str
    session_id: str | None = None
