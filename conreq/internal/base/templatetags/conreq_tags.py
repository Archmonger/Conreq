from django import template
from django.urls import reverse

from conreq.utils.environment import get_base_url, get_env

register = template.Library()
BASE_URL_LEN = len(get_base_url())
SERVER_NAME = get_env("SERVER_NAME", "Conreq")
APP_DESCRIPTION = get_env("APP_DESCRIPTION", "Content Requesting")


@register.simple_tag
def viewport_url(namespace):
    url = reverse(namespace)
    return "#" + url[BASE_URL_LEN:]


@register.simple_tag
def viewport_top_url(namespace):
    url = reverse(namespace)
    return "#" + "/display" + url[BASE_URL_LEN:]


@register.simple_tag
def server_name():
    return SERVER_NAME


@register.simple_tag
def app_description():
    return APP_DESCRIPTION
