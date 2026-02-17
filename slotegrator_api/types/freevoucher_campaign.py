from datetime import datetime

from .base import SlotegratorObject


class FreevoucherCampaign(SlotegratorObject):
    """Freevoucher campaign object."""

    player_id: str
    currency: str
    title: str
    state: str
    valid_from: datetime
    valid_until: datetime
    voucher_id: str
    playable: float
    winnings: float
