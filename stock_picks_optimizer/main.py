from typing import Optional, Annotated
from pathlib import Path

from stock_picks_optimizer.stock_picks.fetcher import StockPicksFetcher
from stock_picks_optimizer.stock_picks.config_manager import StockPicksConfigManager
from stock_picks_optimizer.stock_picks.optimizer import StockPicksOptimizer
from stock_picks_optimizer.utils.config_file_manager import ConfigFileManager
from stock_picks_optimizer.utils.console import pretty_print

import typer

app = typer.Typer()
stock_pick_optimizer = StockPicksOptimizer(stock_info_fetcher=StockPicksFetcher())


@app.command()
def run(config: Annotated[Optional[Path], typer.Option()] = None) -> None:
    stock_pick_config_manager = StockPicksConfigManager(
        config_file_manager=ConfigFileManager()
    )

    try:
        config_data = stock_pick_config_manager.read(config)
        result = stock_pick_optimizer.optimize(config_data.budget, config_data.picks)
        pretty_print(result, config_data.config_file_path)
    except Exception as e:
        print("Error: {}".format(e))
        raise typer.Abort()


@app.command()
def web() -> None:
    print("web")


if __name__ == "__main__":
    app()
