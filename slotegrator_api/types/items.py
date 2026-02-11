from slotegrator_api.types import SlotegratorObject


class Items[T](SlotegratorObject):
    """Items model."""

    items: list[T]
