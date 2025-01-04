from stock_picks_optimizer.constants import (
    __VERSION__,
    __APP_DATA_YFINANCE_CACHE_PATH__,
    __APP_DATA_DB_PATH__,
    __APP_USER_AGENT__,
    __APP_DATA_DB_MIGRATIONS_PATH__,
)
from stock_picks_optimizer.use_cases import (
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
from stock_picks_optimizer.utils.session import CachedLimiterSessionBuilder

import sqlite3
from kink import di


def bootstrap_di() -> None:
    di["app_data_yfinance_cache_path"] = str(__APP_DATA_YFINANCE_CACHE_PATH__)
    di["app_user_agent"] = str(__APP_USER_AGENT__)
    di["app_data_db_migrations_path"] = __APP_DATA_DB_MIGRATIONS_PATH__
    di["app_data_db_path"] = __APP_DATA_DB_PATH__
    di["app_version"] = __VERSION__

    di["db_conn"] = lambda dii: sqlite3.connect(__APP_DATA_DB_PATH__)
    di["fetch_all_stock_groups_use_case"] = lambda dii: FetchAllStockGroupsUseCase(
        dii["db_conn"]
    )
    di["cached_limiter_session"] = lambda dii: (
        CachedLimiterSessionBuilder()
        .cache_path(dii["app_data_yfinance_cache_path"])
        .user_agent_header(dii["app_user_agent"])
        .build()
    )
    di["fetch_latest_stock_prices_use_case"] = (
        lambda dii: FetchLatestStockPricesUseCase(session=dii["cached_limiter_session"])
    )
    di["optimize_stock_groups_use_case"] = lambda dii: OptimizeStockGroupsUseCase(
        dii["fetch_latest_stock_prices_use_case"]
    )
    di["print_latest_optimization_results_use_case"] = lambda dii: (
        PrintLatestOptimizationResultsUseCase(
            fetch_all_stock_groups_use_case=di["fetch_all_stock_groups_use_case"],
            optimize_stock_groups_use_case=di["optimize_stock_groups_use_case"],
            app_version=dii["app_version"],
            app_datastore_path=str(dii["app_data_db_path"]),
        )
    )
    di["add_stock_group_use_case"] = lambda dii: AddStockGroupUseCase(
        db_conn=dii["db_conn"]
    )
    di["check_stock_group_exists_by_name_use_case"] = (
        lambda dii: CheckStockGroupExistsByNameUseCase(db_conn=dii["db_conn"])
    )
    di["add_default_stock_group_use_case"] = lambda dii: AddDefaultStockGroupUseCase(
        add_stock_group_use_case=dii["add_stock_group_use_case"],
        check_stock_group_exists_by_name_use_case=dii[
            "check_stock_group_exists_by_name_use_case"
        ],
    )
    di["ensure_db_ready_use_case"] = lambda dii: EnsureDbReadyUseCase(
        db_conn=dii["db_conn"],
        migrations_dir_path=dii["app_data_db_migrations_path"],
        db_path=dii["app_data_db_path"],
    )
    di["ensure_app_ready_use_case"] = lambda dii: EnsureAppReadyUseCase(
        ensure_db_ready_use_case=dii["ensure_db_ready_use_case"],
        add_default_stock_group_use_case=dii["add_default_stock_group_use_case"],
    )
