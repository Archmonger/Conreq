"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
import traceback


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

    # Run Conreq
    try:
        if int(os.environ.get("SAFE_MODE_DEPTH", 0)) <= 1:
            execute_from_command_line(sys.argv)

    # If Conreq crashes, try to restart in safe mode
    except Exception:
        if int(os.environ.get("SAFE_MODE_DEPTH", 0)) >= 1:
            return
        os.environ["SAFE_MODE"] = "true"
        os.environ["SAFE_MODE_DEPTH"] = str(
            int(os.environ.get("SAFE_MODE_DEPTH", 0)) + 1
        )
        traceback.print_exc()
        print(
            "\x1b[91m"
            + "Conreq has crashed, attempting to restart in safe mode..."
            + "\x1b[0m"
        )
        run_in_safe_mode()
    print("\x1b[91m" + "Conreq has crashed again. Giving up." + "\x1b[0m")


def run_in_safe_mode():
    start_command = f'{sys.executable} {" ".join(sys.argv)}'
    subprocess.run(start_command.split(" "), check=True)


if __name__ == "__main__":
    main()
