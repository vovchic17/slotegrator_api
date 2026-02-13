from http import HTTPMethod

from slotegrator_api.types import Jackpot

from .base import SlotegratorMethod


class GetJackpots(SlotegratorMethod[list[Jackpot]]):
    """Get jackpots method."""

    __return_type__ = list[Jackpot]
    __method_path__ = "/jackpots"
    __http_method__ = HTTPMethod.GET
