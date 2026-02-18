from typing import Literal

from .base import SlotegratorCallback


class Bet(SlotegratorCallback):
    """Bet method."""

    action: Literal["bet"]
    amount: float
    currency: str
    game_uuid: str
    player_id: str
    transaction_id: str
    session_id: str
    type: Literal["bet", "tip", "freespin"]
    freespin_id: str
    quantity: int
    round_id: str | None
    finished: bool | None
    transaction_datetime: str | None
    casino_request_retry_count: int | None
