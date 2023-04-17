from django import template
from django.urls import reverse

from conreq.utils.environment import get_base_url, get_str_from_env

register = template.Library()
base_url_len = len(get_base_url())
conreq_app_name = get_str_from_env("APP_NAME", "Conreq")
conreq_app_description = get_str_from_env("APP_DESCRIPTION", "Content Requesting")


@register.simple_tag
def viewport_url(namespace):
    url = reverse(namespace)
    return f"#{url[base_url_len:]}"


@register.simple_tag
def viewport_top_url(namespace):
    url = reverse(namespace)
    return "#" + "/display" + url[base_url_len:]


@register.simple_tag
def app_name():
    return conreq_app_name


@register.simple_tag
def app_description():
    return conreq_app_description


@register.filter
def contains_valid_id(results):
    if isinstance(results, list):
        for result in results:
            if isinstance(result, dict) and result.get("conreq_valid_id"):
                return True
    return False


@register.filter
def email_enabled(_):
    """Temporary hacky shortcut to determine if email is enabled."""
    from django.conf import settings

    return settings.EMAIL_ENABLED
