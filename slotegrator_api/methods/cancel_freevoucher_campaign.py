from http import HTTPMethod

from slotegrator_api.types import CampaignCancel

from .base import SlotegratorMethod


class CancelFreevoucherCampaign(SlotegratorMethod[CampaignCancel]):
    """Cancel freevoucher campaign method."""

    __return_type__ = CampaignCancel
    __method_path__ = "/freevouchers/cancel"
    __http_method__ = HTTPMethod.POST

    voucher_id: str
    reason: str
