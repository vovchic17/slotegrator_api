from http import HTTPMethod
from typing import Literal

from slotegrator_api.types import PreparedGame

from .base import SlotegratorMethod


class InitDemoGame(SlotegratorMethod[PreparedGame]):
    """Init demo game method."""

    __return_type__ = PreparedGame
    __method_path__ = "/games/init-demo"
    __http_method__ = HTTPMethod.POST

    game_uuid: str
    device: Literal["desktop", "mobile"] | None
    return_url: str | None
    language: str | None
