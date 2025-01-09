from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

from stock_picks_optimizer.core.domain.models import StockPick


@dataclass
class AddStockGroup(BaseModel):
    name: str
    budget: float
    picks: List[StockPick]
