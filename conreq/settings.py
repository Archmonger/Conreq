"""
Django settings for Conreq project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import logging
import os
import secrets
import sys
from importlib import import_module
from logging.config import dictConfig as logging_config
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from split_settings.tools import include
from tzlocal import get_localzone_name

from conreq import Seconds, config
from conreq.utils.apps import find_apps
from conreq.utils.environment import (
    get_base_url,
    get_database_engine,
    get_debug_mode,
    get_env,
    get_home_url,
    get_safe_mode,
    set_env,
)
from conreq.utils.packages import find_packages

_logger = logging.getLogger(__name__)

# Project Directories
ROOT_DIR = Path(__file__).resolve().parent.parent
INTERNAL_DIR = ROOT_DIR / "conreq" / "internal"
DATA_DIR = get_env("DATA_DIR", ROOT_DIR / "data", dot_env=False)
DATABASE_DIR = DATA_DIR / "database"
PACKAGES_DIR = DATA_DIR / "packages" / "__installed__"
PACKAGES_DEV_DIR = DATA_DIR / "packages" / "develop"
MEDIA_DIR = DATA_DIR / "files"
MEDIA_SERVE_DIR = MEDIA_DIR / "serve"
METRICS_DIR = MEDIA_DIR / "metrics"
BACKUP_DIR = DATA_DIR / "backup"
TEMP_DIR = DATA_DIR / "temp"
USER_STATICFILES_DIR = DATA_DIR / "static"
LOG_DIR = DATA_DIR / "logs"
MAKE_DIRS: list[Path] = [
    DATA_DIR,
    DATABASE_DIR,
    PACKAGES_DIR,
    PACKAGES_DEV_DIR,
    MEDIA_DIR,
    MEDIA_SERVE_DIR,
    METRICS_DIR,
    BACKUP_DIR,
    TEMP_DIR,
    USER_STATICFILES_DIR,
    LOG_DIR,
]
if not DATA_DIR.parent.exists:
    raise OSError
for directory in MAKE_DIRS:
    if not directory.exists():
        directory.mkdir(parents=True)


# App Template Diretories
APP_TEMPLATE_DIR = ROOT_DIR / "conreq" / "templates"
PACKAGE_TEMPLATE = APP_TEMPLATE_DIR / "package"
PACKAGE_SLIM_TEMPLATE = APP_TEMPLATE_DIR / "package_slim"
APP_TEMPLATE = APP_TEMPLATE_DIR / "app"
APP_SLIM_TEMPLATE = APP_TEMPLATE_DIR / "app_slim"


# Environment Variables
DOTENV_FILE: Path = DATA_DIR / "settings.env"
if not DOTENV_FILE.exists():
    with open(DOTENV_FILE, "w", encoding="utf-8") as fp:
        pass
DEBUG = get_debug_mode()
SAFE_MODE = get_safe_mode()
DB_ENGINE = get_database_engine()
BASE_URL = get_base_url()
HOME_URL = get_home_url()
WEBSERVER_WORKERS = get_env("WEBSERVER_WORKERS", 3, return_type=int)


# Basic Configuration
CONREQ_VERSION = "0.20.32"
APP_STORE_VERSION = get_env("APP_STORE_VERSION", "1")


# Python Packages
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = METRICS_DIR
SILKY_ANALYZE_QUERIES = DB_ENGINE != "SQLITE3"
SILKY_MAX_RECORDED_REQUESTS = 1000
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
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
    "huey_class": "conreq._core.background_tasks.SqliteHuey",  # Huey implementation to use
    "filename": HUEY_FILENAME,  # Sqlite filename
    "immediate": False,  # If True, run tasks synchronously
    "strict_fifo": True,  # Utilize Sqlite AUTOINCREMENT to have unique task IDs
    "consumer": {
        "workers": 20,
    },
}
IDOM_BASE_URL = BASE_URL[1:] + "idom/"
os.environ["IDOM_DEBUG_MODE"] = str(int(DEBUG))
FILE_UPLOAD_TEMP_DIR = TEMP_DIR
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Logging
CONREQ_LOG_FILE = LOG_DIR / "conreq.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"
LOG_LEVEL = get_env("LOG_LEVEL", "INFO" if DEBUG else "WARNING")
LOGGING_INITIAL = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
        },
        "minimal": {
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
        "django": {
            "level": LOG_LEVEL,
        },
        "hypercorn": {
            "level": LOG_LEVEL,
        },
        "conreq": {
            "level": LOG_LEVEL,
        },
        "huey": {
            "level": LOG_LEVEL,
        },
    },
}
for logger_name in LOGGING_INITIAL["loggers"]:
    LOGGING_INITIAL["loggers"][logger_name]["handlers"] = ["console", "conreq_logs"]
if DEBUG and os.environ.get("RUN_MAIN", None) != "true":
    LOGGING = {"version": 1}
else:
    LOGGING = LOGGING_INITIAL
logging_config(LOGGING)


# Security Settings
SESSION_COOKIE_AGE = get_env("SESSION_COOKIE_AGE", Seconds.month * 3, return_type=int)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = get_env("SECURE_REFERRER_POLICY", "")
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", return_type=list) or [
    get_env("ALLOWED_HOST", "*")
]
SECURE_BROWSER_XSS_FILTER = True


# API Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "conreq._core.api.permissions.HasAPIKey",
    ],
}


# Encryption
FIELD_ENCRYPTION_KEYS = [get_env("DB_ENCRYPTION_KEY")]
SECRET_KEY = get_env("WEB_ENCRYPTION_KEY")
if not FIELD_ENCRYPTION_KEYS[0]:
    FIELD_ENCRYPTION_KEYS = [secrets.token_hex(32)]
    set_env("DB_ENCRYPTION_KEY", FIELD_ENCRYPTION_KEYS[0])
if not SECRET_KEY:
    SECRET_KEY = set_env("WEB_ENCRYPTION_KEY", get_random_secret_key())[1]


# Django Apps & Middleware
INSTALLED_APPS = [
    *(
        [
            "jazzmin",
            "django.contrib.admin",
            "django.contrib.admindocs",
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
    "conreq._core.api",
    "conreq._core.app_store",
    "conreq._core.base",
    "conreq._core.background_tasks",
    "conreq._core.debug",
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
    # FIXME: When DEBUG is false.... 'django-versionfield/fonts/glyphicons-halflings-regular.eot' could not be found
    # "versionfield",  # Allow for version numbers in the DB
    # ASGI
    "channels",  # Websocket library
    "django_idom",  # React JS for Python
    # API
    "rest_framework",  # OpenAPI Framework
    "rest_framework_api_key",  # API Key Manager
    "rest_framework.authtoken",  # API User Authentication
    # Miscellaneous
    "crispy_forms",  # Simplify generating HTML forms
    "django_tables2",  # Simplify generating HTML tables
    "huey.contrib.djhuey",  # Queuing background tasks
    "compressor",  # Minifies CSS/JS files
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


# URL Routing and Page Rendering
ROOT_URLCONF = "conreq.urls"
ASGI_APPLICATION = "conreq.asgi.application"
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


# Databases and Caches
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_DIR / "default.sqlite3",
        "OPTIONS": {
            "timeout": 3,  # 3 second query timeout
        },
    }
}
CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": DATA_DIR / "cache",
        "TIMEOUT": 300,  # Default timeout of each key
        "SHARDS": min(WEBSERVER_WORKERS, 10),  # Number of cache DBs to create
        "DATABASE_TIMEOUT": 0.1,  # 100ms query timeout
        "OPTIONS": {"size_limit": 2 ** 30},  # 1 gigabyte max cache size
    }
}
BACKUP_KEEP_MAX = 20
BACKUP_DATE_FORMAT = "%Y-%m-%d_at_%H%M%S"
BACKUP_COMPRESSION = "xz"


# User Authentication
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


# Internationalization
LANGUAGE_CODE = "en-US"
TIME_ZONE = get_localzone_name()


# Static Files (CSS, JavaScript, Images)
STATIC_ROOT = DATA_DIR / "static_processed"
STATIC_URL = BASE_URL + "static/"
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


# Email
EMAIL_BACKEND = "conreq.app.services.email.EmailBackend"
EMAIL_SUBJECT_PREFIX = ""


# Add packages folder to Python's path
sys.path.append(str(PACKAGES_DEV_DIR))
sys.path.append(str(PACKAGES_DIR))
if not SAFE_MODE:
    INSTALLED_APPS += find_apps()


# Run startup.py
packages = find_packages()
for package in packages:
    try:
        import_module(".".join([package, "startup"]))
    except ModuleNotFoundError:
        pass
    except Exception as exception:
        _logger.error('%s startup script has failed due to "%s"!', package, exception)


# Execute settings scripts from Conreq Apps
include(*config.startup.setting_scripts)


# Add conditional apps
if DEBUG:
    # Performance analysis tools
    INSTALLED_APPS.append("silk")
    # API docs generator
    INSTALLED_APPS.append("drf_yasg")

# Automatically delete dangling files
INSTALLED_APPS.append("django_cleanup.apps.CleanupConfig")


# Ensure Conreq app loader comes last
if not SAFE_MODE:
    INSTALLED_APPS.append("conreq._core.app_loader")
