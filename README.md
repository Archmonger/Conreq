# Conreq Beta

[![Docker Hub](https://img.shields.io/badge/Docker-DockerHub-blue?style=flat-square)](https://hub.docker.com/r/archmonger/conreq) [![GitHub Container Registry](https://img.shields.io/badge/Docker-GitHub-blue?style=flat-square)](https://github.com/Archmonger/Conreq/pkgs/container/conreq) [![Discord](https://img.shields.io/discord/440067432552595457?style=flat-square&label=Discord&logo=discord)](https://discord.gg/gQhGZzEjmX "Chat with the community and get realtime support!")

## Notice - July 11th, 2022

Conreq is currently undergoing an architectural shift. The biggest change will be the addditional of an app store for adding/removing features to Conreq.

Included in the box will only be basic features such as user authentication/management. Features such as content requesting will be installable as apps.

As such, in the future Conreq will be designated as a web app platform.

See the [app store PR](https://github.com/Archmonger/Conreq/pull/295) for more details.

---

Want to join the community or have a question? Join us on [Discord](https://discord.gg/gQhGZzEjmX), discuss on [GitHub Discussions](https://github.com/Archmonger/Conreq/discussions), or see our planned features and roadmap on [GitHub Projects](https://github.com/Archmonger/Conreq/projects)!

Looking for more info? Are you a developer and want to contribute? Check out our [Documentation](https://archmonger.github.io/Conreq/)!

## Installation (Production Environment)

Install through [Unraid Community Applications](https://squidly271.github.io/forumpost0.html), or [Docker](https://archmonger.github.io/Conreq/latest/install/docker/).

Here's a list of all available environment variables:

```nginx
# General Settings
TZ = America/Los_Angeles         # default: UTC (Timezone for log files, in "TZ Database" format)
BASE_URL = requests              # default: None
APP_NAME = RequestCentral        # default: Conreq
APP_DESCRIPTION = Get yo stuff!  # default: Content Requesting
ARR_REFRESH_INTERNAL = */15      # default: */1 (Cron minutes for Sonarr/Radarr library refresh)
LOG_LEVEL = ERROR                # default: WARNING
CONREQ_ENV_PREFIX = CONREQ       # default: None

# Data Storage
DATA_DIR = /example/directory          # default: /config (Defaults to "data" outside of docker)
DB_ENGINE = MYSQL                      # default: SQLITE3
MYSQL_CONFIG_FILE = /config/mysql.cnf  # default: None

# Security
SSL_SECURITY = True                      # default: False (True enables advanced SSL security features)
PWNED_VALIDATOR = False                  # default: True (False disables checking for compromised passwords)
ALLOWED_HOST = 192.168.0.199             # default: * (Comma separated list. Asterisk allows all hosts.)
TRUSTED_ORIGINS = https://*.example.com  # default: None (Comma separated list. Required to be set if using https.)
DEBUG = True                             # default: False (Only enable this during development or testing.)

# Email (Required for password reset features)
EMAIL_USE_TLS = False               # default: True
EMAIL_PORT = 587                    # default: None
EMAIL_HOST = smtp.gmail.com         # default: None
EMAIL_HOST_USER = myself@gmail.com  # default: None
EMAIL_HOST_PASSWORD = dogmemes123   # default: None
```

# Screenshots

| ![Login screen](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_discover.png?raw=true) | ![Discover tab](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_more_info.png?raw=true) |
| :-: | :-: |
| Discover (Desktop) | More Info (Desktop) |

| ![More Info Tab](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_modal_episode_selection.png?raw=true) | ![Content Preview Modal](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_modal_filter.png?raw=true) |
| :-: | :-: |
| Episode Selection Modal (Desktop) | Filter Modal (Desktop) |

| ![Discover Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_modal_preview.png?raw=true) | ![More Info Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/desktop_sign_in.png?raw=true) |
| :-: | :-: |
| Preview Modal (Desktop) | Sign In (Desktop) |

| ![Discover Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_discover.png?raw=true) | ![More Info Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_more_info.png?raw=true) |
| :-: | :-: |
| Discover (Mobile) | More Info (Mobile) |

| ![Discover Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_modal_episode_selection.png?raw=true) | ![More Info Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_modal_filter.png?raw=true) |
| :-: | :-: |
| Episode Selection Modal (Mobile) | Filter Modal (Mobile) |

| ![Discover Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_registration.png?raw=true) | ![More Info Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/misc/screenshots/mobile_sign_in.png?raw=true) |
| :-: | :-: |
| Registration (Mobile) | Sign In (Mobile) |
