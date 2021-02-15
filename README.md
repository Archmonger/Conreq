# Conreq Beta

[![Docker Pulls](https://img.shields.io/docker/pulls/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Stars](https://img.shields.io/docker/stars/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Hub](https://img.shields.io/badge/Open%20On-DockerHub-blue?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Discord](https://img.shields.io/discord/440067432552595457?style=flat-square&label=Discord&logo=discord)](https://discord.gg/gQhGZzEjmX "Chat with the community and get realtime support!")

Conreq, a **Con**tent **Req**uesting platform.

Want to join the community or have a question? Join us on [Discord](https://discord.gg/gQhGZzEjmX), discuss on [GitHub Discussions](https://github.com/Archmonger/Conreq/discussions), or see our planned features and roadmap on [GitHub Projects](https://github.com/Archmonger/Conreq/projects)!

Are you a developer and want to contribute? Check out our [Building Guide](https://github.com/Archmonger/Conreq/wiki/Building-Guide) and [Programmers Guide](https://github.com/Archmonger/Conreq/wiki/Programmers-Guide)!

## Installation (Production Environment)

Install through **[Unraid Community Applications](https://squidly271.github.io/forumpost0.html)**, **[Docker](https://github.com/Roxedus/docker-conreq)**, or **[Dockerhub](https://registry.hub.docker.com/r/roxedus/conreq)**.

Here's a list of all available environment variables:

```python
# General Settings
TZ = "America/Los_Angeles"                # default: UTC (timezone for log files, in "TZ Database" format)
BASE_URL = "requests"                     # default: none

# Data Storage
DATA_DIR = "/example/directory"           # default: /config (defaults to "data" outside of docker)
DB_ENGINE = "MYSQL"                       # default: SQLITE3
MYSQL_CONFIG_FILE = "/config/mysql.cnf"   # default: none

# Security
DEBUG = False                             # default: true (NEVER enable in production. Disables ALL security features.)
ROTATE_SECRET_KEY = True                  # default: false (will sign out users when conreq restarts)
X_FRAME_OPTIONS = "SAMEORIGIN"            # default: DENY (false will disable X-Frame-Options)
USE_SSL = True                            # default: false
SSL_CERT = "/path/to/cert.pem"            # default: none
SSL_KEY = "/path/to/key.pem"              # default: none
```

# Screenshots

| ![Login screen](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_1.png?raw=true) | ![Discover tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_2.png?raw=true) |
| :---------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------: |
|                                                Login Screen                                                 |                                                Discover Tab                                                 |

| ![More Info Tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_3.png?raw=true) | ![Content Preview Modal](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_4.png?raw=true) |
| :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------: |
|                                                More Info Tab                                                 |                                                Content Preview Modal                                                 |

| ![Discover Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_5.png?raw=true) | ![More Info Tab Mobile](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_6.png?raw=true) |
| :----------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------: |
|                                                Discover Tab Mobile                                                 |                                               More Info Tab on Mobile                                               |
