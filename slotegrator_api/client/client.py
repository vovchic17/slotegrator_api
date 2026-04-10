from collections.abc import AsyncIterator
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, FastAPI

from slotegrator_api.callback import CallbackHandler
from slotegrator_api.methods import (
    BalanceNotify,
    CancelFreevoucherCampaign,
    CancelSetCampaign,
    GetFreespinBets,
    GetFreespinCampaign,
    GetFreespinLimits,
    GetFreevoucherCampaign,
    GetGames,
    GetGameTags,
    GetJackpots,
    GetLimits,
    GetLobbyTables,
    InitDemoGame,
    InitGame,
    SelfValidate,
    SetFreespinCampaign,
    SetFreevoucherCampaign,
)
from slotegrator_api.types import (
    BalanceNotification,
    CampaignCancel,
    FreespinBets,
    FreespinCampaign,
    FreespinLimit,
    FreespinSet,
    FreevoucherCampaign,
    FreevoucherSet,
    Game,
    GameTag,
    Jackpot,
    Limit,
    PreparedGame,
    SelfValidation,
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
        self.callback_handler: CallbackHandler | None = None

    async def close(self) -> None:
        await self._session.close()

    def setup_callback(
        self,
        app: FastAPI | APIRouter,
        path: str = "/",
    ) -> None:
        self.callback_handler = CallbackHandler(app, path, self.merchant_key)

    async def get_games(
        self,
        expand: list[Literal["tags", "parameters", "images", "related_games"]]
        | None = None,
        page: int | None = None,
    ) -> list[Game]:
        res = await self._session(GetGames(expand=expand, page=page))
        return res.items

    async def iter_games(
        self,
        expand: list[Literal["tags", "parameters", "images", "related_games"]]
        | None = None,
        start_page: int = 1,
    ) -> AsyncIterator[Game]:
        page = start_page

        while True:
            game_items = await self._session(
                GetGames(expand=expand, page=page),
            )
            pg = game_items.meta
            for game in game_items.items:
                yield game
            if pg.current_page == pg.page_count:
                break
            page += 1

    async def get_game_tags(
        self,
        expand: list[Literal["category"]] | None = None,
        page: int | None = None,
    ) -> list[GameTag]:
        res = await self._session(GetGameTags(expand=expand, page=page))
        return res.items

    async def iter_game_tags(
        self,
        expand: list[Literal["category"]] | None = None,
        start_page: int = 1,
    ) -> AsyncIterator[GameTag]:
        page = start_page

        while True:
            tag_items = await self._session(
                GetGameTags(expand=expand, page=page),
            )
            pg = tag_items.meta
            for tag in tag_items.items:
                yield tag
            if pg.current_page == pg.page_count:
                break
            page += 1

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

    async def get_freespin_bets(
        self,
        game_uuid: str,
        currency: str,
    ) -> FreespinBets:
        return await self._session(
            GetFreespinBets(
                game_uuid=game_uuid,
                currency=currency,
            ),
        )

    async def set_freespin_campaign(
        self,
        player_id: str,
        player_name: str,
        currency: str,
        quantity: int,
        valid_from: int,
        valid_until: int,
        freespin_id: str,
        game_uuid: str,
        bet_id: int | None = None,
        total_bet_id: int | None = None,
        denomination: float | None = None,
    ) -> FreespinSet:
        return await self._session(
            SetFreespinCampaign(
                player_id=player_id,
                player_name=player_name,
                currency=currency,
                quantity=quantity,
                valid_from=valid_from,
                valid_until=valid_until,
                freespin_id=freespin_id,
                game_uuid=game_uuid,
                bet_id=bet_id,
                total_bet_id=total_bet_id,
                denomination=denomination,
            ),
        )

    async def get_freespin_campaign(
        self,
        freespin_id: str,
    ) -> FreespinCampaign:
        return await self._session(
            GetFreespinCampaign(freespin_id=freespin_id),
        )

    async def cancel_set_campaign(self, freespin_id: str) -> CampaignCancel:
        return await self._session(
            CancelSetCampaign(freespin_id=freespin_id),
        )

    async def set_freevoucher_campaign(
        self,
        player_id: str,
        title: str,
        currency: str,
        initial_balance: float,
        max_winnings: float,
        valid_until: datetime,
        voucher_id: str,
        table_ids: list[str],
        short_terms: str | None = None,
        terms_and_conds: str | None = None,
    ) -> FreevoucherSet:
        return await self._session(
            SetFreevoucherCampaign(
                player_id=player_id,
                title=title,
                currency=currency,
                initial_balance=initial_balance,
                max_winnings=max_winnings,
                valid_until=valid_until,
                voucher_id=voucher_id,
                table_ids=table_ids,
                short_terms=short_terms,
                terms_and_conds=terms_and_conds,
            ),
        )

    async def get_freevoucher_campaign(
        self,
        voucher_id: str,
    ) -> FreevoucherCampaign:
        return await self._session(
            GetFreevoucherCampaign(voucher_id=voucher_id),
        )

    async def cancel_freevoucher_campaign(
        self,
        voucher_id: str,
        reason: str,
    ) -> CampaignCancel:
        return await self._session(
            CancelFreevoucherCampaign(voucher_id=voucher_id, reason=reason),
        )

    async def self_validate(self) -> SelfValidation:
        return await self._session(SelfValidate())
