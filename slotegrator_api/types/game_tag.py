from .base import SlotegratorObject


class GameTagCategory(SlotegratorObject):
    """Game tag category object."""

    code: str
    label: str


class GameTag(SlotegratorObject):
    """Game tag object."""

    code: str
    label: str
    category: GameTagCategory | None = None
