from django import template

register = template.Library()


@register.inclusion_tag("conreq/bootstrap_5.html")
def bootstrap_5():
    pass
