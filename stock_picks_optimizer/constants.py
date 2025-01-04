from pathlib import Path

__APP_NAME__ = "stock-picks-optimizer"
__VERSION__ = "v0.1.0"
__APP_DATA_DB_PATH__ = Path(__file__).parent / "data/{}.db".format(__APP_NAME__)
__APP_DATA_DB_MIGRATIONS_PATH__ = Path(__file__).parent / "data/migrations"
__APP_DATA_YFINANCE_CACHE_PATH__ = Path(__file__).parent / "data/yfinance-cache.sqlite"
__APP_USER_AGENT__ = "{}/{}".format(__APP_NAME__, __VERSION__)
