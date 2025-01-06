from typing import List

from stock_picks_optimizer.core.domain.models import StockPicksOptimizerResult

from prettytable import PrettyTable
from stock_picks_optimizer.core.use_cases import (
    FetchAllStockGroupsUseCase,
    OptimizeStockGroupsUseCase,
)


class PrintLatestOptimizationResultsUseCase:
    def __init__(
        self,
        fetch_all_stock_groups_use_case: FetchAllStockGroupsUseCase,
        optimize_stock_groups_use_case: OptimizeStockGroupsUseCase,
        app_version: str,
        app_datastore_path: str,
    ):
        self.__fetch_all_stock_groups_use_case = fetch_all_stock_groups_use_case
        self.__optimize_stock_groups_use_case = optimize_stock_groups_use_case
        self.app_version = app_version
        self.app_datastore_path = app_datastore_path

    def invoke(self) -> None:
        stock_groups = self.__fetch_all_stock_groups_use_case.invoke()
        results = self.__optimize_stock_groups_use_case.invoke(stock_groups)
        print(self._prettify_results(results))

    def _prettify_results(self, results: List[StockPicksOptimizerResult]) -> str:
        formatted_results = []
        for result in results:
            table = PrettyTable()
            table.field_names = ["Symbol", "Percentage", "Price", "Quantity"]
            for row in result.picks:
                table.add_row(
                    [
                        row.symbol,
                        "{}%".format(row.percentage * 100),
                        row.last_price,
                        row.quantity,
                    ]
                )
            formatted_result = """
Stock group: {}
{}
With a budget of ${}, you'll have roughly ${} remaining to invest.
""".format(result.name, table, result.original_budget, result.leftover).strip()
            formatted_results.append(formatted_result)

        comments = (
            """
Comments:
- To add more stock groups, use the web interface via "stock-picks-optimizer web".
        """.strip()
            if len(results) == 1 and results[0].name == "Default"
            else ""
        )

        return """
===================================================================================
Stock Picks Optimizer {}
Datastore: {}

{}

{}
===================================================================================
        """.format(
            self.app_version,
            self.app_datastore_path,
            "".join(formatted_results),
            comments,
        ).strip()
