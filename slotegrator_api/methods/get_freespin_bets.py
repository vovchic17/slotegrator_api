from http import HTTPMethod

from slotegrator_api.types import FreespinBets

from .base import SlotegratorMethod


class GetFreespinBets(SlotegratorMethod[FreespinBets]):
    """Get freespin bets method."""

    __return_type__ = FreespinBets
    __method_path__ = "/freespins/bets"
    __http_method__ = HTTPMethod.GET

    game_uuid: str
    currency: str
