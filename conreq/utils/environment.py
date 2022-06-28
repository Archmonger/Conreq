import json
import os
from typing import Any, Callable, Tuple

import dotenv
from dotenv import dotenv_values

_HOME_URL = None
_BASE_URL = None
_SAFE_MODE = None
_DEBUG_MODE = None
_DB_ENGINE = None
ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "CONREQ").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX += "_"


def dotenv_path() -> str:
    """Load the .env path from a different context to avoid circular imports."""
    # pylint: disable=import-outside-toplevel
    from conreq.settings import DOTENV_FILE

    return DOTENV_FILE


def _parse_env_value(value: Any, default_value: Any, return_type: Callable) -> Any:
    """Returns a value based on the return type."""
    if not value:
        return default_value
    if return_type is bool and isinstance(value, str):
        try:
            return _str_to_bool(value)
        except ValueError:
            return default_value
    if return_type in {list, dict} and isinstance(value, str):
        return json.loads(value)
    if not isinstance(value, return_type):
        return return_type(value)
    return value


def get_env(
    name: str,
    default_value: Any = None,
    sys_env=True,
    dot_env=True,
    return_type: Callable = str,
) -> Any:
    """Returns an environment variable from either system variables or Conreq's dotenv file."""
    if not name or not isinstance(name, str):
        raise ValueError("Did not provide a valid environment variable name!")

    value = os.environ.get(ENV_PREFIX + name.upper()) if sys_env else None
    if dot_env and not value:
        value = dotenv_values(dotenv_path()).get(name.upper())

    return _parse_env_value(value, default_value, return_type)


def get_debug_mode() -> bool:
    """Shortcut to obtain DEBUG from environment variables"""
    # pylint: disable=global-statement
    global _DEBUG_MODE

    if _DEBUG_MODE is None:
        _DEBUG_MODE = get_env("DEBUG_MODE", False, return_type=bool)

    return _DEBUG_MODE


def get_safe_mode() -> bool:
    """Shortcut to obtain SAFE_MODE from environment variables"""
    # pylint: disable=global-statement
    global _SAFE_MODE

    if _SAFE_MODE is None:
        _SAFE_MODE = get_env("SAFE_MODE", False, return_type=bool)

    return _SAFE_MODE


def get_base_url(
    prepend_slash: bool = True, append_slash: bool = True, empty_if_unset: bool = False
) -> str:
    """Obtains the BASE_URL from the environment variables"""
    # pylint: disable=global-statement
    global _BASE_URL

    if _BASE_URL is None:
        _BASE_URL = get_env("BASE_URL", "")

    base_url = _BASE_URL
    if base_url:
        base_url = base_url.replace("/", "").replace("\\", "")

    if empty_if_unset and not base_url:
        return base_url

    if append_slash:
        base_url = f"{base_url}/"
    if prepend_slash:
        base_url = f"/{base_url}"
    base_url = base_url.replace("//", "/")
    return base_url


def get_home_url(
    prepend_slash: bool = True, append_slash: bool = True, empty_if_unset: bool = False
) -> str:
    """Obtains the HOME_URL from the environment variables"""
    # pylint: disable=global-statement
    global _HOME_URL

    if _HOME_URL is None:
        _HOME_URL = get_env("HOME_URL", "home")

    home_url = _HOME_URL
    if home_url:
        home_url = home_url.replace("/", "").replace("\\", "")

    if empty_if_unset and not home_url:
        return home_url

    if append_slash:
        home_url = f"{home_url}/"
    if prepend_slash:
        home_url = f"/{home_url}"
    home_url = home_url.replace("//", "/")
    return home_url


def get_database_engine() -> str:
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    # pylint: disable=global-statement
    global _DB_ENGINE

    if _DB_ENGINE is None:
        _DB_ENGINE = get_env("DB_ENGINE", "").upper()

    if _DB_ENGINE in {"MYSQL"}:
        return _DB_ENGINE

    return "SQLITE3"


def set_env(name: str, value: Any, sys_env=False, dot_env=True) -> Tuple[str, str]:
    """Sets a value in either the system environment, and/or the .env file."""
    if value is None:
        value = ""
    if sys_env:
        os.environ[ENV_PREFIX + name.upper()] = value
    if dot_env:
        dotenv.set_key(dotenv_path(), name.upper(), str(value))
    return (name, value)


def delete_env(name: str, sys_env=False, dot_env=True) -> None:
    """Removes a value in either the system environment, and/or the .env file."""
    if sys_env and os.environ.get(ENV_PREFIX + name.upper()) is not None:
        del os.environ[ENV_PREFIX + name.upper()]
    if dot_env:
        dotenv.unset_key(dotenv_path(), name.upper())


def _str_to_bool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {val}")
