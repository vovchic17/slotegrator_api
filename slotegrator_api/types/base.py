from abc import ABC

from pydantic import BaseModel


class SlotegratorObject(BaseModel, ABC):
    """Base Slotegrator object."""
