from http import HTTPMethod

from fastapi import APIRouter, FastAPI

from slotegrator_api.callback.methods import (
    Balance,
    Bet,
    Refund,
    Rollback,
    Win,
)


class CallbackHandler:
    """Slotegrator callback handler."""

    def __init__(self, app: FastAPI | APIRouter, path: str) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path,
            self.handler,
            methods=[HTTPMethod.POST],
        )
        app.include_router(self.router)

    def handler(self, method: Balance | Bet | Win | Refund | Rollback) -> None:
        print(type(method))  # noqa: T201
