import os

from conreq.utils.generic import str_to_bool

ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


def get_base_url():
    """Obtains the base URL from the environment variables"""
    base_url = os.environ.get("BASE_URL", "")
    if isinstance(base_url, str) and base_url:
        base_url = base_url.replace("/", "").replace("\\", "")
        base_url = "/" + base_url
    return base_url


def get_bool_from_env(name, default_value=False):
    """Obtains a boolean from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    return str_to_bool(env_var, default_value)


def get_str_from_env(name, default_value=""):
    """Obtains a string from an environment variable"""
    return os.environ.get(ENV_PREFIX + name, default_value)


def get_int_from_env(name, default_value=0):
    """Obtains a integer from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    if env_var.isdigit():
        return int(env_var)
    return default_value


def get_env_prefix():
    """Returns the environment variables prefix that should be used."""
    return ENV_PREFIX


def get_debug_from_env():
    """Shortcut to obtain DEBUG from env variables"""
    return get_bool_from_env("DEBUG", True)


def get_database_type():
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    db_engine = os.environ.get("DB_ENGINE", "")
    if db_engine.upper() == "MYSQL":
        return "MYSQL"
    return "SQLITE3"
