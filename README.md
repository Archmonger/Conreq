# Conreq Public Alpha Instructions

Want to contribute? Check out our [Development Guide](https://github.com/Archmonger/Conreq/wiki/Development-Guide) and join us on [Discord](https://discord.gg/b4B7zFCB5E)!

## Installation (Deployment Environment)

Install through [Docker](https://github.com/Roxedus/docker-conreq).
Available environment variables:

```javascript
DEBUG = false                             //default: true (disabling debug will enable security features)
DATA_DIR = /example/directory             //default: none (uses base directory)
USE_ROLLING_SECRET_KEY = true             //default: false
DB_ENGINE = MYSQL                         //default: SQLITE3
MYSQL_CONFIG_FILE = /location/to/file.cnf //default: none
BASE_URL = requests                       //default: none
USE_SSL = true                            //default: false
SSL_CERT = /path/to/cert.pem              //default: none
SSL_KEY = /path/to/key.poem               //default: none
```

## Creating a Development Environment

### Software

- Install [Python 3.8](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
- Install [Visual Studio Code](https://code.visualstudio.com/)
- _If using Windows:_ Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_ -> _MSVC_ and _Windows 10 SDK_)

### Setting Up the Environment

1. Pull the repository from GitHub.
2. Navigate to the repository folder. At this folder location, open PowerShell as administrator.
3. Type `python -m venv venv` to create a virtual environment.
4. _If using Windows:_ type `set-executionpolicy remotesigned` and select Yes to All to allow Python scripts to run on your computer.
5. Type `./venv/Scripts/activate` to enter the virtual environment.
6. Type `pip install -r requirements.txt` to install Python packages within the virtual environment.
7. Open the project folder in Visual Studio Code (File -> Open Folder).
8. Open up the terminal within VS code.
9. Create the Django database by typing `./venv/Scripts/python.exe manage.py migrate`.
10. Create the Django admin account by typing `./venv/Scripts/python.exe manage.py createsuperuser`.
11. Run the Django project by typing `./venv/Scripts/python.exe manage.py runserver`

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
