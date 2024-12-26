import typer
from pathlib import Path


__APP_NAME__ = "com.tjmaynes.stock-picks-optimizer"
__APP_DIRECTORY__ = Path(typer.get_app_dir(__APP_NAME__))
__CONFIG_FILE_NAME__ = "config.yml"
__CONFIG_FILE_PATH__ = __APP_DIRECTORY__ / __CONFIG_FILE_NAME__
__VERSION__ = "v0.1.0"

__DEFAULT_CONFIG_DATA__ = {
    "budget": 2000.0,
    "picks": [
        {
            "symbol": "VTI",
            "percentage": 0.6,
        },
        {
            "symbol": "VXUS",
            "percentage": 0.3,
        },
        {
            "symbol": "BND",
            "percentage": 0.1,
        },
    ],
}
