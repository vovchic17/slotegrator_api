from datetime import datetime

from .base import SlotegratorObject


class FreespinCampaign(SlotegratorObject):
    """Freespin campaign object."""

    player_id: str
    currency: str
    quantity: int
    quantity_left: int
    valid_from: datetime
    valid_until: datetime
    freespin_id: str
    bet_id: int
    total_bet_id: int
    denomination: float
    game_uuid: str
    status: str
    is_canceled: bool
    total_win: float
