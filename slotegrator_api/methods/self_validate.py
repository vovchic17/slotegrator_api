from http import HTTPMethod

from slotegrator_api.types import SelfValidation

from .base import SlotegratorMethod


class SelfValidate(SlotegratorMethod[SelfValidation]):
    """Self validate method."""

    __return_type__ = SelfValidation
    __method_path__ = "/self-validate"
    __http_method__ = HTTPMethod.POST
