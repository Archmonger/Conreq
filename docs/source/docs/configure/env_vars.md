Environment variables can be used to customize core Conreq features at boot.

## Environment Variables File

Editing Conreq's `settings.env` file is the recommended way of adding environment variables.

Here are some common locations of this file.

| Operating System                   | Location                             |
| ---------------------------------- | ------------------------------------ |
| Manually Run (Windows/Linux/MacOS) | `<CONREQ_DIR>/data/settings.env`     |
| Unraid Docker                      | `<APP_DATA_DIR>/conreq/settings.env` |
| Docker                             | `/config/settings.env`               |

## System Variables

Variables can alternatively be set through the system's evironment variables.

_Note: These variables take priority over those stored in `settings.env`._

| Operating System                   | Location                                                                                                                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Manually Run (Windows/Linux/MacOS) | [Varies depending on operating system.](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)                          |
| Unraid Docker                      | Through a docker's `Edit` menu, click `Add another Path, Port, Variable, Label, or Device`, and then under `Config Type` select `Variable`. |
| Docker                             | [Add as a `-e` parameter.](https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers)                  |

## Available Variables

```bash
# General Settings
TZ = America/Los_Angeles                # default: UTC (Timezone for log files, in "TZ Database" format)
BASE_URL = requests                     # default: None
APP_NAME = RequestCentral               # default: Conreq
APP_DESCRIPTION = Get yo stuff!         # default: Content Requesting
ARR_REFRESH_INTERNAL = */15             # default: */1 (Cron minutes for Sonarr/Radarr library refresh)
LOG_LEVEL = ERROR                       # default: WARNING
CONREQ_ENV_PREFIX = CONREQ              # default: None

# Data Storage
DATA_DIR = /example/directory           # default: /config (Defaults to "data" outside of docker)
DB_ENGINE = MYSQL                       # default: SQLITE3
MYSQL_CONFIG_FILE = /config/mysql.cnf   # default: None

# Security
SSL_SECURITY = True                     # default: False (True enables advanced SSL security features)
PWNED_VALIDATOR = False                 # default: True (False disables checking for compromised passwords)
X_FRAME_OPTIONS = SAMEORIGIN            # default: DENY (False disables X-Frame-Options)
ALLOWED_HOST = 192.168.0.199            # default: * (Allows all hosts)
DEBUG = False                           # default: False (Disable security features, only enable this during development. Defaults to True outside of docker.)

# Email
EMAIL_USE_TLS = False                   # default: True
EMAIL_PORT = 587                        # default: None
EMAIL_HOST = smtp.gmail.com             # default: None
EMAIL_HOST_USER = myself@gmail.com      # default: None
EMAIL_HOST_PASSWORD = dogmemes123       # default: None
```
