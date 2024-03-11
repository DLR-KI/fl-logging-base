from pathlib import Path
from typing import Any, Dict, Optional


def get_default_logging_dict(log_filepath: Optional[str] = None, ensure_log_dir: bool = True) -> Dict[str, Any]:
    """
    Get default logging configuration dict.

    Args:
        log_filepath (str, optional): Log file path. Defaults to None.
        ensure_log_dir (bool, optional): Create directory for the log file if not exists. Defaults to True.

    Returns:
        Dict[str, Any]: logging configuration dict
    """
    if log_filepath and ensure_log_dir:
        Path(log_filepath).parent.mkdir(parents=True, exist_ok=True)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console_formatter": {
                "class": "dlr.ki.logging.formatter.colored_console.ColoredConsoleFormatter",
                "format": "[%(levelcolor)s%(levelname)-8s%(colorreset)s] %(ansi.fg.grey)s[%(name)s][%(filename)s:%(lineno)d]%(ansi.fx.reset)s  %(message)s"  # noqa: E501
            },
            "file_formatter": {
                "class": "dlr.ki.logging.formatter.term_escape_code.TermEscapeCodeFormatter",
                "format": "%(asctime)s [%(levelname)-8s] [%(name)s][%(filename)s:%(lineno)d]  %(message)s"
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "level": "INFO",
                "formatter": "console_formatter"
            },
            **({"file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": log_filepath,
                "when": "midnight",
                "level": "DEBUG",
                "formatter": "file_formatter"
            }} if log_filepath else {})
        },
        "loggers": {
            "": {
                "handlers": ["console_handler", "file_handler"] if log_filepath else ["console_handler"],
                "level": "DEBUG",
                "propagate": True
            },
            "celery": {
                "level": "WARNING"
            },
            "matplotlib": {
                "level": "WARNING"
            },
            "numba": {
                "level": "WARNING"
            },
            "PIL": {
                "level": "WARNING"
            }
        }
    }
