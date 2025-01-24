from pathlib import Path

from typer.testing import CliRunner

from stock_picks_optimizer.helpers.process import StockPicksOptimizerModuleRunner
from stock_picks_optimizer.main import app
from stock_picks_optimizer.version import __VERSION__
from stock_picks_optimizer.core.use_cases.fetch_latest_stock_prices import (
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
        datastore_path = Path(__file__).parent / "data/stock-picks-optimizer.db"
        expected_stdout = """
===================================================================================
Stock Picks Optimizer {}
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

Comments:
- To add more stock groups, use the web interface via "stock-picks-optimizer web".
===================================================================================
""".format(__VERSION__, datastore_path).lstrip()
        assert actual.stdout in expected_stdout
        assert actual.exit_code == 0


# TODO: need to understand why subprocess stdout is not working...
def test_web_should_start_web_app():
    module_runner = StockPicksOptimizerModuleRunner(["web", "--port", "8888"])

    # actual_message = module_runner.read_stdout()
    # assert "Uvicorn running on http://0.0.0.0:9090" in actual_message

    exit_code = module_runner.stop()
    assert exit_code == 0

    actual_message = module_runner.read_stderr()
    assert "Uvicorn running on http://0.0.0.0:8888" in actual_message
