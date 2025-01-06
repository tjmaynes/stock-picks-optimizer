import typer
import uvicorn
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
    uvicorn.run(
        "stock_picks_optimizer.web.main:app", host="0.0.0.0", port=port, reload=reload
    )


if __name__ == "__main__":
    app()
