from http import HTTPMethod
from typing import Literal

from slotegrator_api.types import PreparedGame

from .base import SlotegratorMethod


class InitGame(SlotegratorMethod[PreparedGame]):
    """Init game method."""

    __return_type__ = PreparedGame
    __method_path__ = "/games/init"
    __http_method__ = HTTPMethod.POST

    game_uuid: str
    player_id: str
    player_name: str
    currency: str
    session_id: str
    device: Literal["desktop", "mobile"] | None
    return_url: str | None
    language: str | None
    email: str | None
    lobby_data: str | None
