"""
App Configuration for {{ verbose_name }}.

Stores basic information to let Django know about your app.

Additonal variables can be created in here to store metadata and
configuration values for your app.

See more information in the Django AppConfig docs.
"""
from django.apps import AppConfig

MODULE = __name__
PACKAGE = MODULE[: MODULE.find(".")]
APP = MODULE[: MODULE.rfind(".")]

class {{ camel_case_app_name }}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP
    label = verbose_name = "{{ verbose_name }}"

    def ready(self):
        """Code that only executes after Django has been initialized."""
        pass
