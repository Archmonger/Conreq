import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from ..apps import PwaConfig

register = template.Library()


@register.filter(is_safe=True)
def jsonify(obj):
    """Transform a python object so it can be safely used in javascript/JSON."""
    return mark_safe(json.dumps(obj, cls=DjangoJSONEncoder))


@register.inclusion_tag("pwa.html", takes_context=True)
def progressive_web_app_meta(context):  # pylint: disable=unused-argument
    # Pass all PWA_* settings into the template
    return {"pwa": PwaConfig.__dict__}
