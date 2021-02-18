There are two environments to build Conreq for: Development and Production.

If you intend to edit Conreq's code, then proceed with the Development instructions.

---

## Creating a Development Environment

### Software

- Install [Python 3.8](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
- Install [Visual Studio Code](https://code.visualstudio.com/) (Optional: Any editor would work)
- _If using Windows:_ Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)

### Setting Up the Environment

1. Pull the repository from GitHub.
2. Open a terminal (ex. Command Prompt or PowerShell) as administrator at the root of the repository.
3. _If using Windows:_ type `set-executionpolicy remotesigned` and select Yes to All to allow external Python scripts to run on your computer.
4. Type `python -m venv venv` to create a Python virtual environment.
5. Type `./venv/Scripts/activate` to enter the virtual environment.
6. Type `pip install -r requirements.txt` to install all Python dependencies within the virtual environment.
7. Create or update the database by typing `python manage.py migrate`.
8. Type `python manage.py run_huey` to run the background task management system.
9. Open a new terminal and type `./venv/Scripts/activate`.
10. Type `python manage.py runserver` to run the development webserver.

---

## Creating a Production Environment

Follow all instructions laid out within [Creating a Development Environment](https://github.com/Archmonger/Conreq/wiki/Building-Guide#creating-a-development-environment), but do not execute `python manage.py runserver`. Instead, do the following:

1. Set your environment variable of `DEBUG` to `false`. The method of doing this will vary based on operating system.
2. Type `python manage.py collectstatic` to move static files (CSS/JS/images) to their production directory.
3. Type `python manage.py compress` to merge and compress static files.
4. Type `daphne conreq.asgi:application` to run the production webserver on `localhost:8000`. Here's some common execution parameters:
   - `daphne conreq.asgi:application --access-log logs\access.log` - Adds an access log file.
   - `daphne -b 0.0.0.0 conreq.asgi:application` - Binds the webserver to the `0.0.0.0` instead of localhost.
   - `daphne -p 8001 conreq.asgi:application` - Binds the webserver to port `8001` instead of `8000`.
   - `daphne -e ssl:8000:privateKey=key.pem:certKey=cert.pem conreq.asgi:application` - Binds the webserver to the `0.0.0.0` on port `8000` with SSL enabled. **_Note: Do not use `-p` or `-b` in this mode. Using `-e` always binds to `0.0.0.0`._**

---

## Visual Studio Code Configuration (optional)

### Visual Studio Code Extensions

- GitHub
- GitLens
- Python
- MagicPython

### Visual Studio Code Settings

1. If your terminal does not show venv (ex. `(venv) ...`), type `./venv/Scripts/activate`.
2. Type `pip install -r requirements_dev.txt` to install VS Code editor packages within the virtual environment.
3. Enable Python Formatting
   - Settings -> Editor: Format On Save -> `ON`
   - Settings -> Python Formatting Provider -> `Black`
4. Enabling Python Linting
   - Ctrl+Shift+P -> Python: Select Linter -> `pylint`
   - Settings -> Linting: Pylint Args -> Add Item -> `--disable=line-too-long,bare-except,bad-continuation`
