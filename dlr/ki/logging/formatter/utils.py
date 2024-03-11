import re


def non_ansi(text: str) -> str:
    """
    Remove ansi escape characters from text.

    References:

    - <https://stackoverflow.com/a/14693789>

    Args:
        text (str): Text to convert.

    Returns:
        str: text without ansi escape characters
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)
