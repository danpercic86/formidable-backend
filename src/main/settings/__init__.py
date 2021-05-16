import os
from typing import AnyStr, Optional, Union, Tuple, Callable, List

import yaml


class Config:
    def __init__(self, config_file: AnyStr):
        if not os.path.exists(config_file):
            msg = (
                'Could not find "config.yml" file. '
                "Make sure to read the instructions from README.md"
            )
            raise FileNotFoundError(msg)

        with open(config_file) as file:
            self.__config = yaml.safe_load(file)
            if not self.__config:
                raise ValueError("Config file is empty!")

    def get(
        self,
        var_name: str,
        default: Optional[Union[str, int, Tuple]] = None,
        cast: Callable = str,
        raise_error: bool = False,
    ) -> Union[str, int, bool, List[str], None]:
        if value := self.__config.get(var_name, default):
            value = cast(value)
            if isinstance(value, str):
                value = value.strip()
            return value
        if raise_error:
            raise LookupError(fr"Cannot find value for setting {var_name}!")
        return None
