from stock_picks_optimizer.web.main import run as run_web_app

import typer
from kink import di

app = typer.Typer()

di["ensure_app_ready_use_case"].invoke()


@app.command()
def latest() -> None:
    try:
        di["print_latest_optimization_results_use_case"].invoke()
    except Exception as e:
        print("Error: {}".format(e))
        raise typer.Abort()


@app.command()
def web(port: int = 8000, reload: bool = False) -> None:
    try:
        run_web_app(port, reload)
    except Exception as e:
        print("Error: {}".format(e))
        raise typer.Abort()


if __name__ == "__main__":
    app()
