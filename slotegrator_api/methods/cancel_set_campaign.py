from http import HTTPMethod

from slotegrator_api.types import CampaignCancel

from .base import SlotegratorMethod


class CancelSetCampaign(SlotegratorMethod[CampaignCancel]):
    """Cancel set campaign method."""

    __return_type__ = CampaignCancel
    __method_path__ = "/freespins/cancel"
    __http_method__ = HTTPMethod.POST

    freespin_id: str
