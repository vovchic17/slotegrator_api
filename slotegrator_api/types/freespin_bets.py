from .base import SlotegratorObject


class Bet(SlotegratorObject):
    """Bet object."""

    bet_id: str
    bet_per_line: str | float
    lines: int


class TotalBet(SlotegratorObject):
    """Total bet object."""

    bet_id: int
    amount: float


class FreespinBets(SlotegratorObject):
    """Freespin bets object."""

    denominations: list[str]
    bets: list[Bet]
    total_bets: list[TotalBet]
