from stock_picks_optimizer.core.use_cases import (
    EnsureAppReadyUseCase,
    PrintLatestOptimizationResultsUseCase,
)
from stock_picks_optimizer.web.main import run as run_web_app

import typer
from kink import di

app = typer.Typer()

di[EnsureAppReadyUseCase].invoke()


@app.command()
def latest() -> None:
    try:
        di[PrintLatestOptimizationResultsUseCase].invoke()
    except Exception as e:
        print("Error: {}".format(e))
        raise typer.Abort()


@app.command()
def web(port: int = 8000, reload: bool = False) -> None:
    run_web_app(port, reload)


if __name__ == "__main__":
    app()
