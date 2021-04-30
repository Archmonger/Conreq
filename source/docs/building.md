There are two environments to build Conreq for: Development and Production.

If you intend to edit Conreq's code, then proceed with the Development instructions.

---

## Creating a Development Environment

### Software Required

-   Install [Python 3.8](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
-   _Optional_
    -   Install [Visual Studio Code](https://code.visualstudio.com/) (Any editor would work)
-   _If using Windows_
    -   Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)

### Setting Up the Environment

1. Pull the repository from GitHub.
2. Open a terminal (ex. Command Prompt or PowerShell) as administrator at the root of the repository.
3. _If using Windows_
    - Type `set-executionpolicy remotesigned` and select Yes to All to allow external Python scripts to run on your computer.
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

1. Set your environment variable of `DEBUG` to `false`. The method of doing this will [vary based on operating system](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
2. Type `python manage.py collectstatic` to move static files (CSS/JS/images) to their production directory.
3. Type `python manage.py compress` to merge and compress static files.
4. Type `hypercorn conreq.asgi:application` to run the production webserver on `localhost:8000`.
    - For more configuration parameters, see [Hypercorn's documentation](https://pgjones.gitlab.io/hypercorn/how_to_guides/configuring.html#configuration-options).

---

## Optional: Visual Studio Code Configuration

### VS Code Extensions

-   GitHub
-   GitLens
-   Python
-   MagicPython

### VS Code Settings

1. If your terminal does not show `(venv) ...`, type `./venv/Scripts/activate`.
2. Type `pip install -r requirements_dev.txt` to install VS Code editor packages within the virtual environment.
3. Enable Python Formatting
    - Settings -> Editor: Format On Save -> `ON`
    - Settings -> Python Formatting Provider -> `Black`
4. Enabling Python Linting
    - Ctrl+Shift+P -> Python: Select Linter -> `pylint`
    - Settings -> Linting: Pylint Args -> Add Item -> `--disable=line-too-long,bare-except,bad-continuation`
