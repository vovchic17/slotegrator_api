from typing import Literal

from .base import SlotegratorObject
from .game_tag import GameTag


class GameParameters(SlotegratorObject):
    """Game parameters object."""

    rtp: int | None
    volatility: (
        Literal["low", "low-medium", "medium", "medium-high", "high"] | None
    )
    reels_count: int | None
    lines_count: int | None


class GameImage(SlotegratorObject):
    """Game image object."""

    name: str
    file: str
    url: str
    type: str


class Game(SlotegratorObject):
    """Game object."""

    uuid: str
    name: str
    image: str
    type: str
    provider: str
    provider_id: int
    technology: str
    has_lobby: bool
    is_mobile: bool
    has_freespins: bool
    has_tables: bool
    freespin_valid_until_full_day: bool
    label: str
    tags: list[GameTag] | None = None
    parameters: GameParameters | None = None
    images: list[GameImage] | None = None
    related_games: list[object] | None = (
        None  # list[Game] ??? staging returned {'uuid': '', 'is_mobile': 1}
    )
