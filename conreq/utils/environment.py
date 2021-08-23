import functools
import os
from typing import Optional

import dotenv

from conreq.utils.generic import str_to_bool, str_to_int

ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


@functools.cache
def _dotenv_path() -> str:
    """Fetches the .env file path set during Conreq startup."""
    return os.environ["CONREQ_DOTENV_FILE"]


@functools.cache
def _get_str_from_dotenv(name: str, default_value: str = "") -> str:
    """Fetches a value from the .env file."""
    value = dotenv.main.DotEnv(_dotenv_path()).get(str(name).upper())
    if not value:
        value = default_value
    else:
        value = str(value)
    return value


@functools.cache
def get_str_from_env(
    name: str, default_value: str = "", sys_env=True, dot_env=True
) -> str:
    """Obtains a string from an environment variable"""
    value = ""
    if sys_env:
        value = os.environ.get(ENV_PREFIX + str(name).upper(), "")
    if dot_env and not value:
        value = _get_str_from_dotenv(str(name).upper())
    if not value:
        return default_value
    return value


@functools.cache
def get_bool_from_env(
    name: str, default_value: bool = False, sys_env=True, dot_env=True
) -> bool:
    """Obtains a boolean from an environment variable"""
    value = get_str_from_env(name, str(default_value), sys_env, dot_env)
    return str_to_bool(value, default_value)


@functools.cache
def get_int_from_env(
    name: str, default_value: int = 0, sys_env=True, dot_env=True
) -> str:
    """Obtains a integer from an environment variable"""
    value = get_str_from_env(name, str(default_value), sys_env=sys_env, dot_env=dot_env)
    return str_to_int(value, default_value)


@functools.cache
def get_debug() -> bool:
    """Shortcut to obtain DEBUG from environment variables"""
    return get_bool_from_env("DEBUG", True)


@functools.cache
def get_base_url() -> str:
    """Obtains the base URL from the environment variables"""
    base_url = get_str_from_env("BASE_URL")
    if isinstance(base_url, str) and base_url:
        base_url = base_url.replace("/", "").replace("\\", "")
        base_url = "/" + base_url
    return base_url


@functools.cache
def get_database_type() -> str:
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    db_engine = get_str_from_env("DB_ENGINE")
    if db_engine.upper() == "MYSQL":
        return "MYSQL"
    return "SQLITE3"


def set_env(name: str, value: str, sys_env=False, dot_env=True) -> Optional[str]:
    """Sets a value in either the system environment, and/or the .env file."""
    if sys_env:
        os.environ[ENV_PREFIX + str(name).upper()] = str(value)
    if dot_env:
        dotenv.set_key(_dotenv_path(), str(name).upper(), str(value))
    return (name, value)


def remove_env(name: str, sys_env=False, dot_env=True) -> None:
    """Removes a value in either the system environment, and/or the .env file."""
    if sys_env and os.environ.get(ENV_PREFIX + str(name).upper()) is not None:
        del os.environ[ENV_PREFIX + str(name).upper()]
    if dot_env:
        dotenv.unset_key(_dotenv_path(), str(name).upper())
