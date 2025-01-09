from dataclasses import dataclass, field
from typing import List


@dataclass
class StockPick:
    symbol: str
    percentage: float
    last_price: float = 0.0


@dataclass
class StockGroup:
    name: str
    budget: float
    picks: List[StockPick] = field(default_factory=list)
    is_active: bool = True


@dataclass
class StockPickResult(StockPick):
    quantity: int = 0

    def __init__(self, pick: StockPick, quantity: int):
        self.symbol = pick.symbol
        self.percentage = pick.percentage
        self.last_price = pick.last_price
        self.quantity = quantity


@dataclass
class StockPicksOptimizerResult:
    name: str
    picks: List[StockPickResult]
    original_budget: float
    leftover: float
