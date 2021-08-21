from django.apps import AppConfig


class {{ camel_case_subapp_name }}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ app_name }}.{{ subapp_name }}'
