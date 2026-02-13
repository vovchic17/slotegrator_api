from typing import Literal

from slotegrator_api.methods import (
    BalanceNotify,
    GetFreespinLimits,
    GetGames,
    GetGameTags,
    GetJackpots,
    GetLimits,
    GetLobbyTables,
    InitDemoGame,
    InitGame,
)
from slotegrator_api.types import (
    BalanceNotification,
    FreespinLimit,
    Game,
    GameTag,
    Jackpot,
    Limit,
    PreparedGame,
    Table,
)

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
    ) -> list[GameTag]:
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

    async def init_game(
        self,
        game_uuid: str,
        player_id: str,
        player_name: str,
        currency: str,
        session_id: str,
        device: Literal["desktop", "mobile"] | None = "desktop",
        return_url: str | None = None,
        language: str | None = None,
        email: str | None = None,
        lobby_data: str | None = None,
    ) -> PreparedGame:
        return await self._session(
            InitGame(
                game_uuid=game_uuid,
                player_id=player_id,
                player_name=player_name,
                currency=currency,
                session_id=session_id,
                device=device,
                return_url=return_url,
                language=language,
                email=email,
                lobby_data=lobby_data,
            ),
        )

    async def init_demo_game(
        self,
        game_uuid: str,
        device: Literal["desktop", "mobile"] | None = "desktop",
        return_url: str | None = None,
        language: str | None = None,
    ) -> PreparedGame:
        return await self._session(
            InitDemoGame(
                game_uuid=game_uuid,
                device=device,
                return_url=return_url,
                language=language,
            ),
        )

    async def get_limits(self) -> list[Limit]:
        return await self._session(GetLimits())

    async def get_freespin_limits(self) -> list[FreespinLimit]:
        return await self._session(GetFreespinLimits())

    async def get_jackpots(self) -> list[Jackpot]:
        return await self._session(GetJackpots())

    async def balance_notify(
        self,
        balance: float,
        session_id: str,
    ) -> BalanceNotification:
        return await self._session(
            BalanceNotify(
                balance=balance,
                session_id=session_id,
            ),
        )

    async def get_freespin_bets(self): ...  # noqa: ANN201
    async def set_freespin_campaign(self): ...  # noqa: ANN201
    async def get_freespin_campaign(self): ...  # noqa: ANN201
    async def cancel_set_camping(self): ...  # noqa: ANN201
    async def set_freevoucher_campaign(self): ...  # noqa: ANN201
    async def get_freevoucher_campaign(self): ...  # noqa: ANN201
    async def cancel_freevoucher_campaign(self): ...  # noqa: ANN201
    async def self_validate(self): ...  # noqa: ANN201
