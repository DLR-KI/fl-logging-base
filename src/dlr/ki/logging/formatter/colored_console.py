# SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0

from copy import copy
from logging import Formatter
from typing import ClassVar

import ansi.color as ansi
from ansi.colour.base import Graphic as AnsiGraphic
from ansi.cursor import erase_line


class ColoredConsoleFormatter(Formatter):
    """ANSI color-code formatter for colorful console logs."""

    MAPPING: ClassVar[dict[str, AnsiGraphic]] = {
        "DEBUG": ansi.fg.grey,
        "INFO": ansi.fg.default,
        "WARNING": ansi.fg.yellow,
        "ERROR": ansi.fg.red,
        "CRITICAL": ansi.fg.black + ansi.bg.red,
    }
    """
    ANSI Code mapping for each log level.
    """

    def __init__(  # ruff: ignore[undocumented-public-init]
        self, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        # create a dict with all ansi codes to provide them while formatting
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

    def format(self, record):  # ruff: ignore[undocumented-public-method]
        colored_record = copy(record)
        colored_record.levelcolor = ColoredConsoleFormatter.MAPPING.get(
            colored_record.levelname, ColoredConsoleFormatter.MAPPING["DEBUG"]
        )
        colored_record.colorreset = ansi.fx.reset
        colored_record.clearline = erase_line(2) + "\r"
        colored_record.__dict__.update(self.ansi_dict)
        return super().format(colored_record)
