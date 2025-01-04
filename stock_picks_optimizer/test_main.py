from typer.testing import CliRunner
from stock_picks_optimizer.main import app
from stock_picks_optimizer.constants import __APP_DATA_DB_PATH__
from stock_picks_optimizer.use_cases.fetch_latest_stock_prices import (
    FetchLatestStockPricesUseCase,
)

from mock import patch

runner = CliRunner()


def test_latest_it_should_return_optimized_stock_picks_output():
    with patch.object(
        FetchLatestStockPricesUseCase, "invoke"
    ) as mock_fetch_latest_stock_prices_use_case:
        mock_fetch_latest_stock_prices_use_case.return_value = {
            "VTI": 100.0,
            "VXUS": 50.5,
            "BND": 9.09,
        }
        actual = runner.invoke(app, ["latest"])
        expected_stdout = """
================================================================================
Stock Picks Optimizer v0.1.0
Datastore: {}

Stock group: Default
+--------+------------+-------+----------+
| Symbol | Percentage | Price | Quantity |
+--------+------------+-------+----------+
|  VTI   |   60.0%    | 100.0 |    12    |
|  VXUS  |   30.0%    |  50.5 |    11    |
|  BND   |   10.0%    |  9.09 |    22    |
+--------+------------+-------+----------+
With a budget of $2000.0, you'll have roughly $44.52 remaining to invest.
================================================================================
""".format(__APP_DATA_DB_PATH__).lstrip()
        assert actual.stdout in expected_stdout
        assert actual.exit_code == 0

# def test_web_should_start_web_app():
#     actual = runner.invoke(app, args=["web"], input=b"\cc")
#     assert actual.exit_code == 0
