# Conreq Pre-Alpha Instructions

## Prerequisites

- Install [Python 3.8](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
- Install [Visual Studio Code](https://code.visualstudio.com/)
- _If using Windows:_ Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_ -> _MSVC_)

## Set up the environment

1. Pull the repository from GitHub.
2. Navigate to the repository folder. At this folder location, open PowerShell as administrator.
3. Type `python -m venv venv` to create a virtual environment.
4. _If using Windows:_ type `set-executionpolicy remotesigned` and select Yes to All to allow python scripts to run on your computer.
5. Type `./venv/Scripts/activate` to enter the virtual environment.
6. Type `pip install -r requirements.txt` to install Python packages within the virtual environment.
7. Open the project folder in Visual Studio Code (File -> Open Folder).
8. Open up the terminal within VS code.
9. Create the Django database by typing `./venv/Scripts/python.exe manage.py migrate`.
10. Create the Django admin account by typing `./venv/Scripts/python.exe manage.py createsuperuser`.
11. Create a `credentials.json` file at the root of the project folder.

    - Must contain the following values:
    - ```json
      {
        "sonarr_url": "",
        "sonarr_key": "",
        "radarr_url": "",
        "radarr_key": ""
      }
      ```

12. Run the Django project by typing `./venv/Scripts/python.exe manage.py runserver`

## Visual Studio Code Extensions (Optional)

- GitHub
- GitLens
- Python
- MagicPython

## Visual Studio Code Settings (Optional)

1. If your terminal does not show venv (ex. `(venv) ...`), type `./venv/Scripts/Activate`.
2. Type `pip install -r requirements_dev.txt` to install Python packages within the virtual environment.
3. Enable Python Formatting
   - Settings -> Editor: Format On Save -> `ON`
   - Settings -> Python Formatting Provider -> `Black`
4. Enabling Python Linting
   - Ctrl+Shift+P -> Python: Select Linter -> `pylint`
   - Settings -> Linting: Pylint Args -> Add Item -> `--disable=line-too-long,bare-except,bad-continuation`
