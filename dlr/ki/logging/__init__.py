# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

"""DLR Logging Base Module"""

from .config import get_default_logging_dict
from .loader import load, load_default


__all__ = ["get_default_logging_dict", "load", "load_default"]
