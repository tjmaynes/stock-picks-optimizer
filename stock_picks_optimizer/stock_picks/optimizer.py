from typing import List

from stock_picks_optimizer.stock_picks.fetcher import StockPicksFetcher
from stock_picks_optimizer.stock_picks.models import (
    StockPick,
    StockPickResult,
    StockPicksOptimizerResult,
)

import math


class StockPicksOptimizer:
    def __init__(self, stock_info_fetcher: StockPicksFetcher) -> None:
        self._stock_info_fetcher = stock_info_fetcher

    def optimize(
        self, budget: float, picks: List[StockPick]
    ) -> StockPicksOptimizerResult:
        total_percentage = sum(list(map(lambda x: x.percentage, picks)))
        if not math.isclose(total_percentage, 1.0):
            raise Exception("total given pick percentage does not add up to 1")

        symbols = list(map(lambda data: data.symbol, picks))
        last_price_results = self._stock_info_fetcher.get_last_prices(symbols)
        for pick in picks:
            pick.last_price = last_price_results[pick.symbol]

        return self._process_picks(budget, picks)

    def _process_picks(
        self, budget: float, picks: List[StockPick]
    ) -> StockPicksOptimizerResult:
        results = []
        budget_remainder = budget
        sorted_picks = sorted(picks, key=lambda x: x.percentage, reverse=True)

        for pick in sorted_picks:
            allocation = budget * pick.percentage
            quantity = math.floor(math.trunc(allocation / pick.last_price))
            total_cost = pick.last_price * quantity
            budget_remainder -= total_cost
            results.append(StockPickResult(pick=pick, quantity=quantity))

        return StockPicksOptimizerResult(
            results=results,
            original_budget=round(budget, 2),
            leftover=round(budget_remainder, 2),
        )
