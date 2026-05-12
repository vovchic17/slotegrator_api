from abc import ABC
from http import HTTPMethod
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from slotegrator_api.types import SlotegratorType


class SlotegratorMethod[T: SlotegratorType](BaseModel, ABC):
    """Base Slotegrator method."""

    __return_type__: ClassVar[type[T]]
    __method_path__: ClassVar[str]
    __http_method__: ClassVar[HTTPMethod]

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def get_url(self, base_url: str) -> str:
        """Get method url."""
        return f"{base_url}{self.__method_path__}"
