from typing import Any

CONFIG: object = None


def _load_config() -> None:
    """Load configuration functionally to avoid circular imports."""
    # pylint: disable=global-statement,import-outside-toplevel
    global CONFIG

    if not CONFIG:
        from conreq.app.configuration import _Config

        CONFIG = _Config()


def config(attribute: str, value: Any = None) -> Any:
    _load_config()
    if not value:
        return getattr(CONFIG, attribute, None)
    return setattr(CONFIG, attribute)
