???+ summary

    There are two environments Conreq can exist in: [Development](#creating-a-development-environment) and [Production](#creating-a-production-environment).

    If you intend to edit Conreq's code, then proceed with the Development instructions.

??? info "Special instruction for Windows users"

    Windows users will need to type `set-executionpolicy remotesigned` in terminal and select Yes to All to allow external Python scripts to run on your computer.

You will need to follow the steps below in order to create and run Conreq from source code.

1. Pull the repository from GitHub.
2. Open a terminal (ex. Command Prompt) as administrator at the root of the repository.
3. Type `python -m venv .venv` to create a Python virtual environment called ".venv".
4. Type `./.venv/Scripts/activate` to enter the virtual environment.
    - The method of doing this may vary based on operating system.
5. Type `pip install -r requirements.txt` to install all Python dependencies within the virtual environment.
6. Set your `DEBUG` environment variable to `true`.
    - This can either be done within system variables, or within Conreq's `settings.env` file.
    - Doing this disables _a lot_ of **security features**.
7. Type `python manage.py run_conreq` to run the development webserver.

??? question "How do I convert this to a Production environment?"

    Follow all instructions laid out within [Creating a Development Environment](#creating-a-development-environment), however, set your `DEBUG` environment variable to `false`.

    Then, Conreq will boot in production mode the next time you use `python manage.py run_conreq`.
