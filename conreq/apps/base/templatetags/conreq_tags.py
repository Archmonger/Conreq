import os

from conreq.utils.generic import get_base_url
from django import template
from django.urls import reverse

register = template.Library()
base_url_len = len(get_base_url()) + 1
conreq_app_name = os.environ.get("APP_NAME", "Conreq")
conreq_app_description = os.environ.get("APP_DESCRIPTION", "Content Requesting")


@register.simple_tag
def viewport_url(namespace):
    url = reverse(namespace)
    return "#" + url[base_url_len:]


@register.simple_tag
def viewport_top_url(namespace):
    url = reverse(namespace)
    return "#" + "display/" + url[base_url_len:]


@register.simple_tag
def app_name():
    return conreq_app_name


@register.simple_tag
def app_description():
    return conreq_app_description
