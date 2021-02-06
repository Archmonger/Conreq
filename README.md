Conreq, a **Con**tent **Req**uesting platform.

[![Docker Pulls](https://img.shields.io/docker/pulls/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Stars](https://img.shields.io/docker/stars/roxedus/conreq?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Docker Hub](https://img.shields.io/badge/Open%20On-DockerHub-blue?style=flat-square)](https://hub.docker.com/r/roxedus/conreq)
[![Discord](https://img.shields.io/discord/440067432552595457?style=flat-square&label=Discord&logo=discord)](https://discord.gg/gQhGZzEjmX "Chat with the community and get realtime support!" )

# Conreq Beta Instructions

Have a question or want to contribute? Check out our [Development Guide](https://github.com/Archmonger/Conreq/wiki/Development-Guide) or join us on [Discord](https://discord.gg/gQhGZzEjmX)!

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

## Creating a Development Environment

### Software

- Install [Python 3.8](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
- Install [Visual Studio Code](https://code.visualstudio.com/)
- _If using Windows:_ Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)

### Setting Up the Environment

1. Pull the repository from GitHub.
2. Open a terminal (ex. Command Prompt or PowerShell) as administrator at the root of the repository.
3. _If using Windows:_ type `set-executionpolicy remotesigned` and select Yes to All to allow Python scripts to run on your computer.
4. Type `python -m venv venv` to create a Python virtual environment.
5. Type `./venv/Scripts/activate` to enter the virtual environment.
6. Type `pip install -r requirements.txt` to install all Python dependencies within the virtual environment.
7. Create and/or update the database by typing `python manage.py migrate`.
8. Create the Conreq admin account by typing `python manage.py createsuperuser`.
9. Run Conreq by typing `python manage.py runserver`

### Visual Studio Code Extensions (Optional)

- GitHub
- GitLens
- Python
- MagicPython

### Visual Studio Code Settings (Optional)

1. If your terminal does not show venv (ex. `(venv) ...`), type `./venv/Scripts/Activate`.
2. Type `pip install -r requirements_dev.txt` to install Python packages within the virtual environment.
3. Enable Python Formatting
   - Settings -> Editor: Format On Save -> `ON`
   - Settings -> Python Formatting Provider -> `Black`
4. Enabling Python Linting
   - Ctrl+Shift+P -> Python: Select Linter -> `pylint`
   - Settings -> Linting: Pylint Args -> Add Item -> `--disable=line-too-long,bare-except,bad-continuation`

# UX Design Mockups

[Desktop](https://xd.adobe.com/view/17a8150c-a224-467c-af36-36171641d656-42fb/)

[Mobile](https://xd.adobe.com/view/aaef68b5-ddb9-4987-a758-771215bfe578-ffbc/)

# Screenshots

![Login screen](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_1.png?raw=true)
![Discover tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_2.png?raw=true)
![More Info Tab](https://github.com/Archmonger/Conreq/blob/main/resources/screenshots/conreq_3.png?raw=true)
