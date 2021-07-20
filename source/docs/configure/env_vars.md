Environment variables can be used to customize core Conreq features at boot.

If running outside of docker, the method of setting environment variables will [vary based on operating system](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).

For Unraid Docker installations, this will be done by clicking `Add another Path, Port, Variable, Label, or Device` through a docker's `Edit` menu, and then selecting a `Config Type` of `Variable`.

For regular docker installations, you can use the `-e` parameter, such as `docker run -e 'DB_ENGINE'='MYSQL' -e 'MYSQL_CONFIG_FILE'='/config/mysql.cnf`.

If using Docker Compose, see the [relevant documentation](https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers).

## Available Variables

```python
# General Settings
BASE_URL = "requests"                     # default: None
APP_NAME = "RequestCentral"               # default: Conreq
APP_DESCRIPTION = "Get yo stuff!"         # default: Content Requesting
ARR_REFRESH_INTERNAL = "*/15"             # default: */1 (Cron minutes for Sonarr/Radarr library refresh)
LOG_LEVEL = "ERROR"                       # default: WARNING
CONREQ_ENV_PREFIX = "CONREQ"              # default: None (Prefix for all these environment variables)

# Data Storage
DATA_DIR = "/example/directory"           # default: /config (Defaults to "data/" outside of docker)
DB_ENGINE = "MYSQL"                       # default: SQLITE3
MYSQL_CONFIG_FILE = "/config/mysql.cnf"   # default: None

# Security
SSL_SECURITY = "True"                     # default: False (True enables advanced SSL security features)
PWNED_VALIDATOR = "False"                 # default: True (False disables checking for compromised passwords)
X_FRAME_OPTIONS = "SAMEORIGIN"            # default: DENY (False disables X-Frame-Options)
ALLOWED_HOST = "192.168.0.199"            # default: * (Allows all hosts)
DEBUG = "False"                           # default: False (Disable security features, only enable this during development. Defaults to True outside of docker.)

# Email
EMAIL_USE_TLS = "False"                   # default: True
EMAIL_PORT = "587"                        # default: None
EMAIL_HOST = "smtp.gmail.com"             # default: None
EMAIL_HOST_USER = "myself@gmail.com"      # default: None
EMAIL_HOST_PASSWORD = "dogmemes123"       # default: None
```
