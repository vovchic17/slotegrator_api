from typing import Literal

from .base import SlotegratorCallback


class Refund(SlotegratorCallback):
    """Refund method."""

    action: Literal["refund"]
    amount: float
    currency: str
    game_uuid: str
    player_id: str
    transaction_id: str
    session_id: str
    type: str | None = None
    bet_transaction_id: str
    freespin_id: str | None = None
    quantity: int | None = None
    round_id: str | None = None
    finished: bool | None = None
    transaction_datetime: str | None = None
    casino_request_retry_count: int | None = None
