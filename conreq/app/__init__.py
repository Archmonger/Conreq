from typing import Any

_CONFIG_OBJECT = None


def _load_config():
    """Load configuration functionally to avoid circular imports."""
    # pylint: disable=global-statement,import-outside-toplevel
    global _CONFIG_OBJECT

    if not _CONFIG_OBJECT:
        from conreq.app.configuration import _Config

        _CONFIG_OBJECT = _Config()


def config(attribute: str, value: Any = None):
    _load_config()
    if not value:
        return getattr(_CONFIG_OBJECT, attribute, None)
    return setattr(_CONFIG_OBJECT, attribute)
