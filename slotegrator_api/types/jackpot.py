from .base import SlotegratorObject


class Jackpot(SlotegratorObject):
    """Jackpot object."""

    name: str | None
    amount: float
    currency: str
    provider: str
