from http import HTTPMethod

from slotegrator_api.types import FreevoucherCampaign

from .base import SlotegratorMethod


class GetFreevoucherCampaign(SlotegratorMethod[FreevoucherCampaign]):
    """Get freevoucher campaign method."""

    __return_type__ = FreevoucherCampaign
    __method_path__ = "/freevouchers/get"
    __http_method__ = HTTPMethod.GET

    voucher_id: str
