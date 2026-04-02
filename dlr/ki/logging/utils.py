# SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0

from importlib.metadata import metadata, Distribution
from os import get_terminal_size
from textwrap import wrap


def welcome(
    name: str,
    description: str | None = None,
    max_width: int = 80,
    *,
    leading_empty_line: bool = True,
    tailing_empty_line: bool = True,
    print_to_stdout: bool = True,
    package_name: str | None = None,
) -> str:
    """
    Generates welcome message.

    Generates and prints (by default) a welcome message which includes the DLR logo
    and highlights the application name.

    If no description is specified, the package metadata is retrieved from the given package name.
    If the package name is also not provided the given application name will be used.
    The "summary" from the retrieved metadata will then be used as description.

    Args:
        name (str): Application name.
        description (str, optional): Short description of the application.
            If not provided the summary entry from the package metadata will be used.
            Defaults to None.
        max_width (int, optional): Maximal number of characters in one line. Defaults to 80.
        leading_empty_line (bool, optional): Add leading empty line. Defaults to True.
        tailing_empty_line (bool, optional): Add tailing empty line. Defaults to True.
        print_to_stdout (bool, optional): Print welcome message to stdout. Defaults to True.
        package_name (str, optional): Package name to retrieve metadata from if no description
            is provided. If not given, the name will be used. Defaults to None.

    Returns:
        str: Welcome message.
    """
    if description is None:
        description = ""  # fallback
        package_name = package_name or name
        if any(Distribution.discover(name=package_name)):
            description = metadata(package_name).get("summary", "")

    logo = [" __/|__", "/_/_/_/", "  |/ DLR"]
    text_width = min(max_width, get_terminal_size().columns) - 13
    desc = ["\033[1;36m" + name + "\033[0m", *wrap(description or "", text_width)]

    if len(desc) < 3:
        desc.insert(0, "")
    if len(desc) > 3:
        logo.insert(0, "")
    (desc if len(desc) < len(logo) else logo).extend([""] * abs(len(desc) - len(logo)))

    welcome_msg = []
    for logo_part, text_part in zip(logo, desc, strict=True):
        welcome_msg.append(f"{logo_part:<12} {text_part}")
    if leading_empty_line:
        welcome_msg.insert(0, "")
    if tailing_empty_line:
        welcome_msg.append("")

    msg = "\n".join(welcome_msg)
    if print_to_stdout:
        print(msg)
    return msg
