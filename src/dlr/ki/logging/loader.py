# SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0

from logging.config import dictConfig, fileConfig
from pathlib import Path
from typing import Any

import yaml
import yaml.parser

from dlr.ki.logging.config import get_default_logging_dict


def load_default(
    log_filepath: str | Path | None = None, ensure_log_dir: bool = True
) -> None:
    """
    Load default logging configuration.

    Args:
        log_filepath (str | Path, optional): Log file path. Defaults to None.
        ensure_log_dir (bool, optional):
            Create directory for the log file if not exists. Defaults to True.
    """
    load_dict(get_default_logging_dict(log_filepath, ensure_log_dir))


def load(config: str | Path | dict[str, Any], **kwargs) -> None:
    """
    Load logging configuration from file or dict.

    Args:
        config (str | Path | dict[str, Any]): configuration file path or dict
        kwargs: further logging.config.fileConfig arguments

    Raises:
        ValueError: if configuration file could not be loaded
    """
    if isinstance(config, (str, Path)):
        try:
            load_yaml(str(config))
        except yaml.parser.ParserError:
            try:
                load_conf(str(config), **kwargs)
            except Exception as e:
                raise ValueError(f"Cannot load config from '{config}'") from e
    else:
        load_dict(config)


def load_dict(config: dict[str, Any]) -> None:
    """
    Load logging configuration from dict.

    Args:
        config (dict[str, Any]): configuration dict
    """
    dictConfig(config)


def load_yaml(filepath: str | Path) -> None:
    """
    Load logging configuration from yaml file.

    Args:
        filepath (str | Path): yaml file path
    """
    with open(filepath) as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    config["disable_existing_loggers"] = config.get("disable_existing_loggers", False)
    dictConfig(config)


def load_conf(filepath: str | Path, **kwargs) -> None:
    """
    Load logging configuration from conf file.

    Args:
        filepath (str | Path): conf file path
        kwargs: further logging.config.fileConfig arguments
    """
    kwargs["disable_existing_loggers"] = kwargs.get("disable_existing_loggers", False)
    fileConfig(filepath, **kwargs)
