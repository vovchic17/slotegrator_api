from http import HTTPMethod

from slotegrator_api.types import FreespinLimit

from .base import SlotegratorMethod


class GetFreespinLimits(SlotegratorMethod[list[FreespinLimit]]):
    """Get freespin limits method."""

    __return_type__ = list[FreespinLimit]
    __method_path__ = "/limits/freespin"
    __http_method__ = HTTPMethod.GET
