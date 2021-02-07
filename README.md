Conreq, a **Con**tent **Req**uesting platform.

[![Docker Pulls](https://img.shields.io/docker/pulls/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Stars](https://img.shields.io/docker/stars/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Hub](https://img.shields.io/badge/Open%20On-DockerHub-blue?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Discord](https://img.shields.io/discord/440067432552595457?style=flat-square&label=Discord&logo=discord)](https://discord.gg/gQhGZzEjmX "Chat with the community and get realtime support!" )

# Conreq Beta Instructions

Have a question or want to contribute? Join us on [Discord](https://discord.gg/gQhGZzEjmX). Also, check out our [Building Guide](https://github.com/Archmonger/Conreq/wiki/Building-Guide) and [Development Guide](https://github.com/Archmonger/Conreq/wiki/Development-Guide)!

## Installation (Deployment Environment)

Install through Unraid Community Applications, or directly through [Docker](https://github.com/Roxedus/docker-conreq).
Here's a list of all available environment variables:

```python
# General Settings
TZ = "America/Los_Angeles"                # default: Europe/London (timezone for log files, in "TZ Database" format)

# Data Storage
BASE_URL = "requests"                     # default: none
DATA_DIR = "/example/directory"           # default: ./data
DB_ENGINE = "MYSQL"                       # default: SQLITE3
MYSQL_CONFIG_FILE = "/config/mysql.cnf"   # default: none

# Security
DEBUG = False                             # default: true (true enables security features)
USE_ROLLING_SECRET_KEY = True             # default: false (sign users out when app restarts)
X_FRAME_OPTIONS = "SAMEORIGIN"            # default DENY (false disables X-Frame-Options)
USE_SSL = True                            # default: false
SSL_CERT = "/path/to/cert.pem"            # default: none
SSL_KEY = "/path/to/key.pem"              # default: none
```

# Screenshots

![Login screen](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_1.png?raw=true)
![Discover tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_2.png?raw=true)
![More Info Tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_3.png?raw=true)
