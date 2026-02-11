from typing import Literal

from slotegrator_api.methods import GetGames, GetGameTags, GetLobbyTables
from slotegrator_api.types import Game, GameTag, Table

from .session import HTTPSession


class SlotegratorAPI:
    """Slotegrator API client."""

    def __init__(
        self,
        merchant_id: str,
        merchant_key: str,
        base_api_url: str,
        timeout: float = 300.0,
    ) -> None:
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.base_api_url = base_api_url
        self._session = HTTPSession(
            merchant_id=merchant_id,
            merchant_key=merchant_key,
            base_api_url=base_api_url,
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._session.close()

    async def get_games(
        self,
        expand: list[Literal["tags", "parameters", "images", "related_games"]]
        | None = None,
    ) -> list[Game]:
        res = await self._session(GetGames(expand=expand))
        return res.items

    async def get_game_tags(
        self,
        expand: list[Literal["category"]] | None = None,
    ) -> GameTag:
        res = await self._session(GetGameTags(expand=expand))
        return res.items

    async def get_lobby_tables(
        self,
        game_uuid: str,
        currency: str,
        technology: Literal["html5", "flash"] | None = None,
    ) -> list[Table]:
        res = await self._session(
            GetLobbyTables(
                game_uuid=game_uuid,
                currency=currency,
                technology=technology,
            ),
        )
        return res.lobby

    async def init_game(self): ...
    async def init_demo_game(self): ...
    async def get_limits(self): ...
    async def get_freespin_limits(self): ...
    async def get_jackpots(self): ...
    async def get_freespin_bets(self): ...
    async def set_freespin_campaign(self): ...
    async def get_freespin_campaign(self): ...
    async def cancel_set_camping(self): ...
    async def set_freevoucher_campaign(self): ...
    async def get_freevoucher_campaign(self): ...
    async def cancel_freevoucher_campaign(self): ...
    async def self_validate(self): ...
