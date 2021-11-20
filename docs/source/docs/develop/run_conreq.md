There are two environments Conreq can exist in: [Development](#creating-a-development-environment) and [Production](#creating-a-production-environment).

If you intend to edit Conreq's code, then proceed with the Development instructions.

---


## Software Required

-   Install [Python 3.9+](https://www.python.org/downloads/)
    -   Make sure to select "Add Python 3.x to PATH" during installation.
    -   Easiest if this is the only version of python on your computer
-   _If using Windows_: Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)
-   _Optional_: Install [Visual Studio Code](https://code.visualstudio.com/) (Any editor would work)


## Creating a Development Environment

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
    - Doing this enables _a lot_ of **security features**.
2. The webserver is conifgured with good defaults for most cases. But if you want to configure the webserver see our [webserver documentation](/Conreq/configure/webserver/) for more information.
3. Type `python manage.py run_conreq` to run the webserver.

