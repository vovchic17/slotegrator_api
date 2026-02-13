from .base import SlotegratorObject


class Limit(SlotegratorObject):
    """Limit object."""

    amount: str
    currency: str
    providers: list[str]
