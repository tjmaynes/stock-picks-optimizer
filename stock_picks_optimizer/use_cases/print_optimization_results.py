from typing import List

from stock_picks_optimizer.domain.models import StockPicksOptimizerResult

from prettytable import PrettyTable


class PrintOptimizationResultsUseCase:
    def __init__(self, app_version: str, app_datastore_path: str):
        self.app_version = app_version
        self.app_datastore_path = app_datastore_path

    def invoke(self, results: List[StockPicksOptimizerResult]) -> None:
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

        return """
================================================================================
Stock Picks Optimizer {}
Datastore: {}

{}
================================================================================
        """.format(
            self.app_version,
            self.app_datastore_path,
            "".join(formatted_results),
        ).strip()
