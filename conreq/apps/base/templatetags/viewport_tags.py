from django import template
from conreq.utils.generic import get_base_url
from django.urls import reverse

register = template.Library()

base_url_len = len(get_base_url()) + 1


@register.simple_tag
def viewport_url(namespace):
    url = reverse(namespace)
    return "#" + url[base_url_len:]


@register.simple_tag
def viewport_top_url(namespace):
    url = reverse(namespace)
    return "#" + "display/" + url[base_url_len:]