import secrets
from http import HTTPMethod

from fastapi import APIRouter, FastAPI, HTTPException, Request


class CallbackHandler:
    """Slotegrator callback handler."""

    def __init__(self, app: FastAPI | APIRouter, path: str) -> None:
        app.add_api_route(
            path,
            self.handler,
            methods=[HTTPMethod.POST],
        )
        self.balance = 57.12
        self.bets: dict[str, float] = {}
        self.wins: dict[str, float] = {}
        self.refunds: set[str] = set()

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
                    >= 0
                ):
                    if (
                        form["transaction_id"] not in self.bets
                        and form["transaction_id"] not in self.refunds
                    ):
                        self.bets[form["transaction_id"]] = float(
                            form["amount"],
                        )
                        self.balance -= float(form["amount"])
                    return {
                        "balance": self.balance,
                        "transaction_id": form["transaction_id"],
                    }
            case "win":
                if (
                    form["player_id"] == "123"
                    and form["session_id"] == "123"
                    and float(
                        form["amount"],
                    )
                    >= 0
                ):
                    if form["transaction_id"] not in self.wins:
                        self.wins[form["transaction_id"]] = float(
                            form["amount"],
                        )
                        self.balance += float(form["amount"])
                    return {
                        "balance": self.balance,
                        "transaction_id": secrets.token_hex(4),
                    }
            case "refund":
                if form["player_id"] == "123" and form["session_id"] == "123":
                    if form["bet_transaction_id"] in self.bets:
                        self.balance += self.bets[form["bet_transaction_id"]]
                        del self.bets[form["bet_transaction_id"]]
                        self.refunds.add(form["bet_transaction_id"])
                    return {
                        "balance": self.balance,
                        "transaction_id": secrets.token_hex(4),
                    }

        raise HTTPException(400, "Bad Request")
