import hashlib
import hmac
from http import HTTPMethod
from typing import TYPE_CHECKING, cast
from urllib.parse import urlencode

from fastapi import APIRouter, FastAPI, HTTPException, Request

from slotegrator_api.callback.methods import (
    Balance,
    Bet,
    Refund,
    Rollback,
    Win,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Literal, TypedDict

    type BalanceHandler = Callable[[Balance], dict]
    type BetHandler = Callable[[Bet], dict]
    type WinHandler = Callable[[Win], dict]
    type RefundHandler = Callable[[Refund], dict]
    type RollbackHandler = Callable[[Rollback], dict]
    type HandlerUnion = (
        BalanceHandler
        | BetHandler
        | WinHandler
        | RefundHandler
        | RollbackHandler
    )

    type Actions = Literal["balance", "bet", "win", "refund", "rollback"]

    class HandlersDict(TypedDict, total=False):
        """Handler dictionary."""

        balance: BalanceHandler
        bet: BetHandler
        win: WinHandler
        refund: RefundHandler
        rollback: RollbackHandler


class CallbackHandler:
    """Slotegrator callback handler."""

    def __init__(
        self,
        app: FastAPI | APIRouter,
        path: str,
        merchant_key: str,
    ) -> None:
        app.add_api_route(
            path,
            self.handler,
            methods=[HTTPMethod.POST],
        )
        self.merchant_key = merchant_key
        self.handlers: HandlersDict = {}

    def register_handler(
        self,
        action: "Actions",
        func: "HandlerUnion",
    ) -> None:
        self.handlers[action] = func

    def x_sign_validate(
        self,
        request: Request,
        params: dict[str, str],
    ) -> bool:
        headers = {
            "X-Merchant-Id": request.headers.get("X-Merchant-Id", ""),
            "X-Timestamp": request.headers.get("X-Timestamp", ""),
            "X-Nonce": request.headers.get("X-Nonce", ""),
        }
        merged_params = headers | (params or {})
        sorted_params = dict(sorted(merged_params.items()))
        hash_string = urlencode(sorted_params)
        x_sign = hmac.new(
            self.merchant_key.encode(),
            hash_string.encode(),
            hashlib.sha1,
        ).hexdigest()
        return request.headers.get("X-Sign") == x_sign

    async def handler(
        self,
        request: Request,
    ) -> dict:
        form = await request.form()
        params = cast("dict[str, str]", dict(form))
        if not self.x_sign_validate(request, params):
            return {
                "error_code": "INTERNAL_ERROR",
                "error_description": "Incorrect X-Sign",
            }
        print(form) # debug
        match form["action"]:
            case "balance":
                resp = Balance.model_validate(form)
            case "bet":
                resp = Bet.model_validate(form)
            case "win":
                resp = Win.model_validate(form)
            case "refund":
                resp = Refund.model_validate(form)
            case "rollback":
                resp = Rollback.model_validate(form)
        raise HTTPException(400, "Bad Request")
