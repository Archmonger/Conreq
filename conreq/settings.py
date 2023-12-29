"""
Django settings for Conreq project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import logging
import secrets
import site
import sys
from logging.config import dictConfig as logging_config
from pathlib import Path
from typing import Any

import django_stubs_ext
from django.core.management.utils import get_random_secret_key
from split_settings.tools import include
from tzlocal import get_localzone_name

from conreq.types import Seconds
from conreq.utils.apps import find_apps
from conreq.utils.environment import (
    get_base_url,
    get_database_engine,
    get_debug_mode,
    get_env,
    get_safe_mode,
    set_env,
)
from conreq.utils.packages import find_packages

# TODO: Add GUI support for changing most of the settings in this file
# Monkey patches for type hints
django_stubs_ext.monkeypatch()


# // DIRECTORY STRUCTURE //
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR: Path = get_env("DATA_DIR", ROOT_DIR / "data", dot_env=False, return_type=Path)
DATABASE_DIR = DATA_DIR / "databases"
APP_SETTINGS_DIR = DATA_DIR / "app-settings"
MEDIA_DIR = DATA_DIR / "files"
MEDIA_SERVE_DIR = MEDIA_DIR / "serve"
METRICS_DIR = MEDIA_DIR / "metrics"
BACKUP_DIR = DATA_DIR / "backup"
TEMP_DIR = DATA_DIR / "temp"
USER_STATICFILES_DIR = DATA_DIR / "static"
LOG_DIR = DATA_DIR / "logs"
PID_DIR = DATA_DIR / "pids"
MAKE_DIRS: list[Path] = [
    DATA_DIR,
    DATABASE_DIR,
    APP_SETTINGS_DIR,
    MEDIA_DIR,
    MEDIA_SERVE_DIR,
    METRICS_DIR,
    BACKUP_DIR,
    TEMP_DIR,
    USER_STATICFILES_DIR,
    LOG_DIR,
    PID_DIR,
]
if not DATA_DIR.parent.exists():
    raise OSError(f"Parent directory of DATA_DIR ({DATA_DIR.parent}) does not exist.")
for directory in MAKE_DIRS:
    if not directory.exists():
        directory.mkdir(parents=True)
APP_TEMPLATE_DIR = ROOT_DIR / "conreq" / "templates"
PACKAGE_TEMPLATE = APP_TEMPLATE_DIR / "package"
PACKAGE_SLIM_TEMPLATE = APP_TEMPLATE_DIR / "package_slim"
APP_TEMPLATE = APP_TEMPLATE_DIR / "app"
APP_SLIM_TEMPLATE = APP_TEMPLATE_DIR / "app_slim"


# // PROJECT CONFIG //
DOTENV_FILE: Path = DATA_DIR / "settings.env"
if not DOTENV_FILE.exists():
    with open(DOTENV_FILE, "w", encoding="utf-8") as fp:
        pass
DEBUG = get_debug_mode()
WEBSERVER_WORKERS = get_env("WEBSERVER_WORKERS", 1, return_type=int)
with (ROOT_DIR / "VERSION").open() as f:
    CONREQ_VERSION = f.read().strip()
APP_STORE_VERSION = get_env("APP_STORE_VERSION", 1, return_type=int)
ROOT_URLCONF = "conreq.urls"
ASGI_APPLICATION = "conreq.asgi.application"


# // LOGGING //
CONREQ_LOG_FILE = LOG_DIR / "conreq.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"
LOG_LEVEL = get_env("LOG_LEVEL", "INFO" if DEBUG else "WARNING")
LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "class": "conreq.utils.logging.SensitiveFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
        },
        "minimal": {
            "class": "conreq.utils.logging.SensitiveFormatter",
            "format": "%(levelname)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "minimal",
        },
        "conreq_logs": {
            "level": LOG_LEVEL,
            "formatter": "default",
            "encoding": "utf-8",
            "filename": CONREQ_LOG_FILE,
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
    },
    "loggers": {
        "django": {},
        "conreq": {},
        "huey": {},
    },
}
for logger_name in LOGGING["loggers"]:
    LOGGING["loggers"][logger_name]["handlers"] = ["console", "conreq_logs"]
    LOGGING["loggers"][logger_name]["level"] = LOG_LEVEL
if "run_huey" in sys.argv:
    LOGGING["loggers"]["conreq"]["level"] = "ERROR"
    LOGGING["loggers"]["django"]["level"] = "ERROR"
    LOGGING["disable_existing_loggers"] = True
logging_config(LOGGING)
_logger = logging.getLogger(__name__)


# // SECURITY //
SESSION_COOKIE_AGE = get_env("SESSION_COOKIE_AGE", Seconds.month * 3, return_type=int)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = get_env(
    "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin"
)
DEFAULT_HOSTS = ["*", "localhost", "127.0.0.1", "[::1]"]
ALLOWED_HOSTS = [
    host.strip() for host in get_env("ALLOWED_HOSTS", "").split(",") if host
]
ALLOWED_FORWARDING_IPS = [
    addr.strip() for addr in get_env("ALLOWED_FOWARDING_IPS", "").split(",") if addr
]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = DEFAULT_HOSTS
if get_env("CSRF_TRUSTED_ORIGINS", ""):
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in get_env("CSRF_TRUSTED_ORIGINS", "").split(",")
        if origin
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        f"http://{origin.strip()}"
        for origin in ALLOWED_HOSTS
        if origin not in DEFAULT_HOSTS
    ] + [
        f"https://{origin.strip()}"
        for origin in ALLOWED_HOSTS
        if origin not in DEFAULT_HOSTS
    ]
SECURE_BROWSER_XSS_FILTER = True


# // HTTP RESTFUL API //
REST_FRAMEWORK: dict[str, Any] = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "conreq._core.api.permissions.HasAPIKey",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
        "conreq._core.api.authentication.CsrfExemptSessionAuthentication",
    )
SPECTACULAR_SETTINGS = {  # Use Swagger UI for API endpoints
    "TITLE": "Conreq API Endpoints",
    "DESCRIPTION": "Outline for all endpoints available within this Conreq instance.",
    "VERSION": CONREQ_VERSION,
    "CONTACT": {
        "name": "Conreq's Developer",
        "email": "archiethemonger@gmail.com",
    },
    "LICENSE": {"name": "GPL-3.0 License"},
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SCHEMA_PATH_PREFIX": "/api",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "SERVERS": [
        {
            "url": "{protocol}://{host}:{port}/api",
            "variables": {
                "host": {"default": "127.0.0.1"},
                "port": {"default": 7575},
                "protocol": {"enum": ["http", "https"], "default": "http"},
            },
        }
    ],
}


# // ENCRYPTION //
FIELD_ENCRYPTION_KEYS = [get_env("DB_ENCRYPTION_KEY")]
SECRET_KEY = get_env("WEB_ENCRYPTION_KEY")
if not FIELD_ENCRYPTION_KEYS[0]:
    FIELD_ENCRYPTION_KEYS = [secrets.token_hex(32)]
    set_env("DB_ENCRYPTION_KEY", FIELD_ENCRYPTION_KEYS[0])
if not SECRET_KEY:
    SECRET_KEY = set_env("WEB_ENCRYPTION_KEY", get_random_secret_key())[1]


# // DJANGO APPS AND MIDDLEWARE //
INSTALLED_APPS = [
    *(
        [
            "daphne",  # Overrides `runserver` command with an ASGI server
            "jazzmin",  # Pretty admin interface
            "django.contrib.admin",
            "django.contrib.admindocs",
            "massadmin",  # Mass edit actions for admin pages
            "health_check",
            "health_check.db",
            "health_check.cache",
            "health_check.storage",
            "health_check.contrib.migrations",
            "health_check.contrib.psutil",
        ]
        if DEBUG
        else []
    ),
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "conreq._core.debug",
    "conreq._core.api",
    "conreq._core.app_store",
    "conreq._core.backup",
    "conreq._core.base",
    "conreq._core.database",
    "conreq._core.email",
    "conreq._core.initialization",
    "conreq._core.home",
    "conreq._core.landing",
    "conreq._core.password_reset",
    "conreq._core.pwa",
    "conreq._core.server_settings",
    "conreq._core.sign_in",
    "conreq._core.sign_up",
    "conreq._core.user_management",
    "conreq._core.user_settings",
    # Database Fields
    "colorfield",  # HEX colors in the DB
    "encrypted_fields",  # Encrypted text in the DB
    "solo",  # Single-row models in the DB
    "django_ace",  # Code hightlighted form fields
    "versionfield",  # Filterable/sortable version numbers fields in the DB
    # ASGI
    "reactpy_django",  # ReactJS for Python
    # API
    "rest_framework",  # OpenAPI Framework
    "rest_framework_api_key",  # API Key Manager
    "rest_framework.authtoken",  # API User Authentication
    # Miscellaneous
    "crispy_forms",  # Simplify generating HTML forms
    "crispy_bootstrap5",  # Bootstrap 5 support for Crispy Forms
    "django_tables2",  # Simplify generating HTML tables
    "huey.contrib.djhuey",  # Queuing background tasks
    "compressor",  # Minifies CSS/JS files
    "ordered_model",  # Ordered database models
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files through Django securely
    "compression_middleware.middleware.CompressionMiddleware",
    *(["silk.middleware.SilkyMiddleware"] if DEBUG else []),
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = METRICS_DIR
SILKY_ANALYZE_QUERIES = get_database_engine() != "SQLITE3"
SILKY_MAX_RECORDED_REQUESTS = 1000
WHITENOISE_MAX_AGE = 0 if DEBUG else 31536000
COMPRESS_OUTPUT_DIR = "minified"
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = "compressor.storage.BrotliCompressorFileStorage"
COMPRESS_FILTERS = {
    "css": ["compressor.filters.cssmin.rCSSMinFilter"],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
HUEY_FILENAME = DATABASE_DIR / "background_tasks.sqlite3"
HUEY = {
    "name": "huey",  # DB table name
    "huey_class": "conreq._core.database.SqliteHuey",  # Huey implementation to use
    "filename": HUEY_FILENAME,  # Sqlite filename
    "immediate": False,  # If True, run tasks synchronously
    "strict_fifo": True,  # Utilize Sqlite AUTOINCREMENT to have unique task IDs
    "consumer": {
        "workers": WEBSERVER_WORKERS * 5,  # TODO: Add setting to configure this
    },
}
FILE_UPLOAD_TEMP_DIR = TEMP_DIR
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
JAZZMIN_SETTINGS = {"custom_css": "conreq/jazzmin.css"}


# // DATA STORAGE //
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_DIR / "default.sqlite3",
        "OPTIONS": {
            "timeout": 3,  # 3 second query timeout
        },
    }
}
DATABASE_ROUTERS = ["conreq._core.database.router.DatabaseRouter"]
CACHE_SHARDS = min(WEBSERVER_WORKERS, 10)
CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": DATA_DIR / "cache",
        "TIMEOUT": 300,  # Default timeout of each key
        "SHARDS": CACHE_SHARDS,  # Number of cache DBs to create
        "DATABASE_TIMEOUT": 0.05 + (CACHE_SHARDS * 0.01),  # Query timeout
        "OPTIONS": {"size_limit": 2**30},  # 1 gigabyte max cache size
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
BACKUP_KEEP_MAX = 20
BACKUP_DATE_FORMAT = "%Y-%m-%d_at_%H%M"
BACKUP_COMPRESSION = "xz"


# // AUTHENTICATION //
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGIN_REDIRECT_URL = "landing"
LOGIN_URL = "sign_in"


# // COOKIES //
SESSION_COOKIE_NAME = "conreq_sessionidd"
CSRF_COOKIE_NAME = "conreq_csrftoken"
LANGUAGE_COOKIE_NAME = "conreq_language"


# // INTERNATIONALIZATION //
LANGUAGE_CODE = "en-US"
TIME_ZONE = get_localzone_name()
USE_TZ = True


# // STATIC FILES //
STATIC_ROOT = DATA_DIR / "static_processed"
STATIC_URL = f"{get_base_url()}static/"
STATICFILES_DIRS = [
    USER_STATICFILES_DIR,
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "files/"
if get_base_url(empty_if_unset=True):
    MEDIA_URL = get_base_url(append_slash=False) + MEDIA_URL
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# // EMAIL //
EMAIL_BACKEND = "conreq.app.services.email.EmailBackend"
EMAIL_SUBJECT_PREFIX = ""


# // USER INSTALLED APP PACKAGES //
# TODO: Add a user editable setting script
if not get_safe_mode():
    user_apps = find_apps()
    INSTALLED_APPS += user_apps
    if user_apps:
        _logger.info(
            "Booting with the following apps:%s", ("\n+ " + "\n+ ".join(user_apps))
        )
    else:
        _logger.warning("No user installed apps detected.")

    # Execute settings scripts from enabled Conreq Apps
    packages = find_packages()
    site_dir = Path(site.getsitepackages()[1])
    settings_files: list[Path] = []
    if not site.getsitepackages()[1].endswith("site-packages"):
        raise OSError(
            "Expected site-packages directory to end with 'site-packages', "
            f"but got '{site_dir}'."
        )
    for pkg_name in packages:
        # These are settings files defined in the package's directory
        dedicated_settings = site_dir / f"{pkg_name}" / "conreq_settings.py"
        if dedicated_settings.exists():
            settings_files.append(dedicated_settings)

        # These are settings files defined in the database's settings_script field
        simple_settings = APP_SETTINGS_DIR / f"{pkg_name}.py"
        if simple_settings.exists():
            settings_files.append(simple_settings)

    include(*settings_files)  # type: ignore


# // POSITION / TIMING SENSITIVE CODE //
# Debug django apps (must be near last)
if DEBUG:
    INSTALLED_APPS.extend(("silk", "drf_spectacular", "drf_spectacular_sidecar"))
# Auto delete dangling files app (must be near last)
INSTALLED_APPS.append("django_cleanup.apps.CleanupConfig")
# Conreq app loader (must be last)
if not get_safe_mode():
    INSTALLED_APPS.append("conreq._core.app_loader")
