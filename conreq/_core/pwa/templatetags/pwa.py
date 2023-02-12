import functools
import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from conreq._core.pwa.apps import PwaConfig

register = template.Library()


@register.filter(is_safe=True)
def jsonify(obj):
    """Transform a python object so it can be safely used in javascript/JSON."""
    if isinstance(obj, str):
        json_val = functools.cache(json.dumps)(obj, cls=DjangoJSONEncoder)
    else:
        json_val = json.dumps(obj, cls=DjangoJSONEncoder)
    return mark_safe(json_val)


@register.inclusion_tag("conreq/pwa.html", takes_context=True)
def pwa_head_content(context):
    # pylint: disable=unused-argument
    return {"pwa": PwaConfig.__dict__}
