from pydantic import BaseModel


class SlotegratorCallback(BaseModel):
    """Slotegrator callback base model."""

    action: str
