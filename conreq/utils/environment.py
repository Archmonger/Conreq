import functools
import os

import dotenv
from conreq.utils.generic import str_to_bool

DOTENV_FILE = None
ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


@functools.cache
def get_base_url():
    """Obtains the base URL from the environment variables"""
    base_url = os.environ.get("BASE_URL", "")
    if isinstance(base_url, str) and base_url:
        base_url = base_url.replace("/", "").replace("\\", "")
        base_url = "/" + base_url
    return base_url


@functools.cache
def get_bool_from_env(name: str, default_value: bool = False):
    """Obtains a boolean from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    return str_to_bool(env_var, default_value)


@functools.cache
def get_str_from_env(name: str, default_value: str = ""):
    """Obtains a string from an environment variable"""
    return os.environ.get(ENV_PREFIX + name, default_value)


@functools.cache
def get_int_from_env(name: str, default_value: int = 0):
    """Obtains a integer from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    if env_var.isdigit():
        return int(env_var)
    return default_value


@functools.cache
def get_debug_from_env():
    """Shortcut to obtain DEBUG from env variables"""
    return get_bool_from_env("DEBUG", True)


@functools.cache
def get_database_type():
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    db_engine = os.environ.get("DB_ENGINE", "")
    if db_engine.upper() == "MYSQL":
        return "MYSQL"
    return "SQLITE3"


@functools.cache
def get_str_from_dotenv(name: str):
    """Fetches a value from the .env file."""
    return dotenv.get_key(DOTENV_FILE, name)


@functools.cache
def _dotenv_path():
    """Fetches the .env file path set during Conreq startup."""
    global DOTENV_FILE  # pylint: disable=global-statement
    if not DOTENV_FILE:
        DOTENV_FILE = get_str_from_env("CONREQ_DOTENV_FILE")
    return DOTENV_FILE


def set_env(name: str, value: str = "", sys_env=True, dot_env=True):
    """Sets a value in either the system environment, and/or the .env file."""
    if sys_env:
        os.environ[ENV_PREFIX + name] = value
    if dot_env:
        dotenv.set_key(_dotenv_path(), name, value)


def remove_env(name: str, sys_env=True, dot_env=True):
    """Removes a value in either the system environment, and/or the .env file."""
    if sys_env and os.environ.get(ENV_PREFIX + name) is not None:
        del os.environ[ENV_PREFIX + name]
    if dot_env:
        dotenv.unset_key(_dotenv_path(), name)
