from logging.config import dictConfig, fileConfig  # type: ignore [attr-defined]
from typing import Any, Dict, Optional, Union
import yaml
import yaml.parser

from .config import get_default_logging_dict


def load_default(log_filepath: Optional[str] = None, ensure_log_dir: bool = True) -> None:
    """
    Load default logging configuration.

    Args:
        log_filepath (str, optional): Log file path. Defaults to None.
        ensure_log_dir (bool, optional): Create directory for the log file if not exists. Defaults to True.
    """
    load_dict(get_default_logging_dict(log_filepath, ensure_log_dir))


def load(config: Union[str, Dict[str, Any]], **kwargs) -> None:
    """
    Load logging configuration from file or dict.

    Args:
        config (Union[str, Dict[str, Any]]): configuration file path or dict

    Raises:
        ValueError: if configuration file could not be loaded
    """
    if isinstance(config, str):
        try:
            load_yaml(config)
        except yaml.parser.ParserError:
            try:
                load_conf(config, **kwargs)
            except Exception:
                raise ValueError(f"Cannot load config from '{config}'")
    else:
        load_dict(config)


def load_dict(config: Dict[str, Any]) -> None:
    """
    Load logging configuration from dict.

    Args:
        config (Dict[str, Any]): configuration dict
    """
    dictConfig(config)


def load_yaml(filepath: str) -> None:
    """
    Load logging configuration from yaml file.

    Args:
        filepath (str): yaml file path
    """
    with open(filepath, "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    config["disable_existing_loggers"] = config.get("disable_existing_loggers", False)
    dictConfig(config)


def load_conf(filepath: str, **kwargs) -> None:
    """
    Load logging configuration from conf file.

    Args:
        filepath (str): conf file path
    """
    kwargs["disable_existing_loggers"] = kwargs.get("disable_existing_loggers", False)
    fileConfig(filepath, **kwargs)
