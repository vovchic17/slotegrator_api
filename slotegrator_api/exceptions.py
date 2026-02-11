from dataclasses import dataclass

from slotegrator_api.methods import SlotegratorMethod


class SlotegratorError(Exception):
    """Base exception for slotegrator api."""


@dataclass
class SlotegratorAPIError(SlotegratorError):
    """Exception for API errors."""

    method: SlotegratorMethod
    name: str
    message: str
    status: int

    def __str__(self) -> str:
        return (
            f"{self.status} {self.method.__http_method__} "
            f"{self.method.__method_path__}: {self.message}"
        )
