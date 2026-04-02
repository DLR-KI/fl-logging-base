# SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0

"""DLR Logging Base Module"""

from .config import get_default_logging_dict
from .loader import load, load_default


__all__ = ["get_default_logging_dict", "load", "load_default"]
