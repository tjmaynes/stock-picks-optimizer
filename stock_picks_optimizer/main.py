from stock_picks_optimizer.constants import (
    __VERSION__,
    __APP_DATA_YFINANCE_CACHE_PATH__,
    __APP_DATA_DB_PATH__,
    __APP_USER_AGENT__,
    __APP_DATA_DB_MIGRATIONS_PATH__,
)
from stock_picks_optimizer.domain.models import StockGroup, StockPick
from stock_picks_optimizer.use_cases import (
    FetchAllStockGroupsUseCase,
    FetchLatestStockPricesUseCase,
    OptimizeStockGroupsUseCase,
    PrintOptimizationResultsUseCase,
    AddStockGroupUseCase,
    AddDefaultStockGroupUseCase,
    CheckStockGroupExistsByNameUseCase,
)
from stock_picks_optimizer.utils.session import CachedLimiterSessionBuilder
from stock_picks_optimizer.data.migrate import ensure_db_ready

import sqlite3
import typer
import uvicorn

app = typer.Typer()
db_conn = sqlite3.connect(__APP_DATA_DB_PATH__)
cached_limiter_session = (
    CachedLimiterSessionBuilder()
    .cache_path(str(__APP_DATA_YFINANCE_CACHE_PATH__))
    .user_agent_header(str(__APP_USER_AGENT__))
    .build()
)

fetch_all_stock_groups_use_case = FetchAllStockGroupsUseCase(db_conn)
fetch_latest_stock_prices_use_case = FetchLatestStockPricesUseCase(
    session=cached_limiter_session
)
optimize_stock_groups_use_case = OptimizeStockGroupsUseCase(
    fetch_latest_stock_prices_use_case
)
print_optimization_results_use_case = PrintOptimizationResultsUseCase(
    app_version=__VERSION__, app_datastore_path=str(__APP_DATA_DB_PATH__)
)
add_stock_group_use_case = AddStockGroupUseCase(db_conn=db_conn)
check_stock_group_exists_by_name_use_case = CheckStockGroupExistsByNameUseCase(
    db_conn=db_conn
)
add_default_stock_group_use_case = AddDefaultStockGroupUseCase(
    add_stock_group_use_case=add_stock_group_use_case,
    check_stock_group_exists_by_name_use_case=check_stock_group_exists_by_name_use_case,
)

ensure_db_ready(
    db_conn=db_conn,
    migrations_dir_path=__APP_DATA_DB_MIGRATIONS_PATH__,
    db_path=__APP_DATA_DB_PATH__,
)
add_default_stock_group_use_case.invoke(
    StockGroup(
        name="Default",
        budget=2000.0,
        picks=[
            StockPick(symbol="VTI", percentage=0.6),
            StockPick(symbol="VXUS", percentage=0.3),
            StockPick(symbol="BND", percentage=0.1),
        ],
    )
)


@app.command()
def latest() -> None:
    try:
        stock_groups = fetch_all_stock_groups_use_case.invoke()
        results = optimize_stock_groups_use_case.invoke(stock_groups)
        print_optimization_results_use_case.invoke(results)
    except Exception as e:
        print("Error: {}".format(e))
        raise typer.Abort()


@app.command()
def web() -> None:
    uvicorn.run("stock_picks_optimizer.web.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    app()
