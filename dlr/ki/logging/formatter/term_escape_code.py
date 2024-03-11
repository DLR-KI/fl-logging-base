from logging import Formatter  # type: ignore [attr-defined]

from .utils import non_ansi


class TermEscapeCodeFormatter(Formatter):
    """
    A class to strip the escape codes from the message.
    """

    def formatMessage(self, record):
        """
        Format message and strip the escape codes.

        Args:
            record: message record to be formatted

        Returns:
            str: formatted message
        """
        msg = super().formatMessage(record)
        return non_ansi(msg)
