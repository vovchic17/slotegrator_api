from typing import Literal

from .base import SlotegratorObject
from .game_tag import GameTag


class GameParameters(SlotegratorObject):
    """Game parameters object."""

    rtp: float | None
    volatility: (
        Literal["low", "low-medium", "medium", "medium-high", "high", "very-high"] | None
    )
    reels_count: str | None
    lines_count: str | None


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
    image: str | None
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
