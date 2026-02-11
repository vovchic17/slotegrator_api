from typing import Literal

from pydantic import Field

from .base import SlotegratorObject


class Table(SlotegratorObject):
    """Table object."""

    lobby_data: str = Field(alias="lobbyData")
    name: str
    is_open: bool = Field(alias="isOpen")
    open_time: str = Field(alias="openTime")
    close_time: str = Field(alias="closeTime")
    dealer_name: str = Field(alias="dealerName")
    dealer_avatar: str = Field(alias="dealerAvatar")
    technology: (
        Literal["html5", "flash"] | int
    )  # server returned `1` instead of string WTF
    limits: list[object]
    table_id: str = Field(alias="tableId")


class Lobby(SlotegratorObject):
    """Lobby object."""

    lobby: list[Table]
