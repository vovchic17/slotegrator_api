from http import HTTPMethod
from typing import Literal

from slotegrator_api.types import Lobby

from .base import SlotegratorMethod


class GetLobbyTables(SlotegratorMethod[Lobby]):
    """Get lobby tables method."""

    __return_type__ = Lobby
    __method_path__ = "/games/lobby"
    __http_method__ = HTTPMethod.GET

    game_uuid: str
    currency: str
    technology: Literal["html5", "flash"] | None = None
