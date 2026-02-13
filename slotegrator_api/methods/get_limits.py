from http import HTTPMethod

from slotegrator_api.types import Limit

from .base import SlotegratorMethod


class GetLimits(SlotegratorMethod[list[Limit]]):
    """Get limits method."""

    __return_type__ = list[Limit]
    __method_path__ = "/limits"
    __http_method__ = HTTPMethod.GET
