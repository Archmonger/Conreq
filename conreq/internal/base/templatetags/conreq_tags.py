from django import template
from django.urls import reverse

from conreq.utils.environment import get_base_url, get_str_from_env

register = template.Library()
BASE_URL_LEN = len(get_base_url())
APP_NAME = get_str_from_env("APP_NAME", "Conreq")
APP_DESCRIPTION = get_str_from_env("APP_DESCRIPTION", "Content Requesting")


@register.simple_tag
def viewport_url(namespace):
    url = reverse(namespace)
    return "#" + url[BASE_URL_LEN:]


@register.simple_tag
def viewport_top_url(namespace):
    url = reverse(namespace)
    return "#" + "/display" + url[BASE_URL_LEN:]


@register.simple_tag
def app_name():
    return APP_NAME


@register.simple_tag
def app_description():
    return APP_DESCRIPTION
