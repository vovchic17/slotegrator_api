from datetime import datetime
from http import HTTPMethod

from slotegrator_api.types import FreevoucherSet

from .base import SlotegratorMethod


class SetFreevoucherCampaign(SlotegratorMethod[FreevoucherSet]):
    """Set freevoucher campaign method."""

    __return_type__ = FreevoucherSet
    __method_path__ = "/freevouchers/set"
    __http_method__ = HTTPMethod.POST

    player_id: str
    title: str
    currency: str
    initial_balance: float
    max_winnings: float
    valid_until: datetime
    voucher_id: str
    table_ids: list[str]
    short_terms: str | None
    terms_and_conds: str | None
