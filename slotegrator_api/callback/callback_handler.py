import secrets
from http import HTTPMethod

from fastapi import APIRouter, FastAPI, HTTPException, Request


class CallbackHandler:
    """Slotegrator callback handler."""

    def __init__(self, app: FastAPI | APIRouter, path: str) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path,
            self.handler,
            methods=[HTTPMethod.POST],
        )
        self.balance = 57.12
        self.transactions = {}
        app.include_router(self.router)

    async def handler(
        self,
        request: Request,
    ) -> dict:
        form = await request.form()
        print(dict(form))
        match form["action"]:
            case "balance":
                if form["player_id"] == "123" and form["session_id"] == "123":
                    return {
                        "balance": self.balance,
                    }
            case "bet":
                if (
                    form["player_id"] == "123"
                    and form["session_id"] == "123"
                    and float(
                        form["amount"],
                    )
                    > 0
                ):
                    self.transactions[form["transaction_id"]] = float(
                        form["amount"],
                    )
                    self.balance -= float(form["amount"])
                    return {
                        "balance": self.balance,
                        "transaction_id": secrets.token_hex(4),
                    }
            case "win":
                if (
                    form["player_id"] == "123"
                    and form["session_id"] == "123"
                    and float(
                        form["amount"],
                    )
                    > 0
                ):
                    self.balance += float(form["amount"])
                    return {
                        "balance": self.balance,
                        "transaction_id": secrets.token_hex(4),
                    }
            case "refund":
                if form["player_id"] == "123" and form["session_id"] == "123":
                    self.balance += self.transactions.get(
                        form["transaction_id"],
                        0,
                    )
                    if form["transaction_id"] in self.transactions:
                        del self.transactions[form["transaction_id"]]
                    return {
                        "balance": self.balance,
                        "transaction_id": secrets.token_hex(4),
                    }

        raise HTTPException(400, "Bad Request")
