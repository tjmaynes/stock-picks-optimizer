from typing import List

from stock_picks_optimizer.domain.models import (
    StockPicksOptimizerResult,
    StockGroup,
    StockPickResult,
)

import math

from stock_picks_optimizer.use_cases.fetch_latest_stock_prices import (
    FetchLatestStockPricesUseCase,
)


class OptimizeStockGroupsUseCase:
    def __init__(
        self, fetch_latest_stock_prices_use_case: FetchLatestStockPricesUseCase
    ):
        self.__fetch_latest_stock_prices_use_case = fetch_latest_stock_prices_use_case

    def invoke(self, stock_groups: List[StockGroup]) -> List[StockPicksOptimizerResult]:
        result = []
        for stock_group in stock_groups:
            result.append(self._optimize_group(stock_group))
        return result

    def _optimize_group(self, stock_group: StockGroup) -> StockPicksOptimizerResult:
        total_percentage = sum(list(map(lambda x: x.percentage, stock_group.picks)))
        if not math.isclose(total_percentage, 1.0):
            raise Exception("total given pick percentage does not add up to 1")

        symbols = list(map(lambda data: data.symbol, stock_group.picks))

        last_price_results = self.__fetch_latest_stock_prices_use_case.invoke(symbols)

        for pick in stock_group.picks:
            pick.last_price = last_price_results[pick.symbol]

        results = []
        budget_remainder = stock_group.budget
        sorted_picks = sorted(
            stock_group.picks, key=lambda x: x.percentage, reverse=True
        )

        for pick in sorted_picks:
            allocation = stock_group.budget * pick.percentage
            quantity = math.floor(math.trunc(allocation / pick.last_price))
            total_cost = pick.last_price * quantity
            budget_remainder -= total_cost
            results.append(StockPickResult(pick=pick, quantity=quantity))

        return StockPicksOptimizerResult(
            name=stock_group.name,
            picks=results,
            original_budget=round(stock_group.budget, 2),
            leftover=round(budget_remainder, 2),
        )
