from .base import SlotegratorObject


class FreespinLimit(SlotegratorObject):
    """Freespin limit object."""

    quantity: int
    currency: str
    providers: list[str]
