from typing import Optional, Any
from pathlib import Path
from stock_picks_optimizer.constants import (
    __APP_DIRECTORY__,
    __CONFIG_FILE_PATH__,
    __DEFAULT_CONFIG_DATA__,
)

import yaml


class ConfigFileManager:
    def __init__(self) -> None:
        self.app_directory_path = __APP_DIRECTORY__
        self.default_config_path = __CONFIG_FILE_PATH__
        self.default_config_data = __DEFAULT_CONFIG_DATA__

    def ensure_config_file_exists(self) -> Any:
        self.app_directory_path.mkdir(parents=True, exist_ok=True)

        if not self.default_config_path.is_file():
            with open(self.default_config_path, "w") as config_file:
                yaml.dump(
                    self.default_config_data,
                    config_file,
                    default_flow_style=False,
                    sort_keys=False,
                )

        return self.default_config_data

    def read(self, override_default_config: Optional[Path]) -> Any:
        if override_default_config is None:
            return self.ensure_config_file_exists(), self.default_config_path

        try:
            with open(override_default_config, "r") as stream:
                return yaml.safe_load(stream), override_default_config
        except FileNotFoundError:
            raise Exception(
                "unable to find stock picks config file: {}".format(
                    override_default_config
                )
            )
