from typing import Literal

from .base import SlotegratorCallback


class RollbackTransaction(SlotegratorCallback):
    """Rollback transaction method."""

    action: Literal["bet", "win", "refund"]
    amount: float
    transaction_id: str
    type: Literal["bet", "win"]


class Rollback(SlotegratorCallback):
    """Rollback method."""

    action: Literal["rollback"]
    currency: str
    game_uuid: str
    player_id: str
    transaction_id: str
    rollback_transactions: list[RollbackTransaction]
    session_id: str
    type: str
    provider_round_id: str | None = None
    round_id: str | None = None
