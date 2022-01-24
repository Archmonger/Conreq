import json
import os
from distutils.util import strtobool
from typing import Any, Callable, Tuple

import dotenv
from dotenv import dotenv_values

HOME_URL = None
BASE_URL = None
SAFE_MODE = None
DEBUG_MODE = None
DB_ENGINE = None
ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


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
            return bool(strtobool(value))
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
    global DEBUG_MODE

    if DEBUG_MODE is None:
        DEBUG_MODE = get_env("DEBUG_MODE", True, return_type=bool)

    return DEBUG_MODE


def get_safe_mode() -> bool:
    """Shortcut to obtain SAFE_MODE from environment variables"""
    # pylint: disable=global-statement
    global SAFE_MODE

    if SAFE_MODE is None:
        SAFE_MODE = get_env("SAFE_MODE", False, return_type=bool)

    return SAFE_MODE


def get_base_url(
    prepend_slash: bool = True, append_slash: bool = True, empty_if_unset: bool = False
) -> str:
    """Obtains the BASE_URL from the environment variables"""
    # pylint: disable=global-statement
    global BASE_URL

    if BASE_URL is None:
        BASE_URL = get_env("BASE_URL", "")

    base_url = BASE_URL
    if base_url:
        base_url = base_url.replace("/", "").replace("\\", "")

    if empty_if_unset and not base_url:
        return base_url

    if append_slash:
        base_url = base_url + "/"
    if prepend_slash:
        base_url = "/" + base_url
    base_url = base_url.replace("//", "/")
    return base_url


def get_home_url(
    prepend_slash: bool = True, append_slash: bool = True, empty_if_unset: bool = False
) -> str:
    """Obtains the HOME_URL from the environment variables"""
    # pylint: disable=global-statement
    global HOME_URL

    if HOME_URL is None:
        HOME_URL = get_env("HOME_URL", "home")

    home_url = HOME_URL
    if home_url:
        home_url = home_url.replace("/", "").replace("\\", "")

    if empty_if_unset and not home_url:
        return home_url

    if append_slash:
        home_url = home_url + "/"
    if prepend_slash:
        home_url = "/" + home_url
    home_url = home_url.replace("//", "/")
    return home_url


def get_database_engine() -> str:
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    # pylint: disable=global-statement
    global DB_ENGINE

    if DB_ENGINE is None:
        DB_ENGINE = get_env("DB_ENGINE", "").upper()

    if DB_ENGINE in {"MYSQL"}:
        return DB_ENGINE

    return "SQLITE3"


def set_env(
    name: str, value: str, sys_env=False, dot_env=True, remove=False
) -> Tuple[str, str]:
    """Sets a value in either the system environment, and/or the .env file."""
    if value is None:
        value = ""
    if sys_env:
        os.environ[ENV_PREFIX + name.upper()] = str(value)
    if dot_env and not value and remove:
        dotenv.unset_key(dotenv_path(), name.upper())
    elif dot_env:
        dotenv.set_key(dotenv_path(), name.upper(), str(value))
    return (name, value)


def remove_env(name: str, sys_env=False, dot_env=True) -> None:
    """Removes a value in either the system environment, and/or the .env file."""
    if sys_env and os.environ.get(ENV_PREFIX + name.upper()) is not None:
        del os.environ[ENV_PREFIX + name.upper()]
    if dot_env:
        dotenv.unset_key(dotenv_path(), name.upper())
