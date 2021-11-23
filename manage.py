"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys

from conreq.utils.environment import get_safe_mode, set_env


def main():
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
        execute_from_command_line(sys.argv)
    except Exception as exception:
        run_in_safe_mode(exception)


def run_in_safe_mode(exception):
    try:
        print(
            "\x1b[91m"
            + "Conreq has crashed, attempting to restart in safe mode..."
            + "\x1b[0m"
        )
        set_env("SAFE_MODE", True, sys_env=True, dot_env=False)
        get_safe_mode.cache_clear()
        start_command = f"{sys.executable} {' '.join(arg for arg in sys.argv)}"
        subprocess.run(start_command)
    except Exception:
        raise exception


if __name__ == "__main__":
    main()
