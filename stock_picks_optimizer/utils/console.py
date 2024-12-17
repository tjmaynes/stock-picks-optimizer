from stock_picks_optimizer.stock_picks.models import StockPicksOptimizerResult

from prettytable import PrettyTable
from stock_picks_optimizer.constants import __VERSION__


def pretty_print(result: StockPicksOptimizerResult, config_file_path: str) -> None:
    table = PrettyTable()
    table.field_names = ["Symbol", "Percentage", "Price", "Quantity"]
    for row in result.results:
        table.add_row(
            [
                row.symbol,
                "{}%".format(row.percentage * 100),
                row.last_price,
                row.quantity,
            ]
        )

    output = """
================================================================================
Stock Picks Optimizer {}
Config file: {}

{}

With a budget of ${}, you'll have roughly ${} remaining to invest.
================================================================================
    """.format(
        __VERSION__,
        config_file_path,
        table,
        result.original_budget,
        result.leftover,
    ).strip()

    print(output)
