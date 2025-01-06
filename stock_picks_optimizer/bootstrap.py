from stock_picks_optimizer.version import __VERSION__
from stock_picks_optimizer.core.use_cases import (
    FetchAllStockGroupsUseCase,
    FetchLatestStockPricesUseCase,
    OptimizeStockGroupsUseCase,
    PrintLatestOptimizationResultsUseCase,
    AddStockGroupUseCase,
    AddDefaultStockGroupUseCase,
    CheckStockGroupExistsByNameUseCase,
    EnsureAppReadyUseCase,
    EnsureDbReadyUseCase,
)
from stock_picks_optimizer.core.utils.session import CachedLimiterSessionBuilder

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

    di["db_conn"] = lambda _: sqlite3.connect(di["app_data_db_path"])
    di["fetch_all_stock_groups_use_case"] = FetchAllStockGroupsUseCase(di["db_conn"])
    di["cached_limiter_session"] = (
        CachedLimiterSessionBuilder()
        .cache_path(di["app_data_yfinance_cache_path"])
        .user_agent_header(di["app_user_agent"])
        .build()
    )
    di["fetch_latest_stock_prices_use_case"] = FetchLatestStockPricesUseCase(
        session=di["cached_limiter_session"]
    )
    di["optimize_stock_groups_use_case"] = OptimizeStockGroupsUseCase(
        di["fetch_latest_stock_prices_use_case"]
    )
    di["print_latest_optimization_results_use_case"] = (
        PrintLatestOptimizationResultsUseCase(
            fetch_all_stock_groups_use_case=di["fetch_all_stock_groups_use_case"],
            optimize_stock_groups_use_case=di["optimize_stock_groups_use_case"],
            app_version=di["app_version"],
            app_datastore_path=str(di["app_data_db_path"]),
        )
    )
    di["add_stock_group_use_case"] = AddStockGroupUseCase(db_conn=di["db_conn"])
    di["check_stock_group_exists_by_name_use_case"] = (
        CheckStockGroupExistsByNameUseCase(db_conn=di["db_conn"])
    )
    di["add_default_stock_group_use_case"] = AddDefaultStockGroupUseCase(
        add_stock_group_use_case=di["add_stock_group_use_case"],
        check_stock_group_exists_by_name_use_case=di[
            "check_stock_group_exists_by_name_use_case"
        ],
    )
    di["ensure_db_ready_use_case"] = EnsureDbReadyUseCase(
        db_conn=di["db_conn"],
        migrations_dir_path=di["app_data_db_migrations_path"],
        db_path=di["app_data_db_path"],
    )
    di["ensure_app_ready_use_case"] = EnsureAppReadyUseCase(
        ensure_db_ready_use_case=di["ensure_db_ready_use_case"],
        add_default_stock_group_use_case=di["add_default_stock_group_use_case"],
    )
