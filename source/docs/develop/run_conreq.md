There are two environments Conreq can exist in: [Development](#creating-a-development-environment) and [Production](#creating-a-production-environment).

If you intend to edit Conreq's code, then proceed with the Development instructions.

---

## Creating a Development Environment

### Software Required

-   Install [Python 3.8+](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
-   _If using Windows_: Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)
-   _Optional_: Install [Visual Studio Code](https://code.visualstudio.com/) (Any editor would work)

### Setting Up the Environment

1. Pull the repository from GitHub.
2. Open a terminal (ex. Command Prompt or PowerShell) as administrator at the root of the repository.
3. _If using Windows_
    - Type `set-executionpolicy remotesigned` and select Yes to All to allow external Python scripts to run on your computer.
4. Type `python -m venv .venv` to create a Python virtual environment called ".venv".
5. Type `./.venv/Scripts/activate` to enter the virtual environment.
6. Type `pip install -r requirements.txt` to install all Python dependencies within the virtual environment.
7. Type `python manage.py run_conreq` to run the webserver.

---

## Creating a Production Environment

Follow all instructions laid out within [Creating a Development Environment](#creating-a-development-environment), but before running `python manage.py run_conreq` do the following:

1. Set your environment variable of `DEBUG` to `false`. The method of doing this will [vary based on operating system](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
    - Doing this enables _a lot_ of **security features** that are mandatory for any user environment.
2. The webserver is conifgured with good defaults for most cases, but if you want to configure the webserver _(such as changing ports)_ See our [webserver documentation](/webserver/) for more information.

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
