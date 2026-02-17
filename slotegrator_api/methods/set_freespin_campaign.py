from http import HTTPMethod

from slotegrator_api.types import FreespinSet

from .base import SlotegratorMethod


class SetFreespinCampaign(SlotegratorMethod[FreespinSet]):
    """Set freespin campaign method."""

    __return_type__ = FreespinSet
    __method_path__ = "/freespins/set"
    __http_method__ = HTTPMethod.POST

    player_id: str
    player_name: str
    currency: str
    quantity: int
    valid_from: int
    valid_until: int
    freespin_id: str
    bet_id: int | None
    total_bet_id: int | None
    denomination: float | None
    game_uuid: str
