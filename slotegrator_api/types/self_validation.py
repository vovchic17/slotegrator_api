from .base import SlotegratorObject


class SelfValidation(SlotegratorObject):
    """Self validation object."""

    success: bool
    log: list[str]
