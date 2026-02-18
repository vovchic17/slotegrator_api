from datetime import UTC, datetime
from http import HTTPMethod

from pydantic import field_validator

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

    @field_validator("valid_until", mode="before")
    @classmethod
    def validate_valid_until(cls, v: int | str) -> datetime:
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=UTC)
        if isinstance(v, str) and v.isdigit():
            return datetime.fromtimestamp(int(v), tz=UTC)
        raise ValueError
