from http import HTTPMethod

from slotegrator_api.types import BalanceNotification

from .base import SlotegratorMethod


class BalanceNotify(SlotegratorMethod[BalanceNotification]):
    """Balance notify method."""

    __return_type__ = BalanceNotification
    __method_path__ = "/balance/notify"
    __http_method__ = HTTPMethod.POST

    balance: float
    session_id: str
