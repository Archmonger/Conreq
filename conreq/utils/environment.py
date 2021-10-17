import functools
import json
import os
from distutils.util import strtobool
from typing import Any, Callable, Optional

import dotenv
from dotenv import dotenv_values

ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


@functools.cache
def dotenv_path() -> str:
    """Load the .env path from a different context to avoid circular imports."""
    # pylint: disable=import-outside-toplevel
    from conreq.settings import DOTENV_FILE

    return DOTENV_FILE


def get_env(
    name: str,
    default_value: Any = None,
    sys_env=True,
    dot_env=True,
    return_type: Callable = str,
) -> Any:
    """Returns an environment variable from either system variables or Conreq's dotenv file."""
    value = os.environ.get(ENV_PREFIX + name.upper()) if sys_env else None
    if dot_env and not value:
        value = dotenv_values(dotenv_path()).get(name.upper())

    if not value:
        return default_value
    if return_type is bool and isinstance(value, str):
        return strtobool(value)
    if return_type in {list, dict} and isinstance(value, str):
        return json.loads(value)
    if not isinstance(value, return_type):
        return return_type(value)
    return value


@functools.cache
def get_debug() -> bool:
    """Shortcut to obtain DEBUG from environment variables"""
    return get_env("DEBUG", True, return_type=bool)


@functools.cache
def get_safe_mode() -> bool:
    """Shortcut to obtain SAFE_MODE from environment variables"""
    return get_env("SAFE_MODE", False, return_type=bool)


@functools.cache
def get_base_url(append_slash: bool = True, prepend_slash: bool = True) -> str:
    """Obtains the base URL from the environment variables"""
    base_url = get_env("BASE_URL", "")
    if base_url:
        base_url = base_url.replace("/", "").replace("\\", "")
    if append_slash:
        base_url = base_url + "/"
    if prepend_slash:
        base_url = "/" + base_url
    base_url = base_url.replace("//", "/")
    return base_url


@functools.cache
def get_home_url(append_slash: bool = True, prepend_slash: bool = True) -> str:
    """Obtains the base URL from the environment variables"""
    home_url = get_env("HOME_URL", "home")
    if home_url:
        home_url = home_url.replace("/", "").replace("\\", "")
    if append_slash:
        home_url = home_url + "/"
    if prepend_slash:
        home_url = "/" + home_url
    home_url = home_url.replace("//", "/")
    return home_url


@functools.cache
def get_database_type() -> str:
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    db_engine = get_env("DB_ENGINE", "")
    if db_engine.upper() == "MYSQL":
        return "MYSQL"
    return "SQLITE3"


def set_env(name: str, value: str, sys_env=False, dot_env=True) -> Optional[str]:
    """Sets a value in either the system environment, and/or the .env file."""
    if sys_env:
        os.environ[ENV_PREFIX + name.upper()] = value
    if dot_env:
        dotenv.set_key(dotenv_path(), name.upper(), value)
    return (name, value)


def remove_env(name: str, sys_env=False, dot_env=True) -> None:
    """Removes a value in either the system environment, and/or the .env file."""
    if sys_env and os.environ.get(ENV_PREFIX + name.upper()) is not None:
        del os.environ[ENV_PREFIX + name.upper()]
    if dot_env:
        dotenv.unset_key(dotenv_path(), name.upper())
