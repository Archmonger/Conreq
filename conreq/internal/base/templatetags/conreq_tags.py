from django import template
from django.urls import reverse

from conreq.utils.environment import get_base_url, get_env

register = template.Library()
BASE_URL_LEN = len(get_base_url())
SERVER_NAME = get_env("SERVER_NAME", "Conreq")
SERVER_DESCRIPTION = get_env("SERVER_DESCRIPTION", "A hub for great things.")


@register.simple_tag
def server_name():
    return SERVER_NAME


@register.simple_tag
def app_description():
    return SERVER_DESCRIPTION
