import logging
import re


class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information in URLs."""

    @staticmethod
    def _filter(s):
        # Removes query parameters from the URL
        return re.sub(r"( /)(\S+)([?])(\S+?[=]\S+)", r"\1\2", s)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)
