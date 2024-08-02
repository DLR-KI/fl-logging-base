# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from ansi.colour.base import Graphic as AnsiGraphic
import ansi.color as ansi
from ansi.cursor import erase_line
from copy import copy
from logging import Formatter  # type: ignore [attr-defined]
from typing import Dict


class ColoredConsoleFormatter(Formatter):
    """
    Formatter to support ANSI color codes and print colorful logs to the console.
    """

    MAPPING: Dict[str, AnsiGraphic] = {
        "DEBUG":    ansi.fx.bold + ansi.fg.grey,
        "INFO":     ansi.fx.bold + ansi.fg.green,
        "WARNING":  ansi.fx.bold + ansi.fg.yellow,
        "ERROR":    ansi.fx.bold + ansi.fg.red,
        "CRITICAL": ansi.fx.bold + ansi.fg.black + ansi.bg.red,
    }
    """
    ANSI Code mapping for each log level.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # create a dict with all ansi functions to provide them while formating
        self.ansi_dict = {}
        for key, value in ansi.fx.__dict__.items():
            if isinstance(value, AnsiGraphic):
                self.ansi_dict[f"ansi.fx.{key}"] = value
        for key, value in ansi.fg.__dict__.items():
            if isinstance(value, AnsiGraphic):
                self.ansi_dict[f"ansi.fg.{key}"] = value
        for key, value in ansi.bg.__dict__.items():
            if isinstance(value, AnsiGraphic):
                self.ansi_dict[f"ansi.bg.{key}"] = value
        self.ansi_dict.pop("ansi.fg.bold")
        self.ansi_dict.pop("ansi.bg.bold")

    def format(self, record):
        colored_record = copy(record)
        colored_record.levelcolor = ColoredConsoleFormatter.MAPPING.get(
            colored_record.levelname,
            ColoredConsoleFormatter.MAPPING["DEBUG"]
        )
        colored_record.colorreset = ansi.fx.reset
        colored_record.clearline = erase_line(2) + "\r"
        colored_record.__dict__.update(self.ansi_dict)
        return super().format(colored_record)
