from http import HTTPMethod
from typing import Literal

from slotegrator_api.types import CommaList, GameTag, Items

from .base import SlotegratorMethod


class GetGameTags(SlotegratorMethod[Items[GameTag]]):
    """Get game tags method."""

    __return_type__ = Items[GameTag]
    __method_path__ = "/game-tags"
    __http_method__ = HTTPMethod.GET

    expand: CommaList[Literal["category"]] | None = None
    page: int | None = None
