import importlib

from conreq.utils.modules import find_wildcards, validate_conreq_modules
from conreq.utils.packages import find_packages, packages_to_modules


def find_apps() -> set[str]:
    """Returns all apps within installed packages. Apps must be declared
    within a package's `conreq_apps` list. If the declared app contains a
    trailing wildcard, all modules within the given directory are considered Django apps.
    """
    apps = set()
    user_packages = find_packages()
    modules = validate_conreq_modules(packages_to_modules(*user_packages))

    for module_str in modules:
        module = importlib.import_module(module_str)
        conreq_apps = getattr(module, "conreq_apps", None)
        if isinstance(conreq_apps, list):
            for app in conreq_apps:
                if app.endswith(".*"):
                    apps.update(find_wildcards(app))
                else:
                    apps.add(app)
    return apps
