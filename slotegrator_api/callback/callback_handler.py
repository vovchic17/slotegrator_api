import hashlib
import hmac
import re
from http import HTTPMethod
from typing import TYPE_CHECKING, TypedDict, cast
from urllib.parse import urlencode

from fastapi import APIRouter, FastAPI, Request
from fastapi.datastructures import FormData

from slotegrator_api.callback.methods import (
    Balance,
    Bet,
    Refund,
    Rollback,
    Win,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Literal


class TransactionResponse(TypedDict):
    """Transaction response model."""

    balance: float
    transaction_id: str


class RollbackResponse(TransactionResponse):
    """Rollback response model."""

    rollback_transactions: list[str]


type Method = Balance | Bet | Win | Refund | Rollback
type BalanceHandler = Callable[[Balance], Awaitable[float]]
type BetHandler = Callable[[Bet], Awaitable[TransactionResponse]]
type WinHandler = Callable[[Win], Awaitable[TransactionResponse]]
type RefundHandler = Callable[[Refund], Awaitable[TransactionResponse]]
type RollbackHandler = Callable[[Rollback], Awaitable[RollbackResponse]]
type HandlerUnion = (
    BalanceHandler | BetHandler | WinHandler | RefundHandler | RollbackHandler
)

type Action = Literal["balance", "bet", "win", "refund", "rollback"]


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
        action: "Action",
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

    @staticmethod
    def validate_rollback(form: FormData) -> Rollback:
        rollback_re = re.compile(
            r"^rollback_transactions\[(\d+)\]\[(action|amount|transaction_id|type)\]$",
        )
        data: dict = dict(form)

        rollback_transactions: dict[int, dict] = {}

        for key, value in form.multi_items():
            match = rollback_re.match(key)
            if not match:
                continue

            index = int(match.group(1))
            field = match.group(2)

            rollback_transactions.setdefault(index, {})
            rollback_transactions[index][field] = value

        data["rollback_transactions"] = [
            rollback_transactions[i] for i in sorted(rollback_transactions)
        ]

        return Rollback.model_validate(data)

    async def handler(  # noqa: C901, PLR0911
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
        resp: Method
        match form["action"]:
            case "balance":
                resp = Balance.model_validate(form)
                if "balance" not in self.handlers:
                    msg = "Balance handler is not defined."
                    raise RuntimeError(msg)
                balance = await self.handlers["balance"](resp)
                return {"balance": round(balance, 4)}
            case "bet":
                resp = Bet.model_validate(form)
                if "bet" not in self.handlers:
                    msg = "Bet handler is not defined."
                    raise RuntimeError(msg)
                res = await self.handlers["bet"](resp)
                balance = round(res["balance"], 4)
                transaction_id = res["transaction_id"]
                return {
                    "balance": balance,
                    "transaction_id": transaction_id,
                }
            case "win":
                resp = Win.model_validate(form)
                if "win" not in self.handlers:
                    msg = "Win handler is not defined."
                    raise RuntimeError(msg)
                res = await self.handlers["win"](resp)
                balance = round(res["balance"], 4)
                transaction_id = res["transaction_id"]
                return {
                    "balance": balance,
                    "transaction_id": transaction_id,
                }
            case "refund":
                resp = Refund.model_validate(form)
                if "refund" not in self.handlers:
                    msg = "Refund handler is not defined."
                    raise RuntimeError(msg)
                res = await self.handlers["refund"](resp)
                balance = round(res["balance"], 4)
                transaction_id = res["transaction_id"]
                return {
                    "balance": balance,
                    "transaction_id": transaction_id,
                }
            case "rollback":
                resp = self.validate_rollback(form)
                if "rollback" not in self.handlers:
                    msg = "Rollback handler is not defined."
                    raise RuntimeError(msg)
                res = await self.handlers["rollback"](resp)
                balance = round(res["balance"], 4)
                transaction_id = res["transaction_id"]
                rollback_transactions = res["rollback_transactions"]
                return {
                    "balance": balance,
                    "transaction_id": transaction_id,
                    "rollback_transactions": rollback_transactions,
                }
        action = cast("Action", form["action"])
        if action in self.handlers:
            await self.handlers[action](resp)  # type: ignore[arg-type]
        return {"success": True}
