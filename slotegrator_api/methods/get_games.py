from http import HTTPMethod
from typing import Literal

from slotegrator_api.types import CommaList, Game, Items

from .base import SlotegratorMethod


class GetGames(SlotegratorMethod[Items[Game]]):
    """Get games method."""

    __return_type__ = Items[Game]
    __method_path__ = "/games"
    __http_method__ = HTTPMethod.GET

    expand: (
        CommaList[Literal["tags", "parameters", "images", "related_games"]]
        | None
    ) = None
    page: int | None = None
