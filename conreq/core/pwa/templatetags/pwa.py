import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from .. import apps

register = template.Library()


@register.filter(is_safe=True)
def js(obj):
    """Transform a python object so it can be safely used in javascript/JSON."""
    return mark_safe(json.dumps(obj, cls=DjangoJSONEncoder))


@register.inclusion_tag("pwa.html", takes_context=True)
def progressive_web_app_meta(context):  # pylint: disable=unused-argument
    # Pass all PWA_* settings into the template
    return {
        setting_name: getattr(apps, setting_name)
        for setting_name in dir(apps)
        if setting_name.startswith("PWA_")
    }
