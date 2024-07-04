---
title: Home
hide: navigation
---
<!--
SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>

SPDX-License-Identifier: CC-BY-4.0
-->

<!-- markdownlint-disable-next-line MD025 -->
# Logging Base Module

This is a small Python package designed to simplify the process of enabling consistent logging across multiple projects.
Instead of copying code from one project to another, this package provides a simple, reusable solution.

This project is a component of the Federated Learning (FL) platform, serving as a proof of concept for the [Catena-X](https://catena-x.net/en) project.
The FL platform aims to demonstrate the potential of federated learning in a practical, real-world context.

For a comprehensive understanding of the FL platform, please refer to the official [FL platform documentation](https://dlr-ki.github.io/fl-documentation).

A complete list of all repositories relevant to the FL platform can be found [here](https://dlr-ki.github.io/fl-documentation#repositories).

## Install

/// tab | pip
    new: true

```bash
pip install -U "git+https://github.com/DLR-KI/fl-logging-base.git@main"
```

///

/// tab | pyproject.toml
    new: false

```toml
dependencies = [
  "dlr-logging @ git+https://github.com/DLR-KI/fl-logging-base.git@main",
]
```

///

/// tab | setup.py
    new: false

```python
install_requires = [
    "dlr-logging @ git+https://github.com/DLR-KI/fl-logging-base.git@main",
]
```

///

/// tab | poetry
    new: false

```toml
[tool.poetry.dependencies]
dlr-logging = { git = "git+https://github.com/DLR-KI/fl-logging-base.git", branch = "main" }
```

///

## Usage

### Default configuration

```python
import logging
from dlr.ki.logging import load_default

load_default("logs/app.log")
logging.info("Hello World!")
```

### Advanced: Manipulate default configuration

```python
import logging
import logging.config
from dlr.ki.logging import get_default_logging_dict

# get default logging configuration
log_config = get_default_logging_dict("logs/app.log")

# manipulate logging configuration
# e.g. add an additional handler like loki
#      and set the log level from urllib3 to warning
log_config["handlers"]["loki"] = {
    "level": "DEBUG",
    "class": "logging_loki.LokiHandler",
    "url": "http://localhost:3100/loki/api/v1/push",
    "tags": {
        "app": "fl.server"
    },
    "auth": ["admin", "admin"],
    "version": "1",
}
log_config["loggers"][""]["handlers"].append("loki")
log_config["loggers"]["urllib3"] = {"level": "WARNING"}

# load config
logging.config.dictConfig(log_config)
logging.info("Hello World!")
```
