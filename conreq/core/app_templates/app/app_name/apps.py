"""
App Configuration for {{ verbose_name }}.

Stores basic information to let Django know about your app.

Additonal variables can be created in here to store metadata and
configuration values for your app.

See more information in the Django AppConfig docs.
"""
from django.apps import AppConfig

MODULE = __name__
APP = MODULE[: MODULE.rfind(".")]

class {{ camel_case_app_name }}Config(AppConfig):
    name = APP
    verbose_name = "{{ verbose_name }}"
    label = "{{ app_name }}"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """Code that only executes after Django has been initialized."""
        pass
