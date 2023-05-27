"""Django's command-line utility for administrative tasks."""
import contextlib
import os
import subprocess
import sys

from conreq.utils.environment import set_env


# pylint: disable=import-outside-toplevel
def main():
    # TODO: If venv dependencies cause exceptions, try to reinstall Conreq dependencies via pip
    # Make sure we are in a venv
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("Conreq requires a virtual environment.")

    # Check if Django is installed
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conreq.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run Django
    try:
        if int(os.environ.get("SAFE_MODE_DEPTH", 0)) <= 1:
            execute_from_command_line(sys.argv)
    except Exception as exception:
        run_in_safe_mode(exception)


def run_in_safe_mode(exception):
    try:
        if int(os.environ.get("SAFE_MODE_DEPTH", 0)) >= 1:
            return

        import traceback

        traceback.print_exc()
        print(
            "\x1b[91m"
            + "Conreq has crashed, attempting to restart in safe mode..."
            + "\x1b[0m"
        )
        set_env("SAFE_MODE", True, sys_env=True, dot_env=False)

        set_env(
            "SAFE_MODE_DEPTH",
            int(os.environ.get("SAFE_MODE_DEPTH", 0)) + 1,
            sys_env=True,
            dot_env=False,
        )
        start_command = f'{sys.executable} {" ".join(sys.argv)}'
        subprocess.run(start_command.split(" "), check=True)
    except Exception as exception_2:
        raise exception from exception_2


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
