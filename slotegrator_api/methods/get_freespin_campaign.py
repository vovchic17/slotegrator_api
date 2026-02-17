from http import HTTPMethod

from slotegrator_api.types import FreespinCampaign

from .base import SlotegratorMethod


class GetFreespinCampaign(SlotegratorMethod[FreespinCampaign]):
    """Get freespin campaign method."""

    __return_type__ = FreespinCampaign
    __method_path__ = "/freespins/get"
    __http_method__ = HTTPMethod.GET

    freespin_id: str
