from stock_picks_optimizer.version import __VERSION__
from stock_picks_optimizer.core.use_cases import (
    FetchAllStockGroupsUseCase,
    FetchLatestStockPricesUseCase,
    OptimizeStockGroupsUseCase,
    PrintLatestOptimizationResultsUseCase,
    AddStockGroupUseCase,
    AddDefaultStockGroupUseCase,
    FetchStockGroupByNameUseCase,
    EnsureAppReadyUseCase,
    EnsureDbReadyUseCase,
)
from stock_picks_optimizer.core.utils.session import (
    CachedLimiterSessionBuilder,
    CachedLimiterSession,
)

import sqlite3
from pathlib import Path
from kink import di


def bootstrap_di() -> None:
    di["app_name"] = "stock-picks-optimizer"
    di["app_version"] = __VERSION__
    di["app_user_agent"] = "{}/{}".format(di["app_name"], di["app_version"])
    di["app_data_db_path"] = Path(__file__).parent / "data/{}.db".format(di["app_name"])
    di["app_data_db_migrations_path"] = Path(__file__).parent / "data/migrations"
    di["app_data_yfinance_cache_path"] = (
        Path(__file__).parent / "data/yfinance-cache.sqlite"
    )
    di["app_web_templates_path"] = Path(__file__).parent / "web/templates"
    di["app_web_static_path"] = Path(__file__).parent / "web/static"

    di["db_conn"] = lambda _: sqlite3.connect(di["app_data_db_path"])

    di[FetchAllStockGroupsUseCase] = FetchAllStockGroupsUseCase(di["db_conn"])
    di[CachedLimiterSession] = (
        CachedLimiterSessionBuilder()
        .cache_path(di["app_data_yfinance_cache_path"])
        .user_agent_header(di["app_user_agent"])
        .build()
    )
    di[FetchLatestStockPricesUseCase] = FetchLatestStockPricesUseCase(
        session=di[CachedLimiterSession]
    )
    di[OptimizeStockGroupsUseCase] = OptimizeStockGroupsUseCase(
        di[FetchLatestStockPricesUseCase]
    )
    di[PrintLatestOptimizationResultsUseCase] = PrintLatestOptimizationResultsUseCase(
        fetch_all_stock_groups_use_case=di[FetchAllStockGroupsUseCase],
        optimize_stock_groups_use_case=di[OptimizeStockGroupsUseCase],
        app_version=di["app_version"],
        app_datastore_path=str(di["app_data_db_path"]),
    )
    di[FetchStockGroupByNameUseCase] = FetchStockGroupByNameUseCase(
        db_conn=di["db_conn"]
    )
    di[AddStockGroupUseCase] = AddStockGroupUseCase(
        db_conn=di["db_conn"],
        fetch_stock_group_by_name_use_case=di[FetchStockGroupByNameUseCase],
    )
    di[AddDefaultStockGroupUseCase] = AddDefaultStockGroupUseCase(
        add_stock_group_use_case=di[AddStockGroupUseCase],
        fetch_stock_group_by_name_use_case=di[FetchStockGroupByNameUseCase],
    )
    di[EnsureDbReadyUseCase] = EnsureDbReadyUseCase(
        db_conn=di["db_conn"],
        migrations_dir_path=di["app_data_db_migrations_path"],
        db_path=di["app_data_db_path"],
    )
    di[EnsureAppReadyUseCase] = EnsureAppReadyUseCase(
        ensure_db_ready_use_case=di[EnsureDbReadyUseCase],
        add_default_stock_group_use_case=di[AddDefaultStockGroupUseCase],
    )
