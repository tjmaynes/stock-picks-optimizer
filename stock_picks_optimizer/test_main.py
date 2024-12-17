from typer.testing import CliRunner
from stock_picks_optimizer.main import app
from stock_picks_optimizer.constants import __CONFIG_FILE_PATH__
from stock_picks_optimizer.stock_picks.fetcher import StockPicksFetcher

from mock import patch
import re
import os
from pathlib import Path

runner = CliRunner()


def test_when_run_is_called_and_no_config_given_it_should_return_optimized_stock_picks_output():
    safely_remove_file(__CONFIG_FILE_PATH__)

    with patch.object(StockPicksFetcher, "get_last_prices") as mocked_get_last_prices:
        mocked_get_last_prices.return_value = {"VTI": 100.0, "VXUS": 50.5, "BND": 9.09}
        actual = runner.invoke(app, ["run"])
        expected_stdout = """
================================================================================
Stock Picks Optimizer v0.1.0
Config file: {}

+--------+------------+-------+----------+
| Symbol | Percentage | Price | Quantity |
+--------+------------+-------+----------+
|  VTI   |   60.0%    | 100.0 |    12    |
|  VXUS  |   30.0%    |  50.5 |    11    |
|  BND   |   10.0%    |  9.09 |    22    |
+--------+------------+-------+----------+

With a budget of $2000.0, you'll have roughly $44.52 remaining to invest.
================================================================================
""".format(__CONFIG_FILE_PATH__).strip()
        assert expected_stdout in actual.stdout
        assert actual.exit_code == 0


def test_when_run_is_called_and_given_config_arg_does_not_exist_it_should_fail_with_message():
    actual = runner.invoke(app, ["run", "--config", "some-missing-file.yml"])

    assert actual.exit_code == 1

    expected_message_format = re.compile(
        "^Error: unable to find stock picks config file: some-missing-file.yml*"
    )
    assert (
        expected_message_format.match(actual.stdout) is not None
    ), "Result not matching: {}".format(actual.stdout)
    assert "Aborted" in actual.stdout


def safely_remove_file(path: Path):
    if os.path.exists(path):
        os.remove(path)
