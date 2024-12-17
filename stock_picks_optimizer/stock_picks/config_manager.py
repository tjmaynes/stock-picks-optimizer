from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path

from stock_picks_optimizer.stock_picks.models import StockPick
from stock_picks_optimizer.utils.config_file_manager import ConfigFileManager


@dataclass
class StockPicksConfig:
    budget: float
    picks: List[StockPick]
    config_file_path: str


class StockPicksConfigManager:
    def __init__(self, config_file_manager: ConfigFileManager):
        self._config_file_manager = config_file_manager

    def read(self, config: Optional[Path]) -> StockPicksConfig:
        raw_config_data, config_file_path = self._config_file_manager.read(config)

        if not raw_config_data["budget"]:
            raise Exception("bad config file: key 'budget' not found")

        if not raw_config_data["picks"]:
            raise Exception("bad config file: key 'picks' not found")

        return StockPicksConfig(
            config_file_path=config_file_path,
            budget=raw_config_data["budget"],
            picks=list(
                map(
                    lambda raw_data: StockPick(
                        symbol=raw_data["symbol"], percentage=raw_data["percentage"]
                    ),
                    raw_config_data["picks"],
                )
            ),
        )
